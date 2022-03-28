from math import exp
def main(S0,K,TLR,T,O):
    if O == True:
        inferior_limit = max(S0 - K*exp(-TLR*T),0)
        superior_limit = S0
        print(str(inferior_limit) + ' <= c <= ' + str(superior_limit))
    else:
        inferior_limit = max(K*exp(-TLR*T) - S0,0)
        superior_limit = K*exp(-TLR*T)
        print(str(inferior_limit) + ' <= p <= ' + str(superior_limit))

S0   = 12     #Precio hoy
K    = 15     #Precio de ejercicio
TLR  = 0.06   #Tasa
T    = 1/12   #Vencimiento en meses
O    = False  #Bandera True es call, False es put


if __name__=='__main__':
    main(S0,K,TLR,T,O)