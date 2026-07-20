# Presupuesto Familiar v2

App web para organizar el presupuesto mensual familiar.
Desarrollada con **FastAPI + SQLite + openpyxl** — corre 100% local en tu PC.

## Estructura del proyecto

```
presupuesto_familiar/
├── main.py               Servidor FastAPI
├── run.bat               Script para arrancar (Windows)
├── backend/
│   ├── database.py       Conexion SQLite
│   ├── models.py         Modelos Pydantic
│   └── routers/
│       ├── ingresos.py   API de ingresos
│       ├── gastos.py     API de gastos
│       ├── presupuesto.py API de presupuesto y metas
│       └── excel.py      Exportar / Importar Excel
├── frontend/
│   └── index.html        Interfaz web
└── data/                 (local, no incluido en git)
    └── presupuesto.db    Base de datos SQLite
```

## Como usar

### 1. Instalar dependencias (solo la primera vez)

```bash
uv venv
uv pip install fastapi uvicorn openpyxl python-multipart
```

### 2. Arrancar el servidor

Doble click en **`run.bat`** o desde terminal:

```bash
python main.py
```

### 3. Abrir en el navegador

```
http://localhost:8000
```

## Funcionalidades

- **Ingresos** — Registra salarios, freelance, rentas, etc.
- **Gastos** — Por categoria con metodo de pago
- **Presupuesto** — Define limites por categoria, ve el % usado
- **Metas de ahorro** — Vacaciones, auto, casa, etc.
- **Dashboard** — Resumen visual con grafico donut
- **Exportar a Excel** — Descarga .xlsx con 4 hojas (Ingresos, Gastos, Presupuesto, Metas)
- **Importar desde Excel** — Carga datos desde un .xlsx exportado

## Tecnologias

| Capa | Tecnologia |
|------|-----------|
| Backend | Python + FastAPI |
| Base de datos | SQLite (via sqlite3) |
| Excel | openpyxl |
| Frontend | HTML + CSS + JavaScript (vanilla) |
