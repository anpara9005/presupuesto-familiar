"""
routers/gastos.py — CRUD de gastos.
"""
from fastapi import APIRouter, HTTPException
from backend.database import get_conn
from backend.models import Gasto, GastoCreate

router = APIRouter(prefix="/gastos", tags=["gastos"])


def _row(r) -> dict:
    return dict(r)


@router.get("/", response_model=list[Gasto])
def listar():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM gastos ORDER BY fecha DESC, id DESC").fetchall()
    return [_row(r) for r in rows]


@router.post("/", response_model=Gasto, status_code=201)
def crear(item: GastoCreate):
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO gastos (fecha, cat, desc, monto, metodo) VALUES (?,?,?,?,?)",
            (item.fecha, item.cat, item.desc, item.monto, item.metodo),
        )
        row = conn.execute("SELECT * FROM gastos WHERE id=?", (cur.lastrowid,)).fetchone()
    return _row(row)


@router.put("/{id}", response_model=Gasto)
def actualizar(id: int, item: GastoCreate):
    with get_conn() as conn:
        conn.execute(
            "UPDATE gastos SET fecha=?, cat=?, desc=?, monto=?, metodo=? WHERE id=?",
            (item.fecha, item.cat, item.desc, item.monto, item.metodo, id),
        )
        row = conn.execute("SELECT * FROM gastos WHERE id=?", (id,)).fetchone()
    if not row:
        raise HTTPException(404, "Gasto no encontrado")
    return _row(row)


@router.delete("/{id}", status_code=204)
def eliminar(id: int):
    with get_conn() as conn:
        conn.execute("DELETE FROM gastos WHERE id=?", (id,))
