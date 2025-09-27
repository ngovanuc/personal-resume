@echo off
REM Build and Deploy Script for Personal Resume Website (Windows)

setlocal EnableDelayedExpansion

REM Variables
set IMAGE_NAME=personal-resume
set CONTAINER_NAME=personal-resume-web
set TAG=%1
if "%TAG%"=="" set TAG=latest

echo === Personal Resume Website Deployment ===
echo Image: %IMAGE_NAME%:%TAG%
echo Container: %CONTAINER_NAME%
echo.

REM Check if Docker is running
echo [STEP] Checking Docker...
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not running. Please start Docker and try again.
    exit /b 1
)
echo [SUCCESS] Docker is running

REM Stop and remove existing container
echo [STEP] Stopping existing container...
docker stop %CONTAINER_NAME% >nul 2>&1
docker rm %CONTAINER_NAME% >nul 2>&1
echo [SUCCESS] Existing container cleaned up

REM Build new image
echo [STEP] Building Docker image...
docker build -t %IMAGE_NAME%:%TAG% .
if %errorlevel% neq 0 (
    echo [ERROR] Failed to build image
    exit /b 1
)
echo [SUCCESS] Image built successfully

REM Run container
echo [STEP] Starting new container...
docker run -d --name %CONTAINER_NAME% -p 8080:8080 --restart unless-stopped %IMAGE_NAME%:%TAG%
if %errorlevel% neq 0 (
    echo [ERROR] Failed to start container
    exit /b 1
)
echo [SUCCESS] Container started successfully

REM Wait for container to be ready
echo [STEP] Waiting for application to start...
timeout /t 10 /nobreak >nul

REM Health check
echo [STEP] Performing health check...
curl -f http://localhost:8080/ >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Health check failed
    echo Container logs:
    docker logs %CONTAINER_NAME%
    exit /b 1
)
echo [SUCCESS] Health check passed

REM Display status
echo.
echo === Deployment Complete ===
echo ✓ Application is running at: http://localhost:8080
echo ✓ Container name: %CONTAINER_NAME%
echo ✓ Image: %IMAGE_NAME%:%TAG%
echo.
echo Useful commands:
echo   View logs: docker logs -f %CONTAINER_NAME%
echo   Stop: docker stop %CONTAINER_NAME%
echo   Shell access: docker exec -it %CONTAINER_NAME% /bin/bash

pause