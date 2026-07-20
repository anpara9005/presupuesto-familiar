"""
models.py — Modelos Pydantic para validacion de datos en la API.
"""
from pydantic import BaseModel, Field
from typing import Optional


class IngresoCreate(BaseModel):
    fecha:  Optional[str]   = None
    fuente: str
    desc:   Optional[str]   = None
    monto:  float           = Field(gt=0)


class Ingreso(IngresoCreate):
    id: int
    model_config = {"from_attributes": True}


class GastoCreate(BaseModel):
    fecha:  Optional[str]   = None
    cat:    str
    desc:   Optional[str]   = None
    monto:  float           = Field(gt=0)
    metodo: Optional[str]   = "Efectivo"


class Gasto(GastoCreate):
    id: int
    model_config = {"from_attributes": True}


class PresupuestoItem(BaseModel):
    cat:   str
    monto: float = Field(ge=0)


class MetaCreate(BaseModel):
    nombre:   str
    desc:     Optional[str]   = None
    objetivo: float           = Field(gt=0)
    ahorrado: Optional[float] = 0.0
    fecha:    Optional[str]   = None


class Meta(MetaCreate):
    id: int
    model_config = {"from_attributes": True}
