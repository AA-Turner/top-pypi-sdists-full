from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from .paint_source import PaintSource
import skia

class NamedColor(str, Enum):
    """Named color constants from CSS specification.

    Obtained from: https://developer.mozilla.org/en-US/docs/Web/CSS/named-color
    """
    TRANSPARENT = '#00000000'
    ALICEBLUE = '#f0f8ff'
    ANTIQUEWHITE = '#faebd7'
    AQUA = '#00ffff'
    AQUAMARINE = '#7fffd4'
    AZURE = '#f0ffff'
    BEIGE = '#f5f5dc'
    BISQUE = '#ffe4c4'
    BLACK = '#000000'
    BLANCHEDALMOND = '#ffebcd'
    BLUE = '#0000ff'
    BLUEVIOLET = '#8a2be2'
    BROWN = '#a52a2a'
    BURLYWOOD = '#deb887'
    CADETBLUE = '#5f9ea0'
    CHARTREUSE = '#7fff00'
    CHOCOLATE = '#d2691e'
    CORAL = '#ff7f50'
    CORNFLOWERBLUE = '#6495ed'
    CORNSILK = '#fff8dc'
    CRIMSON = '#dc143c'
    CYAN = '#00ffff'  # synonym of aqua
    DARKBLUE = '#00008b'
    DARKCYAN = '#008b8b'
    DARKGOLDENROD = '#b8860b'
    DARKGRAY = '#a9a9a9'
    DARKGREEN = '#006400'
    DARKGREY = '#a9a9a9'  # synonym of darkgray
    DARKKHAKI = '#bdb76b'
    DARKMAGENTA = '#8b008b'
    DARKOLIVEGREEN = '#556b2f'
    DARKORANGE = '#ff8c00'
    DARKORCHID = '#9932cc'
    DARKRED = '#8b0000'
    DARKSALMON = '#e9967a'
    DARKSEAGREEN = '#8fbc8f'
    DARKSLATEBLUE = '#483d8b'
    DARKSLATEGRAY = '#2f4f4f'
    DARKSLATEGREY = '#2f4f4f'  # synonym
    DARKTURQUOISE = '#00ced1'
    DARKVIOLET = '#9400d3'
    DEEPPINK = '#ff1493'
    DEEPSKYBLUE = '#00bfff'
    DIMGRAY = '#696969'
    DIMGREY = '#696969'  # synonym
    DODGERBLUE = '#1e90ff'
    FIREBRICK = '#b22222'
    FLORALWHITE = '#fffaf0'
    FORESTGREEN = '#228b22'
    FUCHSIA = '#ff00ff'
    GAINSBORO = '#dcdcdc'
    GHOSTWHITE = '#f8f8ff'
    GOLD = '#ffd700'
    GOLDENROD = '#daa520'
    GRAY = '#808080'
    GREEN = '#008000'
    GREENYELLOW = '#adff2f'
    GREY = '#808080'  # synonym of gray
    HONEYDEW = '#f0fff0'
    HOTPINK = '#ff69b4'
    INDIANRED = '#cd5c5c'
    INDIGO = '#4b0082'
    IVORY = '#fffff0'
    KHAKI = '#f0e68c'
    LAVENDER = '#e6e6fa'
    LAVENDERBLUSH = '#fff0f5'
    LAWNGREEN = '#7cfc00'
    LEMONCHIFFON = '#fffacd'
    LIGHTBLUE = '#add8e6'
    LIGHTCORAL = '#f08080'
    LIGHTCYAN = '#e0ffff'
    LIGHTGOLDENRODYELLOW = '#fafad2'
    LIGHTGRAY = '#d3d3d3'
    LIGHTGREEN = '#90ee90'
    LIGHTGREY = '#d3d3d3'  # synonym
    LIGHTPINK = '#ffb6c1'
    LIGHTSALMON = '#ffa07a'
    LIGHTSEAGREEN = '#20b2aa'
    LIGHTSKYBLUE = '#87cefa'
    LIGHTSLATEGRAY = '#778899'
    LIGHTSLATEGREY = '#778899'  # synonym
    LIGHTSTEELBLUE = '#b0c4de'
    LIGHTYELLOW = '#ffffe0'
    LIME = '#00ff00'
    LIMEGREEN = '#32cd32'
    LINEN = '#faf0e6'
    MAGENTA = '#ff00ff'  # synonym of fuchsia
    MAROON = '#800000'
    MEDIUMAQUAMARINE = '#66cdaa'
    MEDIUMBLUE = '#0000cd'
    MEDIUMORCHID = '#ba55d3'
    MEDIUMPURPLE = '#9370db'
    MEDIUMSEAGREEN = '#3cb371'
    MEDIUMSLATEBLUE = '#7b68ee'
    MEDIUMSPRINGGREEN = '#00fa9a'
    MEDIUMTURQUOISE = '#48d1cc'
    MEDIUMVIOLETRED = '#c71585'
    MIDNIGHTBLUE = '#191970'
    MINTCREAM = '#f5fffa'
    MISTYROSE = '#ffe4e1'
    MOCCASIN = '#ffe4b5'
    NAVAJOWHITE = '#ffdead'
    NAVY = '#000080'
    OLDLACE = '#fdf5e6'
    OLIVE = '#808000'
    OLIVEDRAB = '#6b8e23'
    ORANGE = '#ffa500'
    ORANGERED = '#ff4500'
    ORCHID = '#da70d6'
    PALEGOLDENROD = '#eee8aa'
    PALEGREEN = '#98fb98'
    PALETURQUOISE = '#afeeee'
    PALEVIOLETRED = '#db7093'
    PAPAYAWHIP = '#ffefd5'
    PEACHPUFF = '#ffdab9'
    PERU = '#cd853f'
    PINK = '#ffc0cb'
    PLUM = '#dda0dd'
    POWDERBLUE = '#b0e0e6'
    PURPLE = '#800080'
    REBECCAPURPLE = '#663399'
    RED = '#ff0000'
    ROSYBROWN = '#bc8f8f'
    ROYALBLUE = '#4169e1'
    SADDLEBROWN = '#8b4513'
    SALMON = '#fa8072'
    SANDYBROWN = '#f4a460'
    SEAGREEN = '#2e8b57'
    SEASHELL = '#fff5ee'
    SIENNA = '#a0522d'
    SILVER = '#c0c0c0'
    SKYBLUE = '#87ceeb'
    SLATEBLUE = '#6a5acd'
    SLATEGRAY = '#708090'
    SLATEGREY = '#708090'  # synonym
    SNOW = '#fffafa'
    SPRINGGREEN = '#00ff7f'
    STEELBLUE = '#4682b4'
    TAN = '#d2b48c'
    TEAL = '#008080'
    THISTLE = '#d8bfd8'
    TOMATO = '#ff6347'
    TURQUOISE = '#40e0d0'
    VIOLET = '#ee82ee'
    WHEAT = '#f5deb3'
    WHITE = '#ffffff'
    WHITESMOKE = '#f5f5f5'
    YELLOW = '#ffff00'
    YELLOWGREEN = '#9acd32'

    _ignore_ = []


@dataclass(frozen=True)
class SolidColor(PaintSource):
    """Represents a solid color with RGBA components.

    This class provides a structured way to handle solid colors, with methods
    for creating instances from various string formats like hex codes or
    standard color names.

    Attributes:
        r (int): The red component of the color (0-255).
        g (int): The green component of the color (0-255).
        b (int): The blue component of the color (0-255).
        a (int): The alpha (opacity) component of the color (0-255), where
            255 is fully opaque. Defaults to 255.
    """
    r: int
    g: int
    b: int
    a: int = 255

    @classmethod
    def _from_hex(cls, hex_str: str) -> SolidColor:
        """Creates a SolidColor object from a hexadecimal string.

        Supports various hex formats: '#RGB', '#RRGGBB', and '#RRGGBBAA'.

        Args:
            hex_str: The hexadecimal color string.

        Returns:
            A new `SolidColor` instance.

        Raises:
            ValueError: If the hex string format is invalid.
        """
        hex_str = hex_str.lstrip('#')

        if len(hex_str) == 3:  # Expand short form like #F0C to #FF00CC
            hex_str = "".join(c * 2 for c in hex_str)

        if len(hex_str) == 8:  # RRGGBBAA
            r, g, b, a = (int(hex_str[i:i + 2], 16) for i in (0, 2, 4, 6))
            return cls(r, g, b, a)
        elif len(hex_str) == 6:  # RRGGBB
            r, g, b = (int(hex_str[i:i + 2], 16) for i in (0, 2, 4))
            return cls(r, g, b)
        else:
            raise ValueError(f"Invalid hex color format: '{hex_str}'")

    @classmethod
    def from_str(cls, value: str) -> SolidColor:
        """Creates a SolidColor object from a general color string.

        This method acts as a factory, supporting standard color names
        (e.g., 'red', 'blue') and hexadecimal codes.

        Args:
            value: The color string to parse.

        Returns:
            A new `SolidColor` instance.

        Raises:
            ValueError: If the color name is unknown or the format is invalid.
        """
        clean_value = value.strip().lower()
        if clean_value.startswith('#'):
            return cls._from_hex(clean_value)
        
        upper_clean_value = clean_value.upper()
        if upper_clean_value in NamedColor.__members__:
            return cls._from_hex(NamedColor.__members__[upper_clean_value].value)

        raise ValueError(f"Unknown color name or format: '{value}'")

    def apply_to_paint(self, paint: skia.Paint, bounds: skia.Rect) -> None:
        """Applies this solid color to a Skia Paint object.

        This method is part of the `PaintSource` interface and is used by the
        rendering engine.

        Args:
            paint: The `skia.Paint` object to modify.
            bounds: The bounding box of the area to be painted. This is not
                used for solid colors but is part of the interface for
                compatibility with gradients.
        """
        paint.setColor(skia.Color(self.r, self.g, self.b, self.a))