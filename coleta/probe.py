"""Sondagem ativa de latencia, jitter e perda de pacotes via ICMP (Scapy).

Requer privilegios de administrador (raw sockets) e Npcap instalado no Windows.
Uso:
    python probe.py --targets 8.8.8.8 1.1.1.1 --count 20 --output ../dados/probes.csv
"""

import argparse
import csv
import os
import statistics
from datetime import datetime, timezone

from scapy.all import ICMP, IP, sr1

DEFAULT_TARGETS = ["8.8.8.8", "1.1.1.1"]
CSV_FIELDS = [
    "timestamp",
    "target",
    "samples_sent",
    "samples_received",
    "loss_pct",
    "rtt_avg_ms",
    "rtt_min_ms",
    "rtt_max_ms",
    "rtt_stdev_ms",
    "jitter_ms",
]


def send_probes(target: str, count: int, timeout: float) -> list[float]:
    rtts = []
    for _ in range(count):
        packet = IP(dst=target) / ICMP()
        sent_at = datetime.now()
        reply = sr1(packet, timeout=timeout, verbose=0)
        if reply is not None:
            rtt_ms = (datetime.now() - sent_at).total_seconds() * 1000
            rtts.append(rtt_ms)
    return rtts


def compute_jitter(rtts: list[float]) -> float:
    if len(rtts) < 2:
        return 0.0
    diffs = [abs(rtts[i] - rtts[i - 1]) for i in range(1, len(rtts))]
    return statistics.mean(diffs)


def build_row(target: str, count: int, rtts: list[float]) -> dict:
    received = len(rtts)
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "target": target,
        "samples_sent": count,
        "samples_received": received,
        "loss_pct": round((count - received) / count * 100, 2),
        "rtt_avg_ms": round(statistics.mean(rtts), 2) if rtts else None,
        "rtt_min_ms": round(min(rtts), 2) if rtts else None,
        "rtt_max_ms": round(max(rtts), 2) if rtts else None,
        "rtt_stdev_ms": round(statistics.stdev(rtts), 2) if len(rtts) > 1 else None,
        "jitter_ms": round(compute_jitter(rtts), 2) if rtts else None,
    }


def append_to_csv(path: str, row: dict) -> None:
    file_exists = os.path.isfile(path)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--targets", nargs="+", default=DEFAULT_TARGETS)
    parser.add_argument("--count", type=int, default=20, help="pacotes por alvo")
    parser.add_argument("--timeout", type=float, default=1.0, help="timeout por pacote (s)")
    parser.add_argument("--output", default="../dados/probes.csv")
    args = parser.parse_args()

    for target in args.targets:
        rtts = send_probes(target, args.count, args.timeout)
        row = build_row(target, args.count, rtts)
        append_to_csv(args.output, row)
        print(f"{row['timestamp']} {target}: "
              f"avg={row['rtt_avg_ms']}ms stdev={row['rtt_stdev_ms']}ms "
              f"jitter={row['jitter_ms']}ms loss={row['loss_pct']}%")


if __name__ == "__main__":
    main()
