# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import not_null, clamped, positive
from ...abc import LightEffect

from dataclasses import dataclass
from numbers import Real
from typing  import ClassVar

# ======================================== EFFECT ========================================
@dataclass(slots=True, frozen=True)
class Bloom(LightEffect):
    """Effect lumineux: Saignement
    
    Args:   
        radius: rayon du saignement
        threshold: seuil minimum d'intesité lumineuse pour saignement
        intensity: intensité du saignement
    """
    radius: Real = 0.0
    threshold: Real = 0.7
    intensity: Real = 1.0

    _ID: ClassVar[str] = "bloom"

    def __post_init__(self) -> None:
        """Transtypage et vérifications"""
        object.__setattr__(self, "radius", abs(float(self.radius)))
        object.__setattr__(self, "threshold", float(self.threshold))
        object.__setattr__(self, "intensity", float(self.intensity))

        if __debug__:
            not_null(self.radius)
            clamped(self.threshold)
            positive(self.intensity)