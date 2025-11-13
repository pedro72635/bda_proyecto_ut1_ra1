# 🧩 BDA_Proyecto_UT1_RA1 · Pipeline de Ingesta, Limpieza y Reporte

Este repositorio implementa un **pipeline ETL completo** (Extract → Transform → Load → Report) que permite:
- Ingestar datos desde múltiples archivos CSV.
- Limpiar y validar registros.
- Almacenar los datos en una base SQLite local.
- Generar un **reporte automático en formato Markdown** con KPIs de negocio.

---

## 📁 Estructura principal del proyecto

```
project/
├── sql/
│   ├── init_db.py          # Inicializa la base de datos SQLite
├── ingest/
│   ├── get_data.py         # Descarga/genera datos de ejemplo
│   ├── ingest_data.py      # Ingesta CSVs → capa RAW
│   ├── run.py              # Pipeline completo
├── transform/
│   ├── transform_data.py   # Limpieza y generación del parquet (capa CLEAN)
├── output/
│   └── report_md.py        # Genera el reporte Markdown final
├── data/
│   ├── raw/                # Datos sin procesar (ingesta)
│   ├── clean/              # Datos limpios (parquet)
│   └── quarantine/         # Registros inválidos
└── requirements.txt
```

---

## ⚙️ Requisitos

- Python **3.10 o superior**
- Paquetes indicados en `requirements.txt`

Instalación rápida:

```bash
python -m venv .venv
.venv\Scripts\activate   # (en Windows)
# o: source .venv/bin/activate   (en Linux/Mac)

pip install -r project/requirements.txt
```

---

## 🚀 Ejecución paso a paso

1️⃣ **Inicializar la base de datos**
```bash
python project/ingest/init_db.py
```
Crea la base `ventas.db` y las tablas necesarias en la capa **RAW**.

---

2️⃣ **Generar datos de ejemplo**
```bash
python project/ingest/get_data.py
```
Descarga o genera los archivos CSV dentro de `project/data/drops/`.

---

3️⃣ **Ejecutar el pipeline completo**
```bash
python project/ingest/run.py
```
Ejecuta automáticamente las siguientes etapas:
- Ingesta (`ingest_data.py`)
- Limpieza (`transform_data.py`)
- Reporte (`report_md.py`)

El proceso muestra mensajes como:
```
Ingesta completada correctamente.
Limpieza y creación del parquet (CLEAN) completado correctamente.
Reporte generado correctamente en: project/output/reporte.md
```

---

## 📊 Salida generada

| Archivo | Descripción |
|----------|--------------|
| `project/data/clean/ventas_clean.parquet` | Datos limpios y validados |
| `project/output/reporte.md` | Reporte final con KPIs y tablas resumen |
| `project/data/quarantine/*.csv` | Registros rechazados por validación |

---

## 🔁 Idempotencia y control de lotes

Cada ejecución procesa los archivos según su **batch_id (YYYY-MM-DD)**.  
Si se vuelve a ejecutar el pipeline sobre el mismo lote, los registros previos se eliminan antes de insertar los nuevos:

```python
conn.execute("DELETE FROM ventas_raw WHERE _batch_id = ?", (batch_id,))
```

Esto asegura que el proceso sea **idempotente y reproducible**.

---

## 📈 KPIs incluidos en el reporte

El archivo `report_md.py` calcula y muestra automáticamente:
- **Ingresos totales**
- **Número de transacciones**
- **Ticket medio**
- **Producto líder por ventas**
- **Top 5 productos por ingresos**
- **Ingresos diarios (últimos 30 días)**

---

## 🧾 Ejemplo de ejecución

```
> python project/ingest/run.py

------------------------------------------------------------
 Ingestando archivo: project/data/raw/2025-11-06/ventas.csv
------------------------------------------------------------
Filas válidas: 5753 | Filas inválidas: 12

 Limpieza y creación del parquet (CLEAN)
------------------------------------------------------------
Datos limpios guardados en: project/data/clean/ventas_clean.parquet
Filas finales: 5753

 Generación del reporte Markdown
------------------------------------------------------------
Reporte generado correctamente en: project/output/reporte.md
```

---

## 📂 Resultados esperados

```
project/
└── output/
    └── reporte.md
```

Ejemplo de salida en `reporte.md`:

```markdown
# 📊 Reporte de Ventas Diarias - Retail Mini

**Última actualización:** 2025-11-07 12:45:32

## 🔑 KPIs
- Ingresos totales: €256,304.50
- Ticket medio: €44.57
- Transacciones: 5,753
- Producto líder: ID 105 (€8,234.00)
```

---

