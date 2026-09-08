# Caderno reproduzível — roteiro
# Execute primeiro:
# python src/preparar_dados.py
#
# Depois, em um notebook Jupyter, carregue:
import pandas as pd
annual = pd.read_csv('../dados/analytical/demografia_anual_municipal.csv')
age = pd.read_csv('../dados/analytical/estrutura_etaria_2022.csv')
maternal = pd.read_csv('../dados/processed/nascimentos_idade_mae.csv')

# Exemplo: resumo estadual
ce = annual.groupby('ano', as_index=False).agg(
    nascimentos=('nascimentos','sum'),
    obitos=('obitos','sum'),
    populacao=('populacao','sum')
)
ce['saldo_natural'] = ce.nascimentos - ce.obitos
ce['natalidade_por_mil'] = ce.nascimentos / ce.populacao * 1000
ce['mortalidade_por_mil'] = ce.obitos / ce.populacao * 1000
ce
