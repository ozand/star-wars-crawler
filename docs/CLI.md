# CLI Reference

Star Wars Crawl Generator поставляется с полнофункциональным интерфейсом командной строки.

## Установка и запуск

### Windows
```cmd
# Прямой запуск
python starwars-cli.py [options]

# Или через batch файл
starwars-cli.bat [options]
```

### Linux/macOS
```bash
# Прямой запуск
python3 starwars-cli.py [options]

# Или через shell скрипт
chmod +x starwars-cli.sh
./starwars-cli.sh [options]
```

## Основные команды

### Создание видео с настройками по умолчанию
```bash
python starwars-cli.py
```
Создает `starwars_crawl.mp4` с классическим текстом Star Wars.

### Просмотр доступных тем
```bash
python starwars-cli.py --list
```
Показывает все готовые конфигурации в `examples/configs/`.

### Использование готовых тем
```bash
# Формат: python starwars-cli.py [theme_name] [options]

# Классические темы
python starwars-cli.py classic_yellow_normal
python starwars-cli.py classic_yellow_large  
python starwars-cli.py classic_yellow_small

# Цветные темы
python starwars-cli.py blue_theme_normal
python starwars-cli.py red_theme_normal
python starwars-cli.py green_theme_normal
python starwars-cli.py purple_theme_normal

# С указанием выходного файла
python starwars-cli.py blue_theme_large -o my_blue_video.mp4
```

### Создание видео из текста
```bash
python starwars-cli.py --title "ЗАГОЛОВОК" --text "Основной текст видео" -o output.mp4
```

**Примеры:**
```bash
# Русский текст
python starwars-cli.py --title "ЭПИЗОД V" --text "Империя наносит ответный удар..." -o episode5.mp4

# Английский текст
python starwars-cli.py --title "EPISODE VI" --text "Return of the Jedi..." -o episode6.mp4

# Короткое видео
python starwars-cli.py --title "ТРЕЙЛЕР" --text "Скоро в кинотеатрах" -o trailer.mp4
```

### Создание шаблона конфигурации
```bash
python starwars-cli.py --template my_config.json
```
Создает JSON файл с базовой конфигурацией, который можно отредактировать.

### Пакетная обработка
```bash
python starwars-cli.py --batch
```
Создает видео для всех конфигураций из `examples/configs/` и сохраняет в `examples/videos/`.

## Параметры командной строки

| Параметр | Краткая форма | Описание |
|----------|---------------|----------|
| `--help` | `-h` | Показать справку |
| `--version` | `-v` | Показать версию |
| `--list` | `-l` | Список доступных тем |
| `--output` | `-o` | Имя выходного файла |
| `--title` | | Заголовок видео |
| `--text` | | Основной текст |
| `--template` | `-t` | Создать шаблон |
| `--batch` | `-b` | Пакетная обработка |

## Примеры использования

### 1. Создание эпизода на русском языке
```bash
python starwars-cli.py \
  --title "ЗВЁЗДНЫЕ ВОЙНЫ\nЭпизод VIII\nПОСЛЕДНИЕ ДЖЕДАИ" \
  --text "Первый Орден правит галактикой железной рукой..." \
  -o last_jedi_ru.mp4
```

### 2. Быстрое создание трейлера
```bash
python starwars-cli.py \
  --title "COMING SOON" \
  --text "This Christmas\nThe saga continues..." \
  -o trailer.mp4
```

### 3. Использование файла конфигурации
```bash
# Создать шаблон
python starwars-cli.py --template my_episode.json

# Отредактировать my_episode.json в текстовом редакторе

# Создать видео
python starwars-cli.py my_episode.json -o my_episode.mp4
```

### 4. Создание серии видео
```bash
# Создать все варианты готовых тем
python starwars-cli.py --batch

# Результат: 15 видео в examples/videos/
# - classic_yellow_small.mp4
# - classic_yellow_normal.mp4  
# - classic_yellow_large.mp4
# - blue_theme_small.mp4
# - ... и т.д.
```

## Конфигурационные файлы

CLI поддерживает те же JSON конфигурации, что и основной API:

```json
{
  "intro_text": {
    "text": "Давным-давно в далёкой-далёкой галактике...",
    "color": "#4A90E2",
    "font_size": 36
  },
  "title": {
    "text": "МОЙ ЭПИЗОД",
    "color": "#FFE81F",
    "font_size": 72
  },
  "main_text": {
    "text": "Текст основной прокрутки...",
    "color": "#FFE81F",
    "font_size": 48
  },
  "animation": {
    "duration": 30
  }
}
```

## Автоматизация

### Интеграция в скрипты
```bash
#!/bin/bash
# create_episodes.sh

episodes=(
  "Episode I:The Phantom Menace"
  "Episode II:Attack of the Clones"  
  "Episode III:Revenge of the Sith"
)

for episode in "${episodes[@]}"; do
  title=$(echo $episode | cut -d: -f1)
  subtitle=$(echo $episode | cut -d: -f2)
  
  python starwars-cli.py \
    --title "$title\n$subtitle" \
    --text "Coming soon to theaters..." \
    -o "${title// /_}.mp4"
done
```

### Batch файл для Windows
```cmd
@echo off
REM create_all_themes.bat

FOR %%t IN (classic_yellow blue_theme red_theme green_theme purple_theme) DO (
  FOR %%s IN (small normal large) DO (
    python starwars-cli.py %%t_%%s -o videos\%%t_%%s.mp4
  )
)
```

## Советы и рекомендации

### Производительность
- Короткие тексты генерируются быстрее
- Меньшие шрифты = быстрее обработка
- Пакетная обработка оптимизирована для множественных видео

### Качество
- Используйте разрешение 1280x720 для веба
- Для презентаций лучше 1920x1080
- 24 fps - стандарт для кинематографичности

### Текст
- Переносы строк: используйте `\n` в JSON или естественные переносы в CLI
- Русский текст: сохраняйте файлы в UTF-8
- Длинные тексты автоматически оптимизируются по времени

### Отладка
```bash
# Проверка доступных тем
python starwars-cli.py --list

# Создание тестового видео
python starwars-cli.py --title "ТЕСТ" --text "Проверка" -o test.mp4

# Создание шаблона для изучения формата
python starwars-cli.py --template example.json
```
