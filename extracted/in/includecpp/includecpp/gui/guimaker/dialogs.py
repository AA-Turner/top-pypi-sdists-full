"""
CSSL GUI Builder - Dialogs (New Project, Code Preview).
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                              QLineEdit, QSpinBox, QPushButton, QTextEdit,
                              QGridLayout, QGroupBox, QWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from . import theme


class NewProjectDialog(QDialog):
    """Dialog for creating a new GUI project."""

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setWindowTitle("New CSSL GUI Project")
        self.setFixedSize(420, 320)
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {theme.DARK_BG};
                color: {theme.TEXT_PRIMARY};
            }}
        """)

        self._class_name = "MyApp"
        self._window_title = "CSSL Application"
        self._window_width = 800
        self._window_height = 600

        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        # Title
        title = QLabel("Create New Project")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {theme.TEXT_PRIMARY};")
        layout.addWidget(title)

        # Form
        group = QGroupBox("Project Settings")
        grid = QGridLayout()
        grid.setSpacing(10)

        # Class name
        grid.addWidget(self._make_label("Class Name"), 0, 0)
        self._class_input = QLineEdit(self._class_name)
        self._class_input.setFixedHeight(30)
        grid.addWidget(self._class_input, 0, 1)

        # Window title
        grid.addWidget(self._make_label("Window Title"), 1, 0)
        self._title_input = QLineEdit(self._window_title)
        self._title_input.setFixedHeight(30)
        grid.addWidget(self._title_input, 1, 1)

        # Window size
        grid.addWidget(self._make_label("Width"), 2, 0)
        self._width_spin = QSpinBox()
        self._width_spin.setRange(200, 4000)
        self._width_spin.setValue(self._window_width)
        self._width_spin.setFixedHeight(30)
        grid.addWidget(self._width_spin, 2, 1)

        grid.addWidget(self._make_label("Height"), 3, 0)
        self._height_spin = QSpinBox()
        self._height_spin.setRange(100, 3000)
        self._height_spin.setValue(self._window_height)
        self._height_spin.setFixedHeight(30)
        grid.addWidget(self._height_spin, 3, 1)

        group.setLayout(grid)
        layout.addWidget(group)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedSize(100, 34)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        create_btn = QPushButton("Create")
        create_btn.setObjectName("primary")
        create_btn.setFixedSize(100, 34)
        create_btn.clicked.connect(self._on_create)
        btn_layout.addWidget(create_btn)

        layout.addLayout(btn_layout)

    def _on_create(self) -> None:
        self._class_name = self._class_input.text().strip() or "MyApp"
        self._window_title = self._title_input.text().strip() or "CSSL Application"
        self._window_width = self._width_spin.value()
        self._window_height = self._height_spin.value()
        self.accept()

    @property
    def class_name(self) -> str:
        return self._class_name

    @property
    def window_title(self) -> str:
        return self._window_title

    @property
    def window_width(self) -> int:
        return self._window_width

    @property
    def window_height(self) -> int:
        return self._window_height

    @staticmethod
    def _make_label(text: str) -> QLabel:
        label = QLabel(text)
        label.setStyleSheet(f"color: {theme.TEXT_SECONDARY}; font-size: 12px;")
        label.setFixedWidth(100)
        return label


class CodePreviewDialog(QDialog):
    """Dialog showing generated CSSL code."""

    def __init__(self, code: str, parent: QWidget = None):
        super().__init__(parent)
        self.setWindowTitle("Generated CSSL Code")
        self.resize(700, 550)
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {theme.DARK_BG};
                color: {theme.TEXT_PRIMARY};
            }}
        """)

        self._code = code
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)

        # Title
        title = QLabel("Generated CSSL Code")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {theme.TEXT_PRIMARY};")
        layout.addWidget(title)

        subtitle = QLabel("This is the code that will be saved to your .cssl file.")
        subtitle.setStyleSheet(f"color: {theme.TEXT_MUTED}; font-size: 12px;")
        layout.addWidget(subtitle)

        # Code editor (read-only)
        self._editor = QTextEdit()
        self._editor.setReadOnly(True)
        self._editor.setPlainText(self._code)
        self._editor.setFont(QFont("Consolas", 12))
        self._editor.setStyleSheet(f"""
            QTextEdit {{
                background-color: {theme.DARK_CARD};
                border: 1px solid {theme.DARK_BORDER};
                border-radius: 6px;
                padding: 12px;
                color: {theme.TEXT_PRIMARY};
                font-family: 'Consolas', 'Fira Code', 'Courier New', monospace;
                font-size: 13px;
                line-height: 1.5;
            }}
        """)
        layout.addWidget(self._editor)

        # Buttons
        btn_layout = QHBoxLayout()

        line_count = QLabel(f"{self._code.count(chr(10)) + 1} lines")
        line_count.setStyleSheet(f"color: {theme.TEXT_MUTED}; font-size: 11px;")
        btn_layout.addWidget(line_count)

        btn_layout.addStretch()

        copy_btn = QPushButton("Copy")
        copy_btn.setFixedSize(90, 34)
        copy_btn.clicked.connect(self._copy_to_clipboard)
        btn_layout.addWidget(copy_btn)

        close_btn = QPushButton("Close")
        close_btn.setObjectName("primary")
        close_btn.setFixedSize(90, 34)
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)

        layout.addLayout(btn_layout)

    def _copy_to_clipboard(self) -> None:
        from PyQt6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        if clipboard:
            clipboard.setText(self._code)
