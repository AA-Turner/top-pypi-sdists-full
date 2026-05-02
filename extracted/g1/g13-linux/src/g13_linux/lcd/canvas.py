"""
LCD Canvas

Drawing primitives for the G13 160x43 monochrome display.
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .fonts import Font
    from .icons import Icon


@dataclass
class Canvas:
    """
    Drawing canvas for G13 LCD.

    The G13 LCD is 160x43 pixels, monochrome.
    Uses ROW-BLOCK byte packing (same as hardware/lcd.py).
    """

    WIDTH = 160
    HEIGHT = 43
    BUFFER_ROWS = 48  # Buffer has 48 rows (6 bytes × 8 bits)
    FRAMEBUFFER_SIZE = 960  # 160 × 6

    def __init__(self, width: int = 160, height: int = 43):
        """Initialize canvas with given dimensions."""
        self.width = width
        self.height = height
        self._buffer = bytearray(self.FRAMEBUFFER_SIZE)

    def clear(self):
        """Clear canvas (all pixels off)."""
        self._buffer = bytearray(self.FRAMEBUFFER_SIZE)

    def fill(self):
        """Fill canvas (all pixels on)."""
        self._buffer = bytearray([0xFF] * self.FRAMEBUFFER_SIZE)

    def set_pixel(self, x: int, y: int, on: bool = True):
        """
        Set a single pixel.

        Args:
            x: X coordinate (0-159)
            y: Y coordinate (0-42)
            on: True for pixel on, False for off
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            return

        byte_idx = x + (y // 8) * self.WIDTH
        bit_in_byte = y % 8

        if on:
            self._buffer[byte_idx] |= 1 << bit_in_byte
        else:
            self._buffer[byte_idx] &= ~(1 << bit_in_byte)

    def get_pixel(self, x: int, y: int) -> bool:
        """
        Get pixel state.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            True if pixel is on
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False

        byte_idx = x + (y // 8) * self.WIDTH
        bit_in_byte = y % 8
        return bool(self._buffer[byte_idx] & (1 << bit_in_byte))

    def draw_hline(self, x: int, y: int, width: int, on: bool = True):
        """
        Draw horizontal line.

        Args:
            x: Start X
            y: Y position
            width: Line width
            on: Pixel state
        """
        for i in range(width):
            self.set_pixel(x + i, y, on)

    def draw_vline(self, x: int, y: int, height: int, on: bool = True):
        """
        Draw vertical line.

        Args:
            x: X position
            y: Start Y
            height: Line height
            on: Pixel state
        """
        for i in range(height):
            self.set_pixel(x, y + i, on)

    def draw_line(self, x1: int, y1: int, x2: int, y2: int, on: bool = True):
        """
        Draw line using Bresenham's algorithm.

        Args:
            x1, y1: Start point
            x2, y2: End point
            on: Pixel state
        """
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            self.set_pixel(x1, y1, on)
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    def draw_rect(
        self, x: int, y: int, width: int, height: int, filled: bool = False, on: bool = True
    ):
        """
        Draw rectangle.

        Args:
            x, y: Top-left corner
            width, height: Dimensions
            filled: If True, fill the rectangle
            on: Pixel state
        """
        if filled:
            for py in range(height):
                for px in range(width):
                    self.set_pixel(x + px, y + py, on)
        else:
            # Top and bottom
            self.draw_hline(x, y, width, on)
            self.draw_hline(x, y + height - 1, width, on)
            # Left and right
            self.draw_vline(x, y, height, on)
            self.draw_vline(x + width - 1, y, height, on)

    def draw_text(
        self, x: int, y: int, text: str, font: "Font | None" = None, on: bool = True
    ) -> int:
        """
        Draw text at position.

        Args:
            x, y: Position
            text: Text to draw
            font: Font to use (default: 5x7)
            on: Pixel state

        Returns:
            Width of rendered text in pixels
        """
        from .fonts import FONT_5X7

        if font is None:
            font = FONT_5X7

        cursor_x = x
        char_spacing = 1

        for char in text:
            glyph = font.get_glyph(char)
            if glyph is None:
                continue

            # Render each column of the glyph
            for col_idx, col_data in enumerate(glyph):
                px = cursor_x + col_idx
                if px >= self.width:
                    break

                for row in range(font.char_height):
                    py = y + row
                    if py >= self.height:
                        continue
                    if col_data & (1 << row):
                        self.set_pixel(px, py, on)

            cursor_x += font.char_width + char_spacing
            if cursor_x >= self.width:
                break

        return cursor_x - x

    def draw_text_centered(self, y: int, text: str, font: "Font | None" = None, on: bool = True):
        """
        Draw text centered horizontally.

        Args:
            y: Y position
            text: Text to draw
            font: Font to use
            on: Pixel state
        """
        from .fonts import FONT_5X7

        if font is None:
            font = FONT_5X7

        text_width = len(text) * (font.char_width + 1)
        x = max(0, (self.width - text_width) // 2)
        self.draw_text(x, y, text, font, on)

    def draw_icon(self, x: int, y: int, icon: "Icon", on: bool = True):
        """
        Draw icon at position.

        Args:
            x, y: Position
            icon: Icon to draw
            on: Pixel state (inverts icon if False)
        """
        for row in range(icon.height):
            for col in range(icon.width):
                byte_idx = col + (row // 8) * icon.width
                if byte_idx >= len(icon.data):
                    continue
                bit = row % 8
                pixel_on = bool(icon.data[byte_idx] & (1 << bit))
                if on:
                    self.set_pixel(x + col, y + row, pixel_on)
                else:
                    self.set_pixel(x + col, y + row, not pixel_on)

    def draw_progress_bar(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        percent: float,
        filled: bool = True,
    ):
        """
        Draw a progress bar.

        Args:
            x, y: Position
            width, height: Dimensions
            percent: Fill percentage (0.0-100.0)
            filled: If True, use solid fill; if False, use dithered
        """
        # Draw border
        self.draw_rect(x, y, width, height, filled=False)

        # Calculate fill width
        inner_width = width - 2
        inner_height = height - 2
        fill_width = int((percent / 100.0) * inner_width)

        # Fill progress
        if filled:
            self.draw_rect(x + 1, y + 1, fill_width, inner_height, filled=True)
        else:
            # Dithered fill
            for py in range(inner_height):
                for px in range(fill_width):
                    if (px + py) % 2 == 0:
                        self.set_pixel(x + 1 + px, y + 1 + py, True)

    def invert_region(self, x: int, y: int, width: int, height: int):
        """
        Invert a rectangular region.

        Args:
            x, y: Top-left corner
            width, height: Dimensions
        """
        for py in range(height):
            for px in range(width):
                current = self.get_pixel(x + px, y + py)
                self.set_pixel(x + px, y + py, not current)

    def blit(self, other: "Canvas", x: int, y: int):
        """
        Copy another canvas onto this one.

        Args:
            other: Source canvas
            x, y: Position to place source
        """
        for py in range(other.height):
            for px in range(other.width):
                if other.get_pixel(px, py):
                    self.set_pixel(x + px, y + py, True)

    def to_bytes(self) -> bytes:
        """
        Get framebuffer as bytes.

        Returns:
            960-byte framebuffer suitable for LCDDisplay.write_frame()
        """
        return bytes(self._buffer)

    def from_bytes(self, data: bytes):
        """
        Load framebuffer from bytes.

        Args:
            data: 960-byte framebuffer
        """
        if len(data) > self.FRAMEBUFFER_SIZE:
            data = data[: self.FRAMEBUFFER_SIZE]
        self._buffer = bytearray(data)
        # Pad if needed
        if len(self._buffer) < self.FRAMEBUFFER_SIZE:
            self._buffer.extend([0] * (self.FRAMEBUFFER_SIZE - len(self._buffer)))
