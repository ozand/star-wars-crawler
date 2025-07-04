# Examples Directory

Эта папка содержит примеры использования Star Wars Crawl Generator.

## Структура

### `configs/`
Конфигурационные файлы в формате JSON для различных тем и размеров:
- `*_theme_*.json` - Тематические конфигурации (blue, classic_yellow, green, purple, red)
- Размеры: `small`, `normal`, `large`

### `data/`
Примеры входных данных:
- `starwars_crawl.json` - JSON структура с настройками текста и цветов
- `starwars_crawl.txt` - Простой текстовый формат

### `videos/`
Примеры выходных видео файлов:
- `*_theme_*.mp4` - Сгенерированные видео с различными темами и размерами

## Использование

Для использования конфигураций из этой папки:

```python
from star_wars_generator import Fixed3DStarWarsGeneratorV2

# Загрузка конфигурации
generator = Fixed3DStarWarsGeneratorV2()
generator.load_config("examples/configs/classic_yellow_normal.json")

# Или использование примера данных
generator.load_text_data("examples/data/starwars_crawl.txt")
```

## Создание собственных примеров

1. Скопируйте существующий конфигурационный файл
2. Измените параметры под ваши нужды
3. Сохраните с описательным именем
4. Добавьте описание в этот README
