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

    #Calculando el valor de las opciones

    #Call y Put Europeo
    cuenta_call = 0
    cuenta_put = 0
    Nodos = nodos(s,u,d,n)
    Nodos1 = Nodos.copy()
    Nodos1 = Nodos1[::-1]
    lcu_y_cd = []
    for i in range(n+1):
        lcu_y_cd.append(Nodos1[i])
    lcu_y_cd = lcu_y_cd[::-1]
    for i in range(n+1):
        #Call Europeo
        cu = max(lcu_y_cd[i]-k,0)
        #Put Europeo
        pu = max(k-lcu_y_cd[i],0)
        combinacion = factorial(n)/((factorial(i))*(factorial(n-i)))
        cuenta_call = cuenta_call + combinacion*(Propabilidad**(n-i))*((uno_probabilidad)**i)*cu
        cuenta_put = cuenta_put + combinacion*(Propabilidad**(n-i))*((uno_probabilidad)**i)*pu 
    valor_del_call = valor_presente1 * cuenta_call
    valor_del_put = valor_presente1 * cuenta_put


    #Call y Put Americano
    lcu_y_cd = []
    lcu_y_cd_nuevo = []

    for i in range(len(Nodos)-(n+1)):
        lcu_y_cd.append(Nodos[i])
    lcu_y_cd = lcu_y_cd[::-1]
    lcu_y_cd_nuevo = lcu_y_cd.copy()
    lcu_y_cd_call = lcu_y_cd.copy()
    lcu_y_cd_put = lcu_y_cd.copy()

    for i in range(n): #Evaluamos los ultimos n valores desde el cero es decir n+1
        nodo_evaluar = lcu_y_cd_nuevo[i]
        up = nodo_evaluar*u
        maxup_call = max(up-k,0)
        maxup_put = max(k-up,0)

        down = nodo_evaluar*d                 
        maxdown_call = max(down-k,0)
        maxdown_put = max(k-down,0)

        call = valor_presenteT*(maxup_call*Propabilidad + maxdown_call*uno_probabilidad)
        put = valor_presenteT*(maxup_put*Propabilidad + maxdown_put*uno_probabilidad)
        rendimiento_ejercer_call = max(nodo_evaluar-k,0)
        rendimiento_ejercer_put = max(k-nodo_evaluar,0)

        if rendimiento_ejercer_call >= call:
            lcu_y_cd_call[i] = rendimiento_ejercer_call
        else:
            lcu_y_cd_call[i] = call         #Hasta aquí solo han cambiado los penultimos del call

        if rendimiento_ejercer_put >= put:
            lcu_y_cd_put[i] = rendimiento_ejercer_put
        else:
            lcu_y_cd_put[i] = put         #Hasta aquí solo han cambiado los penultimos del put

#Vamos a comparar las listas lcy_y_lcd vs lcu_ylcd_call y la del put para esto se necesitan en orden Ascendente
    lcu_y_cd = lcu_y_cd[::-1]
    lcu_y_cd_call = lcu_y_cd_call[::-1]
    lcu_y_cd_put = lcu_y_cd_put[::-1]
    i,h=0,0
    for j in lcu_y_cd_call:
        if j != lcu_y_cd[i]:
            indice_call = lcu_y_cd_call.index(j)
            break
        i+=1
    for j in lcu_y_cd_put:
        if j != lcu_y_cd[h]:
            indice_put = lcu_y_cd_put.index(j)
            break
        h+=1
    contador=0 
    N=n   
        #Ahora empezamos a cambiar los elementos a partir de indice-1
    for i in range(len(lcu_y_cd)-(n)): #A la longitud de la lista de nodos recortada le restamos los n valores desde el cero evaluados antes
        nodo_evaluar_call =  lcu_y_cd_call[indice_call-1]
        nodo_evaluar_put =  lcu_y_cd_put[indice_put-1]
        call = valor_presenteT*(lcu_y_cd_call[indice_call+(N-2)]*Propabilidad + lcu_y_cd_call[indice_call+(N-1)]*uno_probabilidad)
        put = valor_presenteT*(lcu_y_cd_put[indice_put+(N-2)]*Propabilidad + lcu_y_cd_put[indice_put+(N-1)]*uno_probabilidad)
        rendimiento_ejercer_call = max(nodo_evaluar_call-k,0)
        rendimiento_ejercer_put = max(k-nodo_evaluar_put,0)
        if rendimiento_ejercer_call >= call:
            lcu_y_cd_call[indice_call-1] = rendimiento_ejercer_call
        else:
            lcu_y_cd_call[indice_call-1] = call
        indice_call = indice_call -1 

        if rendimiento_ejercer_put >= put:
            lcu_y_cd_put[indice_put-1] = rendimiento_ejercer_put
        else:
            lcu_y_cd_put[indice_put-1] = put
        indice_put = indice_put -1 
        contador = contador + 1
        if contador == N-1:
            N = N-1
            contador = 0
    valor_del_call_americano = valor_presenteT*(Propabilidad*lcu_y_cd_call[1] + uno_probabilidad*lcu_y_cd_call[2])
    valor_del_put_americano = valor_presenteT*(Propabilidad*lcu_y_cd_put[1] + uno_probabilidad*lcu_y_cd_put[2])

    return valor_del_call, valor_del_put, valor_del_call_americano, valor_del_put_americano

def tabla_comparativa(s,T,n,r,k,u,d):
    uno = mbinomial(s,T,n,r,k,u,d)
    datos={'Opción':['Europeo', 'Europeo','Americano', 'Americano'], 'Precio':[uno[0],uno[1],uno[2],uno[3]]}
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
    l = mbinomial(s,T,n,r,k,u,d)
    if opcion == 1:
        tipo = 'Call Europeo'
        v = 0
    elif opcion == 2:
        tipo = 'Put Europeo'
        v = 1
    elif opcion ==3:
        tipo = 'Call Americano'
        v = 2
    elif opcion ==4:
        tipo = 'Put Americano'
        v = 3
    print('\n')
    print(f'El precio del {tipo} solicitado es:{l[v]} \n')
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
            c = l[2]

        else:
            c = l[0]
        
        if OpPut == 1:
            p = l[3]

        else:
            p = l[1]
            
        t=T/12
        paridad(c,p,k,r,s,t)
        print('\n https://github.com/JavisG300/Modelacion-Financiera/blob/master/ModeloBinomial.py')
    else:
        print('El programa finalizó')
        print('\n https://github.com/JavisG300/Modelacion-Financiera/blob/master/ModeloBinomial.py')


if __name__ == '__main__':
    main()