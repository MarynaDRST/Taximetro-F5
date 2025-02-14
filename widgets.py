from PyQt5.QtWidgets import (
    QVBoxLayout, QPushButton, 
    )
from PyQt5.QtGui import QIcon


class ModernButton(QPushButton):
    def __init__(self, text, icon_path=None, color="#FFFFFF"):
        super().__init__()
        self.setText(text)
        if icon_path:
            self.setIcon(QIcon(icon_path))
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border-radius: 10px;
                padding: 15px;
                color: white;
                font-size: 14px;
                min-width: 100px;
                min-height: 80px;
            }}
            QPushButton:hover {{
                background-color: {color.replace(')', ', 0.8)')};
            }}
        """)
        self.setLayout(QVBoxLayout())