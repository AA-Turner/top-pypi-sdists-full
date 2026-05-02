"""
Color Picker Widget

RGB color picker for backlight control.
"""

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QColorDialog, QHBoxLayout, QLabel, QPushButton, QWidget


class ColorPickerWidget(QWidget):
    """RGB color picker with preset buttons"""

    color_changed = pyqtSignal(str)  # Hex color string

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_color = QColor("#FFFFFF")
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout()

        # Current color preview
        self.color_preview = QLabel()
        self.color_preview.setFixedSize(40, 40)
        self._update_preview()
        layout.addWidget(self.color_preview)

        # Color picker button
        picker_btn = QPushButton("Pick Color")
        picker_btn.clicked.connect(self._open_color_dialog)
        layout.addWidget(picker_btn)

        # Preset colors
        presets = [
            ("#FF0000", "Red"),
            ("#00FF00", "Green"),
            ("#0000FF", "Blue"),
            ("#FFFF00", "Yellow"),
            ("#FF00FF", "Magenta"),
            ("#00FFFF", "Cyan"),
            ("#FFFFFF", "White"),
        ]

        for color, name in presets:
            btn = QPushButton(name)
            btn.setMaximumWidth(60)
            btn.clicked.connect(lambda checked=False, c=color: self.set_color(c))
            layout.addWidget(btn)

        layout.addStretch()
        self.setLayout(layout)

    def _open_color_dialog(self):
        """Open Qt color picker dialog"""
        color = QColorDialog.getColor(self.current_color, self, "Select Color")
        if color.isValid():
            self.set_color(color.name())

    def set_color(self, color_hex: str):
        """Set the current color"""
        self.current_color = QColor(color_hex)
        self._update_preview()
        self.color_changed.emit(color_hex)

    def _update_preview(self):
        """Update color preview display"""
        self.color_preview.setStyleSheet(
            f"background-color: {self.current_color.name()}; border: 2px solid black;"
        )
