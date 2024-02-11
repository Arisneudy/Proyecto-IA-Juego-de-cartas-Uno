import os

class Limpiar:
    def clear_console(self):
        if os.name == 'posix':
            _ = os.system('clear')
        else:
            _ = os.system('cls')