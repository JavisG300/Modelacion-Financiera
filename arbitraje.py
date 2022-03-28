import numpy as np
def main(S0, K, T, TLR):
    F = S0*np.exp(TLR*T)
    
    if F > K:
        print(F,'>',K,'Se toma una posición corta respecto al activo (se vende)')
    else:
        print(F,'<',K,'Se toma una posicion larga respecto al activo (se compra con dinero del banco)')
    
S0  = 21    #Precio hoy del activo subyacente
K   = 24    #Precio de ejercicio del futuro o forward
T   = 12/12    #Fecha caducación en meses
TLR = 0.05    #Tasa libre de riesgo

if __name__ == '__main__':
    main(S0, K, T, TLR)