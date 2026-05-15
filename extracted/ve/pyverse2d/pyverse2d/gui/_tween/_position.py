# ======================================== IMPORTS ========================================
from __future__ import annotations

from ...abc import Tween
from ...math import Point
from ...math.easing import linear
from ...typing import EasingFunc

from numbers import Real

# ======================================== TWEEN ========================================
class PositionTween(Tween):
    """Interpolation positionnelle

    Args:
        target_value: position cible
        duration: durée de transition
        easing: fonction d'atténuation
    """
    __slots__ = ()

    def __init__(self, target_value: Point, duration: Real = 0.0, easing: EasingFunc = linear):
        # Transtypage
        target_value = Point(target_value)
        
        # Initialisation de l'interpolation
        super().__init__("position", target_value, duration, easing)

    def interpolate(self, base: Point, target: Point, p: float):
        return (base.x + (target.x - base.x) * p, base.y + (target.y - base.y) * p)
    
# ======================================== EXPORTS ========================================
__all__ = [
    "PositionTween",
]