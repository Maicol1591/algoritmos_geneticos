import Geneticos as gen

def obtener_vecinos(solucion):
    vecinos_proximos = []
    for i in range(len(solucion) - 1):
        for j in range(i + 1, len(solucion)):
            nueva_solucion = solucion.copy()
            nueva_solucion[i], nueva_solucion[j] = nueva_solucion[j], nueva_solucion[i]
            vecinos_proximos.append(nueva_solucion)

    return vecinos_proximos


def hill_climbing(solucion):
    while True:
        vecinos = obtener_vecinos(solucion)
        mejor_vecino = min(vecinos, key=gen.fitness)
        if gen.fitness(mejor_vecino) < gen.fitness(solucion):
            solucion = mejor_vecino
        else:
            print("MEJOR SOLUCION:")
            print(solucion)
            return solucion
