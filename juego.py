import time
from carta import Comodin, Carta, CartaAccion
from mazo import Mazo
from jugador import Jugador
from pila import Pila
from Herramientas import limpiar


class Juego:
    def __init__(self):
        self.mazo = Mazo()
        self.pila = Pila()
        self.color_pila = None

    def obtener_primera_carta(self):
        self.mazo.barajar()
        while True:
            primera_carta = self.mazo.cartas.pop(0)
            if not isinstance(primera_carta, (CartaAccion, Comodin)):
                self.pila.cartas.append(primera_carta)
                break

    def obtener_jugadores(self):
        while True:

            number_of_players = input("¿Cuantas personas juegan? (2-4): ")
            if number_of_players.isdigit():
                number_of_players = int(number_of_players)
                if 2 <= number_of_players <= 4:
                    jugadores = [Jugador(f"Jugador {i + 1}") for i in range(number_of_players)]
                    return jugadores
            print("Por favor, ingresa un número válido entre 2 y 4.")

    def repartir_cartas(self, jugadores):
        cartas_por_jugador = 7
        cartas_repartidas = 0

        while cartas_repartidas < cartas_por_jugador * len(jugadores):
            carta = self.mazo.cartas.pop(0)
            jugador_actual = jugadores[cartas_repartidas % len(jugadores)]
            jugador_actual.cartas.append(carta)
            cartas_repartidas += 1

    def es_carta_valida_para_descartar(self, carta_descartar):
        carta_en_pila = self.pila.cartas[-1]

        if isinstance(carta_descartar, Comodin):
            return True

        if isinstance(carta_en_pila, Comodin):
            return True

        if isinstance(carta_descartar, CartaAccion):
            if isinstance(carta_descartar, CartaAccion) and isinstance(carta_en_pila, CartaAccion):
                return carta_descartar.color == carta_en_pila.color or carta_descartar.accion == carta_en_pila.accion
            elif isinstance(carta_en_pila, Comodin):
                return True
            else:
                return carta_descartar.color == carta_en_pila.color

        if isinstance(carta_descartar, Carta) and not (
                isinstance(carta_en_pila, CartaAccion) or isinstance(carta_en_pila, Comodin)):
            return carta_descartar.color == carta_en_pila.color or carta_descartar.valor == carta_en_pila.valor

        if isinstance(carta_descartar, Carta) and isinstance(carta_en_pila, CartaAccion):
            return carta_descartar.color == carta_en_pila.color

        return False

    def validar_y_descartar_carta(self, jugador, opcion_descartar):
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
        ultima_carta_de_la_pila = self.pila.cartas[-1]

        print("La carta encima de la pila es:", ultima_carta_de_la_pila)
        print("==========")
        print(f"{jugador.nombre}, elige una acción:")
        print("1. Tomar una carta del mazo.")
        print("2. Dejar una carta")
        print("3. Ver mis cartas.")
        print("4. Cantar UNO")

        player_round = True
        while player_round:
            opcion = input("Selecciona una opción: ")
            if opcion == "1":
                if self.mazo.cartas:
                    carta = self.mazo.cartas.pop(0)
                    if len(self.mazo.cartas) != 0:
                        jugador.cartas.append(carta)
                        print(f"{jugador.nombre} tomó una carta del mazo.")
                        print("==========")
                        print(f"{carta} Es la carta Tomada del mazo")
                        print("==========")
                        print(f"{jugador.nombre}. ¿Que desea hacer?")
                    else:
                        print("El mazo está vacío, se está barajando la pila...")
                        self.pila.barajar()
                        self.mazo.cartas.extend(self.pila.cartas[1:])
                        self.pila.cartas[1:] = []
                        time.sleep(2)
                        print("Pila barajada y agregada al mazo.")
                        self.movimiento_de_jugador(jugador, jugadores)

                    player_thinking = True
                    while player_thinking:
                        print("1. Tomar otra carta")
                        print("2. Dejar carta")
                        print("3. Ver la pila.")
                        print("4. Ver mis cartas.")
                        movimiento_de_jugador = input("Seleccione una opción: ")

                        if movimiento_de_jugador == "1":
                            if self.mazo.cartas:
                                carta = self.mazo.cartas.pop(0)
                                jugador.cartas.append(carta)
                                print(f"{jugador.nombre} tomó otra carta del mazo.")
                                print(f"{carta} es la carta tomada del mazo.")
                            else:
                                print("El mazo está vacío.")
                        elif movimiento_de_jugador == "2":
                            self.mostrar_cartas(jugador)
                            while True:
                                self.mostrar_cartas(jugador)
                                opcion_descartar = input(
                                    "Seleccione el número de la carta que desea descartar o ingrese '0' para volver "
                                    "atrás: ")
                                if opcion_descartar == '0':
                                    break
                                if self.validar_y_descartar_carta(jugador, opcion_descartar):
                                    player_round = False
                                    player_thinking = False
                                    break
                        elif movimiento_de_jugador == "3":
                            if self.pila.cartas:
                                print(self.pila.cartas[-1])
                                print("==========")
                            else:
                                print("La pila está vacía.")
                        elif movimiento_de_jugador == "4":
                            if self.pila.cartas:
                                print(self.pila.cartas[-1])
                                print("==========")
                            else:
                                print("La pila está vacía.")
                            self.mostrar_cartas(jugador)
                        else:
                            print("Opción inválida. Por favor, selecciona 1, 2, 3 o 4.")

            elif opcion == "2":
                while True:
                    self.mostrar_cartas(jugador)
                    opcion_descartar = input(
                        "Seleccione el número de la carta que desea descartar o ingrese '0' para volver atrás: ")
                    if opcion_descartar == '0':
                        break
                    if self.validar_y_descartar_carta(jugador, opcion_descartar):
                        player_round = False
                        break

            elif opcion == "3":
                self.mostrar_cartas(jugador)

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

            else:
                print("Opción inválida. Por favor, selecciona 1, 2, 3 o 4.")

    def mostrar_cartas(self, jugador):
        print(f"Cartas de {jugador.nombre}:")
        for i, carta in enumerate(jugador.cartas, 1):
            print(f"{i}. {carta}")
        print("=================")

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

    def iniciar(self):
        self.obtener_primera_carta()
        jugadores = self.obtener_jugadores()
        self.repartir_cartas(jugadores)

        current_player = 0

        while True:
            print(f"Turno del jugador {current_player + 1}:")
            limpiar.clear_console()

            self.movimiento_de_jugador(jugadores[current_player], jugadores)

            carta_ultima_jugada = self.pila.cartas[-1]

            if isinstance(carta_ultima_jugada, CartaAccion):
                if carta_ultima_jugada.accion == "Reversa" and len(jugadores) == 2:
                    current_player = (current_player + 1) % len(jugadores)
                if carta_ultima_jugada.accion == "Reversa":
                    jugadores = jugadores[::-1]
                if carta_ultima_jugada.accion == "Ø":
                    current_player += 1
                    print(
                        f"Al jugador {1 if current_player >= len(jugadores) else current_player + 1} pierde su turno.")
                if carta_ultima_jugada.accion == "+2":
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
                        f"Al jugador {1 if current_player >= len(jugadores) else current_player + 1} pierde su turno.")

            if isinstance(carta_ultima_jugada, Comodin):
                if carta_ultima_jugada.valor == "+4":
                    for _ in range(4):
                        carta = self.mazo.cartas.pop(1)
                        if current_player + 1 >= len(jugadores):
                            jugadores[0].cartas.append(carta)
                        else:
                            jugadores[current_player + 1].cartas.append(carta)

                    current_player += 1
                    print(
                        f"Al jugador {1 if current_player >= len(jugadores) else current_player + 1} se le añaden dos cartas.")
                    print(
                        f"Al jugador {1 if current_player >= len(jugadores) else current_player + 1} pierde su turno.")

                    print("Seleccione el color para cambiar la pila:")
                    print("1. Rojo")
                    print("2. Azul")
                    print("3. Verde")
                    print("4. Amarillo")

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

                elif carta_ultima_jugada.valor == "Comodin":
                    print("Seleccione el color para cambiar la pila:")
                    print("1. Rojo")
                    print("2. Azul")
                    print("3. Verde")
                    print("4. Amarillo")

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
