import sqlite3
import pandas as pd
from tabulate import tabulate
from datetime import date
import os

DB_PATH = os.environ.get('DB_PATH', '/app/data/pme_num_ventes.db')

def run_analyse(conn):
    # 4.a CA total
    try:
        ca_total_query = """
        SELECT SUM(V.quantite * P.prix) AS CA_Total_General
        FROM ventes AS V
        JOIN produits AS P ON LOWER(V.id_reference_produits) = LOWER(P.id_reference_produits);
        """
        
        ca_total = pd.read_sql_query(ca_total_query, conn).iloc[0,0]
        ca_resultat = f"{ca_total:,.2f} €" if ca_total else "N/A"
        print(f" le chiffre d'Affaires Total est : {ca_resultat}")
    except Exception as e:
        print(f" Il y as une erreur de calcul CA total : {e}")

    # 4.b Ventes par produit
    try:
        ventes_query = """
        SELECT P.nom AS Nom_Produit, SUM(V.quantite) AS Quantite_Totale_Vendue
        FROM ventes AS V
        JOIN produits AS P ON LOWER(V.id_reference_produits) = LOWER(P.id_reference_produits)
        GROUP BY P.nom
        ORDER BY Quantite_Totale_Vendue DESC;
        """


        df_ventes = pd.read_sql_query(ventes_query, conn)
        if not df_ventes.empty:
            print("\n  4.b. Ventes par Produit :")
            print(tabulate(df_ventes, headers='keys', tablefmt='fancy_grid', showindex=False))
        else:
            print(" Pas de données dans ventes ou produits.")
    except Exception as e:
        print(f" Erreur ventes par produit : {e}")

    # 4.c CA par ville
    try:
        ca_ville_query = """
        SELECT M.ville AS Ville, SUM(V.quantite * P.prix) AS CA_Total_Region
        FROM ventes AS V
        JOIN produits AS P ON LOWER(V.id_reference_produits) = LOWER(P.id_reference_produits)
        JOIN magasins AS M ON V.id_magasin = M.id_magasin
        GROUP BY M.ville
        ORDER BY CA_Total_Region DESC;
        """

        df_ville = pd.read_sql_query(ca_ville_query, conn)
        if not df_ville.empty:
            df_ville['Date_Analyse'] = date.today().strftime('%Y-%m-%d')
            df_ville.to_sql('analyse_resultats', conn, if_exists='append', index=False)
            print("\n 4.c. CA par Ville/Région :")
            print(tabulate(df_ville, headers='keys', tablefmt='fancy_grid', showindex=False))
            print("Les résultats stockés dans le fichier 'Analyse_Resultats'.")
        else:
            print(" Pas de ventes ou magasins disponibles.")
    except Exception as e:
        print(f" il y as une erreur CA par ville : {e}")

    conn.commit()



if __name__ == '__main__':
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        print(" Ce fichier doit être appelé via main_pipeline.py")
        run_analyse(conn)
    except Exception as e:
        print(f" ÉCHEC TEST LOCAL: {e}")
    finally:
        if conn:
            conn.close()
