import numpy as np
import Geneticos as gen

def vecino_aleatorio(solucion):
    i, j = np.random.choice(len(solucion), 2, replace=False)  # two random indices
    nueva_solucion = solucion.copy()
    nueva_solucion[i], nueva_solucion[j] = nueva_solucion[j], nueva_solucion[i]
    return nueva_solucion

def accept(delta, T):
    if delta < 0:
        return True
    else:
        r = np.random.rand()  # random value between [0, 1]
        if r < np.exp(-delta / T):
            return True
        else:
            return False

def simulated_annealing(solucion, T_max, T_min, cooling_rate):
    T = T_max
    x = solucion.copy()
    E = gen.fitness(x)

    while T > T_min:
        x_new = vecino_aleatorio(x)
        E_new = gen.fitness(x_new)
        delta = E_new - E
        if accept(delta, T):
            x = x_new
            E = E_new
        T = T * cooling_rate
    return x
