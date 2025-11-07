import subprocess
from pathlib import Path

def run_step(description, command):
    """Ejecuta un paso del pipeline y muestra mensajes de estado"""
    print(f"\n {description}")
    print("-" * 60)
    try:
        subprocess.run(["python", command], check=True)
        print(f" {description} completado correctamente.\n")
    except subprocess.CalledProcessError as e:
        print(f" Error durante {description}: {e}\n")
        raise e

def main():
    steps = [
        ("Ingesta de datos (RAW + cuarentena)", "project/ingest/ingest_data.py"),
        ("Limpieza y creación del parquet (CLEAN)", "project/transform/transform_data.py"),
        ("Generación del reporte Markdown", "project/output/reporte_md.py"),
    ]

    for desc, script in steps:
        run_step(desc, script)

    print("=" * 60)
    print("Todos los pasos ejecutados con éxito.")
    print("=" * 60)

if __name__ == "__main__":
    main()
