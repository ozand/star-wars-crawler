@echo off
chcp 65001 >nul
echo 🌟 STAR WARS CRAWL GENERATOR 🌟
echo ================================
echo.
echo Выберите версию для запуска:
echo 1. Простая версия (рекомендуется)
echo 2. Расширенная версия (с эффектами)
echo 3. Оригинальная версия
echo.
set /p choice="Введите номер (1-3): "

if "%choice%"=="1" (
    echo.
    echo Запуск простой версии...
    python simple_generator.py
) else if "%choice%"=="2" (
    echo.
    echo Запуск расширенной версии...
    python star_wars_generator.py
) else if "%choice%"=="3" (
    echo.
    echo Запуск оригинальной версии...
    python main.py
) else (
    echo.
    echo Неверный выбор. Запуск простой версии по умолчанию...
    python simple_generator.py
)

echo.
echo Нажмите любую клавишу для завершения...
pause >nul
