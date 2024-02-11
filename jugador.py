class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.cartas = []

    def __str__(self):
        return f"{self.nombre}: {', '.join(str(carta) for carta in self.cartas)}"