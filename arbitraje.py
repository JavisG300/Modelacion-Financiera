import numpy as np
def main():
    S0  = 1.05    #Precio hoy del activo subyacente
    K   = 1.05    #Precio de ejercicio del futuro o forward
    T   = 2/12    #Fecha caducación en meses
    TLR = 0.02    #Tasa libre de riesgo
    F = S0*np.exp(TLR*T)
    
    if F > K:
        print('Se toma una posición corta respecto al activo (se vende)')
    else:
        print('Se toma una posicion larga respecto al activo (se compra)')
    


if __name__ == '__main__':
    main()