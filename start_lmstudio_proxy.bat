@echo off
REM LM Studio Forwarder Proxy Launcher
REM This script starts the mitmproxy that forwards game API calls to LM Studio

echo.
echo ========================================================================
echo LM STUDIO FORWARDER PROXY
echo ========================================================================
echo.
echo This proxy will forward all game API calls to your local LM Studio.
echo.
echo REQUIREMENTS:
echo   1. LM Studio must be running with a model loaded
echo   2. LM Studio server must be started (check bottom-right of LM Studio)
echo   3. Default LM Studio port is 1234 (check Local Server tab in LM Studio)
echo.
echo If you need to change the port, edit lmstudio_forwarder.py line 20
echo.
echo ========================================================================
echo.
echo Starting forwarder on localhost:8080...
echo.

REM Check if mitmproxy is installed
where mitmdump >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] mitmproxy is not installed!
    echo.
    echo Please install mitmproxy first:
    echo   pip install mitmproxy
    echo.
    echo Or download from: https://mitmproxy.org/
    echo.
    pause
    exit /b 1
)

REM Run mitmproxy with LM Studio forwarder addon
mitmdump -s lmstudio_forwarder.py --listen-port 8080 --ssl-insecure --set confdir=./mitm_config

echo.
echo Forwarder stopped.
pause
