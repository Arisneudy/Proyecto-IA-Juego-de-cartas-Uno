from juego import Juego

if __name__ == "__main__":
    continuar = True
    juego = Juego()

    while continuar:
        print("¡Bienvenido a UNO! ¿Desea jugar?")
        print("Si [s]")
        print("No [n]")
        opcion = input().lower()

        if opcion == 's':
            juego.iniciar()
        elif opcion == 'n':
            print("¡Fin del juego!")
            continuar = False
        else:
            print("Opción no válida. Por favor, ingresa 'j' para jugar o 'q' para salir.")