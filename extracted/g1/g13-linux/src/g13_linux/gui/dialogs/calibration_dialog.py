"""
Calibration Dialog

Interactive G13 button position calibrator integrated into the GUI.
Click on the device image to set button positions.
"""

from pathlib import Path

from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtGui import QColor, QMouseEvent, QPainter, QPen, QPixmap
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)

# Button click order - includes LCD area first for reference positioning
BUTTON_ORDER = [
    "LCD",  # LCD display area (click top-left, then bottom-right)
    "M1",
    "M2",
    "M3",
    "MR",
    "G1",
    "G2",
    "G3",
    "G4",
    "G5",
    "G6",
    "G7",
    "G8",
    "G9",
    "G10",
    "G11",
    "G12",
    "G13",
    "G14",
    "G15",
    "G16",
    "G17",
    "G18",
    "G19",
    "G20",
    "G21",
    "G22",
    "LEFT",
    "DOWN",
    "STICK",
]

# Special items that need two clicks (top-left and bottom-right)
TWO_CLICK_ITEMS = {"LCD", "STICK"}

# Default button sizes
BUTTON_SIZES = {
    "M": (28, 18),  # M-keys (small)
    "G_SMALL": (38, 28),  # G1-G19 (standard)
    "G_WIDE": (42, 28),  # G20-G22 (wider)
    "LEFT": (28, 22),
    "DOWN": (28, 22),
    "STICK": (35, 35),
}


def get_button_size(name: str) -> tuple[int, int]:
    """Get default size for a button."""
    if name.startswith("M"):
        return BUTTON_SIZES["M"]
    if name in ("G20", "G21", "G22"):
        return BUTTON_SIZES["G_WIDE"]
    if name.startswith("G"):
        return BUTTON_SIZES["G_SMALL"]
    return BUTTON_SIZES.get(name, (30, 25))


class ClickableImageLabel(QLabel):
    """Clickable image label that reports click positions."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.click_callback = None

    def mousePressEvent(self, event: QMouseEvent):
        if self.click_callback:
            self.click_callback(event.pos().x(), event.pos().y())


class CalibrationDialog(QDialog):
    """Interactive G13 button position calibrator dialog."""

    # Emitted when calibration is complete with the positions dict
    calibration_complete = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("G13 Button Position Calibrator")
        self.setModal(True)

        # Find the device image
        self.image_path = self._find_device_image()
        if not self.image_path:
            QMessageBox.critical(
                self,
                "Error",
                "Device image not found. Cannot calibrate.",
            )
            return

        self.original_pixmap = QPixmap(str(self.image_path))
        self.positions: dict[str, tuple[int, int, int, int]] = {}
        self.current_idx = 0
        self._pending_first_click: tuple[int, int] | None = None

        self._init_ui()
        self._update_status()

    def _find_device_image(self) -> Path | None:
        """Find the G13 device image."""
        # Try relative to this file
        current_dir = Path(__file__).parent
        gui_dir = current_dir.parent
        image_path = gui_dir / "resources" / "images" / "g13_device.png"

        if image_path.exists():
            return image_path

        return None

    def _init_ui(self):
        """Setup the UI."""
        main_layout = QHBoxLayout()

        # Left side: image
        left_layout = QVBoxLayout()

        # Status/instruction label
        self.status_label = QLabel()
        self.status_label.setStyleSheet(
            "font-size: 14px; font-weight: bold; padding: 8px; "
            "background: #333; color: #0f0; border-radius: 4px;"
        )
        left_layout.addWidget(self.status_label)

        # Clickable image
        self.image_label = ClickableImageLabel()
        self.image_label.setPixmap(self.original_pixmap)
        self.image_label.click_callback = self._on_click
        left_layout.addWidget(self.image_label)

        # Control buttons
        btn_layout = QHBoxLayout()

        self.undo_btn = QPushButton("Undo Last")
        self.undo_btn.clicked.connect(self._undo_last)
        btn_layout.addWidget(self.undo_btn)

        self.reset_btn = QPushButton("Reset All")
        self.reset_btn.clicked.connect(self._reset_all)
        btn_layout.addWidget(self.reset_btn)

        btn_layout.addStretch()

        self.skip_btn = QPushButton("Skip Current")
        self.skip_btn.clicked.connect(self._skip_current)
        btn_layout.addWidget(self.skip_btn)

        left_layout.addLayout(btn_layout)
        main_layout.addLayout(left_layout)

        # Right side: output and actions
        right_layout = QVBoxLayout()
        right_layout.setMinimumWidth(350)

        # Progress indicator
        self.progress_label = QLabel()
        self.progress_label.setStyleSheet("font-size: 12px; color: #aaa;")
        right_layout.addWidget(self.progress_label)

        right_layout.addWidget(QLabel("Generated Code:"))

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setStyleSheet(
            "font-family: monospace; font-size: 10px; background: #1e1e1e; color: #ddd;"
        )
        right_layout.addWidget(self.output_text)

        # Action buttons
        action_layout = QHBoxLayout()

        self.copy_btn = QPushButton("Copy to Clipboard")
        self.copy_btn.clicked.connect(self._copy_to_clipboard)
        action_layout.addWidget(self.copy_btn)

        right_layout.addLayout(action_layout)

        # Dialog buttons
        dialog_btn_layout = QHBoxLayout()
        dialog_btn_layout.addStretch()

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        dialog_btn_layout.addWidget(self.cancel_btn)

        self.apply_btn = QPushButton("Apply Calibration")
        self.apply_btn.setEnabled(False)
        self.apply_btn.clicked.connect(self._apply_calibration)
        self.apply_btn.setStyleSheet(
            "QPushButton { background: #2a5a2a; color: white; padding: 8px 16px; }"
            "QPushButton:disabled { background: #333; color: #666; }"
        )
        dialog_btn_layout.addWidget(self.apply_btn)

        right_layout.addLayout(dialog_btn_layout)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

    def _update_status(self):
        """Update the status label and progress."""
        total = len(BUTTON_ORDER)
        current = self.current_idx

        self.progress_label.setText(f"Progress: {current}/{total} buttons calibrated")

        if current < total:
            btn = BUTTON_ORDER[current]
            is_two_click = btn in TWO_CLICK_ITEMS

            if is_two_click and self._pending_first_click is not None:
                self.status_label.setText(f"Click BOTTOM-RIGHT corner of: {btn}")
                self.status_label.setStyleSheet(
                    "font-size: 14px; font-weight: bold; padding: 8px; "
                    "background: #630; color: #ff0; border-radius: 4px;"
                )
            elif is_two_click:
                self.status_label.setText(f"Click TOP-LEFT corner of: {btn} [2-click item]")
                self.status_label.setStyleSheet(
                    "font-size: 14px; font-weight: bold; padding: 8px; "
                    "background: #036; color: #0ff; border-radius: 4px;"
                )
            else:
                self.status_label.setText(f"Click TOP-LEFT corner of: {btn}")
                self.status_label.setStyleSheet(
                    "font-size: 14px; font-weight: bold; padding: 8px; "
                    "background: #333; color: #0f0; border-radius: 4px;"
                )

            self.apply_btn.setEnabled(False)
        else:
            self.status_label.setText("✓ All buttons mapped!")
            self.status_label.setStyleSheet(
                "font-size: 14px; font-weight: bold; padding: 8px; "
                "background: #060; color: #fff; border-radius: 4px;"
            )
            self.apply_btn.setEnabled(True)

    def _on_click(self, x: int, y: int):
        """Handle click on image."""
        if self.current_idx >= len(BUTTON_ORDER):
            return

        btn_name = BUTTON_ORDER[self.current_idx]
        is_two_click = btn_name in TWO_CLICK_ITEMS

        if is_two_click:
            if self._pending_first_click is None:
                # First click - store top-left corner
                self._pending_first_click = (x, y)
                self._update_status()
                self._update_preview()
                return
            else:
                # Second click - calculate width/height from corners
                x1, y1 = self._pending_first_click
                w = max(1, x - x1)
                h = max(1, y - y1)
                self.positions[btn_name] = (x1, y1, w, h)
                self._pending_first_click = None
        else:
            # Regular single-click button
            w, h = get_button_size(btn_name)
            self.positions[btn_name] = (x, y, w, h)

        self.current_idx += 1

        self._update_preview()
        self._update_status()
        self._generate_output()

    def _update_preview(self):
        """Update the image with button overlays."""
        pixmap = QPixmap(str(self.image_path))
        painter = QPainter(pixmap)

        for name, (x, y, w, h) in self.positions.items():
            # Use different colors for different element types
            if name == "LCD":
                painter.setPen(QPen(QColor(0, 200, 255), 2))  # Cyan for LCD
            elif name == "STICK":
                painter.setPen(QPen(QColor(255, 100, 0), 2))  # Orange for joystick
            else:
                painter.setPen(QPen(QColor(0, 255, 0), 2))  # Green for buttons

            painter.drawRect(x, y, w, h)

            # Draw label
            painter.setPen(QColor(255, 255, 0))
            painter.drawText(x + 2, y + h - 3, name)

        # Show pending first click for two-click items
        if self._pending_first_click is not None:
            x, y = self._pending_first_click
            painter.setPen(QPen(QColor(255, 0, 255), 3))  # Magenta marker
            painter.drawLine(x - 10, y, x + 10, y)
            painter.drawLine(x, y - 10, x, y + 10)
            painter.drawEllipse(x - 5, y - 5, 10, 10)

        painter.end()
        self.image_label.setPixmap(pixmap)

    def _generate_output(self):
        """Generate the Python code."""
        lines = [
            '"""G13 Button Layout - Generated by Calibration Dialog"""',
            "",
            "KEYBOARD_WIDTH = 1024",
            "KEYBOARD_HEIGHT = 1024",
            "",
            "",
            "def _box(x, y, w, h):",
            '    """Create position dict."""',
            '    return {"x": int(x), "y": int(y), "width": int(w), "height": int(h)}',
            "",
            "",
            "G13_BUTTON_POSITIONS = {",
        ]

        # Group by row for readability
        groups = [
            ("# M-keys row", ["M1", "M2", "M3", "MR"]),
            ("# Row 1: G1-G7", ["G1", "G2", "G3", "G4", "G5", "G6", "G7"]),
            ("# Row 2: G8-G14", ["G8", "G9", "G10", "G11", "G12", "G13", "G14"]),
            ("# Row 3: G15-G19", ["G15", "G16", "G17", "G18", "G19"]),
            ("# Row 4: G20-G22", ["G20", "G21", "G22"]),
            ("# Thumb buttons", ["LEFT", "DOWN", "STICK"]),
        ]

        for comment, buttons in groups:
            has_any = any(b in self.positions for b in buttons)
            if has_any:
                lines.append(f"    {comment}")
                for name in buttons:
                    if name in self.positions:
                        x, y, w, h = self.positions[name]
                        lines.append(f'    "{name}": _box({x}, {y}, {w}, {h}),')
                lines.append("")

        lines.append("}")
        lines.append("")

        # Add JOYSTICK_AREA if STICK is defined
        if "STICK" in self.positions:
            x, y, w, h = self.positions["STICK"]
            lines.append(f'JOYSTICK_AREA = {{"x": {x}, "y": {y}, "width": {w}, "height": {h}}}')

        # Add LCD_AREA if LCD is defined
        if "LCD" in self.positions:
            x, y, w, h = self.positions["LCD"]
            lines.append(f'LCD_AREA = {{"x": {x}, "y": {y}, "width": {w}, "height": {h}}}')
        else:
            lines.append('LCD_AREA = {"x": 385, "y": 158, "width": 160, "height": 45}  # Default')

        self.output_text.setText("\n".join(lines))

    def _undo_last(self):
        """Undo the last button placement."""
        # If we're in the middle of a two-click item, cancel it
        if self._pending_first_click is not None:
            self._pending_first_click = None
            self._update_preview()
            self._update_status()
            return

        if self.current_idx > 0:
            self.current_idx -= 1
            btn_name = BUTTON_ORDER[self.current_idx]
            if btn_name in self.positions:
                del self.positions[btn_name]
            self._update_preview()
            self._update_status()
            self._generate_output()

    def _reset_all(self):
        """Reset all button placements."""
        self.positions.clear()
        self.current_idx = 0
        self._pending_first_click = None
        self.image_label.setPixmap(self.original_pixmap)
        self._update_status()
        self.output_text.clear()

    def _skip_current(self):
        """Skip the current button (use default size at 0,0)."""
        if self.current_idx >= len(BUTTON_ORDER):
            return

        # Cancel any pending two-click
        self._pending_first_click = None

        # Move to next button without recording position
        self.current_idx += 1
        self._update_status()
        self._generate_output()

    def _copy_to_clipboard(self):
        """Copy generated code to clipboard."""
        from PyQt6.QtWidgets import QApplication

        QApplication.clipboard().setText(self.output_text.toPlainText())
        self.copy_btn.setText("Copied!")
        QTimer.singleShot(2000, lambda: self.copy_btn.setText("Copy to Clipboard"))

    def _apply_calibration(self):
        """Apply the calibration and close dialog."""
        # Emit the positions
        self.calibration_complete.emit(self.positions)
        self.accept()

    def get_positions(self) -> dict[str, tuple[int, int, int, int]]:
        """Get the calibrated positions."""
        return self.positions.copy()
