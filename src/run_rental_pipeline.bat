@echo off
set PYTHON=C:\Users\emman\AppData\Local\Python\bin\python.exe
set PROJECT=C:\Users\emman\OneDrive\Documents\ontario-rental-market-intelligence
set LOG=%PROJECT%\run_log.txt

cd /d "%PROJECT%"

echo [%date% %time%] Starting pipeline run >> "%LOG%"

echo Running rental_pipeline.py...
"%PYTHON%" "%PROJECT%\rental_pipeline.py"
if %errorlevel% neq 0 (
    echo [%date% %time%] ERROR: rental_pipeline.py failed >> "%LOG%"
    exit /b 1
)

echo Running update_rental_latest.py...
"%PYTHON%" "%PROJECT%\update_rental_latest.py"
if %errorlevel% neq 0 (
    echo [%date% %time%] ERROR: update_rental_latest.py failed >> "%LOG%"
    exit /b 1
)

echo [%date% %time%] Pipeline completed successfully >> "%LOG%"
echo Done.