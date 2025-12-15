-- Lecture des tables après insertion des bdd

select*
from magasins as m;

select*
from produits as p;

select*
from ventes as v ;

SELECT *
from analyse_resultats as ar ;

---------------------------------------

SELECT SUM(V.quantite * P.prix) AS CA_Total_General
FROM ventes AS V
JOIN produits AS P 
	ON LOWER(V.id_reference_produits) = LOWER(P.id_reference_produits);

CA_Total_General|
----------------+
         5268.78|
         
SELECT P.nom AS Nom_Produit, SUM(V.quantite) AS Quantite_Totale_Vendue
FROM ventes AS V
JOIN produits AS P 
	ON LOWER(V.id_reference_produits) = LOWER(P.id_reference_produits)
GROUP BY P.nom
ORDER BY Quantite_Totale_Vendue DESC;

Nom_Produit|Quantite_Totale_Vendue|
-----------+----------------------+
Produit E  |                    35|
Produit B  |                    27|
Produit A  |                    24|
Produit D  |                    21|
Produit C  |                    15|



 SELECT M.ville AS Ville, 
       SUM(V.quantite * P.prix) AS CA_Total_Region
FROM ventes AS V
JOIN produits AS P 
	ON LOWER(V.id_reference_produits) = LOWER(P.id_reference_produits)
JOIN magasins AS M 
	ON V.id_magasin = M.id_magasin
GROUP BY M.ville
ORDER BY CA_Total_Region DESC;
 
 Ville     |CA_Total_Region|
----------+---------------+
Lyon      |        1059.79|
Marseille |        1009.73|
Bordeaux  |         829.81|
Paris     |          799.8|
Nantes    |         739.83|
Strasbourg|         579.89|
Lille     |         249.93|


-- l'utilisation de lower permet de garantir que tt les ventes sont correcteemtn associées à son produits de correspondances
-- Insertion des données dans la table analyse_resulats

INSERT INTO analyse_resultats (
    ville, 
    CA_Total_Region, 
    Date_Analyse)
SELECT 
    M.ville, 
SUM(V.quantite * P.prix) AS CA_Total_Region,
STRFTIME('%Y-%m-%d %H:%M:%S', 'NOW') -- permet d'avoir les dates de maj 
FROM 
    ventes AS V
JOIN 
    produits AS P 
    ON LOWER(V.id_reference_produits) = LOWER(P.id_reference_produits)
JOIN 
    magasins AS M 
    ON V.id_magasin = M.id_magasin
GROUP BY 
    M.ville
 ORDER BY CA_Total_Region DESC;

-- vérification 
SELECT *
from analyse_resultats as ar 

id_analyse|ville     |CA_Total_Region|Date_Analyse       |
----------+----------+---------------+-------------------+
         1|Bordeaux  |         829.81|2025-12-14 21:58:08|
         2|Lille     |         249.93|2025-12-14 21:58:08|
         3|Lyon      |        1059.79|2025-12-14 21:58:08|
         4|Marseille |        1009.73|2025-12-14 21:58:08|
         5|Nantes    |         739.83|2025-12-14 21:58:08|
         6|Paris     |          799.8|2025-12-14 21:58:08|
         7|Strasbourg|         579.89|2025-12-14 21:58:08|
         8|Lyon      |        1059.79|2025-12-14 21:58:57|
         9|Marseille |        1009.73|2025-12-14 21:58:57|
        10|Bordeaux  |         829.81|2025-12-14 21:58:57|
        11|Paris     |          799.8|2025-12-14 21:58:57|
        12|Nantes    |         739.83|2025-12-14 21:58:57|
        13|Strasbourg|         579.89|2025-12-14 21:58:57|
        14|Lille     |         249.93|2025-12-14 21:58:57|