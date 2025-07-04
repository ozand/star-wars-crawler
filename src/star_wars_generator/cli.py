#!/usr/bin/env python3
"""Star Wars Crawl Generator CLI
Командная строка для создания видео в стиле Star Wars.
"""

import argparse
import json
import sys
from pathlib import Path

# Добавляем путь к модулям
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

try:
    from star_wars_generator import Fixed3DStarWarsGeneratorV2
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("💡 Убедитесь, что установлены зависимости: pip install -r requirements.txt")
    sys.exit(1)


class StarWarsCLI:
    """Командная строка Star Wars Generator."""

    # Constants
    MIN_THEME_NAME_PARTS = 3

    def __init__(self) -> None:
        """Initialize the Star Wars CLI with default settings."""
        self.generator = Fixed3DStarWarsGeneratorV2()
        self.examples_dir = project_root / "examples"
        self.configs_dir = self.examples_dir / "configs"
        self.default_output_dir = project_root / "output"

        # Создаем выходную папку если её нет
        self.default_output_dir.mkdir(exist_ok=True)

    def resolve_output_path(self, output: str | None, default_filename: str) -> Path:
        """Разрешает путь вывода с поддержкой папок."""
        if not output:
            # По умолчанию сохраняем в output/
            return self.default_output_dir / default_filename

        output_path = Path(output)

        # Если указана только папка (заканчивается на /)
        if output.endswith(("/", "\\")) or (output_path.exists() and output_path.is_dir()):
            output_path = output_path / default_filename

        # Если путь не имеет расширения, считаем его папкой
        elif not output_path.suffix:
            output_path.mkdir(parents=True, exist_ok=True)
            output_path = output_path / default_filename

        # Создаем родительскую папку если её нет
        output_path.parent.mkdir(parents=True, exist_ok=True)

        return output_path

    def list_themes(self) -> None:
        """Показать доступные темы."""
        print("🎨 Доступные темы:")

        if not self.configs_dir.exists():
            print("❌ Папка с конфигурациями не найдена")
            return

        themes = {}
        for config_file in self.configs_dir.glob("*.json"):
            name_parts = config_file.stem.split("_")
            if len(name_parts) >= self.MIN_THEME_NAME_PARTS:
                theme = "_".join(name_parts[:-1])
                size = name_parts[-1]

                if theme not in themes:
                    themes[theme] = []
                themes[theme].append(size)

        for theme, sizes in themes.items():
            print(f"  📁 {theme}")
            for size in sorted(sizes):
                print(f"    ├─ {size}")

        print(f"\n💡 Всего конфигураций: {len(list(self.configs_dir.glob('*.json')))}")

    def create_video_from_config(self, config_path: str, output: str | None = None,
                               tilt_angle: float | None = None,
                               perspective_min: float | None = None,
                               perspective_max: float | None = None) -> bool:
        """Создать видео из конфигурации."""
        config_file = Path(config_path)

        if not config_file.exists():
            # Попробуем найти в examples/configs/
            config_file = self.configs_dir / config_path
            if not config_file.exists():
                config_file = self.configs_dir / f"{config_path}.json"

        if not config_file.exists():
            print(f"❌ Конфигурация не найдена: {config_path}")
            print("💡 Используйте --list для просмотра доступных тем")
            return False

        try:
            print(f"📋 Загружаем конфигурацию: {config_file.name}")
            self.generator.load_config_file(str(config_file))

            # Применяем дополнительные параметры перспективы если они заданы
            if tilt_angle is not None or perspective_min is not None or perspective_max is not None:
                print("🎯 Применяем дополнительные параметры перспективы:")
                if tilt_angle is not None:
                    self.generator.tilt_angle = tilt_angle
                    print(f"   Угол наклона: {tilt_angle}°")
                if perspective_min is not None:
                    self.generator.base_perspective = perspective_min
                    print(f"   Минимальная перспектива: {perspective_min}")
                if perspective_max is not None:
                    self.generator.max_perspective = perspective_max
                    print(f"   Максимальная перспектива: {perspective_max}")

            # Используем новый метод для определения пути вывода
            default_filename = f"starwars_{config_file.stem}.mp4"
            output_path = self.resolve_output_path(output, default_filename)

            print(f"🎬 Создаем видео: {output_path}")
            self.generator.generate_video(str(output_path))

            if output_path.exists():
                print(f"✅ Видео создано: {output_path}")
                return True
            print("❌ Видео не было создано")
            return False

        except (FileNotFoundError, json.JSONDecodeError, RuntimeError) as e:
            print(f"❌ Ошибка при создании видео: {e}")
            return False

    def create_video_from_text(self, title: str, text: str, output: str | None = None,
                             tilt_angle: float | None = None,
                             perspective_min: float | None = None,
                             perspective_max: float | None = None) -> bool:
        """Создать видео из текста."""
        # Исправляем обработку символов новой строки
        title = title.replace("\\n", "\n")
        text = text.replace("\\n", "\n")

        config = {
            "title": {
                "text": title,
                "color": "#FFE81F",
                "font_size": 72
            },
            "main_text": {
                "text": text,
                "color": "#FFE81F",
                "font_size": 48
            },
            "animation": {
                "duration": 30
            }
        }

        # Добавляем параметры перспективы если они заданы
        if tilt_angle is not None or perspective_min is not None or perspective_max is not None:
            config["perspective"] = {}
            if tilt_angle is not None:
                config["perspective"]["tilt_angle"] = tilt_angle
            if perspective_min is not None:
                config["perspective"]["base_perspective"] = perspective_min
            if perspective_max is not None:
                config["perspective"]["max_perspective"] = perspective_max

        try:
            print(f"📝 Создаем видео с заголовком: {title}")
            self.generator.load_config_dict(config)

            # Используем новый метод для определения пути вывода
            default_filename = "custom_starwars.mp4"
            output_path = self.resolve_output_path(output, default_filename)

            print(f"🎬 Создаем видео: {output_path}")
            self.generator.generate_video(str(output_path))

            if output_path.exists():
                print(f"✅ Видео создано: {output_path}")
                return True
            print("❌ Видео не было создано")
            return False

        except (FileNotFoundError, json.JSONDecodeError, RuntimeError) as e:
            print(f"❌ Ошибка при создании видео: {e}")
            return False

    def create_config_template(self, filename: str) -> bool:
        """Создать шаблон конфигурации."""
        template = {
            "intro_text": {
                "text": "A long time ago in a galaxy far, far away....",
                "color": "#4A90E2",
                "font_size": 36
            },
            "title": {
                "text": "Episode IV\\nA NEW HOPE",
                "color": "#FFE81F",
                "font_size": 72
            },
            "main_text": {
                "text": "It is a period of civil war.\\nRebel spaceships, striking\\nfrom a hidden base, have won\\ntheir first victory against\\nthe evil Galactic Empire.",
                "color": "#FFE81F",
                "font_size": 48
            },
            "animation": {
                "duration": 45
            },
            "video_settings": {
                "width": 1280,
                "height": 720,
                "fps": 24,
                "output_filename": "starwars_crawl.mp4"
            },
            "background": {
                "color": "#000000"
            }
        }

        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(template, f, indent=2, ensure_ascii=False)
            print(f"✅ Шаблон создан: {filename}")
            print(f"💡 Отредактируйте файл и используйте: starwars-cli {filename}")
            return True
        except (FileNotFoundError, PermissionError, OSError) as e:
            print(f"❌ Ошибка при создании шаблона: {e}")
            return False

    def batch_process(self) -> bool:
        """Пакетная обработка всех конфигураций."""
        if not self.configs_dir.exists():
            print("❌ Папка с конфигурациями не найдена")
            return False

        configs = list(self.configs_dir.glob("*.json"))
        if not configs:
            print("❌ Конфигурации не найдены")
            return False

        output_dir = self.examples_dir / "videos"
        output_dir.mkdir(exist_ok=True)

        print(f"🚀 Начинаем пакетную обработку {len(configs)} конфигураций...")

        success_count = 0
        for config_file in configs:
            try:
                print(f"\n📋 Обрабатываем: {config_file.name}")
                self.generator.load_config_file(str(config_file))

                output_path = output_dir / f"{config_file.stem}.mp4"
                self.generator.generate_video(str(output_path))

                if output_path.exists():
                    print(f"✅ Создано: {output_path.name}")
                    success_count += 1
                else:
                    print(f"❌ Не удалось создать: {config_file.name}")

            except (FileNotFoundError, json.JSONDecodeError, RuntimeError) as e:
                print(f"❌ Ошибка при обработке {config_file.name}: {e}")

        print(f"\n🎉 Завершено! Успешно создано: {success_count}/{len(configs)} видео")
        print(f"📁 Результаты в папке: {output_dir}")
        return success_count > 0


def main() -> int:
    """Главная функция CLI."""
    parser = argparse.ArgumentParser(
        description="🎬 Star Wars Crawl Generator - создание видео в стиле Star Wars",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:

  # Простое создание видео с настройками по умолчанию
  starwars-cli

  # Использование готовой темы
  starwars-cli classic_yellow_normal
  starwars-cli blue_theme_large

  # Настройка угла наклона
  starwars-cli classic_yellow_normal --tilt 22 --perspective-min 0.45 --perspective-max 0.7
  starwars-cli --title "МОЙ ЭПИЗОД" --text "Моя история..." --tilt 15

  # Создание видео из файла конфигурации
  starwars-cli my_config.json -o my_video.mp4

  # Создание видео из текста
  starwars-cli --title "МОЙ ЭПИЗОД" --text "История начинается..." -o custom.mp4

  # Просмотр доступных тем
  starwars-cli --list

  # Создание шаблона конфигурации
  starwars-cli --template my_template.json

  # Пакетная обработка всех тем
  starwars-cli --batch

Настройка перспективы:
  --tilt 10          # Слабый наклон (минимальная перспектива)
  --tilt 18          # Стандартный наклон (по умолчанию)
  --tilt 22          # Оптимальный наклон (рекомендуется)
  --tilt 25          # Сильный наклон (драматический эффект)

May the Force be with you! ⚔️✨
        """
    )

    # Основные команды
    parser.add_argument(
        "config",
        nargs="?",
        help="Имя темы или путь к JSON конфигурации (например: classic_yellow_normal, my_config.json)"
    )

    parser.add_argument(
        "-o", "--output",
        help="Путь к выходному файлу или папке (например: video.mp4, ./videos/, ./my_folder/video.mp4). По умолчанию: output/"
    )

    # Создание из текста
    parser.add_argument(
        "--title",
        help="Заголовок для видео (используется с --text)"
    )

    parser.add_argument(
        "--text",
        help="Основной текст для видео (используется с --title)"
    )

    # Параметры перспективы
    parser.add_argument(
        "--tilt",
        type=float,
        metavar="ANGLE",
        help="Угол наклона текста в градусах (рекомендуется: 10-25). Пример: --tilt 22"
    )

    parser.add_argument(
        "--perspective-min",
        type=float,
        metavar="VALUE",
        help="Минимальная интенсивность перспективы (0.0-1.0). Пример: --perspective-min 0.4"
    )

    parser.add_argument(
        "--perspective-max",
        type=float,
        metavar="VALUE",
        help="Максимальная интенсивность перспективы (0.0-1.0). Пример: --perspective-max 0.7"
    )

    # Утилиты
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="Показать доступные темы и конфигурации"
    )

    parser.add_argument(
        "--template", "-t",
        metavar="FILENAME",
        help="Создать шаблон JSON конфигурации"
    )

    parser.add_argument(
        "--batch", "-b",
        action="store_true",
        help="Создать видео для всех готовых конфигураций"
    )

    parser.add_argument(
        "--version", "-v",
        action="version",
        version="Star Wars Crawl Generator 1.0.0"
    )

    args = parser.parse_args()

    # Создаем CLI объект
    cli = StarWarsCLI()

    print("🌟 Star Wars Crawl Generator CLI")
    print("=" * 40)

    # Обработка команд
    if args.list:
        cli.list_themes()
        return 0

    if args.template:
        success = cli.create_config_template(args.template)
        return 0 if success else 1

    if args.batch:
        success = cli.batch_process()
        return 0 if success else 1

    if args.title and args.text:
        success = cli.create_video_from_text(
            args.title, args.text, args.output,
            args.tilt, args.perspective_min, args.perspective_max
        )
        return 0 if success else 1

    if args.title or args.text:
        print("❌ Для создания видео из текста нужны оба параметра: --title и --text")
        return 1

    if args.config:
        success = cli.create_video_from_config(
            args.config, args.output,
            args.tilt, args.perspective_min, args.perspective_max
        )
        return 0 if success else 1

    # По умолчанию - создаем видео с настройками по умолчанию
    print("🎬 Создаем видео с настройками по умолчанию...")
    try:
        # Используем новый метод для определения пути вывода
        default_filename = "starwars_crawl.mp4"
        output_path = cli.resolve_output_path(args.output, default_filename)

        print(f"📁 Сохраняем в: {output_path}")
        cli.generator.generate_video(str(output_path))

        if output_path.exists():
            print(f"✅ Видео создано: {output_path}")
            return 0
        print("❌ Видео не было создано")
        return 1
    except (FileNotFoundError, json.JSONDecodeError, RuntimeError, KeyboardInterrupt) as e:
        print(f"❌ Ошибка при создании видео: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
