from typing import Dict
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt


def get_theme_colors(theme: str) -> Dict[str, QColor]:
    """Получить цвета для темы"""
    if theme == "dark":
        return {
            "window": QColor(53, 53, 53),
            "window_text": QColor(255, 255, 255),
            "base": QColor(25, 25, 25),
            "alternate_base": QColor(53, 53, 53),
            "text": QColor(255, 255, 255),
            "button": QColor(53, 53, 53),
            "button_text": QColor(255, 255, 255),
            "bright_text": QColor(255, 0, 0),
            "highlight": QColor(42, 130, 218),
            "highlight_text": QColor(255, 255, 255),
            "link": QColor(42, 130, 218),
            "link_visited": QColor(130, 42, 218),
            "mid": QColor(77, 77, 77),
            "dark": QColor(45, 45, 45),
            "shadow": QColor(30, 30, 30)
        }
    else:  # light theme
        return {
            "window": QColor(240, 240, 240),
            "window_text": QColor(0, 0, 0),
            "base": QColor(255, 255, 255),
            "alternate_base": QColor(233, 233, 233),
            "text": QColor(0, 0, 0),
            "button": QColor(240, 240, 240),
            "button_text": QColor(0, 0, 0),
            "bright_text": QColor(255, 0, 0),
            "highlight": QColor(0, 120, 215),
            "highlight_text": QColor(255, 255, 255),
            "link": QColor(0, 0, 255),
            "link_visited": QColor(128, 0, 128),
            "mid": QColor(208, 208, 208),
            "dark": QColor(160, 160, 160),
            "shadow": QColor(128, 128, 128)
        }


def apply_theme(theme: str) -> QPalette:
    """Применить тему к приложению"""
    colors = get_theme_colors(theme)
    palette = QPalette()

    # Устанавливаем цвета для различных ролей
    palette.setColor(QPalette.Window, colors["window"])
    palette.setColor(QPalette.WindowText, colors["window_text"])
    palette.setColor(QPalette.Base, colors["base"])
    palette.setColor(QPalette.AlternateBase, colors["alternate_base"])
    palette.setColor(QPalette.Text, colors["text"])
    palette.setColor(QPalette.Button, colors["button"])
    palette.setColor(QPalette.ButtonText, colors["button_text"])
    palette.setColor(QPalette.BrightText, colors["bright_text"])
    palette.setColor(QPalette.Highlight, colors["highlight"])
    palette.setColor(QPalette.HighlightedText, colors["highlight_text"])
    palette.setColor(QPalette.Link, colors["link"])
    palette.setColor(QPalette.LinkVisited, colors["link_visited"])
    palette.setColor(QPalette.Mid, colors["mid"])
    palette.setColor(QPalette.Dark, colors["dark"])
    palette.setColor(QPalette.Shadow, colors["shadow"])

    return palette
