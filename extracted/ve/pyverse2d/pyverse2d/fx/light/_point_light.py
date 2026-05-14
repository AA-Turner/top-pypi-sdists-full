# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import different_from
from ...abc import LightSource
from ...math import Point
from ...math.easing import EasingFunc
from ...asset import Color

from numbers import Real

# ======================================== IMPORTS ========================================
class PointLight(LightSource):
    """Source de lumière: Point
    
    Args:
        position: position du point
        radius: rayon lumineux autour du point
        color: couleur de la lumière émise
        intensity: intensité lumineuse
        falloff: fonction d'atténuation
        enable: activation initiale de la lumière
    """
    __slots__ = ("_radius")

    def __init__(
            self,
            position: Point = (0.0, 0.0),
            radius: Real = 1.0,
            color: Color = (255, 255, 255),
            intensity: Real = 1.0,
            falloff: EasingFunc = None,
            enabled: bool = True,
        ):
        # Initialisation de la source de lumière
        super().__init__(position, color, intensity, falloff, enabled)

        # Transtypage et vérifications
        radius = abs(float(radius))

        if __debug__:
            different_from(radius, 0)

        # Paramètres publiques
        self._radius: float = radius

    # ======================================== PROPERTIES ========================================
    @property
    def radius(self) -> float:
        """Rayon lumineux autour du point

        Le rayon doit être un ``Réel`` non nul.
        """
        return self._radius
    
    @radius.setter
    def radius(self, value: Real) -> None:
        value = float(value)
        if __debug__:
            different_from(value, 0)
        self._radius = value