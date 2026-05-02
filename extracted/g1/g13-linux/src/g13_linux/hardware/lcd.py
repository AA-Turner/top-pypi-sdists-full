"""
G13 LCD Control

Controls the G13's 160x43 monochrome LCD display.

Protocol (from g13-rs/libg13):
- LCD is 160x43 pixels, monochrome (1 bit per pixel)
- Framebuffer size: 960 bytes
- Send format: 32-byte header (first byte = 0x03) + 960-byte framebuffer
- Total packet: 992 bytes via interrupt transfer to endpoint 2
"""

# 5x7 font table - each character is 5 columns of 7 bits (stored as 5 bytes)
# Characters 32-126 (space to ~)
FONT_5X7 = {
    32: [0x00, 0x00, 0x00, 0x00, 0x00],  # space
    33: [0x00, 0x00, 0x5F, 0x00, 0x00],  # !
    34: [0x00, 0x07, 0x00, 0x07, 0x00],  # "
    35: [0x14, 0x7F, 0x14, 0x7F, 0x14],  # #
    36: [0x24, 0x2A, 0x7F, 0x2A, 0x12],  # $
    37: [0x23, 0x13, 0x08, 0x64, 0x62],  # %
    38: [0x36, 0x49, 0x55, 0x22, 0x50],  # &
    39: [0x00, 0x05, 0x03, 0x00, 0x00],  # '
    40: [0x00, 0x1C, 0x22, 0x41, 0x00],  # (
    41: [0x00, 0x41, 0x22, 0x1C, 0x00],  # )
    42: [0x08, 0x2A, 0x1C, 0x2A, 0x08],  # *
    43: [0x08, 0x08, 0x3E, 0x08, 0x08],  # +
    44: [0x00, 0x50, 0x30, 0x00, 0x00],  # ,
    45: [0x08, 0x08, 0x08, 0x08, 0x08],  # -
    46: [0x00, 0x60, 0x60, 0x00, 0x00],  # .
    47: [0x20, 0x10, 0x08, 0x04, 0x02],  # /
    48: [0x3E, 0x51, 0x49, 0x45, 0x3E],  # 0
    49: [0x00, 0x42, 0x7F, 0x40, 0x00],  # 1
    50: [0x42, 0x61, 0x51, 0x49, 0x46],  # 2
    51: [0x21, 0x41, 0x45, 0x4B, 0x31],  # 3
    52: [0x18, 0x14, 0x12, 0x7F, 0x10],  # 4
    53: [0x27, 0x45, 0x45, 0x45, 0x39],  # 5
    54: [0x3C, 0x4A, 0x49, 0x49, 0x30],  # 6
    55: [0x01, 0x71, 0x09, 0x05, 0x03],  # 7
    56: [0x36, 0x49, 0x49, 0x49, 0x36],  # 8
    57: [0x06, 0x49, 0x49, 0x29, 0x1E],  # 9
    58: [0x00, 0x36, 0x36, 0x00, 0x00],  # :
    59: [0x00, 0x56, 0x36, 0x00, 0x00],  # ;
    60: [0x00, 0x08, 0x14, 0x22, 0x41],  # <
    61: [0x14, 0x14, 0x14, 0x14, 0x14],  # =
    62: [0x41, 0x22, 0x14, 0x08, 0x00],  # >
    63: [0x02, 0x01, 0x51, 0x09, 0x06],  # ?
    64: [0x32, 0x49, 0x79, 0x41, 0x3E],  # @
    65: [0x7E, 0x11, 0x11, 0x11, 0x7E],  # A
    66: [0x7F, 0x49, 0x49, 0x49, 0x36],  # B
    67: [0x3E, 0x41, 0x41, 0x41, 0x22],  # C
    68: [0x7F, 0x41, 0x41, 0x22, 0x1C],  # D
    69: [0x7F, 0x49, 0x49, 0x49, 0x41],  # E
    70: [0x7F, 0x09, 0x09, 0x01, 0x01],  # F
    71: [0x3E, 0x41, 0x41, 0x51, 0x32],  # G
    72: [0x7F, 0x08, 0x08, 0x08, 0x7F],  # H
    73: [0x00, 0x41, 0x7F, 0x41, 0x00],  # I
    74: [0x20, 0x40, 0x41, 0x3F, 0x01],  # J
    75: [0x7F, 0x08, 0x14, 0x22, 0x41],  # K
    76: [0x7F, 0x40, 0x40, 0x40, 0x40],  # L
    77: [0x7F, 0x02, 0x04, 0x02, 0x7F],  # M
    78: [0x7F, 0x04, 0x08, 0x10, 0x7F],  # N
    79: [0x3E, 0x41, 0x41, 0x41, 0x3E],  # O
    80: [0x7F, 0x09, 0x09, 0x09, 0x06],  # P
    81: [0x3E, 0x41, 0x51, 0x21, 0x5E],  # Q
    82: [0x7F, 0x09, 0x19, 0x29, 0x46],  # R
    83: [0x46, 0x49, 0x49, 0x49, 0x31],  # S
    84: [0x01, 0x01, 0x7F, 0x01, 0x01],  # T
    85: [0x3F, 0x40, 0x40, 0x40, 0x3F],  # U
    86: [0x1F, 0x20, 0x40, 0x20, 0x1F],  # V
    87: [0x7F, 0x20, 0x18, 0x20, 0x7F],  # W
    88: [0x63, 0x14, 0x08, 0x14, 0x63],  # X
    89: [0x03, 0x04, 0x78, 0x04, 0x03],  # Y
    90: [0x61, 0x51, 0x49, 0x45, 0x43],  # Z
    91: [0x00, 0x00, 0x7F, 0x41, 0x41],  # [
    92: [0x02, 0x04, 0x08, 0x10, 0x20],  # \
    93: [0x41, 0x41, 0x7F, 0x00, 0x00],  # ]
    94: [0x04, 0x02, 0x01, 0x02, 0x04],  # ^
    95: [0x40, 0x40, 0x40, 0x40, 0x40],  # _
    96: [0x00, 0x01, 0x02, 0x04, 0x00],  # `
    97: [0x20, 0x54, 0x54, 0x54, 0x78],  # a
    98: [0x7F, 0x48, 0x44, 0x44, 0x38],  # b
    99: [0x38, 0x44, 0x44, 0x44, 0x20],  # c
    100: [0x38, 0x44, 0x44, 0x48, 0x7F],  # d
    101: [0x38, 0x54, 0x54, 0x54, 0x18],  # e
    102: [0x08, 0x7E, 0x09, 0x01, 0x02],  # f
    103: [0x08, 0x14, 0x54, 0x54, 0x3C],  # g
    104: [0x7F, 0x08, 0x04, 0x04, 0x78],  # h
    105: [0x00, 0x44, 0x7D, 0x40, 0x00],  # i
    106: [0x20, 0x40, 0x44, 0x3D, 0x00],  # j
    107: [0x00, 0x7F, 0x10, 0x28, 0x44],  # k
    108: [0x00, 0x41, 0x7F, 0x40, 0x00],  # l
    109: [0x7C, 0x04, 0x18, 0x04, 0x78],  # m
    110: [0x7C, 0x08, 0x04, 0x04, 0x78],  # n
    111: [0x38, 0x44, 0x44, 0x44, 0x38],  # o
    112: [0x7C, 0x14, 0x14, 0x14, 0x08],  # p
    113: [0x08, 0x14, 0x14, 0x18, 0x7C],  # q
    114: [0x7C, 0x08, 0x04, 0x04, 0x08],  # r
    115: [0x48, 0x54, 0x54, 0x54, 0x20],  # s
    116: [0x04, 0x3F, 0x44, 0x40, 0x20],  # t
    117: [0x3C, 0x40, 0x40, 0x20, 0x7C],  # u
    118: [0x1C, 0x20, 0x40, 0x20, 0x1C],  # v
    119: [0x3C, 0x40, 0x30, 0x40, 0x3C],  # w
    120: [0x44, 0x28, 0x10, 0x28, 0x44],  # x
    121: [0x0C, 0x50, 0x50, 0x50, 0x3C],  # y
    122: [0x44, 0x64, 0x54, 0x4C, 0x44],  # z
    123: [0x00, 0x08, 0x36, 0x41, 0x00],  # {
    124: [0x00, 0x00, 0x7F, 0x00, 0x00],  # |
    125: [0x00, 0x41, 0x36, 0x08, 0x00],  # }
    126: [0x08, 0x08, 0x2A, 0x1C, 0x08],  # ~
}


class G13LCD:
    """
    LCD display controller for G13 (160x43 monochrome).

    The G13 LCD uses ROW-BLOCK byte packing:
    - 160 columns, 48 rows (only 43 visible)
    - Pixels grouped in 8-row vertical blocks
    - Each block spans all 160 columns

    Memory layout (960 bytes):
    - bytes 0-159:   rows 0-7,   all 160 columns
    - bytes 160-319: rows 8-15,  all 160 columns
    - bytes 320-479: rows 16-23, all 160 columns
    - bytes 480-639: rows 24-31, all 160 columns
    - bytes 640-799: rows 32-39, all 160 columns
    - bytes 800-959: rows 40-47, all 160 columns

    Formula: byte_idx = x + (y // 8) * 160
    """

    WIDTH = 160
    HEIGHT = 43
    BUFFER_ROWS = 48  # Buffer has 48 rows (6 bytes × 8 bits)
    BYTES_PER_COLUMN = 6  # 48 bits / 8 = 6 bytes per column
    FRAMEBUFFER_SIZE = 960  # 160 × 6 = 960
    HEADER_SIZE = 32
    COMMAND_BYTE = 0x03
    LCD_ENDPOINT = 2  # USB endpoint for LCD data

    def __init__(self, device_handle=None):
        """
        Initialize LCD controller.

        Args:
            device_handle: Device instance (HidrawDevice or LibUSBDevice)
        """
        self.device = device_handle
        self._framebuffer = bytearray(self.FRAMEBUFFER_SIZE)

    def clear(self):
        """Clear LCD display (all pixels off)."""
        self._framebuffer = bytearray(self.FRAMEBUFFER_SIZE)
        self._send_framebuffer()

    def fill(self):
        """Fill LCD display (all pixels on)."""
        self._framebuffer = bytearray([0xFF] * self.FRAMEBUFFER_SIZE)
        self._send_framebuffer()

    def write_text(self, text: str, x: int = 0, y: int = 0, send: bool = True):
        """
        Write text to LCD using 5x7 font.

        Args:
            text: Text to display
            x: X position (0-159)
            y: Y position (0-42)
            send: If True, send framebuffer to device after rendering
        """
        cursor_x = x
        char_width = 6  # 5 pixels + 1 pixel spacing

        for char in text:
            code = ord(char)
            if code not in FONT_5X7:
                code = 63  # '?' for unknown characters

            glyph = FONT_5X7[code]

            # Render each column of the character
            for col_idx, col_data in enumerate(glyph):
                px = cursor_x + col_idx
                if px >= self.WIDTH:
                    break

                # Render 7 rows of this column
                for row in range(7):
                    py = y + row
                    if py >= self.HEIGHT:
                        continue

                    # Bit 0 is top row, bit 6 is bottom
                    if col_data & (1 << row):
                        self.set_pixel(px, py, True)

            cursor_x += char_width
            if cursor_x >= self.WIDTH:
                break

        if send:
            self._send_framebuffer()

    def write_text_centered(self, text: str, y: int = 18, send: bool = True):
        """
        Write text centered horizontally on the LCD.

        Args:
            text: Text to display
            y: Y position (0-42), defaults to vertical center
            send: If True, send framebuffer to device after rendering
        """
        char_width = 6
        text_width = len(text) * char_width
        x = max(0, (self.WIDTH - text_width) // 2)
        self.write_text(text, x, y, send)

    def write_bitmap(self, bitmap: bytes):
        """
        Write raw bitmap to LCD.

        Args:
            bitmap: Raw bitmap data (960 bytes for full frame)
        """
        if len(bitmap) > self.FRAMEBUFFER_SIZE:
            raise ValueError(f"Bitmap too large: max {self.FRAMEBUFFER_SIZE} bytes")

        # Copy bitmap to framebuffer
        self._framebuffer[: len(bitmap)] = bitmap
        self._send_framebuffer()

    def set_pixel(self, x: int, y: int, on: bool = True):
        """
        Set a single pixel using G13 LCD byte packing.

        The G13 LCD framebuffer uses ROW-BLOCK layout:
        - 160 columns × 48 rows (only 43 visible)
        - Pixels are grouped in 8-row vertical blocks
        - Each block spans all 160 columns

        Layout in memory (960 bytes):
        - bytes 0-159:   row-block 0 (rows 0-7, all columns)
        - bytes 160-319: row-block 1 (rows 8-15, all columns)
        - bytes 320-479: row-block 2 (rows 16-23, all columns)
        - bytes 480-639: row-block 3 (rows 24-31, all columns)
        - bytes 640-799: row-block 4 (rows 32-39, all columns)
        - bytes 800-959: row-block 5 (rows 40-47, all columns)

        Formula: byte_idx = x + (y // 8) * 160
        Bit: y % 8

        Args:
            x: X coordinate (0-159, left to right)
            y: Y coordinate (0-42, top to bottom)
            on: True for pixel on, False for off
        """
        if not (0 <= x < self.WIDTH and 0 <= y < self.HEIGHT):
            return

        # Row-block layout: byte_idx = x + (y // 8) * WIDTH
        byte_idx = x + (y // 8) * self.WIDTH
        bit_in_byte = y % 8

        if on:
            self._framebuffer[byte_idx] |= 1 << bit_in_byte
        else:
            self._framebuffer[byte_idx] &= ~(1 << bit_in_byte)

    def _init_lcd(self):
        """
        Initialize LCD endpoint before writing.

        Sends SET_CONFIGURATION control transfer (required before each write).
        """
        if hasattr(self.device, "_dev") and self.device._dev:
            try:
                # Control transfer: SET_CONFIGURATION
                # bmRequestType=0, bRequest=9, wValue=1, wIndex=0
                self.device._dev.ctrl_transfer(0, 9, 1, 0, None, 1000)
            except Exception as e:
                print(f"[LCD] init_lcd failed: {e}")

    def _send_framebuffer(self):
        """
        Send the framebuffer to the device.

        Protocol: 32-byte header (0x03 + zeros) + 960-byte framebuffer
        Total: 992 bytes sent via interrupt transfer to endpoint 2.
        """
        if not self.device:
            print("[LCD] No device connected")
            return

        try:
            # Initialize LCD endpoint (required before each write)
            self._init_lcd()

            # Build packet: 32-byte header + 960-byte framebuffer
            # First byte of header is command 0x03
            header = bytearray(self.HEADER_SIZE)
            header[0] = self.COMMAND_BYTE

            # Full packet is 992 bytes
            packet = bytes(header) + bytes(self._framebuffer)

            # Send to device - LibUSBDevice.write() sends to OUT endpoint
            bytes_written = self.device.write(packet)
            if bytes_written != len(packet):
                print(f"[LCD] Partial write: {bytes_written}/{len(packet)} bytes")
        except Exception as e:
            print(f"[LCD] Failed to send framebuffer: {e}")

    def set_brightness(self, level: int):
        """
        Set LCD brightness.

        Args:
            level: Brightness level (0-100)

        Note: LCD brightness may not be separately controllable on G13.
        """
        if not 0 <= level <= 100:
            raise ValueError("Brightness must be 0-100")

        print("[LCD] Brightness control not supported on G13 LCD")
