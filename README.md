# Systeme-Expert
L’objectif est de concevoir et réaliser un système expert d’aide au diagnostic de pannes d’un ordinateur.

Instructions de configuration
1. Clonez ce dépôt sur votre machine locale.
2. Accédez au répertoire du projet.
3. Installez Flask à l'aide de pip si ce n'est pas déjà fait :
   ```
   pip install Flask
   ```
4. Lancez l'application Flask :
   ```
   python app.py
   ```
5. Ouvrez un navigateur web et accédez à http://127.0.0.1:5000 pour accéder à l'application.
# Description
Ce système expert utilise une approche basée sur des règles pour diagnostiquer les problèmes de PC. Les règles sont stockées dans un fichier nommé base.txt, où chaque ligne représente une règle au format symptôme:composant_affecté. L'application permet aux utilisateurs de sélectionner plusieurs symptômes dans une liste, et en cliquant sur le bouton "Effectuer le diagnostic", elle analyse les symptômes sélectionnés par rapport aux règles stockées pour déterminer les composants potentiellement défectueux.
# Fichiers du projet:
 ## 1. app.py:
   Ce fichier contient le code Python pour l'application Flask. Il définit les routes pour le serveur web, gère les requêtes utilisateur et orchestre la logique de diagnostic. 
 ## 2.  index.html: 
 C'est le fichier HTML qui définit l'interface utilisateur. Il contient une liste de symptômes à sélectionner et un bouton pour lancer le diagnostic.
 ## 3. base.txt:
 Ce fichier texte contient les règles utilisées par le système expert pour le diagnostic. Chaque ligne représente une règle avec un symptôme et le composant affecté.
## 4.expert.html :
Cela permet à l'utilisateur d'interagir avec le système expert en ajoutant de nouvelles règles, en modifiant des règles existantes ou en supprimant des règles de la base de connaissances.
## 5. symptomes.html : 
cette page permet à l'utilisateur de sélectionner les symptômes observés sur l'ordinateur et de demander un diagnostic au système expert en cliquant sur un bouton. Le système répond ensuite avec le résultat du diagnostic.
