# 🧹 Reglas de limpieza y calidad

---

## 📝 Tipos y formatos

- **`fecha`**: string en formato ISO (`YYYY-MM-DD`). Se fuerza la conversión y formateo correcto tanto en ingestión como en cuarentena.
- **`id_cliente`**: entero en *RAW*, string en cuarentena. Se valida como entero positivo (>0 y <99999), excluyendo valores como `9999`, `-1` o `"None"`.
- **`id_producto`**: entero en *RAW*, string en cuarentena. Solo se admiten números positivos.
- **`unidades`**: entero ≥ 1.
- **`precio_unitario`**: decimal positivo, formato a 2 decimales (tipo Decimal para exactitud monetaria).
- **Meta**: `_batch_id`, `_source_file`, `_ingest_ts` → siempre string.

---

## 🚫 Nulos y cuarentena

- **Obligatorios**: `fecha`, `id_cliente`, `id_producto`, `unidades`, `precio_unitario`.
- Si falta alguno, la fila va a la tabla `ventas_quarantine` junto con la causa específica (`"Cliente inválido;"`, `"Producto inválido;"`, `"Unidades inválidas;"`, etc).
- Chequeo de nulos en todos los campos esenciales, usando `.notnull()` más reglas de validación personalizadas.

---

## 🎯 Rangos y dominios

- `unidades` > 0.
- `precio_unitario` > 0.
- `id_cliente` > 0 y < 99999, valores dummy o atípicos explícitamente filtrados.
- `id_producto` > 0.
- Errores frecuentes (nulos, fuera de rango, códigos ficción) van trazados a la tabla de cuarentena con motivo detallado por fila.

---

## 🧩 Dedupliación

- **Clave natural:** (`fecha`, `id_cliente`, `id_producto`).
- **Política:** “último gana” usando el campo `_ingest_ts` al transformar los datos finales a Parquet (`ventas_clean.parquet`).
- Antes de insertar un lote, se elimina todo lo previo con ese `_batch_id` para asegurar **idempotencia total**.

---

## ✂️ Estandarización de texto

- `.astype(str)` para los registros en cuarentena.
- Fechas y tipos convertidos explícitamente según el modelo limpio.
- Convenciones estrictas para strings en metadatos y para convertir errores en cuarentena.

---

## 🏷️ Trazabilidad

- **Campos:** `_batch_id`, `_source_file`, `_ingest_ts` incluidos en todos los registros.
- Cambios y errores quedan registrados junto con los metadatos en RAW y cuarentena.
- El campo `"motivo"` en cuarentena detalla la causa precisa del rechazo.

---

## 🔎 QA rápida y monitoreo

- Se imprime el conteo de filas válidas e inválidas al finalizar cada ingesta.
- La proporción y principales causas de errores se consulta directo en la tabla `ventas_quarantine`.
- Para análisis volumétrico y control de cobertura, `_batch_id` y `_source_file` permiten estadísticas y validaciones cruzadas por día/lote.

---

## ⚠️ Riesgos y buenas prácticas
- La política de “último gana” exige tener `_ingest_ts` correctamente seteado siempre.
- El modo streaming **no es recomendable** aquí, pues la fuente es diaria/batch.

