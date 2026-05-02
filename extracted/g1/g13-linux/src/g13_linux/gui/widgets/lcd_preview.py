"""
LCD Preview Widget

Renders the G13 LCD framebuffer as a visual preview in the GUI.
"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QPainter, QPen
from PyQt6.QtWidgets import QWidget

# LCD dimensions
LCD_WIDTH = 160
LCD_HEIGHT = 43


class LCDPreviewWidget(QWidget):
    """
    Visual preview of the G13 LCD display.

    Renders a 160x43 monochrome framebuffer with classic LCD styling.
    """

    # Signal emitted when LCD content changes
    content_changed = pyqtSignal()

    # LCD colors (classic green monochrome)
    BG_COLOR = QColor(10, 25, 10)  # Dark green background
    PIXEL_ON = QColor(80, 200, 80)  # Bright green for on pixels
    PIXEL_OFF = QColor(15, 35, 15)  # Slightly lighter than bg for off pixels
    BEZEL_COLOR = QColor(20, 20, 22)  # Dark bezel

    def __init__(self, parent=None):
        super().__init__(parent)
        self._framebuffer = bytearray(960)  # 160 * 6 bytes
        self._scale = 2  # Pixel scale factor
        self._show_grid = False

        # Set minimum size based on LCD dimensions + bezel
        bezel = 8
        self.setMinimumSize(
            LCD_WIDTH * self._scale + bezel * 2, LCD_HEIGHT * self._scale + bezel * 2
        )

    def set_framebuffer(self, framebuffer: bytes | bytearray):
        """
        Update the framebuffer and refresh display.

        Args:
            framebuffer: 960-byte LCD framebuffer data
        """
        if len(framebuffer) >= 960:
            self._framebuffer = bytearray(framebuffer[:960])
            self.update()
            self.content_changed.emit()

    def clear(self):
        """Clear the display (all pixels off)."""
        self._framebuffer = bytearray(960)
        self.update()

    def get_pixel(self, x: int, y: int) -> bool:
        """
        Get pixel state from framebuffer.

        Uses G13 LCD row-block byte packing:
        - byte_idx = x + (y // 8) * 160
        - bit_in_byte = y % 8
        """
        if not (0 <= x < LCD_WIDTH and 0 <= y < LCD_HEIGHT):
            return False

        byte_idx = x + (y // 8) * LCD_WIDTH
        bit_in_byte = y % 8

        return bool(self._framebuffer[byte_idx] & (1 << bit_in_byte))

    def set_scale(self, scale: int):
        """Set pixel scale factor (1-4)."""
        self._scale = max(1, min(4, scale))
        bezel = 8
        self.setMinimumSize(
            LCD_WIDTH * self._scale + bezel * 2, LCD_HEIGHT * self._scale + bezel * 2
        )
        self.update()

    def paintEvent(self, event):
        """Render the LCD display."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Widget dimensions
        w = self.width()
        h = self.height()

        # Calculate LCD area with bezel
        bezel = 6
        lcd_w = LCD_WIDTH * self._scale
        lcd_h = LCD_HEIGHT * self._scale

        # Center LCD in widget
        lcd_x = (w - lcd_w) // 2
        lcd_y = (h - lcd_h) // 2

        # Draw bezel (dark frame around LCD)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self.BEZEL_COLOR)
        painter.drawRoundedRect(
            lcd_x - bezel, lcd_y - bezel, lcd_w + bezel * 2, lcd_h + bezel * 2, 4, 4
        )

        # Draw LCD background
        painter.setBrush(self.BG_COLOR)
        painter.drawRect(lcd_x, lcd_y, lcd_w, lcd_h)

        # Draw pixels
        for y in range(LCD_HEIGHT):
            for x in range(LCD_WIDTH):
                pixel_on = self.get_pixel(x, y)

                if pixel_on:
                    painter.setBrush(self.PIXEL_ON)
                else:
                    painter.setBrush(self.PIXEL_OFF)

                px = lcd_x + x * self._scale
                py = lcd_y + y * self._scale

                # Draw pixel (slightly smaller than scale for LCD effect)
                if self._scale > 1:
                    painter.drawRect(px, py, self._scale - 1, self._scale - 1)
                else:
                    painter.drawRect(px, py, 1, 1)

        # Optional: Draw subtle scanline effect
        if self._scale >= 2:
            painter.setPen(QPen(QColor(0, 0, 0, 30), 1))
            for y in range(0, lcd_h, self._scale):
                painter.drawLine(lcd_x, lcd_y + y, lcd_x + lcd_w, lcd_y + y)

        # Draw subtle screen reflection
        painter.setPen(QPen(QColor(100, 150, 100, 20), 1))
        painter.drawLine(lcd_x + 5, lcd_y + 3, lcd_x + lcd_w - 20, lcd_y + 5)


class LCDPreviewEmbedded(LCDPreviewWidget):
    """
    Embedded LCD preview for use within ButtonMapperWidget.

    Designed to fit within the LCD_AREA of the device image.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._scale = 2
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def paintEvent(self, event):
        """Render LCD without external bezel (parent provides context)."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()

        # Calculate scale to fit widget
        scale_x = w / LCD_WIDTH
        scale_y = h / LCD_HEIGHT
        scale = min(scale_x, scale_y)

        lcd_w = int(LCD_WIDTH * scale)
        lcd_h = int(LCD_HEIGHT * scale)
        lcd_x = (w - lcd_w) // 2
        lcd_y = (h - lcd_h) // 2

        # Draw LCD background
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self.BG_COLOR)
        painter.drawRect(lcd_x, lcd_y, lcd_w, lcd_h)

        # Draw pixels
        pixel_w = lcd_w / LCD_WIDTH
        pixel_h = lcd_h / LCD_HEIGHT

        for y in range(LCD_HEIGHT):
            for x in range(LCD_WIDTH):
                if self.get_pixel(x, y):
                    painter.setBrush(self.PIXEL_ON)
                    px = lcd_x + int(x * pixel_w)
                    py = lcd_y + int(y * pixel_h)
                    pw = max(1, int(pixel_w))
                    ph = max(1, int(pixel_h))
                    painter.drawRect(px, py, pw, ph)
