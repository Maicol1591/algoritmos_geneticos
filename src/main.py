import Geneticos as gen
import Graficos as grf
import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform

# DEFINIENDO PARAMETROS DEL PROBLEMA
cantidad_ciudades = 100
gen.coordenadas_ciudades = [[0.21954616, 0.14581329],
                            [0.17421578, 0.18566283],
                            [0.29122291, 0.80457042],
                            [0.18040537, 0.80267858],
                            [0.3412426, 0.41644281],
                            [0.58179122, 0.49474069],
                            [0.67356906, 0.75094227],
                            [0.88793601, 0.47142495],
                            [0.00779237, 0.53205174],
                            [0.36181121, 0.58683286],
                            [0.01003692, 0.85785187],
                            [0.67929191, 0.24353308],
                            [0.6065664, 0.70519311],
                            [0.72948251, 0.43073781],
                            [0.9607949, 0.54489034],
                            [0.88817971, 0.07955406],
                            [0.52557476, 0.4696241],
                            [0.94650895, 0.03802156],
                            [0.64501347, 0.77524301],
                            [0.87601183, 0.78304364],
                            [0.36018579, 0.93557705],
                            [0.89366112, 0.60359089],
                            [0.97601195, 0.85817543],
                            [0.26127822, 0.71608585],
                            [0.90879018, 0.58434009],
                            [0.91013166, 0.12334488],
                            [0.91736713, 0.23586366],
                            [0.13667125, 0.00201317],
                            [0.94980787, 0.4336497],
                            [0.2038939, 0.93308361],
                            [0.83826848, 0.41281027],
                            [0.32066564, 0.49212394],
                            [0.14341033, 0.91744724],
                            [0.69439039, 0.58776669],
                            [0.7831435, 0.05133785],
                            [0.99532546, 0.77610824],
                            [0.48295153, 0.57015342],
                            [0.93819732, 0.79385582],
                            [0.29426788, 0.64406639],
                            [0.26814418, 0.23473205],
                            [0.16670826, 0.685144],
                            [0.60190034, 0.27357298],
                            [0.65943488, 0.21823561],
                            [0.09769489, 0.8826959],
                            [0.66464977, 0.86631929],
                            [0.3814482, 0.94021531],
                            [0.09677459, 0.10593996],
                            [0.17864128, 0.62865786],
                            [0.01510431, 0.44956381],
                            [0.23513167, 0.41254368],
                            [0.4549013, 0.01794302],
                            [0.80061994, 0.39180504],
                            [0.3417234, 0.37118961],
                            [0.19172995, 0.43508706],
                            [0.13512255, 0.99817623],
                            [0.11329438, 0.90948516],
                            [0.09481105, 0.52652043],
                            [0.60478417, 0.57487087],
                            [0.42949743, 0.35347706],
                            [0.69048789, 0.1950799],
                            [0.99041799, 0.45246021],
                            [0.58163492, 0.80503285],
                            [0.75869429, 0.66096662],
                            [0.6583406, 0.87208508],
                            [0.60404149, 0.32236654],
                            [0.63871647, 0.03338515],
                            [0.64207654, 0.20223676],
                            [0.12276697, 0.68577585],
                            [0.10845472, 0.84312461],
                            [0.53897218, 0.30451347],
                            [0.6133547, 0.02200327],
                            [0.0488243, 0.28018404],
                            [0.57981611, 0.23698127],
                            [0.3168622, 0.5841623],
                            [0.622078, 0.34672988],
                            [0.26934929, 0.63440813],
                            [0.90313144, 0.65774199],
                            [0.12093674, 0.75562179],
                            [0.08036233, 0.44383751],
                            [0.10992283, 0.43391352],
                            [0.08494473, 0.80382135],
                            [0.49516912, 0.774868],
                            [0.95936749, 0.2579975],
                            [0.93321228, 0.88949077],
                            [0.65689517, 0.02874112],
                            [0.19149822, 0.53687667],
                            [0.95414153, 0.91035188],
                            [0.50068953, 0.03360075],
                            [0.65037733, 0.63369655],
                            [0.18609162, 0.74971852],
                            [0.99697744, 0.22788147],
                            [0.73286254, 0.02269668],
                            [0.13865304, 0.58424392],
                            [0.26217996, 0.45843858],
                            [0.82195241, 0.4835036],
                            [0.77293438, 0.88474862],
                            [0.95244401, 0.80528087],
                            [0.35954457, 0.03645583],
                            [0.71485602, 0.81287991],
                            [0.06654975, 0.81823839]]
gen.matriz_tsp_distancias = squareform(pdist(gen.coordenadas_ciudades, 'euclidean'))

# grf.imprimir_ciudades(gen.coordenadas_ciudades)

'''
Experimento 1:
Para un mismo conjunto de 100 ciudades, implementar y comparar la solucion obtenida usando los metodos de seleccion: 
- Roulette wheel selection
- Rank-based selection
- Fitness scaling
- Tournament selection.
'''
'''
# COMPARAR USANDO HYPERPARAMETROS OPTIMOS
cantidad_generaciones = 8000
cantidad_poblacion = 75
elite_size = 30
mutation_rate = 0.10

poblacion_inicial = gen.crear_poblacion_inicial_random(cantidad_poblacion,cantidad_ciudades)

matriz_finess = []
metodos = ["Ruleta", "Rankeo", "Escalado", "Torneo"]
colores = ["red", "green", "blue", "orange"]
for metodo in metodos:
    mejor_ruta, mejor_distancia, nodos_fitness, tiempo_total = gen.genetic_algorithm(cantidad_poblacion,
                                                                                     cantidad_ciudades,
                                                                                     poblacion_inicial,
                                                                                     mutation_rate,
                                                                                     cantidad_generaciones, elite_size,
                                                                                     metodo_seleccion=metodo,
                                                                                     cantidad_participantes_torneo=10)
    matriz_finess.append(nodos_fitness)
    grf.imprimir_ruta(gen.coordenadas_ciudades, mejor_ruta,
                      "Metodo " + metodo + " Fitness(" + str(round(mejor_distancia, 5)) + ") Tiempo (" + str(
                          round(tiempo_total, 5)) + ")",
                      "X", "Y")

grf.imprimir_fitness(matriz_finess, metodos, colores)
'''
'''
Experimento 2:
Para un mismo conjunto de 100 ciudades, implementar y comparar la solucion obtenida usando los metodos de seleccion: 
- Roulette wheel selection
- Rank-based selection
- Fitness scaling
- Tournament selection.
'''
# COMPARAR USANDO HYPERPARAMETROS OPTIMOS
cantidad_generaciones = 5000
cantidad_poblacion = 75
elite_size = 30
mutation_rate = 0.2

matriz_finess = []

metodos_inicializacion = ["Aleatorio", "Heuristico", "Hibrido"]
colores = ["red", "green", "blue"]
for metodo_inicializacion in metodos_inicializacion:
    mejor_ruta, mejor_distancia, nodos_fitness, tiempo_total = gen.genetic_algorithm(cantidad_poblacion,
                                                                                     cantidad_ciudades,
                                                                                     None,
                                                                                     mutation_rate,
                                                                                     cantidad_generaciones, 
                                                                                     elite_size,
                                                                                     metodo_inicializacion,
                                                                                     metodo_seleccion="Ruleta")
    matriz_finess.append(nodos_fitness)
    grf.imprimir_ruta(gen.coordenadas_ciudades, mejor_ruta,
                      "Inicializacion " + metodo_inicializacion + " Fitness(" + str(round(mejor_distancia, 5)) + ") Tiempo (" + str(
                          round(tiempo_total, 5)) + ")",
                      "X", "Y")

grf.imprimir_fitness(matriz_finess, metodos_inicializacion, colores)
