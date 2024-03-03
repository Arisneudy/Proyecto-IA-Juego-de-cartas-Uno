import random
import time

from Propiedades import jugador
from Propiedades.carta import Comodin, CartaAccion, Carta


class IA:
    def __init__(self, max_tiempo_pensamiento):
        self.max_tiempo_pensamiento = max_tiempo_pensamiento

    def elegir_accion(self, juego):
        tiempo_inicio = time.time()
        mejor_puntuacion = float('-inf')
        mejor_accion = None

        # Obtener las posibles acciones
        acciones_posibles = self.obtener_acciones_posibles(juego)

        # Aplicar la búsqueda de profundidad iterativa
        profundidad = 1
        while time.time() - tiempo_inicio < self.max_tiempo_pensamiento:
            for accion in acciones_posibles:
                nuevo_juego = juego.simular_accion(accion)
                puntuacion = self.minimax(nuevo_juego, profundidad, float('-inf'), float('inf'), False)
                if puntuacion > mejor_puntuacion:
                    mejor_puntuacion = puntuacion
                    mejor_accion = accion
            profundidad += 1

        return mejor_accion

    def minimax(self, juego, profundidad, alfa, beta, maximizando_jugador):
        if profundidad == 0 or juego.es_fin_del_juego():
            return self.evaluar(juego)

        if maximizando_jugador:
            max_puntuacion = float('-inf')
            acciones_posibles = self.obtener_acciones_posibles(juego)
            for accion in acciones_posibles:
                nuevo_juego = juego.simular_accion(accion)
                puntuacion = self.minimax(nuevo_juego, profundidad - 1, alfa, beta, False)
                max_puntuacion = max(max_puntuacion, puntuacion)
                alfa = max(alfa, puntuacion)
                if beta <= alfa:
                    break
            return max_puntuacion
        else:
            min_puntuacion = float('inf')
            acciones_posibles = self.obtener_acciones_posibles(juego)
            for accion in acciones_posibles:
                nuevo_juego = juego.simular_accion(accion)
                puntuacion = self.minimax(nuevo_juego, profundidad - 1, alfa, beta, True)
                min_puntuacion = min(min_puntuacion, puntuacion)
                beta = min(beta, puntuacion)
                if beta <= alfa:
                    break
            return min_puntuacion

    def obtener_acciones_posibles(self, juego):
        acciones_posibles = []
        for accion in juego.obtener_posibles_movimientos(jugador):
            if accion[0] == "descartar":
                acciones_posibles.append(accion[1])
        return acciones_posibles

    def evaluar(self, juego):
        valor = 0
        # Heurística 1: Preferir cartas con el mismo color que la carta superior de la pila
        ultima_carta_pila = juego.pila.cartas[-1]
        for carta in juego.cartas:
            if isinstance(carta, Carta) and carta.color == ultima_carta_pila.color:
                valor += 1
            elif isinstance(carta, CartaAccion) and carta.color == ultima_carta_pila.color:
                valor += 2
            elif isinstance(carta, Comodin):
                valor += 4
        # Agregar más heurísticas según sea necesario
        return valor