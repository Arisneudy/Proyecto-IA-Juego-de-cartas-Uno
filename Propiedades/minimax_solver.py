import numpy as np
import time

class MinimaxSolver():
    def __init__(self, player_name):

        self.player_name = player_name
        self.time_start = None
        self.max_time = None

    def maximizar(self, estado, alfa, beta, profundidad):
        if time.time() - self.time_start >= self.max_time:
            raise StopIteration("Se quedo sin tiempo!")

        if estado.es_terminal():
            return None, estado.obtener_ganador()

        # if profundidad <= 0:
        #     return None, estado.heuristica_distancia_para_ganar(self.player_name)

        if profundidad <= 0:
            heuristica_valor = estado.heuristica_distancia_para_ganar(self.player_name)
            heuristica_valor += estado.heuristica_balance_de_color(estado.players[estado.current_player])
            heuristica_valor += estado.heuristica_variedad_de_cartas(estado.players[estado.current_player])
            heuristica_valor += estado.heuristica_ventaja_de_turno(estado.players[estado.current_player])
            return None, heuristica_valor


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
        if time.time() - self.time_start >= self.max_time:
            raise StopIteration("Se quedo sin tiempo!")

        if estado.es_terminal():
            return None, estado.obtener_ganador()

        minimo_hijo, menor_utilidad = None, np.inf

        # if profundidad <= 0:
        #     return None, estado.heuristica_distancia_para_ganar(self.player_name)

        if profundidad <= 0:
            heuristica_valor = estado.heuristica_distancia_para_ganar(self.player_name)
            heuristica_valor += estado.heuristica_balance_de_color(estado.players[estado.current_player])
            heuristica_valor += estado.heuristica_variedad_de_cartas(estado.players[estado.current_player])
            heuristica_valor += estado.heuristica_ventaja_de_turno(estado.players[estado.current_player])
            return None, heuristica_valor

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

    def resolver(self, estado, max_time):
        self.time_start = time.time()
        self.max_time = max_time

        for profundidad in range(2, 10000):
            try:
                mejor_opcion, _ = self.maximizar(estado, -np.inf, np.inf, profundidad)
            except StopIteration:
                break

        return mejor_opcion
