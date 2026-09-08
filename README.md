# Projeto 1 — Demografia e Registro Civil do Ceará

Projeto aplicado da disciplina de Ciência de Dados, Tema 3 — **Demografia e Registro Civil**.

## Pergunta orientadora
Como a estrutura populacional, os nascimentos e os óbitos revelam a transição demográfica dos municípios cearenses?

## Bases obrigatórias
- SIDRA 9514 — população por sexo e idade (2022)
- SIDRA 2612 — nascidos vivos (2014–2024)
- SIDRA 2654 — óbitos (2014–2024)
- SIDRA 6579 — população estimada (2014–2021 e 2024)

As bases originais estão preservadas em `dados/raw`. O tratamento gera `processed` e `analytical`.

## Estrutura
```text
projeto_demografia/
├── app/app.py
├── dados/raw/
├── dados/processed/
├── dados/analytical/
├── docs/
├── notebooks/
├── src/preparar_dados.py
├── requirements.txt
└── README.md
```

## Execução
```bash
pip install -r requirements.txt
python src/preparar_dados.py
streamlit run app/app.py
```

## Regras de integração
A integração é feita pelo código IBGE de sete dígitos do município, nunca pelo nome. A granularidade da tabela anual integrada é **município-ano**. A cardinalidade esperada é 1:1 entre cada tabela agregada nessa granularidade.

## Indicadores
- Nascimentos e óbitos anuais
- Saldo natural = nascimentos − óbitos
- Natalidade por mil = nascimentos / população × 1.000
- Mortalidade por mil = óbitos / população × 1.000
- Proporção de jovens = população 0–14 / total × 100
- Proporção de idosos = população 60+ / total × 100
- Índice de envelhecimento = população 60+ / população 0–14 × 100

## Limitações
O pacote não contém denominador municipal para 2023, então as taxas municipais desse ano não são calculadas. Eventos registrados podem estar sujeitos a sub-registro. Taxa bruta de mortalidade é influenciada pela estrutura etária. O saldo natural não mede migração. Não são feitas conclusões causais.

## Principais resultados observados
1. No Ceará, os nascimentos caíram de 124.114 em 2014 para 104.290 em 2024.
2. A taxa bruta de natalidade caiu de 14,04 para 11,29 por mil entre 2014 e 2024.
3. Em 2024, a mortalidade foi 6,56 por mil no agregado estadual, acima de 5,55 por mil em 2014.
4. Em 2022, a população de 60 anos ou mais representou cerca de 14,67% da estrutura etária municipal agregada, enquanto 0–14 anos representou cerca de 20,49%.
5. A participação de mães de 15–19 anos entre os nascimentos caiu de 18,93% em 2014 para 10,89% em 2024; grupos de 30–39 anos ganharam participação.

Os resultados são associações descritivas e não devem ser interpretados como causalidade.
