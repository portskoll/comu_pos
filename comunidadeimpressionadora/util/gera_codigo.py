
import random

def gerar_cod():
    # definir o conjunto de caracteres possíveis
    caracteres = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    # definir o tamanho do código
    tamanho = 6

    # gerar o código usando uma compreensão de lista
    codigo = "".join([random.choice(caracteres) for i in range(tamanho)])

    # imprimir o código
    return codigo