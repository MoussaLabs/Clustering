# Guide du dépôt — Clustering des abonnés KaraFun

Ce document explique comment le dépôt est organisé, à quoi sert chaque fichier, dans quel ordre tout s'enchaîne et quels résultats on obtient. Il suffit pour reprendre le projet sans avoir suivi le travail.

---

## 1. Le projet en bref

**Demande** : le marketing de KaraFun veut connaître le profil de ses abonnés, pour adapter ses actions de fidélisation et d'acquisition.

**Réponse** : une typologie de **6 segments**, construite selon la méthode du cours en 3 étapes :

| Étape du cours | Ce qu'on fait | Où dans le dépôt |
|---|---|---|
| 0. Prise en main | contrôles, statistiques descriptives, regroupement des modalités | `notebooks/analyse_avant_acm_v2.ipynb` (parties 1 à 10) |
| 1. Analyse factorielle | ACM pour choisir les variables et obtenir des coordonnées | `analyse_avant_acm_v2.ipynb` (parties 11 à 14) + `classification_affectation.ipynb` (partie 2) |
| 2. Classification | CAH puis nuées dynamiques (classification mixte) | `classification_affectation.ipynb` (parties 3 à 5) |
| 3. Affectation | régression logistique : donner un segment à chaque client | `classification_affectation.ipynb` (partie 6) |

---

## 2. Arborescence

```
Clustering/
├── README.md                     présentation rapide + commandes
├── docs/
│   ├── Cours Clustering.pdf      cours et consignes (livrables, planning)
│   ├── TD-TP Clustering.pages    énoncé du TD
│   ├── Explication_analyse_avant_ACM.docx   support oral du notebook v2 (étapes avant l'ACM)
│   └── GUIDE_REPO.md             ce document
├── data/
│   ├── raw/
│   │   ├── td_clustering_karafun.csv    données d'origine (341 092 clients, 16 colonnes)
│   │   └── td_clustering_karafun.xlsx   même chose en Excel
│   └── processed/
│       ├── td_clustering_karafun_regroupe.csv   sortie de src/regroupements.py (ancienne version, non utilisée ensuite)
│       ├── td_clustering_karafun_modifie.xlsx   sortie du notebook v2 : base nettoyée et regroupée (341 069 clients)
│       └── clients_segments.csv                 RÉSULTAT FINAL : le segment de chaque client
├── notebooks/
│   ├── analyse_avant_acm.ipynb          v1 : analyse avant ACM, très commentée, s'arrête à l'ACM de test
│   ├── analyse_avant_acm_v2.ipynb       v2 : même analyse + ACM sur échantillon et choix des variables
│   └── classification_affectation.ipynb  ACM finale, CAH, k-means, description, affectation
├── src/
│   ├── stats_descriptives.py     premières stats descriptives (script autonome)
│   └── regroupements.py          première version des regroupements (script autonome)
├── sas/
│   └── pgm_clustering.sas        programme SAS modèle du cours (étapes 1 à 6), non adapté
└── outputs/figures/              graphiques produits
```

---

## 3. Les données

Une ligne = un abonné. Toutes les variables sont qualitatives (en tranches), sauf `nb_abo_periode` (nombre de 1 à 12).

| Variable | Sens |
|---|---|
| `id_anonyme` | identifiant de l'abonné |
| `anciennete_client_tr` | ancienneté depuis le tout premier abonnement |
| `anciennete_abonnement_tr` | ancienneté du cycle d'abonnement en cours |
| `statut_abonnement` | actif / non actif |
| `type_client` | nouveau / retained / reactivated / churn |
| `type_very_first_abo` | nature du tout premier abonnement (payant / réduc / offert) |
| `type_first_abo_last_streak` | nature du premier abonnement du cycle en cours |
| `ratio_fidelite_tr` | part des mois où le client a été abonné depuis le début |
| `methode_paiement` | Stripe, Apple, Android, Paypal, Amazon… |
| `nb_abo_periode` | nombre de mois abonnés sur les 12 mois observés |
| `valeur_12M_tr` | valeur générée sur la période |
| `avg_sessions_actifs_tr` | sessions moyennes par mois actif |
| `avg_songs_sessions_tr` | chansons moyennes par session |
| `utilise_remote` | a déjà utilisé la fonction remote |
| `zone_geo` | zone géographique |
| `contactable` | accepte d'être contacté (absente du tableau du cours, présente dans le fichier) |

---

## 4. Ordre d'exécution

Les notebooks s'exécutent **depuis le dossier `notebooks/`** (chemins en `../data/...`). Les scripts de `src/` s'exécutent **depuis la racine**.

1. `notebooks/analyse_avant_acm_v2.ipynb` → crée `data/processed/td_clustering_karafun_modifie.xlsx`
2. `notebooks/classification_affectation.ipynb` → lit ce fichier, crée `data/processed/clients_segments.csv` et les figures `cah_*.png`, `clusters_*.png`

Les scripts `src/*.py` et le notebook v1 ne sont **pas nécessaires** à la chaîne finale (voir §5).

Dépendances : `pandas numpy scipy scikit-learn matplotlib openpyxl`.
Tous les tirages aléatoires sont fixés (`random_state`) : les résultats sont identiques à chaque exécution.

---

## 5. Fichier par fichier

### 5.1 `src/stats_descriptives.py`

Premier contact avec la base.
- Taille, types, valeurs manquantes, doublons d'identifiant.
- `nb_abo_periode` : description et répartition de 1 à 12 (distribution en U).
- Effectifs et % de chaque modalité de chaque variable.
- Un tableau croisé `type_client × statut_abonnement`.
- Sortie : `outputs/figures/stats_descriptives.png` (un diagramme en barres par variable).

### 5.2 `src/regroupements.py`

**Première version** des regroupements de modalités, faite avant l'analyse détaillée. Elle écrit `data/processed/td_clustering_karafun_regroupe.csv`.

⚠️ Elle a été **remplacée par le notebook v2**, qui a testé et corrigé ces regroupements. Différences principales :

| | `regroupements.py` | notebook v2 (version retenue) |
|---|---|---|
| `valeur_12M_tr` | 6 classes (90-110 fusionnée avec 110+) | 7 classes (90-110 gardée seule) |
| `avg_sessions_actifs_tr` | 2-3 seule, 3-5, 5+ | 2-5 ensemble, 5-10, 10+ |
| `methode_paiement` | Amazon + Credit + Others = « Autre » | Others supprimé, Credit → Stripe, Amazon → Android |
| `zone_geo` | Autre/Inconnu dans Reste_du_monde | Autre/Inconnu supprimé (22 clients) |
| `type_first_abo_last_streak` | non regroupé | offert + réduc regroupés |

Le CSV qu'il produit n'est **pas utilisé** par la suite.

### 5.3 `notebooks/analyse_avant_acm.ipynb` (v1)

Version longue et très commentée de l'analyse avant ACM (parties 1 à 12). Utile pour **comprendre le raisonnement** : chaque regroupement y est justifié en détail, avec un tableau récapitulatif des décisions (partie 9.6). Elle s'arrête à une ACM de test sur toute la base.

### 5.4 `notebooks/analyse_avant_acm_v2.ipynb` (v2) — étape 0 et 1

Même analyse en plus concis, **plus** l'ACM sur échantillon et le choix final des variables. C'est la version qui alimente la suite. Le document `docs/Explication_analyse_avant_ACM.docx` en est le support oral.

**Parties 1-3 : contrôles.** 341 092 lignes, 16 colonnes, aucune valeur manquante, aucun doublon. `nb_abo_periode` en U : 28,5 % à 1 mois, 21 % à 12.

**Partie 4 : modalités rares.** Repérage des modalités sous 5 %. Raison : en ACM, une modalité rare pèse trop et peut créer un axe à elle seule.

**Parties 5-7 : liens entre variables (V de Cramér).** Avec 341 000 lignes le khi-deux est toujours significatif, donc on mesure la force des liens avec le V de Cramér (0 = aucun lien, 1 = même information). Constats :
- `statut_abonnement` × `type_client` : V = 1 (churn = non actif) → `statut_abonnement` retirée.
- `methode_paiement` × `type_first_abo_last_streak` : V = 0,64, dû à la seule modalité Credit (0,2 %).
- `nb_abo_periode` × `valeur_12M_tr` : V = 0,63.
- les clients de moins d'un mois = les « vient de s'abonner » ; les « pas de session » sont les mêmes dans les deux variables d'usage.

**Partie 8 : conclusion avant regroupement.** Quelles variables retirer, lesquelles mettre en illustratives.

**Partie 9 : regroupements** (sur une copie `df2`). Règles :
1. on ne fusionne que des tranches voisines ;
2. sous 2 % : toujours fusionnée ;
3. entre 2 et 5 % : fusionnée seulement si elle ressemble à sa classe ;
4. au-dessus de 5 % : on fusionne pour avoir 5 à 7 modalités.

La ressemblance est mesurée par l'écart de profil entre deux modalités sur toutes les autres variables (fonctions `ecart`, `ecarts_voisins`, `ecarts_classes`). Résultat : 23 lignes supprimées, **341 069 clients**, enregistrés dans `td_clustering_karafun_modifie.xlsx`.

**Partie 10 : V de Cramér après regroupement.** La plupart des liens bougent de moins de 0,05 : les regroupements ne déforment pas les données. `valeur × nb_abo` monte à 0,84 (presque redondantes).

**Partie 11-12 : ACM de test** (toute la base, 11 variables actives). L'ACM est codée à la main à partir du tableau de Burt (équivalent de `proc corresp mca benzecri`). Axe 1 = engagement ; axe 2 = effet Guttman (le milieu contre les extrêmes) ; axe 3 = clients sans session.

**Partie 13 : ACM sur un échantillon de 20 %** (`random_state=1`, 68 214 clients, représentatif à 0,3 point près). Trois ACM successives pour choisir les variables actives :
- ACM 1 (11 variables) : `methode_paiement`, `zone_geo`, `type_very_first_abo` ne construisent aucun axe → illustratives ; `avg_songs_sessions_tr` ne contribue que par « pas de session », déjà comptée → illustrative. Deux regroupements en plus : ancienneté client 25 mois et plus, sessions 1 à 5.
- ACM 2 (7 variables) : `avg_sessions_actifs_tr` et `utilise_remote` ne construisent plus rien → illustratives.
- ACM 3 (5 variables) : toutes contribuent.

**Partie 14 : bilan.** Variables actives retenues :
`anciennete_client_tr`, `anciennete_abonnement_tr`, `ratio_fidelite_tr`, `nb_abo_periode`, `valeur_12M_tr`.

### 5.5 `notebooks/classification_affectation.ipynb` — étapes 1 (fin), 2 et 3

**Partie 1 : reconstruction de l'échantillon.** Relit `td_clustering_karafun_modifie.xlsx`, refait le même tirage de 20 % (on retrouve les 68 214 clients) et les deux regroupements de la partie 13.4 (fonction `regroupements_acm`).

**Partie 2 : ACM finale.**
- Fonction `acm` (reprise du v2) + `coord_clients` (coordonnées de chaque client).
- Choix du nombre d'axes avec les 3 critères du cours :

| Critère | Axes |
|---|---|
| au-dessus de l'inertie moyenne (4,35 %) | 9 (trop généreux en ACM) |
| 50 % d'inertie cumulée | 5 |
| 95 % d'inertie corrigée de Benzécri | 5 |

→ **5 axes** (50,7 % / 18,9 % / 12,5 % / 8,1 % / 6,5 % Benzécri).
- Description des 4 premiers axes : 1 = engagement (1 mois et moins de 10 contre 12 mois et 70 et plus) ; 2 = le milieu (4-6 mois) contre les extrêmes et les nouveaux ; 3 = les clients qui débutent contre ceux arrivés il y a 6-12 mois ; 4 = les testeurs à 2-3 mois.
- Chaque client reçoit 5 coordonnées. Il n'y a que 607 profils différents parmi 68 214 clients.

**Partie 3 : CAH (choix du nombre de classes).**
- Une CAH sur 68 214 clients demanderait environ 18 Go de mémoire. On la fait donc (méthode de Ward) sur **10 000 clients** tirés dans l'échantillon, et deux fois (deux tirages) pour vérifier.
- Indicateurs : dendrogramme, R², R² semi-partiel (SPRSQ), pseudo-F. Le CCC est propre à SAS et n'existe pas en Python.
- **6 classes** : le SPRSQ chute de 11,4 % (6 → 5 classes) à 3,6 % (7 → 6), R² = 0,80 à 6 classes, et le pseudo-F fait un grand saut entre 5 et 6 classes.

**Partie 4 : nuées dynamiques (consolidation).**
- k-means sur les 68 214 clients, en partant des 6 centres de la CAH : 3 itérations, 123 clients déplacés (0,2 %), **R² = 0,81**.
- Stabilité (ARI, 1 = identique) : sous-échantillon 1 contre 2 = 1,000 ; avec des k-means au hasard = 0,998.
- Renumérotation des classes selon leur position sur l'axe 1 (engagement).

**Partie 5 : description des classes.**
- Khi-deux + V de Cramér entre la classe et chaque variable : `nb_abo_periode` 0,94, `valeur` 0,77, `type_client` 0,62 (illustrative !), usage/paiement/zone ≤ 0,21.
- Profils détaillés (% de chaque modalité par classe), tableau de synthèse, carte de chaleur, portraits.

**Partie 6 : affectation.**
- Régression logistique multinomiale (équivalent de `proc logistic link=glogit`) sur les 5 variables actives. Apprise sur 70 % de l'échantillon, testée sur 30 % : **99,89 %** de bien classés.
- Comparée à une règle simple (nombre de mois abonnés) : 95,5 %.
- Appliquée à **toute la base** (341 069). Sur les 272 855 clients hors échantillon (les 80 %), même segment que la méthode de référence (projection sur l'ACM + centre le plus proche) pour 99,89 % ; même répartition des segments qu'avec l'échantillon.
- Sortie : `data/processed/clients_segments.csv` (`id_anonyme`, `cluster`, `segment`).

**Partie 7 : bilan et limites.**

### 5.6 `sas/pgm_clustering.sas`

Programme SAS **modèle** fourni avec le cours (import, `proc freq`, échantillon, `proc corresp`, `proc cluster`, `proc tree`, SPRSQ/CCC, macro de lecture des classes, `proc logistic`). Il n'a **pas été adapté** : il travaille sur les données brutes et toutes les variables. Le travail réel est fait en Python, avec la même logique. Pour le lancer : changer `chemin_fichier` (ligne 11) dans SAS OnDemand.

### 5.7 `outputs/figures/`

| Fichier | Contenu |
|---|---|
| `stats_descriptives.png` | répartition de chaque variable (script `stats_descriptives.py`) |
| `cah_dendrogramme.png` | dendrogramme de la CAH, coupure à 6 classes |
| `cah_indicateurs.png` | R², SPRSQ et pseudo-F de 2 à 10 classes, sur les deux sous-échantillons |
| `clusters_plan_acm.png` | les 6 classes sur le plan 1-2 de l'ACM |
| `clusters_profils.png` | carte de chaleur des profils (churn, retained, usage, US, contactable) |

---

## 6. Résultats : les 6 segments

Chiffres sur la base complète (341 069 clients). La valeur est estimée au milieu de chaque tranche de `valeur_12M_tr`.

| # | Segment | Clients | Valeur estimée | Ce qui le définit | Statut |
|---|---|---|---|---|---|
| 1 | Nouveaux arrivants | 22 659 (6,6 %) | 0,8 % | 1 mois, arrivés il y a moins de 3 mois | 60 % nouveaux, 40 % déjà partis ; 73 % contactables |
| 2 | Partis après un mois | 70 497 (20,7 %) | 2,6 % | 1 seul mois, moins de 10 de valeur | 97 % churn ; 17 % sans aucune session |
| 3 | Testeurs | 63 509 (18,6 %) | 7,9 % | 2 à 3 mois, 10 à 20 de valeur | 69 % churn |
| 4 | Intermédiaires | 49 540 (14,5 %) | 11,1 % | 4 à 6 mois, 20 à 40 de valeur | 57 % churn, 20 % réactivés |
| 5 | Réguliers | 62 446 (18,3 %) | 29,0 % | 7 à 11 mois, 40 à 70 de valeur | 37 % réactivés, 46 % US |
| 6 | Fidèles | 72 418 (21,2 %) | 48,6 % | 12 mois sur 12, plus de 70 de valeur | 88 % retained ; plus gros utilisateurs ; 51 % contactables |

**Règle simple** (juste à 95,5 %) : 12 mois → Fidèle ; 7-11 → Régulier ; 4-6 → Intermédiaire ; 2-3 → Testeur ; 1 mois → Nouvel arrivant si client depuis moins de 3 mois, sinon Parti après un mois.

**Préconisations principales** : réussir le premier mois (segments 1-2), allonger les abonnements avec l'offre annuelle et une option pause (segments 3-5), reconnaître les fidèles et en faire des parrains (segment 6). Côté transverse : passer par l'application pour joindre les non-contactables, recalculer les segments chaque mois.

---

## 7. Limites à connaître

- **Typologie d'engagement, pas d'usage** : le segment dépend surtout du nombre de mois abonnés (V = 0,94). C'est la conséquence du choix des variables actives : les variables d'usage ne construisaient aucun axe.
- **`nb_abo_periode` et `valeur_12M_tr` presque redondantes** (V = 0,84) : en retirer une est une variante à tester.
- **Photo sur 12 mois** : un client peut changer de segment, d'où l'affectation mensuelle.
- **Valeur estimée** : un ordre de grandeur, pas un chiffre comptable.

---

## 8. Livrables (hors dépôt)

- **Rapport** (étude + partie technique) : document Claude Docs, exportable en Word ou PDF.
- **Présentation marketing** : deck de 12 slides avec notes orateur, exportable en .pptx.
- Nommage demandé : `G1_B9_NOM1_NOM2_rapport` / `..._prez` (noms par ordre alphabétique), à envoyer à la responsable du cours.
