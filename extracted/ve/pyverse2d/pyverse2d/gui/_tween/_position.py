# ======================================== IMPORTS ========================================
from __future__ import annotations

from ...abc import Tween
from ...math import Point
from ...math.easing import EasingFunc, linear

from numbers import Real

# ======================================== TWEEN ========================================
class PositionTween(Tween):
    """Interpolation positionnelle"""
    __slots__ = ()

    def __init__(self, target_value: Point, duration: Real = 0.0, easing: EasingFunc = linear):
        target_value = Point(target_value)
        
        super().__init__("position", target_value, duration, easing)

    def interpolate(self, base: Point, target: Point, p: float):
        return (base.x + (target.x - base.x) * p, base.y + (target.y - base.y) * p)