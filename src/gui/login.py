from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QMessageBox, QRadioButton,
    QButtonGroup, QApplication
)
from PySide6.QtCore import Qt, Signal
from src.core.crypto import CryptoManager
from src.core.storage import Storage
import base64


class LoginWindow(QDialog):
    login_successful = Signal()

    def __init__(self, crypto_manager: CryptoManager, storage: Storage):
        super().__init__()
        self.crypto_manager = crypto_manager
        self.storage = storage
        self._can_close = False  # Флаг разрешения закрытия

        self.setWindowTitle("Вход в P2P Chat")
        self.setMinimumWidth(400)
        self.setModal(True)

        self._create_ui()

    def closeEvent(self, event):
        if not self._can_close:
            QApplication.quit()  # Завершить всё приложение
        else:
            event.accept()

    def _create_ui(self):
        """Создание пользовательского интерфейса"""
        layout = QVBoxLayout(self)

        # Заголовок
        title = QLabel("Добро пожаловать в P2P Chat")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Выбор режима
        mode_group = QButtonGroup(self)

        new_user_radio = QRadioButton("Новый пользователь")
        new_user_radio.setChecked(True)
        mode_group.addButton(new_user_radio)

        existing_user_radio = QRadioButton("Существующий пользователь")
        mode_group.addButton(existing_user_radio)

        layout.addWidget(new_user_radio)
        layout.addWidget(existing_user_radio)

        # Поля для ключей
        self.private_key_input = QLineEdit()
        self.private_key_input.setPlaceholderText("Приватный ключ")
        self.private_key_input.setVisible(False)

        self.verify_key_input = QLineEdit()
        self.verify_key_input.setPlaceholderText("Ключ верификации")
        self.verify_key_input.setVisible(False)

        layout.addWidget(self.private_key_input)
        layout.addWidget(self.verify_key_input)

        # Кнопки
        button_layout = QHBoxLayout()

        self.generate_btn = QPushButton("Сгенерировать ключи")
        self.generate_btn.clicked.connect(self.generate_keys)

        self.load_btn = QPushButton("Загрузить ключи")
        self.load_btn.clicked.connect(self.load_keys)
        self.load_btn.setVisible(False)

        button_layout.addWidget(self.generate_btn)
        button_layout.addWidget(self.load_btn)

        layout.addLayout(button_layout)

        # Обработчики событий
        new_user_radio.toggled.connect(self.on_mode_changed)
        existing_user_radio.toggled.connect(self.on_mode_changed)

    def on_mode_changed(self, checked: bool):
        """Обработка изменения режима"""
        is_new_user = self.sender().text() == "Новый пользователь"

        self.private_key_input.setVisible(not is_new_user)
        self.verify_key_input.setVisible(not is_new_user)
        self.generate_btn.setVisible(is_new_user)
        self.load_btn.setVisible(not is_new_user)

    def generate_keys(self):
        """Генерация новых ключей"""
        try:
            # Генерируем ключи
            self.crypto_manager.generate_keys()

            # Получаем все ключи
            public_key = base64.b64encode(
                self.crypto_manager.get_public_key()).decode()
            verify_key = base64.b64encode(
                self.crypto_manager.get_verify_key()).decode()
            private_key = base64.b64encode(
                self.crypto_manager.get_private_key()).decode()
            signing_key = base64.b64encode(
                self.crypto_manager.get_signing_key()).decode()

            # Сохраняем все ключи
            self.storage.save_keys(
                public_key, verify_key, private_key, signing_key)

            # Показываем ключи пользователю
            keys_info = (
                "Ваши ключи успешно сгенерированы!\n\n"
                "Публичный ключ (для обмена с другими пользователями):\n"
                f"{public_key}\n\n"
                "Ключ верификации (для обмена с другими пользователями):\n"
                f"{verify_key}\n\n"
                "Приватный ключ (храните в надежном месте):\n"
                f"{private_key}\n\n"
                "Ключ подписи (храните в надежном месте):\n"
                f"{signing_key}\n\n"
                "ВНИМАНИЕ: Сохраните приватный ключ и ключ подписи в надежном месте!\n"
                "Они необходимы для доступа к вашему аккаунту."
            )

            QMessageBox.information(
                self,
                "Ключи сгенерированы",
                keys_info
            )

            self._can_close = True
            self.login_successful.emit()
            self.accept()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Не удалось сгенерировать ключи: {str(e)}"
            )

    def load_keys(self):
        """Загрузка существующих ключей"""
        try:
            private_key = self.private_key_input.text().strip()
            verify_key = self.verify_key_input.text().strip()

            if not private_key or not verify_key:
                raise ValueError("Введите оба ключа")

            # Декодируем ключи из base64
            private_key_bytes = base64.b64decode(private_key)
            verify_key_bytes = base64.b64decode(verify_key)

            # Загружаем ключи
            self.crypto_manager.load_keys(private_key_bytes, verify_key_bytes)

            # Сохраняем ключи в хранилище
            public_key = base64.b64encode(
                self.crypto_manager.get_public_key()).decode()
            verify_key = base64.b64encode(
                self.crypto_manager.get_verify_key()).decode()
            private_key = base64.b64encode(
                self.crypto_manager.get_private_key()).decode()
            signing_key = base64.b64encode(
                self.crypto_manager.get_signing_key()).decode()

            self.storage.save_keys(
                public_key, verify_key, private_key, signing_key)

            self._can_close = True
            self.login_successful.emit()
            self.accept()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Не удалось загрузить ключи: {str(e)}"
            )
