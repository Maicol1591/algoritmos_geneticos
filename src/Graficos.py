import numpy as np
from matplotlib import pyplot as plt


def get_cmap(n, name='hsv'):
    return plt.cm.get_cmap(name, n)


def imprimir_ciudades(nodes):
    x = [node[0] for node in nodes]
    y = [node[1] for node in nodes]

    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, color='blue', zorder=2)  # Plot nodes

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('TSP Nodes')
    plt.grid(True)
    plt.show()


def imprimir_ruta(nodes, route, titulo='TSP Nodes and Route', ejeX="X", ejeY="Y"):
    x = [node[0] for node in nodes]
    y = [node[1] for node in nodes]

    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, color='blue', zorder=2)  # Plot nodes

    for i in range(len(route) - 1):
        node1 = route[i]
        node2 = route[i + 1]
        plt.plot([nodes[node1][0], nodes[node2][0]], [nodes[node1][1], nodes[node2][1]], color='red',
                 zorder=1)  # Plot route

    # Connect the last node to the first node to form a loop
    node1 = route[-1]
    node2 = route[0]
    plt.plot([nodes[node1][0], nodes[node2][0]], [nodes[node1][1], nodes[node2][1]], color='red',
             zorder=1)  # Plot route

    plt.xlabel(ejeX)
    plt.ylabel(ejeY)
    plt.title(titulo)
    plt.grid(True)
    plt.show()


def imprimir_fitness(nodos_fitness, leyenda, color_linea):
    nodo = {}
    i = 0
    #cmap = get_cmap(len(nodos_fitness),"Pastel1")
    plt.figure(figsize=(8, 6))
    fig, ax = plt.subplots()
    for nodo in nodos_fitness:
        x = nodo.keys()
        y = nodo.values()
        #color_linea = cmap(i)
        #color_linea = (np.random.random(), np.random.random(), np.random.random())
        #ax.scatter(x, y, color=color_linea)  # Plot nodes
        ax.plot(x, y, color=color_linea[i])
        ax.legend(leyenda)
        i += 1

    plt.xlabel("Generaciones")
    plt.ylabel("Fitness")
    plt.title("Fitness vs Generaciones")
    plt.grid(True)
    plt.show()
