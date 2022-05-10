import numpy as np
def paridad(c,p,k,r,S0,t):
    call = c + k*np.exp(-r*t)
    call = round(call,6)
    put  = p + S0 
    put  = round(put,6) 
    estrategia(c,p,k,r,S0,t,put,call)

def estrategia(c,p,k,r,S0,t,put,call):
    if call > put:
        print('Si hay oportunidad de arbitraje')
        print('El call está sobrevaluado y el put subvaluado')
        print(f'Se va a comprar el put y el activo subyacente {-p - S0} y se venderá el call en {c} = {-p - S0 + c}')
        print(f'1) Para comprar el put y la acción se piden al banco {p + S0 - c} a una tasa de: {r}% a pagar en {t * 12} meses')
        print(f'2) Después de {t} meses se debe pagar al banco {(p + S0 - c)*np.exp(r*t)}')
        print('Se tienen dos opciones: ')
        print(f'Si ST > K ----> Se ejerce el call y yo gano {k}')
        print(f'Si ST < K ----> Se ejerce el put y gano {k}')
        print(f'Beneficio: {k - (p + S0 - c)*np.exp(r*t) }')

    elif put > call:
        print('Si hay oportunidad de arbitraje')
        print('El put está sobrevaluado y el call subvaluado')
        print(f'Se va a comprar el call {-c} y se venderá el put + el activo subayacente {p + S0} = {p + S0 - c}')
        print(f'1) Se invierte en el banco {p + S0 - c} a una tasa de: {r}%  a pagar en {t * 12} meses')
        print(f'2) Después de {t*12} meses se recibe del banco {(p + S0 - c)*np.exp(r*t)}')
        print('Se tienen dos opciones: ')
        print(f'Si ST > K ----> Se ejerce el call y pago {k}')
        print(f'Si ST < K ----> Se ejerce el put y pago {k}')
        print(f'Beneficio: {(p + S0 - c)*np.exp(r*t) - k}')
    elif call == put:
        print(f'No hay oportunidad de arbitraje {call} = {put} ')

c  = 2.162771        #valor del call
p  = 1.903577      #valor del put
k  = 51        #precio de ejercicio
r  = 0.05      #tasa de interes
S0 = 50        #precio al inicio
t  = 6/12      #tiempo de vencimiento


if __name__ == '__main__':
    paridad(c,p,k,r,S0,t)