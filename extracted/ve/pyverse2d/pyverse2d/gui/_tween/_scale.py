# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import different_from
from ...abc import Tween
from ...math.easing import linear
from ...typing import EasingFunc

from numbers import Real

# ======================================== TWEEN ========================================
class ScaleTween(Tween):
    """Interpolation de la taille

    Args:
        target_value: facteur de redimensionnement cible
        duration: durée de transition
        easing: fonction d'atténuation
    """
    __slots__ = ()

    def __init__(self, target_value: Real, duration: Real = 0.0, easing: EasingFunc = linear):
        # Transtypage et vérifications
        target_value = float(target_value)

        if __debug__:
            different_from(target_value, 0.0)

        # Initialisation de l'interpolation
        super().__init__("scale", target_value, duration, easing)

# ======================================== EXPORTS ========================================
__all__ = [
    "ScaleTween",
]