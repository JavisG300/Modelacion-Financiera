#Modelo Binomial para valuar opciones tipo Call y Put (sin incorporar volatilidad)
#Datos que se necesitan: ¿Es un call o es un put?, ¿Europeo o americano?, S0, K, r, T, n, u, d
#Datos que se pueden calcular a partir de los anteriores:
# pu: "prob al alza", 1-pu: "prob a la baja", DeltaT: dt=T/n, Valor Presente o factor de descuento: VP=exp(-r*dT)
#Librerías que usaremos:

import numpy as np  #Para usar la exponencial, también se puede usar math
from pandas import DataFrame  #Sirve para hacer una tabla
import matplotlib.pyplot as plt  #Harémos un gráfico para ver la convergencia


#PARTE I: pedimos los datos al usuario

tipo_opcion=input("Indique el tipo de opcion a valuar (""c""= call, ""p""= put) : ")
if tipo_opcion=='c':
    tipo_opcion="call"
    cop=1
else:
    tipo_opcion="put"
    cop=-1
clase=input("Indique si el {tipo_opcion} es europeo o americano (""e""= europeo, ""a""= americano) : "\
            .format(tipo_opcion=tipo_opcion))
if clase=='e':
    clase = " europeo"
else:
    clase = " americano"
tipo_opcion=tipo_opcion+clase

S0=float(input("Indique el precio hoy del activo subyacente S0: "))
K=float(input("Indique el precio de ejercicio K: "))
T=float(input("Indique el Tiempo "'T'" al vencimiento en meses: "))
n=int(input("Indique el número de periodos (ramas) n: "))
r=float(input("Indique la tasa ANUAL Libre de Riesgo en unidades porcentuales r:  "))
u=float(input("Indique factor al alza en términos porcentuales u: "))
d=float(input("Indique factor a la baja en términos porcentuales d: "))

#Cambiamos a decimales los porcentajes y calculamos el resto de los datos necesarios

r=0.01*r
u=1+0.01*u
d=1-0.01*d
T=T/12
Dt=T/n
pu1=(np.exp(r*Dt)-d)/(u-d)
pd1=1-pu1
VP1=np.exp(-r*Dt)
VPT=np.exp(-r*T)

#construimos una tabla para visualizar los datos
datos = {'Abreviatura': ['','S0 =', 'K =', 'T =','n =','dt =', 'r =', 'u =','d =','pu =','pd =', 'VP =','VPT ='],
        'Valor Ingresado': [tipo_opcion, S0, K, T, n, Dt, r , u, d, pu1, pd1, VP1, VPT]}
cuadro_datos = DataFrame(datos, columns=['Abreviatura', 'Valor Ingresado'], 
                   index=['Tipo de opción','Precio Hoy del activo subyacente', 'Precio de Ejercicio', 'Tiempo al vencimiento',\
                          'Número de Periodos','DeltaT', 'Tasa Anual Libre de Riesgo', 'Factor al alza','Factor a la baja',\
                          'Probabilidad al alza','Probabilidad a la baja', 'Factor de Descuento cada dt','Factor de Descuento al tiempo T'])
print(cuadro_datos.round(4))
#Parte II: Definimos funciones para calcular el precio de la opción
def binomialE(S0,K,T,r,n,u,d,cop):  #call o put tipo europeo
    
    pu=(np.exp(r*T/n)-d)/(u-d)
    pd=1-pu
    VP=np.exp(-r*T/n)
    
    S= np.zeros((n+1,n+1))  #Creamos una matriz de ceros del precio de la acción de tamaño uno más que el número de ramas (n+1 puntos)
    S[0,0] = S0             #Asignamos a la primer entrada el precio S0
    for i in range(1,n+1):  #Para crear la trayectoria de los precios, llenamos la primera fila con los incrementos u
        S[0,i] = S[0,i-1]*u
        for j in range(1,n+1):    # Y para cada incremento vamos llenando cuando baja en el factor d
            S[j,i]=S[j-1,i-1]*d
            
    VOPC=np.zeros((n+1,n+1)) #Ahora creamos una matriz con el precio de la opción y calculamos el valor de la opción en los nodos finales
    for i in range(n+1):
        VOPC[i,n]=max(cop*(S[i,n]-K),0)  #Hay que notar que si cop=-1 estamos calculando el precio de un put
    
    #Usamos el modelo binomial para ir calculando hacia atrás el precio de la opción    
    for i in range(n-1, -1, -1):  #inicia en el penúltimo nodo hasta acabar disminuyendo en 1
        for j in range(0,i+1):
            VOPC[(j, i)] = VP * (pu * VOPC[(j, i+1)] + pd*VOPC[(j+1, i+1)])
            
    return(VOPC[0,0])

def binomialA(S0,K,T,r,n,u,d,cop):  #call o put tipo americano
    
    pu=(np.exp(r*T/n)-d)/(u-d)
    pd=1-pu
    VP=np.exp(-r*T/n)
    
    S= np.zeros((n+1,n+1))
    S[0,0] = S0
    for i in range(1,n+1):
        S[0,i] = S[0,i-1]*u
        for j in range(1,n+1):
            S[j,i]=S[j-1,i-1]*d
    VOPC=np.zeros((n+1,n+1))
    
    for i in range(n+1):
        VOPC[i,n]=max(cop*(S[i,n]-K),0)
    
    for i in range(n-1, -1, -1):
        for j in range(0,i+1):  #La función sólo cambia en esta línea siguiente, comparando nodos
            VOPC[(j, i)] = max(cop*(S[j,i]-K), VP*(pu * VOPC[(j, i+1)] + pd*VOPC[(j+1, i+1)]))
            
    return(VOPC[0,0])

ce=binomialE(S0,K,T,r,n,u,d,1)
pe=binomialE(S0,K,T,r,n,u,d,-1)
ca=binomialA(S0,K,T,r,n,u,d,1)
pa=binomialA(S0,K,T,r,n,u,d,-1)
if clase==" europeo":
    print("EL precio del {tipo_opcion} con {n} ramas es: ".format(tipo_opcion=tipo_opcion, n=n),binomialE(S0,K,T,r,n,u,d,cop))
if clase==" americano":
    print("EL precio del {tipo_opcion} con {n} ramas es: ".format(tipo_opcion=tipo_opcion,n=n),binomialA(S0,K,T,r,n,u,d,cop))

if clase == " europeo":
    if cop==1:
        ppc_put=ce+K*VPT-S0
        print('Usando la Paridad Put-Call el precio del\nput europeo es = ',ppc_put)
    if cop==-1:
        ppc_call=pe+S0-K*VPT
        print('Usando Paridad Put-Call el precio del\ncall europeo es = ',ppc_call)
        
precios = {'Tipo de Opción':['Call', 'Put','Call','Put'], 'Clase':['europeo','europeo','americano','americano'],\
                  'Precio':[ce, pe, ca, pa]}
cuadro_precios = DataFrame(precios, columns=['Tipo de Opción', 'Clase','Precio'], index=['1. ', '2. ','3. ','4. '])
index = cuadro_precios.index
index.name = 'Resumen'
print(cuadro_precios.round(6))