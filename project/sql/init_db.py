import sqlite3
from pathlib import Path


def init_database():
    # Rutas base
    base_dir = Path(__file__).resolve().parent.parent
    sql_path = base_dir / "sql" / "create_tables.sql"
    db_dir = base_dir / "data" / "database"
    db_dir.mkdir(parents=True, exist_ok=True)
    db_path = db_dir / "ventas.db"

    # Leer el archivo SQL
    with open(sql_path, "r", encoding="utf-8") as f:
        sql_script = f.read()

    # Crear la base de datos y ejecutar el SQL
    with sqlite3.connect(db_path) as conn:
        conn.executescript(sql_script)
        conn.commit()

    print(f"✅ Base de datos inicializada en: {db_path}")


if __name__ == "__main__":
    init_database()
