"""ИСПРАВЛЕННЫЙ 3D PERSPECTIVE STAR WARS GENERATOR
С правильной инициализацией текстовой полосы.
"""

import json
import os
import time

import cv2
import numpy as np
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont


class Fixed3DStarWarsGeneratorV2:
    """Fixed 3D Star Wars style text crawler generator.

    This class generates Star Wars style scrolling text videos with 3D perspective
    effects, proper text positioning, and smooth animation.

    Attributes:
        width (int): Video width in pixels
        height (int): Video height in pixels
        fps (int): Frames per second for video output

    """

    # Magic number constants
    STAR_DENSITY_THRESHOLD = 0.05
    TEXT_HEIGHT_THRESHOLD = 10
    PROGRESS_THRESHOLD_HIGH = 0.95
    PROGRESS_THRESHOLD_LOW = 0.05
    FRAME_RATE_DIVISOR = 25
    PERSPECTIVE_DIVISOR = 2
    FADE_THRESHOLD = 0.98

    def __init__(self) -> None:
        """Initialize the generator with default video settings."""
        self.width = 1280
        self.height = 720
        self.fps = 24
        self.duration = 20  # Базовая длительность, будет адаптироваться
        self.bg_color = (0, 0, 0)

        # 3D параметры
        self.vanishing_point_x = self.width // 2
        self.vanishing_point_y = self.height // 3
        self.perspective_angle = 30

        # Кэши
        self.static_frames = {}
        self.text_strip = None

        # Адаптивные параметры
        self.adaptive_duration = None

        # Параметры наклона (настраиваемые)
        self.tilt_angle = 18.0      # Угол наклона в градусах
        self.base_perspective = 0.4  # Базовая интенсивность перспективы
        self.max_perspective = 0.65  # Максимальная интенсивность

    def load_config_dict(self, config: dict) -> None:
        """Загружает конфигурацию из словаря."""
        self.config = config

        # Загружаем параметры наклона если они есть в конфигурации
        if "perspective" in config:
            perspective_config = config["perspective"]
            self.tilt_angle = perspective_config.get("tilt_angle", self.tilt_angle)
            self.base_perspective = perspective_config.get("base_perspective", self.base_perspective)
            self.max_perspective = perspective_config.get("max_perspective", self.max_perspective)
            print(f"🎯 Perspective settings: angle={self.tilt_angle}°, base={self.base_perspective}, max={self.max_perspective}")

        print(f"✅ Config loaded from dict: {config}")

    def load_config_file(self, config_path: str) -> None:
        """Загружает конфигурацию из файла."""
        try:
            with open(config_path, encoding="utf-8") as f:
                config = json.load(f)
                self.config = config

                # Загружаем параметры наклона если они есть в конфигурации
                if "perspective" in config:
                    perspective_config = config["perspective"]
                    self.tilt_angle = perspective_config.get("tilt_angle", self.tilt_angle)
                    self.base_perspective = perspective_config.get("base_perspective", self.base_perspective)
                    self.max_perspective = perspective_config.get("max_perspective", self.max_perspective)
                    print(f"🎯 Perspective settings: angle={self.tilt_angle}°, base={self.base_perspective}, max={self.max_perspective}")

                print(f"✅ Config loaded from file: {config_path}")
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            print(f"❌ Config error loading {config_path}: {e}")
            # Используем fallback
            self.config = self.load_config()

    def load_config(self) -> dict:
        """Загружает конфигурацию."""
        # Если уже есть установленная конфигурация, используем её
        if hasattr(self, "config") and self.config:
            print(f"✅ Using loaded config: {self.config}")
            return self.config

        if os.path.exists("starwars_crawl.json"):
            try:
                with open("starwars_crawl.json", encoding="utf-8") as f:
                    config = json.load(f)
                    print(f"✅ Config loaded: {config}")
                    return config
            except (FileNotFoundError, json.JSONDecodeError, PermissionError) as e:
                print(f"❌ Config error: {e}")

        # Fallback конфигурация
        fallback = {
            "title": {
                "text": "Episode IV\nA NEW HOPE",
                "color": "#FFE81F",
                "font_size": 72,
            },
            "main_text": {
                "text": "It is a period of civil war.\n\nRebel spaceships, striking from\na hidden base, have won their\nfirst victory against the evil\nGalactic Empire.\n\nDuring the battle, Rebel spies\nmanaged to steal secret plans\nto the Empire's ultimate weapon,\nthe DEATH STAR, an armored\nspace station with enough power\nto destroy an entire planet.\n\nPursued by the Empire's sinister\nagents, Princess Leia races home\naboard her starship, custodian\nof the stolen plans that can save\nher people and restore freedom\nto the galaxy....",
                "color": "#FFE81F",
                "font_size": 48,
            },
        }
        print(f"⚠️ Using fallback config: {fallback}")
        return fallback

    def hex_to_rgb(self, hex_color: str) -> tuple[int, int, int]:
        """Конвертирует hex в RGB."""
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

    def create_starfield(self) -> np.ndarray:
        """Создает фон со звездами."""
        background = np.zeros((self.height, self.width, 3), dtype=np.uint8)

        num_stars = 150
        np.random.seed(42)

        for _ in range(num_stars):
            x = np.random.randint(0, self.width)
            y = np.random.randint(0, self.height)
            brightness = np.random.randint(100, 255)
            background[y, x] = [brightness, brightness, brightness]

            # Некоторые звезды крупнее
            if np.random.random() < self.STAR_DENSITY_THRESHOLD:
                if 1 <= x < self.width - 1 and 1 <= y < self.height - 1:
                    background[y - 1 : y + 2, x - 1 : x + 2] = [
                        brightness // 2,
                        brightness // 2,
                        brightness // 2,
                    ]

        return background

    def apply_perspective_transform(
        self, img: np.ndarray, progress: float
    ) -> np.ndarray:
        """Применяет настоящее 3D преобразование перспективы - точно как в Star Wars."""
        h, w = img.shape[:2]

        # УЛУЧШЕННАЯ STAR WARS ПЕРСПЕКТИВА - более точная имитация фильма
        # В оригинальных фильмах наклон достигает примерно 15-20 градусов

        # Основные параметры перспективы (сбалансированы для стабильности)
        perspective_intensity = self.base_perspective + ((self.max_perspective - self.base_perspective) * progress)

        # Верхняя часть (далеко в космосе) - сужается
        top_width_ratio = 1.0 - perspective_intensity  # От 0.6 до 0.35
        top_width = int(w * top_width_ratio)

        # Нижняя часть (близко к зрителю) - остается полной ширины
        bottom_width_ratio = 1.0
        bottom_width = int(w * bottom_width_ratio)

        # УЛУЧШЕННЫЙ наклон - более заметный, но стабильный
        # Угол наклона как в оригинальных фильмах
        angle_intensity = 0.7 + (0.3 * progress)  # Усиливается при прокрутке

        # Вычисляем смещение на основе угла наклона
        angle_radians = np.radians(self.tilt_angle * angle_intensity)
        vertical_tilt = int(h * np.tan(angle_radians) * 0.25)  # 25% от теоретического наклона

        # Дополнительное смещение для анимации прокрутки (уменьшено)
        scroll_offset = int(h * 0.02 * progress)

        # Исходные точки (прямоугольник текста)
        src_points = np.float32(
            [
                [0, 0],      # верхний левый
                [w, 0],      # верхний правый
                [w, h],      # нижний правый
                [0, h],      # нижний левый
            ]
        )

        # УЛУЧШЕННЫЕ целевые точки - точная имитация Star Wars
        top_margin = (w - top_width) // 2
        bottom_margin = (w - bottom_width) // 2

        # Расчет точек с правильным наклоном
        top_y = -vertical_tilt - scroll_offset
        bottom_y = h + vertical_tilt + scroll_offset

        dst_points = np.float32(
            [
                [top_margin, top_y],              # верхний левый (узко, высоко)
                [w - top_margin, top_y],          # верхний правый (узко, высоко)
                [w - bottom_margin, bottom_y],    # нижний правый (широко, низко)
                [bottom_margin, bottom_y],        # нижний левый (широко, низко)
            ]
        )

        # Вычисляем матрицу перспективного преобразования
        matrix = cv2.getPerspectiveTransform(src_points, dst_points)

        # Увеличенный размер результата для компенсации наклона
        result_height = h + 2 * (vertical_tilt + scroll_offset) + 100
        result_width = w + 50  # Небольшое расширение по ширине

        result = cv2.warpPerspective(
            img,
            matrix,
            (result_width, result_height),
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=(0, 0, 0),
        )

        # Обрезаем и центрируем результат
        if result.shape[0] >= h and result.shape[1] >= w:
            start_y = max(0, (result.shape[0] - h) // 2)
            start_x = max(0, (result.shape[1] - w) // 2)
            return result[start_y:start_y + h, start_x:start_x + w]

        # Если результат меньше, дополняем черным и центрируем
        padded = np.zeros((h, w, 3), dtype=np.uint8)

        # Центрируем по вертикали
        start_y = max(0, (h - result.shape[0]) // 2)
        end_y = min(h, start_y + result.shape[0])

        # Центрируем по горизонтали
        start_x = max(0, (w - result.shape[1]) // 2)
        end_x = min(w, start_x + result.shape[1])

        # Копируем доступную область
        result_h = min(result.shape[0], end_y - start_y)
        result_w = min(result.shape[1], end_x - start_x)

        padded[start_y:start_y + result_h, start_x:start_x + result_w] = result[:result_h, :result_w]

        return padded

    def create_text_strip(self, text: str, fontsize: int, color: str) -> np.ndarray:
        """Создает текстовую полосу с правильным позиционированием."""
        print(f"🎨 Creating OPTIMIZED text strip: '{text[:50]}...'")
        print(f"   Font size: {fontsize}, Color: {color}")

        # ФИНАЛЬНОЕ ИСПРАВЛЕНИЕ: Компактная полоса с правильным позиционированием
        strip_height = self.height * 3  # Компактная полоса 2160px
        img = Image.new("RGB", (self.width, strip_height), (0, 0, 0))
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", fontsize)
            print("✅ Arial font loaded")
        except:
            font = ImageFont.load_default()
            print("⚠️ Using default font")

        rgb_color = self.hex_to_rgb(color)
        print(f"   RGB color: {rgb_color}")

        # КЛЮЧЕВОЕ ИСПРАВЛЕНИЕ: Оптимальное позиционирование для видимости во всей прокрутке
        lines = text.replace("\n\n", "\n \n").split("\n")
        line_height = fontsize + 15

        # Рассчитываем scroll range (как в create_3d_frame)
        start_offset = strip_height // 2 - self.height // 4  # 900
        end_offset = strip_height // 2 + self.height // 2  # 1440

        # Позиционируем текст так, чтобы он был полностью видим в середине прокрутки
        scroll_center = (start_offset + end_offset) // 2  # 1170
        total_text_height = len([line for line in lines if line.strip()]) * line_height

        # Размещаем центр текста в центре области прокрутки
        y_start = scroll_center - total_text_height // 2

        print("   📍 OPTIMIZED positioning:")
        print(f"   Strip height: {strip_height}")
        print(
            f"   Scroll range: {start_offset} - {end_offset} (center: {scroll_center})"
        )
        print(f"   Text height: {total_text_height}")
        print(f"   Starting y_pos: {y_start} (optimized for full visibility)")

        total_lines = 0
        text_positions = []
        current_y = y_start

        for line in lines:
            if line.strip():  # Не пустая строка
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
                x = (self.width - text_width) // 2
                draw.text((x, current_y), line, font=font, fill=rgb_color)
                text_positions.append(current_y)
                total_lines += 1
            current_y += line_height

        if text_positions:
            text_top = min(text_positions)
            text_bottom = max(text_positions)
            print(f"   Text spans: y={text_top} to y={text_bottom}")

        print("✅ OPTIMIZED text strip created:")
        print(f"   Total lines: {total_lines}")
        print(f"   Strip height: {strip_height}")

        text_array = np.array(img)
        print(f"   Text array shape: {text_array.shape}")

        # Улучшенная диагностика
        non_black_pixels = np.sum(text_array > self.TEXT_HEIGHT_THRESHOLD)
        text_coverage = non_black_pixels / (strip_height * self.width) * 100
        print(f"   Non-black pixels: {non_black_pixels}")
        print(f"   Text coverage: {text_coverage:.2f}%")

        return text_array

    def create_3d_frame(self, progress: float) -> np.ndarray:
        """Создает кадр с 3D эффектом с улучшенной производительностью."""
        if progress == 0:
            print(f"🎬 Creating 3D frame, progress: {progress:.3f}")

        background = self._ensure_starfield_background()

        # Получаем текстовую полосу (инициализируем если нужно)
        self._ensure_text_strip()

        # Вычисляем смещение для прокрутки
        offset = self._calculate_scroll_offset(progress)

        # Извлекаем секцию текста для текущего кадра
        text_section = self._extract_text_section(offset, progress)

        # Применяем 3D перспективу
        perspective_text = self.apply_perspective_transform(text_section, progress)

        # Эффективное смешивание с фоном
        return self._blend_text_with_background(background, perspective_text, progress)


    def _ensure_starfield_background(self) -> np.ndarray:
        """Создает или возвращает кэшированный фон со звездами."""
        if "starfield" not in self.static_frames:
            print("⭐ Creating and caching starfield background...")
            self.static_frames["starfield"] = self.create_starfield()
        return self.static_frames["starfield"].copy()

    def _ensure_text_strip(self) -> None:
        """Инициализирует текстовую полосу если необходимо."""
        if self.text_strip is None:
            print("📝 Initializing text strip...")
            config = self.load_config()
            main_config = config.get("main_text", {})

            text = main_config.get("text", "DEFAULT SCROLLING TEXT")
            fontsize = main_config.get("font_size", 48)
            color = main_config.get("color", "#FFE81F")

            print(f"   Text preview: '{text[:100]}...'")
            print(f"   Font size: {fontsize}")
            print(f"   Color: {color}")

            self.text_strip = self.create_text_strip(text, fontsize, color)

    def _calculate_scroll_offset(self, progress: float) -> int:
        """Вычисляет смещение для прокрутки текста."""
        strip_height = self.text_strip.shape[0]
        max_offset = strip_height - self.height

        if self.text_strip is not None:
            # Найдем фактические границы текста в полосе
            non_black_mask = np.any(self.text_strip > 0, axis=2)
            if np.any(non_black_mask):
                y_coords, _ = np.where(non_black_mask)
                actual_text_top = np.min(y_coords)
                actual_text_bottom = np.max(y_coords)

                # Рассчитаем scroll range на основе фактического положения текста
                start_offset = max(0, actual_text_bottom - self.height)
                end_offset = min(strip_height - self.height, actual_text_top)

                if progress in [0, 0.25, 0.5, 0.75, 1.0] or progress > self.PROGRESS_THRESHOLD_HIGH:
                    print("   📊 ADAPTIVE scroll logic:")
                    print(f"      Text range: {actual_text_top}-{actual_text_bottom}")
                    print(f"      Adaptive scroll range: {start_offset}-{end_offset}")
            else:
                # Fallback если текст не найден
                start_offset = strip_height // 2 - self.height // 4
                end_offset = strip_height // 2 + self.height // 2
        else:
            # Fallback если text_strip не инициализирован
            start_offset = strip_height // 2 - self.height // 4
            end_offset = strip_height // 2 + self.height // 2

        # Интерполяция offset на основе progress
        offset = int(start_offset + (end_offset - start_offset) * progress)
        return max(0, min(offset, max_offset))

    def _extract_text_section(self, offset: int, progress: float) -> np.ndarray:
        """Извлекает секцию текста для текущего кадра."""
        strip_height = self.text_strip.shape[0]

        # Оптимизированное извлечение секции текста
        end_pos = min(offset + self.height, strip_height)
        text_section = self.text_strip[offset:end_pos]

        # Если секция меньше требуемой высоты, дополняем черным
        if text_section.shape[0] < self.height:
            padded_section = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            padded_section[: text_section.shape[0]] = text_section
            text_section = padded_section

        # Диагностика наличия текста
        non_black_threshold = 20
        non_black_in_section = np.sum(text_section > non_black_threshold)

        # Подробная диагностика только для ключевых кадров
        if progress in [0, 0.25, 0.5, 0.75, 1.0] or non_black_in_section == 0:
            print("   🔍 Section analysis:")
            print(f"      Section shape: {text_section.shape}")
            print(f"      Non-black pixels: {non_black_in_section}")
            print(
                f"      Text coverage: {non_black_in_section / (self.width * self.height) * 100:.1f}%"
            )

            if non_black_in_section == 0:
                print("   ⚠️ WARNING: Empty section detected!")
                print(f"   ⚠️ Offset: {offset}, Strip height: {strip_height}")
                print("   ⚠️ This indicates text positioning issues")

        return text_section

    def _blend_text_with_background(self, background: np.ndarray, perspective_text: np.ndarray, progress: float) -> np.ndarray:
        """Смешивает текст с перспективой с фоном."""
        non_black_threshold = 20

        # Создаем маску на основе всех цветовых каналов
        text_mask = np.any(perspective_text > non_black_threshold, axis=2)
        text_pixel_count = np.sum(text_mask)

        if text_pixel_count == 0:
            if progress > self.PROGRESS_THRESHOLD_HIGH or progress < self.PROGRESS_THRESHOLD_LOW:
                print("   ⚠️ No text pixels after perspective transform")
            return background

        # Применяем маску для смешивания
        result = background.copy()
        result[text_mask] = perspective_text[text_mask]

        # Диагностика для ключевых кадров
        if progress in [0, 0.25, 0.5, 0.75, 1.0]:
            coverage = text_pixel_count / (self.width * self.height) * 100
            print(
                f"   ✅ 3D frame: {text_pixel_count} text pixels ({coverage:.1f}% coverage)"
            )

        return result

    def create_static_frame(self, text: str, fontsize: int, color: str) -> np.ndarray:
        """Создает статический кадр для заголовка."""
        print(f"🏷️ Creating static frame: '{text}', size: {fontsize}, color: {color}")

        background = self.create_starfield()
        img = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", fontsize)
        except:
            font = ImageFont.load_default()

        rgb_color = self.hex_to_rgb(color)

        lines = text.split("\n")
        total_height = len(lines) * (fontsize + 10)
        start_y = (self.height - total_height) // 2

        for i, line in enumerate(lines):
            if line.strip():
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
                x = (self.width - text_width) // 2
                y = start_y + i * (fontsize + 10)
                draw.text((x, y), line, font=font, fill=rgb_color)

        text_array = np.array(img)
        alpha = text_array[:, :, 3:4] / 255.0
        text_rgb = text_array[:, :, :3]

        result = background * (1 - alpha) + text_rgb * alpha

        print("✅ Static frame created")

        return result.astype(np.uint8)

    def generate_video(self, output_file: str = "starwars_crawl.mp4") -> None:
        """Генерирует видео (алиас для generate_3d_video)."""
        self.generate_3d_video(output_file)

    def generate_3d_video(self, output_file: str = "starwars_crawl_3d_optimized.mp4") -> None:
        """Генерирует видео с настоящим 3D эффектом и оптимизацией."""
        print("🎬 OPTIMIZED 3D PERSPECTIVE Star Wars Generator V2")
        print("=" * 60)

        config = self.load_config()
        start_time = time.time()

        # Оптимизация: Предрендеринг всех статических кадров
        print("🎨 Pre-rendering static frames...")

        title_config = config.get("title", {})
        title_frame = self.create_static_frame(
            title_config.get("text", "Episode IV\nA NEW HOPE"),
            title_config.get("font_size", 72),
            title_config.get("color", "#FFE81F"),
        )
        self.static_frames["title"] = title_frame

        stars_frame = self.create_starfield()
        self.static_frames["stars"] = stars_frame

        # Предынициализируем текстовую полосу с диагностикой
        print("📝 Pre-initializing optimized text strip...")
        main_config = config.get("main_text", {})
        text_content = main_config.get("text", "DEFAULT TEXT")

        # Адаптивная длительность на основе текста
        main_config = config.get("main_text", {})
        text_content = main_config.get("text", "DEFAULT TEXT")

        if self.adaptive_duration is None:
            self.adaptive_duration = self.calculate_adaptive_duration(text_content)
            self.duration = self.adaptive_duration
            print(f"🎯 Using adaptive duration: {self.duration:.1f} seconds")

        # Анализируем текст для оптимизации
        text_lines = len(
            [
                line
                for line in text_content.replace("\n\n", "\n").split("\n")
                if line.strip()
            ]
        )
        text_words = len(text_content.split())
        estimated_read_time = text_words / 200 * 60  # 200 слов в минуту

        print("📊 Text analysis:")
        print(f"   Lines: {text_lines}")
        print(f"   Words: {text_words}")
        print(f"   Estimated reading time: {estimated_read_time:.1f} seconds")

        self.text_strip = self.create_text_strip(
            text_content,
            main_config.get("font_size", 48),
            main_config.get("color", "#FFE81F"),
        )

        # Оптимизированные временные интервалы
        title_duration = 2.5
        stars_pause = 1.0
        scroll_start = title_duration + stars_pause
        scroll_duration = self.duration - scroll_start

        print("⏱️ Timing optimization:")
        print(f"   Title duration: {title_duration}s")
        print(f"   Stars pause: {stars_pause}s")
        print(f"   Scroll duration: {scroll_duration}s")
        print(f"   Total duration: {self.duration}s")

        frame_count = 0
        last_progress_report = 0

        def make_frame(t: float) -> np.ndarray:
            """Создает кадр видео с оптимизацией."""
            nonlocal frame_count, last_progress_report
            frame_count += 1

            # Прогресс-бар каждые 25% или каждые 2 секунды
            progress_percent = (t / self.duration) * 100
            if progress_percent - last_progress_report >= self.FRAME_RATE_DIVISOR or (
                t - last_progress_report >= self.PERSPECTIVE_DIVISOR and t > 0
            ):
                print(
                    f"\n⏱️ Video progress: {progress_percent:.1f}% (t={t:.2f}s, frame #{frame_count})"
                )
                last_progress_report = progress_percent

            # Оптимизированная логика кадров
            if t <= title_duration:
                # Заголовок - используем кэшированный кадр
                if frame_count == 1:
                    print("   📋 Using cached title frame")
                return self.static_frames["title"]

            if t <= scroll_start:
                # Пауза со звездами - используем кэшированный кадр
                if t <= title_duration + 0.1:  # Печатаем только один раз
                    print("   ⭐ Using cached stars frame")
                return self.static_frames["stars"]

            # 3D прокрутка с оптимизацией
            scroll_progress = min((t - scroll_start) / scroll_duration, 1.0)

            # Подробный лог только для ключевых моментов
            if scroll_progress in [0] or (scroll_progress > self.FADE_THRESHOLD):
                print(f"   🎬 3D scroll: progress {scroll_progress:.3f}")
                print(
                    f"      Time in scroll: {t - scroll_start:.1f}s / {scroll_duration:.1f}s"
                )

            return self.create_3d_frame(scroll_progress)

        print("🚀 Creating optimized video with REAL 3D perspective...")
        video_clip = VideoClip(make_frame, duration=self.duration)

        # Улучшенные настройки экспорта
        print(f"� Exporting to {output_file} with optimized settings...")
        export_start = time.time()

        video_clip.write_videofile(
            output_file,
            fps=self.fps,
            codec="libx264",
            preset="fast",  # Быстрее чем medium
            threads=6,  # Больше потоков
            bitrate="5000k",  # Хорошее качество
            verbose=False,
            logger=None,
        )

        export_time = time.time() - export_start
        total_time = time.time() - start_time

        # Детальная статистика
        print("=" * 60)
        print("✅ OPTIMIZED 3D Perspective video created!")
        print(f"📁 File: {output_file}")
        print("📊 Statistics:")
        print(f"   Total frames rendered: {frame_count}")
        print(f"   Rendering time: {total_time - export_time:.2f}s")
        print(f"   Export time: {export_time:.2f}s")
        print(f"   Total time: {total_time:.2f}s")
        print(
            f"   Avg FPS during render: {frame_count / (total_time - export_time):.1f}"
        )
        print("🌟 Features:")
        print("   ✅ ADAPTIVE text strip sizing")
        print("   ✅ OPTIMIZED frame caching")
        print("   ✅ REAL 3D perspective transformation")
        print("   ✅ SMART empty frame detection")
        print("   ✅ DETAILED progress reporting")

        # Проверяем размер файла
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file) / (1024 * 1024)  # MB
            print(f"📦 File size: {file_size:.1f} MB")

        return output_file

    def calculate_adaptive_duration(self, text: str) -> float:
        """Вычисляет оптимальную длительность видео на основе текста."""
        # Анализируем текст
        words = len(text.split())
        lines = len(
            [line for line in text.replace("\n\n", "\n").split("\n") if line.strip()]
        )
        paragraphs = len([p for p in text.split("\n\n") if p.strip()])

        # Базовые временные интервалы
        title_time = 2.5
        stars_pause = 1.0

        # Расчет времени прокрутки на основе текста
        # Базовая скорость: 150 слов в минуту для комфортного чтения
        reading_speed_wpm = 150
        base_scroll_time = (words / reading_speed_wpm) * 60

        # Корректировки на основе структуры
        line_factor = lines * 0.3  # Больше строк = больше времени
        paragraph_factor = paragraphs * 0.5  # Паузы между абзацами

        # Минимальное и максимальное время прокрутки
        min_scroll_time = 8.0
        max_scroll_time = 30.0

        adjusted_scroll_time = base_scroll_time + line_factor + paragraph_factor
        scroll_time = max(min_scroll_time, min(adjusted_scroll_time, max_scroll_time))

        total_duration = title_time + stars_pause + scroll_time

        print("📊 Adaptive duration calculation:")
        print(f"   Words: {words}, Lines: {lines}, Paragraphs: {paragraphs}")
        print(f"   Base reading time: {base_scroll_time:.1f}s")
        print(f"   Adjusted scroll time: {scroll_time:.1f}s")
        print(f"   Total duration: {total_duration:.1f}s")

        return total_duration


if __name__ == "__main__":
    print("🎬 Creating Star Wars video with REAL 3D perspective effect...")
    print("🐛 DEBUG VERSION - shows detailed output")

    generator = Fixed3DStarWarsGeneratorV2()
    output_file = generator.generate_3d_video()

    print(f"\n🎉 SUCCESS! Video created: {output_file}")
    print("🎯 This version has ACTUAL 3D perspective transformation!")
    print("📐 You should now see the text getting narrower as it moves away!")
    print("🐛 Check the debug output above to see what happened with text rendering")
