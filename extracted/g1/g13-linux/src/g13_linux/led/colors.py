"""
RGB Color Utilities

Provides RGB dataclass and color manipulation functions.
"""

from dataclasses import dataclass


@dataclass
class RGB:
    """RGB color with 0-255 components."""

    r: int
    g: int
    b: int

    def __post_init__(self):
        """Clamp values to valid range."""
        self.r = max(0, min(255, self.r))
        self.g = max(0, min(255, self.g))
        self.b = max(0, min(255, self.b))

    @classmethod
    def from_hex(cls, hex_string: str) -> "RGB":
        """
        Create RGB from hex string.

        Args:
            hex_string: Color in #RRGGBB or RRGGBB format

        Returns:
            RGB instance
        """
        hex_string = hex_string.lstrip("#")
        if len(hex_string) != 6:
            raise ValueError("Hex color must be 6 characters")

        try:
            r = int(hex_string[0:2], 16)
            g = int(hex_string[2:4], 16)
            b = int(hex_string[4:6], 16)
            return cls(r, g, b)
        except ValueError:
            raise ValueError(f"Invalid hex color: {hex_string}")

    @classmethod
    def from_name(cls, name: str) -> "RGB":
        """
        Create RGB from named color.

        Args:
            name: Color name (case-insensitive)

        Returns:
            RGB instance
        """
        name_lower = name.lower()
        if name_lower not in NAMED_COLORS:
            available = ", ".join(sorted(NAMED_COLORS.keys()))
            raise ValueError(f"Unknown color '{name}'. Available: {available}")
        return NAMED_COLORS[name_lower]

    def to_hex(self) -> str:
        """Convert to hex string with # prefix."""
        return f"#{self.r:02X}{self.g:02X}{self.b:02X}"

    def to_tuple(self) -> tuple[int, int, int]:
        """Convert to (r, g, b) tuple."""
        return (self.r, self.g, self.b)

    def __iter__(self):
        """Allow unpacking: r, g, b = color"""
        return iter((self.r, self.g, self.b))


# Named colors dictionary
NAMED_COLORS: dict[str, RGB] = {
    "red": RGB(255, 0, 0),
    "green": RGB(0, 255, 0),
    "blue": RGB(0, 0, 255),
    "yellow": RGB(255, 255, 0),
    "cyan": RGB(0, 255, 255),
    "magenta": RGB(255, 0, 255),
    "white": RGB(255, 255, 255),
    "black": RGB(0, 0, 0),
    "orange": RGB(255, 128, 0),
    "purple": RGB(128, 0, 255),
    "pink": RGB(255, 105, 180),
    "lime": RGB(0, 255, 128),
    "teal": RGB(0, 128, 128),
    "coral": RGB(255, 127, 80),
    "gold": RGB(255, 215, 0),
    "crimson": RGB(220, 20, 60),
    "indigo": RGB(75, 0, 130),
    "violet": RGB(238, 130, 238),
    "turquoise": RGB(64, 224, 208),
    "salmon": RGB(250, 128, 114),
}


def blend(color1: RGB, color2: RGB, factor: float) -> RGB:
    """
    Blend two colors.

    Args:
        color1: First color
        color2: Second color
        factor: Blend factor (0.0 = color1, 1.0 = color2)

    Returns:
        Blended RGB color
    """
    factor = max(0.0, min(1.0, factor))
    inv = 1.0 - factor
    return RGB(
        int(color1.r * inv + color2.r * factor),
        int(color1.g * inv + color2.g * factor),
        int(color1.b * inv + color2.b * factor),
    )


def brighten(color: RGB, factor: float) -> RGB:
    """
    Brighten a color (blend toward white).

    Args:
        color: Input color
        factor: Brightening factor (0.0 = no change, 1.0 = white)

    Returns:
        Brightened RGB color
    """
    return blend(color, RGB(255, 255, 255), factor)


def dim(color: RGB, factor: float) -> RGB:
    """
    Dim a color (blend toward black).

    Args:
        color: Input color
        factor: Dimming factor (0.0 = no change, 1.0 = black)

    Returns:
        Dimmed RGB color
    """
    return blend(color, RGB(0, 0, 0), factor)


def hsv_to_rgb(h: float, s: float, v: float) -> RGB:
    """
    Convert HSV to RGB.

    Args:
        h: Hue (0.0-1.0)
        s: Saturation (0.0-1.0)
        v: Value/brightness (0.0-1.0)

    Returns:
        RGB color
    """
    if s == 0.0:
        val = int(v * 255)
        return RGB(val, val, val)

    h = h % 1.0
    i = int(h * 6.0)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))

    i = i % 6
    if i == 0:
        r, g, b = v, t, p
    elif i == 1:
        r, g, b = q, v, p
    elif i == 2:
        r, g, b = p, v, t
    elif i == 3:
        r, g, b = p, q, v
    elif i == 4:
        r, g, b = t, p, v
    else:
        r, g, b = v, p, q

    return RGB(int(r * 255), int(g * 255), int(b * 255))
