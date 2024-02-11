from mazo import Mazo
from jugador import Jugador
from pila import Pila

class Juego:
    def __init__(self):
        self.mazo = Mazo()
        self.pila = Pila()

    def obtener_primera_carta(self):
        self.mazo.barajar()
        primera_carta = self.mazo.cartas.pop(0)
        self.pila.cartas.append(primera_carta)

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

    def movimiento_de_jugador(self, jugador):
        print(f"{jugador.nombre}, elige una acción:")
        print("1. Tomar una carta del mazo.")
        print("2. Dejar una carta")
        print("3. Ver la pila.")
        print("4. Ver mis cartas.")

        while True:
            opcion = input("Selecciona una opción: ")
            if opcion == "1":
                if self.mazo.cartas:
                    carta = self.mazo.cartas.pop(0)
                    jugador.cartas.append(carta)
                    print(f"{jugador.nombre} tomó una carta del mazo.")
                    print(f"{jugador.nombre}. ¿Que desea hacer?")

                    player_thinking = True
                    while player_thinking:
                        print("1. Dejar carta")
                        print("2. Ver la pila.")
                        print("3. Ver mis cartas.")
                        movimiento_de_jugador = input("Seleccione una opcion: ")

                        if movimiento_de_jugador == "1":
                            self.mostrar_cartas(jugador)

                            seleccionando_carta = True
                            while seleccionando_carta:
                                opcion_descartar = input()
                                if opcion_descartar.isdigit():
                                    carta_descartar = jugador.cartas.pop(int(opcion_descartar) - 1)
                                    self.pila.agregar_carta(carta_descartar)
                                    print(f"{jugador.nombre} descartó la carta: {carta_descartar}")

                                    # Validar si la carta es un comodin
                                    # Validar si es una carta accion
                                    # Validar si la carta accion es del mismo color de la carta de la pila o si hay otra carta
                                    # accion del mismo tipo en la pila
                                    # Validar la es posible dejar la carta solicitada en la pila, por color o numero
                                    # Si no es posible continue with the cycle
                                    player_thinking = False
                                    break
                                else:
                                    print("Seleccione una carta valida")
                                continue
                            continue
                        if movimiento_de_jugador == "2":
                            if self.pila.cartas:
                                print(self.pila.cartas[-1])
                                print("==========")
                            else:
                                print("La pila está vacía.")
                            continue
                        if movimiento_de_jugador == "3":
                            if self.pila.cartas:
                                print(self.pila.cartas[-1])
                                print("==========")
                            else:
                                print("La pila está vacía.")
                            self.mostrar_cartas(jugador)
                            continue

                        print("Opción inválida. Por favor, selecciona 1, 2, 3 o 4.")
                        continue
                else:
                    print("El mazo está vacío.")

            if opcion == "2":
                self.mostrar_cartas(jugador)
                seleccionando_carta = True
                while seleccionando_carta:
                    opcion_descartar = input()
                    if opcion_descartar.isdigit():
                        if len(jugador.cartas) < int(opcion_descartar) - 1:
                            print("Seleccione una carta valida")
                            break

                        carta_descartar = jugador.cartas.pop(int(opcion_descartar) - 1)
                        self.pila.agregar_carta(carta_descartar)
                        print(f"{jugador.nombre} descartó la carta: {carta_descartar}")

                        # Validar si la carta es un comodin
                        # Validar si es una carta accion
                        # Validar si la carta accion es del mismo color de la carta de la pila o si hay otra carta
                        # accion del mismo tipo en la pila
                        # Validar la es posible dejar la carta solicitada en la pila, por color o numero
                        # Si no es posible continue with the cycle
                        break
                    else:
                        print("Seleccione una carta valida")
                    continue

                # Validar si la carta es un comodin
                # Validar si es una carta accion
                # Validar si la carta accion es del mismo color de la carta de la pila o si hay otra carta
                # accion del mismo tipo en la pila
                # Validar la es posible dejar la carta solicitada en la pila, por color o numero
                # Si no es posible continue with the cycle
                break
            if opcion == "3":
                if self.pila.cartas:
                    print(self.pila.cartas[-1])
                    print("==========")
                    continue
                else:
                    print("La pila está vacía.")
            if opcion == "4":
                self.mostrar_cartas(jugador)
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

        is_active_game = True
        current_player = 0

        while is_active_game:
            print(f"Turno del jugador {current_player + 1}:")
            self.movimiento_de_jugador(jugadores[current_player])

            current_player += 1

            if current_player == len(jugadores):
                current_player = 0
