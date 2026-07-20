"""
routers/presupuesto.py — CRUD de presupuestos por categoria y metas de ahorro.
"""
from fastapi import APIRouter, HTTPException
from backend.database import get_conn
from backend.models import PresupuestoItem, Meta, MetaCreate

router = APIRouter(tags=["presupuesto"])


def _row(r) -> dict:
    return dict(r)

# ── Presupuestos ──────────────────────────────────────────────────────────────

pres = APIRouter(prefix="/presupuestos")


@pres.get("/", response_model=list[PresupuestoItem])
def listar_presupuestos():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM presupuestos ORDER BY cat").fetchall()
    return [_row(r) for r in rows]


@pres.put("/{cat}", response_model=PresupuestoItem)
def actualizar_presupuesto(cat: str, item: PresupuestoItem):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO presupuestos (cat, monto) VALUES (?,?) ON CONFLICT(cat) DO UPDATE SET monto=excluded.monto",
            (cat, item.monto),
        )
        row = conn.execute("SELECT * FROM presupuestos WHERE cat=?", (cat,)).fetchone()
    return _row(row)


# ── Metas ─────────────────────────────────────────────────────────────────────

metas = APIRouter(prefix="/metas")


@metas.get("/", response_model=list[Meta])
def listar_metas():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM metas ORDER BY id").fetchall()
    return [_row(r) for r in rows]


@metas.post("/", response_model=Meta, status_code=201)
def crear_meta(item: MetaCreate):
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO metas (nombre, desc, objetivo, ahorrado, fecha) VALUES (?,?,?,?,?)",
            (item.nombre, item.desc, item.objetivo, item.ahorrado, item.fecha),
        )
        row = conn.execute("SELECT * FROM metas WHERE id=?", (cur.lastrowid,)).fetchone()
    return _row(row)


@metas.put("/{id}", response_model=Meta)
def actualizar_meta(id: int, item: MetaCreate):
    with get_conn() as conn:
        conn.execute(
            "UPDATE metas SET nombre=?, desc=?, objetivo=?, ahorrado=?, fecha=? WHERE id=?",
            (item.nombre, item.desc, item.objetivo, item.ahorrado, item.fecha, id),
        )
        row = conn.execute("SELECT * FROM metas WHERE id=?", (id,)).fetchone()
    if not row:
        raise HTTPException(404, "Meta no encontrada")
    return _row(row)


@metas.delete("/{id}", status_code=204)
def eliminar_meta(id: int):
    with get_conn() as conn:
        conn.execute("DELETE FROM metas WHERE id=?", (id,))


router.include_router(pres)
router.include_router(metas)
