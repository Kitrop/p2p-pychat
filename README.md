# P2P Чат

Безопасный P2P мессенджер с шифрованием и минималистичным интерфейсом.

## Особенности

- 🔒 Сквозное шифрование (ECDH + AES-256-GCM)
- 🌐 P2P соединения без центрального сервера
- 💬 Поддержка личных и групповых чатов
- 🎨 Светлая и тёмная темы
- ⏱️ Самоудаляющиеся сообщения
- 🔄 NAT traversal через STUN

## Требования

- Python 3.10 или выше
- PySide6
- PyNaCl
- aiortc
- cryptography

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/p2p-chat.git
cd p2p-chat
```

2. Создайте виртуальное окружение:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Сборка

### Windows

1. Установите необходимые инструменты:
```bash
pip install pyinstaller
```

2. Запустите сборку:
```bash
python build.py
```

3. Готовый exe-файл будет находиться в папке `dist`

### macOS

1. Установите необходимые инструменты:
```bash
pip install pyinstaller
```

2. Запустите сборку:
```bash
python build.py
```

3. Готовый app-файл будет находиться в папке `dist`

### Linux

1. Установите необходимые зависимости:
```bash
# Ubuntu/Debian
sudo apt-get install python3-dev python3-pip python3-venv
sudo apt-get install libgl1-mesa-dev

# Fedora
sudo dnf install python3-devel python3-pip
sudo dnf install mesa-libGL-devel
```

2. Установите PyInstaller:
```bash
pip install pyinstaller
```

3. Запустите сборку:
```bash
python build.py
```

4. Готовый бинарный файл будет находиться в папке `dist`

## Запуск

### Из исходников
```bash
python src/main.py
```

### Из собранного приложения

- Windows: Запустите `dist/p2p-chat.exe`
- macOS: Запустите `dist/p2p-chat.app`
- Linux: Запустите `dist/p2p-chat`

## Безопасность

- Все сообщения шифруются с использованием ECDH и AES-256-GCM
- Ключи хранятся локально и никогда не передаются
- Поддержка самоудаляющихся сообщений
- Безопасный обмен ключами

## Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для ваших изменений
3. Внесите изменения
4. Отправьте pull request

## Лицензия

MIT 