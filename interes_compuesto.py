def inter(m,r,n):
    factor = (1 + r / m)**(n*m)
    print(factor)
m = 1     #Periodo de capitalizacion; anual, semestral, bimestral, etc.
r = 0.08  #Tasa
n = 1     #Numero de años
if __name__ == '__main__':
    inter(m,r,n)