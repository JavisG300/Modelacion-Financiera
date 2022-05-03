import string
from urllib.request import ProxyBasicAuthHandler
import numpy as np
from pandas import DataFrame #Para hacer una tabla con los datos
def nodos(s,u,d,n):
    abecedario = list(string.ascii_uppercase)
    numeros = [numero+1 for numero in range(1,n**n)]
    dic_nodos = {}
    lista_nodos = [s]
    j = 0
    i = 0
    ramas = [numeros[rama] for rama in range(n)]
    longitud = sum(ramas)
    while len(lista_nodos) <= longitud:
        up = s*u
        up = round(up,2)
        if up not in lista_nodos:
            lista_nodos.append(up)
        down = s*d
        down = round(down,2)
        if down not in lista_nodos:
            lista_nodos.append(down)
        s = lista_nodos[i+1]
        i+=1
    for i in lista_nodos:
        dic_nodos[abecedario[j]] = lista_nodos[j] 
        j += 1
    print(dic_nodos)

def mbinomial(s,opcion,T,n,r,k,u,d):
    Dt = T/n
    Propabilidad = (np.exp(r*Dt) - d)/(u - d)
    uno_probabilidad = 1 - Propabilidad
    valor_presente1 = np.exp(-r*Dt)
    valor_presenteT = np.exp(-r*T)

    if opcion == 1:
       pass
    elif opcion == 2:
        pass
    elif opcion == 3:
        pass
    else:
        pass




s      = float(input("Indica el precio incial del activo subyacente: "))
opcion = float(input("""
Escribe el número de la opción que será valuada
1) Call Europeo
2) Put Europeo
3) Call Americano
4) Put Americano
""")) 
T      = float(input("Indica el tiempo de vencimiento en años (n/12)=: "))
n      = int(input("Indica el número de periodos: "))
r      = float(input("Indica la tasa de interés anualizada: "))
k      = float(input("Indica el precio de ejercicio: "))
u      = float(input("Indica el porcentaje/probabilidad de subida con la unidad: "))
d      = float(input("Indica el porcentaje/probabilidad de bajada con la unidad: "))

if __name__ == '__main__':
    #mbinomial(s,opcion,T,n,r,k,u,d)
    nodos(s,u,d,n)