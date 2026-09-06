#Integrantes: Elias Gonzalez, Daniel Navarrete
#Ramo: Computacion Numerica
import numpy as np
from cargar_datos import cargar_dolar
from errores import redondear_cifras_sig, error_absoluto, propagar_suma_resta
 
N_CIFRAS = 3  # el enunciado pide 3 cifras significativas para las restas
 
 
def variacion_anual():
    d = cargar_dolar()
    anios = np.unique(d["anio"])
 
    resultados = []
    for a in anios:
        # Ubicamos el precio de enero y de diciembre de este año
        mask_ene = (d["anio"] == a) & (d["mes_num"] == 1)
        mask_dic = (d["anio"] == a) & (d["mes_num"] == 12)
        p_ene = d["precio"][mask_ene][0]
        p_dic = d["precio"][mask_dic][0]
 
        # Redondeamos ambos precios antes de restar (así lo pide el enunciado)
        p_ene_r = redondear_cifras_sig(p_ene, N_CIFRAS)
        p_dic_r = redondear_cifras_sig(p_dic, N_CIFRAS)
 
        # Error absoluto de cada redondeo individual
        ea_ene = error_absoluto(p_ene, p_ene_r)
        ea_dic = error_absoluto(p_dic, p_dic_r)
 
        # Es una resta -> los errores absolutos se suman
        delta = p_dic_r - p_ene_r
        ea_delta = propagar_suma_resta(ea_ene, ea_dic)
        er_delta = ea_delta / abs(delta) * 100 if delta != 0 else np.inf
 
        resultados.append({
            "anio": int(a),
            "p_enero": p_ene_r,
            "p_diciembre": p_dic_r,
            "delta": delta,
            "ea_delta": ea_delta,
            "er_delta": er_delta,
        })
 
    # Menor error relativo = más confiable, va primero
    resultados.sort(key=lambda r: r["er_delta"])
    return resultados
 
 
if __name__ == "__main__":
    for r in variacion_anual():
        print(r["anio"], r["delta"], "+-", round(r["ea_delta"], 2), f"({r['er_delta']:.1f}%)")
