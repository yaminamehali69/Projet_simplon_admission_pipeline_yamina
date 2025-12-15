## Projet d'Analyse des Ventes PME - Pipeline Data Engineer
 Ce projet a été réalisé dans le cadre de ma candidature à la formation Data Engineer chez Simplon et sert de démonstration complète de mes compétences en construction de pipelines de données autonomes et conteneurisés

## Réalisation:

- Création d'un environnement (Docker) : J'ai utilisé Docker pour enfermer le code Python et la base de données SQLite. Cela garantit que le projet fonctionne exactement de la même manière sur n'importe quel ordinateur et rend l'installation très simple.


- Automatisation de l'Importation (ETL) : J'ai développé un programme Python qui gère l'ensemble du processus : il prend les données brutes, les nettoie, et les insère dans la base de données. J'ai aussi mis en place une logique pour éviter les doublons lors des mises à jour.


- Structure de la Base de Données (SQL) : J'ai conçu la structure des tables "Magasins, Produits, Ventes" pour qu'elle soit organisée et fiable. C'est essentiel pour garantir que les calculs sont justes.


- Calcul des Résultats Clés : J'ai écrit des requêtes SQL pour calculer automatiquement les indicateurs importants, comme le CA total, les quantitées vendues par produits ainsi que les ventes par région.


- Mise à disposition des Résultats : Les résultats de l'analyse sont stockés directement dans la uen table appeller "Analyse_résultats, ce qui permet de les utiliser facilement pour des outils de reporting ou de visualisation.


## Langages & Outils : 

Conteneurisation: Docker, Docker Compose

BDD : SQLite, SQL 

Langage Principal: Python

Méthodologie ETL : Extraction, Transformation, Chargement 

Administration et inspection DB : DBeaver
