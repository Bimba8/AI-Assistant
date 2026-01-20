"""Конфигурация приложения"""
import os
from pathlib import Path

# Базовая директория проекта
BASE_DIR = Path(__file__).parent

# Папка для сохранения истории
HISTORY_DIR = BASE_DIR / "chat_history"
HISTORY_DIR.mkdir(exist_ok=True)

# API ключ (из переменной окружения или спросить у пользователя)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

# Настройки по умолчанию
DEFAULT_MODEL = "meta-llama/llama-3.3-70b-instruct:free"
DEFAULT_MAX_HISTORY = 20
DEFAULT_TEMPERATURE = 0.8

# Доступные модели
AVAILABLE_MODELS = {
    "1": ("meta-llama/llama-3.3-70b-instruct:free", "Llama 3.3 70B (быстрая)"),
    "2": ("deepseek/deepseek-r1:free", "DeepSeek R1 (умная, медленная)"),
    "3": ("google/gemini-2.5-flash-image-preview:free", "Gemini 2.5 Flash"),
}