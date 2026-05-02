"""
G13 Backlight Control

Controls the G13's RGB backlight via USB HID feature reports.

Protocol:
- Report ID: 0x07
- Format: [0x07, R, G, B, 0x00] (5 bytes)
"""


class G13Backlight:
    """RGB backlight controller for G13"""

    REPORT_ID = 0x07
    REPORT_SIZE = 5

    def __init__(self, device_handle=None):
        """
        Initialize backlight controller.

        Args:
            device_handle: HidrawDevice instance from device.py
        """
        self.device = device_handle
        self._current_color = (255, 255, 255)  # Default white
        self._current_brightness = 100

    def set_color(self, r: int, g: int, b: int):
        """
        Set RGB backlight color.

        Args:
            r: Red value (0-255)
            g: Green value (0-255)
            b: Blue value (0-255)
        """
        if not all(0 <= val <= 255 for val in (r, g, b)):
            raise ValueError("RGB values must be 0-255")

        self._current_color = (r, g, b)

        if self.device:
            # Send feature report: [report_id, R, G, B, 0x00]
            report = bytes([self.REPORT_ID, r, g, b, 0x00])
            try:
                self.device.send_feature_report(report)
            except OSError as e:
                print(f"[Backlight] Failed to set color: {e}")
        else:
            print(f"[Backlight] No device - would set RGB({r}, {g}, {b})")

    def set_color_hex(self, color_hex: str):
        """
        Set color from hex string.

        Args:
            color_hex: Color in #RRGGBB format
        """
        color_hex = color_hex.lstrip("#")
        if len(color_hex) != 6:
            raise ValueError("Hex color must be in #RRGGBB format")

        try:
            r = int(color_hex[0:2], 16)
            g = int(color_hex[2:4], 16)
            b = int(color_hex[4:6], 16)
            self.set_color(r, g, b)
        except ValueError:
            raise ValueError("Invalid hex color format")

    def set_brightness(self, brightness: int):
        """
        Set brightness level by scaling RGB values.

        Args:
            brightness: Brightness (0-100)
        """
        if not 0 <= brightness <= 100:
            raise ValueError("Brightness must be 0-100")

        self._current_brightness = brightness
        # Re-apply color with brightness scaling
        self._apply_color()

    def _apply_color(self):
        """Apply current color with brightness scaling."""
        r, g, b = self._current_color
        scale = self._current_brightness / 100.0
        scaled_r = int(r * scale)
        scaled_g = int(g * scale)
        scaled_b = int(b * scale)

        if self.device:
            report = bytes([self.REPORT_ID, scaled_r, scaled_g, scaled_b, 0x00])
            try:
                self.device.send_feature_report(report)
            except OSError as e:
                print(f"[Backlight] Failed to apply color: {e}")

    def get_color(self) -> tuple[int, int, int]:
        """Get current RGB color"""
        return self._current_color

    def get_brightness(self) -> int:
        """Get current brightness"""
        return self._current_brightness
