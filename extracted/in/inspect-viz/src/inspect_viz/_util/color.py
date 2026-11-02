import colorsys
from typing import cast


def lighten_color_blend(hex_color: str, factor: float = 0.5) -> str:
    rgb = hex_to_rgb(hex_color)

    # blend with white (255, 255, 255)
    lightened = tuple(int(rgb[i] + (255 - rgb[i]) * factor) for i in range(3))

    return rgb_to_hex(lightened)


def lighten_color_hsl(hex_color: str, factor: float = 0.5) -> str:
    rgb = hex_to_rgb(hex_color)

    # Convert to HSL (normalized 0-1)
    r, g, b = [x / 255.0 for x in rgb]
    h, l, s = colorsys.rgb_to_hls(r, g, b)  # noqa: E741

    # Increase lightness
    l = min(1.0, l + (1.0 - l) * factor)  # noqa: E741

    # Convert back to RGB
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    rgb_new = tuple(int(x * 255) for x in (r, g, b))

    return rgb_to_hex(rgb_new)


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Convert hex color to RGB tuple (0-255 range)."""
    hex_color = hex_color.lstrip("#")
    return cast(
        tuple[int, int, int], tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    )


def rgb_to_hex(rgb: tuple[int, ...]) -> str:
    """Convert RGB tuple to hex color."""
    return "#{:02x}{:02x}{:02x}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
