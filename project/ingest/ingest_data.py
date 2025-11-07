import pandas as pd
import sqlite3
from pathlib import Path
from datetime import datetime


def validar_datos(df):
    """Valida los datos del DataFrame y devuelve un DataFrame limpio."""
    condiciones = (
        df["unidades"].notnull() &
        (df["unidades"] > 0) &
        df["precio_unitario"].notnull() &
        (df["precio_unitario"] > 0) &
        df["id_cliente"].notnull() &
        (df["id_cliente"].astype(float) > 0) &
        (df["id_cliente"].astype(float) < 99999) &
        df["id_producto"].notnull() &
        (df["id_producto"].astype(float) > 0)
    )
    validos = df[condiciones].copy()
    invalidos = df[~condiciones].copy()

    # Explicación del motivo (para cuarentena)
    invalidos["causa_error"] = ""
    invalidos.loc[df["unidades"].isna() | (df["unidades"] <= 0), "causa_error"] += "Unidades inválidas; "
    invalidos.loc[df["precio_unitario"].isna() | (df["precio_unitario"] <= 0), "causa_error"] += "Precio inválido; "
    invalidos.loc[df["id_cliente"].isna() | (df["id_cliente"].astype(float) <= 0), "causa_error"] += "Cliente inválido; "
    invalidos.loc[df["id_producto"].isna() | (df["id_producto"].astype(float) <= 0), "causa_error"] += "Producto inválido; "

    return validos, invalidos


def ingest_data():
    base_dir = Path(__file__).resolve().parent.parent
    drops_dir = base_dir / "data" / "drops"
    quarantine_dir = base_dir / "data" / "quarantine"
    raw_db = base_dir / "data" / "database" / "ventas.db"

    quarantine_dir.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(raw_db)
    total_validos, total_invalidos = 0, 0

    for csv_file in drops_dir.glob("*/ventas.csv"):
        print(f"Ingestando archivo: {csv_file}")
        # batch_id único e idempotente
        batch_id = csv_file.parent.name  # YYYY-MM-DD como batch_id
        ingest_ts = datetime.now().isoformat()

        df = pd.read_csv(csv_file)

        df["_batch_id"] = batch_id
        df["_source_file"] = str(csv_file)
        df["_ingest_ts"] = ingest_ts
        
        validos, invalidos = validar_datos(df)
        total_validos += len(validos)
        total_invalidos += len(invalidos)

        # 🧩 Control de idempotencia: eliminar registros previos del mismo batch_id
        conn.execute("DELETE FROM ventas_raw WHERE _batch_id = ?", (batch_id,))

        # Guardar válidos en SQLite (capa RAW)
        validos.to_sql("ventas_raw", conn, if_exists="append", index=False)

        # Guardar inválidos en cuarentena
        if not invalidos.empty:
            quarantine_file = quarantine_dir / f"quarantine_{batch_id}.csv"
            invalidos.to_csv(quarantine_file, index=False)
            print(f"Datos en cuarentena guardados en: {quarantine_file}")
    
    conn.commit()
    conn.close()
    print(f"Ingesta completada. Total válidos: {total_validos}, Total inválidos: {total_invalidos}")


if __name__ == "__main__":
    ingest_data()
