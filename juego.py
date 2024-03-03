import time
import random

from Propiedades.carta import Comodin, Carta, CartaAccion
from Propiedades.mazo import Mazo
from Propiedades.jugador import Jugador, TipoJugador
from Propiedades.pila import Pila
from Herramientas import limpiar


class Juego:
    def __init__(self):
        self.mazo = Mazo()
        self.pila = Pila()
        self.color_pila = None

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
                    return players
            print("Por favor, ingresa un número válido entre 1 y 4 para el número de jugadores y de IA.")

    def repartir_cartas(self, jugadores):
        cartas_por_jugador = 7

        for _ in range(cartas_por_jugador):
            for jugador in jugadores:
                carta = self.mazo.cartas.pop(0)
                jugador.cartas.append(carta)

    def es_carta_valida_para_descartar(self, carta_descartar):
        carta_en_pila = self.pila.cartas[-1]

        if isinstance(carta_descartar, Comodin):
            return True

        if isinstance(carta_en_pila, Comodin):
            if isinstance(carta_descartar, Carta) or isinstance(carta_descartar, CartaAccion):
                if carta_descartar.color == self.color_pila:
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

    def validar_y_descartar_carta(self, jugador, opcion_descartar):
        opcion_descartar = str(opcion_descartar)

        if opcion_descartar.isdigit():
            opcion_descartar = int(opcion_descartar) - 1
            if 0 <= opcion_descartar < len(jugador.cartas):
                carta_descartar = jugador.cartas[opcion_descartar]

                if isinstance(carta_descartar, Comodin):
                    jugador.cartas.remove(carta_descartar)
                    self.pila.agregar_carta(carta_descartar)
                    print(f"{jugador.nombre} descartó la carta: {carta_descartar}")
                    return True

                if self.color_pila is not None:
                    if carta_descartar.color == self.color_pila:
                        jugador.cartas.remove(carta_descartar)
                        self.pila.agregar_carta(carta_descartar)
                        print(f"{jugador.nombre} descartó la carta: {carta_descartar}")

                        self.color_pila = None
                        return True
                    else:
                        print("Debe jugar una carta del color de la pila.")
                        return False
                else:
                    if self.es_carta_valida_para_descartar(carta_descartar):
                        jugador.cartas.remove(carta_descartar)
                        self.pila.agregar_carta(carta_descartar)
                        print(f"{jugador.nombre} descartó la carta: {carta_descartar}")
                        return True

        print("Seleccione una carta válida")
        return False

    def movimiento_de_jugador(self, jugador, jugadores):
        #TODO: Remove before production
        for option, card in self.obtener_posibles_movimientos(jugador):
                if option == "descartar":
                    print(f"Descartar carta: {card}")
                elif option == "tomar_carta":
                    print("Tomar una carta del mazo")

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
                posibles_movimientos_IA = self.obtener_posibles_movimientos(jugador)
                movimiento_IA = random.choice(posibles_movimientos_IA)

                if movimiento_IA[0] == "descartar":
                    carta_a_descartar = movimiento_IA[1]
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

    def obtener_posibles_movimientos(self, jugador):
        posibles_movimientos = []

        for carta in jugador.cartas:
            if self.es_carta_valida_para_descartar(carta):
                posibles_movimientos.append(("descartar", carta))

        if self.mazo.cartas:
            posibles_movimientos.append(("tomar_carta", None))

        return posibles_movimientos

    def obtener_mejor_color_de_pila_para_IA(self, jugador):
        colores = {'Rojo': 0, 'Azul': 0, 'Verde': 0, 'Amarillo': 0}

        for carta in jugador.cartas:
            if isinstance(carta, Carta):
                colores[carta.color] += 1

        mejor_color = max(colores, key=colores.get)
        return mejor_color

    def obtener_decision_aleatoria_IA(self, jugador):
        pass

    def iniciar(self):
        self.obtener_primera_carta()
        jugadores = self.obtener_jugadores()
        self.repartir_cartas(jugadores)

        current_player = 0

        while True:
            limpiar.clear_console()
            print("| ------------------------------------------ |")
            print(f"| Turno del jugador {current_player + 1}:                       |")

            current_player_obj = jugadores[current_player]

            self.movimiento_de_jugador(current_player_obj, jugadores)

            ultima_carta_jugada = self.pila.cartas[-1]

            for jugador in jugadores:
                if len(jugador.cartas) == 0:
                    print(f"¡{jugador.nombre} ha ganado el juego!")
                    return

            if isinstance(ultima_carta_jugada, CartaAccion):
                if ultima_carta_jugada.accion == "Reversa" and len(jugadores) == 2:
                    current_player = (current_player + 1) % len(jugadores)
                if ultima_carta_jugada.accion == "Reversa":
                    jugadores = jugadores[::-1]
                    if current_player == 0:
                        current_player = len(jugadores) - 1
                    else:
                        current_player -= 1
                if ultima_carta_jugada.accion == "Ø":
                    current_player += 1
                    print(
                        f"El jugador {1 if current_player >= len(jugadores) else current_player + 1} pierde su turno.")
                if ultima_carta_jugada.accion == "+2":
                    for _ in range(2):
                        carta = self.mazo.cartas.pop(1)
                        if current_player + 1 >= len(jugadores):
                            jugadores[current_player].cartas.append(carta)
                        else:
                            jugadores[current_player + 1].cartas.append(carta)

                    current_player += 1
                    print(
                        f"Al jugador {1 if current_player >= len(jugadores) else current_player + 1} se le añaden dos cartas.")
                    print(
                        f"El jugador {1 if current_player >= len(jugadores) else current_player + 1} pierde su turno.")

            if isinstance(ultima_carta_jugada, Comodin):
                if ultima_carta_jugada.valor == "+4":
                    for _ in range(4):
                        carta = self.mazo.cartas.pop(1)
                        if current_player + 1 >= len(jugadores):
                            jugadores[0].cartas.append(carta)
                        else:
                            jugadores[current_player + 1].cartas.append(carta)

                    current_player += 1

                    limpiar.clear_console()
                    print(
                        f"Al jugador {1 if current_player >= len(jugadores) else current_player + 1} se le añaden cuatro cartas.")
                    print(
                        f"El jugador {1 if current_player >= len(jugadores) else current_player + 1} pierde su turno.")

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

            current_player = (current_player + 1) % len(jugadores)
