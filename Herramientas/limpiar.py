import os


def clear_console():
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        _ = os.system('cls')
