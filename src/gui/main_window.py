from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QListWidget,
    QMessageBox, QSplitter, QDialog
)
from PySide6.QtCore import Qt, QTimer
import asyncio
from typing import Optional
from src.core.crypto import CryptoManager
from src.core.network import P2PConnection
from src.core.storage import Storage
from src.gui.chat import ChatWindow
from src.gui.login import LoginWindow
from src.utils.config import WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT
from src.utils.themes import apply_theme
from PySide6.QtGui import QAction
from PySide6.QtCore import Slot


class AddContactDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить контакт")
        self.setModal(True)

        layout = QVBoxLayout(self)

        # Поле для ввода публичного ключа
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Введите публичный ключ контакта")
        layout.addWidget(self.key_input)

        # Кнопки
        button_layout = QHBoxLayout()
        ok_button = QPushButton("Добавить")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

    def get_key(self) -> str:
        return self.key_input.text().strip()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("P2P Чат")
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

        # Инициализация компонентов
        self.crypto = CryptoManager()
        self.storage = Storage()
        self.storage.crypto = self.crypto  # Добавляем crypto в storage
        self.connection = P2PConnection(self.crypto)
        self.current_connection: Optional[P2PConnection] = None

        # Настройка асинхронного цикла событий
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        # Таймер для обработки асинхронных задач
        self.async_timer = QTimer()
        self.async_timer.timeout.connect(self._process_async_tasks)
        self.async_timer.start(50)  # Проверяем каждые 50 мс

        # Создание UI
        self._create_ui()
        self._create_menu()

        # Проверка наличия ключей
        if not self.storage.load_keys():
            self.show_login_window()

    def _process_async_tasks(self):
        """Обработка асинхронных задач"""
        try:
            # Обрабатываем все ожидающие задачи
            pending = asyncio.all_tasks(self.loop)
            if pending:
                self.loop.run_until_complete(asyncio.gather(*pending))
        except Exception as e:
            print(f"Ошибка в обработке асинхронных задач: {e}")

    def _create_ui(self):
        """Создание пользовательского интерфейса"""
        # Главный виджет
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Главный layout
        layout = QHBoxLayout(main_widget)

        # Создание сплиттера
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)

        # Левая панель (контакты)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        # Список контактов
        self.contacts_list = QListWidget()
        self.contacts_list.itemClicked.connect(self.on_contact_selected)
        left_layout.addWidget(QLabel("Контакты"))
        left_layout.addWidget(self.contacts_list)

        # Кнопка добавления контакта
        add_contact_btn = QPushButton("Добавить контакт")
        add_contact_btn.clicked.connect(self.show_add_contact_dialog)
        left_layout.addWidget(add_contact_btn)

        # Правая панель (чат)
        self.chat_widget = QWidget()
        chat_layout = QVBoxLayout(self.chat_widget)
        chat_layout.addWidget(QLabel("Выберите контакт для начала общения"))

        # Добавление панелей в сплиттер
        splitter.addWidget(left_panel)
        splitter.addWidget(self.chat_widget)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)

    def _create_menu(self):
        """Создание меню"""
        menubar = self.menuBar()

        # Меню Файл
        file_menu = menubar.addMenu("Файл")

        new_chat_action = QAction("Новый чат", self)
        new_chat_action.triggered.connect(self.show_add_contact_dialog)
        file_menu.addAction(new_chat_action)

        file_menu.addSeparator()

        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Меню Настройки
        settings_menu = menubar.addMenu("Настройки")

        theme_action = QAction("Тема", self)
        theme_action.triggered.connect(self.toggle_theme)
        settings_menu.addAction(theme_action)

        # Меню Помощь
        help_menu = menubar.addMenu("Помощь")

        about_action = QAction("О программе", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def show_login_window(self):
        """Показать окно входа"""
        self.login_window = LoginWindow(self.crypto, self.storage)
        self.login_window.login_successful.connect(self.on_login_successful)
        self.login_window.show()

    @Slot()
    def on_login_successful(self):
        """Обработка успешного входа"""
        self.login_window.close()
        self.load_contacts()

    def load_contacts(self):
        """Загрузка списка контактов"""
        self.contacts_list.clear()
        contacts = self.storage.get_contacts()
        self.contacts_list.addItems([c["public_key"] for c in contacts])

    def show_add_contact_dialog(self):
        """Показать диалог добавления контакта"""
        dialog = AddContactDialog(self)
        if dialog.exec() == QDialog.Accepted:
            key = dialog.get_key()
            if key:
                try:
                    self.storage.add_contact(key)
                    self.load_contacts()
                    QMessageBox.information(
                        self, "Успех", "Контакт успешно добавлен")
                    self.open_chat(key)  # Открыть чат сразу после добавления
                except Exception as e:
                    QMessageBox.critical(
                        self, "Ошибка", f"Не удалось добавить контакт: {str(e)}")

    def on_contact_selected(self, item):
        """Обработка выбора контакта"""
        peer_id = item.text()
        self.open_chat(peer_id)

    def open_chat(self, peer_id: str):
        """Открыть чат с контактом"""
        # Очищаем правую панель
        for i in reversed(range(self.chat_widget.layout().count())):
            self.chat_widget.layout().itemAt(i).widget().setParent(None)

        # Создаем новое соединение для чата
        self.current_connection = P2PConnection(self.crypto)

        # Создаем новое окно чата
        chat_window = ChatWindow(peer_id, self.crypto,
                                 self.storage, self.current_connection)

        # Устанавливаем обработчики событий
        self.current_connection.set_callbacks(
            lambda msg: chat_window.on_message_received(peer_id, msg),
            lambda: chat_window.on_connection_closed(peer_id)
        )

        # Инициализируем соединение
        try:
            self.loop.create_task(self.current_connection.create_connection())
        except Exception as e:
            QMessageBox.critical(
                self, "Ошибка", f"Не удалось установить соединение: {str(e)}")

        self.chat_widget.layout().addWidget(chat_window)

    def toggle_theme(self):
        """Переключение темы"""
        # Получаем текущую тему из настроек или используем светлую по умолчанию
        current_theme = self.storage.get_setting("theme", "light")
        new_theme = "dark" if current_theme == "light" else "light"

        # Применяем новую тему
        self.setPalette(apply_theme(new_theme))

        # Сохраняем выбор темы
        self.storage.save_setting("theme", new_theme)

    def show_about(self):
        """Показать информацию о программе"""
        QMessageBox.about(self, "О программе",
                          "P2P Chat\n"
                          "Версия 1.0\n\n"
                          "Безопасный P2P мессенджер с end-to-end шифрованием")

    def closeEvent(self, event):
        """Обработка закрытия окна"""
        try:
            if self.current_connection:
                self.loop.run_until_complete(self.current_connection.close())
            self.async_timer.stop()
            self.loop.close()
        except Exception as e:
            print(f"Ошибка при закрытии окна: {e}")
        event.accept()
