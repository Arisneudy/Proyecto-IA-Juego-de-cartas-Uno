class Carta:
    def __init__(self, valor, color):
        self.valor = valor
        self.color = color

    def __str__(self):
        return f"{self.valor} {self.color}"


class CartaAccion:
    def __init__(self, color, accion):
        self.accion = accion
        self.color = color

    def __str__(self):
        return f"{self.accion} {self.color}"


class Comodin:
    def __init__(self, valor):
        self.valor = valor

    def __str__(self):
        return f"{self.valor}"
