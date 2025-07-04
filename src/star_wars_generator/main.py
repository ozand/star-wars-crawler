"""Главный модуль для запуска Star Wars Generator."""

import argparse
import sys
from pathlib import Path

from star_wars_generator import Fixed3DStarWarsGeneratorV2

# Добавляем src в путь для импорта (если необходимо)
src_path = Path(__file__).parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))


def main() -> None:
    """Главная функция запуска генератора."""
    parser = argparse.ArgumentParser(
        description="Star Wars Style Text Crawler Generator"
    )
    parser.add_argument(
        "--config",
        default="starwars_crawl.json",
        help="Path to JSON configuration file",
    )
    parser.add_argument("--output", default="output.mp4", help="Output video file path")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")

    args = parser.parse_args()

    try:
        generator = Fixed3DStarWarsGeneratorV2()

        if args.debug:
            print("🎬 Starting Star Wars Generator...")
            print(f"📄 Config: {args.config}")
            print(f"📁 Output: {args.output}")

        # Запуск генерации (пока используем существующий метод)
        generator.create_video()

        if args.debug:
            print("✅ Video generation completed successfully!")

    except (FileNotFoundError, ImportError, RuntimeError) as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
