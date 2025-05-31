import os
import sys
from pathlib import Path


def setup_environment():
    """Настройка окружения для Windows"""
    # Получаем путь к директории с исполняемым файлом
    if getattr(sys, 'frozen', False):
        app_path = Path(sys._MEIPASS)
    else:
        app_path = Path(__file__).parent.parent.parent

    # Добавляем пути к ресурсам
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = str(
        app_path / 'PySide6' / 'plugins')
    os.environ['QT_PLUGIN_PATH'] = str(app_path / 'PySide6' / 'plugins')


setup_environment()
