@echo off
REM LocalTunnel Auto-Start Script for Personal Resume

echo Starting Personal Resume with LocalTunnel...
echo.

REM Check if Docker container is running
docker ps | findstr "my-resume" >nul
if %errorlevel% neq 0 (
    echo [INFO] Starting Docker container...
    docker start my-resume
    timeout /t 5 /nobreak >nul
) else (
    echo [INFO] Docker container already running
)

REM Check container health
echo [INFO] Checking container health...
timeout /t 3 /nobreak >nul

REM Start LocalTunnel
echo [INFO] Starting LocalTunnel...
echo [INFO] Your website will be available at: https://random-word.loca.lt
echo [INFO] Press Ctrl+C to stop tunnel
echo.

lt --port 8080 --subdomain ngovanuc-resume

pause