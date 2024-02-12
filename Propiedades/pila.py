import random


class Pila:
    def __init__(self):
        self.cartas = []

    def agregar_carta(self, carta):
        self.cartas.append(carta)

    def tomar_carta(self):
        if self.cartas:
            return self.cartas.pop()
        else:
            return None
    def barajar(self):
        random.shuffle(self.cartas)