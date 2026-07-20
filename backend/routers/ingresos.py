"""
routers/ingresos.py — CRUD de ingresos.
"""
from fastapi import APIRouter, HTTPException
from backend.database import get_conn
from backend.models import Ingreso, IngresoCreate

router = APIRouter(prefix="/ingresos", tags=["ingresos"])


def _row(r) -> dict:
    return dict(r)


@router.get("/", response_model=list[Ingreso])
def listar():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM ingresos ORDER BY fecha DESC, id DESC").fetchall()
    return [_row(r) for r in rows]


@router.post("/", response_model=Ingreso, status_code=201)
def crear(item: IngresoCreate):
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO ingresos (fecha, fuente, desc, monto) VALUES (?,?,?,?)",
            (item.fecha, item.fuente, item.desc, item.monto),
        )
        row = conn.execute("SELECT * FROM ingresos WHERE id=?", (cur.lastrowid,)).fetchone()
    return _row(row)


@router.put("/{id}", response_model=Ingreso)
def actualizar(id: int, item: IngresoCreate):
    with get_conn() as conn:
        conn.execute(
            "UPDATE ingresos SET fecha=?, fuente=?, desc=?, monto=? WHERE id=?",
            (item.fecha, item.fuente, item.desc, item.monto, id),
        )
        row = conn.execute("SELECT * FROM ingresos WHERE id=?", (id,)).fetchone()
    if not row:
        raise HTTPException(404, "Ingreso no encontrado")
    return _row(row)


@router.delete("/{id}", status_code=204)
def eliminar(id: int):
    with get_conn() as conn:
        conn.execute("DELETE FROM ingresos WHERE id=?", (id,))
