from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QMessageBox, QListWidget
)
from PySide6.QtCore import Qt
from src.core.storage import Storage
import logging

logger = logging.getLogger(__name__)


class ContactsDialog(QDialog):
    def __init__(self, storage: Storage, parent=None):
        super().__init__(parent)
        self.storage = storage
        self.setWindowTitle("Контакты")
        self.setMinimumSize(400, 500)
        self._create_ui()
        self._apply_theme()
        self.load_contacts()

    def _apply_theme(self):
        """Применение текущей темы"""
        theme = self.storage.get_setting("theme", "light")
        if theme == "dark":
            self.setStyleSheet("""
                :root {
                    --bg-color: #23272f;
                    --text-color: #f5f6fa;
                    --border-color: #353b48;
                    --input-bg: #2f3640;
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
                QListWidget {
                    background-color: var(--input-bg);
                    color: var(--text-color);
                    border: none;
                    border-radius: 0;
                    font-size: 14px;
                }
                QListWidget::item {
                    padding: 10px 12px;
                    border-bottom: 1px solid var(--border-color);
                    cursor: pointer;
                }
                QListWidget::item:selected {
                    background-color: var(--primary-color);
                    color: white;
                }
                QPushButton {
                    background-color: var(--primary-color);
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 6px 14px;
                    min-width: 40px;
                    font-size: 14px;
                    cursor: pointer;
                }
                QPushButton:hover {
                    background-color: var(--primary-hover);
                }
                QLineEdit {
                    background-color: var(--input-bg);
                    color: var(--text-color);
                    border: 1px solid var(--border-color);
                    border-radius: 6px;
                    padding: 7px 12px;
                    font-size: 14px;
                }
            """)
        else:
            self.setStyleSheet("""
                :root {
                    --bg-color: #f7f8fa;
                    --text-color: #23272f;
                    --border-color: #e0e0e0;
                    --input-bg: #ffffff;
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
                QListWidget {
                    background-color: var(--input-bg);
                    color: var(--text-color);
                    border: none;
                    border-radius: 0;
                    font-size: 14px;
                }
                QListWidget::item {
                    padding: 10px 12px;
                    border-bottom: 1px solid var(--border-color);
                    cursor: pointer;
                }
                QListWidget::item:selected {
                    background-color: var(--primary-color);
                    color: white;
                }
                QPushButton {
                    background-color: var(--primary-color);
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 6px 14px;
                    min-width: 40px;
                    font-size: 14px;
                    cursor: pointer;
                }
                QPushButton:hover {
                    background-color: var(--primary-hover);
                }
                QLineEdit {
                    background-color: var(--input-bg);
                    color: var(--text-color);
                    border: 1px solid var(--border-color);
                    border-radius: 6px;
                    padding: 7px 12px;
                    font-size: 14px;
                }
            """)

    def _create_ui(self):
        """Создание пользовательского интерфейса"""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # Заголовок
        title = QLabel("Управление контактами")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Поле для ввода ключа
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Введите публичный ключ контакта")
        layout.addWidget(self.key_input)

        # Кнопки добавления
        add_layout = QHBoxLayout()
        add_button = QPushButton("Добавить контакт")
        add_button.clicked.connect(self.add_contact)
        add_layout.addWidget(add_button)
        layout.addLayout(add_layout)

        # Список контактов
        self.contacts_list = QListWidget()
        layout.addWidget(self.contacts_list)

        # Кнопки управления
        button_layout = QHBoxLayout()

        delete_button = QPushButton("Удалить")
        delete_button.clicked.connect(self.delete_contact)
        button_layout.addWidget(delete_button)

        button_layout.addStretch()

        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)

        layout.addLayout(button_layout)

    def load_contacts(self):
        """Загрузка списка контактов"""
        try:
            contacts = self.storage.get_contacts()
            self.contacts_list.clear()
            for contact in contacts:
                self.contacts_list.addItem(contact["public_key"])
        except Exception as e:
            logger.error(f"Ошибка при загрузке контактов: {e}")
            QMessageBox.critical(
                self, "Ошибка", "Не удалось загрузить контакты")

    def add_contact(self):
        """Добавление нового контакта"""
        key = self.key_input.text().strip()
        if not key:
            QMessageBox.warning(self, "Предупреждение",
                                "Введите публичный ключ")
            return

        try:
            self.storage.add_contact(key)
            self.key_input.clear()
            self.load_contacts()
            QMessageBox.information(self, "Успех", "Контакт успешно добавлен")
        except Exception as e:
            logger.error(f"Ошибка при добавлении контакта: {e}")
            QMessageBox.critical(
                self, "Ошибка", f"Не удалось добавить контакт: {str(e)}")

    def delete_contact(self):
        """Удаление выбранного контакта"""
        current_item = self.contacts_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Предупреждение",
                                "Выберите контакт для удаления")
            return

        key = current_item.text()
        try:
            self.storage.delete_contact(key)
            self.load_contacts()
            QMessageBox.information(self, "Успех", "Контакт успешно удален")
        except Exception as e:
            logger.error(f"Ошибка при удалении контакта: {e}")
            QMessageBox.critical(
                self, "Ошибка", f"Не удалось удалить контакт: {str(e)}")
