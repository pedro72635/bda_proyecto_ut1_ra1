import pandas as pd
import sqlite3
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP, getcontext

getcontext().prec = 10


def transformar_datos():
    """"Limpia y modela los datos de ventas_raw a ventas_clean.parquet"""""
    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"
    clean_dir = data_dir / "clean"
    clean_dir.mkdir(parents=True, exist_ok=True)
    
    # Conectar a la base de datos SQLite y leer la tabla ventas_raw
    db_path = data_dir / "database" / "ventas.db" 
    conn = sqlite3.connect(db_path)

    # Leer datos de la tabla ventas_raw en un DataFrame 
    df = pd.read_sql("SELECT * FROM ventas_raw", conn)
    conn.close()

    # Aplicamos el tipado de datos
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    df["id_cliente"] = df["id_cliente"].astype(int)
    df["id_producto"] = df["id_producto"].astype(int)
    df["unidades"] = df["unidades"].astype(int)

    df["precio_unitario"] = df["precio_unitario"].apply(
        lambda x: Decimal(str(x)).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )
    )

    df["importe"] = df.apply(
        lambda r: (r["precio_unitario"] * Decimal(r["unidades"])).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
        axis=1
    )

    df.sort_values(
        by=[
            "fecha",
            "id_cliente",
            "id_producto",
            "_ingest_ts",
        ],
        inplace=True
    )
    df = df.drop_duplicates(
        subset=["fecha", "id_cliente", "id_producto"],
        keep="last"
    )

    parquet_path = clean_dir / "ventas_clean.parquet"
    # Convertimos las columnas Decimal a str para guardarlas en Parquet, ya que Parquet no soporta Decimal de Pandas
    df["precio_unitario"] = df["precio_unitario"].astype(str)
    df["importe"] = df["importe"].astype(str)
    df.to_parquet(parquet_path, index=False)

    print(f"Datos limpios guardados en: {parquet_path}")
    print(f"Filas finales: {len(df)}")


if __name__ == "__main__":
    transformar_datos()
