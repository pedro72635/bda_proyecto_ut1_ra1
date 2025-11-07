CREATE TABLE IF NOT EXISTS ventas_raw (
    fecha TEXT,
    id_cliente INTEGER,
    id_producto INTEGER,
    unidades INTEGER,
    precio_unitario REAL,
    _batch_id TEXT,
    _source_file TEXT,
    _ingest_ts TEXT
);

CREATE TABLE IF NOT EXISTS ventas_quarantine (
    fecha TEXT,
    id_cliente TEXT,
    id_producto TEXT,
    unidades TEXT,
    precio_unitario TEXT,
    motivo TEXT,
    _batch_id TEXT,
    _source_file TEXT,
    _ingest_ts TEXT
);