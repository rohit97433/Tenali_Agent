@echo off
:: ============================================================
:: TENALI v1 - SHELL TOOL INSTRUCTIONS
:: ============================================================
:: HOW TO USE THIS AS A GLOBAL COMMAND:
:: 1. Copy the path to this folder (e.g., C:\Projects\Tenali)
:: 2. Search for 'Edit the system environment variables' in Windows
:: 3. Click 'Environment Variables' -> 'Path' -> 'Edit' -> 'New'
:: 4. Paste the folder path and save.
:: 5. Now you can type 'tenali' in any terminal to wake the agent!
:: ============================================================
:: PRE-REQUISITES:
:: - Create venv: python -m venv venv
:: - Install dependencies: pip install -r requirements.txt
:: ============================================================

:: %~dp0 ensures the script finds its files even if called from a different folder
set "PROJECT_ROOT=%~dp0"
cd /d "%PROJECT_ROOT%"

echo [Tenali] Waking up...

:: 1. Activate the environment (using relative path)
if exist "venv\Scripts\activate" (
    call "venv\Scripts\activate"
) else (
    echo [ERROR] Virtual environment not found in %PROJECT_ROOT%
    echo Run: python -m venv venv
    pause
    exit /b
)

:: 2. Execute with absolute reference to the main.py
:: This ensures the python interpreter knows exactly where main.py lives
python "%PROJECT_ROOT%main.py"

if %errorlevel% neq 0 (
    echo.
    echo [CRASH] Tenali encountered an error.
    pause
)
