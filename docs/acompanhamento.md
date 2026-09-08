# Acompanhamento — Projeto 1 | Tema 3

**Tema:** Demografia e Registro Civil  
**Problema:** compreender como estrutura etária, nascimentos e óbitos evidenciam mudanças demográficas nos municípios do Ceará.

## 1. Perguntas de análise
- Como evoluíram nascimentos, óbitos e saldo natural entre 2014 e 2024?
- Como se distribui a população por idade em 2022?
- Quais municípios apresentam maior índice de envelhecimento?
- Como mudou a distribuição da idade materna?
- Existe associação descritiva entre envelhecimento e mortalidade em 2024?

## 2. Inventário
| Tabela | Período | Granularidade usada | Unidade |
|---|---|---|---|
| 9514 | 2022 | município × sexo × idade | pessoas |
| 2612 | 2014–2024 | município × ano × dimensões de nascimento | nascimentos |
| 2654 | 2014–2024 | município × ano × dimensões de óbito | óbitos |
| 6579 | 2014–2021 e 2024 | município × ano | pessoas |

## 3. Qualidade e tratamento
Os arquivos raw foram preservados. As dimensões foram filtradas para `Total` quando o objetivo era obter o total municipal. Valores foram convertidos numericamente somente após a seleção das categorias. Os símbolos especiais do SIDRA não são convertidos silenciosamente em zero; devem ser tratados segundo a documentação da tabela.

## 4. Integração
A tabela analítica `demografia_anual_municipal.csv` integra nascimentos, óbitos e população estimada pela chave `cod_ibge + ano`. A granularidade final é município-ano. Foram encontradas 184 municipalidades no conjunto de nascimentos/óbitos. O denominador de população não existe no pacote para 2022 e 2023; portanto as taxas ficam indisponíveis nesses anos.

## 5. Visualizações preliminares
1. Série temporal de nascimentos, óbitos e saldo natural.
2. Distribuição 0–14, 15–59 e 60+ em 2022.
3. Ranking do índice de envelhecimento.
4. Evolução da participação por idade materna.
5. Dispersão entre índice de envelhecimento e mortalidade em 2024.

## 6. Insights preliminares
- Nascimentos no Ceará diminuíram de 124.114 em 2014 para 104.290 em 2024.
- A natalidade caiu de 14,04 para 11,29 por mil.
- A mortalidade estadual passou de 5,55 para 6,56 por mil; o pico ocorreu em 2021, com 7,63 por mil.
- A participação de mães de 15–19 anos caiu de 18,93% para 10,89% entre 2014 e 2024.
- São João do Jaguaribe apresentou o maior índice de envelhecimento do recorte de 2022, cerca de 171,8 idosos para cada 100 jovens de 0–14 anos.

## 7. Limitações
Eventos registrados podem estar sujeitos a sub-registro. O saldo natural não incorpora migração. Taxas brutas dependem da estrutura etária. O pacote não fornece população municipal de 2023. As associações entre indicadores são exploratórias e não causais.
