# ======================================== IMPORTS ========================================
from __future__ import annotations

from ...abc import Tween
from ...math.easing import EasingFunc, linear

from numbers import Real

# ======================================== TWEEN ========================================
class RotationTween(Tween):
    """Interpolation rotationnelle"""
    __slots__ = ()

    def __init__(self, target_value: Real, duration: Real = 0.0, easing: EasingFunc = linear):
        target_value = float(target_value)
        
        super().__init__("rotation", target_value, duration, easing)