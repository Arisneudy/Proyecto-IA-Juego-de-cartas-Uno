import random
from Propiedades.carta import Carta
from Propiedades.carta import CartaAccion
from Propiedades.carta import Comodin


class Mazo:
    def __init__(self):
        self.cartas = []
        self.cartas_numeradas = []
        self.cartas_accion = []
        self.cartas_comodin = []
        
        colores = ['Rojo', 'Azul', 'Verde', 'Amarillo']
        valores = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        acciones = ['Reversa', 'Ø', '+2']
        comodines = ['+4', 'Comodin']
        #Generamos 72 cartas, del 1 al 9 de cada color 2 veces.
        for color in colores:
            for valor in valores:
                for _ in range(2):
                    self.cartas_numeradas.append(Carta(valor, color))
        #Generamos 4 cartas de con el numero 0, una de cada color.
        for color in colores:
            self.cartas_numeradas.append(Carta("0", color))
        #Generamos 24 cartas de acción, 2 de cada color.
        for accion in acciones:
            for color in colores:
                for _ in range(2):
                    self.cartas_accion.append(CartaAccion(color, accion))
        #Generamos 8 comodines, 4 +4 y 4 Comodines de cambio de color.
        for comodin in comodines:
            for _ in range(4):
                self.cartas_comodin.append(Comodin(comodin))
        #Agregamos un total de 108 carta
        self.cartas = self.cartas_numeradas + self.cartas_accion + self.cartas_comodin

    def barajar(self):
        random.shuffle(self.cartas)

    def imprimir_mazo(self):
        for carta in self.cartas:
            print(carta)
    def imprimir_cuenta_del_mazo(self):
        print(len(self.cartas))
