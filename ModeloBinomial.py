import string
from urllib.request import ProxyBasicAuthHandler
import numpy as np
from pandas import DataFrame #Para hacer una tabla con los datos

def mbinomial(s,opcion,T,n,r,k,u,d):
    Dt = T/n
    Propabilidad = (np.exp(r*Dt) - d)/(u - d)
    uno_probabilidad = 1 - Propabilidad
    valor_presente1 = np.exp(-r*Dt)
    valor_presenteT = np.exp(-r*T)
 #   S = np.zeros((n+1,n+1))
 #   S[0,0]=s

 #   for i in range(1,n+1):
 #       S[0,i] = S[0,i-1]*u
 #       for j in range(1,n+1):
 #           S[j,i]=S[j-1,i-1]*d
 #   VOPC = np.zeros((n+1,n+1))

 #   for i in range(n+1):
 #       VOPC[i,n]=max(cop*(S[i,n]-k),0)

    lista_nodos = [s]
    if opcion == 1:
        for i in range(1,n+2):
            up = s*u
            up = round(up,2)
            if up not in lista_nodos:
                lista_nodos.append(up)
            down = s*d
            down = round(down,2)
            if down not in lista_nodos:
                lista_nodos.append(down)

            s = lista_nodos[i]
            
        print(lista_nodos, Propabilidad)
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
T      = float(input("Indica el tiempo de vencimiento en años (n/12): "))
n      = int(input("Indica el número de periodos: "))
r      = float(input("Indica la tasa de interés anualizada: "))
k      = float(input("Indica el precio de ejercicio: "))
u      = float(input("Indica el porcentaje/probabilidad de subida con la unidad: "))
d      = float(input("Indica el porcentaje/probabilidad de bajada con la unidad: "))

if __name__ == '__main__':
    mbinomial(s,opcion,T,n,r,k,u,d)