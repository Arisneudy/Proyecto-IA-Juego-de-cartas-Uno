peso_mapper = {
    "Reversa": 10,
    "Ø": 10,
    "+2": 15,
    "Comodin": 25,
    "+4": 30
}

class Carta:
    def __init__(self, valor, color):
        self.valor = valor
        self.color = color
        self.peso = int(valor)

    def __str__(self):
        return f"{self.valor} {self.color}"


class CartaAccion:
    def __init__(self, color, accion):
        self.accion = accion
        self.color = color
        self.peso = int(peso_mapper.get(accion))

    def __str__(self):
        return f"{self.accion} {self.color}"


class Comodin:
    def __init__(self, valor):
        self.valor = valor
        self.peso = int(peso_mapper.get(valor))

    def __str__(self):
        return f"{self.valor}"
