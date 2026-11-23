# Qualidade de Internet no Brasil com Dados Abertos (Anatel)

Trabalho de Redes de Computadores — prof. Iguatemi — UFPB, 2026.2

Mede a qualidade real da conexão de internet (latência, jitter, perda de pacotes) via sondagem ativa
com ICMP (biblioteca Scapy), organiza os dados coletados em janelas horárias e compara os resultados
com indicadores públicos de qualidade de internet no Brasil (Anatel/SIMET).

> Extensão do **ICMP Pinger Lab**, um dos trabalhos de programação oficiais do livro-texto
> Kurose & Ross — ver [`docs/guia_coleta.pdf`](docs/guia_coleta.pdf) para a justificativa completa.

## Estrutura

```
.
├── coleta/
│   ├── probe.py           # sondagem ativa (Scapy): RTT, stdev, jitter, perda de pacotes
│   └── run_probe.bat       # wrapper para rodar via Agendador de Tarefas do Windows
├── analise/
│   └── aggregate.py       # agrega probes.csv em janelas horárias + features temporais
├── dados/                  # saída da coleta (gerada localmente, não versionada)
├── docs/
│   ├── introducao.md       # Seção 1 do trabalho (contextualização, objetivos)
│   ├── guia_coleta.pdf     # passo a passo de instalação e coleta, para o grupo
│   ├── projeto_overview.pdf # visão geral do projeto + cronograma da disciplina
│   └── enunciado-oficial.pdf # especificação do professor
└── requirements.txt
```

## Como rodar a coleta

1. Instalar dependências:
   ```
   pip install -r requirements.txt
   ```
2. No Windows, instalar o [Npcap](https://npcap.com/#download) (necessário para o Scapy enviar pacotes brutos).
3. Rodar o terminal **como Administrador** (raw sockets exigem privilégio elevado) e executar:
   ```
   python coleta/probe.py --targets 8.8.8.8 1.1.1.1 --count 20 --output dados/probes.csv
   ```

Cada execução grava uma linha por alvo em `dados/probes.csv` com: timestamp (UTC), RTT médio/mín/máx,
desvio-padrão, jitter e % de perda. Passo a passo detalhado (com screenshots do Agendador de Tarefas):
[`docs/guia_coleta.pdf`](docs/guia_coleta.pdf).

## Coleta recorrente

Para capturar variação ao longo do dia, agendar execuções periódicas via **Agendador de Tarefas do
Windows**, por exemplo a cada 15 minutos, usando `coleta/run_probe.bat` — os dados se acumulam por
`append` em `dados/probes.csv`.

## Como agregar os dados

Depois de acumular algumas horas/dias de coleta:
```
python analise/aggregate.py --input dados/probes.csv --output dados/hourly.csv
```

Agrupa as coletas por **alvo + janela de hora** (média de RTT/stdev/jitter/perda) e adiciona features
temporais (`hora_dia`, `dia_semana`, `horario_pico` — flag para 19h-22h) para a etapa de análise/ML.

## Documentação do projeto

- [`docs/introducao.md`](docs/introducao.md) — contextualização, problema, objetivos
- [`docs/projeto_overview.pdf`](docs/projeto_overview.pdf) — visão geral, etapas e status atual
- [`docs/guia_coleta.pdf`](docs/guia_coleta.pdf) — guia de instalação/coleta para o grupo
- [`docs/enunciado-oficial.pdf`](docs/enunciado-oficial.pdf) — especificação da disciplina

## Próximos passos

- [ ] Coleta real rodando nas máquinas do grupo
- [ ] Visualização dos dados agregados (séries temporais por alvo)
- [ ] Detector simples de degradação (limiar estatístico)
- [ ] Comparação com dados abertos da Anatel (plano principal) e SIMET (complementar)
