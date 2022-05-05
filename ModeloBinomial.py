import string                #Para hacer el diccionario de nodos con letras
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
        #up = round(up,3)
        lista_nodos.append(up)
        integrantes = len(lista_nodos)
        dif = abs(lista_nodos[(integrantes-1)] - lista_nodos[(integrantes-2)])
        if dif <= 0.01:
           lista_nodos.pop()
                
        else:
            lista_nodos

        down = s*d
        #down = round(down,3)
        lista_nodos.append(down)
        integrantes = len(lista_nodos)
        diff = abs(lista_nodos[(integrantes-1)] - lista_nodos[(integrantes-2)])  
        if diff <= 0.01:
            lista_nodos.pop()
        else:
            lista_nodos = lista_nodos
        s = lista_nodos[i+1]
        i+=1
    for i in lista_nodos:
        dic_nodos[abecedario[j]] = lista_nodos[j] 
        j += 1
    print('\n',dic_nodos)

def tabla(s,opcion,T,n,r,k,u,d):
    T = T/12
    Dt = T/n
    Propabilidad = (np.exp(r*Dt) - d)/(u - d)
    uno_probabilidad = 1 - Propabilidad
    if opcion == 1:
        option = 'Call Europeo'
    elif opcion ==2:
        option =  'Put Europeo'
    elif opcion ==3:
        option = 'Call Americano'
    elif opcion == 4:
        option = 'Put Americano'
    datos={'Dato':['Opción','S0','k','T','n','r','u','d','Dt','Probabilidad a la alza', 'Probabilidad a la baja'],
    'Valor ingresado':[option, s,k,T,n,r,u,d,Dt,Propabilidad,uno_probabilidad]}
    tabla_datos = DataFrame(datos, columns = ['Dato','Valor ingresado'], 
    index=['Tipo de opción','Precio incial del activo subyacente','Precio de ejercicio','Tiempo de vencimiento','Número de periodos',
    'Tasa libre de riesgo','Porcentaje de subida','Porcentaje de bajada', 'Delta t', 'Probabilidad a la alza', 'Probabilidad a la baja'])
    print('\n')
    print(tabla_datos.round(4))

def mbinomial(s,opcion,T,n,r,k,u,d):
    T = T/12
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
T      = float(input("Indica el tiempo de vencimiento en meses: "))
n      = int(input("Indica el número de periodos: "))
r      = float(input("Indica la tasa de interés anualizada: "))
k      = float(input("Indica el precio de ejercicio: "))
u      = float(input("Indica el porcentaje/probabilidad de subida con la unidad: "))
d      = float(input("Indica el porcentaje/probabilidad de bajada con la unidad: "))

if __name__ == '__main__':
    #mbinomial(s,opcion,T,n,r,k,u,d)
    tabla(s,opcion,T,n,r,k,u,d)
    nodos(s,u,d,n)