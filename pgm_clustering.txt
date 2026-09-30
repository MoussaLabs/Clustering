/* ================================================================
   TD CLUSTERING M2 SIAD — Segmentation des abonnés KaraFun Premium
   Programme complet (Etapes 1 a 6)
   ================================================================ */


/* ================================================================
   PARTIE 1 : IMPORTATION ET STATISTIQUES DESCRIPTIVES
   ================================================================ */

%let chemin_fichier = /home/ldap/TON_LOGIN/td_clustering_karafun.csv;

proc import datafile="&chemin_fichier."
    out=clustering_karafun_export
    dbms=csv
    replace;
    getnames=yes;
    guessingrows=max;
run;

proc contents data=clustering_karafun_export; run;

proc print data=clustering_karafun_export (obs=10); run;


*Etape 2: Statistiques descriptives de la base (statistiques simples - croisées);

proc freq data=clustering_karafun_export;
    table
        statut_abonnement
        type_client
        type_very_first_abo
        type_first_abo_last_streak
        methode_paiement
        nb_abo_periode
        anciennete_client_tr
        anciennete_abonnement_tr
        valeur_12M_tr
        avg_sessions_actifs_tr
        avg_songs_sessions_tr
        utilise_remote
        zone_geo
        / missing;
run;

proc freq data=clustering_karafun_export;
    table type_client * statut_abonnement
          type_client * anciennete_client_tr
          type_client * anciennete_abonnement_tr
          type_client * valeur_12M_tr
          type_client * avg_sessions_actifs_tr
          type_client * avg_songs_sessions_tr
          type_client * methode_paiement
          type_client * zone_geo
        / missing chisq;
run;

/* A partir d'ici : à vous de construire les croisements que vous jugez
   pertinents avec d'autres variables pivot (au-delà de type_client), pour
   identifier les modalités à regrouper avant l'ACM. */


/* ================================================================
   PARTIE 2 : ECHANTILLONNAGE ET ACM
   ================================================================ */

*Etape 3: Création échantillon préalable à l'ACM;

proc sql noprint;
    select count(*) into :nb_total
    from clustering_karafun_export;
quit;

%let n_ech = %sysfunc(round(%sysevalf(&nb_total. * 0.2)));

data clustering_karafun_export;
set clustering_karafun_export;
alea=uniform(0);
run;

proc sort data=clustering_karafun_export;
by alea;
run;

data wrk.cm_karafun_ech;
set clustering_karafun_export (obs=&n_ech.);
run;



*Etape 4a: ACM exploratoire (sans les individus);

/* Ce premier passage sert uniquement à analyser les modalités des variables
   (valeurs propres, contributions, qualité de représentation) pour décider
   quelles variables garder et quelles modalités regrouper. Pas d'individus
   à ce stade -> option mca seule, pas de CAH possible sur cette sortie. */

proc corresp data=wrk.cm_karafun_ech dimens=20 outc=wrk.cm_karafun_recupacm_explo mca benzecri /*noprint*/;
tables
    statut_abonnement
    type_client
    type_very_first_abo
    type_first_abo_last_streak
    methode_paiement
    nb_abo_periode
    anciennete_client_tr
    anciennete_abonnement_tr
    valeur_12M_tr
    avg_sessions_actifs_tr
    avg_songs_sessions_tr
    utilise_remote
    zone_geo
;
run;

*On récupère la sortie de l'ACM exploratoire pour analyse des axes retenus;
data wrk.cm_karafun_analyse_acm (keep=_NAME_ Quality Mass Inertia dim1-dim6 Contr1-Contr6 SqCos1-SqCos6);
set wrk.cm_karafun_recupacm_explo (where=(_TYPE_='VAR'));
run;

/* A ce stade : regarder wrk.cm_karafun_analyse_acm, décider du nombre
   d'axes à retenir, et le cas échéant retravailler la liste de variables
   ci-dessous et/ou regrouper des modalités trop rares avant de relancer
   l'ACM finale ci-après. */


*Etape 4b: ACM finale (avec les individus, sert de base à la CAH);

/* Second passage, une fois les variables/modalités arbitrées : id_anonyme
   est mis en ligne supplémentaire pour que SAS calcule aussi les
   coordonnées des individus (_TYPE_='OBS'), nécessaires pour la CAH en
   partie 3. */

proc corresp data=wrk.cm_karafun_ech dimens=20 outc=wrk.cm_karafun_recupacm /*noprint*/;
tables id_anonyme,
    statut_abonnement
    type_client
    type_very_first_abo
    type_first_abo_last_streak
    methode_paiement
    nb_abo_periode
    anciennete_client_tr
    anciennete_abonnement_tr
    valeur_12M_tr
    avg_sessions_actifs_tr
    avg_songs_sessions_tr
    utilise_remote
    zone_geo
;
run;


/* ================================================================
   PARTIE 3 : CLASSIFICATION CAH ET MODELISATION
   ================================================================ */

* Etape 5: Classification type CAH;

*Récupération des coordonnées des individus sur l'échantillon (phase préalable CAH);

data wrk.cm_karafun_recupacm (keep=id_anonyme dim1-dim20);
set wrk.cm_karafun_recupacm (where=(_TYPE_='OBS'));

length id_anonyme $64.;

id_anonyme=_NAME_;

run;


proc sort data=wrk.cm_karafun_recupacm;
by id_anonyme;
run;

proc sort data=wrk.cm_karafun_ech;
by id_anonyme;
run;

data wrk.cm_karafun_recupacm_ech;
merge wrk.cm_karafun_recupacm (in=p1)
      wrk.cm_karafun_ech (in=p2);
by id_anonyme;
if p1 & p2;
run;

* CAH sur échantillon ;

proc cluster data=wrk.cm_karafun_recupacm_ech method=ward outtree=wrk.cm_tree noprint ;
var dim1-dim6;
id id_anonyme;
run;

* Arbre hiérarchique;

ods html file="seg_cah1_karafun.html";
goptions device=gif;

proc tree data=wrk.cm_tree graphics horizontal;
run;


*****sprsq***** il mesure la perte d'inertie interclasse provoquée en regroupant 2 classes, on choisit le creux après un pic;
proc sort data = wrk.cm_tree ;by _ncl_ ;run;

data sprsq;
set wrk.cm_tree;
by _ncl_;
if first._ncl_;
keep _ncl_ _sprsq_;
run;

proc gplot data=sprsq gout=sprsq_cah1_karafun;
where _ncl_<10 and _ncl_ ne 1;
plot _sprsq_ *_ncl_;
symbol1 i=join;
run;quit;


*****ccc***** on choisit le pic après un creux si >2 alors bonne classif si <0 KO;
proc sort data = wrk.cm_tree ;by _ncl_ ;run;

data ccc;
set wrk.cm_tree;
by _ncl_;
if first._ncl_;
keep _ncl_ _ccc_;
run;

proc gplot data=ccc gout=ccc_cah1_karafun;
where _ncl_<10 and _ncl_ ne 1;
plot _ccc_ *_ncl_;
symbol1 i=join;
run;quit;


* Macro permettant de récupérer les résultats de la CAH à partir du fichier de
  sortie et du nombre de classes : permet de lire le contenu de chaque classe;

%macro resu_cah (tabent=,nb=,ident=,tabvar=,lvar=,tabsort=,fictxt=);

ods html file="seg_cah2_karafun.html";
goptions device=gif;

proc tree data=&tabent out=wrk.cm_cah nclusters=&nb noprint;
run;

data wrk.cm_cah;
set wrk.cm_cah (rename=(_NAME_=&ident));
run;

proc sort data=wrk.cm_cah;
by &ident;
run;

proc sort data=&tabvar;
by &ident;
run;

data tabsort;
merge wrk.cm_cah (in=p1)
      &tabvar (in=p2);
by &ident;
run;

%let nbvar=%eval(%length(&lvar)-%length(%sysfunc(compress(&lvar,' ')))+1);

%do i=1 %to &nbvar;
%let var=%scan(&lvar,&i);

proc summary data=tabsort missing nway;
class &var cluster;
output out=sum_&var;
run;

proc sort data=sum_&var (keep=&var cluster _FREQ_);
by &var;
run;

data wrk.sum_&var.2 (keep=variable modalite clust1-clust&nb);
set sum_&var;
by &var;

length clust1-clust&nb 3 variable modalite $25;

%do j=1 %to &nb;
retain clust&j 0;
%end;

if first.&var then do;
%do j=1 %to &nb;
clust&j=0;
%end;
end;

%do j=1 %to &nb;
if cluster=&j then clust&j=_FREQ_;
%end;

if last.&var;

variable="&var";
modalite=&var;

run;

%end;

data &tabsort;
set %do i=1 %to &nbvar;%let var=%scan(&lvar,&i); wrk.sum_&var.2 %end;;
run;

filename fs "&fictxt..txt";

data _NULL_;
set &tabsort;
file fs delimiter='|';

put variable modalite clust1-clust&nb;
run;


%mend;


%resu_cah (tabent=wrk.cm_tree,nb=6,ident=id_anonyme,tabvar=wrk.cm_karafun_ech,
lvar=statut_abonnement type_client type_very_first_abo type_first_abo_last_streak
methode_paiement nb_abo_periode anciennete_client_tr anciennete_abonnement_tr
valeur_12M_tr avg_sessions_actifs_tr avg_songs_sessions_tr utilise_remote zone_geo
,tabsort=wrk.cm_karafun_resu_cah,fictxt=cm_karafun_resu_cah);
/* nb=6 est une valeur de départ, à ajuster selon les graphiques sprsq/ccc. */

data wrk.cm_karafun_cah_indiv;
set tabsort;
run;



* Etape 6: Modélisation de la classification choisie: régression logistique généralisée;

proc logistic data=wrk.cm_karafun_cah_indiv;
class statut_abonnement type_client type_very_first_abo type_first_abo_last_streak
      methode_paiement nb_abo_periode anciennete_client_tr anciennete_abonnement_tr
      valeur_12M_tr avg_sessions_actifs_tr avg_songs_sessions_tr utilise_remote zone_geo;
model cluster= statut_abonnement type_client type_very_first_abo type_first_abo_last_streak
      methode_paiement nb_abo_periode anciennete_client_tr anciennete_abonnement_tr
      valeur_12M_tr avg_sessions_actifs_tr avg_songs_sessions_tr utilise_remote zone_geo
      /link=glogit;
output out=wrk.cm_pred predprobs=(individual);
score data=clustering_karafun_export out=wrk.cm_class_cah5_5;
run;

proc freq data=wrk.cm_pred; table _from_*_into_/missing;run;