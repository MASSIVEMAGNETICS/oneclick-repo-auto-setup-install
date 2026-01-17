@echo off
REM Launcher script for the Universal Repository Setup Wizard (Windows)
REM This script ensures Python and dependencies are available

echo.
echo Universal Repository Setup Wizard Launcher
echo ===========================================
echo.

REM Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://www.python.org/
    echo.
    pause
    exit /b 1
)

REM Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Found Python %PYTHON_VERSION%

REM Check for tkinter
python -c "import tkinter" >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] tkinter not found
    echo tkinter should be included with Python on Windows
    echo If missing, reinstall Python with tkinter enabled
    echo.
    pause
    exit /b 1
)

echo [OK] tkinter is available

REM Check for Git (optional)
git --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=3" %%i in ('git --version 2^>^&1') do set GIT_VERSION=%%i
    echo [OK] Git %GIT_VERSION% is available
) else (
    echo [WARNING] Git not found (needed for URL cloning)
)

echo.
echo Starting Setup Wizard...
echo.

REM Launch the wizard
python "%~dp0setup_wizard.py" %*
