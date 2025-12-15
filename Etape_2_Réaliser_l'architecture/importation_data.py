
import sqlite3  ## Permet de se connecter et manipuler une base de données SQLite "créer des tables, insérer, lire des données"
import pandas as pd  ### permet de manipuler et analyser des données sous forme de Df "tri, calculs, jointures, export"
import requests ## permet de récup des données depuis des URL ou APi , permet de faire des query HTTP
from io import StringIO  ## permet de lire des csv sous format txt 
from datetime import datetime ##permet de gerer les dates et les heures 


DB_PATH = '/app/data/pme_num_ventes.db'
### bdd présent sur github 
URLS = {
    'Produits': "https://raw.githubusercontent.com/yaminamehali69/Projet_simplon_admission_pipeline_yamina/refs/heads/main/produits.csv",
    'Magasins': "https://raw.githubusercontent.com/yaminamehali69/Projet_simplon_admission_pipeline_yamina/refs/heads/main/magasins.csv",
    'Ventes': "https://raw.githubusercontent.com/yaminamehali69/Projet_simplon_admission_pipeline_yamina/refs/heads/main/ventes.csv",
}
### permet de lire les url 
def collect_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        df = pd.read_csv(StringIO(response.text))
        print(f"   -> {len(df)} lignes téléchargées.")
        return df
    except Exception as e:
        print(f" Erreur des liens HTTP ou lecture CSV : {e}")
        return pd.DataFrame()
### Rendu inutile par le remplacement complet de la table 'ventes', mais conservé
def get_max_date(conn):
    
    try:
        df = pd.read_sql("SELECT MAX(date) AS max_date FROM ventes", conn) 
        value = df.iloc[0, 0]
        return pd.to_datetime(value).date() if value else datetime(1900,1,1).date()
    except:
        return datetime(1900,1,1).date()

def clean_and_normalize_columns(df):
    """Nettoie les noms de colonnes : minuscule, remplace espaces-accents par underscore."""
    df.columns = df.columns.str.lower().str.replace('id ', 'id_').str.replace(' ', '_').str.replace('é', 'e').str.replace('è', 'e').str.replace('à', 'a').str.replace('(', '').str.replace(')', '')
    return df
## Connexion à la base SQLite + activation des clé étrangère 
def run_import_logic(conn):
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    print("\n=== Importation et maj des données =====")
### Récupère les données des produits, magasins et ventes, les nettoie et les met à jour
#  dans la bdd  en s’assurant que toutes les relations entre les tables sont juste 
    #  IMPORt produit 
    print("\n Chargement de la table : Produits")
    df_produits = collect_data(URLS["Produits"])
    if not df_produits.empty:
        df_produits = clean_and_normalize_columns(df_produits)
        # Normalisation de la clé de référence en minuscules avant l'insertion
        df_produits['id_reference_produits'] = df_produits['id_reference_produits'].str.lower()
        df_produits.to_sql("produits", conn, if_exists="replace", index=False) 
        print(" produits importé ")

    # IMPORT mag
    print("\n Chargement de la table : Magasins")
    df_magasins = collect_data(URLS["Magasins"])
    if not df_magasins.empty:
        df_magasins = clean_and_normalize_columns(df_magasins)
        df_magasins.to_sql("magasins", conn, if_exists="replace", index=False)
        print(" Magasins importé ")

    # IMPORT vente
    print("\n Chargement de la table : Ventes")
    df_ventes = collect_data(URLS['Ventes'])
    if df_ventes.empty:
        print(" Aucun fichier ventes récupéré.")
        return

### nettoyage si besoin des colonnes pour homogénisation
    df_ventes = clean_and_normalize_columns(df_ventes)
    
   
    # 1. id_magasin doit être INT 
    df_ventes['id_magasin'] = pd.to_numeric(df_ventes['id_magasin'], errors='coerce').astype('Int64')

    # 2. id_reference_produits doit être en minuscules
    df_ventes['id_reference_produits'] = df_ventes['id_reference_produits'].str.lower()
    
    # --- Vérification de l'intégrité référentielle avant insertion ---
    
    # On lit les IDs valides que nous venons d'insérer (en tenant compte de la casse)
    existing_magasins = pd.read_sql("SELECT id_magasin FROM magasins", conn)['id_magasin'].tolist() 
    existing_produits = pd.read_sql("SELECT id_reference_produits FROM produits", conn)['id_reference_produits'].tolist()

    # On filtre les ventes pour ne garder que celles qui ont des IDs valides.
    df_ventes = df_ventes[
        df_ventes['id_magasin'].isin(existing_magasins) & 
        df_ventes['id_reference_produits'].isin(existing_produits)
    ]

    if df_ventes.empty:
        print(" Aucune vente valide à insérer après nettoyage des IDs.")
        return

    # Insertion complète (REPLACE) pour garantir que toutes les clés sont valides.
    df_ventes.to_sql('ventes', conn, if_exists='replace', index=False)
    conn.commit()
    print(f" {len(df_ventes)} lignes insérées dans ventes (REPLACE).")

if __name__ == '__main__':
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        run_import_logic(conn)
    except Exception as e:
        print(f" echec test: {e}")
    finally:
        if conn:
            conn.close()