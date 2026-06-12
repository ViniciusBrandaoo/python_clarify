import pandas as pd
import numpy as np

# ==========================
# CARREGAR CSV
# ==========================

df = pd.read_csv("drinks.csv")

# ==========================
# RENOMEAR COLUNAS
# ==========================

df.columns = [
    "Pais",
    "Cerveja",
    "Destilados",
    "Vinho",
    "LitrosAlcool"
]

# ==========================
# VISUALIZAÇÃO INICIAL
# ==========================

print("=== PRIMEIRAS 5 LINHAS ===")
print(df.head())

print("\n=== INFORMAÇÕES DO DATAFRAME ===")
print(df.info())

print("\n=== ESTATÍSTICAS GERAIS ===")
print(df.describe())

# ==========================
# ESTATÍSTICAS COM NUMPY
# ==========================

print("\n=== ESTATÍSTICAS DE CERVEJA ===")

print(f"Média: {np.mean(df['Cerveja']):.2f}")
print(f"Mediana: {np.median(df['Cerveja']):.2f}")
print(f"Maior Consumo: {np.max(df['Cerveja'])}")
print(f"Menor Consumo: {np.min(df['Cerveja'])}")
print(f"Desvio Padrão: {np.std(df['Cerveja']):.2f}")

# ==========================
# TOP 10 CERVEJA
# ==========================

print("\n=== TOP 10 PAÍSES QUE MAIS CONSOMEM CERVEJA ===")

top10 = df.nlargest(10, "Cerveja")

print(
    top10[
        ["Pais", "Cerveja"]
    ]
)

# ==========================
# TOP 10 VINHO
# ==========================

print("\n=== TOP 10 PAÍSES QUE MAIS CONSOMEM VINHO ===")

print(
    df.nlargest(10, "Vinho")
    [["Pais", "Vinho"]]
)

# ==========================
# FILTROS
# ==========================

media_alcool = df["LitrosAlcool"].mean()

print("\n=== ACIMA DA MÉDIA DE ÁLCOOL ===")

print(
    df[
        df["LitrosAlcool"] > media_alcool
    ][
        ["Pais", "LitrosAlcool"]
    ]
)

# ==========================
# NOVA COLUNA TOTAL
# ==========================

df["TotalBebidas"] = (
    df["Cerveja"] +
    df["Destilados"] +
    df["Vinho"]
)

print("\n=== TOTAL DE BEBIDAS ===")

print(
    df[
        ["Pais", "TotalBebidas"]
    ].head()
)

# ==========================
# CLASSIFICAÇÃO COM NUMPY
# ==========================

condicoes = [
    df["LitrosAlcool"] < 2,
    df["LitrosAlcool"] < 5,
    df["LitrosAlcool"] < 8,
    df["LitrosAlcool"] >= 8
]

categorias = [
    "Muito Baixo",
    "Baixo",
    "Médio",
    "Alto"
]

df["NivelConsumo"] = np.select(
    condicoes,
    categorias,
    default="Não Informado"
)

print("\n=== CLASSIFICAÇÃO DE CONSUMO ===")

print(
    df[
        ["Pais", "LitrosAlcool", "NivelConsumo"]
    ].head(20)
)

# ==========================
# CONTAGEM POR CATEGORIA
# ==========================

print("\n=== QUANTIDADE DE PAÍSES POR NÍVEL ===")

print(
    df["NivelConsumo"]
    .value_counts()
)

# ==========================
# PAÍS COM MAIOR CONSUMO TOTAL
# ==========================

maior_consumo = df.loc[
    df["TotalBebidas"].idxmax()
]

print("\n=== MAIOR CONSUMIDOR ===")

print(maior_consumo)

# ==========================
# ACIMA DA MÉDIA EM TUDO
# ==========================

media_cerveja = df["Cerveja"].mean()
media_destilados = df["Destilados"].mean()
media_vinho = df["Vinho"].mean()

print("\n=== ACIMA DA MÉDIA EM TODAS AS BEBIDAS ===")

resultado = df[
    (df["Cerveja"] > media_cerveja) &
    (df["Destilados"] > media_destilados) &
    (df["Vinho"] > media_vinho)
]

print(
    resultado[
        ["Pais", "Cerveja", "Destilados", "Vinho"]
    ]
)

# ==========================
# CORRELAÇÃO
# ==========================

print("\n=== MATRIZ DE CORRELAÇÃO ===")

print(
    df[
        [
            "Cerveja",
            "Destilados",
            "Vinho",
            "LitrosAlcool"
        ]
    ].corr()
)

# ==========================
# ORDENAÇÃO
# ==========================

print("\n=== TOP 20 CONSUMO TOTAL ===")

print(
    df.sort_values(
        by="TotalBebidas",
        ascending=False
    )
    [
        ["Pais", "TotalBebidas"]
    ]
    .head(20)
)

# ==========================
# SALVAR CSV
# ==========================

df.to_csv(
    "drinks_processado.csv",
    index=False
)