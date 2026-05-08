@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   ROBOT SYNC - CAP TOC 2026
echo ========================================
echo.
powershell -ExecutionPolicy Bypass -File "%~dp0sync_playlist.ps1"
echo.
pause
