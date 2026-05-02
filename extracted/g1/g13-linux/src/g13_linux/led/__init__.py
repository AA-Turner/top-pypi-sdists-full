"""
G13 LED Control Module

Provides RGB color management, effects engine, and LED controller.
"""

from .colors import NAMED_COLORS, RGB, blend, brighten, dim
from .controller import LEDController
from .effects import EffectType, alert, fade, pulse, rainbow, solid

__all__ = [
    "RGB",
    "NAMED_COLORS",
    "blend",
    "brighten",
    "dim",
    "EffectType",
    "solid",
    "pulse",
    "rainbow",
    "fade",
    "alert",
    "LEDController",
]
