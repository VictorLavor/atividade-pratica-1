import os
import pandas as pd

# === 1) CONFIGURAÇÃO ===
CAMINHO_JSON = r"C:\Users\victo\OneDrive\Documentos\Faculdade Senac\4 Periodo\Big Data\API\data\meios_pagamentos.json"
PASTA_TRATADOS = os.path.join(os.path.dirname(CAMINHO_JSON), "..", "tratados")
os.makedirs(PASTA_TRATADOS, exist_ok=True)

# === 2) LEITURA DO JSON ===
df = pd.read_json(CAMINHO_JSON)

# === 3) AJUSTE DE DATAS ===
df["AnoMes"] = pd.to_datetime(df["AnoMes"], format="%Y%m")
df = df.sort_values("AnoMes")

# === 4) SALVAR CSV TRATADO ===
caminho_tratado = os.path.join(PASTA_TRATADOS, "meios_pagamentos_tratado.csv")
df.to_csv(caminho_tratado, index=False, encoding="utf-8")

print(f"CSV tratado salvo em:\n{caminho_tratado}")
print(df.head())
