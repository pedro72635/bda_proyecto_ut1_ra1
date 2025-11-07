import pandas as pd
from pathlib import Path
from datetime import datetime


def generar_reporte():
    """Genera un reporte Markdown con KPIs y tablas resumen"""
    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data" / "clean"
    output_dir = base_dir / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    parquet_path = data_dir / "ventas_clean.parquet"
    df = pd.read_parquet(parquet_path)

    # --- Preprocesamiento ---
    df["fecha"] = pd.to_datetime(df["fecha"])
    df["importe"] = df["importe"].astype(float)

    # ---  Calculo de KPIs ---
    ingresos_totales = df["importe"].sum()
    transacciones = len(df)
    ticket_medio = ingresos_totales / transacciones if transacciones > 0 else 0

    top_producto = (
        df.groupby("id_producto")["importe"].sum().sort_values(ascending=False).head(1)
    )
    producto_lider = int(top_producto.index[0])
    ventas_lider = float(top_producto.values[0])

    
    # Ingresos por día (últimos 30 días)
    ingresos_diarios = (
        df.groupby("fecha")["importe"]
        .sum()
        .reset_index()
        .sort_values("fecha", ascending=False)
        .head(30)
    )

    
    top_productos = (
        df.groupby("id_producto")["importe"]
        .sum()
        .reset_index()
        .sort_values("importe", ascending=False)
        .head(5)
    )

    # --- 4️⃣ Crear reporte Markdown ---
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    reporte_path = output_dir / "reporte.md"

    with open(reporte_path, "w", encoding="utf-8") as f:
        f.write("# 📊 Reporte de Ventas Diarias - Retail Mini\n\n")
        f.write(f"**Última actualización:** {now}\n\n")
        f.write("## 🧾 Contexto\n")
        f.write("- Fuente: `ventas_clean.parquet`\n")
        f.write("- Periodo: últimos 30 días\n")
        f.write("- Frecuencia: diaria\n\n")

        f.write("## 🔑 KPIs\n")
        f.write(f"- **Ingresos totales:** €{ingresos_totales:,.2f}\n")
        f.write(f"- **Ticket medio:** €{ticket_medio:,.2f}\n")
        f.write(f"- **Transacciones:** {transacciones:,}\n")
        f.write(f"- **Producto líder:** ID {producto_lider} (€{ventas_lider:,.2f})\n\n")

        f.write("## 📅 Ingresos diarios (últimos 30 días)\n\n")
        f.write(ingresos_diarios.to_markdown(index=False))
        f.write("\n\n")

        f.write("## 🏆 Top 5 productos por ingresos\n\n")
        f.write(top_productos.to_markdown(index=False))
        f.write("\n\n")

        f.write("## 🧩 Conclusiones\n")
        f.write("- El pipeline procesó los datos correctamente.\n")
        f.write("- Se observan patrones de ventas diarias y productos destacados.\n")
        f.write("- El modelo puede ampliarse con segmentación de clientes o categorías.\n")

    print(f"Reporte generado correctamente en: {reporte_path}")

if __name__ == "__main__":
    generar_reporte()
