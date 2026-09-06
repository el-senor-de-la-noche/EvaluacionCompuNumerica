import numpy as np
import matplotlib.pyplot as plt
from cargar_datos import cargar_dolar
from errores import redondear_cifras_sig, error_absoluto
 
def demo_b1():
    # Guardar 3 cifras significativas es lo mismo que truncar la
    # mantisa a pocos bits: perdemos información y eso es un error.
    x = 1000.76
    x3 = redondear_cifras_sig(x, 3)
    print(x, "->", x3, "error =", error_absoluto(x, x3))
 
 
def ida_y_vuelta(monto=1_000_000.0):
    # Convertimos M a dólares y de vuelta a pesos con el MISMO precio.
    # Matemáticamente M/P*P = M exacto; medimos si la máquina lo cumple.
    d = cargar_dolar()
    precios = d["precio"]
 
    usd = monto / precios
    monto_final = usd * precios
    diferencia = monto_final - monto  # debería ser ~0 en todos los meses
 
    plt.figure(figsize=(10, 4))
    plt.plot(d["etiqueta"], diferencia, marker="o")
    plt.xticks(rotation=90, fontsize=6)
    plt.ylabel("Diferencia respecto a M (CLP)")
    plt.title("Deriva de la ida y vuelta en punto flotante")
    plt.tight_layout()
    plt.savefig("graficos/ida_y_vuelta.png")
    plt.close()
 
    return diferencia
 
 
def demo_b4():
    # Misma resta en dos precisiones distintas para comparar
    # cuántas cifras confiables quedan en cada una.
    a = np.float32(875.66)
    b = np.float32(874.67)
    r32 = a - b  # el valor exacto sería 0.99
 
    c = np.float64(875.66)
    e = np.float64(874.67)
    r64 = c - e
 
    print("float32:", r32)
    print("float64:", r64)
    return r32, r64
 
 
if __name__ == "__main__":
    demo_b1()
    ida_y_vuelta()
    demo_b4()