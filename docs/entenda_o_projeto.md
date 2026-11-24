# Entenda o Projeto — Guia de Estudo

Este documento existe pra você (e o resto do grupo) conseguir explicar o projeto com segurança,
responder perguntas do professor, e principalmente **entender o porquê** de cada decisão — não só
decorar o roteiro da apresentação. Vai do zero: assume que você não sabe nada de redes ainda.

---

## 1. Conceitos de rede que você precisa saber

### 1.1 O que é um pacote

Quando dois computadores "conversam" pela internet, eles não trocam um fluxo contínuo de dados — eles
trocam **pacotes**: pequenos blocos de informação, cada um com um "envelope" (cabeçalho) dizendo de onde
veio, pra onde vai, e o que tem dentro. É como mandar uma carta pelo correio: o envelope tem remetente,
destinatário, e dentro vai o conteúdo.

### 1.2 O que é ICMP e o `ping`

**ICMP** (Internet Control Message Protocol) é um protocolo criado especificamente para **diagnóstico de
rede** — não carrega "conteúdo útil" como um vídeo ou uma página web, ele serve só pra perguntar "você
está aí?" e receber "sim, estou, levei X milissegundos pra responder".

O comando `ping`, que você provavelmente já usou ou ouviu falar, funciona exatamente assim:

1. Seu computador manda um pacote ICMP do tipo **Echo Request** ("você está aí?") pra um servidor.
2. O servidor responde com um ICMP **Echo Reply** ("sim, estou aqui"), ecoando os mesmos dados que recebeu.
3. Seu computador mede quanto tempo levou entre mandar e receber a resposta.

É literalmente isso que o nosso `probe.py` faz — só que de forma programática, em massa, salvando os
resultados, em vez de você digitar `ping google.com` manualmente.

### 1.3 As três métricas que medimos

| Métrica | O que é | Analogia |
|---|---|---|
| **RTT (latência)** | Tempo entre mandar o Echo Request e receber o Echo Reply, em milissegundos | Tempo entre você perguntar algo e a pessoa responder |
| **Jitter** | O quanto o RTT varia de um pacote pro outro | Se a pessoa às vezes responde na hora e às vezes demora muito, mesmo em média sendo rápida |
| **Perda de pacotes** | % de pacotes que você mandou e nunca recebeu resposta | Perguntas que ficaram "no vácuo" |

**Por que essas três, e não só "velocidade"?** Porque uma conexão pode ter velocidade de download boa
(você baixa um arquivo grande rápido) e ainda assim ser ruim pra videochamada ou jogo online, se o jitter
for alto ou a perda de pacotes for grande — é justamente isso que os dados do CGI.br mostravam quando
falavam em "qualidade desigual" mesmo com acesso quase universal.

---

## 2. Por que isso é tecnicamente difícil (e por que precisa de Scapy/Npcap)

### 2.1 Sockets normais vs. sockets brutos (raw sockets)

Quando um programa comum (seu navegador, por exemplo) manda dados pela rede, ele usa o que se chama
**socket**: uma interface que o sistema operacional oferece, onde você só diz "manda isso pra esse
endereço" e o próprio Windows/Linux monta todo o cabeçalho do pacote por trás dos panos, de forma segura.

Só que pra mandar um pacote **ICMP Echo Request** (o "ping"), ou pra inspecionar pacotes byte a byte, você
precisa de um **socket bruto (raw socket)** — onde VOCÊ monta o pacote inteiro, cabeçalho incluso, igual
um carteiro que em vez de só entregar a carta, também escreve o envelope do zero.

Isso é poderoso, mas perigoso (dá pra forjar pacotes, fazer varreduras de rede, etc.), então os sistemas
operacionais **restringem esse poder a processos com privilégio de administrador**. É por isso que, sem o
Npcap, nosso script exigia rodar como admin.

### 2.2 O que é o Scapy

**Scapy** é uma biblioteca Python que faz exatamente esse trabalho de "montar o pacote na mão" por você —
ela sabe construir o cabeçalho ICMP (tipo, código, checksum, etc.) e cuidar de mandar/receber, então o
nosso código só precisa dizer `IP(dst=alvo)/ICMP()` e o Scapy monta tudo.

### 2.3 O que é o Npcap (e por que resolveu nosso problema de admin)

**Npcap** é um driver pro Windows (sucessor do antigo WinPcap) que dá acesso de baixo nível à placa de
rede de um jeito mais seguro e controlado que o acesso "nativo" do Windows. Quando o Scapy usa o Npcap em
vez do socket nativo do Windows, ele consegue mandar e receber pacotes **sem precisar de admin total** —
foi exatamente isso que resolveu o bug que tivemos (o script "funcionava" mas não gerava dado nenhum
quando rodava via Agendador de Tarefas, porque o Windows bloqueava silenciosamente o socket nativo).

---

## 3. A base teórica acadêmica do projeto

### 3.1 O ICMP Pinger Lab

O site oficial do livro-texto da disciplina (Kurose & Ross, *Redes de Computadores e a Internet*) lista
três trabalhos de programação oficiais, e um deles é o **ICMP Pinger Lab**: o exercício pede exatamente
pra você implementar seu próprio "ping" em Python, manualmente, usando socket bruto.

**O nosso projeto é uma extensão direta desse lab.** A diferença é que o lab oficial pede pra montar o
cabeçalho ICMP byte a byte na mão (campo "tipo", "código", calcular o checksum, etc.), e nós usamos o
Scapy pra fazer essa parte, porque nosso foco não é provar que sabemos montar um cabeçalho ICMP — é
**escalar a coleta** (múltiplos alvos, rodando continuamente, milhares de amostras) e fazer análise de
dados em cima disso. Isso é uma decisão de engenharia válida, não um atalho pra fugir do trabalho difícil.

### 3.2 Se o professor perguntar "por que não fizeram na mão?"

Essa é literalmente a resposta do parágrafo acima. Vale até mostrar que vocês conhecem o que tem "por
baixo": o cabeçalho ICMP tem os campos **Type** (8 = Echo Request, 0 = Echo Reply), **Code**, **Checksum**
(verificação de erro), **Identifier** e **Sequence Number** (pra casar pergunta com resposta). O Scapy
preenche tudo isso automaticamente quando você escreve `ICMP()`.

---

## 4. Nossa arquitetura, passo a passo (o porquê de cada peça)

```
1. COLETA  →  2. AGREGAÇÃO  →  3. VISUALIZAÇÃO  →  4. DETECÇÃO  →  5. COMPARAÇÃO
(probe.py)    (aggregate.py)    (pendente)         (pendente)      (pendente)
```

### 4.1 Coleta (`probe.py`) — já pronto e funcionando

O script manda um Echo Request pra cada alvo (Google `8.8.8.8` e Cloudflare `1.1.1.1`), repete várias
vezes seguidas (padrão: 20 vezes), e no final calcula:

- **Quantos pacotes voltaram** → vira a métrica de perda
- **Qual foi o tempo de ida-e-volta de cada um** → vira RTT médio, mínimo, máximo e desvio-padrão
- **Quanto o RTT variou entre um pacote e o próximo** → vira o jitter

Tudo isso é salvo numa linha de um arquivo CSV (uma planilha), com data e hora.

**Por que rodar em loop, de 15 em 15 minutos, por vários dias?** Porque a pergunta central do projeto é
"a qualidade da conexão muda dependendo do horário?" — isso só dá pra responder com um **histórico**, não
com uma medição única. Uma medição isolada só diz "agora está bom ou ruim"; muitas medições ao longo do
tempo dizem "costuma piorar às 20h" ou "não tem padrão nenhum".

### 4.2 Agregação (`aggregate.py`) — já pronto e testado

Com centenas de linhas no CSV (uma a cada 15 min), fica difícil enxergar padrão olhando linha por linha.
Esse script agrupa as medições **por hora do dia**, calculando a média de RTT/jitter/perda naquela hora, e
adiciona informações extras que vão ajudar a análise depois:

- `hora_dia`: 0 a 23 (em que hora do dia foi aquela medição)
- `dia_semana`: segunda, terça, etc.
- `horario_pico`: verdadeiro/falso, se foi entre 19h e 22h

Isso transforma "um monte de números soltos" em algo que dá pra comparar — por exemplo, "a média de RTT
às 20h é maior que a média às 10h?".

### 4.3 O que ainda falta (e por quê)

- **Visualização**: gráficos mostrando RTT/jitter/perda ao longo do dia — é a forma mais simples de
  "enxergar" se existe um padrão, antes de qualquer modelo mais sofisticado.
- **Detecção de degradação**: em vez de um modelo de machine learning complexo, a ideia é algo simples e
  confiável — por exemplo, calcular a média móvel do RTT e marcar como "degradado" quando um valor foge
  muito da média (um "limiar estatístico"). Isso é mais fácil de explicar, de confiar no resultado, e de
  demonstrar ao vivo do que um modelo de previsão complexo.
- **Comparação com dados públicos**: confrontar nossa média de RTT/qualidade com os indicadores da Anatel
  (plano principal, dados já confirmados como baixáveis) e do SIMET/NIC.br (complementar, se eles
  responderem sobre acesso a dado bruto) — serve pra dizer "nossa medição bate com o cenário nacional?"

---

## 5. Glossário rápido (consulta durante perguntas)

| Termo | Definição em uma frase |
|---|---|
| **ICMP** | Protocolo usado só para diagnóstico de rede (é o que o `ping` usa) |
| **RTT** | Tempo de ida e volta de um pacote (latência) |
| **Jitter** | Variação do RTT entre pacotes consecutivos |
| **Perda de pacotes** | % de pacotes que não tiveram resposta |
| **Socket** | Interface que um programa usa pra mandar/receber dados pela rede |
| **Raw socket** | Socket de baixo nível onde você monta o pacote inteiro manualmente |
| **Scapy** | Biblioteca Python que monta e envia pacotes de rede |
| **Npcap** | Driver do Windows que permite capturar/enviar pacotes sem precisar de admin total |
| **Desvio-padrão (stdev)** | O quanto os valores de RTT, em média, se afastam da média geral |
| **Dados abertos** | Dados públicos disponibilizados por órgãos (Anatel, IBGE, etc.) para qualquer um consultar |

---

## 6. Perguntas que o professor pode fazer — e como responder

**"Por que ICMP e não TCP/UDP?"**
ICMP é o protocolo padrão de diagnóstico (é o que o `ping` usa), e é literalmente o que o ICMP Pinger Lab
do livro trabalha — faz sentido como ponto de partida pra medir qualidade de conexão.

**"Scapy não é meio 'fazer tudo por você'? Vocês entendem o que tá por baixo?"**
Sim — o cabeçalho ICMP tem Type, Code, Checksum, Identifier e Sequence Number; o Scapy só preenche isso
automaticamente. Decidimos usar porque o foco do projeto é escalar a coleta e fazer análise de dados, não
reimplementar o protocolo byte a byte.

**"Por que medir de 15 em 15 minutos e não só uma vez?"**
Porque a pergunta de pesquisa é sobre variação ao longo do tempo (ex: horário de pico), e isso só aparece
com uma série histórica de medições, não com uma medição isolada.

**"O que vocês fazem se a conexão cair de vez (perda 100%)?"**
O script registra isso normalmente: a linha fica com `loss_pct = 100` e RTT vazio — é um dado válido
(significa "rede fora do ar naquele momento"), não um erro.

**"Qual a diferença entre jitter e desvio-padrão, já que os dois 'medem variação'?"**
Desvio-padrão olha a dispersão de **todos** os valores em torno da média. Jitter olha a diferença entre
**cada par de medições consecutivas** — é mais sensível a oscilações rápidas, momento a momento.
