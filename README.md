# BOT Telegram de maintenances de ViaRézo

C'est un bot telegram qui gère les différentes types de maintenances au sein de l'assiociation ViaRézo du campus de CentraleSupélec.  

## Fichiers et fonctionalités 

**main** : 
Fichier principal qui s'occupe de l'interaction du bot avec les utilisateurs 

/maintenace (sans argument) : va récupérer toutes les informations de maintenace  en cours ou s'il y en a pas de la prochaine
/maintenance list : fournit la liste des identifiants des maintenaces en cours ou futurs
/maintenance ( avec argument = identifiant de la maintenance) : va récuprérer les informations de cette maintenance spécifiquement 

**monitoring** :
Ce fichier va permettre de gérer l'ensemble des autorisations de modifications d'erreurs, d'ajout de personnes capables d'éffectuer les maintenances
/add : va fournir une liste des élèments à saisir pour compléter la création d'une maintenance
/edit list : fournit la liste des élèments à modifer
/edit ( avec argument= élèment dans la liste) : bot envoie une nouvelle question de ce qu'on veut modifier
/argument choisi : la modofication
/suscribe (argument) : ajouter le nom à la liste des memebres pour la maintenance choisie


**python** : 
On a une classe Bot avec les propriétes suivantes:

**database** : 
Pour identifier l'ensembles des informations de maintenance on va introduire  l'Entité maintenance avec les attributs suivants:
-type
-date_heure
-duree
-membres
-nom
-deroule
-echelle_de_risque
-commentaire_risque
-tag
-identifiant
-proprietaire


