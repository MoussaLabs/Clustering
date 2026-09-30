"""
Premières statistiques descriptives sur le jeu de données KaraFun.

Lancement (depuis le dossier Clustering) :
    python3 stats_descriptives.py
"""

import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------------
# 1. Chargement des données
# ---------------------------------------------------------------
df = pd.read_csv("td_clustering_karafun.csv")

print("=" * 60)
print("1. APERÇU GÉNÉRAL")
print("=" * 60)
print(f"Nombre de lignes   : {df.shape[0]}")
print(f"Nombre de colonnes : {df.shape[1]}")
print("\nLes 5 premières lignes :")
print(df.head())

# ---------------------------------------------------------------
# 2. Types des variables et valeurs manquantes
# ---------------------------------------------------------------
print("\n" + "=" * 60)
print("2. TYPES ET VALEURS MANQUANTES")
print("=" * 60)
resume = pd.DataFrame({
    "type": df.dtypes,
    "nb_manquants": df.isna().sum(),
    "nb_modalites": df.nunique(),
})
print(resume)

# Vérification des doublons sur l'identifiant client
nb_doublons = df["id_anonyme"].duplicated().sum()
print(f"\nNombre d'identifiants en double : {nb_doublons}")

# ---------------------------------------------------------------
# 3. Variable numérique : nb_abo_periode
# ---------------------------------------------------------------
print("\n" + "=" * 60)
print("3. VARIABLE NUMÉRIQUE : nb_abo_periode")
print("=" * 60)
print(df["nb_abo_periode"].describe())

# Répartition par modalité (chaque valeur de 1 à 12 vue comme une modalité)
effectifs = df["nb_abo_periode"].value_counts().sort_index()
pourcentages = (effectifs / len(df) * 100).round(1)
tableau = pd.DataFrame({
    "effectif": effectifs,
    "pourcentage (%)": pourcentages,
    "pourcentage cumulé (%)": (effectifs.cumsum() / len(df) * 100).round(1),
})
print("\nRépartition par modalité :")
print(tableau)

# ---------------------------------------------------------------
# 4. Variables qualitatives : effectifs et pourcentages
# ---------------------------------------------------------------
print("\n" + "=" * 60)
print("4. VARIABLES QUALITATIVES")
print("=" * 60)

# Toutes les colonnes sauf l'identifiant et la variable numérique
variables_quali = [c for c in df.columns if c not in ("id_anonyme", "nb_abo_periode")]

for col in variables_quali:
    effectifs = df[col].value_counts(dropna=False).sort_index()
    pourcentages = (effectifs / len(df) * 100).round(1)
    tableau = pd.DataFrame({"effectif": effectifs, "pourcentage (%)": pourcentages})
    print(f"\n--- {col} ---")
    print(tableau)

# ---------------------------------------------------------------
# 5. Un exemple de tableau croisé
# ---------------------------------------------------------------
print("\n" + "=" * 60)
print("5. TABLEAU CROISÉ : type_client x statut_abonnement (% en ligne)")
print("=" * 60)
croise = pd.crosstab(df["type_client"], df["statut_abonnement"], normalize="index") * 100
print(croise.round(1))

# ---------------------------------------------------------------
# 6. Graphiques : un diagramme en barres par variable qualitative
# ---------------------------------------------------------------
nb = len(variables_quali)
nb_colonnes = 3
nb_lignes = (nb + nb_colonnes - 1) // nb_colonnes

fig, axes = plt.subplots(nb_lignes, nb_colonnes, figsize=(16, 4 * nb_lignes))
axes = axes.flatten()

for ax, col in zip(axes, variables_quali):
    df[col].value_counts().sort_index().plot(kind="bar", ax=ax, color="steelblue")
    ax.set_title(col)
    ax.set_xlabel("")
    ax.tick_params(axis="x", labelrotation=45, labelsize=8)

# On cache les cases vides s'il en reste
for ax in axes[nb:]:
    ax.set_visible(False)

plt.tight_layout()
plt.savefig("stats_descriptives.png", dpi=100)
print("\nGraphiques enregistrés dans stats_descriptives.png")
plt.show()
