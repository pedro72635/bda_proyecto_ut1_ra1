---
title: "Definición de métricas y tablas oro"
owner: "equipo-alumno"
periodicidad: "diaria"
version: "1.0.0"
---

# 🏅 Modelo de negocio (capa oro)

## 📊 Tablas oro

- **clean_ventas** (archivo Parquet generado en `data/clean/ventas_clean.parquet`): granularidad **línea de venta**
- **ventas_diarias** (vista agregada): granularidad **día** (creada dinámicamente en reportes a partir de clean_ventas)

---

## 📈 Métricas (KPI)

- **Ingresos netos**: Suma de `unidades * precio_unitario` sobre `clean_ventas`
- **Ticket medio**: `Ingresos netos / número de registros (transacciones)` en clean_ventas
- **Top producto**: `id_producto` con mayor ingreso (`importe`) en el periodo seleccionado (últimos 30 días)

---

## 💡 Supuestos

- Todos los importes están en EUR constantes (“sin impuestos”)
- Dedupe aplicado en clean_ventas según la política “último gana” usando `_ingest_ts`
- Se excluyen registros inválidos vía quarantine

---

## 🛠️ Consultas base (SQL conceptual)
```sql
-- Ingresos por día
SELECT fecha, SUM(unidadesprecio_unitario) AS importe_total, COUNT() AS lineas
FROM clean_ventas
GROUP BY fecha;

-- Top productos en el periodo
SELECT id_producto, SUM(unidades*precio_unitario) AS importe
FROM clean_ventas
GROUP BY id_producto
ORDER BY importe DESC
LIMIT 5;
```

## 📄 Notas de implementación

- **clean_ventas** se modela y deduplica mediante el script `transform_data.py`, a partir de la tabla `ventas_raw`
- La deduplicación respeta la clave natural `(fecha, id_cliente, id_producto)` y se conserva el registro con el `_ingest_ts` más reciente
- Las métricas se calculan sobre los datos limpios sin incluir ningún registro cuarentenado
- El pipeline y los reportes son generados automáticamente cada día después de la ingesta y transformación

---
