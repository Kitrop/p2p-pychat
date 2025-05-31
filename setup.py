from setuptools import setup, find_packages

setup(
    name="p2p-chat",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "PySide6>=6.6.0",
        "pynacl>=1.5.0",
        "cryptography>=42.0.0",
        "aiortc>=1.5.0",
        "aioice>=0.9.0",
    ],
    entry_points={
        "console_scripts": [
            "p2p-chat=src.main:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="Безопасный P2P мессенджер с end-to-end шифрованием",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/p2p-chat",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Topic :: Communications :: Chat",
    ],
    python_requires=">=3.10",
)
