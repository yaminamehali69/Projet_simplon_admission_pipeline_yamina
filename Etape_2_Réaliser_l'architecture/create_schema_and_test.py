import sqlite3 ## Permet de se connecter et manipuler une base de données SQLite "créer des tables, insérer, lire des données"
import os ###permet d'intérargir avec le système d'explotation , lire les variable d'envi comme le db_path 
from tabulate import tabulate ## permet d'afficher correctement les tableaux 

DB_PATH = os.environ.get('DB_PATH', '/app/data/pme_num_ventes.db')  ### Cette ligne permet de définir le chemin de la base de données à partir d’une variable d’environnement l'os , avec une valeur par défaut si elle n’est pas définie

print("\n--- Démarrage du Service Python : Création du Schéma ---")
print(f"Hello-World Yamina : Connexion au chemin BDD : {DB_PATH}")  ##  Sert de test visuel pour vérifier que DB_PATH est bien chargé

def create_schema(conn): ### def les fonctions qui sert à créer ou configurer le schéma de la  bdd à partir d’une connexion SQLite
    cursor = conn.cursor() 
    cursor.execute("PRAGMA foreign_keys = ON;")

    print("\n--- 1. CRÉATION DU SCHÉMA (Étape 3.2) ---")

    # TABLE MAGASINS ## permet d'exécuter les créations de schéma des tables 
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS magasins (
        id_magasin INTEGER PRIMARY KEY,
        ville TEXT NOT NULL,
        nombre_de_salaries INTEGER
    );
    ''')

    # TABLE PRODUITS
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS produits (
        nom TEXT NOT NULL,
        id_reference_produits TEXT PRIMARY KEY,
        prix REAL NOT NULL,
        stock INTEGER
    );
    ''')

    # TABLE VENTES (Tables et références tout en minuscules pour la cohérence)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ventes (  
        id_vente INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        quantite INTEGER NOT NULL,
        id_reference_produits TEXT,
        id_magasin INTEGER,
        FOREIGN KEY(id_reference_produits) REFERENCES produits(id_reference_produits), 
        FOREIGN KEY(id_magasin) REFERENCES magasins(id_magasin)
    );
    ''')

    # TABLE ANALYSE RESULTATS (Nom de table et colonnes en minuscules pour la cohérence)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS analyse_resultats (
        id_analyse INTEGER PRIMARY KEY AUTOINCREMENT,
        ville TEXT,
        CA_Total_Region REAL,
        Date_Analyse TEXT
    );
    ''')

    conn.commit() ### permet de confirmer les modifications et la création du schéma dans la  bdd
    print(" Schéma créé .")

    # Diagnostic des noms de tables en minuscules, permet de vérifier que les tables existent bien , afficher la structure de chaque table et analyser rapidement un problème de schéma "erreur de type, colonne manquante"
    print("\n--- Vérification des structures SQL ---")
    for table in ['magasins', 'produits', 'ventes', 'analyse_resultats']:
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()
        print(f"\n-- Structure de la table {table}:")
        print(tabulate(columns, headers=["cid", "name", "type", "notnull", "dflt_value", "pk"], tablefmt="fancy_grid"))

### ce bloc permet  de tester le script en local et empêche l’exécution auto quand le fichier est importé
if __name__ == '__main__':
    conn = None
    try:
        print("\n--- Mode Test Local ---")
        conn = sqlite3.connect(DB_PATH)
        create_schema(conn)
    except sqlite3.Error as e:
        print(f" Erreur SQLite lors du test local : {e}")
    finally:
        if conn:
            conn.close()
            print(" SQLite fermée.")