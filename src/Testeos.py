import numpy as np
from scipy.spatial.distance import pdist, squareform
import Geneticos as gen
import HillClimbing as hlcl
import Graficos as grf
leyenda = ["A","B"]
colores = ["red","orange"]
diccionario = {}
matriz_nodos = []
for i in range(1,11):
    diccionario[i] = np.random.randint(1,100)
matriz_nodos.append(diccionario.copy())
diccionario = {}
for i in range(1,11):
    diccionario[i] = np.random.randint(1,100)
matriz_nodos.append(diccionario.copy())
print(matriz_nodos)
grf.imprimir_fitness(matriz_nodos,leyenda,colores)
