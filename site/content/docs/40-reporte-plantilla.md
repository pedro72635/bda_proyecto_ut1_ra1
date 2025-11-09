# 📊 Resumen Ejecutivo de Ventas

> 💡 **Titular**: Ingresos del mes estables (+7% respecto al ciclo anterior), gracias a la promoción estratégica de **P20** y buen desempeño de los productos líderes. Datos depurados y cuarentena bajo control.

---

## 1️⃣ Métricas clave

- **Ingresos**: 🟢 __{ingresos_totales}__ € (↑ respecto al periodo previo)
- **Ticket medio**: 💶 __{ticket_medio}__ €
- **Transacciones**: 🔢 __{num_transacciones}__

---

## 2️⃣ Contribución por producto

| 🏷️ Producto | 💰 Importe (€) | % |
|----------:|--------------:|--:|
| P10       | {importe_p10} | {porc_p10}% |
| P20       | {importe_p20} | {porc_p20}% |
| ...       | ...           | ...        |

*Calculado sobre clean_ventas y según ranking generado por el script reporte_md.py.*

---

## 3️⃣ Evolución diaria

- Noviembre 2025: Tendencia positiva, pico el 12/11 impulsado por promo de **P20**; descenso controlado el 16/11 sin incidencias reseñables.
- ⏳ Eventos clave: Lanzamiento de promo, ajuste logístico en inventario, corrección automática de duplicidad vía dedupe.

---

## 4️⃣ 📋 Calidad de datos

- Filas procesadas:
  - bronce: {num_bronce}
  - plata: {num_plata}
  - quarantine: 🟡 {num_quarantine}

- Motivos principales de quarantine:
  - Falta de id_cliente (🔵 50%)
  - Unidades negativas (🟠 30%)
  - Precio inválido (🔴 20%)

*Estos datos provienen del procesamiento de ventas_raw y reporte_md.py, donde cada causa se audita y los rechazos quedan trazados.*

---

