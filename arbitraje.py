import numpy as np
def main(S0, K, T, TLR):
    F = S0*np.exp(TLR*T)
    estrategia(S0,K,T,TLR,F)

def estrategia(S0,K,T,TLR,F):
    if F > K:
        print('Se toma una posición corta respecto al activo, se vende el activo en: ' + str(S0))
        print('1) Se invierte ' + str(S0) + ' en el banco a una tasa de ' + str(TLR))
        print('2) Se pacta un futuro para comprar a ' + str(K))
        print('3) Despues de ' + str(T*12) + ' meses se cobran del banco ' + str(F) + ' y se compra el activo en ' + str(K))
        print('Beneficio: ', F - K)
    else:
        print('Se toma una posición larga respecto al activo, se compra el activo con dinero del banco: ' + str(S0))
        print('1) Se pide al banco ' + str(S0) + ' a una tasa de ' + str(TLR))
        print('2) Se pacta un futuro para vender en ' + str(K))
        print('3) Despues de ' + str(T*12) + ' meses se vende el activo en ' + str(K)  + ' y se paga al banco ' + str(F))
        print('Beneficio: ', K - F)
    
S0  = 1.05    #Precio hoy del activo subyacente
K   = 1.05    #Precio de ejercicio del futuro o forward
T   = 2/12    #Fecha caducación en meses
TLR = 0.02    #Tasa libre de riesgo

if __name__ == '__main__':
    main(S0, K, T, TLR)