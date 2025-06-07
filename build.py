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
        '--hidden-import=_cffi_backend',  # Добавляем скрытый импорт
        '--hidden-import=nacl.bindings.crypto_aead',  # Добавляем скрытый импорт
        '--hidden-import=nacl.bindings.crypto_box',  # Добавляем скрытый импорт
        '--hidden-import=nacl.bindings.crypto_secretbox',  # Добавляем скрытый импорт
        '--hidden-import=nacl.bindings.crypto_sign',  # Добавляем скрытый импорт
        '--hidden-import=nacl.bindings.crypto_stream',  # Добавляем скрытый импорт
        '--hidden-import=nacl.bindings.crypto_generichash',  # Добавляем скрытый импорт
        '--hidden-import=nacl.bindings.crypto_hash',  # Добавляем скрытый импорт
        '--hidden-import=nacl.bindings.crypto_shorthash',  # Добавляем скрытый импорт
        '--hidden-import=nacl.bindings.crypto_pwhash',  # Добавляем скрытый импорт
        '--hidden-import=nacl.bindings.crypto_scalarmult',  # Добавляем скрытый импорт
        '--hidden-import=nacl.bindings.crypto_core',  # Добавляем скрытый импорт
        '--hidden-import=nacl.bindings.crypto_secretstream',  # Добавляем скрытый импорт
        '--hidden-import=nacl.bindings.crypto_kx',  # Добавляем скрытый импорт
        '--hidden-import=nacl.bindings.crypto_auth',  # Добавляем скрытый импорт
        '--hidden-import=nacl.bindings.crypto_onetimeauth',  # Добавляем скрытый импорт
        '--collect-all=nacl',  # Собираем все модули PyNaCl
        '--collect-all=cffi',  # Собираем все модули CFFI
        '--collect-all=aiortc',  # Собираем все модули aiortc
        '--hidden-import=aiortc',  # Добавляем скрытый импорт aiortc
        '--hidden-import=aiortc.mediastreams',  # Добавляем скрытый импорт медиапотоков
        # Добавляем скрытый импорт RTCPeerConnection
        '--hidden-import=aiortc.rtcpeerconnection',
        '--hidden-import=aiortc.rtcrtpsender',  # Добавляем скрытый импорт RTCRtpSender
        # Добавляем скрытый импорт RTCRtpReceiver
        '--hidden-import=aiortc.rtcrtpreceiver',
        # Добавляем скрытый импорт RTCRtpTransceiver
        '--hidden-import=aiortc.rtcrtptransceiver',
        # Добавляем скрытый импорт RTCRtpParameters
        '--hidden-import=aiortc.rtcrtpparameters',
        # Добавляем скрытый импорт RTCRtpContributingSource
        '--hidden-import=aiortc.rtcrtpcontributingsource',
        # Добавляем скрытый импорт RTCRtpEncodingParameters
        '--hidden-import=aiortc.rtcrtpencodingparameters',
        # Добавляем скрытый импорт RTCRtpCodecParameters
        '--hidden-import=aiortc.rtcrtpcodecparameters',
        '--hidden-import=aiortc.rtcrtpheader',  # Добавляем скрытый импорт RTCRtpHeader
        '--hidden-import=aiortc.rtcrtppacket',  # Добавляем скрытый импорт RTCRtpPacket
        '--hidden-import=aiortc.rtcrtpsender',  # Добавляем скрытый импорт RTCRtpSender
        # Добавляем скрытый импорт RTCRtpReceiver
        '--hidden-import=aiortc.rtcrtpreceiver',
        # Добавляем скрытый импорт RTCRtpTransceiver
        '--hidden-import=aiortc.rtcrtptransceiver',
        # Добавляем скрытый импорт RTCRtpParameters
        '--hidden-import=aiortc.rtcrtpparameters',
        # Добавляем скрытый импорт RTCRtpContributingSource
        '--hidden-import=aiortc.rtcrtpcontributingsource',
        # Добавляем скрытый импорт RTCRtpEncodingParameters
        '--hidden-import=aiortc.rtcrtpencodingparameters',
        # Добавляем скрытый импорт RTCRtpCodecParameters
        '--hidden-import=aiortc.rtcrtpcodecparameters',
        '--hidden-import=aiortc.rtcrtpheader',  # Добавляем скрытый импорт RTCRtpHeader
        '--hidden-import=aiortc.rtcrtppacket',  # Добавляем скрытый импорт RTCRtpPacket
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
