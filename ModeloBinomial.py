import string                #Para hacer el diccionario de nodos con letras
import numpy as np           #Para exp
from pandas import DataFrame #Para hacer una tabla con los datos
from math import factorial
from paridad_put_call import paridad #Función de paridad put call programada anteriormente

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
        lista_nodos.append(up)
        integrantes = len(lista_nodos)
        dif = abs(lista_nodos[(integrantes-1)] - lista_nodos[(integrantes-2)])
        if dif <= 0.01:
           lista_nodos.pop()
                
        else:
            lista_nodos

        down = s*d
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
    return dic_nodos

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

def mbinomial(s,opcion,T,n,r,k,u,d): #Funcion para determinar el precio de la opcion
    T = T/12
    Dt = T/n
    Propabilidad = (np.exp(r*Dt) - d)/(u - d)
    uno_probabilidad = 1 - Propabilidad
    valor_presente1 = np.exp(-n*r*Dt)
    valor_presenteT = np.exp(-r*Dt)

    #Calculando el valor de la opción
    if opcion == 1:
        cuenta = 0
        Nodos = nodos(s,u,d,n)
        lista_de_nodos = []
        lcu_y_cd = []
        for value in Nodos.values():
            valor = value 
            lista_de_nodos.append(valor)
        for i in range(len(lista_de_nodos)-1,len(lista_de_nodos)-(n+2),-1):
            lcu_y_cd.append(lista_de_nodos[i])
        lcu_y_cd = lcu_y_cd[::-1]
        for i in range(n+1):
            cu = max(lcu_y_cd[i]-k,0)
            combinancion = factorial(n)/((factorial(i))*(factorial(n-i)))
            cuenta = cuenta + combinancion*(Propabilidad**(n-i))*((uno_probabilidad)**i)*cu 
        valor_del_call = valor_presente1 * cuenta
        return valor_del_call, Nodos

    elif opcion == 2:
        cuenta = 0
        Nodos = nodos(s,u,d,n)
        lista_de_nodos = []
        lcu_y_cd = []     
        for value in Nodos.values():
            valor = value 
            lista_de_nodos.append(valor)
        for i in range(len(lista_de_nodos)-1,len(lista_de_nodos)-(n+2),-1):
            lcu_y_cd.append(lista_de_nodos[i])
        lcu_y_cd = lcu_y_cd[::-1]
        for i in range(n+1):
            cu = max(k-lcu_y_cd[i],0)
            combinancion = factorial(n)/((factorial(i))*(factorial(n-i)))
            cuenta = cuenta + combinancion*(Propabilidad**(n-i))*((uno_probabilidad)**i)*cu 
        valor_del_put = valor_presente1 * cuenta
        return valor_del_put, Nodos

    elif opcion == 3:
        Nodos = nodos(s,u,d,n)
        lista_de_nodos = []
        lcu_y_cd = []
        lista_llaves = []
        for value in Nodos.values():
            valor = value 
            lista_de_nodos.append(valor)
        for i in range(len(lista_de_nodos)-(n+1)):
            lcu_y_cd.append(lista_de_nodos[i])
        lcu_y_cd = lcu_y_cd[::-1]
        for i in range(len(lcu_y_cd)-1):
            nodo_evaluar = lcu_y_cd[i]
            up = nodo_evaluar*u
            maxup = max(up-k,0)
            down = nodo_evaluar*d
            maxdown = max(down-k,0)
            call = valor_presenteT*(maxup*Propabilidad + maxdown*uno_probabilidad)
            rendimiento_ejercer = max(nodo_evaluar-k,0)
            if rendimiento_ejercer > call:
                lcu_y_cd[i] = rendimiento_ejercer
            else:
                lcu_y_cd[i] = call
        lcu_y_cd = lcu_y_cd[::-1]
        for value in Nodos.keys():
            llave = value 
            lista_llaves.append(llave)
        for i in range(len(lcu_y_cd)):
            Nodos[lista_llaves[i]] = lcu_y_cd[i]
        valor_del_call_americano = valor_presenteT*(Propabilidad*lcu_y_cd[1] + uno_probabilidad*lcu_y_cd[2])
        Nodos['A'] = valor_del_call_americano
        return valor_del_call_americano, Nodos


    elif opcion == 4:
        Nodos = nodos(s,u,d,n)
        lista_de_nodos = []
        lcu_y_cd = []
        lista_llaves = []
        for value in Nodos.values():
            valor = value 
            lista_de_nodos.append(valor)
        for i in range(len(lista_de_nodos)-(n+1)):
            lcu_y_cd.append(lista_de_nodos[i])
        lcu_y_cd = lcu_y_cd[::-1]
        for i in range(len(lcu_y_cd)-1):
            nodo_evaluar = lcu_y_cd[i]
            up = nodo_evaluar*u
            maxup = max(k-up,0)
            down = nodo_evaluar*d
            maxdown = max(k-down,0)
            put = valor_presenteT*(maxup*Propabilidad + maxdown*uno_probabilidad)
            rendimiento_ejercer = max(k-nodo_evaluar,0)
            if rendimiento_ejercer > put:
                lcu_y_cd[i] = rendimiento_ejercer
            else:
                lcu_y_cd[i] = put
        lcu_y_cd = lcu_y_cd[::-1]
        for value in Nodos.keys():
            llave = value 
            lista_llaves.append(llave)
        for i in range(len(lcu_y_cd)):
            Nodos[lista_llaves[i]] = lcu_y_cd[i]
        valor_del_put_americano = valor_presenteT*(Propabilidad*lcu_y_cd[1] + uno_probabilidad*lcu_y_cd[2])
        Nodos['A'] = valor_del_put_americano
        return valor_del_put_americano, Nodos

def tabla_comparativa(s,T,n,t,k,u,d):
    datos={'Opción':['Europeo', 'Europeo','Americano', 'Americano'], 'Precio/Nodos':[mbinomial(s,1,T,n,r,k,u,d),
    mbinomial(s,2,T,n,r,k,u,d),mbinomial(s,3,T,n,r,k,u,d),mbinomial(s,4,T,n,r,k,u,d)]}
    tabla_datos = DataFrame(datos, columns = ['Opción','Precio/Nodos'], 
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
T      = float(input("Indica el tiempo de vencimiento en meses: "))
n      = int(input("Indica el número de periodos: "))
r      = float(input("Indica la tasa de interés anualizada de forma decimal: "))
k      = float(input("Indica el precio de ejercicio: "))
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
    print(f'El precio del {tipo} solicitado es:{l[0]} \n')
    print(f'Los nodos de la ocpión son: {l[1]} \n \n')
    print("""
    ---------------------------------------------------------------------------------------------------------------
    || A continuación se muestra una tabla comparativa de la opción solicitada junto a los demás tipos de opción || 
    ---------------------------------------------------------------------------------------------------------------
    """)
    tabla_comparativa(s,T,n,r,k,u,d)
    print('\n')
    Paridad = input(('¿Quieres comprobar la paridad Put-Call entre algunas de las opciones. y/n'))
    Paridad = Paridad.lower()
    if Paridad == 'y':
        OpCall = int(input("""
        ¿Qué Call quieres usar? 

        1) Americano
        2) Europeo 
        """))
        OpPut = int(input("""
        ¿Qué Put quieres usar? 

        1) Americano
        2) Europeo 
        """))
        if OpCall == 1:
            c = mbinomial(s,3,T,n,r,k,u,d)
            C = c[0]

        else:
            c = mbinomial(s,1,T,n,r,k,u,d)
            C = c[0]
        
        if OpPut == 1:
            p = mbinomial(s,4,T,n,r,k,u,d)
            P = p[0]

        else:
            p = mbinomial(s,2,T,n,r,k,u,d)
            P = p[0]
            
        t=T/12
        paridad(C,P,k,r,s,t)
    else:
        print('El programa finalizó')


if __name__ == '__main__':
    main()