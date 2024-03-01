from enum import Enum
class TipoJugador(Enum):
    HUMANO = 1
    IA = 2

class Jugador:
    def __init__(self, nombre, tipo):
        self.nombre = nombre
        self.tipo = tipo
        self.cartas = []

    def __str__(self):
        return f"{self.nombre}: {', '.join(str(carta) for carta in self.cartas)}"