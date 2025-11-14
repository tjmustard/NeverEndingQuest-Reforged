@echo off
REM Master Launcher for LM Studio Mode
REM This opens both terminals needed to run the game with LM Studio

echo.
echo ========================================================================
echo NEVERENDINGQUEST - LM STUDIO MODE LAUNCHER
echo ========================================================================
echo.
echo This will launch TWO terminal windows:
echo.
echo   WINDOW 1: LM Studio Forwarder Proxy (runs in background)
echo   WINDOW 2: NeverEndingQuest Game (your main window)
echo.
echo ========================================================================
echo.
echo REQUIREMENTS CHECKLIST:
echo.
echo [ ] LM Studio is installed and running
echo [ ] A model is loaded in LM Studio
echo [ ] LM Studio's Local Server is started (bottom-right of LM Studio)
echo [ ] You can see "Server running on port 1234" in LM Studio
echo [ ] mitmproxy is installed (pip install mitmproxy)
echo.
echo ========================================================================
echo.
echo If everything is ready, press any key to launch...
pause >nul

echo.
echo [1/2] Opening LM Studio Forwarder Proxy in new window...

REM Open the forwarder in a new terminal
start "LM Studio Forwarder Proxy" cmd /k "start_lmstudio_proxy.bat"

echo [WAIT] Waiting 3 seconds for proxy to initialize...
timeout /t 3 /nobreak >nul

echo.
echo [2/2] Opening NeverEndingQuest Game in new window...

REM Open the game in a new terminal
start "NeverEndingQuest - LM Studio Mode" cmd /k "run_with_lmstudio.bat"

echo.
echo ========================================================================
echo BOTH WINDOWS LAUNCHED!
echo ========================================================================
echo.
echo You should now see:
echo   - LM Studio Forwarder Proxy window (running in background)
echo   - NeverEndingQuest Game window (your main game interface)
echo.
echo IMPORTANT: Do NOT close the Forwarder Proxy window while playing!
echo.
echo To stop everything:
echo   1. Close the game window
echo   2. Close the forwarder proxy window
echo.
echo ========================================================================
echo.
echo This master launcher window can now be closed.
echo.
pause
