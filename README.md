# Problema — La ganancia que se evapora

Cancelación y propagación del error con el dólar observado del SII (2022–2025).
Laboratorio evaluado 1 — Análisis de error (cifras significativas, punto flotante,
error absoluto, relativo y propagación).

**Integrantes:** Elias Gonzalez, Daniel Navarrete

## Estructura

```
problema2-dolar-sii/
├── README.md
├── INFORME.md              <- documento de entrega con la conclusión
├── requirements.txt
├── data/
│   └── dolar_observado_sii_2022_2025.csv
├── src/
│   ├── cargar_datos.py     <- carga el CSV con numpy (np.genfromtxt)
│   ├── errores.py          <- error absoluto, relativo y propagado entre puntos
│   │                          (funciones base + A1, A2, A3, A5 + gráficos 1-4)
│   ├── anualidad.py        <- variación y error año a año (A4)
│   └── punto_flotante.py   <- float32/float64, ida y vuelta, cancelación (B1, B2, B4)
└── graficos/
    ├── 1_serie_mensual.png
    ├── 2_variacion_mensual.png
    ├── 3_error_representacion.png
    ├── 4_rentabilidad_min_vs_meses.png
    └── 5_ida_y_vuelta.png    <- generado por punto_flotante.py (B2)
```

## Cómo ejecutar

Todo se corre **desde la raíz del repositorio** (los paths a `data/` y
`graficos/` son relativos a ahí):

```bash
pip install -r requirements.txt
python3 src/errores.py          # A1, A2, A3, A5 (imprime resultados y genera graficos/1 a 4)
python3 src/anualidad.py        # A4
python3 src/punto_flotante.py   # B1, B2, B4 (genera graficos/ida_y_vuelta.png)
```

## Norma arbitraria adoptada (cifras significativas)

- **2 cifras significativas** para representar un precio individual (A1) y
  para las operaciones de compra/venta (A2, A5), siguiendo el ejemplo del
  enunciado (963.44 → 960).
- **3 cifras significativas** para comparar dos meses parecidos y restarlos
  (A3, A4 — `N_CIFRAS_RESTA` en `errores.py` y `N_CIFRAS` en `anualidad.py`), porque con
  solo 2 cifras casi cualquier resta entre meses vecinos queda completamente
  indeterminada. Esta es la norma que el enunciado pide establecer
  explícitamente frente al problema de cancelación.

Detalle completo del análisis, los números y la conclusión final en
[INFORME.md](INFORME.md).