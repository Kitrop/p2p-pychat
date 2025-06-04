from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTextEdit, QLabel, QLineEdit, QMessageBox
)
from PySide6.QtCore import Qt, Signal, Slot
from src.core.crypto import CryptoManager
from src.core.network import P2PConnection
from src.core.storage import Storage
from src.utils.config import CHAT_HISTORY_LIMIT


class ChatWindow(QWidget):
    message_received = Signal(str, str)  # peer_id, message
    connection_closed = Signal(str)  # peer_id

    def __init__(self, peer_id: str, crypto_manager: CryptoManager,
                 storage: Storage, connection: P2PConnection):
        super().__init__()
        self.peer_id = peer_id
        self.crypto = crypto_manager
        self.storage = storage
        self.connection = connection

        self._create_ui()
        self._load_history()
        self._setup_connection()

    def _create_ui(self):
        """Создание пользовательского интерфейса"""
        layout = QVBoxLayout(self)

        # Заголовок
        header = QLabel(f"Чат с {self.peer_id}")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        # История сообщений
        self.history = QTextEdit()
        self.history.setReadOnly(True)
        layout.addWidget(self.history)

        # Поле ввода
        input_layout = QHBoxLayout()
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Введите сообщение...")
        self.message_input.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.message_input)

        send_button = QPushButton("Отправить")
        send_button.clicked.connect(self.send_message)
        input_layout.addWidget(send_button)

        layout.addLayout(input_layout)

    def _load_history(self):
        """Загрузка истории сообщений"""
        messages = self.storage.load_chat_history(self.peer_id)
        for msg in messages:
            self._add_message_to_history(
                msg.get("sender", self.peer_id), msg.get("text", ""))

    def _setup_connection(self):
        """Настройка соединения"""
        self.connection.message_received.connect(self.on_message_received)
        self.connection.connection_closed.connect(self.on_connection_closed)

    @Slot(str, str)
    def on_message_received(self, peer_id: str, message: str):
        """Обработка полученного сообщения"""
        if peer_id == self.peer_id:
            self._add_message_to_history(peer_id, message)
            self.storage.add_message(
                self.peer_id, {"sender": peer_id, "text": message})

    @Slot(str)
    def on_connection_closed(self, peer_id: str):
        """Обработка закрытия соединения"""
        if peer_id == self.peer_id:
            self.connection_closed.emit(peer_id)
            QMessageBox.warning(self, "Соединение закрыто",
                                f"Соединение с {peer_id} было закрыто")

    def send_message(self):
        """Отправка сообщения"""
        text = self.message_input.text().strip()
        if not text:
            return

        try:
            self.connection.send_message(self.peer_id, text)
            self._add_message_to_history("me", text)
            self.storage.add_message(
                self.peer_id, {"sender": "me", "text": text})
            self.message_input.clear()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка",
                                 f"Не удалось отправить сообщение: {str(e)}")

    def _add_message_to_history(self, sender: str, text: str):
        """Добавление сообщения в историю"""
        if sender == "me":
            self.history.append(f"<b>Вы:</b> {text}")
        else:
            self.history.append(f"<b>{sender}:</b> {text}")

        # Ограничение истории
        if self.history.document().blockCount() > CHAT_HISTORY_LIMIT:
            cursor = self.history.textCursor()
            cursor.movePosition(cursor.Start)
            cursor.movePosition(cursor.Down, cursor.KeepAnchor,
                                self.history.document().blockCount() - CHAT_HISTORY_LIMIT)
            cursor.removeSelectedText()

    def closeEvent(self, event):
        """Обработка закрытия окна"""
        self.connection.message_received.disconnect(self.on_message_received)
        self.connection.connection_closed.disconnect(self.on_connection_closed)
        event.accept()
