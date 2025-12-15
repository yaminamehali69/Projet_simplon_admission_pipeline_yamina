import sqlite3
import os
import time
from datetime import datetime

# Import des modules locaux
from create_schema_and_test import create_schema as run_schema_creation
from importation_data import run_import_logic
from analyse_data import run_analyse 

# Chemin de la BDD (Docker)
DB_PATH = os.environ.get('DB_PATH', '/app/data/pme_num_ventes.db')

def main_pipeline():
    conn = None
    try:
        print("==============================================")
        print(" Démarrage du Pipeline ETL : Final")
        print("==============================================")

        conn = sqlite3.connect(DB_PATH)
        print(f" Base de données utilisée : {DB_PATH}")
        print(" Connexion SQLite établie.\n")

        # 1️⃣ Création du schéma
        print(" E:1/3 Création du schéma...")
        run_schema_creation(conn)
        print(" Schéma créé.\n")

        # 2️⃣ Importation des données CSV (avec DROP TABLE pour éviter les conflits)
        print(" E:2/3 Importation des données CSV...")
        run_import_logic(conn)
        print(" Importation terminée.\n")

        # 3️⃣ Analyse & résultats
        print(" E:3/3 Analyse des données...")
        run_analyse(conn)
        print(" Analyse terminée.\n")

        print("==============================================")
        conn.close()
        print("\n--- Pipeline ETL Complet  ---")
        print("==============================================")

        
    except Exception as e:
        print(f" ÉCHEC CRITIQUE DU PIPELINE: {e}")
        time.sleep(5)
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    main_pipeline()
