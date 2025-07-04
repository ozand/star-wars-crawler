@echo off
REM Star Wars CLI launcher for Windows
REM Ensures proper UTF-8 encoding for Unicode support
chcp 65001 >nul
python "%~dp0starwars-cli.py" %*
