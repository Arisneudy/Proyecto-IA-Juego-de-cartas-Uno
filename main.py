from juego import Juego
from Herramientas import limpiar

if __name__ == "__main__":
    continuar = True
    juego = Juego()

    while continuar:
        limpiar.Limpiar().clear_console()
        print("¡Bienvenido a UNO! ¿Desea jugar?")
        print("Si [s]")
        print("No [n]")
        opcion = input().lower()

        if opcion == 's':
            limpiar.Limpiar().clear_console()
            juego.iniciar()
        elif opcion == 'n':
            limpiar.Limpiar().clear_console()
            print("¡Fin del juego!")
            continuar = False
        else:
            print("Opción no válida. Por favor, ingresa 'j' para jugar o 'q' para salir.")