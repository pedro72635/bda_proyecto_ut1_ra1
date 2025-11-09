# 📊 Reporte de Ventas - Retail Analytics

**Última actualización:** 2025-11-09 16:42:34

## 🧾 Contexto
- Fuente: `ventas_clean.parquet` + `ventas_quarantine` (SQLite)
- Periodo analizado: últimos 30 días
- Frecuencia de ingestión: diaria
- Los datos son generados dinámicamente durante la ejecución del pipeline.

## 🔑 Indicadores Clave (KPIs)
| KPI | Definición | Valor |
|------|-------------|--------|
| Ingresos Totales | Suma de `importe` en los últimos 30 días | €2,182,002.26 |
| Ticket Medio | Ingresos / Nº Transacciones | €379.21 |
| Transacciones | Nº de registros válidos | 5,754 |
| Producto Líder | ID con mayor ingreso | 15 (€59,673.65) |

## ⚙️ Calidad de Datos
- Total registros inválidos: 238
- Porcentaje inválidos: 3.97%

### Principales causas de error
| Causa                                                   |   Registros |
|:--------------------------------------------------------|------------:|
| Precio inválido;                                        |          60 |
| Unidades inválidas;                                     |          59 |
| Precio inválido; Producto inválido;                     |          58 |
| Cliente inválido;                                       |          36 |
|                                                         |          23 |
| Unidades inválidas; Precio inválido; Producto inválido; |           1 |
| Cliente inválido; Precio inválido; Producto inválido;   |           1 |

## 📅 Ingresos diarios (últimos 30 días)

| fecha               |   importe |
|:--------------------|----------:|
| 2025-11-09 00:00:00 |   72310.3 |
| 2025-11-08 00:00:00 |   77086.1 |
| 2025-11-07 00:00:00 |   71653.7 |
| 2025-11-06 00:00:00 |   74728.9 |
| 2025-11-05 00:00:00 |   72961.2 |
| 2025-11-04 00:00:00 |   79051.5 |
| 2025-11-03 00:00:00 |   71698.1 |
| 2025-11-02 00:00:00 |   67262.8 |
| 2025-11-01 00:00:00 |   69804.9 |
| 2025-10-31 00:00:00 |   66774.7 |
| 2025-10-30 00:00:00 |   75527.5 |
| 2025-10-29 00:00:00 |   72527.9 |
| 2025-10-28 00:00:00 |   73969.1 |
| 2025-10-27 00:00:00 |   80788.1 |
| 2025-10-26 00:00:00 |   72828.9 |
| 2025-10-25 00:00:00 |   73730.4 |
| 2025-10-24 00:00:00 |   74261.2 |
| 2025-10-23 00:00:00 |   69908.9 |
| 2025-10-22 00:00:00 |   69882.8 |
| 2025-10-21 00:00:00 |   69197.7 |
| 2025-10-20 00:00:00 |   70000.8 |
| 2025-10-19 00:00:00 |   78053.8 |
| 2025-10-18 00:00:00 |   69629.6 |
| 2025-10-17 00:00:00 |   69039.3 |
| 2025-10-16 00:00:00 |   66544.3 |
| 2025-10-15 00:00:00 |   71971   |
| 2025-10-14 00:00:00 |   73794.1 |
| 2025-10-13 00:00:00 |   77769.8 |
| 2025-10-12 00:00:00 |   73033   |
| 2025-10-11 00:00:00 |   76211.9 |

## 🏆 Top 5 productos por ingresos

|   id_producto |   importe |
|--------------:|----------:|
|            15 |   59673.7 |
|            34 |   53304.5 |
|            37 |   53231.3 |
|            32 |   53168.6 |
|             5 |   52093.4 |

## 🧩 Conclusiones
- El pipeline procesó correctamente los datos generados del último mes.
- Se dispone de un control completo de trazabilidad y calidad de datos.
- Los registros inválidos son trazados en la tabla `ventas_quarantine` con su causa.
- El producto líder mantiene un volumen destacado de ingresos.
