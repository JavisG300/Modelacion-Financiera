def mbinomial():
    pass

s      = int(input("Indica el precio incial del activo subyacente: "))
opcion = int(input("""
Escribe el número de la opcion que será valuada
1) Call Europeo
2) Put Europeo
3) Call Americano
4) Put Americano
""")) 
T      = int(input("Indica el tiempo de vencimiento: "))
n      = int(input("Indica el número de periodos: "))
r      = int(input("Indica la tasa de interés anualizada: "))
k      = int(input("Indica el precio de ejercicio: "))
u      = int(input("Indica el porcentaje de subida: 1 + 0."))
d      = int(input("Indica el porcentaje de bajada: 1 - 0."))

if __name__ == '__main__':
    mbinomial()