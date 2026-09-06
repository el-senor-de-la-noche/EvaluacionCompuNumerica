import numpy as np


def redondear_cifras_sig(x, n):
    x = np.asarray(x, dtype=float)
    with np.errstate(divide="ignore"):
        exponente = np.floor(np.log10(np.abs(np.where(x == 0, 1, x))))
    decimales = (n - 1 - exponente).astype(int)
    factor = 10.0 ** decimales
    resultado = np.round(x * factor) / factor
    resultado = np.where(x == 0, 0.0, resultado)
    return resultado.item() if resultado.ndim == 0 else resultado


def error_absoluto(valor_real, valor_aprox):
    return np.abs(np.asarray(valor_real, dtype=float) - np.asarray(valor_aprox, dtype=float))


def error_relativo(valor_real, valor_aprox, porcentaje=True):
    ea = error_absoluto(valor_real, valor_aprox)
    er = ea / np.abs(np.asarray(valor_real, dtype=float))
    return er * 100 if porcentaje else er


def propagar_mult_div(er_a, er_b):
    return np.asarray(er_a, dtype=float) + np.asarray(er_b, dtype=float)


def propagar_suma_resta(ea_a, ea_b):
    return np.asarray(ea_a, dtype=float) + np.asarray(ea_b, dtype=float)


if __name__ == "__main__":
    r1 = redondear_cifras_sig(963.44, 2)
    r2 = redondear_cifras_sig(1000.76, 3)
    print(r1, r2)
    print(error_absoluto(963.44, r1), error_relativo(963.44, r1))