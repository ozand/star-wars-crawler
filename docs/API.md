# API Reference

## Основной класс: Fixed3DStarWarsGeneratorV2

### Импорт
```python
from star_wars_generator import Fixed3DStarWarsGeneratorV2
```

### Методы

#### `__init__()`
Создает новый экземпляр генератора.

```python
generator = Fixed3DStarWarsGeneratorV2()
```

#### `generate_video(output_path: str)`
Генерирует видео с текущими настройками.

**Параметры:**
- `output_path` (str): Путь для сохранения видео файла

**Пример:**
```python
generator.generate_video("my_video.mp4")
```

#### `load_config(config_path: str)`
Загружает настройки из JSON файла.

**Параметры:**
- `config_path` (str): Путь к JSON файлу конфигурации

**Пример:**
```python
generator.load_config("examples/configs/classic_yellow_normal.json")
```

#### `load_config_dict(config: dict)`
Загружает настройки из словаря Python.

**Параметры:**
- `config` (dict): Словарь с настройками

**Пример:**
```python
config = {
    "title": {"text": "My Title", "color": "#FFE81F", "font_size": 72}
}
generator.load_config_dict(config)
```

#### `load_text_data(text_path: str)`
Загружает текст из простого текстового файла.

**Параметры:**
- `text_path` (str): Путь к .txt файлу

**Пример:**
```python
generator.load_text_data("examples/data/starwars_crawl.txt")
```

## Структура конфигурации

### Полная схема JSON

```json
{
  "intro_text": {
    "text": "string",
    "color": "hex_color",
    "font_size": number
  },
  "title": {
    "text": "string",
    "color": "hex_color",
    "font_size": number
  },
  "main_text": {
    "text": "string",
    "color": "hex_color",
    "font_size": number
  },
  "animation": {
    "duration": number
  },
  "video_settings": {
    "width": number,
    "height": number,
    "fps": number,
    "output_filename": "string"
  },
  "background": {
    "color": "hex_color"
  }
}
```

### Значения по умолчанию

```json
{
  "intro_text": {
    "text": "A long time ago in a galaxy far, far away....",
    "color": "#4A90E2",
    "font_size": 36
  },
  "title": {
    "text": "Episode IV\nA NEW HOPE",
    "color": "#FFE81F",
    "font_size": 72
  },
  "main_text": {
    "text": "It is a period of civil war...",
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
```

## Примеры использования

### Базовый пример
```python
from star_wars_generator import Fixed3DStarWarsGeneratorV2

generator = Fixed3DStarWarsGeneratorV2()
generator.generate_video("output.mp4")
```

### С конфигурацией
```python
generator = Fixed3DStarWarsGeneratorV2()
generator.load_config("examples/configs/blue_theme_large.json")
generator.generate_video("blue_video.mp4")
```

### Программная настройка
```python
config = {
    "title": {
        "text": "МОЙ ФИЛЬМ",
        "color": "#FF6B6B",
        "font_size": 80
    },
    "main_text": {
        "text": "Это история о...",
        "color": "#FFE81F",
        "font_size": 50
    },
    "animation": {
        "duration": 30
    }
}

generator = Fixed3DStarWarsGeneratorV2()
generator.load_config_dict(config)
generator.generate_video("my_movie.mp4")
```
