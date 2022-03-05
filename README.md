# AlgoritmoGenetico
Algoritmo Genético realizado en la universidad durante la optativa de "Algoritmos Genéticos y Evolutivos". Modular

Este algoritmo hace una seleccion mediante torneos y el cruce cogiendo la mitad de cada pariente, saliendo de cada
pareja de progenitores 2 hijos.

#Parametros
-Torneo: porcentaje de individuos que participan en el torneo. Numero entre 0 y 1. Puede cambiarse a un numero entero fijo independiente de la poblacion.
-Parada: numero maximo de generaciones que se van a realizar. Primer criterio de parada. Se recomienda un numero alto.
-RondasMax: numero de generaciones sin alcanzar un fitness mejor. Superado este valor, el algoritmo se detiene. Segundo criterio de parada.
-Mejores: fichero donde se guardan los mejores de cada generacion. Direccion de este fichero.
-csv: se guarda el mejor fitness de cada generacion y el mejor de ese momento.
-csv2: se guardan datos globales de cada generacion.
-gradoMutacion: porcentaje de mutacion en cada generacion. Numero entre 0 y 1.
-sizePoblacion: numero de individuos que tiene una poblacion. Se recomienda un numero alto.
-sizeCromosoma: numero de genes del cromosoma. Mayor o igual que 1.
-web: web o servidor donde esta alojada la funcion de fitness. A esta web se le pone por detras el tamaño del cromosoma (linea 110)

Este codigo se realizo para la practica 1 de algoritmos geneticos. Los cromosomas pueden valor 0 o 1 y tratará de minimizar el valor
de fitness. Cuenta con control de excepciones para el acceso a la web, por si esta diese problemas o tardase en reaccionar.
