# 📝 Lecciones aprendidas

## ✅ Qué salió bien
- 🟢 Ingesta automatizada y deduplicación robusta gracias a las claves naturales y campos de control en el pipeline (`ingest_data.py`, `transform_data.py`).
- 📊 Generación automática de reportes ejecutivos directos desde los datos (con `reporte_md.py`) que permiten visualizar KPIs, la evolución diaria, productos líderes y causas de cuarentena.
- 🛠️ Separación clara entre capas (raw, quarantine, clean/oro), facilitando trazabilidad, análisis y auditoría posterior de todos los procesos.

## 🔧 Qué mejorar
- 🚨 Profundizar en la validación de campos obligatorios de cliente desde la fuente, para reducir el porcentaje de registros en cuarentena.
- ⚡ Mejorar el SLA en el procesamiento de grandes lotes, analizando opciones de ejecución paralela o escalabilidad.
- 📣 Implementar alertas automáticas cuando el ratio de cuarentena supere el umbral definido (ejemplo: >5%) y registrar evidencia en los logs.

## 🚀 Siguientes pasos
- 📈 Generar dashboard interactivo con visualización de KPIs y calidad en tiempo real para el equipo de negocio.
- 🔍 Incorporar comparativas históricas y correlación con acciones comerciales (promociones, estacionalidad) en los reportes.
- 🧪 Añadir tests automáticos sobre lógica de validación, así como simulaciones de errores para fortalecer la robustez y prevención.

## 📎 Apéndice (evidencias)
- Capturas de pantalla del sistema de integración continua en `Actions` mostrando builds y ejecuciones exitosas.
- Fragmentos de logs donde se observan errores detectados y solucionados (por ejemplo, entradas en quarantine por id_cliente nulo, luego corregidas en ingesta y transformación).

---
