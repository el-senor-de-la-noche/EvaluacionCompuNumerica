#Integrantes: Elias Gonzalez, Daniel Navarrete
#Ramo: Computacion Numerica

import numpy as np
import matplotlib.pyplot as plt
from cargar_datos import cargar_dolar


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


# A1. Error de representacion mes a mes (2 cifras significativas)

N_CIFRAS_PRECIO = 2   # cifras significativas para representar un precio (A1, A2, A5)
N_CIFRAS_RESTA = 3    # cifras significativas para restar dos meses parecidos (A3)
MONTO = 1_000_000.0


def a1_error_representacion():
    d = cargar_dolar()
    precios = d["precio"]

    redondeado = redondear_cifras_sig(precios, N_CIFRAS_PRECIO)
    ea = error_absoluto(precios, redondeado)
    er = error_relativo(precios, redondeado)

    idx_peor = int(np.argmax(er))
    return {
        "etiquetas": d["etiqueta"],
        "precio_real": precios,
        "precio_redondeado": redondeado,
        "ea": ea,
        "er": er,
        "mes_peor_error": d["etiqueta"][idx_peor],
        "peor_er": er[idx_peor],
    }


# A2 y A5. Compra-venta con propagacion de error (division, multiplicacion, resta)
def compra_venta(precio_compra, precio_venta, monto=MONTO, n_cifras=N_CIFRAS_PRECIO):
    # Redondeamos los precios (representacion en punto flotante "corto")
    pc_r = redondear_cifras_sig(precio_compra, n_cifras)
    pv_r = redondear_cifras_sig(precio_venta, n_cifras)
    er_pc = error_relativo(precio_compra, pc_r)
    er_pv = error_relativo(precio_venta, pv_r)

    # Comprar dolares = division: USD = Monto / Precio_compra
    # El monto se asume exacto -> su error relativo es 0
    usd = monto / pc_r
    er_usd = propagar_mult_div(0.0, er_pc)

    # Vender dolares = multiplicacion: pesos_final = USD * Precio_venta
    pesos_final = usd * pv_r
    er_pesos_final = propagar_mult_div(er_usd, er_pv)
    ea_pesos_final = (er_pesos_final / 100) * pesos_final

    # Ganancia = resta: G = pesos_final - Monto (Monto exacto -> Ea = 0)
    ganancia = pesos_final - monto
    ea_ganancia = propagar_suma_resta(ea_pesos_final, 0.0)
    er_ganancia = ea_ganancia / abs(ganancia) * 100 if ganancia != 0 else np.inf

    # Rentabilidad = division: rentabilidad = Ganancia / Monto * 100
    rentabilidad = ganancia / monto * 100
    er_rentabilidad = propagar_mult_div(er_ganancia, 0.0)

    return {
        "precio_compra_r": pc_r,
        "precio_venta_r": pv_r,
        "usd": usd,
        "ganancia": ganancia,
        "ea_ganancia": ea_ganancia,
        "er_ganancia": er_ganancia,
        "rentabilidad": rentabilidad,
        "er_rentabilidad": er_rentabilidad,
    }


# A3. Cancelacion: Dic-2022 (875.66) vs Dic-2023 (874.67), 3 cifras sig.
def a3_cancelacion():
    p_2022 = 875.66
    p_2023 = 874.67

    p22_r = redondear_cifras_sig(p_2022, N_CIFRAS_RESTA)
    p23_r = redondear_cifras_sig(p_2023, N_CIFRAS_RESTA)
    ea_22 = error_absoluto(p_2022, p22_r)
    ea_23 = error_absoluto(p_2023, p23_r)

    delta = p23_r - p22_r
    ea_delta = propagar_suma_resta(ea_22, ea_23)
    er_delta = ea_delta / abs(delta) * 100 if delta != 0 else np.inf

    return {
        "p_dic2022_r": p22_r,
        "p_dic2023_r": p23_r,
        "delta": delta,
        "ea_delta": ea_delta,
        "er_delta": er_delta,
        "afirmable": abs(delta) > ea_delta,
    }



# A5. Mejor compra y mejor venta (minimo y maximo global del periodo)
def a5_mejor_compra_venta():
    d = cargar_dolar()
    precios = d["precio"]

    idx_min = int(np.argmin(precios))
    idx_max = int(np.argmax(precios))

    resultado = compra_venta(precios[idx_min], precios[idx_max])
    resultado["mes_min"] = d["etiqueta"][idx_min]
    resultado["precio_min"] = precios[idx_min]
    resultado["mes_max"] = d["etiqueta"][idx_max]
    resultado["precio_max"] = precios[idx_max]
    return resultado


# Funciones de los graficos 1 a 4 
def graficar_serie_mensual(d):
    precios = d["precio"]
    plt.figure(figsize=(12, 5))
    plt.plot(range(len(precios)), precios, color="#1f77b4", linewidth=1.5)
    xt = range(0, len(precios), 3)
    plt.xticks(list(xt), [d["etiqueta"][i] for i in xt], rotation=90, fontsize=7)
    plt.ylabel("CLP por USD")
    plt.title("Dolar observado promedio mensual (SII), 2022-2025")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("graficos/1_serie_mensual.png")
    plt.close()


def graficar_variacion_mensual(d):
    precios = d["precio"]
    redondeado = redondear_cifras_sig(precios, N_CIFRAS_PRECIO)
    ea = error_absoluto(precios, redondeado)

    delta = np.diff(precios)
    ea_delta = ea[:-1] + ea[1:]  # resta -> se suman los errores absolutos
    colores = ["#2ca02c" if abs(dp) > e else "#d62728" for dp, e in zip(delta, ea_delta)]

    plt.figure(figsize=(12, 5))
    plt.bar(range(len(delta)), delta, color=colores)
    plt.errorbar(range(len(delta)), delta, yerr=ea_delta, fmt="none",
                 ecolor="black", elinewidth=0.7, capsize=2, alpha=0.6)
    xt = range(0, len(delta), 3)
    plt.xticks(list(xt), [d["etiqueta"][i + 1] for i in xt], rotation=90, fontsize=7)
    plt.ylabel("Variacion mensual (CLP)")
    plt.title("Variacion mes a mes con error propagado\nVerde = variacion supera al error | Rojo = cancelacion")
    plt.axhline(0, color="gray", linewidth=0.8)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("graficos/2_variacion_mensual.png")
    plt.close()


def graficar_error_representacion(d):
    precios = d["precio"]
    redondeado = redondear_cifras_sig(precios, N_CIFRAS_PRECIO)
    er = error_relativo(precios, redondeado)

    plt.figure(figsize=(12, 5))
    plt.bar(range(len(precios)), er, color="#9467bd")
    xt = range(0, len(precios), 3)
    plt.xticks(list(xt), [d["etiqueta"][i] for i in xt], rotation=90, fontsize=7)
    plt.ylabel("Error relativo (%)")
    plt.title(f"Error relativo de representacion por mes ({N_CIFRAS_PRECIO} cifras significativas)")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("graficos/3_error_representacion.png")
    plt.close()


def graficar_rentabilidad(d):
    precios = d["precio"]
    idx_min = int(np.argmin(precios))

    rentabilidades, errores = [], []
    for j in range(idx_min + 1, len(precios)):
        r = compra_venta(precios[idx_min], precios[j])
        rentabilidades.append(r["rentabilidad"])
        # Si el precio de venta redondeado coincide con el de compra
        # redondeamos, la ganancia simulada es 0 y el error relativo queda indefinido.
        if not np.isfinite(r["er_rentabilidad"]) or r["rentabilidad"] == 0:
            errores.append(0.0)
        else:
            errores.append(abs(r["er_rentabilidad"]) / 100 * abs(r["rentabilidad"]))

    xs = range(idx_min + 1, len(precios))
    plt.figure(figsize=(12, 5))
    plt.bar(xs, rentabilidades, yerr=errores, color="#ff7f0e",
            ecolor="black", capsize=2, error_kw={"elinewidth": 0.7, "alpha": 0.6})
    xt = [i for i in xs if i % 3 == 0]
    plt.xticks(xt, [d["etiqueta"][i] for i in xt], rotation=90, fontsize=7)
    plt.ylabel("Rentabilidad (%)")
    plt.title(f"Rentabilidad de comprar en el minimo ({d['etiqueta'][idx_min]}) y vender despues")
    plt.axhline(0, color="gray", linewidth=0.8)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("graficos/4_rentabilidad_min_vs_meses.png")
    plt.close()


if __name__ == "__main__":
    # Autoprueba con los ejemplos exactos del enunciado
    r1 = redondear_cifras_sig(963.44, 2)
    r2 = redondear_cifras_sig(1000.76, 3)
    print(r1, r2)
    print(error_absoluto(963.44, r1), error_relativo(963.44, r1))

    print("\n=== A1: error de representacion ===")
    a1 = a1_error_representacion()
    print(f"Mes con mayor error relativo: {a1['mes_peor_error']} ({a1['peor_er']:.3f}%)")

    print("\n=== A2: compra-venta (ejemplo Mayo-2023 -> Enero-2025) ===")
    a2 = compra_venta(798.64, 1000.76)
    print(f"Ganancia = {a2['ganancia']:.0f} +- {a2['ea_ganancia']:.0f} ({a2['er_ganancia']:.2f}%)")

    print("\n=== A3: cancelacion Dic-2022 vs Dic-2023 ===")
    a3 = a3_cancelacion()
    print(f"delta = {a3['delta']:+.2f} +- {a3['ea_delta']:.2f} ({a3['er_delta']:.1f}%) "
          f"-> afirmable: {a3['afirmable']}")

    print("\n=== A5: mejor compra y mejor venta ===")
    a5 = a5_mejor_compra_venta()
    print(f"Comprar en {a5['mes_min']} ({a5['precio_min']:.2f}), "
          f"vender en {a5['mes_max']} ({a5['precio_max']:.2f})")
    print(f"Rentabilidad = {a5['rentabilidad']:.2f}% +- {a5['er_rentabilidad']:.2f}%")

    print("\nGenerando graficos 1 a 4...")
    d = cargar_dolar()
    graficar_serie_mensual(d)
    graficar_variacion_mensual(d)
    graficar_error_representacion(d)
    graficar_rentabilidad(d)
    print("Listo, guardados en graficos/")
