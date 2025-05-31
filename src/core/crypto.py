from nacl.public import PrivateKey, PublicKey, Box
from nacl.secret import SecretBox
from nacl.utils import random
from nacl.signing import SigningKey, VerifyKey
import base64
import json
from typing import Tuple, Dict, Optional
from ..utils.config import KEY_SIZE, NONCE_SIZE


class CryptoManager:
    def __init__(self):
        self._private_key: Optional[PrivateKey] = None
        self._public_key: Optional[PublicKey] = None
        self._signing_key: Optional[SigningKey] = None
        self._verify_key: Optional[VerifyKey] = None

    def generate_keys(self) -> Tuple[bytes, bytes]:
        """Генерация пары ключей для шифрования и подписи"""
        self._private_key = PrivateKey.generate()
        self._public_key = self._private_key.public_key
        self._signing_key = SigningKey.generate()
        self._verify_key = self._signing_key.verify_key

        return (
            base64.b64encode(self._public_key.encode()).decode(),
            base64.b64encode(self._verify_key.encode()).decode()
        )

    def load_keys(self, private_key: bytes, verify_key: bytes) -> None:
        """Загрузка существующих ключей"""
        self._private_key = PrivateKey(private_key)
        self._public_key = self._private_key.public_key
        self._signing_key = SigningKey(verify_key)
        self._verify_key = self._signing_key.verify_key

    def encrypt_message(self, message: str, recipient_public_key: bytes) -> Dict[str, str]:
        """Шифрование сообщения для получателя"""
        if not self._private_key:
            raise ValueError("Ключи не инициализированы")

        # Создаем Box для ECDH
        box = Box(self._private_key, PublicKey(recipient_public_key))

        # Генерируем случайный nonce
        nonce = random(NONCE_SIZE)

        # Шифруем сообщение
        encrypted = box.encrypt(message.encode(), nonce)

        # Подписываем сообщение
        signature = self._signing_key.sign(encrypted).signature

        return {
            "encrypted": base64.b64encode(encrypted).decode(),
            "nonce": base64.b64encode(nonce).decode(),
            "signature": base64.b64encode(signature).decode()
        }

    def decrypt_message(self, encrypted_data: Dict[str, str], sender_public_key: bytes) -> str:
        """Расшифровка сообщения от отправителя"""
        if not self._private_key:
            raise ValueError("Ключи не инициализированы")

        # Создаем Box для ECDH
        box = Box(self._private_key, PublicKey(sender_public_key))

        # Декодируем данные
        encrypted = base64.b64decode(encrypted_data["encrypted"])
        nonce = base64.b64decode(encrypted_data["nonce"])
        signature = base64.b64decode(encrypted_data["signature"])

        # Проверяем подпись
        verify_key = VerifyKey(sender_public_key)
        try:
            verify_key.verify(encrypted, signature)
        except Exception as e:
            raise ValueError("Неверная подпись сообщения") from e

        # Расшифровываем сообщение
        decrypted = box.decrypt(encrypted, nonce)
        return decrypted.decode()

    def get_public_key(self) -> bytes:
        """Получение публичного ключа"""
        if not self._public_key:
            raise ValueError("Ключи не инициализированы")
        return self._public_key.encode()

    def get_verify_key(self) -> bytes:
        """Получение ключа верификации"""
        if not self._verify_key:
            raise ValueError("Ключи не инициализированы")
        return self._verify_key.encode()
