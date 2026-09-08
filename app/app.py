import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
ANA = ROOT/"dados"/"analytical"
PROC = ROOT/"dados"/"processed"
RAW = ROOT/"dados"/"raw"

st.set_page_config(page_title="Demografia do Ceará", page_icon="📊", layout="wide")
st.title("Demografia e Registro Civil dos municípios do Ceará")
st.caption("Projeto aplicado — IBGE/SIDRA | Tema 3")

annual = pd.read_csv(ANA/"demografia_anual_municipal.csv")
age = pd.read_csv(ANA/"estrutura_etaria_2022.csv")
maternal = pd.read_csv(PROC/"nascimentos_idade_mae.csv")

municipios = sorted(annual["municipio"].dropna().unique())
sel = st.sidebar.selectbox("Município", ["Todos"] + municipios)
ano_min, ano_max = int(annual.ano.min()), int(annual.ano.max())
years = st.sidebar.slider("Período", ano_min, ano_max, (ano_min, ano_max))
d = annual[(annual.ano.between(years[0], years[1])) & ((annual.municipio==sel) if sel!="Todos" else True)].copy()

st.info("As taxas por mil usam a população estimada em 2014–2021 e 2024. O pacote não contém denominador municipal de 2023; por isso 2022–2023 aparecem sem taxa.")
latest_year = 2024 if 2024 in d.ano.unique() else int(d.ano.max())
latest = d[d.ano==latest_year]
if sel=="Todos":
    births = latest.nascimentos.sum()
    deaths = latest.obitos.sum()
    pop = latest.populacao.sum()
    nat = births/pop*1000 if pop else None
    mort = deaths/pop*1000 if pop else None
else:
    row = latest[latest.municipio==sel]
    births = row.nascimentos.iloc[0] if len(row) else 0
    deaths = row.obitos.iloc[0] if len(row) else 0
    pop = row.populacao.iloc[0] if len(row) else 0
    nat = row.natalidade_por_mil.iloc[0] if len(row) else None
    mort = row.mortalidade_por_mil.iloc[0] if len(row) else None

c1,c2,c3,c4 = st.columns(4)
c1.metric(f"Nascimentos ({latest_year})", f"{births:,.0f}".replace(",",".")) 
c2.metric(f"Óbitos ({latest_year})", f"{deaths:,.0f}".replace(",",".")) 
c3.metric("Natalidade / mil", "—" if pd.isna(nat) else f"{nat:.2f}")
c4.metric("Mortalidade / mil", "—" if pd.isna(mort) else f"{mort:.2f}")

st.subheader("1. Evolução de nascimentos, óbitos e saldo natural")
if sel=="Todos":
    trend=d.groupby("ano",as_index=False)[["nascimentos","obitos","saldo_natural"]].sum()
else:
    trend=d.groupby("ano",as_index=False)[["nascimentos","obitos","saldo_natural"]].sum()
fig=px.line(trend,x="ano",y=["nascimentos","obitos","saldo_natural"],markers=True,
            labels={"value":"Eventos","variable":"Indicador","ano":"Ano"})
st.plotly_chart(fig,use_container_width=True)

st.subheader("2. Estrutura etária — Censo 2022")
ae=age.copy()
if sel!="Todos": ae=ae[ae.municipio==sel]
else:
    ae=pd.DataFrame([{"grupo":"0-14","populacao":age["0-14"].sum()},
                     {"grupo":"15-59","populacao":age["15-59"].sum()},
                     {"grupo":"60+","populacao":age["60+"].sum()}])
if sel!="Todos":
    ae=ae.melt(id_vars=["cod_ibge","municipio"],value_vars=["0-14","15-59","60+"],var_name="grupo",value_name="populacao")
fig2=px.bar(ae,x="grupo",y="populacao",labels={"populacao":"Pessoas","grupo":"Faixa etária"})
st.plotly_chart(fig2,use_container_width=True)

st.subheader("3. Municípios por índice de envelhecimento")
rank=age[["municipio","prop_jovens_pct","prop_idosos_pct","indice_envelhecimento"]].sort_values("indice_envelhecimento",ascending=False).head(15)
fig3=px.bar(rank.sort_values("indice_envelhecimento"),x="indice_envelhecimento",y="municipio",orientation="h",
            labels={"indice_envelhecimento":"Idosos por 100 jovens","municipio":"Município"})
st.plotly_chart(fig3,use_container_width=True)

st.subheader("4. Perfil da idade materna")
m=maternal.copy()
cats=[c for c in m.idade_mae.dropna().unique() if c not in ["Idade da mãe na ocasião do parto","Total"]]
m=m[m.idade_mae.isin(cats)]
if sel!="Todos": m=m[m.municipio==sel]
g=m.groupby(["ano","idade_mae"],as_index=False).nascimentos.sum()
tot=g.groupby("ano",as_index=False).nascimentos.sum().rename(columns={"nascimentos":"total"})
g=g.merge(tot,on="ano"); g["participacao_pct"]=g.nascimentos/g.total*100
fig4=px.line(g,x="ano",y="participacao_pct",color="idade_mae",markers=True,
             labels={"participacao_pct":"Participação (%)","idade_mae":"Idade da mãe","ano":"Ano"})
st.plotly_chart(fig4,use_container_width=True)

st.subheader("5. Cruzamento: envelhecimento × mortalidade em 2024")
x=annual[annual.ano==2024].merge(age,on=["cod_ibge","municipio"],how="inner")
fig5=px.scatter(x,x="indice_envelhecimento",y="mortalidade_por_mil",size="populacao",hover_name="municipio",
                labels={"indice_envelhecimento":"Índice de envelhecimento","mortalidade_por_mil":"Óbitos por mil habitantes"})
st.plotly_chart(fig5,use_container_width=True)

st.subheader("Fontes e metodologia")
st.markdown("""
- **Tabela 9514** — população por sexo e idade, 2022.
- **Tabela 2612** — nascidos vivos, 2014–2024.
- **Tabela 2654** — óbitos, 2014–2024.
- **Tabela 6579** — população estimada, 2014–2021 e 2024.
- Chave de integração: **código IBGE de sete dígitos do município**.
- O dashboard usa apenas arquivos estáticos versionados no repositório; não há chamadas à API do SIDRA.
- Nascimento e óbito são eventos registrados e podem estar sujeitos a sub-registro. O saldo natural não mede migração.
""")
