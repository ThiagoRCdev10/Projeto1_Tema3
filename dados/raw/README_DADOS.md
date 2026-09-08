# Equipe 03 — Demografia e Registro Civil

Este diretório contém respostas brutas da API oficial do SIDRA, preparadas para uso local pelos alunos. Não há dados limpos, cruzamentos, indicadores calculados ou conclusões analíticas.

## Arquivos

| Tabela | Arquivo(s) | Seleção |
|---|---|---|
| [9514](https://sidra.ibge.gov.br/tabela/9514) | `dados_originais/t9514_populacao_sexo_idade_2022_ce_br.csv` | População residente em 2022 por sexo e grupos quinquenais de idade |
| [2612](https://sidra.ibge.gov.br/tabela/2612) | `dados_originais/t2612_nascidos_residencia_2014_2019_ce_br.csv` e `dados_originais/t2612_nascidos_residencia_2020_2024_ce_br.csv` | Nascidos vivos ocorridos no ano, segundo residência da mãe, sexo e idade da mãe |
| [2654](https://sidra.ibge.gov.br/tabela/2654) | quatro arquivos `dados_originais/t2654_*.csv` | Óbitos ocorridos no ano, segundo residência do falecido, sexo e idade |
| [6579](https://sidra.ibge.gov.br/tabela/6579) | `dados_originais/t6579_populacao_estimada_2014_2021_2024_ce_br.csv` | População residente estimada nos anos disponíveis do recorte |

Os arquivos 2612 e 2654 foram particionados somente por período porque a API limita cada requisição a 50.000 valores. Cada parte continua sendo uma resposta original completa do SIDRA; nenhuma linha foi transformada. Para analisar toda a série, concatene as partes da mesma tabela depois da leitura.

## Territórios e formato

Todos os arquivos incluem:

- Brasil: nível `1`, código territorial `1`;
- Ceará: nível `3`, código territorial `23`;
- os 184 municípios do Ceará: nível `6`, código territorial de sete dígitos.

Os CSVs foram retornados diretamente pelo SIDRA em UTF-8, separados por ponto e vírgula. A primeira linha contém os nomes curtos das colunas (`NC`, `NN`, `D1C`, `D1N`, ..., `MC`, `MN`, `V`) e a segunda contém os rótulos descritivos. Os dados começam na terceira linha.

Leitura recomendada, preservando códigos e símbolos:

```python
import pandas as pd

df = pd.read_csv(
    "dados_originais/arquivo.csv",
    sep=";",
    header=0,
    skiprows=[1],
    dtype=str,
    keep_default_na=False,
)
```

- `NC`/`NN`: código e nome do nível territorial;
- `D1C`/`D1N`: código e nome da unidade territorial;
- demais pares `DnC`/`DnN`: código e nome da variável, ano ou classificação, na ordem descrita na segunda linha;
- `MC`/`MN`: código e nome da unidade de medida;
- `V`: valor.

Use como chave a combinação de `NC` com todas as colunas `DnC` presentes. Não converta `D1C` para número antes de preservar o código original e não faça junções por nome do município.

## Seleções concretas

### Tabela 9514

- Variável 93: População residente.
- Ano: 2022.
- Sexo: Total (6794), Homens (4), Mulheres (5).
- Idade: Total (100362); 0–4 (93070); 5–9 (93084); 10–14 (93085); 15–19 (93086); 20–24 (93087); 25–29 (93088); 30–34 (93089); 35–39 (93090); 40–44 (93091); 45–49 (93092); 50–54 (93093); 55–59 (93094); 60–64 (93095); 65–69 (93096); 70–74 (93097); 75–79 (93098); 80–84 (49108); 85–89 (49109); 90–94 (60040); 95–99 (60041); 100 anos ou mais (6653).
- Forma de declaração da idade: Total (113635).

### Tabela 2612

- Variável 218: Nascidos vivos ocorridos no ano.
- Anos: 2014 a 2024.
- Mês do nascimento, local do nascimento e número de nascidos por parto: Total (0).
- Sexo: Total (0), Homens (4), Mulheres (5), Ignorado (104539).
- Idade da mãe: Total (0), menos de 15 (5370), 15–19 (5414), 20–24 (5376), 25–29 (5382), 30–34 (5388), 35–39 (5394), 40–44 (5400), 45–49 (5406), 50 anos ou mais (5412), Ignorada (5413).

### Tabela 2654

- Variável 343: Número de óbitos ocorridos no ano.
- Anos: 2014 a 2024.
- Mês de ocorrência, natureza do óbito e local de ocorrência: Total (0).
- Sexo: Total (0), Homens (4), Mulheres (5), Ignorado (104539).
- Idade: Total (0), menos de 1 ano (5922), 1–4 (5948), 5–9 (5953), 10–14 (5959), grupos quinquenais de 15–19 (5966) a 80–84 (5979), 85 anos ou mais (5980), idade ignorada (5997).

### Tabela 6579

- Variável 9324: População residente estimada.
- Anos: 2014 a 2021 e 2024.
- Sem classificações adicionais.

## Símbolos e limitações

- O símbolo `-` significa zero absoluto no SIDRA e deve ser convertido para zero apenas na etapa de limpeza. Não foram encontrados `...`, `..` ou `X` neste pacote.
- Categorias `Total` e seus componentes coexistem nos arquivos para permitir conferência. Não some o total novamente aos componentes.
- As tabelas 2612 e 2654 usam lugar de residência, não lugar do registro.
- Totais publicados para Ceará e Brasil devem ser tratados como benchmarks próprios; registros sem município especificado podem impedir igualdade exata com a soma dos municípios.
- A tabela 6579 contém estimativas com referência em 1º de julho. O denominador de 2022 está na tabela 9514; 2023 não está disponível na seleção oficial usada. Não interpole sem documentar uma metodologia própria.
- Taxas brutas, razões ou indicadores derivados não fazem parte destes arquivos.

## Validações executadas

- HTTP 200 em todas as requisições;
- UTF-8 e esquema tabular consistente, com duas linhas de cabeçalho;
- períodos, variável e categorias exatamente iguais às seleções acima;
- Brasil, Ceará e o mesmo conjunto de 184 municípios em todos os arquivos;
- ausência de chaves duplicadas;
- Homens + Mulheres = Total na tabela 9514;
- Homens + Mulheres + Ignorado = Total nas tabelas 2612 e 2654;
- soma dos grupos etários mutuamente exclusivos = Total nas tabelas 9514, 2612 e 2654.

As URLs completas, horários, quantidades de linhas e hashes SHA-256 estão em `fontes.csv`.
