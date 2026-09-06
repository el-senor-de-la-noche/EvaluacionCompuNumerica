import numpy as np
 
 
def cargar_dolar(ruta_csv="data/dolar_observado_sii_2022_2025.csv"):
    # names=True usa la primera fila del CSV como nombres de columna
    # dtype=None deja que numpy adivine el tipo de cada columna
    datos = np.genfromtxt(
        ruta_csv,
        delimiter=",",
        names=True,
        dtype=None,
        encoding="utf-8",
    )
 
    # Forzamos los tipos porque numpy a veces los deja mal inferidos
    anio = datos["anio"].astype(int)
    mes_num = datos["mes_num"].astype(int)
    precio = datos["dolar_observado_promedio_clp"].astype(float)
 
    # Etiqueta tipo "2022-01" para usar en los ejes de los gráficos
    etiqueta = np.array([f"{a}-{m:02d}" for a, m in zip(anio, mes_num)])
 
    return {
        "anio": anio,
        "mes_num": mes_num,
        "precio": precio,
        "etiqueta": etiqueta,
    }
 
 
if __name__ == "__main__":
    # Autoprueba: al correr "python src/cargar_datos.py" desde la
    # raíz del repo, debe imprimir 48 y el primer/último registro.
    d = cargar_dolar()
    print(len(d["precio"]))
    print(d["etiqueta"][0], d["precio"][0])
    print(d["etiqueta"][-1], d["precio"][-1])