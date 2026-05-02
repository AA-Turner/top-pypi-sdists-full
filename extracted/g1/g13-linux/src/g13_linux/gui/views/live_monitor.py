"""
Live Monitor Widget

Real-time event monitoring and visualization.
"""

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class LiveMonitorWidget(QWidget):
    """Real-time event monitoring and visualization"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.max_lines = 1000
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()

        # Header
        header = QLabel("Live Event Monitor")
        header.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(header)

        # Options
        options_layout = QHBoxLayout()
        self.show_raw = QCheckBox("Show raw HID reports")
        self.show_decoded = QCheckBox("Show decoded events")
        self.show_decoded.setChecked(True)
        options_layout.addWidget(self.show_raw)
        options_layout.addWidget(self.show_decoded)
        options_layout.addStretch()
        layout.addLayout(options_layout)

        # Event log
        self.event_log = QTextEdit()
        self.event_log.setReadOnly(True)
        self.event_log.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                color: #00FF00;
                font-family: monospace;
                font-size: 10px;
            }
        """)
        layout.addWidget(self.event_log)

        # Clear button
        clear_btn = QPushButton("Clear Log")
        clear_btn.clicked.connect(self.clear_log)
        layout.addWidget(clear_btn)

        self.setLayout(layout)

    @pyqtSlot(bytes)
    def on_raw_event(self, data: bytes):
        """Display raw HID report"""
        if self.show_raw.isChecked():
            hex_str = " ".join(f"{b:02x}" for b in data)
            self.append_log(f"RAW: {hex_str}")

    @pyqtSlot(str, bool)
    def on_button_event(self, button_id: str, is_pressed: bool):
        """Display decoded button event"""
        if self.show_decoded.isChecked():
            state_str = "PRESSED" if is_pressed else "RELEASED"
            self.append_log(f"{button_id}: {state_str}")

    @pyqtSlot(int, int)
    def on_joystick_event(self, x: int, y: int):
        """Display joystick movement"""
        if self.show_decoded.isChecked():
            self.append_log(f"JOYSTICK: X={x}, Y={y}")

    def append_log(self, message: str):
        """Add line to log with line limit"""
        self.event_log.append(message)

        # Limit lines (simplified)
        text = self.event_log.toPlainText()
        lines = text.split("\n")
        if len(lines) > self.max_lines:
            self.event_log.setPlainText("\n".join(lines[-self.max_lines :]))

    def clear_log(self):
        """Clear event log"""
        self.event_log.clear()
