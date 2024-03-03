import numpy as np
import time

class MinimaxSolver:
    def __init__(self, nombre_jugador):
        self.nombre_jugador = nombre_jugador
        self.tiempo_inicio = None
        self.tiempo_maximo = None

    def __maximizar(self, estado, alfa, beta, profundidad):
        if time.time() - self.tiempo_inicio >= self.tiempo_maximo:
            raise StopIteration("¡Se acabó el tiempo!")

        if estado.es_terminal():
            return None, estado.obtener_puntos_ganadores()[self.nombre_jugador]

        if profundidad <= 0:
            return None, estado.heuristica(self.nombre_jugador)

        mejor_opcion, mejor_utilidad = None, -np.inf

        for opcion, hijo in estado.hijos():
            if hijo.jugador_actual.nombre == self.nombre_jugador:
                _, utilidad = self.__maximizar(estado, alfa, beta, profundidad-1)
            else:
                _, utilidad = self.__minimizar(estado, alfa, beta, profundidad-1)

            if utilidad > mejor_utilidad:
                mejor_opcion, mejor_utilidad = opcion, utilidad

            if mejor_utilidad >= beta:
                break

            alfa = max(alfa, mejor_utilidad)

        return mejor_opcion, mejor_utilidad

    def __minimizar(self, estado, alfa, beta, profundidad):
        if time.time() - self.tiempo_inicio >= self.tiempo_maximo:
            raise StopIteration("¡Se acabó el tiempo!")

        if estado.es_terminal():
            return None, estado.obtener_puntos_ganadores()[self.nombre_jugador]

        if profundidad <= 0:
            return None, estado.heuristica(self.nombre_jugador)

        mejor_opcion, mejor_utilidad = None, np.inf

        for opcion, hijo in estado.hijos():
            if hijo.jugador_actual.nombre == self.nombre_jugador:
                _, utilidad = self.__maximizar(estado, alfa, beta, profundidad-1)
            else:
                _, utilidad = self.__minimizar(estado, alfa, beta, profundidad-1)

            if utilidad < mejor_utilidad:
                mejor_opcion, mejor_utilidad = opcion, utilidad

            if mejor_utilidad <= alfa:
                break

            beta = min(beta, mejor_utilidad)

        return mejor_opcion, mejor_utilidad

    def resolver(self, estado, tiempo_maximo):
        self.tiempo_inicio = time.time()
        self.tiempo_maximo = tiempo_maximo
        for profundidad in range(2, 10000):
            try:
                mejor_opcion, _ = self.__maximizar(estado, -np.inf, np.inf, profundidad)
            except StopIteration:
                break

        return mejor_opcion
