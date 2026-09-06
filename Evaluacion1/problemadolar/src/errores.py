#Integrantes: Elias Gonzalez, Daniel Navarrete
#Ramo: Computacion Numerica

import numpy as np
 
 
def redondear_cifras_sig(x, n):
    # Redondea x a n cifras significativas.
    # Ejemplos del enunciado:
    #   963.44 con 2 cifras  -> 960.0
    #   1000.76 con 3 cifras -> 1000.0
    x = np.asarray(x, dtype=float)
 
    # log10(x) da el orden de magnitud; floor() lo deja como entero.
    # np.where evita romper el cálculo si x trae algún 0.
    with np.errstate(divide="ignore"):
        exponente = np.floor(np.log10(np.abs(np.where(x == 0, 1, x))))
 
    # Cuántos decimales hay que conservar para dejar n cifras en total
    decimales = (n - 1 - exponente).astype(int)
    factor = 10.0 ** decimales
 
    # Redondear multiplicando, aproximando al entero y dividiendo de vuelta
    resultado = np.round(x * factor) / factor
    resultado = np.where(x == 0, 0.0, resultado)
 
    # Si la entrada fue un solo número, devolvemos un solo número
    return resultado.item() if resultado.ndim == 0 else resultado
 
 
def error_absoluto(valor_real, valor_aprox):
    # Ea = |valor_real - valor_aproximado|, en las mismas unidades del valor
    return np.abs(np.asarray(valor_real, dtype=float) - np.asarray(valor_aprox, dtype=float))
 
 
def error_relativo(valor_real, valor_aprox, porcentaje=True):
    # Er = Ea / |valor_real|, opcionalmente expresado en %
    ea = error_absoluto(valor_real, valor_aprox)
    er = ea / np.abs(np.asarray(valor_real, dtype=float))
    return er * 100 if porcentaje else er
 
 
def propagar_mult_div(er_a, er_b):
    # En multiplicación y división los errores RELATIVOS se suman.
    # Ambos parámetros deben venir en la misma unidad (ambos % o ambos fracción).
    return np.asarray(er_a, dtype=float) + np.asarray(er_b, dtype=float)
 
 
def propagar_suma_resta(ea_a, ea_b):
    # En suma y resta los errores ABSOLUTOS se suman.
    return np.asarray(ea_a, dtype=float) + np.asarray(ea_b, dtype=float)
 
 
if __name__ == "__main__":
    # Autoprueba con los ejemplos exactos del enunciado
    r1 = redondear_cifras_sig(963.44, 2)
    r2 = redondear_cifras_sig(1000.76, 3)
    print(r1, r2)
    print(error_absoluto(963.44, r1), error_relativo(963.44, r1))
