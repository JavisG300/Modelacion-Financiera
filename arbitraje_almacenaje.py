import numpy as np
def main(S0, K, T, TLR,CA):
    F1 = S0*np.exp(TLR*T)
    F2 = S0*np.exp(TLR*T) + CA
    estrategia(S0,K,T,TLR,F1,F2)

def estrategia(S0,K,T,TLR,F1,F2):
    if F1 > K:
        print('Se toma una posición corta respecto al activo, se vende el activo en: ' + str(S0))
        print('1) Se invierte ' + str(S0) + ' en el banco a una tasa de ' + str(TLR) + ' para recibir ' + str(F1))
        print('2) Se pacta un futuro para comprar a ' + str(K))
        print('3) Despues de ' + str(T*12) + ' meses se cobran del banco ' + str(F1) + ' y se compra el activo en ' + str(K))
        print('Beneficio: ', F1 - K)
    elif F2 < K:
        print('Se toma una posición larga respecto al activo, se compra el activo con dinero del banco: ' + str(S0))
        print('1) Se pide al banco ' + str(S0) + ' a una tasa de ' + str(TLR))
        print('2) Se pacta un futuro para vender en ' + str(K))
        print('3) Despues de ' + str(T*12) + ' meses se vende el activo en ' + str(K)  + ' y se paga al banco ' + str(F2))
        print('Beneficio: ', K - F2)

S0  = 552.77    #Precio hoy del activo subyacente
K   = 575.30    #Precio de ejercicio del futuro o forward
T   = 12/12    #Fecha caducación en meses
TLR = 0.08    #Tasa libre de riesgo
CA  = 11.6    #Costo de almacenaje a futuro, CUIDADO con la capitalización
if __name__ == '__main__':
    main(S0, K, T, TLR,CA)