"""Agrega o CSV bruto de sondagens em janelas por hora e extrai features temporais.

Uso:
    python aggregate.py --input ../dados/probes.csv --output ../dados/hourly.csv
"""

import argparse

import pandas as pd

DIAS_SEMANA_PT = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]


def load_raw(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["timestamp"])
    df["timestamp"] = df["timestamp"].dt.tz_convert(None)
    return df


def aggregate_hourly(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["hora_janela"] = df["timestamp"].dt.floor("h")

    hourly = (
        df.groupby(["target", "hora_janela"])
        .agg(
            rtt_avg_ms=("rtt_avg_ms", "mean"),
            rtt_stdev_ms=("rtt_stdev_ms", "mean"),
            jitter_ms=("jitter_ms", "mean"),
            loss_pct=("loss_pct", "mean"),
            rtt_max_ms=("rtt_max_ms", "max"),
            n_coletas=("timestamp", "count"),
        )
        .reset_index()
    )

    hourly["hora_dia"] = hourly["hora_janela"].dt.hour
    hourly["dia_semana"] = hourly["hora_janela"].dt.dayofweek.map(lambda i: DIAS_SEMANA_PT[i])
    hourly["horario_pico"] = hourly["hora_dia"].between(19, 22)

    return hourly.sort_values(["target", "hora_janela"]).reset_index(drop=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default="../dados/probes.csv")
    parser.add_argument("--output", default="../dados/hourly.csv")
    args = parser.parse_args()

    raw = load_raw(args.input)
    hourly = aggregate_hourly(raw)
    hourly.to_csv(args.output, index=False)
    print(f"{len(raw)} coletas brutas -> {len(hourly)} janelas horárias em {args.output}")


if __name__ == "__main__":
    main()
