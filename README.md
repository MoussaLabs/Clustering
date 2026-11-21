# TD Clustering — Segmentation des abonnés KaraFun Premium

Projet de clustering réalisé dans le cadre du M2 DS SIAD.

## Arborescence

```
Clustering/
├── docs/               Cours et énoncé du TD-TP
├── data/
│   ├── raw/            Données d'origine (td_clustering_karafun.csv / .xlsx)
│   └── processed/      Données transformées (regroupements, version modifiée)
├── notebooks/          Analyse exploratoire avant ACM
├── src/                Scripts Python
├── sas/                Programme SAS complet (étapes 1 à 6)
└── outputs/figures/    Graphiques générés
```

## Utilisation

Lancer les scripts **depuis la racine du repo** :

```bash
python3 src/stats_descriptives.py   # stats descriptives -> outputs/figures/stats_descriptives.png
python3 src/regroupements.py        # regroupement des modalités -> data/processed/td_clustering_karafun_regroupe.csv
```

Le notebook `notebooks/analyse_avant_acm.ipynb` s'exécute depuis son propre dossier (chemins en `../data/...`).

Le programme `sas/pgm_clustering.sas` est prévu pour SAS OnDemand : adapter la macro-variable
`chemin_fichier` (ligne 11) à ton espace sur le serveur.

## Dépendances

```bash
python3 -m pip install pandas matplotlib openpyxl
```
