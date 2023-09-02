# BOT Maintenance

C'est un bot telegram qui gère les différentes types de maintenances au sein de l'assiociation ViaRézo du campus de CentraleSupélec. 

## Librairies utilisées 

sqlite3 - telegram - telegram.ext

## Fichiers et fonctionalités 

**database.db** : 
Pour identifier l'ensembles des informations de maintenance, on utilise un tableau SQL ayant les colonnes suivantes :
- id : un entier unique pour chaque maintenance incrémenté par 1.
- name : un nom court mais aussi descriptif.
- procedure : procédure effectué lors de la maintenance.
- date : date de la maintenance sous forme jj-mm-aa.
- length : durée de la maintenance en nombre d'heures.
- owner : le propriétaires qui a créé la maintenance (par défaut on prend l'@ telegram du créateur).
- members : les membres participants à cette maintenance.
- risk_lvl : le niveau du risque exprimé par un entier entre 0 et 5.
- risk_cmt : commentaire sur le risque/downtime de la maintenance.
- comment : commentaire général.
- tags : tags réseau, vm, infra..etc.

**bot.py** : 
Fichier qui gére la database en utilisant sqlite3. 
On définit une classe *logs* représentant notre tableau de maintenances : 
 - init() : Crée une table sql (si elle n'existait pas déjà) appelée maintenances.
 - add(*args*) : Ajoute une ligne (maintenance) dans la table ayant comme atrribues les *args*.
 - latest() : Retourne les 3 dernières lignes.
 - edit(*id*, *edits*) : Modifie la maintenance ayant l'*id* précisé avec les modifications *edits*



**main** : 
Fichier principal qui s'occupe de l'interaction du bot avec les utilisateurs (membres de l'associations). 





