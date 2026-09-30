"""
Regroupement des modalités avant l'ACM.

Pourquoi regrouper ?
    - En ACM, une modalité rare (moins de ~2-5 % des individus) pèse trop
      lourd et peut créer à elle seule un axe sans intérêt.
    - Une variable avec beaucoup de modalités pèse plus qu'une variable avec
      peu de modalités. On vise donc environ 4 à 6 modalités par variable.

Ce script :
    1. lit le fichier d'origine td_clustering_karafun.csv
    2. regroupe les modalités de plusieurs variables
    3. enregistre le résultat dans td_clustering_karafun_regroupe.csv
       (le fichier d'origine n'est PAS modifié)

Lancement (depuis le dossier Clustering) :
    python3 regroupements.py

Méthode utilisée pour chaque variable :
    On écrit un dictionnaire  { ancienne_modalité : nouvelle_modalité }
    puis on l'applique à la colonne avec .map().
    Les nouvelles modalités commencent par un numéro (01_, 02_ ...) pour
    qu'elles restent dans le bon ordre quand on les trie.
"""

import pandas as pd


# 1. Chargement des données
df = pd.read_csv("td_clustering_karafun.csv")


# ---------------------------------------------------------------
# 2. nb_abo_periode : variable QUANTITATIVE -> QUALITATIVE (5 classes)
# ---------------------------------------------------------------
# L'ACM n'accepte que des variables qualitatives. nb_abo_periode est la
# seule variable numérique du fichier : on découpe ses valeurs (1 à 12)
# en classes, et chaque classe devient une modalité (du texte).
# Beaucoup de clients à 1 (28,5 %) et à 12 (21 %), peu entre les deux.
# Ici les clés du dictionnaire sont des NOMBRES (pas de guillemets),
# car la colonne d'origine contient des nombres.
groupes_nb_abo = {
    1: "01_1_abo",
    2: "02_2a3_abo",
    3: "02_2a3_abo",
    4: "03_4a6_abo",
    5: "03_4a6_abo",
    6: "03_4a6_abo",
    7: "04_7a11_abo",
    8: "04_7a11_abo",
    9: "04_7a11_abo",
    10: "04_7a11_abo",
    11: "04_7a11_abo",
    12: "05_12_abo",
}
df["nb_abo_periode"] = df["nb_abo_periode"].map(groupes_nb_abo)


# ---------------------------------------------------------------
# 3. anciennete_client_tr : 20 modalités -> 6 classes
# ---------------------------------------------------------------
groupes_anciennete_client = {
    "00_moins_1_mois":     "01_moins_3_mois",
    "01_1_mois":           "01_moins_3_mois",
    "02_2_mois":           "01_moins_3_mois",
    "03_3_mois":           "02_3a5_mois",
    "04_4_mois":           "02_3a5_mois",
    "05_5_mois":           "02_3a5_mois",
    "06_6_mois":           "03_6a12_mois",
    "07_7a9_mois":         "03_6a12_mois",
    "08_10a12_mois":       "03_6a12_mois",
    "09_13a15_mois":       "04_13a24_mois",
    "10_16a18_mois":       "04_13a24_mois",
    "11_19a21_mois":       "04_13a24_mois",
    "12_22a24_mois":       "04_13a24_mois",
    "13_25a30_mois":       "05_25a48_mois",
    "14_31a36_mois":       "05_25a48_mois",
    "15_37a48_mois":       "05_25a48_mois",
    "16_49a60_mois":       "06_49_mois_et_plus",
    "17_61a84_mois":       "06_49_mois_et_plus",
    "18_85a120_mois":      "06_49_mois_et_plus",
    "19_121_mois_et_plus": "06_49_mois_et_plus",
}
df["anciennete_client_tr"] = df["anciennete_client_tr"].map(groupes_anciennete_client)


# ---------------------------------------------------------------
# 4. anciennete_abonnement_tr : 20 modalités -> 5 classes
# ---------------------------------------------------------------
# Mêmes tranches que l'ancienneté client, mais au-delà de 25 mois il y a
# très peu d'abonnements : on met tout "25 mois et plus" ensemble.
groupes_anciennete_abo = {
    "00_moins_1_mois":     "01_moins_3_mois",
    "01_1_mois":           "01_moins_3_mois",
    "02_2_mois":           "01_moins_3_mois",
    "03_3_mois":           "02_3a5_mois",
    "04_4_mois":           "02_3a5_mois",
    "05_5_mois":           "02_3a5_mois",
    "06_6_mois":           "03_6a12_mois",
    "07_7a9_mois":         "03_6a12_mois",
    "08_10a12_mois":       "03_6a12_mois",
    "09_13a15_mois":       "04_13a24_mois",
    "10_16a18_mois":       "04_13a24_mois",
    "11_19a21_mois":       "04_13a24_mois",
    "12_22a24_mois":       "04_13a24_mois",
    "13_25a30_mois":       "05_25_mois_et_plus",
    "14_31a36_mois":       "05_25_mois_et_plus",
    "15_37a48_mois":       "05_25_mois_et_plus",
    "16_49a60_mois":       "05_25_mois_et_plus",
    "17_61a84_mois":       "05_25_mois_et_plus",
    "18_85a120_mois":      "05_25_mois_et_plus",
    "19_121_mois_et_plus": "05_25_mois_et_plus",
}
df["anciennete_abonnement_tr"] = df["anciennete_abonnement_tr"].map(groupes_anciennete_abo)


# ---------------------------------------------------------------
# 5. valeur_12M_tr : 12 modalités -> 6 classes
# ---------------------------------------------------------------
groupes_valeur = {
    "00_moins_10":    "01_moins_10",
    "01_10a15":       "02_10a20",
    "02_15a20":       "02_10a20",
    "03_20a25":       "03_20a40",
    "04_25a30":       "03_20a40",
    "05_30a40":       "03_20a40",
    "06_40a50":       "04_40a70",
    "07_50a60":       "04_40a70",
    "08_60a70":       "04_40a70",
    "09_70a90":       "05_70a90",
    "10_90a110":      "06_90_et_plus",
    "11_110_et_plus": "06_90_et_plus",
}
df["valeur_12M_tr"] = df["valeur_12M_tr"].map(groupes_valeur)


# ---------------------------------------------------------------
# 6. avg_sessions_actifs_tr : 14 modalités -> 6 classes
# ---------------------------------------------------------------
groupes_sessions = {
    "00_pas_de_session": "00_pas_de_session",
    "01_moins_1":        "01_moins_1",
    "02_1a2":            "02_1a2",
    "03_2a3":            "03_2a3",
    "04_3a4":            "04_3a5",
    "05_4a5":            "04_3a5",
    "06_5a6":            "05_5_et_plus",
    "07_6a8":            "05_5_et_plus",
    "08_8a10":           "05_5_et_plus",
    "09_10a15":          "05_5_et_plus",
    "10_15a20":          "05_5_et_plus",
    "11_20a30":          "05_5_et_plus",
    "12_30a50":          "05_5_et_plus",
    "13_50_et_plus":     "05_5_et_plus",
}
df["avg_sessions_actifs_tr"] = df["avg_sessions_actifs_tr"].map(groupes_sessions)


# ---------------------------------------------------------------
# 7. avg_songs_sessions_tr : 13 modalités -> 6 classes
# ---------------------------------------------------------------
groupes_songs = {
    "00_pas_de_session": "00_pas_de_session",
    "01_1a2":            "01_1a3",
    "02_2a3":            "01_1a3",
    "03_3a4":            "02_3a6",
    "04_4a5":            "02_3a6",
    "05_5a6":            "02_3a6",
    "06_6a8":            "03_6a10",
    "07_8a10":           "03_6a10",
    "08_10a15":          "04_10a20",
    "09_15a20":          "04_10a20",
    "10_20a30":          "05_20_et_plus",
    "11_30a50":          "05_20_et_plus",
    "12_50_et_plus":     "05_20_et_plus",
}
df["avg_songs_sessions_tr"] = df["avg_songs_sessions_tr"].map(groupes_songs)


# ---------------------------------------------------------------
# 8. methode_paiement : 7 modalités -> 5 classes
# ---------------------------------------------------------------
# Amazon (0,8 %), Credit (0,2 %) et Others (1 seul client !) sont trop rares.
groupes_paiement = {
    "Stripe":  "Stripe",
    "Apple":   "Apple",
    "Android": "Android",
    "Paypal":  "Paypal",
    "Amazon":  "Autre",
    "Credit":  "Autre",
    "Others":  "Autre",
}
df["methode_paiement"] = df["methode_paiement"].map(groupes_paiement)


# ---------------------------------------------------------------
# 9. zone_geo : 11 modalités -> 6 classes
# ---------------------------------------------------------------
# Les petites zones (chacune autour de 1-2 %) sont réunies ensemble.
groupes_zone = {
    "US":                  "US",
    "Europe":              "Europe",
    "FR":                  "FR",
    "UK":                  "UK",
    "CA":                  "CA",
    "Oceanie":             "Reste_du_monde",
    "Asie":                "Reste_du_monde",
    "Afrique":             "Reste_du_monde",
    "Amerique_Sud":        "Reste_du_monde",
    "Amerique_Nord_Autre": "Reste_du_monde",
    "Autre/Inconnu":       "Reste_du_monde",
}
df["zone_geo"] = df["zone_geo"].map(groupes_zone)


# ---------------------------------------------------------------
# 10. type_very_first_abo : 3 modalités -> 2 classes
# ---------------------------------------------------------------
# "offert" (2,5 %) et "reduc" (0,6 %) sont rares : on les réunit.
groupes_first_abo = {
    "payant": "payant",
    "offert": "non_payant",
    "reduc":  "non_payant",
}
df["type_very_first_abo"] = df["type_very_first_abo"].map(groupes_first_abo)


# ---------------------------------------------------------------
# 11. Vérification : aucune valeur perdue
# ---------------------------------------------------------------
# Si une modalité avait été oubliée dans un dictionnaire, .map() l'aurait
# remplacée par une valeur vide (NaN). On vérifie donc qu'il n'y en a aucune.
nb_vides = df.isna().sum().sum()
print(f"Nombre de valeurs vides après regroupement : {nb_vides}  (doit être 0)")


# ---------------------------------------------------------------
# 12. Affichage des nouvelles répartitions (pour contrôle)
# ---------------------------------------------------------------
variables_regroupees = [
    "nb_abo_periode",
    "anciennete_client_tr",
    "anciennete_abonnement_tr",
    "valeur_12M_tr",
    "avg_sessions_actifs_tr",
    "avg_songs_sessions_tr",
    "methode_paiement",
    "zone_geo",
    "type_very_first_abo",
]

for col in variables_regroupees:
    effectifs = df[col].value_counts().sort_index()
    pourcentages = (effectifs / len(df) * 100).round(1)
    tableau = pd.DataFrame({"effectif": effectifs, "pourcentage (%)": pourcentages})
    print(f"\n--- {col} ---")
    print(tableau)


# ---------------------------------------------------------------
# 13. Enregistrement du nouveau fichier
# ---------------------------------------------------------------
# index=False : on n'écrit pas les numéros de ligne de pandas dans le CSV.
df.to_csv("td_clustering_karafun_regroupe.csv", index=False)
print("\nFichier enregistré : td_clustering_karafun_regroupe.csv")
