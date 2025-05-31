import sys
import asyncio
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from src.gui.main_window import MainWindow


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
