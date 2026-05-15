# ======================================== IMPORTS ========================================
from __future__ import annotations

from ...abc import Tween
from ...math.easing import linear
from ...typing import EasingFunc

from numbers import Real

# ======================================== TWEEN ========================================
class RotationTween(Tween):
    """Interpolation rotationnelle

    Args:
        target_value: rotation cible
        duration: durée de transition
        easing: fonction d'atténuation
    """
    __slots__ = ()

    def __init__(self, target_value: Real, duration: Real = 0.0, easing: EasingFunc = linear):
        # Transtypage
        target_value = float(target_value)
        
        # Initialisation de l'interpolation
        super().__init__("rotation", target_value, duration, easing)

# ======================================== EXPORTS ========================================
__all__ = [
    "RotationTween",
]