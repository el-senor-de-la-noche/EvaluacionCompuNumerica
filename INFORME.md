# INFORME — La ganancia que se evapora

Cancelación y propagación del error con el dólar observado del SII (2022–2025)

**Integrantes:** Elias Gonzalez, Daniel Navarrete

Todos los valores de este informe salen de ejecutar el código en `src/`
sobre `data/dolar_observado_sii_2022_2025.csv` (48 meses, Ene-2022 a Dic-2025).

---

## Norma arbitraria adoptada

- **2 cifras significativas** para representar cualquier precio individual
  (A1) y para las operaciones de compra/venta (A2, A5).
- **3 cifras significativas** para comparar dos meses parecidos (A3, A4),
  ya que con solo 2 cifras casi toda resta entre meses vecinos queda
  completamente indeterminada.

---

## A1. Error de representación mes a mes

*(`src/errores.py`, función `a1_error_representacion`)*

Redondeando los 48 precios a 2 cifras significativas, el mes con **mayor
error relativo** corresponde a **Abril 2022**: 815.12 → 820 (Ea = 4.88, Er = 0.599 %).

Para el error relativo de redondear a 2 cifras se mueve entre ~0.02 % y ~0.6 %
para todo el período: como todos los precios están en el rango de los
cientos, la mantisa de 2 cifras siempre deja fuera "decenas" o "unidades"
de un número de tamaño similar (gráfico `3_error_representacion.png`).

## A2. Evaluación entre dos puntos (compra-venta)

*(`src/errores.py`, función `compra_venta`)*

Ejemplo: comprar en **Mayo 2023** (798.64) y vender en **Enero 2025**
(1000.76), con M = 1.000.000 CLP:

- USD comprados = 1.000.000 / 800 (precio de compra redondeado)
- Pesos finales = USD × 1000 (precio de venta redondeado)
- **Ganancia = 250.000 ± 3.078 CLP (Er = 1.23 %)**

El error es chico frente a la ganancia (1.2 % del resultado), así que la
operación es claramente rentable incluso considerando el redondeo.

## A3. Cancelación (Dic-2022 vs Dic-2023)

*(`src/errores.py`, función `a3_cancelacion`)*

Con 3 cifras significativas: 875.66 → 876, 874.67 → 875.

**ΔP = 875 − 876 = −1.00 ± 0.67 CLP (Er = 67.0 %)**

El error relativo es enorme (67 %) porque la resta involucra dos números
casi idénticos: el tamaño del resultado (−1.00) es del mismo orden que su
propio margen de error (0.67). El signo negativo "sobrevive" por poco
(1.00 > 0.67), pero con un error tan grande en proporción al resultado, no
es una conclusión sólida: es el caso límite exacto de cancelación que
describe el enunciado.

## A4. Anualidad (variación enero → diciembre)

*(`src/anualidad.py`, función `variacion_anual`)*

| Año  | Enero    | Diciembre | ΔP     | Ea   | Er (%) |
|------|----------|-----------|--------|------|--------|
| 2024 | 907.99   | 982.30    | +74.00 | 0.31 | 0.42   |
| 2022 | 822.05   | 875.66    | +54.00 | 0.39 | 0.72   |
| 2025 | 1000.76  | 916.16    | −84.00 | 0.92 | 1.10   |
| 2023 | 826.34   | 874.67    | +49.00 | 0.67 | 1.37   |

Ordenados del **más confiable** (2024) al **menos confiable** (2023). Lo que
tienen en común los años menos confiables no es un error absoluto más
grande (de hecho es parecido en los 4 años), sino que su ΔP es más **chico
en magnitud** — 2022 y 2023 tienen las variaciones anuales más pequeñas (54
y 49 CLP), así que el mismo error absoluto pesa proporcionalmente más. Los 4
años siguen siendo confiables en términos absolutos (la variación siempre es
mucho mayor que el error), pero el ranking muestra la tendencia hacia el
terreno peligroso de A3 a medida que el movimiento anual se achica.

## A5. Mejor compra y mejor venta

*(`src/errores.py`, función `a5_mejor_compra_venta`)*

- **Mínimo del período:** Febrero 2023, 798.26 CLP/USD.
- **Máximo del período:** Enero 2025, 1000.76 CLP/USD.

**Rentabilidad = 25.00 % ± 1.47 % de error relativo** (Ganancia = 250.000 ±
3.674 CLP).

¿Sobrevive al error? **Sí, con claridad.** El margen de error (1.47 % del
25 %) es mucho menor que la rentabilidad misma. Además, ambos extremos son
robustos frente a sus vecinos: Febrero-2023 (798.26) está 28.08 CLP por
debajo de Enero-2023 (826.34) y 11.24 CLP por debajo de Marzo-2023 (809.50);
Enero-2025 (1000.76) está 18.46 CLP por encima de Diciembre-2024 (982.30) y
44.14 CLP por encima de Febrero-2025 (956.62). Todas esas diferencias son
mucho mayores que el error de redondeo, así que el mínimo y el máximo no son
un accidente del redondeo: son extremos reales.

**Hallazgo adicional (gráfico `4_rentabilidad_min_vs_meses.png`):** al
simular la venta mes a mes desde el mínimo, tres meses cercanos (Abr, May y
Jun de 2023) dan una rentabilidad de **exactamente 0 %**. No es que el dólar
no se haya movido: pasa que esos precios (803.84, 798.64, 799.87) redondean
con 2 cifras significativas al **mismo valor** que el mínimo (800), así que
la "ganancia" simulada se anula y el error relativo queda matemáticamente
indefinido (división por cero). Es el mismo problema de cancelación de A3,
pero aplicado a montos: con solo 2 cifras significativas, meses realmente
distintos se vuelven indistinguibles entre sí.

---

## B1. Cifras significativas = mantisa corta

*(`src/punto_flotante.py`, función `demo_b1`)*

Guardar un precio con solo 2 o 3 cifras significativas es lo mismo que hace
un computador cuando reserva un número fijo de bits para la mantisa en punto
flotante: se descartan los dígitos que sobran, y esos dígitos descartados
son el error de representación.

Ejemplo con **1000.76** a 3 cifras significativas:
1000.76 → 1.00×10³ = **1000** → **Ea = 0.76**, Er = 0.076 %.

## B2. La ida y vuelta que no vuelve

*(`src/punto_flotante.py`, función `ida_y_vuelta`, gráfico `ida_y_vuelta.png`)*

Se convirtió M = 1.000.000 CLP a USD con el precio **real** de cada mes (sin
redondear), y se volvió a convertir a CLP con el mismo precio. La diferencia
contra el monto original resultó estar siempre entre **0 y ±1.16×10⁻¹⁰
CLP** en los 48 meses — prácticamente cero, del orden del épsilon de máquina
de `float64`.

Esto confirma que dividir y multiplicar por **el mismo número** se cancela
casi a la perfección incluso en la máquina: la deriva que se ve en el
gráfico no viene del redondeo a cifras significativas (aquí no se usó
ninguno), sino del límite de precisión binaria de `float64`. Es distinto al
error de A2: ahí el error aparece porque el precio de compra y el de venta
son **distintos**, cada uno con su propio error de redondeo, y esos errores
se van sumando.

## B4. Cancelación en la máquina (float32 vs float64)

*(`src/punto_flotante.py`, función `demo_b4`)*

Para 875.66 − 874.67 (valor exacto = 0.99):

| Precisión | Resultado    | Error frente al exacto |
|-----------|--------------|--------------------------|
| float32   | 0.98999023   | ≈ 9.77 × 10⁻⁶            |
| float64   | 0.9900000000000091 | ≈ 9.1 × 10⁻¹⁵      |

`float32` pierde casi 6 órdenes de magnitud de precisión frente a `float64`
en esta resta. Esto conecta con A3: incluso con la máquina de mayor
precisión disponible (float64), el error de fondo en A3 no viene del
computador, sino de que nosotros redondeamos los precios a 3 cifras
significativas antes de restar. `float32` solo demuestra que, si además se
usa una precisión de máquina baja, el problema de cancelación se agrava
todavía más.

---

## Conclusión final

**1. ¿Cuándo conviene comprar?**
El dólar estuvo más barato en **Febrero 2023** (798.26 CLP). Es un mínimo
confiable: está entre 11 y 28 CLP por debajo de los meses vecinos, una
diferencia muy superior al error de redondeo de unos pocos pesos.

**2. ¿Cuándo conviene vender?**
El dólar estuvo más caro en **Enero 2025** (1000.76 CLP). También es un
máximo confiable: está entre 18 y 44 CLP por encima de los meses vecinos.

**3. La mejor jugada completa.**
Comprar en Febrero 2023 y vender en Enero 2025 rinde una **rentabilidad de
25.00 % ± 1.47 %** sobre 1.000.000 CLP (ganancia de 250.000 ± 3.674 CLP). Es
una recomendación **sólida**: el error es pequeño frente al resultado.

**4. Tramos donde NO se puede recomendar nada.**
El caso más claro es **Diciembre 2022 → Diciembre 2023**: ΔP = −1.00 ± 0.67
CLP, con un error relativo de 67 %. Otro caso llamativo son los meses
Abril–Junio de 2023 frente al mínimo (Febrero 2023): al redondear a 2
cifras, todos esos precios colapsan al mismo valor (800) y la "ganancia" se
anula por completo, quedando el error relativo indefinido. En ambos casos,
afirmar algo con confianza sería irresponsable: el ruido del redondeo es
del mismo tamaño (o mayor) que la señal.

**5. La lección de método.**
Cuando una "diferencia" sale de restar dos números grandes y parecidos, el
resultado se achica pero el error absoluto no — así que hay que mirar
siempre el error relativo del resultado (no el de los datos originales)
antes de confiar en una diferencia pequeña.
