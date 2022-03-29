from interes_compuesto import inter
def main():
    cap = int(input(""" Elige el periodo de capitalización:

    1) Anual
    2) Semestral
    3) Cuatrimestral
    4) Trimestral
    12) Mensual
    """))

    rate = float(input("""
    ¿Cuál es la tasa de interés?
    """))

    years = float(input("""
    ¿Por cuántos años es la inversión?
    """))

    inter(cap,rate,years)


if __name__ == '__main__':
    main()