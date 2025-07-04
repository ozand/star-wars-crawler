# Developer Guide: Star Wars Text Perspective System

**Версия:** 2.0  
**Дата обновления:** 3 июля 2025  
**Для разработчиков:** Архитектура, API, расширение функциональности

---

## 📋 Содержание

1. [Архитектура системы](#архитектура-системы)
2. [Система перспективы](#система-перспективы)
3. [API Reference](#api-reference)
4. [Расширение функциональности](#расширение-функциональности)
5. [Алгоритмы и математика](#алгоритмы-и-математика)
6. [Отладка и тестирование](#отладка-и-тестирование)
7. [Performance оптимизации](#performance-оптимизации)

---

## 🏗️ Архитектура системы

### Структура проекта
```
src/star_wars_generator/
├── core.py              # Основной движок генерации
├── cli.py               # Интерфейс командной строки
└── __init__.py          # Экспорт классов

examples/
├── configs/             # JSON конфигурации
└── videos/              # Результаты batch-обработки

docs/                    # Документация
tests/                   # Тесты (планируется)
output/                  # Вывод по умолчанию
```

### Основные компоненты

#### 1. `Fixed3DStarWarsGeneratorV2` (core.py)
**Назначение:** Основной класс для генерации видео с 3D перспективой

**Ключевые атрибуты:**
```python
# Базовые параметры видео
self.width = 1280          # Ширина кадра
self.height = 720          # Высота кадра  
self.fps = 24              # Частота кадров
self.duration = 20         # Базовая длительность

# Параметры перспективы (настраиваемые)
self.tilt_angle = 18.0           # Угол наклона в градусах
self.base_perspective = 0.4      # Минимальная интенсивность перспективы
self.max_perspective = 0.65      # Максимальная интенсивность

# 3D параметры (фиксированные)
self.vanishing_point_x = self.width // 2   # Точка схода по X
self.vanishing_point_y = self.height // 3  # Точка схода по Y

# Кэши для оптимизации
self.static_frames = {}    # Кэш статических кадров
self.text_strip = None     # Предварительно созданная текстовая полоса
```

#### 2. `StarWarsCLI` (cli.py)
**Назначение:** Интерфейс командной строки и управление конфигурациями

**Основные методы:**
- `create_video_from_config()` - создание из JSON конфигурации
- `create_video_from_text()` - создание из текста напрямую
- `resolve_output_path()` - обработка путей вывода
- `list_themes()` - просмотр доступных тем

---

## 🎯 Система перспективы

### Математическая модель

Система использует **перспективное преобразование OpenCV** для создания эффекта глубины:

```python
def apply_perspective_transform(self, img: np.ndarray, progress: float) -> np.ndarray:
    """
    Применяет 3D перспективное преобразование
    
    Args:
        img: Исходное изображение текста
        progress: Прогресс анимации (0.0-1.0)
    
    Returns:
        Трансформированное изображение с перспективой
    """
```

### Ключевые параметры

#### `tilt_angle` (Угол наклона)
```python
# Диапазон: 5-30 градусов
# По умолчанию: 18.0
# Рекомендуется: 22.0 для Star Wars

angle_radians = np.radians(self.tilt_angle * angle_intensity)
vertical_tilt = int(h * np.tan(angle_radians) * 0.25)
```

**Влияние на результат:**
- 10-15° → Слабая перспектива (субтитры, документальные)
- 18-22° → Стандартная перспектива (Star Wars классика)
- 25-30° → Сильная перспектива (эпические сцены)
- 30°+ → Критическая зона (возможна потеря текста)

#### `base_perspective` (Минимальная интенсивность)
```python
# Диапазон: 0.0-1.0
# По умолчанию: 0.4
# Контролирует сужение в начале

top_width_ratio = 1.0 - perspective_intensity
top_width = int(w * top_width_ratio)
```

#### `max_perspective` (Максимальная интенсивность)
```python
# Диапазон: 0.0-1.0  
# По умолчанию: 0.65
# Контролирует максимальное сужение

perspective_intensity = self.base_perspective + 
    ((self.max_perspective - self.base_perspective) * progress)
```

### Алгоритм трансформации

```python
# 1. Вычисление интенсивности перспективы
perspective_intensity = base + ((max - base) * progress)

# 2. Расчёт ширины верхней и нижней части
top_width = w * (1.0 - perspective_intensity)     # Сужается
bottom_width = w * 1.0                            # Остаётся полной

# 3. Вычисление наклона
angle_radians = np.radians(tilt_angle * angle_intensity)
vertical_tilt = h * np.tan(angle_radians) * 0.25

# 4. Создание матрицы перспективного преобразования
src_points = [[0,0], [w,0], [w,h], [0,h]]        # Исходный прямоугольник
dst_points = [
    [top_margin, -vertical_tilt],                  # Верхний левый (узко, высоко)
    [w-top_margin, -vertical_tilt],                # Верхний правый
    [w-bottom_margin, h+vertical_tilt],            # Нижний правый (широко, низко)
    [bottom_margin, h+vertical_tilt]               # Нижний левый
]

matrix = cv2.getPerspectiveTransform(src_points, dst_points)
result = cv2.warpPerspective(img, matrix, output_size)
```

---

## 🔧 API Reference

### Основной класс

```python
class Fixed3DStarWarsGeneratorV2:
    def __init__(self):
        """Инициализация генератора с настройками по умолчанию"""
        
    def load_config_dict(self, config: dict) -> None:
        """
        Загружает конфигурацию из словаря
        
        Args:
            config: Словарь с параметрами конфигурации
            
        Example:
            config = {
                "perspective": {
                    "tilt_angle": 22.0,
                    "base_perspective": 0.45,
                    "max_perspective": 0.72
                }
            }
            generator.load_config_dict(config)
        """
        
    def load_config_file(self, config_path: str) -> None:
        """
        Загружает конфигурацию из JSON файла
        
        Args:
            config_path: Путь к JSON файлу конфигурации
        """
        
    def generate_video(self, output_path: str) -> None:
        """
        Генерирует итоговое видео
        
        Args:
            output_path: Путь для сохранения MP4 файла
            
        Raises:
            Exception: При ошибках во время генерации
        """
```

### Конфигурационные структуры

#### Полная JSON конфигурация
```json
{
    "title": {
        "text": "Episode IV\\nA NEW HOPE",
        "color": "#FFE81F",
        "font_size": 72
    },
    "main_text": {
        "text": "It is a period of civil war...",
        "color": "#FFE81F", 
        "font_size": 48
    },
    "animation": {
        "duration": 25
    },
    "perspective": {
        "tilt_angle": 22.0,
        "base_perspective": 0.45,
        "max_perspective": 0.72
    },
    "video_settings": {
        "width": 1280,
        "height": 720,
        "fps": 24
    }
}
```

#### Структура perspective объекта
```python
perspective_config = {
    "tilt_angle": float,        # 5.0-30.0, угол наклона в градусах
    "base_perspective": float,  # 0.0-1.0, минимальная интенсивность
    "max_perspective": float    # 0.0-1.0, максимальная интенсивность
}
```

### CLI Интерфейс

```python
class StarWarsCLI:
    def create_video_from_config(
        self, 
        config_path: str, 
        output: Optional[str] = None,
        tilt_angle: Optional[float] = None,
        perspective_min: Optional[float] = None,
        perspective_max: Optional[float] = None
    ) -> bool:
        """
        Создает видео из конфигурации с возможностью переопределения параметров
        
        Args:
            config_path: Путь к конфигурации или имя темы
            output: Путь вывода (файл или папка)
            tilt_angle: Переопределение угла наклона
            perspective_min: Переопределение min perspective
            perspective_max: Переопределение max perspective
            
        Returns:
            True если видео создано успешно
        """
        
    def resolve_output_path(self, output: Optional[str], default_filename: str) -> Path:
        """
        Разрешает путь вывода с поддержкой папок и файлов
        
        Args:
            output: Пользовательский путь (может быть None, папкой или файлом)
            default_filename: Имя файла по умолчанию
            
        Returns:
            Полный путь к файлу вывода
            
        Example:
            resolve_output_path(None, "video.mp4")           → "output/video.mp4"
            resolve_output_path("videos/", "video.mp4")      → "videos/video.mp4"
            resolve_output_path("my_video.mp4", "video.mp4") → "my_video.mp4"
        """
```

---

## 🚀 Расширение функциональности

### Добавление новых параметров перспективы

#### 1. Расширение core.py
```python
class Fixed3DStarWarsGeneratorV2:
    def __init__(self):
        # ...existing code...
        
        # Новые параметры
        self.perspective_curve = 1.0        # Кривизна перспективы
        self.depth_intensity = 0.8          # Интенсивность глубины
        self.vanishing_offset = 0.0         # Смещение точки схода
        
    def load_config_dict(self, config: dict) -> None:
        # ...existing code...
        
        if 'perspective' in config:
            perspective_config = config['perspective']
            # ...existing parameters...
            
            # Новые параметры
            self.perspective_curve = perspective_config.get('curve', self.perspective_curve)
            self.depth_intensity = perspective_config.get('depth', self.depth_intensity)
            self.vanishing_offset = perspective_config.get('vanishing_offset', self.vanishing_offset)
```

#### 2. Интеграция в алгоритм трансформации
```python
def apply_perspective_transform(self, img: np.ndarray, progress: float) -> np.ndarray:
    # ...existing code...
    
    # Применение кривизны перспективы
    curved_progress = pow(progress, self.perspective_curve)
    perspective_intensity = self.base_perspective + (
        (self.max_perspective - self.base_perspective) * curved_progress
    )
    
    # Динамическое смещение точки схода
    dynamic_vanishing_y = self.vanishing_point_y + (self.vanishing_offset * progress)
    
    # ...rest of transformation...
```

#### 3. Добавление CLI параметров
```python
# В main() функции cli.py
parser.add_argument(
    "--perspective-curve",
    type=float,
    metavar="VALUE", 
    help="Кривизна перспективы (0.5-2.0). Пример: --perspective-curve 1.2"
)

parser.add_argument(
    "--depth-intensity", 
    type=float,
    metavar="VALUE",
    help="Интенсивность глубины (0.0-1.0). Пример: --depth-intensity 0.9"
)
```

### Добавление новых эффектов

#### Эффект затухания текста
```python
def apply_fade_effect(self, img: np.ndarray, progress: float) -> np.ndarray:
    """Применяет эффект затухания к тексту"""
    
    fade_start = 0.8  # Начало затухания (80% видео)
    
    if progress > fade_start:
        fade_progress = (progress - fade_start) / (1.0 - fade_start)
        alpha = 1.0 - fade_progress
        
        # Применение alpha канала
        img_with_alpha = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        img_with_alpha[:, :, 3] = img_with_alpha[:, :, 3] * alpha
        return img_with_alpha
    
    return img
```

#### Эффект свечения текста
```python
def apply_glow_effect(self, img: np.ndarray, intensity: float = 0.3) -> np.ndarray:
    """Добавляет эффект свечения к тексту"""
    
    # Создание размытой копии для свечения
    blurred = cv2.GaussianBlur(img, (15, 15), 0)
    
    # Смешивание оригинала и размытой версии
    glowing = cv2.addWeighted(img, 1.0, blurred, intensity, 0)
    
    return glowing
```

### Создание пресетов

```python
class PerspectivePresets:
    """Предустановленные наборы параметров перспективы"""
    
    SUBTITLES = {
        "tilt_angle": 12.0,
        "base_perspective": 0.3,
        "max_perspective": 0.5
    }
    
    DOCUMENTARY = {
        "tilt_angle": 15.0,
        "base_perspective": 0.35,
        "max_perspective": 0.55
    }
    
    STAR_WARS_CLASSIC = {
        "tilt_angle": 22.0,
        "base_perspective": 0.45,
        "max_perspective": 0.72
    }
    
    EPIC_TRAILER = {
        "tilt_angle": 25.0,
        "base_perspective": 0.5,
        "max_perspective": 0.8
    }
    
    @classmethod
    def get_preset(cls, preset_name: str) -> dict:
        """Получить пресет по имени"""
        return getattr(cls, preset_name.upper(), cls.STAR_WARS_CLASSIC)
```

---

## 🧮 Алгоритмы и математика

### Математическая модель перспективы

#### Формула перспективного сужения
```
top_width = base_width × (1 - perspective_intensity)
bottom_width = base_width × 1.0

где perspective_intensity = base + (max - base) × progress
```

#### Расчёт вертикального наклона
```
vertical_offset = height × tan(angle_radians) × damping_factor

где:
- angle_radians = tilt_angle × π / 180 × angle_intensity
- damping_factor = 0.25 (для стабильности)
- angle_intensity = 0.7 + 0.3 × progress
```

#### Матрица перспективного преобразования
```
src = [[0,0], [w,0], [w,h], [0,h]]

dst = [
    [(w-top_w)/2, -v_tilt],      # Верхний левый
    [(w+top_w)/2, -v_tilt],      # Верхний правый  
    [w, h+v_tilt],               # Нижний правый
    [0, h+v_tilt]                # Нижний левый
]

M = getPerspectiveTransform(src, dst)
```

### Алгоритм адаптивной длительности

```python
def calculate_adaptive_duration(self, text: str) -> float:
    """
    Автоматически рассчитывает оптимальную длительность
    на основе количества текста
    """
    
    words = len(text.split())
    lines = text.count('\n') + 1
    paragraphs = text.count('\n\n') + 1
    
    # Базовое время чтения (200 WPM)
    reading_time = words / 200 * 60
    
    # Коэффициенты для прокрутки
    scroll_multiplier = 1.3 + (lines * 0.02) + (paragraphs * 0.1)
    scroll_time = reading_time * scroll_multiplier
    
    # Добавляем время на заголовок и паузы
    total_time = 2.5 + 1.0 + scroll_time  # title + pause + scroll
    
    return max(15.0, min(60.0, total_time))  # Ограничения: 15-60 сек
```

### Оптимизация производительности

#### Кэширование статических кадров
```python
def create_static_frame(self, text: str, fontsize: int, color: str) -> np.ndarray:
    """Создает и кэширует статический кадр"""
    
    cache_key = f"{text}_{fontsize}_{color}"
    
    if cache_key in self.static_frames:
        return self.static_frames[cache_key]
    
    # Создание кадра
    frame = self._generate_static_frame(text, fontsize, color)
    
    # Кэширование
    self.static_frames[cache_key] = frame
    
    return frame
```

#### Предварительная инициализация текстовой полосы
```python
def pre_initialize_text_strip(self, config: dict) -> None:
    """Предварительно создает текстовую полосу для ускорения рендеринга"""
    
    main_text = config['main_text']
    self.text_strip = self.create_text_strip(
        main_text['text'], 
        main_text['font_size'], 
        main_text['color']
    )
    
    print("📝 Text strip pre-initialized for faster rendering")
```

---

## 🐛 Отладка и тестирование

### Отладочные функции

#### Визуализация параметров перспективы
```python
def debug_perspective_params(self, progress: float) -> dict:
    """Возвращает отладочную информацию о параметрах перспективы"""
    
    perspective_intensity = self.base_perspective + (
        (self.max_perspective - self.base_perspective) * progress
    )
    
    angle_intensity = 0.7 + (0.3 * progress)
    angle_radians = np.radians(self.tilt_angle * angle_intensity)
    
    return {
        "progress": progress,
        "tilt_angle": self.tilt_angle,
        "angle_intensity": angle_intensity,
        "effective_angle": self.tilt_angle * angle_intensity,
        "perspective_intensity": perspective_intensity,
        "base_perspective": self.base_perspective,
        "max_perspective": self.max_perspective
    }
```

#### Экспорт промежуточных кадров
```python
def export_debug_frames(self, output_dir: str, frame_count: int = 10) -> None:
    """Экспортирует промежуточные кадры для анализа"""
    
    os.makedirs(output_dir, exist_ok=True)
    
    for i in range(frame_count):
        progress = i / (frame_count - 1)
        
        # Получение кадра с текущим прогрессом
        frame = self.create_3d_frame(progress)
        
        # Сохранение с отладочной информацией
        debug_info = self.debug_perspective_params(progress)
        filename = f"debug_frame_{i:03d}_progress_{progress:.2f}_angle_{debug_info['effective_angle']:.1f}.png"
        
        cv2.imwrite(os.path.join(output_dir, filename), frame)
        
        print(f"Exported: {filename}")
```

### Модульное тестирование

#### Тест параметров перспективы
```python
import unittest

class TestPerspectiveSystem(unittest.TestCase):
    
    def setUp(self):
        self.generator = Fixed3DStarWarsGeneratorV2()
    
    def test_default_parameters(self):
        """Проверка параметров по умолчанию"""
        self.assertEqual(self.generator.tilt_angle, 18.0)
        self.assertEqual(self.generator.base_perspective, 0.4)
        self.assertEqual(self.generator.max_perspective, 0.65)
    
    def test_config_loading(self):
        """Проверка загрузки конфигурации"""
        config = {
            "perspective": {
                "tilt_angle": 22.0,
                "base_perspective": 0.45,
                "max_perspective": 0.72
            }
        }
        
        self.generator.load_config_dict(config)
        
        self.assertEqual(self.generator.tilt_angle, 22.0)
        self.assertEqual(self.generator.base_perspective, 0.45)
        self.assertEqual(self.generator.max_perspective, 0.72)
    
    def test_perspective_calculation(self):
        """Проверка расчёта интенсивности перспективы"""
        debug_info = self.generator.debug_perspective_params(0.5)
        
        expected_intensity = 0.4 + ((0.65 - 0.4) * 0.5)  # 0.525
        self.assertAlmostEqual(debug_info['perspective_intensity'], expected_intensity, places=3)
    
    def test_angle_boundaries(self):
        """Проверка граничных значений углов"""
        # Минимальный угол
        self.generator.tilt_angle = 5.0
        debug_info = self.generator.debug_perspective_params(1.0)
        self.assertGreater(debug_info['effective_angle'], 0)
        
        # Максимальный безопасный угол  
        self.generator.tilt_angle = 30.0
        debug_info = self.generator.debug_perspective_params(1.0)
        self.assertLess(debug_info['effective_angle'], 35.0)
```

#### Интеграционные тесты
```python
class TestVideoGeneration(unittest.TestCase):
    
    def test_video_creation(self):
        """Тест создания видео с разными параметрами"""
        generator = Fixed3DStarWarsGeneratorV2()
        
        test_configs = [
            {"tilt_angle": 10.0, "base_perspective": 0.3, "max_perspective": 0.5},
            {"tilt_angle": 22.0, "base_perspective": 0.45, "max_perspective": 0.72},
            {"tilt_angle": 25.0, "base_perspective": 0.5, "max_perspective": 0.8}
        ]
        
        for i, params in enumerate(test_configs):
            config = {
                "title": {"text": f"Test {i}", "color": "#FFE81F", "font_size": 72},
                "main_text": {"text": "Test text", "color": "#FFE81F", "font_size": 48},
                "perspective": params
            }
            
            generator.load_config_dict(config)
            output_path = f"test_output_{i}.mp4"
            
            # Проверяем что видео создается без ошибок
            try:
                generator.generate_video(output_path)
                self.assertTrue(os.path.exists(output_path))
            finally:
                if os.path.exists(output_path):
                    os.remove(output_path)
```

---

## ⚡ Performance оптимизации

### Профилирование производительности

```python
import time
import cProfile
import pstats

def profile_video_generation():
    """Профилирование генерации видео"""
    
    def generate_test_video():
        generator = Fixed3DStarWarsGeneratorV2()
        generator.generate_video("profile_test.mp4")
    
    # Профилирование с cProfile
    pr = cProfile.Profile()
    pr.enable()
    
    start_time = time.time()
    generate_test_video()
    end_time = time.time()
    
    pr.disable()
    
    # Анализ результатов
    stats = pstats.Stats(pr)
    stats.sort_stats('cumulative')
    stats.print_stats(20)  # Топ 20 функций
    
    print(f"Total generation time: {end_time - start_time:.2f} seconds")
```

### Оптимизация памяти

```python
class MemoryOptimizedGenerator(Fixed3DStarWarsGeneratorV2):
    """Версия с оптимизацией памяти для больших проектов"""
    
    def __init__(self):
        super().__init__()
        self.max_cache_size = 50  # Максимум кэшированных кадров
        self.cache_access_count = {}
        
    def create_static_frame(self, text: str, fontsize: int, color: str) -> np.ndarray:
        """Создает кадр с ограниченным кэшированием"""
        
        cache_key = f"{text}_{fontsize}_{color}"
        
        # Управление размером кэша
        if len(self.static_frames) >= self.max_cache_size:
            self._cleanup_cache()
        
        if cache_key in self.static_frames:
            self.cache_access_count[cache_key] += 1
            return self.static_frames[cache_key]
        
        # Создание нового кадра
        frame = self._generate_static_frame(text, fontsize, color)
        self.static_frames[cache_key] = frame
        self.cache_access_count[cache_key] = 1
        
        return frame
    
    def _cleanup_cache(self):
        """Очистка наименее используемых кадров из кэша"""
        # Удаляем 25% наименее используемых кадров
        items_to_remove = len(self.static_frames) // 4
        
        sorted_items = sorted(
            self.cache_access_count.items(), 
            key=lambda x: x[1]
        )
        
        for cache_key, _ in sorted_items[:items_to_remove]:
            if cache_key in self.static_frames:
                del self.static_frames[cache_key]
            if cache_key in self.cache_access_count:
                del self.cache_access_count[cache_key]
```

### Многопоточная обработка

```python
import concurrent.futures
from typing import List

class ParallelBatchProcessor:
    """Параллельная обработка множественных конфигураций"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
    
    def process_configs_parallel(self, config_paths: List[str], output_dir: str) -> List[bool]:
        """
        Обрабатывает конфигурации параллельно
        
        Args:
            config_paths: Списки путей к конфигурациям
            output_dir: Папка для вывода
            
        Returns:
            Список результатов обработки (True/False)
        """
        
        def process_single_config(config_path: str) -> bool:
            try:
                generator = Fixed3DStarWarsGeneratorV2()
                generator.load_config_file(config_path)
                
                output_name = os.path.basename(config_path).replace('.json', '.mp4')
                output_path = os.path.join(output_dir, output_name)
                
                generator.generate_video(output_path)
                return True
                
            except Exception as e:
                print(f"Error processing {config_path}: {e}")
                return False
        
        # Параллельная обработка
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            results = list(executor.map(process_single_config, config_paths))
        
        return results
```

---

## 📝 Примеры расширения

### Добавление нового эффекта "Particle System"

```python
class ParticleStarField:
    """Продвинутая система частиц для звёздного неба"""
    
    def __init__(self, width: int, height: int, particle_count: int = 200):
        self.width = width
        self.height = height
        self.particles = self._generate_particles(particle_count)
    
    def _generate_particles(self, count: int) -> List[dict]:
        """Генерация частиц звёзд"""
        import random
        
        particles = []
        for _ in range(count):
            particle = {
                'x': random.randint(0, self.width),
                'y': random.randint(0, self.height),
                'brightness': random.randint(50, 255),
                'size': random.choice([1, 1, 1, 2, 2, 3]),  # Больше мелких звёзд
                'twinkle_phase': random.random() * 2 * np.pi,
                'twinkle_speed': random.uniform(0.1, 0.3)
            }
            particles.append(particle)
        
        return particles
    
    def render_frame(self, progress: float) -> np.ndarray:
        """Рендеринг кадра с анимированными звёздами"""
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        for particle in self.particles:
            # Анимация мерцания
            twinkle = np.sin(particle['twinkle_phase'] + progress * particle['twinkle_speed'])
            current_brightness = int(particle['brightness'] * (0.7 + 0.3 * twinkle))
            
            # Отрисовка звезды
            x, y = particle['x'], particle['y']
            size = particle['size']
            
            if size == 1:
                frame[y, x] = [current_brightness] * 3
            else:
                # Звёзды большего размера
                for dy in range(-size//2, size//2 + 1):
                    for dx in range(-size//2, size//2 + 1):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.width and 0 <= ny < self.height:
                            distance = np.sqrt(dx*dx + dy*dy)
                            if distance <= size/2:
                                intensity = current_brightness * (1 - distance/(size/2))
                                frame[ny, nx] = [int(intensity)] * 3
        
        return frame

# Интеграция в основной класс
class Enhanced3DStarWarsGenerator(Fixed3DStarWarsGeneratorV2):
    """Расширенная версия с продвинутым звёздным небом"""
    
    def __init__(self):
        super().__init__()
        self.particle_system = ParticleStarField(self.width, self.height)
    
    def create_starfield_background(self, progress: float = 0.0) -> np.ndarray:
        """Создание анимированного звёздного неба"""
        return self.particle_system.render_frame(progress)
```

### Создание системы плагинов

```python
from abc import ABC, abstractmethod

class EffectPlugin(ABC):
    """Базовый класс для эффектов-плагинов"""
    
    @abstractmethod
    def apply_effect(self, frame: np.ndarray, progress: float, **kwargs) -> np.ndarray:
        """Применить эффект к кадру"""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Получить имя эффекта"""
        pass

class GlowEffectPlugin(EffectPlugin):
    """Плагин эффекта свечения"""
    
    def apply_effect(self, frame: np.ndarray, progress: float, **kwargs) -> np.ndarray:
        intensity = kwargs.get('intensity', 0.3)
        blur_radius = kwargs.get('blur_radius', 15)
        
        blurred = cv2.GaussianBlur(frame, (blur_radius, blur_radius), 0)
        return cv2.addWeighted(frame, 1.0, blurred, intensity, 0)
    
    def get_name(self) -> str:
        return "glow"

class PluginManager:
    """Менеджер плагинов эффектов"""
    
    def __init__(self):
        self.plugins = {}
    
    def register_plugin(self, plugin: EffectPlugin):
        """Регистрация плагина"""
        self.plugins[plugin.get_name()] = plugin
    
    def apply_effect(self, effect_name: str, frame: np.ndarray, progress: float, **kwargs) -> np.ndarray:
        """Применение эффекта по имени"""
        if effect_name in self.plugins:
            return self.plugins[effect_name].apply_effect(frame, progress, **kwargs)
        return frame
    
    def list_effects(self) -> List[str]:
        """Список доступных эффектов"""
        return list(self.plugins.keys())

# Использование системы плагинов
class PluginEnabledGenerator(Fixed3DStarWarsGeneratorV2):
    """Генератор с поддержкой плагинов"""
    
    def __init__(self):
        super().__init__()
        self.plugin_manager = PluginManager()
        
        # Регистрация стандартных эффектов
        self.plugin_manager.register_plugin(GlowEffectPlugin())
    
    def create_3d_frame(self, progress: float) -> np.ndarray:
        """Создание кадра с применением плагинов"""
        frame = super().create_3d_frame(progress)
        
        # Применение эффектов из конфигурации
        if hasattr(self, 'config') and 'effects' in self.config:
            for effect_config in self.config['effects']:
                effect_name = effect_config['name']
                effect_params = effect_config.get('params', {})
                
                frame = self.plugin_manager.apply_effect(
                    effect_name, frame, progress, **effect_params
                )
        
        return frame
```

---

## 🔗 Заключение

Данный Developer Guide предоставляет полную техническую документацию для разработчиков, работающих с системой Star Wars Text Perspective. Документ включает:

- **Архитектурные решения** и структуру кода
- **Подробное API** для всех компонентов  
- **Математические модели** перспективных преобразований
- **Практические примеры** расширения функциональности
- **Инструменты отладки** и тестирования
- **Оптимизации производительности**

Для получения дополнительной информации см. также:
- [TILT_CONFIGURATION_GUIDE.md](TILT_CONFIGURATION_GUIDE.md) - пользовательское руководство
- [PERSPECTIVE_FIX_REPORT.md](PERSPECTIVE_FIX_REPORT.md) - история исправлений
- [API.md](API.md) - справочник API
- [EXAMPLES.md](EXAMPLES.md) - примеры использования

---

**Версия документа:** 2.0  
**Последнее обновление:** 3 июля 2025
