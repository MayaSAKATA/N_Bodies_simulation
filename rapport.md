## Première version : programmation naïve
Dans cette première version, on utilise une approche objet avec la définition des classes *Corps* et *NCorps*. La classe *Corps* correspond à une étoile, caractérisée par sa masse, sa couleur, sa position et sa vitesse. La classe *NCorps* correspond elle à une collection d'objets de type Corps.  
On exécute le programme *galaxy_body.py* avec un pas de temps dt=0.01 afin d'assurer la précision et la stabilité du résultat.

Temps de calcul et nombre de frame par seconde en fonction du nombre des corps :
| Nombre de corps              | 100     | 500      | 1000      | 2500      |
|------------------------------|---------|----------|-----------|-----------|
| Temps de calcul              | 1.42 s  | 36.39 s  | 143.05 s  | 914.91 s  |
| Nombre de frame par secondes | 5.63    | 0.27     | 0.07      | 0.01      |


## Deuxième version : vectorisation 
Dans cette deuxième version, on vectorise les calculs afin d'accélérer le temps de calcul. Pour cela, on défini trois tableaux, contenant la position de tous les corps, la vitesse de tous les corps et la couleur de tous les corps. Un corps sera maintenant défini par son indice dans ces trois tableaux. On exécute le code *galaxy_vectorized.py* avec dt=0.01 .

Temps de calcul et nombre de frame par seconde en fonction du nombre des corps :
| Nombre de corps              | 100       | 500       | 1000      | 2500       |
|------------------------------|-----------|-----------|-----------|------------|
| Temps de calcul              | 0.0168 s  | 0.4740 s  | 1.8783 s  | 11.2770 s  |
| Nombre de frame par secondes | 25        | 11        | 4         | 0.8        |

On remarque que la version vectorisé est beaucoup plus rapide (presque 100x plus) que la première version avec les classes. Cela nous permet donc de générer des galaxies avec un nombre d'étoiles important tout en ayant un temps de calcul convenable.


## Troisième version : utilisation de numba
**Mesurez le temps pris par les diverses fonctions**
**Mesurez le gain de temps obtenu à l'aide de numba**
**Mesurez de nouveau avec la parallélisation le temps obtenu et comparez en fonction du nombre de cœurs possédés par la plateforme sur laquelle vous exécutez le code.**
**Essayez plusieurs pas de temps (en année terrestre). Que constatez-vous ? Comment expliquez-vous ce phénomène ?**