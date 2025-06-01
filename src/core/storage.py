import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from ..utils.config import CHATS_DIR, KEYS_DIR, DEFAULT_MESSAGE_EXPIRY
from .crypto import CryptoManager
import base64
import logging

logger = logging.getLogger(__name__)


class Storage:
    def __init__(self, crypto_manager: CryptoManager):
        self.crypto = crypto_manager
        self._ensure_directories()
        self.settings_file = Path("data") / "settings.json"
        self.contacts_file = Path("data") / "contacts.json"
        self._ensure_settings_file()
        self._ensure_contacts_file()

    def _ensure_directories(self) -> None:
        """Создание необходимых директорий"""
        try:
            logger.info(f"Создание директории для ключей: {KEYS_DIR}")
            KEYS_DIR.mkdir(parents=True, exist_ok=True)
            logger.info(f"Создание директории для чатов: {CHATS_DIR}")
            CHATS_DIR.mkdir(parents=True, exist_ok=True)
            logger.info(f"Создание директории data: {Path('data')}")
            Path("data").mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.error(f"Ошибка при создании директорий: {e}")
            raise

    def _ensure_settings_file(self) -> None:
        """Создание файла настроек, если он не существует"""
        if not self.settings_file.exists():
            # Устанавливаем светлую тему по умолчанию
            self.save_setting("theme", "light")

    def _ensure_contacts_file(self) -> None:
        """Создание файла контактов, если он не существует"""
        if not self.contacts_file.exists():
            with open(self.contacts_file, "w") as f:
                json.dump({"contacts": []}, f, indent=2)

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

    def save_keys(self, public_key: str, verify_key: str, private_key: str, signing_key: str) -> None:
        """Сохранение ключей"""
        try:
            keys_file = KEYS_DIR / "keys.json"
            logger.info(f"Сохранение ключей в файл: {keys_file}")

            keys_data = {
                "info": "Этот файл содержит ваши криптографические ключи. Храните его в надежном месте!",
                "keys": {
                    "public_key": {
                        "description": "Публичный ключ для шифрования (можно делиться с другими)",
                        "value": public_key
                    },
                    "verify_key": {
                        "description": "Ключ верификации (можно делиться с другими)",
                        "value": verify_key
                    },
                    "private_key": {
                        "description": "Приватный ключ для расшифровки (храните в секрете!)",
                        "value": private_key
                    },
                    "signing_key": {
                        "description": "Ключ подписи (храните в секрете!)",
                        "value": signing_key
                    }
                },
                "created_at": datetime.now().isoformat()
            }

            with open(keys_file, "w") as f:
                json.dump(keys_data, f, indent=2)

            logger.info("Ключи успешно сохранены")
        except Exception as e:
            logger.error(f"Ошибка при сохранении ключей: {e}")
            raise

    def load_keys(self) -> bool:
        """Загрузка ключей"""
        keys_file = KEYS_DIR / "keys.json"
        if not keys_file.exists():
            return False

        try:
            with open(keys_file, "r") as f:
                keys_data = json.load(f)

            # Загружаем ключи в CryptoManager
            self.crypto.load_keys(
                base64.b64decode(keys_data["keys"]["private_key"]["value"]),
                base64.b64decode(keys_data["keys"]["signing_key"]["value"])
            )
            return True
        except Exception as e:
            logger.error(f"Ошибка загрузки ключей: {e}")
            return False

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

    def add_contact(self, public_key: str) -> None:
        """Добавление нового контакта"""
        try:
            # Проверяем формат ключа
            if not public_key or len(public_key) < 32:
                raise ValueError("Неверный формат публичного ключа")

            # Загружаем существующие контакты
            contacts = []
            if self.contacts_file.exists():
                with open(self.contacts_file, "r") as f:
                    data = json.load(f)
                    contacts = data.get("contacts", [])

            # Проверяем, не существует ли уже такой контакт
            for contact in contacts:
                if contact["public_key"] == public_key:
                    raise ValueError("Контакт уже существует")

            # Добавляем новый контакт
            contacts.append({
                "public_key": public_key,
                "added_at": datetime.now().isoformat()
            })

            # Сохраняем обновленный список контактов
            with open(self.contacts_file, "w") as f:
                json.dump({"contacts": contacts}, f, indent=2)

            logger.info(f"Контакт успешно добавлен: {public_key[:10]}...")
        except Exception as e:
            logger.error(f"Ошибка при добавлении контакта: {e}")
            raise

    def get_contacts(self) -> List[Dict]:
        """Получение списка контактов"""
        if not self.contacts_file.exists():
            return []

        try:
            with open(self.contacts_file, "r") as f:
                data = json.load(f)
                return data.get("contacts", [])
        except Exception as e:
            logger.error(f"Ошибка при получении контактов: {e}")
            return []
