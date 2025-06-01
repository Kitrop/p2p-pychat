import sys
import asyncio
import logging
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from src.gui.main_window import MainWindow


def get_app_dir() -> Path:
    """Получение директории приложения"""
    if getattr(sys, 'frozen', False):
        # Если приложение собрано в exe
        return Path(sys._MEIPASS)
    else:
        # Если запущено из исходников
        return Path(__file__).parent.parent


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)


def main():
    # Создаем приложение
    app = QApplication(sys.argv)

    # Создаем главное окно
    window = MainWindow()
    window.show()

    # Настраиваем обработку асинхронных задач
    timer = QTimer()
    # Пустой обработчик для обработки событий
    timer.timeout.connect(lambda: None)
    timer.start(100)  # Проверяем каждые 100 мс

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
