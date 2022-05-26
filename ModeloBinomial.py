from operator import index
import numpy as np           #Para exp
from pandas import DataFrame #Para hacer una tabla con los datos
from math import factorial
from paridad_put_call import paridad #Función de paridad put call programada anteriormente

def nodos(s,u,d,n):
    numeros = [numero+1 for numero in range(1,n+1)]
    l=[0]
    for i in range(1,n+1):
        numeronuevo = l[i-1]+i
        l.append(numeronuevo)
    longitud = sum(numeros)
    lista_nodos = [s]
    i = 0
    while len(lista_nodos) <= longitud:
        if i == 0 or lista_nodos.index(s) in l:
            up = s*u
            lista_nodos.append(up)
            down = s*d
            lista_nodos.append(down)
        else:
            down = s*d
            lista_nodos.append(down)
        s = lista_nodos[i+1]
        i+=1
    return lista_nodos

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
    datos={'Dato         ':['Opción','S0','k','T','n','r','u','d','Dt','Probabilidad a la alza', 'Probabilidad a la baja'],
    '   Valor ingresado   ':[option, s,k,T,n,r,u,d,Dt,Propabilidad,uno_probabilidad]}
    tabla_datos = DataFrame(datos, columns = ['Dato         ','   Valor ingresado   '], 
    index=['Tipo de opción','Precio incial del activo subyacente','Precio de ejercicio','Tiempo de vencimiento','Número de periodos',
    'Tasa libre de riesgo','Porcentaje de subida','Porcentaje de bajada', 'Delta t', 'Probabilidad a la alza', 'Probabilidad a la baja'])
    print('\n')
    print(tabla_datos.round(4))

def mbinomial(s,T,n,r,k,u,d): #Funcion para determinar el precio de las opcion
    T = T/12
    Dt = T/n
    Propabilidad = (np.exp(r*Dt) - d)/(u - d)
    uno_probabilidad = 1 - Propabilidad
    valor_presente1 = np.exp(-n*r*Dt)
    valor_presenteT = np.exp(-r*Dt)

    #Calculando el valor de la opción
    #Call Europeo
    cuenta = 0
    Nodos = nodos(s,u,d,n)
    Nodos1 = Nodos.copy()
    Nodos1 = Nodos1[::-1]
    lcu_y_cd = []
    for i in range(n+1):
        lcu_y_cd.append(Nodos1[i])
    lcu_y_cd = lcu_y_cd[::-1]
    for i in range(n+1):
        cu = max(lcu_y_cd[i]-k,0)
        combinacion = factorial(n)/((factorial(i))*(factorial(n-i)))
        cuenta = cuenta + combinacion*(Propabilidad**(n-i))*((uno_probabilidad)**i)*cu 
    valor_del_call = valor_presente1 * cuenta
    

    #Put Europeo
    cuenta = 0
    Nodos = nodos(s,u,d,n)
    Nodos1 = Nodos.copy()
    Nodos1 = Nodos1[::-1]
    lcu_y_cd = []     
    for i in range(n+1):
        lcu_y_cd.append(Nodos1[i])
    lcu_y_cd = lcu_y_cd[::-1]
    for i in range(n+1):
        cu = max(k-lcu_y_cd[i],0)
        combinacion = factorial(n)/((factorial(i))*(factorial(n-i)))
        cuenta = cuenta + combinacion*(Propabilidad**(n-i))*((uno_probabilidad)**i)*cu 
    valor_del_put = valor_presente1 * cuenta
        

    #Call Americano
    Nodos = nodos(s,u,d,n) #Lista de los nodos de subida y bajada
    lcu_y_cd = []
    lcu_y_cd_nuevo = []

    for i in range(len(Nodos)-(n+1)):
        lcu_y_cd.append(Nodos[i])
    lcu_y_cd = lcu_y_cd[::-1]
    lcu_y_cd_nuevo = lcu_y_cd.copy()

    for i in range(n): #Evaluamos los ultimos n valores desde el cero es decir n+1
        nodo_evaluar = lcu_y_cd_nuevo[i]
        up = nodo_evaluar*u
        maxup = max(up-k,0)
        down = nodo_evaluar*d                 
        maxdown = max(down-k,0)
        call = valor_presenteT*(maxup*Propabilidad + maxdown*uno_probabilidad)
        rendimiento_ejercer = max(nodo_evaluar-k,0)
        if rendimiento_ejercer >= call:
            lcu_y_cd_nuevo[i] = rendimiento_ejercer
        else:
            lcu_y_cd_nuevo[i] = call         #Hasta aquí solo han cambiado los penultimos 
        #Vamos a comparar las listas lcy_y_lcd vs lcu_ylcd_nuevo para esto se necesitan en orden Ascendente
    lcu_y_cd = lcu_y_cd[::-1]
    lcu_y_cd_nuevo = lcu_y_cd_nuevo[::-1]
    i=0
    for j in lcu_y_cd_nuevo:
        if j != lcu_y_cd[i]:
            indice = lcu_y_cd_nuevo.index(j)
            break
        i+=1
    contador = 0
    N=n
        #Ahora empezamos a cambiar los elementos a partir de indice-1
    for i in range(len(lcu_y_cd)-(n)): #A la longitud de la lista de nodos recortada le restamos los n valores desde el cero evaluados antes
        nodo_evaluar =  lcu_y_cd_nuevo[indice-1]
        call = valor_presenteT*(lcu_y_cd_nuevo[indice+(N-2)]*Propabilidad + lcu_y_cd_nuevo[indice+(N-1)]*uno_probabilidad)
        rendimiento_ejercer = max(nodo_evaluar-k,0)
        if rendimiento_ejercer >= call:
            lcu_y_cd_nuevo[indice-1] = rendimiento_ejercer
        else:
            lcu_y_cd_nuevo[indice-1] = call
        indice = indice -1 
        contador = contador + 1
        if contador == N-1:
            N = N-1
            contador = 0
    valor_del_call_americano = valor_presenteT*(Propabilidad*lcu_y_cd_nuevo[1] + uno_probabilidad*lcu_y_cd_nuevo[2])
        


    #Put Americano
    Nodos = nodos(s,u,d,n)
    lcu_y_cd = []
    lcu_y_cd_nuevo = []

    for i in range(len(Nodos)-(n+1)):
        lcu_y_cd.append(Nodos[i])
    lcu_y_cd = lcu_y_cd[::-1]
    lcu_y_cd_nuevo = lcu_y_cd.copy()
    for i in range(n): #Evaluamos los ultimos n valores desde el cero
        nodo_evaluar = lcu_y_cd_nuevo[i]
        up = nodo_evaluar*u
        maxup = max(k-up,0)
        down = nodo_evaluar*d                 
        maxdown = max(k-down,0)
        put = valor_presenteT*(maxup*Propabilidad + maxdown*uno_probabilidad)
        rendimiento_ejercer = max(k-nodo_evaluar,0)
        if rendimiento_ejercer >= put:
            lcu_y_cd_nuevo[i] = rendimiento_ejercer
        else:
            lcu_y_cd_nuevo[i] = put         #Hasta aquí solo han cambiado los penultimos 
        #Vamos a comparar las listas lcy_y_lcd vs lcu_ylcd_nuevo para esto se necesitan en orden Ascendente
    lcu_y_cd = lcu_y_cd[::-1]
    lcu_y_cd_nuevo = lcu_y_cd_nuevo[::-1]
    i=0
    for j in lcu_y_cd_nuevo:
        if j != lcu_y_cd[i]:
            indice = lcu_y_cd_nuevo.index(j)
            break
        i+=1
    contador=0 
    N=n   
        #Ahora empezamos a cambiar los elementos a partir de indice-1
    for i in range(len(lcu_y_cd)-(n)): #A la longitud de la lista de nodos recortada le restamos los n valores desde el cero evaluados antes
        nodo_evaluar =  lcu_y_cd_nuevo[indice-1]
        put = valor_presenteT*(lcu_y_cd_nuevo[indice+(N-2)]*Propabilidad + lcu_y_cd_nuevo[indice+(N-1)]*uno_probabilidad)
        rendimiento_ejercer = max(k-nodo_evaluar,0)
        if rendimiento_ejercer >= put:
            lcu_y_cd_nuevo[indice-1] = rendimiento_ejercer
        else:
            lcu_y_cd_nuevo[indice-1] = put
        indice = indice -1 
        contador = contador + 1
        if contador == N-1:
            N = N-1
            contador = 0

    valor_del_put_americano = valor_presenteT*(Propabilidad*lcu_y_cd_nuevo[1] + uno_probabilidad*lcu_y_cd_nuevo[2])
    return valor_del_call, valor_del_put, valor_del_call_americano, valor_del_put_americano

def tabla_comparativa(s,T,n,r,k,u,d):
    uno = mbinomial(s,1,T,n,r,k,u,d)
    dos = mbinomial(s,2,T,n,r,k,u,d)
    tres = mbinomial(s,3,T,n,r,k,u,d)
    cuatro = mbinomial(s,4,T,n,r,k,u,d)
    datos={'Opción':['Europeo', 'Europeo','Americano', 'Americano'], 'Precio':[uno,dos,tres,cuatro]}
    tabla_datos = DataFrame(datos, columns = ['Opción','Precio'], 
    index=['Call','Put','Call','Put'])
    print('\n')
    print(tabla_datos.round(4))

print("""
--------------------------------------------------------------------
|| Bienvenido a la calculadora de opciones con el modelo binomial || 
||                                                                ||
|| Por favor introduce los datos que se solicitan a continuación  ||
--------------------------------------------------------------------

""")
opcion = float(input("""
Escribe el número de la opción que será valuada
1) Call Europeo
2) Put Europeo
3) Call Americano
4) Put Americano 
 """)) 
print(f'---Su selección fue el inciso {opcion} ---\n')
s      = float(input("Indica el precio incial del activo subyacente: "))
k      = float(input("Indica el precio de ejercicio: "))
T      = float(input("Indica el tiempo de vencimiento en meses: "))
n      = int(input("Indica el número de periodos: "))
r      = float(input("Indica la tasa de interés anualizada de forma decimal: "))
u      = float(input("Indica el porcentaje/probabilidad de subida con la unidad: "))
d      = float(input("Indica el porcentaje/probabilidad de bajada con la unidad: "))

def main():
    print("""
    ---------------------------------------
    || Resumen de los datos introducidos ||
    ---------------------------------------""")
    tabla(s,opcion,T,n,r,k,u,d)
    nodos(s,u,d,n)
    l = mbinomial(s,opcion,T,n,r,k,u,d)
    if opcion == 1:
        tipo = 'Call Europeo'
    elif opcion == 2:
        tipo = 'Put Europeo'
    elif opcion ==3:
        tipo = 'Call Americano'
    elif opcion ==4:
        tipo = 'Put Americano'
    print('\n')
    print(f'El precio del {tipo} solicitado es:{l} \n')
    print("""
    ---------------------------------------------------------------------------------------------------------------
    || A continuación se muestra una tabla comparativa de la opción solicitada junto a los demás tipos de opción || 
    ---------------------------------------------------------------------------------------------------------------
    """)
    tabla_comparativa(s,T,n,r,k,u,d)
    print('\n')
    Paridad = input(('¿Quieres comprobar la paridad Put-Call entre algunas de las opciones. y/n: '))
    Paridad = Paridad.lower()
    if Paridad == 'y':
        OpCall = int(input("""
        ¿Qué Call quieres usar? 

        1) Americano
        2) Europeo 
        """))
        print(f'---Su selección fue el inciso {OpCall} ---\n')
        OpPut = int(input("""
        ¿Qué Put quieres usar? 

        1) Americano
        2) Europeo 
        """))
        print(f'---Su selección fue el inciso {OpPut} ---\n')
        if OpCall == 1:
            c = mbinomial(s,3,T,n,r,k,u,d)

        else:
            c = mbinomial(s,1,T,n,r,k,u,d)
        
        if OpPut == 1:
            p = mbinomial(s,4,T,n,r,k,u,d)

        else:
            p = mbinomial(s,2,T,n,r,k,u,d)
            
        t=T/12
        paridad(c,p,k,r,s,t)
        print('\n https://github.com/JavisG300/Modelacion-Financiera/blob/master/ModeloBinomial.py')
    else:
        print('El programa finalizó')
        print('\n https://github.com/JavisG300/Modelacion-Financiera/blob/master/ModeloBinomial.py')


if __name__ == '__main__':
    main()