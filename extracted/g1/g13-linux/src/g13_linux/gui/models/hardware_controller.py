"""
Hardware Controller

Unified facade for controlling G13 hardware (LCD and backlight).
"""

from ...hardware.backlight import G13Backlight
from ...hardware.lcd import G13LCD


class HardwareController:
    """Unified hardware control interface for GUI"""

    def __init__(self):
        self.lcd: G13LCD | None = None
        self.backlight: G13Backlight | None = None
        self._initialized = False

    def initialize(self, device_handle):
        """
        Initialize hardware controllers with device.

        Args:
            device_handle: USB device handle from hidapi
        """
        self.lcd = G13LCD(device_handle)
        self.backlight = G13Backlight(device_handle)
        self._initialized = True

    @property
    def is_initialized(self) -> bool:
        """Check if hardware is initialized"""
        return self._initialized

    def set_lcd_text(self, text: str):
        """
        Display text on LCD.

        Args:
            text: Text to display
        """
        if self.lcd:
            self.lcd.clear()
            self.lcd.write_text(text)
        else:
            print(f"[Hardware] LCD not initialized: {text}")

    def clear_lcd(self):
        """Clear LCD display"""
        if self.lcd:
            self.lcd.clear()

    def set_backlight_color(self, color_hex: str):
        """
        Set backlight color from hex string.

        Args:
            color_hex: Color in #RRGGBB format
        """
        if self.backlight:
            self.backlight.set_color_hex(color_hex)
        else:
            print(f"[Hardware] Backlight not initialized: {color_hex}")

    def set_backlight_brightness(self, brightness: int):
        """
        Set backlight brightness.

        Args:
            brightness: Brightness level (0-100)
        """
        if self.backlight:
            self.backlight.set_brightness(brightness)
        else:
            print(f"[Hardware] Backlight not initialized: {brightness}%")

    def get_backlight_color(self) -> tuple[int, int, int] | None:
        """Get current backlight RGB color"""
        if self.backlight:
            return self.backlight.get_color()
        return None

    def get_backlight_brightness(self) -> int | None:
        """Get current backlight brightness"""
        if self.backlight:
            return self.backlight.get_brightness()
        return None
