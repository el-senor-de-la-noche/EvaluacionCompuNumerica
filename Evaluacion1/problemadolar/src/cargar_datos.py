import numpy as np

def cargar_dolar(ruta_csv = "data/dolar_observado_sii_2022_2025.csv"):
    
    datos = np.genfromtxt(
        ruta_csv,
        delimiter=",",
        names=True,
        dtype=None,
        encoding="utf-8"
    )
    anio = datos["anio"].astype(int)
    mes_num = datos["mes_num"].astype(int)
    precio = datos["dolar_observado_promedio_clp"].astype(float)

    etiqueta = np.array([f"{a}-{m:02d}" for a, m in zip(anio, mes_num)])

    return {
        "anio": anio,
        "mes_num": mes_num,
        "precio": precio,
        "etiqueta": etiqueta
    }

if __name__ == "__main__":
    d = cargar_dolar()
    print("cantidad de meses cargados:" , len(d["precio"]))
    print("primer registro:", d["etiqueta"][0],d["precio"][0])
    print("ultimo registro:", d["etiqueta"][-1],d["precio"][-1])

#daniel gay
