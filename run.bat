@echo off
title Presupuesto Familiar - Servidor Local
echo.
echo  Iniciando Presupuesto Familiar v2...
echo  Abre tu navegador en: http://localhost:8000
echo.
cd /d "%~dp0"
.venv\Scripts\python.exe main.py
pause
