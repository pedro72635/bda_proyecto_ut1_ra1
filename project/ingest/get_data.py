import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

# Funcion para generar los datos

def generar_datos(num_days=30, rows_per_day=200):
    """Genera un DataFrame simulado con datos de ventas diarias."""
    base_dir = Path(__file__).resolve().parent.parent
    drops_dir = base_dir / "data" / "drops"
    today = datetime.now()

    # Bucle para crear diferentes días y sus datos
    for d in range(num_days):
        day = today - timedelta(days=d)
        folder = drops_dir / day.strftime("%Y-%m-%d")
        folder.mkdir(parents=True, exist_ok=True)

        # Creamos el dataframe con datos simulados
        df = pd.DataFrame({
            "fecha": [day.strftime("%Y-%m-%d")] * rows_per_day,
            "id_cliente": np.random.randint(1000, 2000, rows_per_day),
            "id_producto": np.random.randint(1, 50, rows_per_day),
            "unidades": np.random.randint(1, 10, rows_per_day),
            "precio_unitario": np.random.uniform(5.0, 150.0, rows_per_day).round(2)
            })
        
        # --- Introducir errores aleatorios ---
        errores = int(rows_per_day * 0.05)  # 5% de filas con errores

        # 1. Asignar algunos precios negativos
        idx_precios = np.random.choice(df.index, errores // 4, replace=False)
        df.loc[idx_precios, "precio_unitario"] = -np.abs(df.loc[idx_precios, "precio_unitario"])

        # 2. Unidades negativas o cero
        idx_unidades = np.random.choice(df.index, errores // 4, replace=False)
        df.loc[idx_unidades, "unidades"] = np.random.choice([-5, 0], len(idx_unidades))

        # 3. IDs fuera de rango
        idx_clientes = np.random.choice(df.index, errores // 4, replace=False)
        df.loc[idx_clientes, "id_cliente"] = np.random.choice([None, 99999, -1], len(idx_clientes))

        # 4. Valores nulos
        idx_nulos = np.random.choice(df.index, errores // 4, replace=False)
        for col in ["id_producto", "precio_unitario"]:
            df.loc[idx_nulos, col] = np.nan

        # Guardamos el DataFrame en un archivo CSV
        file_path = folder / "ventas.csv"
        df.to_csv(file_path, index=False)
        print(f"CSV generado en : {file_path}")
    print("Datos generados correctamente.")


if __name__ == "__main__":
    generar_datos()