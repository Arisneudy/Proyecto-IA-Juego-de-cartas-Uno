import numpy as np

class MinimaxSolver():
    def __init__(self, player_name):

        self.player_name = player_name
        self.time_start = None
        self.max_time = None

    def maximizar(self, estado, alfa, beta, profundidad):
        if estado.es_terminal():
            return None, estado.obtener_ganador()

        if profundidad == 0:
            return None, estado.heuristic(self.player_name)

        mayor_hijo, mayor_utilidad = None, -np.inf

        for option, child in estado.children():

            if child.players[child.current_player].nombre == self.player_name:
                _, utilidad = self.maximizar(estado, alfa, beta, profundidad - 1)
            else:
                _, utilidad = self.minimizar(estado, alfa, beta, profundidad - 1)

            if utilidad > mayor_utilidad:
                mayor_hijo, mayor_utilidad = option, utilidad

            if mayor_utilidad >= beta:
                break

            alfa = max(alfa, mayor_utilidad)

        return mayor_hijo, mayor_utilidad

    def minimizar(self, estado, alfa, beta, profundidad):
        if estado.es_terminal():
            return None, estado.obtener_ganador()

        minimo_hijo, menor_utilidad = None, np.inf

        if profundidad == 0:
            return None, estado.heuristic(self.player_name)

        for option, child in estado.children():

            if child.players[child.current_player].nombre == self.player_name:
                _, utilidad = self.maximizar(estado, alfa, beta, profundidad - 1)
            else:
                _, utilidad = self.minimizar(estado, alfa, beta, profundidad - 1)

            if utilidad < menor_utilidad:
                minimo_hijo, menor_utilidad = option, utilidad

            if menor_utilidad <= alfa:
                break

            beta = min(beta, menor_utilidad)

        return minimo_hijo, menor_utilidad

    def resolver(self, estado):
        hijo, _ = self.maximizar(estado, -np.inf, np.inf, 2)
        return hijo
