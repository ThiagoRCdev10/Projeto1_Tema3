import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "dados" / "raw"
PROC = ROOT / "dados" / "processed"
ANA = ROOT / "dados" / "analytical"
PROC.mkdir(parents=True, exist_ok=True)
ANA.mkdir(parents=True, exist_ok=True)

def read_csv(path):
    return pd.read_csv(path, sep=None, engine="python", dtype=str)

def only_municipalities(df):
    return df[df["D1C"].str.fullmatch(r"\d{7}", na=False)].copy()

def total_dimensions(df, cols):
    for c in cols:
        df = df[df[c].str.lower().eq("total")]
    return df.copy()

def main():
    births = pd.concat([read_csv(RAW / "t2612_nascidos_residencia_2014_2019_ce_br.csv"),
                        read_csv(RAW / "t2612_nascidos_residencia_2020_2024_ce_br.csv")], ignore_index=True)
    deaths = pd.concat([read_csv(RAW / "t2654_obitos_residencia_2014_2016_ce_br.csv"),
                        read_csv(RAW / "t2654_obitos_residencia_2017_2019_ce_br.csv"),
                        read_csv(RAW / "t2654_obitos_residencia_2020_2022_ce_br.csv"),
                        read_csv(RAW / "t2654_obitos_residencia_2023_2024_ce_br.csv")], ignore_index=True)
    pop = read_csv(RAW / "t6579_populacao_estimada_2014_2021_2024_ce_br.csv")
    age = read_csv(RAW / "t9514_populacao_sexo_idade_2022_ce_br.csv")

    births = only_municipalities(births)
    deaths = only_municipalities(deaths)
    pop = only_municipalities(pop)
    age = only_municipalities(age)

    b_total = total_dimensions(births, ["D4N","D5N","D6N","D7N","D8N"])
    d_total = total_dimensions(deaths, ["D4N","D5N","D6N","D7N","D8N"])
    b = b_total[["D1C","D1N","D3N","V"]].rename(columns={"D1C":"cod_ibge","D1N":"municipio","D3N":"ano","V":"nascimentos"})
    d = d_total[["D1C","D1N","D3N","V"]].rename(columns={"D1C":"cod_ibge","D1N":"municipio","D3N":"ano","V":"obitos"})
    p = pop[["D1C","D1N","D3N","V"]].rename(columns={"D1C":"cod_ibge","D1N":"municipio","D3N":"ano","V":"populacao"})
    for df, col in [(b,"nascimentos"),(d,"obitos"),(p,"populacao")]:
        df["ano"] = pd.to_numeric(df["ano"], errors="coerce")
        df[col] = pd.to_numeric(df[col], errors="coerce")

    annual = b.merge(d[["cod_ibge","ano","obitos"]], on=["cod_ibge","ano"], how="outer")
    annual = annual.merge(p[["cod_ibge","ano","populacao"]], on=["cod_ibge","ano"], how="left")
    annual["saldo_natural"] = annual["nascimentos"] - annual["obitos"]
    annual["natalidade_por_mil"] = annual["nascimentos"] / annual["populacao"] * 1000
    annual["mortalidade_por_mil"] = annual["obitos"] / annual["populacao"] * 1000
    annual["crescimento_natural_por_mil"] = annual["saldo_natural"] / annual["populacao"] * 1000
    annual.to_csv(ANA/"demografia_anual_municipal.csv", index=False)

    a = total_dimensions(age, ["D4N","D6N"])
    a = a[["D1C","D1N","D4N","D5N","V"]].rename(columns={"D1C":"cod_ibge","D1N":"municipio","D4N":"sexo","D5N":"idade","V":"populacao"})
    a["populacao"] = pd.to_numeric(a["populacao"], errors="coerce")
    a.to_csv(PROC/"populacao_sexo_idade_2022.csv", index=False)

    age_groups = {
        "0-14": ["0 a 4 anos","5 a 9 anos","10 a 14 anos"],
        "15-59": ["15 a 19 anos","20 a 24 anos","25 a 29 anos","30 a 34 anos","35 a 39 anos","40 a 44 anos","45 a 49 anos","50 a 54 anos","55 a 59 anos"],
        "60+": ["60 a 64 anos","65 a 69 anos","70 a 74 anos","75 a 79 anos","80 a 84 anos","85 a 89 anos","90 a 94 anos","95 a 99 anos","100 anos ou mais"]
    }
    aa = a[a["idade"].isin(sum(age_groups.values(), []))].copy()
    inv = {v:k for k,vals in age_groups.items() for v in vals}
    aa["grupo"] = aa["idade"].map(inv)
    summary = aa.groupby(["cod_ibge","municipio","grupo"], as_index=False)["populacao"].sum()
    wide = summary.pivot(index=["cod_ibge","municipio"], columns="grupo", values="populacao").reset_index().fillna(0)
    for c in ["0-14","15-59","60+"]:
        if c not in wide: wide[c]=0
    wide["total"] = wide[["0-14","15-59","60+"]].sum(axis=1)
    wide["prop_jovens_pct"] = wide["0-14"]/wide["total"]*100
    wide["prop_idosos_pct"] = wide["60+"]/wide["total"]*100
    wide["indice_envelhecimento"] = wide["60+"]/wide["0-14"]*100
    wide.to_csv(ANA/"estrutura_etaria_2022.csv", index=False)

    bm = total_dimensions(births, ["D4N","D5N","D6N","D7N"])
    bm = bm[["D1C","D1N","D3N","D8N","V"]].rename(columns={"D1C":"cod_ibge","D1N":"municipio","D3N":"ano","D8N":"idade_mae","V":"nascimentos"})
    bm["ano"] = pd.to_numeric(bm["ano"], errors="coerce")
    bm["nascimentos"] = pd.to_numeric(bm["nascimentos"], errors="coerce")
    bm.to_csv(PROC/"nascimentos_idade_mae.csv", index=False)

if __name__ == "__main__":
    main()
