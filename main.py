"""
main.py — Punto de entrada FastAPI.
Sirve el frontend estatico y monta todos los routers de la API.
"""
from pathlib import Path
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.database import init_db
from backend.routers.ingresos   import router as r_ingresos
from backend.routers.gastos     import router as r_gastos
from backend.routers.presupuesto import router as r_presupuesto
from backend.routers.excel      import router as r_excel

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    print("\n  Presupuesto Familiar v2.0")
    print("  Abre en tu navegador: http://localhost:8000\n")
    yield


app = FastAPI(title="Presupuesto Familiar API", version="2.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar routers bajo /api
app.include_router(r_ingresos,    prefix="/api")
app.include_router(r_gastos,      prefix="/api")
app.include_router(r_presupuesto, prefix="/api")
app.include_router(r_excel,       prefix="/api")

# Servir frontend
FRONTEND = Path(__file__).parent / "frontend"
app.mount("/static", StaticFiles(directory=FRONTEND), name="static")


@app.get("/")
def root():
    return FileResponse(FRONTEND / "index.html")


@app.get("/health")
def health():
    return {"status": "ok"}




if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
