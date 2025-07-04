#!/usr/bin/env python3
"""Скрипт автоматизации ежедневного чек-листа для Python проекта."""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: str, description: str) -> bool:
    """Запускает команду и возвращает успешность выполнения."""
    print(f"🔄 {description}...")
    try:
        # Устанавливаем кодировку UTF-8 для Windows
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if result.returncode == 0:
            print(f"✅ {description} - успешно")
            return True
        print(f"❌ {description} - ошибка:")
        print(result.stderr)
        return False
    except Exception as e:
        print(f"❌ {description} - исключение: {e}")
        return False


def daily_checklist():
    """Выполняет ежедневный чек-лист."""
    print("🚀 ЕЖЕДНЕВНЫЙ ЧЕК-ЛИСТ PYTHON ПРОЕКТА")
    print("=" * 50)

    # 1. Форматирование кода
    success = run_command("ruff format .", "Форматирование кода (ruff format)")

    # 2. Проверка ошибок
    success &= run_command("ruff check . --fix", "Проверка и исправление ошибок")

    # 3. Проверка зависимостей (UV не имеет autoremove, используем другую команду)
    print("🔍 Проверка зависимостей...")
    run_command("uv pip list", "Просмотр установленных пакетов")

    # 4. Запуск тестов (если есть)
    if Path("tests").exists():
        success &= run_command("pytest tests/ -v", "Запуск тестов")

    print("\n" + "=" * 50)
    if success:
        print("✅ Все проверки пройдены успешно!")
    else:
        print("⚠️ Обнаружены проблемы, требующие внимания")

    return success


def weekly_checklist() -> None:
    """Выполняет еженедельный чек-лист."""
    print("🗓️ ЕЖЕНЕДЕЛЬНЫЙ ЧЕК-ЛИСТ")
    print("=" * 50)

    # 1. Проверка обновлений
    run_command("uv pip list --outdated", "Проверка устаревших пакетов")

    # 2. Поиск мертвого кода
    run_command("ruff check --select F401,F841 src/", "Поиск неиспользуемого кода")

    print("✅ Еженедельные проверки завершены")


def monthly_checklist() -> None:
    """Выполняет ежемесячный чек-лист."""
    print("📅 ЕЖЕМЕСЯЧНЫЙ ЧЕК-ЛИСТ")
    print("=" * 50)

    # 1. Полный аудит кода
    run_command("ruff check src/", "Полный аудит кода")

    # 2. Проверка зависимостей
    print("🔍 Проверка зависимостей...")
    run_command("uv pip list", "Просмотр зависимостей")

    # 3. Проверка архитектуры
    arch_file = Path("ARCHITECTURE.md")
    if arch_file.exists():
        print(f"📖 Файл архитектуры существует: {arch_file}")
        print("⚠️ Рекомендуется обновить ARCHITECTURE.md вручную")
    else:
        print("❌ Отсутствует файл ARCHITECTURE.md")

    print("✅ Ежемесячные проверки завершены")


def pre_commit_checklist():
    """Выполняет проверки перед коммитом."""
    print("📝 ЧЕК-ЛИСТ ПЕРЕД КОММИТОМ")
    print("=" * 50)

    success = True

    # 1. Форматирование
    success &= run_command("ruff format .", "Форматирование кода")

    # 2. Линтер
    success &= run_command("ruff check .", "Проверка линтера")

    # 3. Проверка зависимостей
    print("🔍 Проверка зависимостей...")
    run_command("uv pip list", "Просмотр зависимостей")

    # 4. Проверка структуры файлов
    print("🔍 Проверка структуры проекта...")

    required_files = ["src/", "tests/", "pyproject.toml", "ARCHITECTURE.md"]
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ Отсутствует: {file_path}")
            success = False

    print("\n" + "=" * 50)
    if success:
        print("✅ Готов к коммиту!")
    else:
        print("⚠️ Исправьте проблемы перед коммитом")

    return success


def main() -> None:
    """Главная функция."""
    if len(sys.argv) < 2:
        print("Использование:")
        print("  python checklist.py daily     - ежедневные проверки")
        print("  python checklist.py weekly    - еженедельные проверки")
        print("  python checklist.py monthly   - ежемесячные проверки")
        print("  python checklist.py pre-commit - проверки перед коммитом")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "daily":
        success = daily_checklist()
    elif command == "weekly":
        weekly_checklist()
        success = True
    elif command == "monthly":
        monthly_checklist()
        success = True
    elif command == "pre-commit":
        success = pre_commit_checklist()
    else:
        print(f"❌ Неизвестная команда: {command}")
        sys.exit(1)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
