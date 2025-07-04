# Примеры использования

## Готовые конфигурации

В папке `examples/configs/` находятся готовые конфигурации для быстрого старта.

### Классические темы

#### Желтая классическая тема
```bash
# Малый размер
python src/star_wars_generator/main.py examples/configs/classic_yellow_small.json

# Обычный размер
python src/star_wars_generator/main.py examples/configs/classic_yellow_normal.json

# Большой размер
python src/star_wars_generator/main.py examples/configs/classic_yellow_large.json
```

#### Цветные темы
```bash
# Синяя тема
python src/star_wars_generator/main.py examples/configs/blue_theme_normal.json

# Красная тема
python src/star_wars_generator/main.py examples/configs/red_theme_normal.json

# Зеленая тема
python src/star_wars_generator/main.py examples/configs/green_theme_normal.json

# Фиолетовая тема
python src/star_wars_generator/main.py examples/configs/purple_theme_normal.json
```

## Создание собственных конфигураций

### Пример 1: Русский эпизод

Создайте файл `my_russian_episode.json`:

```json
{
  "intro_text": {
    "text": "Давным-давно в далёкой-далёкой галактике...",
    "color": "#4A90E2",
    "font_size": 40
  },
  "title": {
    "text": "ЗВЁЗДНЫЕ ВОЙНЫ\nЭпизод IX\nВОЗРОЖДЕНИЕ СКАЙУОКЕРА",
    "color": "#FFE81F",
    "font_size": 60
  },
  "main_text": {
    "text": "Император мёртв. Но его наследие продолжает терзать галактику. Рей завершает обучение джедая под руководством генерала Леи, в то время как Сопротивление готовится к финальной битве против Первого Ордена.",
    "color": "#FFE81F",
    "font_size": 44
  },
  "animation": {
    "duration": 50
  },
  "video_settings": {
    "width": 1920,
    "height": 1080,
    "fps": 24,
    "output_filename": "russian_episode.mp4"
  }
}
```

Запуск:
```bash
python src/star_wars_generator/main.py my_russian_episode.json
```

### Пример 2: Короткий трейлер

Создайте файл `trailer.json`:

```json
{
  "title": {
    "text": "COMING SOON\nTO THEATERS EVERYWHERE",
    "color": "#FF6B6B",
    "font_size": 70
  },
  "main_text": {
    "text": "The saga continues...\n\nThis Christmas",
    "color": "#FFE81F",
    "font_size": 50
  },
  "animation": {
    "duration": 15
  },
  "video_settings": {
    "output_filename": "trailer.mp4"
  }
}
```

### Пример 3: Собственная история

Создайте файл `my_story.json`:

```json
{
  "intro_text": {
    "text": "В недалёком будущем...",
    "color": "#9775FA",
    "font_size": 36
  },
  "title": {
    "text": "КОСМИЧЕСКАЯ ОДИССЕЯ\nЧасть I\nНАЧАЛО",
    "color": "#51CF66",
    "font_size": 65
  },
  "main_text": {
    "text": "Человечество впервые достигло далёких звёзд. Команда исследователей обнаруживает странные сигналы с планеты Кеплер-442b. Что скрывают эти таинственные послания? Смогут ли люди разгадать секреты древней цивилизации?",
    "color": "#51CF66",
    "font_size": 46
  },
  "animation": {
    "duration": 40
  },
  "video_settings": {
    "width": 1280,
    "height": 720,
    "fps": 30,
    "output_filename": "my_space_odyssey.mp4"
  },
  "background": {
    "color": "#001122"
  }
}
```

## Программные примеры

### Генерация серии видео

```python
from star_wars_generator import Fixed3DStarWarsGeneratorV2

episodes = [
    {
        "title": "Эпизод I\nСКРЫТАЯ УГРОЗА",
        "main_text": "Республика охвачена беспорядками...",
        "filename": "episode_1.mp4"
    },
    {
        "title": "Эпизод II\nАТАКА КЛОНОВ",
        "main_text": "Прошло десять лет...",
        "filename": "episode_2.mp4"
    },
    {
        "title": "Эпизод III\nМЕСТЬ СИТХОВ",
        "main_text": "Война! Республика осаждена...",
        "filename": "episode_3.mp4"
    }
]

generator = Fixed3DStarWarsGeneratorV2()

for episode in episodes:
    config = {
        "title": {
            "text": episode["title"],
            "color": "#FFE81F",
            "font_size": 70
        },
        "main_text": {
            "text": episode["main_text"],
            "color": "#FFE81F",
            "font_size": 48
        }
    }

    generator.load_config_dict(config)
    generator.generate_video(episode["filename"])
    print(f"Создан {episode['filename']}")
```

### Случайные цвета

```python
import random
from star_wars_generator import Fixed3DStarWarsGeneratorV2

colors = ["#FFE81F", "#4A90E2", "#FF6B6B", "#51CF66", "#9775FA", "#FD79A8"]

generator = Fixed3DStarWarsGeneratorV2()

for i in range(5):
    color = random.choice(colors)
    config = {
        "title": {
            "text": f"ВИДЕО #{i+1}",
            "color": color,
            "font_size": 72
        },
        "main_text": {
            "text": f"Это видео номер {i+1} в случайном цвете!",
            "color": color,
            "font_size": 48
        }
    }

    generator.load_config_dict(config)
    generator.generate_video(f"random_video_{i+1}.mp4")
```

## Пакетная обработка

Создайте несколько JSON файлов в папке и обработайте их все:

```python
import os
from star_wars_generator import Fixed3DStarWarsGeneratorV2

config_folder = "my_configs"
output_folder = "my_videos"

os.makedirs(output_folder, exist_ok=True)

generator = Fixed3DStarWarsGeneratorV2()

for filename in os.listdir(config_folder):
    if filename.endswith('.json'):
        config_path = os.path.join(config_folder, filename)
        output_name = filename.replace('.json', '.mp4')
        output_path = os.path.join(output_folder, output_name)

        generator.load_config(config_path)
        generator.generate_video(output_path)
        print(f"Создано: {output_path}")
```

## Советы и хитрости

### Оптимальные размеры шрифтов
- **Интро текст:** 30-40px
- **Заголовок:** 60-80px
- **Основной текст:** 40-50px

### Популярные цветовые схемы
- **Классика:** `#FFE81F` (золотисто-желтый)
- **Синий космос:** `#4A90E2`
- **Сит красный:** `#FF6B6B`
- **Джедай зеленый:** `#51CF66`
- **Королевский фиолетовый:** `#9775FA`

### Длительность видео
- **Трейлер:** 10-15 секунд
- **Стандартный:** 30-45 секунд
- **Полный:** 60+ секунд

### Качество видео
- **Web:** 1280x720, 24fps
- **HD:** 1920x1080, 30fps
- **Cinema:** 1920x1080, 24fps
