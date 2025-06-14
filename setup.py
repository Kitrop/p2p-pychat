# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="p2p-pychat",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "PySide6>=6.6.0",
        "pynacl>=1.5.0",
        "cryptography>=42.0.0",
        "aiortc>=1.5.0",
        "aioice>=0.9.0",
        "pytest>=8.0.0",
        "pytest-asyncio>=0.23.0",
        "pyinstaller>=6.3.0",
        "cffi>=1.16.0",
        "pycparser>=2.21"
    ],
    entry_points={
        "console_scripts": [
            "p2p-chat=src.main:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="Secure P2P messenger with end-to-end encryption",
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/p2p-chat",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Topic :: Communications :: Chat",
    ],
    python_requires=">=3.8",
)
