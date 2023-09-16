# BOT Maintenance

C'est un bot telegram qui gère les différentes types de maintenances au sein de l'assiociation ViaRézo du campus de CentraleSupélec. 

## Librairies utilisées 

sqlite3 - telegram - telebot - python-telegram-bot

## Fichiers et fonctionalités 

**database.db** : 
Pour identifier l'ensembles des informations de maintenance, on utilise un tableau SQL ayant les colonnes suivantes :

| Colonne/attribue              | Valeur par défaut                       | Description                                                  |
|-------------------------------|-----------------------------------------|--------------------------------------------------------------|
| id                            | max(id) from maintenances + 1           | Un entier unique pour chaque maintenance incrémenté par 1.   |
| name                          |                                         | Un nom court mais aussi descriptif de la maintenance.        |
| procedure                     |                                         | Procédure effectué lors de la maintenance.                   |
| date                          |                                         | Date de la maintenance sous forme jj/mm/aa.                  |
| length                        |                                         | Durée de la maintenance en nombre d'heures.                  |
| owner                         | username du créateur de la maintenance  | Le propriétaires qui est responsable de la maintenance.      |
| members                       |                                         | Les membres participants à cette maintenance séparés par '-'.| 
| risk_lvl                      |                                         | Le niveau du risque exprimé par un entier entre 0 et 5.      |
| risk_cmt                      | string vide                             | Commentaire sur le risque/downtime de la maintenance.        |
| comment                       | string vide                             | Commentaire général.                                         |
| tags                          | string vide                             | Tags comme : réseau, vm, infra..etc.                         |

**bot.py** : 
Fichier qui gére la database en utilisant sqlite3.  
On définit une classe *logs* qui représente notre tableau de maintenances où on peut le manipuler à travers plusieurs fonctions comme:  
 - init() : Crée une table sql (si elle n'existe pas déjà) appelée maintenances.
 - add(*args*) : Ajoute une ligne (maintenance) dans la table ayant comme atrribues les *args*.
 - latest() : Retourne les 3 dernières lignes.
 - edit(*id*, *edits*) : Modifie la maintenance ayant l'*id* précisé avec les modifications *edits*


**main** : 
Fichier principal qui s'occupe de l'interaction du bot avec les utilisateurs (membres de l'associations). 
Il intéragit avec l'utilisateur à travers plusieurs fonctions et *conversations* : 

- /start : Montre un clavier qui suggère des commandes utiles du bot.
- /help : Donne une description courte des commandes du bot.
- /add : Commence la conversation *add* pour ajouter une maintenance.
- /get : Commence la conversation *get* pour visualiser une maintenance dont vous connaisez le nom.
- /latest : Donne directement les 3 dernières maintenance enrigistrées.
- /edit : Commence la conversation *edit* pour modifier une maintenance dont vous connaissez l'id.
- /delete : Commence la conversation *delete* pour supprimer définitivement une maintenance dont vous connaissez l'id.
- /cancel : Annule la conversation au courant.

## Structure des conversations :

**Conversation ADD** 

<img src="./diagrammes/add_conv.jpg?raw=true" /> 

**Conversation GET** 

<img src="./diagrammes/get_conv.jpg?raw=true" /> 

**Conversation EDIT** 

<img src="./diagrammes/edit_conv.jpg?raw=true" /> 

**Conversation DELETE** 

<img src="./diagrammes/delete_conv.jpg?raw=true" /> 

## Execution en local : 

**1. Clone Repo**

```bash
git clone https://gitlab.viarezo.fr/2022ouchnaya/bot_maintenance.git
```

**2. Installations**

```bash
py -m pip install telegram
py -m pip install telegram.ext
```

**3. Configurer le token de votre bot**

Ouvrir le fichier txt *TOKEN.txt*  et écrire votre token donné par [Botfather](https://t.me/Botfather)

**4. Executer le code**

Executer le fichier *main.py*  et c'est bon!

## A venir :
=> Construire un système d'autorisation d'accès pour les utilisateurs (*monitoring.py*).



