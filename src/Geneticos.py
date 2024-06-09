from scipy.spatial.distance import pdist, squareform
import numpy as np
import random
import pandas as pd
import HillClimbing as hlcl
import SimulatedAnnealling as sa
import time
from tqdm import tqdm

matriz_tsp_distancias = []
coordenadas_ciudades = []

# ALGORITMOS DE INICIALIZACION
def crear_ciudades(cantidad_ciudades):
    coordenadas_ciudades = np.random.rand(cantidad_ciudades, 2)
    matriz_tsp_distancias = squareform(pdist(coordenadas_ciudades, 'euclidean'))
    return coordenadas_ciudades, matriz_tsp_distancias

def crear_poblacion_inicial_random(cantidad_poblacion, cantidad_ciudades):
    poblacion = []
    for _ in range(cantidad_poblacion):
        individual = list(np.random.permutation(cantidad_ciudades))  # create a random solution
        poblacion.append(individual)
    return poblacion

def crear_poblacion_inicial_heuristica(cantidad_poblacion, cantidad_ciudades):
    T_max = 1000
    T_min = 1
    cooling_rate = 0.9995
    poblacion = []
    for _ in tqdm(range(cantidad_poblacion)):
        individual = list(np.random.permutation(cantidad_ciudades))  # create a random solution
        new_individual = sa.simulated_annealing(individual, T_max, T_min, cooling_rate)
        poblacion.append(new_individual)
    return poblacion  

def crear_poblacion_inicial_hibrida(cantidad_poblacion, cantidad_ciudades):
    T_max = 1000
    T_min = 1
    cooling_rate = 0.9995
    poblacion = []
    for _ in tqdm(range(cantidad_poblacion)):
        individual = list(np.random.permutation(cantidad_ciudades))  # create a random solution
        if np.random.random() > 0.5:
            new_individual = sa.simulated_annealing(individual, T_max, T_min, cooling_rate)
            poblacion.append(new_individual)
        else:
            poblacion.append(individual)
    return poblacion  


def fitness(solucion):  # depende del problema
    distancia_total = 0
    for i in range(len(solucion) - 1):
        distancia_total += matriz_tsp_distancias[solucion[i]][solucion[i + 1]]
    return distancia_total


# ALGORITMOS DE SELECCION
def metodo_roulete_wheel(poblacion, all_fitness=None):
    if all_fitness is None:
        all_fitness = [fitness(sol) for sol in poblacion]
    max_fitness = max(all_fitness)
    fitness_invertido = [max_fitness - f for f in all_fitness]
    total_fitness = sum(fitness_invertido)
    selection_probs = [f / total_fitness for f in fitness_invertido]  # it works for maximization
    return poblacion[np.random.choice(len(poblacion), p=selection_probs)]

def metodo_rank_based(poblacion, all_fitness=None):
    if all_fitness is None:
        all_fitness = [fitness(sol) for sol in poblacion]
    matriz_ranking = np.array(all_fitness).argsort().argsort()
    max_ranking = max(matriz_ranking)
    ranking_invertido = [max_ranking - r for r in matriz_ranking]
    total_ranking = sum(ranking_invertido)
    selection_probs = [r / total_ranking for r in ranking_invertido]  # it works for maximization
    return poblacion[np.random.choice(len(poblacion), p=selection_probs)]

def metodo_fitness_scalling(poblacion, all_fitness=None, min=50, max=100):
    if all_fitness is None:
        all_fitness = [fitness(sol) for sol in poblacion]
    fitness_np = np.array(all_fitness)
    reescalado_fitness = np.interp(fitness_np, (fitness_np.min(), fitness_np.max()), (min, max))
    return metodo_roulete_wheel(poblacion, reescalado_fitness)

def metodo_tournament_selection(poblacion, numero_participantes=3):
    participantes_torneo = np.random.choice(poblacion, numero_participantes)
    ganador_torneo = np.minimum(participantes_torneo, fitness)
    return ganador_torneo


# ALGORITMOS DE CRUCE
def cruce_single_point(padre, madre):
    punto_cruce = random.randint(1, len(padre) - 1)
    hijo1 = padre[:punto_cruce] + madre[punto_cruce:]
    hijo2 = madre[:punto_cruce] + padre[punto_cruce:]
    return hijo1, hijo2

def cruce_double_point(padre, madre):
    size = len(padre)
    min_cruce, max_cruce = sorted(random.sample(range(size), 2))
    hijo1 = padre[:min_cruce] + madre[min_cruce:max_cruce] + padre[max_cruce:]
    hijo2 = madre[:min_cruce] + padre[min_cruce:max_cruce] + madre[max_cruce:]
    return hijo1, hijo2

def cruce_uniform(padre, madre):
    mascara = np.random.randint(0, 2, size=len(padre))
    hijo1 = padre * mascara + madre * (1 - mascara)
    hijo2 = madre * mascara + padre * (1 - mascara)
    return hijo1, hijo2

def llenado_hijo(child, parent, end):
    size = len(parent)
    current_pos = (end + 1) % size
    for gene in parent:
        if gene not in child:
            child[current_pos] = gene
            current_pos = (current_pos + 1) % size

def cruce_ordered(parent1, parent2):
    size = len(parent1)
    hijo1, hijo2 = [-1] * size, [-1] * size
    min_cruce, max_cruce = sorted(random.sample(range(size), 2))
    hijo1[min_cruce:max_cruce + 1] = parent2[min_cruce:max_cruce + 1]
    hijo2[min_cruce:max_cruce + 1] = parent1[min_cruce:max_cruce + 1]
    llenado_hijo(hijo1, parent1, max_cruce)
    llenado_hijo(hijo2, parent2, max_cruce)
    return hijo1, hijo2


# ALGORITMOS DE MUTACION
def mutacion_swap(individuo):
    i, j = np.random.choice(len(individuo), 2, replace=False)  # two random indices
    nuevo_individuo = individuo.copy()
    nuevo_individuo[i], nuevo_individuo[j] = individuo[j], individuo[i]
    return nuevo_individuo

def mutacion_invert(individuo):
    indice = np.random.randint(0, len(individuo))
    nuevo_individuo = np.append(individuo[:indice + 1], individuo[len(individuo):indice:-1])
    return nuevo_individuo


# ALGORITMOS DE SELECCION
def select_elite(population, all_fitness, elite_size):  # selecciona los que tengan el menor fitness
    elite_indices = np.argsort(all_fitness)[:elite_size]
    return np.array(population)[elite_indices], elite_indices


"""Integration"""


# Genetic Algorithm
def genetic_algorithm(
        cantidad_poblacion, 
        cantidad_ciudades,
        poblacion_inicial = None, 
        ratio_mutacion=0.01, 
        generaciones=10,
        cantidad_elites=3, 
        metodo_inicializacion="Aleatorio", 
        metodo_seleccion="Ruleta", 
        cantidad_participantes_torneo=3,
        print_each=100
    ):
    """
    Realiza un algoritmo genético para encontrar la solución óptima para un problema dado.

    Args:
        cantidad_poblacion (int): El tamaño de la población.
        cantidad_ciudades (int): El número de ciudades en el problema.
        poblacion_inicial (list, optional): Una población inicial. Defaults a None.
        ratio_mutacion (float, optional): La proporción de mutación. Defaults a 0.01.
        generaciones (int, optional): El número de generaciones. Defaults a 10.
        cantidad_elites (int, optional): El número de individuos elitistas que se preservan. Defaults a 3.
        metodo_inicializacion (str, optional): El método para inicializar la población. Defaults a "Aleatorio".
        metodo_seleccion (str, optional): El método para seleccionar los padres. Defaults a "Ruleta".
        cantidad_participantes_torneo (int, optional): El número de participantes en la selección de torneos. Defaults a 3.

    Returns:
        tuple: Una tupla que contiene la mejor ruta, la mejor distancia, un diccionario de valores de aptitud para cada generación, y el tiempo total utilizado.
    """
    nodos_fitness = {}
    population = []
    if poblacion_inicial is None:
        if metodo_inicializacion == "Aleatorio":
            population = crear_poblacion_inicial_random(cantidad_poblacion, cantidad_ciudades)
        elif metodo_inicializacion == "Heuristico":
            print("[INICIALIZACION HEURISTICA] Se inicializo la creacion de la poblacion")
            population = crear_poblacion_inicial_heuristica(cantidad_poblacion, cantidad_ciudades)
            print("[INICIALIZACION HEURISTICA] Se completo la creacion de la poblacion")
        elif metodo_inicializacion == "Hibrido":
            print("[INICIALIZACION HIBRIDA] Se inicializo la creacion de la poblacion")
            population = crear_poblacion_inicial_hibrida(cantidad_poblacion, cantidad_ciudades)
            print("[INICIALIZACION HIBRIDA] Se completo la creacion de la poblacion")
    else:
        population = poblacion_inicial
    all_fitness = [fitness(sol) for sol in population]

    inicio = time.time()
    for generation in range(generaciones):
        new_population = []
        # Preserve elite individuals
        selected_elite, elite_indices = select_elite(population, all_fitness, cantidad_elites)
        new_population.extend(selected_elite)

        # Create new population through crossover and mutation
        while len(new_population) < cantidad_poblacion:
            parent1 = []
            parent2 = []
            if metodo_seleccion == "Ruleta":
                parent1 = metodo_roulete_wheel(population, all_fitness)
                parent2 = metodo_roulete_wheel(population, all_fitness)
            elif metodo_seleccion == "Rankeo":
                parent1 = metodo_rank_based(population, all_fitness)
                parent2 = metodo_rank_based(population, all_fitness)
            elif metodo_seleccion == "Escalado":
                parent1 = metodo_fitness_scalling(population, all_fitness)
                parent2 = metodo_fitness_scalling(population, all_fitness)
            elif metodo_seleccion == "Torneo":
                parent1 = metodo_fitness_scalling(population, all_fitness, cantidad_participantes_torneo)
                parent2 = metodo_fitness_scalling(population, all_fitness, cantidad_participantes_torneo)

            child1, child2 = cruce_ordered(parent1, parent2)

            if random.random() < ratio_mutacion:
                child1 = mutacion_swap(child1)
            if random.random() < ratio_mutacion:
                child2 = mutacion_swap(child2)

            new_population.extend([child1, child2])

        population = new_population[:cantidad_poblacion]  # replace with new population
        all_fitness = [fitness(sol) for sol in population]
        if generation % print_each == 0:
            print(f"Generation {generation} | Best distance: {min(all_fitness)}")
            nodos_fitness[generation] = min(all_fitness)

    fin = time.time()
    tiempo_total = fin-inicio
    best_route_index = np.argmin(all_fitness)
    best_route = population[best_route_index]
    best_distance = all_fitness[best_route_index]

    print(f"Final best distance: {best_distance}")
    return best_route, best_distance, nodos_fitness, tiempo_total
