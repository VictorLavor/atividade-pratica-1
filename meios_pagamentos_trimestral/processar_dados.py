import pandas as pd
import requests

BASE = "https://olinda.bcb.gov.br/olinda/servico/MPV_DadosAbertos/versao/v1/odata/MeiosdePagamentosTrimestral"

select = (
    "datatrimestre,valorPix,valorTED,"
    "quantidadePix,quantidadeTED,quantidadeCheque,"
    "quantidadeBoleto"
)

rows, skip, top = [], 0, 100
while True:
    params = {
        "$select": select,
        "$format": "json",
        "$top": top,
        "$skip": skip,
    }
    r = requests.get(BASE, params=params, timeout=60)
    r.raise_for_status()

    batch = r.json().get("value", [])
    if not batch:
        break

    rows.extend(batch)
    if len(batch) < top:
        break
    skip += top

df = pd.DataFrame(rows)

if df.empty:
    print("Nenhum dado encontrado.")
else:
    # Converte datatrimestre para inteiro e cria colunas Ano e Trimestre
    df["datatrimestre"] = df["datatrimestre"].astype(int)
    df["Ano"] = df["datatrimestre"] // 100
    df["Tri"] = df["datatrimestre"] % 100

    # Filtra somente de 2023 em diante
    df = df[df["Ano"] >= 2023]

    # Converte colunas numéricas
    num_cols = [c for c in df.columns if c.startswith(("valor", "quantidade"))]
    df[num_cols] = df[num_cols].apply(pd.to_numeric, errors="coerce")

    # Ordena
    df = df.sort_values(["Ano", "Tri"], ignore_index=True)

    # Salva CSV
    df.to_csv("meios_pagamentos_trimestrais_2023_hoje.csv", index=False, encoding="utf-8")

    print(df.head())
    print("\nLinhas x Colunas:", df.shape)
    print("\nArquivo salvo como: meios_pagamentos_trimestrais_2023_hoje.csv")

