import json
import logging
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QMessageBox, QTabWidget,
    QWidget, QScrollArea, QFrame, QApplication,
    QGroupBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon
from src.core.storage import Storage
from src.utils.config import KEYS_DIR

# Настройка логирования
logger = logging.getLogger(__name__)


class ErrorMessageBox(QMessageBox):
    def __init__(self, title: str, message: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setText(message)
        self.setIcon(QMessageBox.Critical)
        self.setStyleSheet("""
            QMessageBox {
                background-color: var(--bg-color);
            }
            QMessageBox QLabel {
                color: var(--text-color);
                font-size: 12px;
                min-width: 300px;
            }
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 15px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)


class KeyGroup(QGroupBox):
    def __init__(self, title: str, key_value: str, parent=None):
        super().__init__(title, parent)
        self.setStyleSheet("""
            QGroupBox {
                background-color: var(--bg-color);
                border: 1px solid var(--border-color);
                border-radius: 6px;
                margin-top: 12px;
                padding: 10px;
            }
            QGroupBox::title {
                color: var(--text-color);
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QLineEdit {
                background-color: var(--input-bg);
                color: var(--text-color);
                border: 1px solid var(--border-color);
                border-radius: 4px;
                padding: 5px;
                font-family: 'Consolas', monospace;
            }
            QPushButton {
                background-color: var(--primary-color);
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: var(--primary-hover);
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # Поле для ключа
        self.key_input = QLineEdit(key_value)
        self.key_input.setReadOnly(True)
        self.key_input.setStyleSheet("""
            QLineEdit {
                background-color: var(--input-bg);
                color: var(--text-color);
                border: 1px solid var(--border-color);
                border-radius: 4px;
                padding: 5px;
                font-family: 'Consolas', monospace;
            }
        """)
        layout.addWidget(self.key_input)

        # Кнопка копирования
        copy_button = QPushButton("Копировать")
        copy_button.setIcon(QIcon("assets/copy.png"))
        copy_button.clicked.connect(self._copy_key)
        layout.addWidget(copy_button)

    def _copy_key(self):
        """Копирование ключа в буфер обмена"""
        key = self.key_input.text()
        if key:
            QApplication.clipboard().setText(key)
            QMessageBox.information(
                self, "Успех", "Ключ скопирован в буфер обмена")


class SettingsDialog(QDialog):
    def __init__(self, storage: Storage, parent=None):
        super().__init__(parent)
        self.storage = storage
        self.setWindowTitle("Настройки")
        self.setMinimumSize(600, 400)
        self._create_ui()
        self._apply_theme()

    def _apply_theme(self):
        """Применение текущей темы"""
        theme = self.storage.get_setting("theme", "light")
        if theme == "dark":
            self.setStyleSheet("""
                :root {
                    --bg-color: #2d2d2d;
                    --text-color: #ffffff;
                    --border-color: #404040;
                    --input-bg: #3d3d3d;
                    --primary-color: #2196F3;
                    --primary-hover: #1976D2;
                }
                QDialog {
                    background-color: var(--bg-color);
                    color: var(--text-color);
                }
                QLabel {
                    color: var(--text-color);
                }
                QTabWidget::pane {
                    border: 1px solid var(--border-color);
                    background-color: var(--bg-color);
                }
                QTabBar::tab {
                    background: var(--input-bg); 
                    color: var(--text-color);
                    border: 1px solid var(--border-color);
                    border-bottom: none;
                    border-top-left-radius: 4px;
                    border-top-right-radius: 4px;
                    padding: 8px 16px;
                    margin-right: 2px;
                }
                QTabBar::tab:selected {
                    background: var(--bg-color);
                    border-bottom: 1px solid var(--bg-color);
                }
                QScrollArea {
                    border: none;
                    background-color: var(--bg-color);
                }
                QScrollBar:vertical {
                    border: none;
                    background: var(--input-bg);
                    width: 10px;
                    margin: 0px;
                }
                QScrollBar::handle:vertical {
                    background: var(--border-color);
                    min-height: 20px;
                    border-radius: 5px;
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    height: 0px;
                }
                QPushButton {
                    background-color: var(--primary-color);
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 4px 8px;
                    min-width: 60px;
                    max-width: 80px;
                    cursor: pointer;
                }
                QPushButton:hover {
                    background-color: var(--primary-hover);
                }
            """)
        else:
            self.setStyleSheet("""
                :root {
                    --bg-color: #ffffff;
                    --text-color: #000000;
                    --border-color: #cccccc;
                    --input-bg: #f5f5f5;
                    --primary-color: #2196F3;
                    --primary-hover: #1976D2;
                }
                QDialog {
                    background-color: var(--bg-color);
                    color: var(--text-color);
                }
                QLabel {
                    color: var(--text-color);
                }
                QTabWidget::pane {
                    border: 1px solid var(--border-color);
                    background-color: var(--bg-color);
                }
                QTabBar::tab {
                    background: var(--input-bg);
                    color: var(--text-color);
                    border: 1px solid var(--border-color);
                    border-bottom: none;
                    border-top-left-radius: 4px;
                    border-top-right-radius: 4px;
                    padding: 8px 16px;
                    margin-right: 2px;
                }
                QTabBar::tab:selected {
                    background: var(--bg-color);
                    border-bottom: 1px solid var(--bg-color);
                }
                QScrollArea {
                    border: none;
                    background-color: var(--bg-color);
                }
                QScrollBar:vertical {
                    border: none;
                    background: var(--input-bg);
                    width: 10px;
                    margin: 0px;
                }
                QScrollBar::handle:vertical {
                    background: var(--border-color);
                    min-height: 20px;
                    border-radius: 5px;
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    height: 0px;
                }
                QPushButton {
                    background-color: var(--primary-color);
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 4px 8px;
                    min-width: 60px;
                    max-width: 80px;
                    cursor: pointer;
                }
                QPushButton:hover {
                    background-color: var(--primary-hover);
                }
            """)

    def _create_ui(self):
        """Создание пользовательского интерфейса"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Заголовок
        title = QLabel("Настройки приложения")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Создаем вкладки
        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)

        # Вкладка с ключами
        keys_tab = QWidget()
        keys_layout = QVBoxLayout(keys_tab)
        keys_layout.setSpacing(15)

        # Создаем скролл-область для ключей
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(15)

        # Получаем ключи
        try:
            logger.info("Загрузка ключей из хранилища")
            keys = self.storage.get_keys()
            if not keys:
                logger.warning("Ключи не найдены в хранилище")
                QMessageBox.warning(self, "Предупреждение", "Ключи не найдены")
                return

            logger.info(f"Загружено {len(keys)} ключей")
            # Добавляем поля для каждого ключа
            for key_name, key_info in keys.items():
                key_group = KeyGroup(
                    key_info.get("description", key_name),
                    key_info.get("value", "")
                )
                scroll_layout.addWidget(key_group)

        except Exception as e:
            error_msg = f"Не удалось загрузить ключи: {str(e)}"
            logger.error(error_msg, exc_info=True)
            ErrorMessageBox("Ошибка", error_msg, self).exec()
            return

        # Добавляем скролл в layout
        scroll.setWidget(scroll_content)
        keys_layout.addWidget(scroll)

        # Добавляем вкладку
        tab_widget.addTab(keys_tab, "Ключи")

        # Кнопки внизу окна
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        close_button = QPushButton("Закрыть")
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)

        layout.addLayout(button_layout)

    def get_keys(self) -> dict:
        """Получить все ключи из файла"""
        keys_file = KEYS_DIR / "keys.json"
        if not keys_file.exists():
            return {}
        try:
            with open(keys_file, "r") as f:
                keys_data = json.load(f)
            return keys_data.get("keys", {})
        except Exception as e:
            logger.error(f"Ошибка при получении ключей: {e}")
            return {}
