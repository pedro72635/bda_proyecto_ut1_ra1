import pandas as pd
import sqlite3
from pathlib import Path
from datetime import datetime


def generar_reporte():
    """Genera un reporte Markdown completo con KPIs, calidad y tendencias"""
    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data" / "clean"
    db_path = base_dir / "data" / "database" / "ventas.db"
    output_dir = base_dir / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    parquet_path = data_dir / "ventas_clean.parquet"
    df = pd.read_parquet(parquet_path)

    # Conexión a SQLite para leer la tabla de cuarentena
    conn = sqlite3.connect(db_path)
    df_quarantine = pd.read_sql("SELECT * FROM ventas_quarantine", conn)
    conn.close()

    # --- Preprocesamiento ---
    df["fecha"] = pd.to_datetime(df["fecha"])
    df["importe"] = df["importe"].astype(float)

    # --- KPIs principales ---
    ingresos_totales = df["importe"].sum()
    transacciones = len(df)
    ticket_medio = ingresos_totales / transacciones if transacciones > 0 else 0
    top_producto = (
        df.groupby("id_producto")["importe"].sum().sort_values(ascending=False).head(1)
    )
    producto_lider = int(top_producto.index[0])
    ventas_lider = float(top_producto.values[0])

    # --- Calidad de datos ---
    registros_invalidos = len(df_quarantine)
    porcentaje_invalidos = (
        registros_invalidos / (transacciones + registros_invalidos) * 100
        if transacciones + registros_invalidos > 0
        else 0
    )

    errores_por_causa = (
        df_quarantine["motivo"].value_counts().reset_index()
        if not df_quarantine.empty
        else pd.DataFrame(columns=["index", "motivo"])
    )
    errores_por_causa.columns = ["Causa", "Registros"]

    # --- Ingresos por día (últimos 30 días) ---
    ingresos_diarios = (
        df.groupby("fecha")["importe"]
        .sum()
        .reset_index()
        .sort_values("fecha", ascending=False)
    )

    # --- Top 5 productos ---
    top_productos = (
        df.groupby("id_producto")["importe"]
        .sum()
        .reset_index()
        .sort_values("importe", ascending=False)
        .head(5)
    )

    # --- Generar reporte Markdown ---
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    reporte_path = output_dir / "reporte.md"

    with open(reporte_path, "w", encoding="utf-8") as f:
        f.write("# 📊 Reporte de Ventas - Retail Analytics\n\n")
        f.write(f"**Última actualización:** {now}\n\n")
        f.write("## 🧾 Contexto\n")
        f.write("- Fuente: `ventas_clean.parquet` + `ventas_quarantine` (SQLite)\n")
        f.write("- Periodo analizado: últimos 30 días\n")
        f.write("- Frecuencia de ingestión: diaria\n")
        f.write("- Los datos son generados dinámicamente durante la ejecución del pipeline.\n\n")

        f.write("## 🔑 Indicadores Clave (KPIs)\n")
        f.write("| KPI | Definición | Valor |\n")
        f.write("|------|-------------|--------|\n")
        f.write(f"| Ingresos Totales | Suma de `importe` en los últimos 30 días | €{ingresos_totales:,.2f} |\n")
        f.write(f"| Ticket Medio | Ingresos / Nº Transacciones | €{ticket_medio:,.2f} |\n")
        f.write(f"| Transacciones | Nº de registros válidos | {transacciones:,} |\n")
        f.write(f"| Producto Líder | ID con mayor ingreso | {producto_lider} (€{ventas_lider:,.2f}) |\n\n")

        f.write("## ⚙️ Calidad de Datos\n")
        f.write(f"- Total registros inválidos: {registros_invalidos}\n")
        f.write(f"- Porcentaje inválidos: {porcentaje_invalidos:.2f}%\n\n")

        if not errores_por_causa.empty:
            f.write("### Principales causas de error\n")
            f.write(errores_por_causa.to_markdown(index=False))
            f.write("\n\n")
        else:
            f.write("✅ No se detectaron registros inválidos durante la ingestión.\n\n")

        f.write("## 📅 Ingresos diarios (últimos 30 días)\n\n")
        f.write(ingresos_diarios.to_markdown(index=False))
        f.write("\n\n")

        f.write("## 🏆 Top 5 productos por ingresos\n\n")
        f.write(top_productos.to_markdown(index=False))
        f.write("\n\n")

        f.write("## 🧩 Conclusiones\n")
        f.write("- El pipeline procesó correctamente los datos generados del último mes.\n")
        f.write("- Se dispone de un control completo de trazabilidad y calidad de datos.\n")
        f.write("- Los registros inválidos son trazados en la tabla `ventas_quarantine` con su causa.\n")
        f.write("- El producto líder mantiene un volumen destacado de ingresos.\n")
        f.write("- Este pipeline puede ampliarse fácilmente con segmentación de clientes o categorías.\n")

    print(f"✅ Reporte generado correctamente en: {reporte_path}")


if __name__ == "__main__":
    generar_reporte()
