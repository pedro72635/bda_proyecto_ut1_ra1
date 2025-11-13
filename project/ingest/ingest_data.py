import pandas as pd
import sqlite3
from pathlib import Path
from datetime import datetime


def validar_datos(df):
    """Valida los datos del DataFrame y devuelve un DataFrame limpio."""

    invalidos_id_cliente = (
        (df["id_cliente"].astype(str).str.strip().isin(["9999", "-1", "None"])) |  # Valores explícitos no válidos
        (df["id_cliente"].astype(float) <= 0) |  
        (df["id_cliente"].astype(float) >= 99999)  
    )
    
    condiciones = (
        df["unidades"].notnull() & 
        (df["unidades"] > 0) & 
        df["precio_unitario"].notnull() & 
        (df["precio_unitario"] > 0) & 
        df["id_cliente"].notnull() & 
        ~invalidos_id_cliente &  
        df["id_producto"].notnull() & 
        (df["id_producto"].astype(float) > 0)
    )
    
    validos = df[condiciones].copy()
    invalidos = df[~condiciones].copy()

    # Explicación del motivo (para cuarentena)
    invalidos["causa_error"] = ""
    
    # Añadir causa para los invalidos de id_cliente
    invalidos.loc[invalidos_id_cliente, "causa_error"] += "Cliente inválido; "

    invalidos.loc[df["unidades"].isna() | (df["unidades"] <= 0), "causa_error"] += "Unidades inválidas; "
    invalidos.loc[df["precio_unitario"].isna() | (df["precio_unitario"] <= 0), "causa_error"] += "Precio inválido; "
    invalidos.loc[df["id_producto"].isna() | (df["id_producto"].astype(float) <= 0), "causa_error"] += "Producto inválido; "

    return validos, invalidos


def ingest_data():
    base_dir = Path(__file__).resolve().parent.parent
    drops_dir = base_dir / "data" / "drops"
    raw_db = base_dir / "data" / "database" / "ventas.db"

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

        # Borrar casos anterioers
        conn.execute("DELETE FROM ventas_raw WHERE _batch_id = ?", (batch_id,))
        conn.execute("DELETE FROM ventas_quarantine WHERE _batch_id = ?", (batch_id,))

        # Guardar válidos en SQLite (capa RAW)
        validos.to_sql("ventas_raw", conn, if_exists="append", index=False)

        # Guardar inválidos en la tabla de cuarentena (ventas_quarantine)
        if not invalidos.empty:
            invalidos["fecha"] = pd.to_datetime(invalidos["fecha"], errors='coerce').dt.strftime('%Y-%m-%d')  # Asegurar que la fecha esté en formato correcto
            invalidos["id_cliente"] = invalidos["id_cliente"].astype(str)  
            invalidos["id_producto"] = invalidos["id_producto"].astype(str)  
            invalidos["unidades"] = invalidos["unidades"].astype(str)  
            invalidos["precio_unitario"] = invalidos["precio_unitario"].astype(str) 

            # Insertar en la tabla de cuarentena
            for _, row in invalidos.iterrows():
                conn.execute("""
                    INSERT INTO ventas_quarantine (fecha, id_cliente, id_producto, unidades, precio_unitario, motivo, _batch_id, _source_file, _ingest_ts)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    row["fecha"],
                    row["id_cliente"],
                    row["id_producto"],
                    row["unidades"],
                    row["precio_unitario"],
                    row["causa_error"],
                    batch_id,
                    str(csv_file),
                    ingest_ts
                ))
            print(f"Datos en cuarentena insertados para el batch {batch_id}.")
    
    conn.commit()
    conn.close()
    print(f"Ingesta completada. Total válidos: {total_validos}, Total invalidos: {total_invalidos}")


if __name__ == "__main__":
    ingest_data()
