#!/usr/bin/env python3
"""Pre-commit hook script для автоматических проверок."""

import subprocess
import sys


def run_command(command: str, description: str) -> bool:
    """Выполняет команду и возвращает успешность."""
    print(f"🔍 {description}...")
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            print(f"✅ {description} - успешно")
            return True
        print(f"❌ {description} - ошибка:")
        print(result.stdout)
        print(result.stderr)
        return False
    except Exception as e:
        print(f"❌ {description} - исключение: {e}")
        return False


def main() -> int:
    """Основная функция pre-commit хука."""
    print("🚀 PRE-COMMIT ПРОВЕРКИ")
    print("=" * 50)

    # Список проверок
    checks = [
        ("ruff format . --check", "Проверка форматирования кода"),
        ("ruff check .", "Проверка качества кода"),
        ("python -m pytest tests/ -v", "Запуск тестов"),
        ("python -c \"import src.star_wars_generator; print('Import OK')\"", "Проверка импортов"),
    ]

    success = True

    for command, description in checks:
        if not run_command(command, description):
            success = False

    print("\n" + "=" * 50)
    if success:
        print("✅ Все проверки пройдены! Коммит разрешен.")
        return 0
    print("❌ Обнаружены проблемы. Коммит заблокирован.")
    print("💡 Исправьте ошибки и попробуйте снова.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
