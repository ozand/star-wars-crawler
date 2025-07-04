import cv2
import numpy as np
from moviepy.editor import ColorClip, CompositeVideoClip, TextClip

# === Настройки ===
WIDTH, HEIGHT = 1280, 720
DURATION = 45  # секунд
FPS = 24
FONT_SIZE = 48
FONT = "Arial-Bold"


# === Функция для чтения текста из файла ===
def read_crawl_text(filename="starwars_crawl.txt"):
    """Читает текст из файла для Star Wars Crawl"""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Файл {filename} не найден!")
        return None
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None


# === Читаем текст из файла ===
CRAWL_TEXT = read_crawl_text()
if CRAWL_TEXT is None:
    print("Не удалось прочитать текст. Завершение программы.")
    exit(1)

print("Текст успешно загружен из файла starwars_crawl.txt")

# === Создание текстового клипа ===
print("Создание текстового клипа...")
try:
    text_clip = TextClip(
        CRAWL_TEXT,
        fontsize=FONT_SIZE,
        color="#FFE81F",  # Классический желтый цвет Star Wars
        font="Arial-Bold",
        kerning=2,
        method="caption",
        size=(WIDTH - 200, None),  # Уменьшаем ширину для лучшего отображения
        align="center",
    )
    print("Текстовый клип создан успешно")

    # Тестовое сохранение кадра
    text_clip.save_frame("text_test.png", t=0)
    print("Тестовый кадр сохранен в text_test.png")
except Exception as e:
    print(f"Ошибка создания текстового клипа: {str(e)}")
    exit(1)


# === Функция для перспективного преобразования ===
def perspective_transform(get_frame, t):
    """Применяет перспективное преобразование для эффекта 'уходящего вдаль' текста"""
    frame = get_frame(t)
    h, w, _ = frame.shape

    # Коэффициент масштабирования - текст уменьшается по мере движения
    scale_factor = 1 + 0.5 * (t / DURATION)

    # Создаем матрицу перспективного преобразования
    src_points = np.float32([[0, 0], [w, 0], [w, h], [0, h]])

    # Уменьшаем верхнюю часть больше нижней для эффекта перспективы
    top_scale = 0.3 / scale_factor
    bottom_scale = 1.0 / scale_factor

    dst_points = np.float32(
        [
            [w * (1 - top_scale) / 2, 0],
            [w * (1 + top_scale) / 2, 0],
            [w * (1 + bottom_scale) / 2, h],
            [w * (1 - bottom_scale) / 2, h],
        ]
    )

    # Применяем перспективное преобразование
    matrix = cv2.getPerspectiveTransform(src_points, dst_points)
    warped = cv2.warpPerspective(frame, matrix, (w, h))

    return warped


# === Создание фона со звездами ===
def create_starfield(width, height):
    """Создает простое звездное поле"""
    stars = np.zeros((height, width, 3), dtype=np.uint8)

    # Добавляем случайные звезды
    np.random.seed(42)  # Для воспроизводимости
    num_stars = 200

    for _ in range(num_stars):
        x = np.random.randint(0, width)
        y = np.random.randint(0, height)
        brightness = np.random.randint(100, 255)
        stars[y, x] = [brightness, brightness, brightness]

    return stars


# === Анимация прокрутки и перспективы ===
# Устанавливаем длительность для текстового клипа
text_clip = text_clip.set_duration(DURATION)

# Применяем перспективное преобразование
text_clip = text_clip.fl(perspective_transform, apply_to=["mask"])


# Анимация движения текста снизу вверх
def move_text(t):
    # Начальная позиция внизу экрана
    start_y = HEIGHT + 100
    # Конечная позиция вверху экрана (за пределами видимости)
    end_y = -text_clip.h - 100

    # Линейное движение от низа к верху
    current_y = start_y + (end_y - start_y) * (t / DURATION)
    return ("center", current_y)


text_clip = text_clip.set_position(move_text)

# === Создание фона ===
print("Создание фона...")
# Создаем черный фон
background = ColorClip(size=(WIDTH, HEIGHT), color=(0, 0, 0), duration=DURATION)

# Опционально: можно добавить звездное поле
# starfield = create_starfield(WIDTH, HEIGHT)
# background = ImageClip(starfield, duration=DURATION)

# === Финальная композиция ===
print("Создание финального видео...")
video = (
    CompositeVideoClip([background, text_clip], size=(WIDTH, HEIGHT))
    .set_duration(DURATION)
    .set_fps(FPS)
)

# === Экспорт ===
print("Экспорт видео... Это может занять некоторое время.")
output_filename = "starwars_crawl.mp4"

try:
    video.write_videofile(
        output_filename,
        codec="libx264",
        audio=False,
        temp_audiofile="temp-audio.m4a",
        remove_temp=True,
        verbose=True,
        logger="bar",
    )
    print(f"Видео успешно создано: {output_filename}")
except Exception as e:
    print(f"Ошибка при экспорте видео: {e}")
    # Попробуем альтернативный метод экспорта
    print("Попытка экспорта с упрощенными настройками...")
    try:
        video.write_videofile(output_filename, codec="libx264", audio=False)
        print(f"Видео создано с упрощенными настройками: {output_filename}")
    except Exception as e2:
        print(f"Не удалось создать видео: {e2}")

print("Программа завершена!")
print("Текст был загружен из файла: starwars_crawl.txt")
print(f"Длительность видео: {DURATION} секунд")
print(f"Разрешение: {WIDTH}x{HEIGHT}")
print(f"FPS: {FPS}")
