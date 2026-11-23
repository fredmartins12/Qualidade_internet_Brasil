# 1. Introdução

## 1.1 Contextualização

Nas últimas duas décadas, o acesso à internet no Brasil passou por uma expansão expressiva. Segundo a Pesquisa Nacional por Amostra de Domicílios Contínua (PNAD Contínua TIC), do IBGE, em 2025 a internet já estava presente em 95,0% dos domicílios brasileiros — cerca de 76 milhões de residências —, com a conexão por banda larga fixa (89,2%) superando a banda larga móvel (85,9%) como principal forma de acesso (IBGE, 2025). De forma complementar, a pesquisa TIC Domicílios 2025, do Centro Regional de Estudos para o Desenvolvimento da Sociedade da Informação (Cetic.br/CGI.br), aponta que 86% dos domicílios possuem acesso à rede, totalizando 157 milhões de usuários de internet no país, o equivalente a 85% da população (CGI.br, 2025).

Apesar da quase universalização do acesso, as próprias pesquisas do CGI.br destacam que **a qualidade desse acesso permanece desigual**: enquanto famílias de classe A têm conectividade praticamente plena, as classes D e E ainda enfrentam limitações significativas, tanto em disponibilidade quanto em desempenho da conexão (CGI.br, 2025). Esse cenário evidencia que medir apenas a presença ou ausência de internet não é suficiente para compreender a experiência real do usuário brasileiro: é necessário avaliar métricas técnicas de qualidade de serviço (QoS), como latência, variação de latência (jitter) e perda de pacotes, que impactam diretamente aplicações sensíveis a tempo real — chamadas de vídeo, jogos online, VoIP e serviços em nuvem.

Órgãos como a Agência Nacional de Telecomunicações (Anatel) e o Núcleo de Informação e Coordenação do Ponto BR (NIC.br), por meio do Sistema de Medição de Tráfego da Internet (SIMET), disponibilizam dados públicos sobre o setor de telecomunicações e sobre a qualidade de conexão medida por usuários em todo o país. Esses dados abertos representam uma oportunidade valiosa para pesquisas acadêmicas, mas, por serem coletados de forma agregada e eventual, não substituem uma medição ativa, controlada e contínua, capaz de capturar variações de qualidade ao longo do dia e em diferentes condições de rede.

## 1.2 Problema

Diante desse contexto, surge a seguinte questão: **como caracterizar, de forma objetiva e quantitativa, a qualidade da conexão de internet de um usuário ao longo do tempo, e como essa caracterização se relaciona com os dados públicos de qualidade divulgados por iniciativas como o SIMET?**

A dificuldade central está em transformar métricas de rede brutas — coletadas em instantes isolados — em um panorama consistente, capaz de revelar padrões de degradação (por exemplo, piora da latência em horários de pico) e de permitir comparações justas com os indicadores oficiais do setor.

## 1.3 Justificativa

A escolha por uma abordagem de medição ativa, utilizando a biblioteca Scapy para construção e envio de pacotes de rede, se justifica pela necessidade de dados próprios, granulares e replicáveis, que não dependem exclusivamente de terceiros. Ao enviar sondas para múltiplos destinos em diferentes horários, é possível isolar problemas de rede local de problemas no destino ou na rota, algo que relatórios agregados dificilmente permitem. Complementarmente, o uso de técnicas de ciência de dados e aprendizado de máquina possibilita identificar padrões de degradação que não seriam evidentes em uma simples inspeção visual das séries temporais, além de permitir prever momentos de maior probabilidade de piora na qualidade da conexão.

Por fim, confrontar os resultados obtidos com dados públicos como os do SIMET fornece um contexto mais amplo, permitindo situar a experiência medida localmente dentro do panorama nacional de qualidade de internet.

## 1.4 Objetivos

### 1.4.1 Objetivo Geral

Desenvolver uma metodologia de coleta, análise e previsão da qualidade da conexão de internet, a partir de métricas de rede obtidas por sondagem ativa, comparando os resultados com dados públicos de qualidade disponibilizados por iniciativas como o SIMET/NIC.br e a Anatel.

### 1.4.2 Objetivos Específicos

- Implementar uma ferramenta de coleta de métricas de rede (latência, jitter e perda de pacotes) utilizando a biblioteca Scapy, com envio de sondas a múltiplos destinos em diferentes horários do dia;
- Construir um pipeline de organização e tratamento dos dados coletados, incluindo limpeza, agregação temporal e extração de features relevantes;
- Aplicar técnicas de visualização de dados para identificar padrões de variação da qualidade da conexão ao longo do tempo;
- Utilizar técnicas de aprendizado de máquina para identificar padrões de degradação da conexão e estimar a probabilidade de piora da qualidade em diferentes janelas de tempo;
- Comparar os resultados obtidos com dados públicos de qualidade de internet (SIMET e/ou Anatel), discutindo convergências e limitações entre a medição local e os indicadores nacionais.

## 1.5 Estrutura do Trabalho

Este trabalho está organizado da seguinte forma: a Seção 2 apresenta a fundamentação teórica sobre métricas de qualidade de rede e os conceitos técnicos utilizados; a Seção 3 descreve a metodologia de coleta de dados com Scapy e o pipeline de processamento; a Seção 4 detalha a abordagem de análise de dados e aprendizado de máquina aplicada; a Seção 5 apresenta os resultados obtidos e a comparação com os dados públicos do SIMET; por fim, a Seção 6 traz as considerações finais e sugestões para trabalhos futuros.

---

## Referências (preliminares, formato a ajustar conforme norma da disciplina)

- IBGE. **PNAD Contínua TIC 2025**: Internet chega a 95% de domicílios do país em 2025. Agência de Notícias IBGE, 2025. Disponível em: https://agenciadenoticias.ibge.gov.br/agencia-noticias/2012-agencia-de-noticias/noticias/47410-internet-chega-a-95-de-domicilios-do-pais-em-2025
- CGI.br / Cetic.br. **TIC Domicílios 2025 — Principais Resultados**. Disponível em: https://cetic.br/pt/pesquisa/domicilios/indicadores/
- NIC.br. **Medições — SIMET**. Disponível em: https://medicoes.nic.br/
- ANATEL. **Dados Abertos**. Disponível em: https://www.gov.br/anatel/pt-br/dados/dados-abertos
