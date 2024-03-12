import time
import copy

from Propiedades.carta import Comodin, Carta, CartaAccion
from Propiedades.mazo import Mazo
from Propiedades.jugador import Jugador, TipoJugador
from Propiedades.pila import Pila
from Herramientas import limpiar
from Propiedades.minimax_solver import MinimaxSolver


class Juego:
    def __init__(self):
        self.mazo = Mazo()
        self.pila = Pila()
        self.color_pila = None
        self.current_player = 0
        self.players = []
        self.cartas_por_jugador = 7
        self.minimax_time = 3

    def obtener_primera_carta(self):
        self.mazo.barajar()
        primera_carta = None
        for carta in self.mazo.cartas:
            if not isinstance(carta, (CartaAccion, Comodin)):
                primera_carta = carta
                break
        if primera_carta:
            self.mazo.cartas.remove(primera_carta)
            self.pila.cartas.append(primera_carta)

    def obtener_jugadores(self):
        while True:
            number_of_players = input("¿Cuantas personas juegan? (1-4): ")
            number_of_IA = input("¿Cuantos robots juegan? (1-4): ")
            if number_of_players.isdigit() and number_of_IA.isdigit():
                number_of_players = int(number_of_players)
                number_of_IA = int(number_of_IA)
                if 1 <= number_of_players <= 4 and 1 <= number_of_IA <= 4:
                    players = []
                    for i in range(number_of_players):
                        players.append(Jugador(f"Jugador {i + 1}", TipoJugador.HUMANO))
                    for i in range(number_of_IA):
                        players.append(Jugador(f"IA {i + 1}", TipoJugador.IA))
                    self.players = players
                    return players
            print("Por favor, ingresa un número válido entre 1 y 4 para el número de jugadores y de IA.")

    def repartir_cartas(self, jugadores):
        for _ in range(self.cartas_por_jugador):
            for jugador in jugadores:
                carta = self.mazo.cartas.pop(0)
                jugador.cartas.append(carta)

    def es_carta_valida_para_descartar(self, carta_descartar, child=None):
        if child:
            carta_en_pila = child.pila.cartas[-1]
            color_pila = child.color_pila
        else:
            carta_en_pila = self.pila.cartas[-1]
            color_pila = self.color_pila

        if isinstance(carta_descartar, Comodin):
            return True

        if isinstance(carta_en_pila, Comodin):
            if isinstance(carta_descartar, Carta) or isinstance(carta_descartar, CartaAccion):
                if carta_descartar.color == color_pila:
                    return True
            return False

        if isinstance(carta_descartar, CartaAccion) or isinstance(carta_en_pila, CartaAccion):
            if isinstance(carta_descartar, CartaAccion) and isinstance(carta_en_pila, CartaAccion):
                return carta_descartar.color == carta_en_pila.color or carta_descartar.accion == carta_en_pila.accion
            elif isinstance(carta_descartar, CartaAccion):
                return carta_descartar.color == carta_en_pila.color
            elif isinstance(carta_en_pila, CartaAccion):
                return carta_descartar.color == carta_en_pila.color

        if isinstance(carta_descartar, Carta) and not (
                isinstance(carta_en_pila, CartaAccion) or isinstance(carta_en_pila, Comodin)):
            return carta_descartar.color == carta_en_pila.color or carta_descartar.valor == carta_en_pila.valor

        if isinstance(carta_descartar, Carta) and isinstance(carta_en_pila, CartaAccion):
            return carta_descartar.color == carta_en_pila.color

        return False

    def validar_y_descartar_carta(self, jugador, opcion_descartar, child=None):
        opcion_descartar = str(opcion_descartar)

        if child:
            color_pila = child.color_pila
        else:
            color_pila = self.color_pila

        if opcion_descartar.isdigit():
            opcion_descartar = int(opcion_descartar) - 1
            if 0 <= opcion_descartar < len(jugador.cartas):
                carta_descartar = jugador.cartas[opcion_descartar]

                if isinstance(carta_descartar, Comodin):
                    jugador.cartas.remove(carta_descartar)
                    self.pila.agregar_carta(carta_descartar)
                    print(f"{jugador.nombre} descartó la carta: {carta_descartar}")
                    return True

                if color_pila is not None:
                    if carta_descartar.color == color_pila:
                        jugador.cartas.remove(carta_descartar)
                        self.pila.agregar_carta(carta_descartar)
                        print(f"{jugador.nombre} descartó la carta: {carta_descartar}")

                        if not child:
                            self.color_pila = None

                        return True
                    else:
                        print("Debe jugar una carta del color de la pila.")
                        return False
                else:
                    if self.es_carta_valida_para_descartar(carta_descartar, child):
                        jugador.cartas.remove(carta_descartar)
                        self.pila.agregar_carta(carta_descartar)
                        print(f"{jugador.nombre} descartó la carta: {carta_descartar}")
                        return True

        print("Seleccione una carta válida")
        return False

    def movimiento_de_jugador(self, jugador, jugadores, is_prediction=False, options=None, child=None, decision=None):
        if is_prediction and options is not None and decision is None:
            if options[0] == "tomar_carta":
                carta = child.mazo.cartas.pop(0)
                if len(child.mazo.cartas) != 0:
                    jugador.cartas.append(carta)
                else:
                    child.pila.barajar()
                    child.mazo.cartas.extend(child.pila.cartas[1:])
                    child.pila.cartas[1:] = []
                    child.movimiento_de_jugador(child.players[child.current_player], child.players, is_prediction=False)
            elif options[0] == "descartar":
                carta_a_descartar = options[1]

                for card in child.players[child.current_player].cartas:
                    if str(carta_a_descartar) == str(card):
                        child.players[child.current_player].cartas.remove(card)
                        break

                if self.es_carta_valida_para_descartar(carta_a_descartar, child):
                    child.pila.agregar_carta(carta_a_descartar)
                    if len(child.players[child.current_player].cartas) == 0:
                        print("")
                    else:
                        if isinstance(carta_a_descartar, CartaAccion):
                            if carta_a_descartar.accion == "Reversa" and len(child.players) == 2:
                                child.current_player = (child.current_player + 1) % len(child.players)
                            if carta_a_descartar.accion == "Reversa":
                                child.players = child.players[::-1]
                                if child.current_player == 0:
                                    child.current_player = len(child.players) - 1
                                else:
                                    child.current_player -= 1
                            if carta_a_descartar.accion == "Ø":
                                child.current_player += 1
                            if carta_a_descartar.accion == "+2":
                                for _ in range(2):
                                    carta = child.mazo.cartas.pop(1)
                                    if child.current_player + 1 >= len(child.players):
                                        child.players[child.current_player].cartas.append(carta)
                                    else:
                                        child.players[child.current_player + 1].cartas.append(carta)

                                child.current_player += 1

                        if isinstance(carta_a_descartar, Comodin):
                            if carta_a_descartar.valor == "+4":
                                for _ in range(4):
                                    carta = child.mazo.cartas.pop(1)
                                    if child.current_player + 1 >= len(child.players):
                                        child.players[0].cartas.append(carta)
                                    else:
                                        child.players[child.current_player + 1].cartas.append(carta)

                                child.current_player += 1

                                if child.current_player >= len(child.players):
                                    mejor_opcion_de_la_pila = self.obtener_mejor_color_de_pila_para_IA(
                                        child.players[0])
                                else:
                                    mejor_opcion_de_la_pila = self.obtener_mejor_color_de_pila_para_IA(
                                        child.players[child.current_player])

                                child.color_pila = mejor_opcion_de_la_pila

                            if carta_a_descartar.valor == "Comodin":
                                if child.current_player >= len(child.players):
                                    mejor_opcion_de_la_pila = self.obtener_mejor_color_de_pila_para_IA(
                                        child.players[0])
                                else:
                                    mejor_opcion_de_la_pila = self.obtener_mejor_color_de_pila_para_IA(
                                        child.players[child.current_player])

                                child.color_pila = mejor_opcion_de_la_pila
                        child.current_player = (child.current_player + 1) % len(child.players)
            return

        ultima_carta_de_la_pila = self.pila.cartas[-1]

        print("| ------------------------------------------ |")
        print()
        print(" ~ La carta encima de la pila es:", ultima_carta_de_la_pila, " ~")
        print()
        print("| ------------------------------------------ |")
        print(f"| {jugador.nombre}, elige una acción:               |")
        print("| ------------------------------------------ |")
        print("| 1. Tomar una carta del mazo                |")
        print("| 2. Dejar una carta                         |")
        print("| 3. Ver mis cartas                          |")
        print("| 4. Cantar UNO                              |")
        print("| 0. Salir del juego                         |")
        print("| __________________________________________ |")
        print()

        player_round = True
        while player_round:
            if (jugador.tipo == TipoJugador.IA):
                if decision is not None:
                    carta_a_descartar = None
                    for carta in jugador.cartas:
                        if str(carta) == str(decision):
                            carta_a_descartar = carta
                            break

                    self.validar_y_descartar_carta(jugador, jugador.cartas.index(carta_a_descartar) + 1)
                    return

                opcion = "1"
            else:
                opcion = input("Selecciona una opción: ")

            if opcion == "1":
                if self.mazo.cartas:
                    carta = self.mazo.cartas.pop(0)
                    if len(self.mazo.cartas) != 0:
                        jugador.cartas.append(carta)
                        limpiar.clear_console()
                        print()
                        print(" ~ La carta encima de la pila es:", ultima_carta_de_la_pila, " ~")
                        print()
                        print("| ------------------------------------------ |")
                        print(f"| {jugador.nombre} tomó una carta del mazo          |")
                        print("| ------------------------------------------ |")
                        print()
                        print(" La carta tomada del mazo es:", carta)
                        print()
                        print("| ------------------------------------------ |")
                        print(f"| {jugador.nombre}, elige una acción:               |")
                        print("| ------------------------------------------ |")
                        print("| 1. Tomar una carta del mazo                |")
                        print("| 2. Dejar una carta                         |")
                        print("| 3. Ver mis cartas                          |")
                        print("| 4. Cantar UNO                              |")
                        print("| 0. Salir del juego                         |")
                        print("| __________________________________________ |")
                        print()
                        if jugador.tipo == TipoJugador.IA:
                            return
                    else:
                        print("El mazo está vacío, se está barajando la pila...")
                        self.pila.barajar()
                        self.mazo.cartas.extend(self.pila.cartas[1:])
                        self.pila.cartas[1:] = []
                        time.sleep(2)
                        print("Pila barajada y agregada al mazo.")
                        self.movimiento_de_jugador(jugador, jugadores)

            elif opcion == "2":
                while True:
                    self.mostrar_cartas(jugador)
                    opcion_descartar = input(
                        "Seleccione el número de la carta que desea descartar o ingrese '0' para volver atrás: ")
                    if opcion_descartar == '0':
                        limpiar.clear_console()
                        print("| ------------------------------------------ |")
                        print()
                        print(" ~ La carta encima de la pila es:", ultima_carta_de_la_pila, " ~")
                        print()
                        print("| ------------------------------------------ |")
                        print(f"| {jugador.nombre}, elige una acción:               |")
                        print("| ------------------------------------------ |")
                        print("| 1. Tomar una carta del mazo                |")
                        print("| 2. Dejar una carta                         |")
                        print("| 3. Ver mis cartas                          |")
                        print("| 4. Cantar UNO                              |")
                        print("| 0. Salir del juego                         |")
                        print("| __________________________________________ |")
                        print()
                        break
                    if self.validar_y_descartar_carta(jugador, opcion_descartar):
                        player_round = False
                        break

            elif opcion == "3":
                self.mostrar_cartas(jugador)
                input("Presiona enter para continuar....")
                limpiar.clear_console()

                print("| ------------------------------------------ |")
                print()
                print(" ~ La carta encima de la pila es:", ultima_carta_de_la_pila, " ~")
                print()
                print("| ------------------------------------------ |")
                print(f"| {jugador.nombre}, elige una acción:               |")
                print("| ------------------------------------------ |")
                print("| 1. Tomar una carta del mazo                |")
                print("| 2. Dejar una carta                         |")
                print("| 3. Ver mis cartas                          |")
                print("| 4. Cantar UNO                              |")
                print("| 0. Salir del juego                         |")
                print("| __________________________________________ |")
                print()

            elif opcion == "4":
                if len(jugador.cartas) == 1:
                    print(f"{jugador.nombre} grita '¡UNO!'")
                else:
                    print("¡Oops! ¡Solo puedes gritar 'UNO' cuando tienes una sola carta en la mano!")

                for jugador_iter in jugadores:
                    if len(jugador_iter.cartas) == 1 and jugador_iter != jugador_iter:
                        opcion = input(
                            f"{jugador_iter.nombre} ha atrapado a {jugador_iter.nombre} sin gritar 'UNO'. ¿Quieres gritar '¡UNO!'? (s/n): ")
                        if opcion.lower() == "s":
                            print(f"{jugador_iter.nombre} grita '¡UNO!'")
                            print(f"{jugador_iter.nombre} debe robar dos cartas adicionales.")
                            self.repartir_cartas([jugador_iter, jugador_iter])

            elif opcion == "0":
                limpiar.clear_console()
                print("¡Fin del juego!")
                exit()
            else:
                print("Opción inválida. Por favor, selecciona 1, 2, 3 o 4.")

    def mostrar_cartas(self, jugador):
        limpiar.clear_console()
        print()
        print(" ~ La carta encima de la pila es:", self.pila.cartas[-1], " ~")
        print()
        print(f"Cartas de {jugador.nombre}:")
        print()
        for i, carta in enumerate(jugador.cartas, 1):
            print(f"{i}. {carta}")
        print()

    def descartar_carta(self, jugador):
        while True:
            opcion_descartar = input("Elige una carta para descartar (1-6): ")
            if opcion_descartar.isdigit() and 1 <= int(opcion_descartar) <= 6:
                carta_descartar = jugador.cartas.pop(int(opcion_descartar) - 1)
                self.pila.agregar_carta(carta_descartar)
                print(f"{jugador.nombre} descartó la carta: {carta_descartar}")
                break
            else:
                print("Opción inválida. Por favor, elige un número entre 1 y 6.")

    # Esta funcion obtiene los posibles movimientos que puede hacer un jugador en su turno.
    def obtener_posibles_movimientos(self, jugador):
        posibles_movimientos = []

        for carta in jugador.cartas:
            if self.es_carta_valida_para_descartar(carta):
                posibles_movimientos.append(("descartar", carta))

        if self.mazo.cartas:
            posibles_movimientos.append(("tomar_carta", None))

        return posibles_movimientos

    # Esta funcion obtiene el mejor color de pila para la IA.
    def obtener_mejor_color_de_pila_para_IA(self, jugador):
        colores = {'Rojo': 0, 'Azul': 0, 'Verde': 0, 'Amarillo': 0}

        for carta in jugador.cartas:
            if isinstance(carta, Carta):
                colores[carta.color] += 1
            if isinstance(carta, CartaAccion):
                colores[carta.color] += 1

        mejor_color = max(colores, key=colores.get)
        return mejor_color

    # esta funcion obtiene el ganador del juego.
    def obtener_ganador(self):
        for jugador in self.players:
            if len(jugador.cartas) == 0:
                return jugador.nombre
            
    # es_terminal: Valida si ya no hay mas jugadas legales en el juego, en este caso, si ya un jugador llegó a 0 cartas.
    def es_terminal(self):
        for jugador in self.players:
            if len(jugador.cartas) == 0:
                limpiar.clear_console()
                print(f"¡{jugador.nombre} ha dicho UNO y ganado el juego!")
                time.sleep(1)
                return True
        return False
    
    #Children: se crea una copia del estado actual del juego y retorna un arreglo con todos los posibles estados del juego.
    def children(self):
        jugador = self.players[self.current_player]
        options = self.obtener_posibles_movimientos(jugador)
        children = []

        for option in options:
            child = copy.deepcopy(self)
            child.movimiento_de_jugador(child.players[child.current_player], child.players, True, option, child)
            children.append((option[1], child))

        return children
    
    #obtener_decision_de_ai_minimax: se evalua cual es la mejor opción de los estados obtenidos de la función children.
    def obtener_decision_de_ai_minimax(self):
        minimax_solver = MinimaxSolver(self.players[self.current_player].nombre)
        estado = copy.deepcopy(self)
        decision = minimax_solver.resolver(estado, self.minimax_time)
        # print(f"{self.players[self.current_player].nombre} ha jugado {decision}")
        return decision
    
    #heuristica_distancia_para_ganar: Evalua que la IA tenga la menor cantidad de cartas posibles y los otros jugador tengan la mayor cantidad de cartas posibles.
    def heuristica_distancia_para_ganar(self, nombre_jugador):
        heur = 0
        for jugador in self.players:
            if jugador.nombre == nombre_jugador:
                heur -= len(jugador.cartas)
            else:
                heur += len(jugador.cartas)
        return heur

    #heuristica_balance_de_color: Asigna un balance de cartas a cada color.
    def heuristica_balance_de_color(self, jugador):
        colores = {'Rojo': 0, 'Azul': 0, 'Verde': 0, 'Amarillo': 0}

        for carta in jugador.cartas:
            if isinstance(carta, Carta):
                colores[carta.color] += 1

        max_cuenta_de_color = max(colores.values())
        min_cuenta_de_color = min(colores.values())

        balance_score = max_cuenta_de_color - min_cuenta_de_color

        return balance_score

    #heuristica_variedad_de_cartas: Evalua la variedad de cartas que tiene la IA en el momento, 
    #mientras más cartas de acción y comodines tiene, mós alta es la puntuación de variedad
    def heuristica_variedad_de_cartas(self, jugador):
        puntuacion_de_variedad = 0
        action_cards = []

        for carta in jugador.cartas:
            if isinstance(carta, CartaAccion):
                action_cards.append(carta.accion)
            if isinstance(carta, Comodin):
                action_cards.append(carta.valor)

        puntuacion_de_variedad = len(action_cards) / len(jugador.cartas)

        return puntuacion_de_variedad

    def iniciar(self):
        self.obtener_primera_carta()
        self.players = self.obtener_jugadores()
        self.repartir_cartas(self.players)

        while True:
            limpiar.clear_console()
            print("| ------------------------------------------ |")
            print(f"| Turno del jugador {self.current_player + 1}:                       |")

            current_player_obj = self.players[self.current_player]

            if current_player_obj.tipo == TipoJugador.IA:
                ai_decision = self.obtener_decision_de_ai_minimax()
                self.movimiento_de_jugador(current_player_obj, self.players, decision=ai_decision)
            else:
                self.movimiento_de_jugador(current_player_obj, self.players)

            ultima_carta_jugada = self.pila.cartas[-1]

            for jugador in self.players:
                if len(jugador.cartas) == 0:
                    print(f"¡{jugador.nombre} ha ganado el juego!")
                    return

            if isinstance(ultima_carta_jugada, CartaAccion):
                if ultima_carta_jugada.accion == "Reversa" and len(self.players) == 2:
                    self.current_player = (self.current_player + 1) % len(self.players)
                if ultima_carta_jugada.accion == "Reversa":
                    self.players = self.players[::-1]
                    if self.current_player == 0:
                        self.current_player = len(self.players) - 1
                    else:
                        self.current_player -= 1
                if ultima_carta_jugada.accion == "Ø":
                    self.current_player += 1
                    print(
                        f"El jugador {1 if self.current_player >= len(self.players) else self.current_player + 1} pierde su turno.")
                if ultima_carta_jugada.accion == "+2":
                    for _ in range(2):
                        carta = self.mazo.cartas.pop(1)
                        if self.current_player + 1 >= len(self.players):
                            self.players[self.current_player].cartas.append(carta)
                        else:
                            self.players[self.current_player + 1].cartas.append(carta)

                    self.current_player += 1

                    print(
                        f"Al jugador {1 if self.current_player >= len(self.players) else self.current_player + 1} se le añaden dos cartas.")
                    print(
                        f"El jugador {1 if self.current_player >= len(self.players) else self.current_player + 1} pierde su turno.")

            if isinstance(ultima_carta_jugada, Comodin):
                if ultima_carta_jugada.valor == "+4":
                    for _ in range(4):
                        carta = self.mazo.cartas.pop(1)
                        if self.current_player + 1 >= len(self.players):
                            self.players[0].cartas.append(carta)
                        else:
                            self.players[self.current_player + 1].cartas.append(carta)

                    self.current_player += 1

                    limpiar.clear_console()
                    print(
                        f"Al jugador {1 if self.current_player >= len(self.players) else self.current_player + 1} se le añaden cuatro cartas.")
                    print(
                        f"El jugador {1 if self.current_player >= len(self.players) else self.current_player + 1} pierde su turno.")

                    print("Seleccione el color para cambiar la pila:")
                    print("1. Rojo")
                    print("2. Azul")
                    print("3. Verde")
                    print("4. Amarillo")

                    if current_player_obj.tipo == TipoJugador.IA:
                        mejor_opcion_de_la_pila = self.obtener_mejor_color_de_pila_para_IA(current_player_obj)

                        self.color_pila = mejor_opcion_de_la_pila
                        print(f"La pila ha cambiado de color a {self.color_pila}.")
                    else:
                        while True:
                            color_option = input("Elija una opción: ")
                            if color_option.isdigit():
                                color_option = int(color_option)
                                if 1 <= color_option <= 4:
                                    if color_option == 1:
                                        self.color_pila = "Rojo"
                                    elif color_option == 2:
                                        self.color_pila = "Azul"
                                    elif color_option == 3:
                                        self.color_pila = "Verde"
                                    elif color_option == 4:
                                        self.color_pila = "Amarillo"

                                    print(f"La pila ha cambiado de color a {self.color_pila}.")
                                    break
                                else:
                                    print("Ingrese una opción válida (1, 2, 3 o 4)")
                            else:
                                print("Ingrese una opción válida (1, 2, 3 o 4)")


                elif ultima_carta_jugada.valor == "Comodin":
                    limpiar.clear_console()
                    print("Seleccione el color para cambiar la pila:")
                    print("1. Rojo")
                    print("2. Azul")
                    print("3. Verde")
                    print("4. Amarillo")

                    if current_player_obj.tipo == TipoJugador.IA:
                        mejor_opcion_de_la_pila = self.obtener_mejor_color_de_pila_para_IA(current_player_obj)

                        self.color_pila = mejor_opcion_de_la_pila
                        print(f"La pila ha cambiado de color a {self.color_pila}.")

                    else:
                        while True:
                            color_option = input("Elija una opción: ")
                            if color_option.isdigit():
                                color_option = int(color_option)
                                if 1 <= color_option <= 4:
                                    if color_option == 1:
                                        self.color_pila = "Rojo"
                                    elif color_option == 2:
                                        self.color_pila = "Azul"
                                    elif color_option == 3:
                                        self.color_pila = "Verde"
                                    elif color_option == 4:
                                        self.color_pila = "Amarillo"

                                    print(f"La pila ha cambiado de color a {self.color_pila}.")
                                    break
                                else:
                                    print("Ingrese una opción válida (1, 2, 3 o 4)")
                            else:
                                print("Ingrese una opción válida (1, 2, 3 o 4)")

            self.current_player = (self.current_player + 1) % len(self.players)
