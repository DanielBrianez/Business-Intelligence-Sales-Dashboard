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


# ============================================================
# 4. FEATURE ENGINEERING
# ============================================================

df["year"] = df["order_date"].dt.year
df["month"] = df["order_date"].dt.month
df["month_name"] = df["order_date"].dt.month_name()

df["day"] = df["order_date"].dt.day

df["weekday"] = df["order_date"].dt.day_name()

df["quarter"] = df["order_date"].dt.quarter

df["sales"] = df["sales"].astype(float)

# ============================================================
# 5. KPIs EXECUTIVOS
# ============================================================

total_revenue = df["sales"].sum()

total_orders = df["order_id"].nunique()

average_ticket = (
    total_revenue / total_orders
)

top_state = (
    df.groupby("state")["sales"]
    .sum()
    .sort_values(ascending=False)
    .head(1)
)

top_category = (
    df.groupby("category")["sales"]
    .sum()
    .sort_values(ascending=False)
    .head(1)
)

# print("\n===== KPIs EXECUTIVOS =====")

# print(f"Total Revenue: ${total_revenue:,.2f}")

# print(f"Total Orders: {total_orders}")

# print(f"Average Ticket: ${average_ticket:,.2f}")

# print("\nTop State by Revenue:")
# print(top_state)

# print("\nTop Category by Revenue:")
# print(top_category)

# ============================================================
# 6. VISUALIZAÇÕES
# ============================================================


# ============================================================
# 6.1 RECEITA POR MÊS
# ============================================================

revenue_by_month = (
    df.groupby("month_name")["sales"]
    .sum()
    .reset_index()
)

month_order = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

revenue_by_month["month_name"] = pd.Categorical(
    revenue_by_month["month_name"],
    categories=month_order,
    ordered=True
)

revenue_by_month = (
    revenue_by_month
    .sort_values("month_name")
)

plt.figure(figsize=(12, 6))

plt.plot(
    revenue_by_month["month_name"],
    revenue_by_month["sales"],
    marker="o"
)

plt.title(
    "Revenue by Month",
    fontsize=16
)

plt.xlabel(
    "Month",
    fontsize=12
)

plt.ylabel(
    "Revenue",
    fontsize=12
)

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "graficos/revenue_by_month.png",
    dpi=300
)

plt.close()

# ============================================================
# 6.2 RECEITA POR ESTADO
# ============================================================

revenue_by_state = (
    df.groupby("state")["sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

plt.figure(figsize=(12, 6))

bars = plt.barh(
    revenue_by_state["state"],
    revenue_by_state["sales"]
)

plt.title(
    "Top 10 States by Revenue",
    fontsize=16
)

plt.xlabel(
    "Revenue",
    fontsize=12
)

plt.ylabel(
    "State",
    fontsize=12
)

plt.gca().invert_yaxis()


# ============================================================
# LABELS NAS BARRAS
# ============================================================

for bar in bars:

    width = bar.get_width()

    plt.text(
        width + 1000,
        bar.get_y() + bar.get_height() / 2,
        f"${width:,.0f}",
        va="center",
        fontsize=10
    )

plt.tight_layout()

plt.savefig(
    "graficos/revenue_by_state.png",
    dpi=300
)

plt.close()

# ============================================================
# 6.3 RECEITA POR CATEGORIA
# ============================================================

revenue_by_category = (
    df.groupby("category")["sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

plt.figure(figsize=(10, 6))

bars = plt.bar(
    revenue_by_category["category"],
    revenue_by_category["sales"]
)

plt.title(
    "Revenue by Category",
    fontsize=16
)

plt.xlabel(
    "Category",
    fontsize=12
)

plt.ylabel(
    "Revenue",
    fontsize=12
)


# ============================================================
# LABELS NAS BARRAS
# ============================================================

for bar in bars:

    height = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height + 5000,
        f"${height:,.0f}",
        ha="center",
        fontsize=10
    )

plt.tight_layout()

plt.savefig(
    "graficos/revenue_by_category.png",
    dpi=300
)

plt.close()

# ============================================================
# 6.4 TOP 10 CLIENTES POR RECEITA
# ============================================================

top_customers = (
    df.groupby("customer_name")["sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

plt.figure(figsize=(12, 6))

bars = plt.barh(
    top_customers["customer_name"],
    top_customers["sales"]
)

plt.title(
    "Top 10 Customers by Revenue",
    fontsize=16
)

plt.xlabel(
    "Revenue",
    fontsize=12
)

plt.ylabel(
    "Customer",
    fontsize=12
)

plt.gca().invert_yaxis()


# ============================================================
# LABELS NAS BARRAS
# ============================================================

for bar in bars:

    width = bar.get_width()

    plt.text(
        width + 1000,
        bar.get_y() + bar.get_height() / 2,
        f"${width:,.0f}",
        va="center",
        fontsize=10
    )

plt.tight_layout()

plt.savefig(
    "graficos/top_customers.png",
    dpi=300
)

plt.close()

# ============================================================
# 6.5 CRESCIMENTO MENSAL
# ============================================================

monthly_growth = (
    df.groupby(["year", "month", "month_name"])["sales"]
    .sum()
    .reset_index()
)

monthly_growth = monthly_growth.sort_values(
    ["year", "month"]
)


# ============================================================
# CÁLCULO DE CRESCIMENTO
# ============================================================

monthly_growth["growth_percentage"] = (
    monthly_growth["sales"]
    .pct_change() * 100
)

# ============================================================
# REMOVER PRIMEIRO VALOR NULO
# ============================================================

monthly_growth = monthly_growth.dropna(
    subset=["growth_percentage"]
)

# ============================================================
# CRIAR COLUNA YEAR_MONTH
# ============================================================

monthly_growth["year_month"] = (
    monthly_growth["year"].astype(str)
    + "-"
    + monthly_growth["month"].astype(str).str.zfill(2)
)

# ============================================================
# GRÁFICO
# ============================================================

plt.figure(figsize=(14, 6))

plt.plot(
    monthly_growth["year_month"],
    monthly_growth["growth_percentage"],
    marker="o"
)

plt.title(
    "Monthly Revenue Growth (%)",
    fontsize=16
)

plt.xlabel(
    "Year-Month",
    fontsize=12
)

plt.ylabel(
    "Growth (%)",
    fontsize=12
)


# ============================================================
# LINHA DE REFERÊNCIA
# ============================================================

plt.axhline(
    y=0,
    color="gray",
    linestyle="--"
)


# ============================================================
# AJUSTES VISUAIS
# ============================================================

plt.xticks(rotation=45)

plt.tight_layout()


# ============================================================
# EXPORTAR GRÁFICO
# ============================================================

plt.savefig(
    "graficos/monthly_growth.png",
    dpi=300
)

plt.close()

# ============================================================
# 6.6 TOP 10 PRODUTOS POR RECEITA
# ============================================================

top_products = (
    df.groupby("product_name")["sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)


# ============================================================
# GRÁFICO
# ============================================================

plt.figure(figsize=(14, 6))

bars = plt.barh(
    top_products["product_name"],
    top_products["sales"]
)

plt.title(
    "Top 10 Products by Revenue",
    fontsize=16
)

plt.xlabel(
    "Revenue",
    fontsize=12
)

plt.ylabel(
    "Product",
    fontsize=12
)

plt.gca().invert_yaxis()


# ============================================================
# LABELS NAS BARRAS
# ============================================================

for bar in bars:

    width = bar.get_width()

    plt.text(
        width + 500,
        bar.get_y() + bar.get_height() / 2,
        f"${width:,.0f}",
        va="center",
        fontsize=10
    )


# ============================================================
# AJUSTES VISUAIS
# ============================================================

plt.tight_layout()

# ============================================================
# EXPORTAR GRÁFICO
# ============================================================

plt.savefig(
    "graficos/top_products.png",
    dpi=300
)

plt.close()

# ============================================================
# 7. ARMAZENAMENTO DOS DADOS
# ============================================================

df.to_sql(
    "sales",
    conexao,
    if_exists="replace",
    index=False
)

# ============================================================
# 8. LEITURA DAS QUERIES SQL
# ============================================================

def carregar_query(nome_arquivo):
    caminho = f"queries/{nome_arquivo}"

    with open(caminho, "r", encoding="utf-8") as arquivo:
        return arquivo.read()


query_total_revenue = carregar_query("total_revenue.sql")
query_revenue_by_month = carregar_query("revenue_by_month.sql")
query_revenue_by_category = carregar_query("revenue_by_category.sql")
query_top_products = carregar_query("top_products.sql")
query_top_customers = carregar_query("top_customers.sql")


total_revenue_sql = pd.read_sql_query(query_total_revenue, conexao)
revenue_by_month_sql = pd.read_sql_query(query_revenue_by_month, conexao)
revenue_by_category_sql = pd.read_sql_query(query_revenue_by_category, conexao)
top_products_sql = pd.read_sql_query(query_top_products, conexao)
top_customers_sql = pd.read_sql_query(query_top_customers, conexao)

# ============================================================
# 9. EXPORTAÇÃO DOS DADOS
# ============================================================

df.to_csv(
    "dados/sales_clean.csv",
    index=False
)