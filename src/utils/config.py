import os
from pathlib import Path

# Базовые пути
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"
KEYS_DIR = DATA_DIR / "keys"
CHATS_DIR = DATA_DIR / "chats"
CONFIG_DIR = DATA_DIR / "config"

# Создаем необходимые директории
for directory in [DATA_DIR, KEYS_DIR, CHATS_DIR, CONFIG_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Настройки сети
DEFAULT_PORT = 5000
STUN_SERVERS = [
    "stun:stun.l.google.com:19302",
    "stun:stun1.l.google.com:19302"
]

# Настройки криптографии
CURVE = "curve25519"
KEY_SIZE = 32  # bytes
NONCE_SIZE = 24  # bytes for XChaCha20-Poly1305

# Настройки GUI
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 600
CHAT_HISTORY_LIMIT = 1000
DEFAULT_THEME = "light"

# Настройки безопасности
MESSAGE_EXPIRY = 7 * 24 * 60 * 60  # 7 дней в секундах
MAX_MESSAGE_SIZE = 1024 * 1024  # 1MB
DEFAULT_MESSAGE_EXPIRY = 24 * 60 * 60  # 24 часа в секундах

# Настройки сборки
BUILD_DIR = BASE_DIR / "build"
DIST_DIR = BASE_DIR / "dist"
SPEC_FILE = BASE_DIR / "p2p-chat.spec"
