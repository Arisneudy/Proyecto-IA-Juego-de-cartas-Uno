from Propiedades.carta import Comodin, CartaAccion, Carta
from Propiedades.jugador import Jugador, TipoJugador
from Propiedades.mazo import Mazo
from Propiedades.pila import Pila


class GestorDeJuego:
    def __init__(self):
        self.mazo = Mazo()
        self.pila = Pila()
        self.color_pila = None

    def obtener_primera_carta(self):
        self.mazo.barajar()
        for carta in self.mazo.cartas:
            if not isinstance(carta, (CartaAccion, Comodin)):
                self.pila.cartas.append(carta)
                break

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
        try:
            opcion_descartar = int(opcion_descartar) - 1
            if 0 <= opcion_descartar < len(jugador.cartas):
                carta_descartar = jugador.cartas[opcion_descartar]
                if self.es_carta_valida_para_descartar(carta_descartar):
                    jugador.cartas.remove(carta_descartar)
                    self.pila.agregar_carta(carta_descartar)
                    print(f"{jugador.nombre} descartó la carta: {carta_descartar}")
                    return True
                else:
                    print("La carta seleccionada no es válida para descartar.")
            else:
                print("Seleccione una carta válida.")
        except ValueError:
            print("Ingrese un número válido.")
        return False

    def obtener_posibles_movimientos(self, jugador):
        posibles_movimientos = []

        for carta in jugador.cartas:
            if self.es_carta_valida_para_descartar(carta):
                posibles_movimientos.append(("descartar", carta))

        if self.mazo.cartas:
            posibles_movimientos.append(("tomar_carta", None))

        return posibles_movimientos

