import os
import sys
import shutil
from pathlib import Path
import PyInstaller.__main__


def clean_build():
    """Очистка директорий сборки"""
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)


def build_app():
    """Сборка приложения"""
    # Определяем параметры для разных платформ
    platform = sys.platform
    icon_ext = '.ico' if platform == 'win32' else '.icns' if platform == 'darwin' else '.png'
    icon_file = f'assets/icon{icon_ext}'

    # Базовые аргументы PyInstaller
    args = [
        'src/main.py',  # Основной скрипт
        '--name=p2p-chat',  # Имя приложения
        '--onefile',  # Собрать в один файл
        '--windowed',  # Без консольного окна
        '--clean',  # Очистить кэш
        '--noconfirm',  # Не спрашивать подтверждения
    ]

    # Добавляем иконку, если она существует
    if os.path.exists(icon_file):
        args.append(f'--icon={icon_file}')

    # Платформо-зависимые настройки
    if platform == 'win32':
        args.extend([
            '--runtime-hook=src/utils/windows_hook.py',
            '--target-architecture=x86_64',
        ])
    elif platform == 'darwin':
        args.extend([
            '--runtime-hook=src/utils/macos_hook.py',
            '--target-architecture=arm64',
            '--codesign-identity=-',  # Отключаем подпись кода
        ])
    else:  # Linux
        args.extend([
            '--runtime-hook=src/utils/linux_hook.py',
        ])

    # Запускаем сборку
    PyInstaller.__main__.run(args)


def main():
    """Основная функция"""
    print("Очистка предыдущей сборки...")
    clean_build()

    print("Начало сборки приложения...")
    build_app()

    print("Сборка завершена!")
    print(
        f"Исполняемый файл находится в директории: {os.path.abspath('dist')}")


if __name__ == '__main__':
    main()
