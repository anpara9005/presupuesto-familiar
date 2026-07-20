"""
database.py — Conexion SQLite y creacion de tablas.
Unica fuente de verdad para la capa de datos.
"""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "presupuesto.db"

CATEGORIAS = [
    "Vivienda", "Alimentacion", "Transporte", "Salud", "Educacion",
    "Entretenimiento", "Ropa y accesorios", "Servicios (luz, agua, internet)",
    "Deudas / Prestamos", "Otros",
]


def get_conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db() -> None:
    """Crea las tablas si no existen."""
    with get_conn() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS ingresos (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha      TEXT,
                fuente     TEXT NOT NULL,
                desc       TEXT,
                monto      REAL NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS gastos (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha      TEXT,
                cat        TEXT NOT NULL,
                desc       TEXT,
                monto      REAL NOT NULL,
                metodo     TEXT DEFAULT 'Efectivo',
                created_at TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS presupuestos (
                cat   TEXT PRIMARY KEY,
                monto REAL NOT NULL DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS metas (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre     TEXT NOT NULL,
                desc       TEXT,
                objetivo   REAL NOT NULL,
                ahorrado   REAL DEFAULT 0,
                fecha      TEXT,
                created_at TEXT DEFAULT (datetime('now'))
            );
        """)
        # Seed categorias en presupuestos si no existen
        for cat in CATEGORIAS:
            conn.execute(
                "INSERT OR IGNORE INTO presupuestos (cat, monto) VALUES (?, 0)", (cat,)
            )
