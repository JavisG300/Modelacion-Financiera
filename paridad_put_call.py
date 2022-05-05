import numpy as np
def paridad(c,p,k,r,S0,t):
    call = c + k*np.exp(-r*t)
    put  = p + S0 
    estrategia(c,p,k,r,S0,t,put,call)

def estrategia(c,p,k,r,S0,t,put,call):
    if call > put:
        print('Si hay oportunidad de arbitraje')
        print('El call está sobrevaluado y el put subvaluado')
        print('Se va a comprar el put y el activo subyacente ' + str(-p - S0) + ' y se venderá el call ' + str(c) + ' = ' + str(-p - S0 + c))
        print('1) Para comprar el put y la acción se piden al banco ' + str(p + S0 - c) + ' a una tasa de: ' + str(r) + ' a pagar en ' + str(t * 12) + ' meses')
        print('2) Después de ' + str(t) + ' se debe pagar al banco ' + str((p + S0 - c)*np.exp(r*t)))
        print('Se tienen dos opciones: ')
        print('Si ST > K ----> Se ejerce el call y yo gano ' + str(k))
        print('Si ST < K ----> Se ejerce el put y gano ' + str(k))
        print('Beneficio: ' + str(k - (p + S0 - c)*np.exp(r*t) ))

    elif put > call:
        print('Si hay oportunidad de arbitraje')
        print('El put está sobrevaluado y el call subvaluado')
        print('Se va a comprar el call ' + str(-c) + ' y se venderá el put + el activo subayacente ' + str(p + S0) + ' = ' + str(p + S0 - c))
        print('1) Se invierte en el banco ' + str(p + S0 - c) + ' a una tasa de: ' + str(r) + ' a pagar en ' + str(t * 12))
        print('2) Después de ' + str(t) + ' se recibe del banco ' + str((p + S0 - c)*np.exp(r*t)))
        print('Se tienen dos opciones: ')
        print('Si ST > K ----> Se ejerce el call y pago ' + str(k))
        print('Si ST < K ----> Se ejerce el put y pago ' + str(k))
        print('Beneficio: ' + str((p + S0 - c)*np.exp(r*t) - k))
    elif call == put:
        print('No hay oportunidad de arbitraje')

c  = 3         #valor del call
p  = 2.25      #valor del put
k  = 30        #precio de ejercicio
r  = 0.10      #tasa de interes
S0 = 31        #precio al inicio
t  = 3/12      #tiempo de vencimiento


if __name__ == '__main__':
    paridad(c,p,k,r,S0,t)