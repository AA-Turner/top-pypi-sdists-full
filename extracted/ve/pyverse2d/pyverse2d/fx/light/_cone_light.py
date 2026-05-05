# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import not_null, clamped
from ...abc import LightSource
from ...math import Point, Vector
from ...math.easing import EasingFunc
from ...asset import Color

from numbers import Real
import math

# ======================================== IMPORTS ========================================
class ConeLight(LightSource):
    """Source de lumière: Point
    
    Args:
        position: position du point
        direction: vecteur directionnel
        radius: rayon du cone
        angle: demi angle du cone
        softness: douceur du bord
        color: couleur de la lumière émise
        intensity: intensité lumineuse
        falloff: fonction d'atténuation
        enable: activation initiale de la lumière
    """
    __slots__ = ("_direction", "_radius", "_angle", "_softness")

    def __init__(
            self,
            position: Point = (0.0, 0.0),
            direction: Vector = (1.0, 0.0),
            radius: Real = 0.0,
            angle: Real = 30.0,
            softness: Real = 0.0,
            color: Color = (255, 255, 255),
            intensity: Real = 1.0,
            falloff: EasingFunc = None,
            enabled: bool = True,
        ):
        # Initialisation de la source de lumière
        super().__init__(position, color, intensity, falloff, enabled)

        # Paramètres publiques
        self._direction: Vector = Vector(direction).normalized
        self._radius: float = abs(float(radius))
        self._angle: float = abs(float(angle))
        self._softness: float = float(softness)

        if __debug__:
            if self._direction.is_null(): raise ValueError(f"direction cannot be null vector")
            not_null(self._angle)
            clamped(self._softness)

    # ======================================== PROPERTIES ========================================
    @property
    def direction(self) -> Vector:
        """Vecteur directionnel du cone

        La direction peut être un object ``Vector`` ou n'importe quel tuple ``(dx, dy)``.
        La norme du vecteur n'est pas prise en considération.
        La direction ne peut pas être le vecteur nul.
        """
        return self._direction
    
    @direction.setter
    def direction(self, value: Vector) -> None:
        value = Vector(value)
        assert not value.is_null(), f"direction cannot be null vector"
        self._direction = value.normalized

    @property
    def radius(self) -> float:
        """Rayon du cone

        Le rayon doit être un ``Réel``.
        Mettre cette propriété à 0.0 pour un cone infini.
        """
        return  self._radius
    
    @radius.setter
    def radius(self, value: Real) -> None:
        value = abs(float(value))
        self._radius = value

    @property
    def angle(self) -> float:
        """Demi angle du cone

        L'angle doit être un ``Réel`` non nul.
        L'angle est *en degrés*.
        """
        return self._angle
    
    @angle.setter
    def angle(self, value: Real) -> None:
        value = abs(float(value))
        assert  value != 0.0, f"angle ({value}) cannot be null"
        self._angle = value
    
    @property
    def softness(self) -> float:
        """Douceur du bord du cone

        La douceur doit être un ``Réel`` compris dans l'intervalle *[0, 1]*.
        Mettre cette propriété à 0.0 pour un cone nette, et 1.0 pour un fondu total.
        """
        return self._softness
    
    @softness.setter
    def softness(self, value: Real) -> None:
        value = float(value)
        assert 0.0 <= value <= 1.0, f"softness ({value}) must be within 0.0 and 1.0"
        self._softness = value

    # ======================================== GETTERS ========================================
    def get_inner_angle(self) -> float:
        """Renvoie l'angle intérieur du bord"""
        return self._angle * (1.0 - self._softness)
    
    def get_outer_angle(self) -> float:
        """Renvoie l'angle extérieur du bord"""
        return self._angle
    
    # ======================================== INTERFACE ========================================
    def rotate(self, angle: Real) -> None:
        """Applique une rotation dans le sens trigonométrique *(CCW)*

        Args:
            angle: angle de rotation *en degrés*
        """
        theta = math.radians(angle)
        x, y = self._direction
        self._direction.x = x * math.cos(theta) - y * math.sin(theta)
        self._direction.y = x * math.sin(theta) + y * math.cos(theta)