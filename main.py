from juego import Juego
from Herramientas import limpiar

if __name__ == "__main__":
    continuar = True
    juego = Juego()

    while continuar:
        limpiar.clear_console()
        print("| -------------------------------- |")
        print("| ¡Bienvenido a UNO! ¿Desea jugar? |")
        print("| -------------------------------- |")
        print("|                                  |")
        print("| 1. Si [s]                        |")
        print("| 2. No [n]                        |")
        print("|                                  |")
        print("| -------------------------------- |")
        print()
        opcion = input("Ingresa tu opción: ").lower() 

        if opcion == 's':
            limpiar.clear_console()
            juego.iniciar()
        elif opcion == 'n':
            limpiar.clear_console()
            print("¡Fin del juego!")
            continuar = False
        else:
            limpiar.clear_console()
            print("Opción no válida. Por favor, ingresa 'j' para jugar o 'q' para salir.")