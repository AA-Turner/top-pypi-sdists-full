# ======================================== IMPORTS ========================================
from __future__ import annotations

from ...abc import Tween
from ...asset import Color
from ...math.easing import EasingFunc, linear

from numbers import Real

# ======================================== TWEEN ========================================
class ColorTween(Tween):
    """Interpolation des couleurs"""
    __slots__ = ()

    def __init__(self, target_value: Color, duration: Real = 0.0, easing: EasingFunc = linear):
        target_value = Color(target_value)
        super().__init__("color", target_value, duration, easing)

    def interpolate(self, base: Color, target: Color, p: float):
        p = max(0.0, min(p, 1.0))
        r = base.r + (target.r - base.r) * p
        g = base.g + (target.g - base.g) * p
        b = base.b + (target.b - base.g) * p
        a = base.a + (target.a - base.a) * p
        return (r, g, b, a)