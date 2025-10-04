@echo off
REM ============================================================================
REM NeverEndingQuest - Windows Installation Script with Virtual Environment
REM Automated installer for non-technical users
REM ============================================================================

SETLOCAL EnableDelayedExpansion

echo.
echo ========================================
echo   NeverEndingQuest Installation
echo ========================================
echo.

REM Step 1: Check for Python
echo Step 1: Checking for Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    echo.
    echo Please install Python 3.9 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANT: During installation, check the box "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

python --version
echo [OK] Python found!
echo.

REM Step 2: Check for Git
echo Step 2: Checking for Git...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Git not found. Attempting to install...
    echo.

    REM Try winget first (Windows 10+)
    winget install --id Git.Git -e --source winget >nul 2>&1
    if %errorlevel% equ 0 (
        echo [OK] Git installed via winget!
        echo Please restart this script to continue.
        pause
        exit /b 0
    ) else (
        echo ERROR: Could not auto-install Git
        echo.
        echo Please install Git manually from:
        echo https://git-scm.com/download/win
        echo.
        echo After installing Git, run this script again.
        pause
        exit /b 1
    )
)

git --version
echo [OK] Git found!
echo.

REM Step 3: Clone repository
echo Step 3: Cloning repository...
echo Installing to: %CD%
echo.

if exist "NeverEndingQuest" (
    echo Repository folder already exists. Updating...
    cd NeverEndingQuest
    git pull
    if %errorlevel% neq 0 (
        echo Warning: Git pull failed. Continuing with existing version...
    )
    cd ..
) else (
    git clone https://github.com/MoonlightByte/NeverEndingQuest.git
    if %errorlevel% neq 0 (
        echo ERROR: Failed to clone repository
        echo.
        echo Please check your internet connection and try again.
        pause
        exit /b 1
    )
    echo [OK] Repository cloned successfully!
)

cd NeverEndingQuest

REM Step 4: Create virtual environment
echo.
echo Step 4: Creating Python virtual environment...
if not exist "venv" (
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)

REM Step 5: Activate venv and install dependencies
echo.
echo Step 5: Installing dependencies in virtual environment...
echo This may take a few minutes...
echo.

call venv\Scripts\activate.bat

python -m pip install --upgrade pip
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    echo.
    echo Try running manually:
    echo   cd %CD%
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    pause
    exit /b 1
)

echo [OK] Dependencies installed successfully!

REM Step 6: Setup configuration
echo.
echo Step 6: Setting up configuration...
if not exist "config.py" (
    copy config_template.py config.py
    echo [OK] Created config.py from template
    echo.
    echo ========================================
    echo   IMPORTANT: API Key Required
    echo ========================================
    echo.
    echo Opening config.py for you to add your OpenAI API key...
    echo.
    echo Find this line:
    echo   OPENAI_API_KEY = "your-api-key-here"
    echo.
    echo And replace "your-api-key-here" with your actual API key
    echo Get your key at: https://platform.openai.com/api-keys
    echo.
    timeout /t 3 >nul
    notepad config.py

    echo.
    echo After adding your API key, save and close Notepad.
    pause
) else (
    echo [OK] config.py already exists
)

REM Step 7: Create desktop shortcut and launch script
echo.
echo Step 7: Creating launch scripts...

REM Create launch_game.bat in the repo folder
echo @echo off > launch_game.bat
echo cd /d "%%~dp0" >> launch_game.bat
echo call venv\Scripts\activate.bat >> launch_game.bat
echo python run_web.py >> launch_game.bat
echo pause >> launch_game.bat

echo [OK] Created launch_game.bat

REM Create desktop shortcut
set SCRIPT_DIR=%CD%
set SHORTCUT_TARGET=%USERPROFILE%\Desktop\NeverEndingQuest.lnk

powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%SHORTCUT_TARGET%'); $s.TargetPath = '%SCRIPT_DIR%\launch_game.bat'; $s.WorkingDirectory = '%SCRIPT_DIR%'; $s.IconLocation = '%SCRIPT_DIR%\web\static\favicon.ico'; $s.Description = 'Launch NeverEndingQuest AI Dungeon Master'; $s.Save()" >nul 2>&1

if exist "%USERPROFILE%\Desktop\NeverEndingQuest.lnk" (
    echo [OK] Desktop shortcut created!
) else (
    echo [WARNING] Could not create desktop shortcut
    echo You can manually create a shortcut to: %CD%\launch_game.bat
)

echo.
echo ========================================
echo   Installation Complete!
echo ========================================
echo.
echo Installation location: %CD%
echo.
echo HOW TO RUN:
echo   Option 1: Double-click "NeverEndingQuest" icon on your Desktop
echo   Option 2: Run launch_game.bat in this folder
echo   Option 3: Run manually:
echo            venv\Scripts\activate
echo            python run_web.py
echo.
echo The game will open at: http://localhost:8357
echo.
echo Press any key to launch the game now...
pause >nul

REM Launch the game
call venv\Scripts\activate.bat
start http://localhost:8357
python run_web.py

:END
