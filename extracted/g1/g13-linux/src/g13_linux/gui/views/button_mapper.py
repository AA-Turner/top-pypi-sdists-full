"""
Button Mapper Widget

Visual G13 keyboard layout with clickable buttons.
"""

import os

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QPainter, QPen, QPixmap
from PyQt6.QtWidgets import QWidget

from ..resources.g13_layout import (
    G13_BUTTON_POSITIONS,
    JOYSTICK_AREA,
    KEYBOARD_HEIGHT,
    KEYBOARD_WIDTH,
    LCD_AREA,
)
from ..widgets.g13_button import G13Button
from ..widgets.lcd_preview import LCDPreviewEmbedded


class ButtonMapperWidget(QWidget):
    """Visual G13 keyboard layout with clickable buttons"""

    button_clicked = pyqtSignal(str)  # Button ID clicked for configuration

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(KEYBOARD_WIDTH, KEYBOARD_HEIGHT)
        self.buttons = {}
        self.background_image = self._load_background_image()
        self._init_buttons()
        self._init_lcd_preview()
        # Joystick position (0-255 for X and Y, 128 = center)
        self._joystick_x = 128
        self._joystick_y = 128

    def _init_lcd_preview(self):
        """Create LCD preview widget positioned over LCD area."""
        self.lcd_preview = LCDPreviewEmbedded(self)
        self.lcd_preview.setGeometry(
            LCD_AREA["x"],
            LCD_AREA["y"],
            LCD_AREA["width"],
            LCD_AREA["height"],
        )
        # Hide by default - the reference image already shows the LCD
        self.lcd_preview.hide()

    def update_lcd(self, framebuffer: bytes | bytearray):
        """Update LCD preview with new framebuffer data."""
        self.lcd_preview.set_framebuffer(framebuffer)

    def clear_lcd(self):
        """Clear the LCD preview."""
        self.lcd_preview.clear()

    def _load_background_image(self):
        """Load G13 device background image if available"""
        # Try to find the image in the resources directory
        possible_paths = [
            os.path.join(os.path.dirname(__file__), "..", "resources", "images", "g13_device.png"),
            os.path.join(os.path.dirname(__file__), "..", "resources", "images", "g13_layout.png"),
            os.path.join(os.path.dirname(__file__), "..", "resources", "images", "g13_layout.jpg"),
        ]

        for path in possible_paths:
            if os.path.exists(path):
                pixmap = QPixmap(path)
                if not pixmap.isNull():
                    # Scale to exactly match widget dimensions
                    return pixmap.scaled(
                        KEYBOARD_WIDTH,
                        KEYBOARD_HEIGHT,
                        Qt.AspectRatioMode.IgnoreAspectRatio,
                        Qt.TransformationMode.SmoothTransformation,
                    )
        return None

    def _init_buttons(self):
        """Create all G13 buttons based on layout"""
        for button_id, position in G13_BUTTON_POSITIONS.items():
            btn = G13Button(button_id, self)
            btn.clicked.connect(lambda checked=False, bid=button_id: self.button_clicked.emit(bid))
            self.buttons[button_id] = btn
        # Position buttons after creation
        self._update_button_positions()

    def _update_button_positions(self):
        """Update button positions based on current widget size"""
        # Calculate scale factors
        scale_x = self.width() / KEYBOARD_WIDTH
        scale_y = self.height() / KEYBOARD_HEIGHT

        for button_id, position in G13_BUTTON_POSITIONS.items():
            if button_id in self.buttons:
                btn = self.buttons[button_id]
                x = int(position["x"] * scale_x)
                y = int(position["y"] * scale_y)
                w = int(position["width"] * scale_x)
                h = int(position["height"] * scale_y)
                btn.setGeometry(x, y, w, h)

    def resizeEvent(self, event):
        """Handle widget resize - scale buttons and LCD preview"""
        super().resizeEvent(event)
        self._update_button_positions()

        # Update LCD preview position
        scale_x = self.width() / KEYBOARD_WIDTH
        scale_y = self.height() / KEYBOARD_HEIGHT
        self.lcd_preview.setGeometry(
            int(LCD_AREA["x"] * scale_x),
            int(LCD_AREA["y"] * scale_y),
            int(LCD_AREA["width"] * scale_x),
            int(LCD_AREA["height"] * scale_y),
        )

        # Scale background image to current size
        if self.background_image:
            self.background_image = self._load_background_image()
            if self.background_image:
                self.background_image = self.background_image.scaled(
                    self.width(),
                    self.height(),
                    Qt.AspectRatioMode.IgnoreAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )

    def set_button_mapping(self, button_id: str, key_name: str):
        """Update button label with mapped key"""
        if button_id in self.buttons:
            self.buttons[button_id].set_mapping(key_name)

    def highlight_button(self, button_id: str, highlight: bool):
        """Highlight button when physically pressed"""
        if button_id in self.buttons:
            self.buttons[button_id].set_highlighted(highlight)

    def clear_all_highlights(self):
        """Clear all button highlights"""
        for btn in self.buttons.values():
            btn.set_highlighted(False)

    def update_button_positions(
        self,
        button_positions: dict,
        lcd_area: dict | None = None,
        joystick_area: dict | None = None,
    ):
        """Update button positions from calibration.

        Args:
            button_positions: Dict of button_id -> {x, y, width, height}
            lcd_area: Optional LCD area position dict
            joystick_area: Optional joystick area position dict
        """
        # Update the module-level positions (for this session only)
        global G13_BUTTON_POSITIONS, LCD_AREA, JOYSTICK_AREA

        # Merge new positions with existing
        for button_id, pos in button_positions.items():
            G13_BUTTON_POSITIONS[button_id] = pos

        if lcd_area:
            # Update LCD area - need to reassign since it's a dict
            LCD_AREA.update(lcd_area)

        if joystick_area:
            JOYSTICK_AREA.update(joystick_area)

        # Refresh all button positions
        self._update_button_positions()

        # Update LCD preview position
        scale_x = self.width() / KEYBOARD_WIDTH
        scale_y = self.height() / KEYBOARD_HEIGHT
        self.lcd_preview.setGeometry(
            int(LCD_AREA["x"] * scale_x),
            int(LCD_AREA["y"] * scale_y),
            int(LCD_AREA["width"] * scale_x),
            int(LCD_AREA["height"] * scale_y),
        )

        # Trigger repaint
        self.update()

    def update_joystick(self, x: int, y: int):
        """Update joystick position indicator (0-255 for each axis)"""
        self._joystick_x = x
        self._joystick_y = y
        self.update()  # Trigger repaint

    def paintEvent(self, event):
        """Draw G13 keyboard layout - dark theme matching real device"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self.background_image:
            # Draw the background image
            painter.drawPixmap(0, 0, self.background_image)
        else:
            # Draw G13-style dark background
            self._draw_device_background(painter)

            # Draw LCD area with green/black display look
            self._draw_lcd_area(painter)

        # Draw joystick position indicator
        self._draw_joystick_indicator(painter)

    def _draw_device_background(self, painter: QPainter):
        """Draw dark G13 device background with curved shape"""
        # Dark background for entire widget
        painter.fillRect(0, 0, KEYBOARD_WIDTH, KEYBOARD_HEIGHT, QColor(20, 20, 22))

        # Main device body outline - rounded rectangle with G13 proportions
        body_rect = (30, 80, KEYBOARD_WIDTH - 60, KEYBOARD_HEIGHT - 150)

        # Draw outer glow/edge
        painter.setPen(QPen(QColor(60, 60, 65), 4))
        painter.setBrush(QColor(35, 35, 38))
        painter.drawRoundedRect(*body_rect, 40, 40)

        # Inner body with subtle gradient
        inner_rect = (35, 85, KEYBOARD_WIDTH - 70, KEYBOARD_HEIGHT - 160)
        painter.setPen(QPen(QColor(50, 50, 55), 2))
        painter.setBrush(QColor(28, 28, 32))
        painter.drawRoundedRect(*inner_rect, 35, 35)

        # Palm rest area (bottom curved section)
        palm_rect = (80, KEYBOARD_HEIGHT - 350, KEYBOARD_WIDTH - 160, 280)
        painter.setPen(QPen(QColor(45, 45, 50), 2))
        painter.setBrush(QColor(25, 25, 28))
        painter.drawRoundedRect(*palm_rect, 60, 60)

    def _draw_lcd_area(self, painter: QPainter):
        """Draw LCD display area with authentic green/black look"""
        x, y, w, h = LCD_AREA["x"], LCD_AREA["y"], LCD_AREA["width"], LCD_AREA["height"]

        # LCD bezel (dark frame around screen)
        bezel_margin = 8
        painter.setPen(QPen(QColor(20, 20, 22), 3))
        painter.setBrush(QColor(15, 15, 18))
        painter.drawRoundedRect(
            x - bezel_margin, y - bezel_margin, w + bezel_margin * 2, h + bezel_margin * 2, 8, 8
        )

        # LCD screen - classic green/black monochrome look
        painter.setPen(QPen(QColor(30, 80, 30), 2))
        painter.setBrush(QColor(10, 25, 10))  # Very dark green background
        painter.drawRect(x, y, w, h)

        # LCD text area with scanline effect hint
        painter.setPen(QColor(40, 120, 40))
        painter.setFont(QFont("Courier", 11, QFont.Weight.Bold))
        painter.drawText(x + 15, y + 35, "G13 LCD Display")
        painter.setFont(QFont("Courier", 9))
        painter.setPen(QColor(30, 90, 30))
        painter.drawText(x + 15, y + 55, "160 x 43 pixels")

        # Subtle screen reflection/glare line
        painter.setPen(QPen(QColor(50, 100, 50, 40), 1))
        painter.drawLine(x + 10, y + 10, x + w - 30, y + 15)

    def _draw_joystick_indicator(self, painter: QPainter):
        """Draw thumbstick area matching G13's actual joystick look"""
        center_x = JOYSTICK_AREA["x"] + JOYSTICK_AREA["width"] // 2
        center_y = JOYSTICK_AREA["y"] + JOYSTICK_AREA["height"] // 2
        radius = min(JOYSTICK_AREA["width"], JOYSTICK_AREA["height"]) // 2 - 5

        # Outer housing ring (dark metal look)
        painter.setPen(QPen(QColor(45, 45, 50), 3))
        painter.setBrush(QColor(30, 30, 35))
        painter.drawEllipse(
            center_x - radius - 5, center_y - radius - 5, (radius + 5) * 2, (radius + 5) * 2
        )

        # Inner recessed area (where stick moves)
        painter.setPen(QPen(QColor(25, 25, 28), 2))
        painter.setBrush(QColor(18, 18, 22))
        painter.drawEllipse(center_x - radius, center_y - radius, radius * 2, radius * 2)

        # Map joystick position (0-255) to pixel offset from center
        offset_x = int((self._joystick_x - 128) / 128 * (radius - 20))
        offset_y = int((self._joystick_y - 128) / 128 * (radius - 20))

        # Draw thumbstick cap (rubber texture look)
        stick_x = center_x + offset_x
        stick_y = center_y + offset_y
        stick_radius = 25

        # Stick shadow
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(10, 10, 12, 150))
        painter.drawEllipse(
            stick_x - stick_radius + 3,
            stick_y - stick_radius + 3,
            stick_radius * 2,
            stick_radius * 2,
        )

        # Stick base (dark rubber)
        painter.setPen(QPen(QColor(50, 50, 55), 2))
        painter.setBrush(QColor(35, 35, 40))
        painter.drawEllipse(
            stick_x - stick_radius, stick_y - stick_radius, stick_radius * 2, stick_radius * 2
        )

        # Stick top with concave grip pattern
        inner_radius = stick_radius - 5
        painter.setPen(QPen(QColor(60, 60, 65), 1))
        painter.setBrush(QColor(45, 45, 50))
        painter.drawEllipse(
            stick_x - inner_radius, stick_y - inner_radius, inner_radius * 2, inner_radius * 2
        )

        # Center dimple (like real thumbstick)
        dimple_radius = 8
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(35, 35, 40))
        painter.drawEllipse(
            stick_x - dimple_radius, stick_y - dimple_radius, dimple_radius * 2, dimple_radius * 2
        )

        # Position indicator - subtle colored ring based on deflection
        distance = (offset_x**2 + offset_y**2) ** 0.5
        max_distance = radius - 20
        intensity = min(distance / max_distance, 1.0) if max_distance > 0 else 0

        if intensity > 0.1:
            # Show activity with teal glow (matches G13 backlight theme)
            glow_color = QColor(
                0, int(150 + 50 * intensity), int(150 + 50 * intensity), int(100 * intensity)
            )
            painter.setPen(QPen(glow_color, 2))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawEllipse(
                stick_x - stick_radius - 2,
                stick_y - stick_radius - 2,
                (stick_radius + 2) * 2,
                (stick_radius + 2) * 2,
            )
