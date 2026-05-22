# ============================================================
# PROJETO: BUSINESS INTELLIGENCE SALES DASHBOARD
# ============================================================

import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# 1. CONFIGURAÇÃO DO PROJETO
# ============================================================

ARQUIVO_VENDAS = "dados/superstore_sales.csv"

os.makedirs("graficos", exist_ok=True)

conexao = sqlite3.connect("sales_analytics.db")


# ============================================================
# 2. LEITURA DOS DADOS
# ============================================================

df = pd.read_csv(ARQUIVO_VENDAS)

# ============================================================
# 3. LIMPEZA INICIAL
# ============================================================

df.columns = (
    df.columns
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("-", "_")
)

df["order_date"] = pd.to_datetime(df["order_date"], dayfirst=True)
df["ship_date"] = pd.to_datetime(df["ship_date"], dayfirst=True)

df["postal_code"] = df["postal_code"].fillna(0).astype(int)

print(df.head())
print(df.info())