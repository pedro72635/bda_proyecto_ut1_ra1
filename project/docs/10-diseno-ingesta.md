# 🧩 Diseño de Ingestión

## 📘 Resumen
El proceso de **ingestión** se encarga de incorporar diariamente los archivos CSV con datos de ventas desde la carpeta `project/data/drops/`.  
Cada ejecución del pipeline procesa los nuevos lotes de datos, aplicando controles de calidad, trazabilidad e idempotencia antes de almacenarlos en la base de datos y generar el reporte.

---

## 📂 Fuente
- **Origen:** `project/data/drops/YYYY-MM-DD/ventas.csv`
- **Formato:** CSV con cabecera (`fecha`, `id_cliente`, `id_producto`, `unidades`, `precio_unitario`)
- **Frecuencia:** diaria
- **Volumen típico:** entre 4 000 y 10 000 filas por lote

---

## ⚙️ Estrategia
- **Modo:** `batch` diario (se ejecuta manualmente)
- **Incremental:** por fecha de carpeta (`YYYY-MM-DD`)
- **Particionado:** por fecha de carga (`batch_id` = nombre de la carpeta)
- **Control de duplicados:** eliminación previa por `batch_id` antes de insertar
- **Persistencia:** en SQLite (`ventas_raw`) y Parquet (`ventas_clean.parquet`)

---

## 🔁 Idempotencia y deduplicación
- **`_batch_id`:** obtenido del nombre de la carpeta (`YYYY-MM-DD`)
- **`_ingest_ts`:** marca temporal ISO del momento de ingesta (`datetime.now().isoformat()`)
- **`_source_file`:** ruta absoluta del archivo CSV original
- **Clave natural:** (`fecha`, `id_cliente`, `id_producto`)
- **Política:** “último gana por `_ingest_ts`” → si existen duplicados con la misma clave natural, se conserva la versión más reciente.
- **Mecanismo:** antes de insertar, se ejecuta  
  ```python
  conn.execute("DELETE FROM ventas_raw WHERE _batch_id = ?", (batch_id,))
  ```
  asegurando **idempotencia total** (reprocesar un lote no duplica registros).

---

## 🧾 Checkpoints y trazabilidad
- **Campos de trazabilidad incluidos en todas las filas:**
  - `_ingest_ts` → fecha y hora de ingesta
  - `_source_file` → ruta del archivo original
  - `_batch_id` → identificador único del lote
- **Cuarentena (DLQ):**
 Los registros inválidos no se descartan:  
 se almacenan en la tabla **`ventas_quarantine`** con la causa del error y metadatos del lote.

---

## ⏰ SLA (Service Level Agreement)
- **Disponibilidad esperada:** los datos deben estar ingesados antes de las **03:00 UTC** del día siguiente.
- **Procesamiento:** completo en menos de 30 s con el volumen actual.
- **Alertas:** (no implementadas en esta versión, pero se recomienda registrar errores críticos en log o email de aviso).

---

## ⚠️ Riesgos / Antipatrones
- Procesar en modo `streaming` no es recomendable: los archivos son diarios y no eventuales.
- La falta de una clave natural afectaría la deduplicación. En este caso se define correctamente como `(fecha, id_cliente, id_producto)`.
- No usar `_batch_id` podría duplicar datos si se reejecuta el pipeline.
