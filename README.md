# Star Wars Crawl Generator ⭐

Создавайте эпичные видео в стиле Star Wars с прокручивающимся текстом!

## ✨ Ключевые возможности

- 🎯 **Правильная 3D перспектива** - текст уходит в глубину экрана, как в оригинале
- 🎛️ **Настраиваемый наклон** - точная настройка угла перспективы (5-30°)
- 📁 **Организованная структура** - чистая архитектура проекта
- 🎯 **Гибкие пути сохранения** - поддержка папок и конкретных путей
- ⚡ **Быстрый запуск** - готовые скрипты для всех платформ

## 🚀 Быстрый старт

```bash
# 1. Установите зависимости
pip install -r requirements.txt

# 2. Создайте ваше первое видео
python starwars-cli.py

# 3. Результат: output/starwars_crawl.mp4 готов!
```

### 🎯 CLI Команды

```bash
# Просмотр справки
python starwars-cli.py --help

# Список доступных тем
python starwars-cli.py --list

# Использование готовой темы
python starwars-cli.py classic_yellow_normal -o my_video.mp4

# Сохранение в конкретную папку
python starwars-cli.py classic_yellow_normal -o ./videos/

# Создание видео из текста
python starwars-cli.py --title "МОЙ ЭПИЗОД" --text "Текст видео..." -o custom.mp4

# Настройка угла наклона текста
python starwars-cli.py --title "ТЕСТ" --text "Мой текст" --tilt 22 -o video.mp4

# Полная настройка перспективы
python starwars-cli.py classic_yellow_normal --tilt 22 --perspective-min 0.45 --perspective-max 0.72

# Сохранение в подпапку
python starwars-cli.py --title "ТЕСТ" --text "Текст..." -o my_folder/video.mp4

# Создание шаблона конфигурации  
python starwars-cli.py --template my_config.json

# Пакетная обработка всех тем
python starwars-cli.py --batch
```

## ✨ Возможности

- ⭐ **Классический эффект Star Wars** - точная имитация оригинала
- 🎨 **Настраиваемые цвета и шрифты** - создайте уникальный стиль  
- 🌍 **Поддержка русского языка** - полная поддержка UTF-8
- 📋 **JSON конфигурации** - легкая настройка через файлы
- 🎬 **Готовые темы** - 5 цветовых схем, 3 размера
- ⚡ **Быстрая генерация** - видео за секунды
- 🎯 **Правильная 3D перспектива** - текст уходит в глубину экрана, как в оригинале
- 📁 **Организованный вывод** - файлы сохраняются в папку `output/` по умолчанию
- 🎛️ **Гибкие пути сохранения** - поддержка папок и конкретных путей

### 🔧 Последние улучшения

**✅ Исправлена перспектива текста (январь 2025)**
- Текст теперь правильно уходит **В ГЛУБИНУ** экрана (не наружу)
- Верхняя часть текста **УЖЕ** (далеко), нижняя **ШИРЕ** (близко)
- Динамическая интенсивность перспективы
- Полная совместимость со всеми существующими конфигурациями

**✅ Настраиваемый наклон текста (январь 2025)**
- Параметры CLI: `--tilt`, `--perspective-min`, `--perspective-max`
- Оптимальные настройки для каждого типа контента
- Рекомендуемый угол: 22° для максимального соответствия оригиналу
- Безопасный диапазон: 10-25° (больше может привести к искажениям)

> 📄 Подробности в [docs/PERSPECTIVE_FIX_REPORT.md](docs/PERSPECTIVE_FIX_REPORT.md)  
> 🎯 Руководство по настройке: [docs/TILT_CONFIGURATION_GUIDE.md](docs/TILT_CONFIGURATION_GUIDE.md)

## 📖 Примеры

### Использование готовых тем
```bash
# Классическая желтая тема
python starwars-cli.py classic_yellow_normal

# Синяя тема
python starwars-cli.py blue_theme_normal

# Красная тема
python starwars-cli.py red_theme_normal
```

### Создание собственной конфигурации
```json
{
  "title": {
    "text": "МОЙ ЭПИЗОД\nЗВЁЗДНЫЕ ВОЙНЫ",
    "color": "#FFE81F",
    "font_size": 72
  },
  "main_text": {
    "text": "Давным-давно в далёкой-далёкой галактике...",
    "color": "#FFE81F",
    "font_size": 48
  },
  "animation": {
    "duration": 30
  }
}
```

### Программное использование
```python
from star_wars_generator import Fixed3DStarWarsGeneratorV2

generator = Fixed3DStarWarsGeneratorV2()
generator.load_config("examples/configs/classic_yellow_normal.json")
generator.generate_video("my_video.mp4")
```

## 📁 Управление выходными файлами

По умолчанию все видео сохраняются в папку `output/`, что помогает держать проект в порядке.

### Варианты указания пути сохранения:

```bash
# По умолчанию - в папку output/
python starwars-cli.py classic_yellow_normal
# Результат: output/starwars_classic_yellow_normal.mp4

# Указать конкретное имя файла
python starwars-cli.py classic_yellow_normal -o my_awesome_video.mp4
# Результат: output/my_awesome_video.mp4

# Сохранить в конкретную папку
python starwars-cli.py classic_yellow_normal -o ./my_videos/
# Результат: my_videos/starwars_classic_yellow_normal.mp4

# Полный путь к файлу
python starwars-cli.py classic_yellow_normal -o ./projects/starwars/episode4.mp4
# Результат: projects/starwars/episode4.mp4

# Папка создается автоматически если не существует
python starwars-cli.py classic_yellow_normal -o ./new_folder/subfolder/
# Результат: new_folder/subfolder/starwars_classic_yellow_normal.mp4
```

### Структура проекта после использования:
```
star_war_crawler/
├── output/                    # 📁 Основная папка для видео
│   ├── starwars_crawl.mp4    # Видео по умолчанию
│   └── custom_videos.mp4     # Пользовательские видео
├── examples/                  
│   └── configs/              # Готовые конфигурации
└── src/                      # Исходный код
```

## 🎯 Результат

Сгенерированные видео:
- **Формат:** MP4 (H.264)
- **Разрешение:** 1280x720 HD или 1920x1080 Full HD
- **Частота кадров:** 24 fps (киношная)
- **Длительность:** 15-60 секунд (настраивается)

## 📚 Документация

- [CLI Reference](docs/CLI.md) - полное руководство по командной строке
- [API Reference](docs/API.md) - полное описание API
- [Примеры использования](docs/EXAMPLES.md) - подробные примеры
- [Настройка наклона](docs/TILT_CONFIGURATION_GUIDE.md) - **руководство по настройке перспективы**
- [FAQ](docs/FAQ.md) - часто задаваемые вопросы

## 🎯 Настройка наклона текста

### Быстрая настройка через CLI
```bash
# Слабый наклон (для субтитров)
python starwars-cli.py --title "Заголовок" --text "Текст" --tilt 12

# Оптимальный наклон (как в оригинале)  
python starwars-cli.py classic_yellow_normal --tilt 22

# Сильный наклон (для эпических сцен)
python starwars-cli.py --title "ЭПИЗОД" --text "Текст" --tilt 25 --perspective-max 0.8
```

### Рекомендуемые углы
- **10-15°** - Информационные экраны, субтитры
- **18°** - Стандартная настройка по умолчанию  
- **22°** - **Оптимально** для Star Wars (рекомендуется)
- **25°** - Драматический эффект для трейлеров

> ⚠️ **Важно:** Углы больше 30° могут привести к исчезновению текста

**📖 Подробное руководство:** [docs/TILT_CONFIGURATION_GUIDE.md](docs/TILT_CONFIGURATION_GUIDE.md)

## 🛠️ Системные требования

- **Python:** 3.8+
- **ОС:** Windows, macOS, Linux
- **RAM:** 2 GB минимум
- **Диск:** 100 MB для зависимостей

## 🚀 Пакетная обработка

Создание множества видео с разными настройками:

```bash
# Создать все варианты из examples/configs/
python starwars-cli.py --batch
```

Результат в папке `examples/videos/` - 15 видео с разными темами и размерами!

## 🎊 Примеры видео

После первого запуска в корне появится `starwars_crawl.mp4` - ваше первое Star Wars видео!

**May the Force be with you!** ⚔️✨

---

*Больше примеров и инструкций в папке [docs/](docs/)*
