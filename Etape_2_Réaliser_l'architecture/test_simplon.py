
### Etape 2 : Réaliser  l'architecture 
##1.a et 1.b
import os ### permet d'agir avec l'os du conteneur, pour lire les variables d'environnement
import sqlite3 ## permet d'avoir les fonction nécéssaire  pour les connexions, exécutions de commandes SQL
import tabulate  ### C'est une librairie qui va me permettre d'afficher la structure des tables et vérifier leurs contenues. 

DB_PATH = os.environ.get('DB_PATH', '/app/data/pme_num_ventes.db')  ## Elle récupère le chemin du fichier de la BDD,  si  DB_PATH existe elle sera définie dans docker-compose.yml, sinon utilise le chemin  /app/data/pme_service_num_ventes.db


print("\n Démarrage du Service Python ")
print(f"Hello-World yamina : Le script démarre bien ")
print(f"Test de connexion au futur emplacement de la BDD  : {DB_PATH}")

try:
    ## Tente de se connecter au chemin du volume. Mais étant donner que je n'ai pas encore monté le vol, ca ne va pas fonctionner 
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    ### J'ai crée table test  pour prouver que l'écriture est possible dans le volume
    cursor.execute("CREATE TABLE IF NOT EXISTS Test_Volume (id INTEGER PRIMARY KEY, statut TEXT)")
    conn.commit()
    conn.close()
    
    print("✅ Le conteneur Python est fonctionnel et a vérifié l'accès en écriture au volume de la BDD.")
    
except sqlite3.Error as e:
    # je n'ai pas lancer le script docker compose donc il y aura une erreur c normal 
    print(f"ÉCHEC : Erreur SQLite, le volume n'ai pas crée de docker compose : {e}")

print("-----------------------------------\n")







