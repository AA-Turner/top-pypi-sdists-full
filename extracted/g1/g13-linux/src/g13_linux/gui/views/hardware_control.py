"""
Hardware Control Widget

LCD and backlight control UI.
"""

from datetime import datetime

from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ..widgets.color_picker import ColorPickerWidget


class HardwareControlWidget(QWidget):
    """LCD and backlight control UI"""

    lcd_text_changed = pyqtSignal(str)
    backlight_color_changed = pyqtSignal(str)  # Hex color
    backlight_brightness_changed = pyqtSignal(int)
    calibration_requested = pyqtSignal()  # Request to open calibration dialog

    def __init__(self, parent=None):
        super().__init__(parent)
        self._clock_enabled = False
        self._clock_timer = QTimer(self)
        self._clock_timer.timeout.connect(self._update_clock)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()

        # LCD Control
        lcd_group = QGroupBox("LCD Display (160x43)")
        lcd_layout = QVBoxLayout()

        lcd_label = QLabel("Text to display:")
        lcd_layout.addWidget(lcd_label)

        self.lcd_text = QTextEdit()
        self.lcd_text.setMaximumHeight(60)
        self.lcd_text.setPlaceholderText("Enter text for LCD...")
        lcd_layout.addWidget(self.lcd_text)

        lcd_btn_layout = QHBoxLayout()
        send_btn = QPushButton("Send to LCD")
        send_btn.clicked.connect(lambda: self.lcd_text_changed.emit(self.lcd_text.toPlainText()))
        lcd_btn_layout.addWidget(send_btn)

        clear_btn = QPushButton("Clear LCD")
        clear_btn.clicked.connect(lambda: self.lcd_text_changed.emit(""))
        lcd_btn_layout.addWidget(clear_btn)

        lcd_layout.addLayout(lcd_btn_layout)

        # Clock display option
        clock_layout = QHBoxLayout()

        self.clock_checkbox = QCheckBox("Show Clock")
        self.clock_checkbox.toggled.connect(self._toggle_clock)
        clock_layout.addWidget(self.clock_checkbox)

        self.clock_format = QComboBox()
        self.clock_format.addItem("24-hour", "24")
        self.clock_format.addItem("12-hour", "12")
        self.clock_format.currentIndexChanged.connect(self._on_format_changed)
        clock_layout.addWidget(self.clock_format)

        self.show_seconds = QCheckBox("Seconds")
        self.show_seconds.setChecked(True)
        self.show_seconds.toggled.connect(self._on_format_changed)
        clock_layout.addWidget(self.show_seconds)

        self.show_date = QCheckBox("Date")
        self.show_date.toggled.connect(self._on_format_changed)
        clock_layout.addWidget(self.show_date)

        clock_layout.addStretch()
        lcd_layout.addLayout(clock_layout)

        lcd_group.setLayout(lcd_layout)
        layout.addWidget(lcd_group)

        # Backlight Control
        backlight_group = QGroupBox("RGB Backlight")
        backlight_layout = QVBoxLayout()

        # Color picker
        color_label = QLabel("Color:")
        backlight_layout.addWidget(color_label)

        self.color_picker = ColorPickerWidget()
        self.color_picker.color_changed.connect(self.backlight_color_changed.emit)
        backlight_layout.addWidget(self.color_picker)

        # Brightness slider
        brightness_label = QLabel("Brightness:")
        backlight_layout.addWidget(brightness_label)

        brightness_layout = QHBoxLayout()
        self.brightness_slider = QSlider(Qt.Orientation.Horizontal)
        self.brightness_slider.setRange(0, 100)
        self.brightness_slider.setValue(100)
        self.brightness_slider.valueChanged.connect(self.backlight_brightness_changed.emit)
        brightness_layout.addWidget(self.brightness_slider)

        self.brightness_value = QLabel("100%")
        self.brightness_slider.valueChanged.connect(
            lambda v: self.brightness_value.setText(f"{v}%")
        )
        brightness_layout.addWidget(self.brightness_value)

        backlight_layout.addLayout(brightness_layout)
        backlight_group.setLayout(backlight_layout)
        layout.addWidget(backlight_group)

        # Button Calibration
        calibration_group = QGroupBox("Button Calibration")
        calibration_layout = QVBoxLayout()

        calibration_desc = QLabel(
            "If button clicks are not registering correctly on the device image, "
            "you can recalibrate the button positions."
        )
        calibration_desc.setWordWrap(True)
        calibration_desc.setStyleSheet("color: #aaa; font-size: 11px;")
        calibration_layout.addWidget(calibration_desc)

        calibrate_btn = QPushButton("Calibrate Button Positions...")
        calibrate_btn.clicked.connect(self.calibration_requested.emit)
        calibration_layout.addWidget(calibrate_btn)

        calibration_group.setLayout(calibration_layout)
        layout.addWidget(calibration_group)

        layout.addStretch()
        self.setLayout(layout)

    def _toggle_clock(self, enabled: bool):
        """Toggle clock display on/off."""
        self._clock_enabled = enabled
        if enabled:
            self._update_clock()  # Immediate update
            self._clock_timer.start(1000)  # Update every second
            self.lcd_text.setEnabled(False)
        else:
            self._clock_timer.stop()
            self.lcd_text.setEnabled(True)

    def _on_format_changed(self):
        """Handle clock format change."""
        if self._clock_enabled:
            self._update_clock()

    def _update_clock(self):
        """Update LCD with current time."""
        now = datetime.now()

        # Time format
        if self.clock_format.currentData() == "12":
            if self.show_seconds.isChecked():
                time_str = now.strftime("%I:%M:%S %p")
            else:
                time_str = now.strftime("%I:%M %p")
        else:
            if self.show_seconds.isChecked():
                time_str = now.strftime("%H:%M:%S")
            else:
                time_str = now.strftime("%H:%M")

        # Date format
        if self.show_date.isChecked():
            date_str = now.strftime("%Y-%m-%d")
            display_text = f"{time_str}\n{date_str}"
        else:
            display_text = time_str

        self.lcd_text_changed.emit(display_text)
