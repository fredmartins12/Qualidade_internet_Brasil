# Roteiro da Prévia (5 minutos)

Qualidade de Internet no Brasil com Dados Abertos (Anatel) — 25/Nov/2026

**Regra de ouro:** 5 minutos é pouco. Só 1 ou 2 pessoas falam. Sugestão: uma pessoa narra os slides 1-5 e 7,
e outra (ou a mesma) conduz a demonstração ao vivo no slide 6, já com o terminal aberto de antemão.

Tempo total alvo: **~4min50 a 5min**, com folga pra imprevisto na demo.

---

## Slide 1 — Capa (15s)

> "Boa tarde. Nosso projeto é sobre qualidade de internet no Brasil usando dados abertos da Anatel.
> Somos [nomes da equipe], orientados pelo professor Iguatemi."

---

## Slide 2 — Motivação (35s)

> "A internet já chegou em 95% dos domicílios brasileiros, segundo o IBGE. Mas ter acesso não é a mesma
> coisa que ter uma conexão boa — os próprios dados do CGI.br mostram que a qualidade continua desigual.
> Isso levanta a pergunta que guia o projeto: dá pra medir essa qualidade na prática, e identificar
> quando e por que ela piora?"

---

## Slide 3 — Objetivo (40s)

> "Nosso objetivo geral é desenvolver uma metodologia de coleta, análise e — se der tempo — previsão da
> qualidade da conexão, comparando com dados públicos. Pra isso, dividimos em objetivos específicos:
> coletar métricas de rede direto na fonte, organizar esses dados, visualizar os padrões, detectar
> degradação, e comparar com indicadores públicos como os da Anatel."

---

## Slide 4 — Arquitetura em 5 etapas (45s)

> "O pipeline tem 5 etapas: coleta via ICMP, usando a biblioteca Scapy; agregação dos dados em janelas
> por hora; visualização dos padrões; um detector de degradação; e por fim a comparação com dados
> públicos. Vale destacar que essa coleta é uma extensão do ICMP Pinger Lab, um dos trabalhos de
> programação oficiais do livro-texto do Kurose & Ross — usamos o Scapy pra conseguir escalar a coleta
> pra múltiplos alvos e milhares de amostras, em vez de reimplementar o protocolo byte a byte."

*(Se o professor perguntar "por que não fizeram o socket raw na mão?": essa é a resposta — decisão
consciente de engenharia, não atalho.)*

---

## Slide 5 — Onde estamos (35s)

> "Até agora já temos: o script de coleta funcionando, capturando RTT, desvio-padrão, jitter e perda de
> pacotes via ICMP; a coleta rodando em loop contínuo, sem precisar de privilégio de administrador; o
> script de agregação horária implementado e testado; e o repositório no GitHub organizado. O que falta
> é a visualização, o detector de degradação e a comparação com os dados públicos — previstos pra
> apresentação final."

---

## Slide 6 — Demonstração ao vivo (80-90s)

**Preparação antes de começar a falar:** já deixar um terminal aberto, dentro da pasta `coleta`, com o
comando digitado (mas não executado ainda).

> "Vamos mostrar a coleta rodando agora, ao vivo."

Comando a rodar na hora:
```
python probe.py --targets 8.8.8.8 1.1.1.1 --count 20
```

> "Aqui o script está enviando pacotes ICMP de verdade pro Google e pro Cloudflare, e calculando RTT
> médio, desvio-padrão, jitter e perda de pacotes em tempo real."

*(Enquanto roda — leva uns 2-3 segundos — pode já ir falando a próxima frase, ou esperar o resultado
aparecer e comentar os números específicos.)*

> "Essas linhas vão sendo salvas num CSV, que depois alimenta o script de agregação por hora — é essa
> base de dados que vamos usar na análise e no modelo da apresentação final."

Opcional, se sobrar tempo: abrir rapidamente o `dados/probes.csv` e mostrar as linhas acumuladas.

---

## Slide 7 — Próximos passos (25s)

> "Pros próximos passos até a apresentação final: visualização dos dados coletados, um detector de
> degradação baseado em limiar estatístico, e a comparação com os dados da Anatel — e se sobrar tempo,
> também do SIMET. A apresentação final é dia 7 de dezembro, com demonstração prática obrigatória.
> Obrigado."

---

## Perguntas prováveis do professor (e respostas prontas)

| Pergunta | Resposta curta |
|---|---|
| Por que usar Scapy em vez de socket raw puro? | É extensão do ICMP Pinger Lab do livro-texto; Scapy permite escalar pra múltiplos alvos e milhares de amostras sem reimplementar o protocolo byte a byte. |
| Por que ICMP e não TCP/UDP? | ICMP é o protocolo padrão de diagnóstico de rede (é o que o `ping` usa) e é o que o próprio lab do livro trabalha. |
| Como vão garantir que a comparação com Anatel/SIMET é justa? | Anatel é o plano principal (dados abertos confirmados, baixáveis em CSV); SIMET é complementar, condicionado a uma resposta deles sobre acesso a dado bruto. |
| Quantas máquinas estão coletando? | [responder com o número real de integrantes que já estão coletando no momento] |
| O que é jitter, tecnicamente? | Variação média entre RTTs consecutivos — mede estabilidade da conexão, não só velocidade. |
