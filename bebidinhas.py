import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================
# PALETA VISUAL
# ==========================

BG    = "#0a0804"
CARD  = "#110e06"
GOLD  = "#c9a84c"
GOLD2 = "#a8864a"
GOLD3 = "#7a6535"
GOLD4 = "#4a3c20"

plt.rcParams.update({
    "figure.facecolor":  BG,
    "axes.facecolor":    CARD,
    "axes.edgecolor":    GOLD4,
    "axes.labelcolor":   GOLD2,
    "xtick.color":       GOLD3,
    "ytick.color":       GOLD3,
    "text.color":        GOLD,
    "grid.color":        GOLD4,
    "grid.alpha":        0.3,
    "font.family":       "monospace",
    "axes.spines.top":   False,
    "axes.spines.right": False,
})

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

media_cerveja    = df["Cerveja"].mean()
media_destilados = df["Destilados"].mean()
media_vinho      = df["Vinho"].mean()

print("\n=== ACIMA DA MÉDIA EM TODAS AS BEBIDAS ===")

resultado = df[
    (df["Cerveja"]     > media_cerveja) &
    (df["Destilados"]  > media_destilados) &
    (df["Vinho"]       > media_vinho)
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
# SALVAR CSV PROCESSADO
# ==========================

df.to_csv(
    "drinks_processado.csv",
    index=False
)

print("\n=== CSV PROCESSADO SALVO ===")

# ==========================
# VISUALIZAÇÃO 1 — TOP 10
# ==========================

fig1, axes = plt.subplots(1, 3, figsize=(18, 6))
fig1.patch.set_facecolor(BG)
fig1.suptitle(
    "Top 10 Países por Tipo de Bebida",
    fontsize=14, color=GOLD, y=1.02, fontweight="bold"
)

bebidas = [
    ("Cerveja",    GOLD),
    ("Vinho",      GOLD2),
    ("Destilados", GOLD3),
]

for ax, (col, cor) in zip(axes, bebidas):
    top = df.nlargest(10, col)[["Pais", col]].sort_values(col)
    bars = ax.barh(top["Pais"], top[col], color=cor, alpha=0.85, height=0.65)
    ax.set_title(f"Top 10 · {col}", color=GOLD, fontsize=11, pad=10)
    ax.set_xlabel("Doses / ano", fontsize=9)
    ax.grid(axis="x", alpha=0.2)
    for bar in bars:
        w = bar.get_width()
        ax.text(w + 2, bar.get_y() + bar.get_height() / 2,
                f"{int(w)}", va="center", fontsize=8, color=GOLD3)
    ax.set_facecolor(CARD)

plt.tight_layout()
plt.savefig("viz_top10.png", dpi=150, bbox_inches="tight", facecolor=BG)
plt.close()
print("=== GRÁFICO 1 SALVO: viz_top10.png ===")

# ==========================
# VISUALIZAÇÃO 2 — HEATMAP
# ==========================

fig2, ax = plt.subplots(figsize=(7, 5))
fig2.patch.set_facecolor(BG)
ax.set_facecolor(CARD)

corr = df[["Cerveja", "Destilados", "Vinho", "LitrosAlcool"]].corr()

sns.heatmap(
    corr, ax=ax,
    annot=True, fmt=".2f",
    cmap="YlOrBr",
    linewidths=0.5, linecolor=BG,
    annot_kws={"size": 11, "color": BG},
    cbar_kws={"shrink": 0.8}
)

ax.set_title("Matriz de Correlação", color=GOLD, fontsize=13, pad=14, fontweight="bold")
plt.setp(ax.get_xticklabels(), rotation=30, color=GOLD2)
plt.setp(ax.get_yticklabels(), rotation=0,  color=GOLD2)

plt.tight_layout()
plt.savefig("viz_correlacao.png", dpi=150, bbox_inches="tight", facecolor=BG)
plt.close()
print("=== GRÁFICO 2 SALVO: viz_correlacao.png ===")

# ==========================
# VISUALIZAÇÃO 3 — PIZZA
# ==========================

fig3, ax = plt.subplots(figsize=(7, 6))
fig3.patch.set_facecolor(BG)
ax.set_facecolor(BG)

niveis  = df["NivelConsumo"].value_counts()
cores   = [GOLD, GOLD2, GOLD3, GOLD4]
explode = [0.04] * len(niveis)

wedges, texts, autotexts = ax.pie(
    niveis,
    labels=niveis.index,
    autopct="%1.1f%%",
    colors=cores[:len(niveis)],
    explode=explode,
    startangle=140,
    pctdistance=0.78,
    wedgeprops=dict(edgecolor=BG, linewidth=2)
)

for t in texts:
    t.set_color(GOLD2)
    t.set_fontsize(11)
for t in autotexts:
    t.set_color(BG)
    t.set_fontsize(10)
    t.set_fontweight("bold")

ax.set_title(
    "Distribuição por Nível de Consumo",
    color=GOLD, fontsize=13, pad=16, fontweight="bold"
)

plt.tight_layout()
plt.savefig("viz_pizza.png", dpi=150, bbox_inches="tight", facecolor=BG)
plt.close()
print("=== GRÁFICO 3 SALVO: viz_pizza.png ===")

# ==========================
# VISUALIZAÇÃO 4 — SCATTER
# ==========================

fig4, ax = plt.subplots(figsize=(9, 6))
fig4.patch.set_facecolor(BG)
ax.set_facecolor(CARD)

nivel_cores = {
    "Alto":       GOLD,
    "Médio":      GOLD2,
    "Baixo":      GOLD3,
    "Muito Baixo": GOLD4,
}

for nivel, grupo in df.groupby("NivelConsumo"):
    ax.scatter(
        grupo["TotalBebidas"],
        grupo["LitrosAlcool"],
        color=nivel_cores.get(nivel, GOLD3),
        label=nivel,
        alpha=0.85,
        s=55,
        edgecolors=BG,
        linewidths=0.5
    )

# Linha de tendência
m, b = np.polyfit(df["TotalBebidas"], df["LitrosAlcool"], 1)
x_line = np.linspace(df["TotalBebidas"].min(), df["TotalBebidas"].max(), 100)
ax.plot(x_line, m * x_line + b,
        color=GOLD, linewidth=1.5, linestyle="--", alpha=0.7, label="Tendência")

# Destacar top 5
top5 = df.nlargest(5, "TotalBebidas")
for _, row in top5.iterrows():
    ax.annotate(
        row["Pais"],
        xy=(row["TotalBebidas"], row["LitrosAlcool"]),
        xytext=(8, 4), textcoords="offset points",
        fontsize=7.5, color=GOLD2
    )

ax.set_xlabel("Total de Doses (Cerveja + Vinho + Destilados)", fontsize=10)
ax.set_ylabel("Litros de Álcool Puro / ano", fontsize=10)
ax.set_title(
    "Consumo Total vs Litros de Álcool Puro por País",
    color=GOLD, fontsize=13, pad=14, fontweight="bold"
)
ax.legend(fontsize=9, facecolor=CARD, edgecolor=GOLD4, labelcolor=GOLD2)
ax.grid(True, alpha=0.15)

plt.tight_layout()
plt.savefig("viz_scatter.png", dpi=150, bbox_inches="tight", facecolor=BG)
plt.close()
print("=== GRÁFICO 4 SALVO: viz_scatter.png ===")

print("\n✓ Análise completa. Arquivos gerados:")
print("  - drinks_processado.csv")
print("  - viz_top10.png")
print("  - viz_correlacao.png")
print("  - viz_pizza.png")
print("  - viz_scatter.png")
