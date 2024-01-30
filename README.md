# DataEngineering Projet étude des performances à Fort Boyard
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Scrapy](https://img.shields.io/badge/Scrapy-%2314D08C.svg?style=for-the-badge&logo=scrapy&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white)

## Description
L'objectif de ce projet est d'étudier les performances des équipes participant à la mythique émission TV Fort Boyard. 

Pour cela nous récupérons les informations par WebScraping avec la librairie Scrapy sur le site [https://o.fortboyard.tv/gains.php#parsaison](https://o.fortboyard.tv/gains.php#parsaison), et nous les compilons dans un fichier json.  

Ensuite ce fichier json est importé dans une base MongoDB pour avoir un meilleur contrôle sur l'accès des données.

Enfin nous extrayons les données qui nous intéressent et les visualisons avec la librairie plot dans un dashboard implémentée grâce à la librairie dash.

Chaque étape du projet est isolée dans un container Docker.

Le projet est managé grâce à un docker compose.

Le dossier __natif__ contient :

* Les programmes non conteneurisés

* Les fichiers contenant les librairies nécessaires (Pipfile et requirements.txt) au fonctionnement des programmes.

## Pré-requis
Ce projet nécessite l'utilisation de Docker. S'il n'est pas déjà téléchargé :

* [Pour Windows](https://docs.docker.com/desktop/install/windows-install/)

* [Pour Linux](https://docs.docker.com/desktop/install/linux-install/)

* [Pour Mac](https://docs.docker.com/desktop/install/mac-install/)


## Guide d'installation
Dans un terminal de commandes, commencez par vous déplacer vers le dossier où sera enregistré le projet avec la commande :

``
cd chemin_vers_le_dossier_de_votre_choix
``

Cloner le projet avec la commande:

``
git clone https://github.com/RyanKHOU/Project_DataEngineering_Khou_Le.git
``

Créer les containers et les images du projet avec la commande (à la racine du projet)

``
docker-compose build 
``

Lancer  l'exécution du projet avec la commande 

``
docker-compose up -d
``

## Guide d'utilisation
* main.py
* data_collectinng.py
* data_cleaning.py
* data_filtering.py
* vizualisation.py
