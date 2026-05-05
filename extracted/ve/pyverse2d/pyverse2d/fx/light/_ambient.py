# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import clamped
from ...abc import LightEffect
from ...asset import Color

from dataclasses import dataclass
from numbers import Real
from typing import ClassVar

# ======================================== EFFECT ========================================
@dataclass(slots=True, frozen=True)
class Ambient(LightEffect):
    """Effect lumineux: Ambiance
    
    Args:
        level: niveau de luminosité *[0, 1]*
        shade: couleur d'assombrissement *(RGB)*
    """
    level: Real = 1.0
    shade: Color = (0, 0, 0)

    _ID: ClassVar[str] = "ambient"

    def __post_init__(self) -> None:
        """Transtypage et vérifications"""
        object.__setattr__(self, "level", float(self.level))
        object.__setattr__(self, "shade", Color(self.shade))

        if __debug__:
            clamped(self.level)