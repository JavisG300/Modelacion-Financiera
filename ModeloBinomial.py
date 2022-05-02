import string

def mbinomial(s,opcion,T,n,r,k,u,d):
    abecedario = list(string.ascii_uppercase)
    nodos      = {"A":s}
    lista_nodos=nodos.values()
    for i in range(n): #Por cada piso añadir y restar ¿como?
        nodos[abecedario[i+1]] = s*(1+u)
        nodos[abecedario[i+2]] = s*(1-d)
        lista_nodos.append(nodos.values())
    print(nodos)


s      = float(input("Indica el precio incial del activo subyacente: "))
opcion = float(input("""
Escribe el número de la opcion4 que será valuada
1) Call Europeo
2) Put Europeo
3) Call Americano
4) Put Americano
""")) 
T      = float(input("Indica el tiempo de vencimiento: "))
n      = float(input("Indica el número de periodos: "))
r      = float(input("Indica la tasa de interés anualizada: "))
k      = float(input("Indica el precio de ejercicio: "))
u      = float(input("Indica el porcentaje de subida: 1 + 0."))
d      = float(input("Indica el porcentaje de bajada: 1 - 0."))

if __name__ == '__main__':
    mbinomial()