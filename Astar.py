import heapq
import matplotlib.pyplot as plt
import numpy as np
import random

DIRECCIONES = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def heuristica(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

class AStar:
    def __init__(self, mapa, inicio, meta):
        self.mapa = mapa
        self.inicio = inicio
        self.meta = meta
        self.filas = len(mapa)
        self.columnas = len(mapa[0])
        self.open_list = []
        self.closed_list = set()
        self.padre = {}

    def es_valido(self, x, y):
        return 0 <= x < self.filas and 0 <= y < self.columnas and self.mapa[x][y] != 1

    def obtener_vecinos(self, nodo):
        vecinos = []
        for dx, dy in DIRECCIONES:
            nx, ny = nodo[0] + dx, nodo[1] + dy
            if self.es_valido(nx, ny):
                vecinos.append((nx, ny))
        return vecinos

    def buscar(self):
        heapq.heappush(self.open_list, (0 + heuristica(self.inicio, self.meta), 0, self.inicio))
        g = {self.inicio: 0}
        f = {self.inicio: heuristica(self.inicio, self.meta)}
        self.padre[self.inicio] = None

        while self.open_list:
            _, coste_actual, nodo_actual = heapq.heappop(self.open_list)
            if nodo_actual == self.meta:
                return self.reconstruir_ruta(nodo_actual)

            self.closed_list.add(nodo_actual)

            for vecino in self.obtener_vecinos(nodo_actual):
                if vecino in self.closed_list:
                    continue

                nuevo_coste = coste_actual + 1
                if vecino not in g or nuevo_coste < g[vecino]:
                    g[vecino] = nuevo_coste
                    f[vecino] = nuevo_coste + heuristica(vecino, self.meta)
                    self.padre[vecino] = nodo_actual
                    heapq.heappush(self.open_list, (f[vecino], nuevo_coste, vecino))

        return None

    def reconstruir_ruta(self, nodo):
        ruta = []
        while nodo is not None:
            ruta.append(nodo)
            nodo = self.padre[nodo]
        return ruta[::-1]

def visualizar_mapa(mapa, inicio=None, meta=None, ruta=None):
    fig, ax = plt.subplots(figsize=(8, 8))

    colores = np.array(mapa, dtype=int)
    cmap = plt.cm.colors.ListedColormap(["white", "dimgray"])
    ax.imshow(colores, cmap=cmap, origin='upper')

    ax.set_xticks(np.arange(len(mapa[0])))
    ax.set_yticks(np.arange(len(mapa)))
    ax.set_xticklabels(range(len(mapa[0])))
    ax.set_yticklabels(range(len(mapa)))

    ax.set_xticks(np.arange(-0.5, len(mapa[0]), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(mapa), 1), minor=True)
    ax.grid(which="minor", color="lightgray", linestyle='-', linewidth=0.5)

    if inicio:
        ax.scatter(inicio[1], inicio[0], color='limegreen', s=100, edgecolors='black', label="Inicio")
    if meta:
        ax.scatter(meta[1], meta[0], color='royalblue', s=100, edgecolors='black', label="Meta")

    if ruta:
        for (x, y) in ruta:
            ax.add_patch(plt.Rectangle((y - 0.5, x - 0.5), 1, 1, color='orange', alpha=0.6))

    ax.legend()
    plt.xlabel("Columnas")
    plt.ylabel("Filas")
    plt.show()

def crear_mapa():
    filas = int(input("Introduce el número de filas del mapa: "))
    columnas = int(input("Introduce el número de columnas del mapa: "))
    porcentaje_obstaculos = float(input("Introduce el porcentaje de obstáculos (0-100): "))

    mapa = [[0 for _ in range(columnas)] for _ in range(filas)]
    total_celdas = filas * columnas
    num_obstaculos = int((porcentaje_obstaculos / 100) * total_celdas)

    posiciones = [(x, y) for x in range(filas) for y in range(columnas)]
    obstaculos = random.sample(posiciones, num_obstaculos)

    for x, y in obstaculos:
        mapa[x][y] = 1

    visualizar_mapa(mapa)
    return mapa

def ejecutar():
    while True:
        mapa = crear_mapa()
        print("Introduce las coordenadas de inicio (x, y):")
        x_inicio, y_inicio = map(int, input().split())
        print("Introduce las coordenadas de destino (x, y):")
        x_meta, y_meta = map(int, input().split())

        inicio = (x_inicio, y_inicio)
        meta = (x_meta, y_meta)
        astar = AStar(mapa, inicio, meta)

        ruta = astar.buscar()
        if ruta:
            print("Ruta encontrada:", ruta)
            visualizar_mapa(mapa, inicio, meta, ruta)
        else:
            print("No se ha encontrado ninguna ruta.")

        # Preguntar si quiere repetir
        repetir = input("\n¿Quieres empezar de nuevo? (S/N): ").strip().lower()
        if repetir != "s":
            print("¡Hasta la próxima!")
            break

if __name__ == "__main__":
    ejecutar()