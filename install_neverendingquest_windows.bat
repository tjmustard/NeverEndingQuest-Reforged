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

REM Copy template if config.py doesn't exist
if not exist "config.py" (
    copy config_template.py config.py
    echo [OK] Created config.py from template
)

REM Check if API key needs to be configured (check for default placeholder)
findstr /C:"your_openai_api_key_here" config.py >nul 2>&1
if %errorlevel% equ 0 (
    REM API key is still the default placeholder
    echo.
    echo ========================================
    echo   OpenAI API Key Setup
    echo ========================================
    echo.
    echo Choose your setup method:
    echo   1. Enter API key now (recommended)
    echo   2. Skip and add manually later
    echo.
    choice /C 12 /N /M "Enter your choice (1 or 2): "

    if errorlevel 2 (
        REM User chose to skip
        echo.
        echo [SKIPPED] You can add your API key later by editing config.py
        echo Find this line: OPENAI_API_KEY = "your_openai_api_key_here"
        echo Get your key at: https://platform.openai.com/api-keys
        echo.
        timeout /t 3 >nul
    ) else (
        REM User chose to enter key now
        echo.
        echo Opening API key entry dialog...
        echo.

        REM Use PowerShell to show input dialog with proper assembly loading
        for /f "usebackq delims=" %%i in (`powershell -NoProfile -Command "Add-Type -AssemblyName Microsoft.VisualBasic; $key = [Microsoft.VisualBasic.Interaction]::InputBox('Enter your OpenAI API key (starts with sk-):\n\nGet your key at: https://platform.openai.com/api-keys\n\nLeave blank to skip and add manually later.', 'NeverEndingQuest - API Key Setup', ''); if ($key) { Write-Output $key } else { Write-Output 'SKIP_BLANK' }"`) do set API_KEY=%%i

        if "!API_KEY!"=="SKIP_BLANK" (
            echo [SKIPPED] You can add your API key later by editing config.py
            timeout /t 2 >nul
        ) else if "!API_KEY!"=="" (
            echo [SKIPPED] Dialog was cancelled. You can add the key later by editing config.py
            timeout /t 2 >nul
        ) else (
            REM Replace the API key in config.py (match actual template placeholder)
            powershell -NoProfile -Command "(Get-Content config.py) -replace 'your_openai_api_key_here', '!API_KEY!' | Set-Content config.py"
            echo [OK] API key added to config.py successfully!
            timeout /t 2 >nul
        )
    )
) else (
    echo [OK] API key already configured in config.py
)

REM Step 6b: Create empty party_tracker.json to prevent startup errors
echo.
echo Step 6b: Creating initial game files...

if not exist "party_tracker.json" (
    echo {} > party_tracker.json
    echo [OK] Created empty party_tracker.json
) else (
    echo [OK] party_tracker.json already exists
)

REM Step 6c: Module selection
echo.
echo ========================================
echo   Module Selection
echo ========================================
echo.
echo Choose your starting modules:
echo   1. Default modules (Thornwood Watch + Keep of Doom)
echo   2. Community modules (from neverendingquest-modules repo)
echo.
choice /C 12 /N /M "Enter your choice (1 or 2): "

if errorlevel 2 (
    REM User chose community modules
    echo.
    echo Fetching available community modules...
    echo.

    REM Clone the modules repo if it doesn't exist
    if not exist "..\neverendingquest-modules" (
        cd ..
        git clone https://github.com/MoonlightByte/neverendingquest-modules.git
        if !errorlevel! neq 0 (
            echo [WARNING] Failed to clone modules repository
            echo Continuing with default modules...
            timeout /t 3 >nul
            cd NeverEndingQuest
            goto SKIP_MODULE_SETUP
        )
        cd NeverEndingQuest
    ) else (
        REM Update existing modules repo
        cd ..\neverendingquest-modules
        git pull >nul 2>&1
        cd ..\NeverEndingQuest
    )

    REM List available modules
    echo.
    echo Available community modules:
    echo.
    set MODULE_COUNT=0
    for /d %%d in ("..\neverendingquest-modules\*") do (
        REM Skip .git and other non-module directories
        if /I not "%%~nxd"==".git" (
            if exist "%%d\manifest.json" (
                set /a MODULE_COUNT+=1
                echo   !MODULE_COUNT!. %%~nxd
                set MODULE_!MODULE_COUNT!=%%~nxd
            ) else (
                REM Check for module.json pattern
                for %%f in ("%%d\*_module.json") do (
                    set /a MODULE_COUNT+=1
                    echo   !MODULE_COUNT!. %%~nxd
                    set MODULE_!MODULE_COUNT!=%%~nxd
                    goto NEXT_MODULE
                )
                :NEXT_MODULE
            )
        )
    )

    if !MODULE_COUNT! equ 0 (
        echo [WARNING] No community modules found
        echo Continuing with default modules...
        timeout /t 3 >nul
        goto SKIP_MODULE_SETUP
    )

    echo.
    echo Enter module number to install (or press Enter for all):
    set /p MODULE_CHOICE=

    echo.
    echo Do you want to:
    echo   1. Add to existing default modules
    echo   2. Replace default modules
    echo.
    choice /C 12 /N /M "Enter your choice (1 or 2): "

    if errorlevel 2 (
        REM Replace - delete default modules
        echo.
        echo Removing default modules...
        if exist "modules\The_Thornwood_Watch" (
            rmdir /s /q "modules\The_Thornwood_Watch"
            echo [OK] Removed Thornwood Watch
        )
        if exist "modules\Keep_of_Doom" (
            rmdir /s /q "modules\Keep_of_Doom"
            echo [OK] Removed Keep of Doom
        )
    )

    REM Copy selected module(s)
    echo.
    echo Installing community module(s)...

    if "!MODULE_CHOICE!"=="" (
        REM Install all modules
        for /l %%i in (1,1,!MODULE_COUNT!) do (
            echo Copying !MODULE_%%i!...
            xcopy "..\neverendingquest-modules\!MODULE_%%i!" "modules\!MODULE_%%i!" /E /I /Y >nul
            if !errorlevel! equ 0 (
                echo [OK] Installed !MODULE_%%i!
            ) else (
                echo [WARNING] Failed to install !MODULE_%%i!
            )
        )
    ) else (
        REM Install specific module
        if defined MODULE_!MODULE_CHOICE! (
            echo Copying !MODULE_%MODULE_CHOICE%!...
            xcopy "..\neverendingquest-modules\!MODULE_%MODULE_CHOICE%!" "modules\!MODULE_%MODULE_CHOICE%!" /E /I /Y >nul
            if !errorlevel! equ 0 (
                echo [OK] Installed !MODULE_%MODULE_CHOICE%!
            ) else (
                echo [WARNING] Failed to install !MODULE_%MODULE_CHOICE%!
            )
        ) else (
            echo [WARNING] Invalid module selection
        )
    )
) else (
    REM User chose default modules - they're already in the repo
    echo [OK] Using default modules (Thornwood Watch + Keep of Doom)
)

:SKIP_MODULE_SETUP

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

powershell -NoProfile -ExecutionPolicy Bypass -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%SHORTCUT_TARGET%'); $s.TargetPath = '%SCRIPT_DIR%\launch_game.bat'; $s.WorkingDirectory = '%SCRIPT_DIR%'; $s.Description = 'Launch NeverEndingQuest AI Dungeon Master'; $s.Save()" 2>nul

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
