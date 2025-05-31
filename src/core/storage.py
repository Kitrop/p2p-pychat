import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from ..utils.config import CHATS_DIR, KEYS_DIR, DEFAULT_MESSAGE_EXPIRY
from .crypto import CryptoManager


class Storage:
    def __init__(self, crypto_manager: CryptoManager):
        self.crypto = crypto_manager
        self._ensure_directories()
        self.settings_file = Path("data") / "settings.json"
        self._ensure_settings_file()

    def _ensure_directories(self) -> None:
        """Создание необходимых директорий"""
        CHATS_DIR.mkdir(parents=True, exist_ok=True)
        KEYS_DIR.mkdir(parents=True, exist_ok=True)
        Path("data").mkdir(parents=True, exist_ok=True)

    def _ensure_settings_file(self) -> None:
        """Создание файла настроек, если он не существует"""
        if not self.settings_file.exists():
            # Устанавливаем светлую тему по умолчанию
            self.save_setting("theme", "light")

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Получение значения настройки"""
        if not self.settings_file.exists():
            return default

        try:
            with open(self.settings_file, "r") as f:
                settings = json.load(f)
                return settings.get(key, default)
        except (json.JSONDecodeError, IOError):
            return default

    def save_setting(self, key: str, value: Any) -> None:
        """Сохранение значения настройки"""
        settings = {}
        if self.settings_file.exists():
            try:
                with open(self.settings_file, "r") as f:
                    settings = json.load(f)
            except (json.JSONDecodeError, IOError):
                pass

        settings[key] = value

        with open(self.settings_file, "w") as f:
            json.dump(settings, f, indent=2)

    def save_keys(self, public_key: str, verify_key: str) -> None:
        """Сохранение ключей"""
        keys_file = KEYS_DIR / "keys.json"
        keys_data = {
            "public_key": public_key,
            "verify_key": verify_key,
            "created_at": datetime.now().isoformat()
        }

        with open(keys_file, "w") as f:
            json.dump(keys_data, f, indent=2)

    def load_keys(self) -> Optional[Dict[str, str]]:
        """Загрузка ключей"""
        keys_file = KEYS_DIR / "keys.json"
        if not keys_file.exists():
            return None

        with open(keys_file, "r") as f:
            return json.load(f)

    def save_chat_history(self, peer_id: str, messages: List[Dict]) -> None:
        """Сохранение истории чата"""
        chat_file = CHATS_DIR / f"{peer_id}.json"
        chat_data = {
            "peer_id": peer_id,
            "messages": messages,
            "last_updated": datetime.now().isoformat()
        }

        with open(chat_file, "w") as f:
            json.dump(chat_data, f, indent=2)

    def load_chat_history(self, peer_id: str) -> List[Dict]:
        """Загрузка истории чата"""
        chat_file = CHATS_DIR / f"{peer_id}.json"
        if not chat_file.exists():
            return []

        with open(chat_file, "r") as f:
            data = json.load(f)
            messages = data.get("messages", [])

            # Удаляем истекшие сообщения
            current_time = datetime.now()
            valid_messages = []

            for message in messages:
                if "expiry" in message:
                    expiry_time = datetime.fromisoformat(
                        message["timestamp"]) + timedelta(seconds=message["expiry"])
                    if current_time < expiry_time:
                        valid_messages.append(message)
                else:
                    valid_messages.append(message)

            # Если были удалены сообщения, сохраняем обновленную историю
            if len(valid_messages) != len(messages):
                self.save_chat_history(peer_id, valid_messages)

            return valid_messages

    def add_message(self, peer_id: str, message: Dict, expiry: Optional[int] = None) -> None:
        """Добавление нового сообщения в историю"""
        messages = self.load_chat_history(peer_id)
        message_data = {
            **message,
            "timestamp": datetime.now().isoformat(),
            "expiry": expiry or DEFAULT_MESSAGE_EXPIRY
        }
        messages.append(message_data)
        self.save_chat_history(peer_id, messages)

    def get_all_chats(self) -> List[str]:
        """Получение списка всех чатов"""
        return [f.stem for f in CHATS_DIR.glob("*.json")]

    def delete_chat(self, peer_id: str) -> None:
        """Удаление чата"""
        chat_file = CHATS_DIR / f"{peer_id}.json"
        if chat_file.exists():
            chat_file.unlink()

    def clear_all_chats(self) -> None:
        """Очистка всех чатов"""
        for chat_file in CHATS_DIR.glob("*.json"):
            chat_file.unlink()

    def cleanup_expired_messages(self) -> None:
        """Очистка всех истекших сообщений"""
        for chat_file in CHATS_DIR.glob("*.json"):
            peer_id = chat_file.stem
            # Это автоматически удалит истекшие сообщения
            self.load_chat_history(peer_id)
