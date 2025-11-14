@echo off
REM Run NeverEndingQuest with LM Studio (via patched OpenAI library)

echo.
echo ========================================================================
echo NEVERENDINGQUEST - LM STUDIO MODE
echo ========================================================================
echo.
echo This will run the game using your local LM Studio instead of OpenAI API.
echo.
echo BEFORE RUNNING THIS:
echo   1. Make sure start_lmstudio_proxy.bat is running in another terminal
echo   2. Make sure LM Studio is running with a model loaded
echo   3. Make sure LM Studio's server is started
echo.
echo ========================================================================
echo.

REM Check if the forwarder is already running
netstat -an | find "8080" | find "LISTENING" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] The forwarder proxy does not appear to be running!
    echo.
    echo Please start start_lmstudio_proxy.bat in another terminal first.
    echo.
    echo Press Ctrl+C to cancel, or any key to continue anyway...
    pause >nul
)

echo Starting game with LM Studio integration...
echo.

REM Run the game with the patcher
python openai_patcher.py

pause
