#!/usr/bin/env python3
"""Точка входа для Star Wars CLI."""

import sys
from pathlib import Path

from star_wars_generator.cli import main

# Добавляем путь к модулям (если необходимо)
project_root = Path(__file__).parent
if str(project_root / "src") not in sys.path:
    sys.path.insert(0, str(project_root / "src"))

if __name__ == "__main__":
    sys.exit(main())
