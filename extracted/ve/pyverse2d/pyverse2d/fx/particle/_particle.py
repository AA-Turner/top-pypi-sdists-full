# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import positive, under, expect_callable
from ...asset import Color
from ...math.easing import linear, EasingFunc

from dataclasses import dataclass
from typing import Tuple
from numbers import Real

# ======================================== PARTICLE ========================================
@dataclass(slots=True, frozen=True)
class Particle:
    """Pattern de configuration d'une particule

    Args:
        lifetime: durée de vie (min, max) en secondes
        speed: vitesse (min, max) en unités monde
        size: taille initiale (min, max) en unités monde
        size_end: taille finale en unités monde
        angular_velocity: vitesse angulaire (min, max) en degrés/s
        color_start: couleur initiale
        color_end: couleur finale
        easing: fonction d'atténuation temporelle
    """
    lifetime: Tuple[Real, Real] = (1.0, 2.0)
    speed: Tuple[Real, Real] = (50.0, 150.0)
    size: Tuple[Real, Real] = (5.0, 10.0)
    size_end: Real = 0.0
    angular_velocity: Tuple[Real, Real] = (-180.0, 180.0)
    color_start: Color = None
    color_end: Color = None
    easing: EasingFunc = linear

    def __post_init__(self) -> None:
        object.__setattr__(self, 'lifetime', (float(self.lifetime[0]), float(self.lifetime[1])))
        object.__setattr__(self, 'speed', (float(self.speed[0]), float(self.speed[1])))
        object.__setattr__(self, 'size', (float(self.size[0]), float(self.size[1])))
        object.__setattr__(self, 'size_end', float(self.size_end))
        object.__setattr__(self, 'angular_velocity', (float(self.angular_velocity[0]), float(self.angular_velocity[1])))
        object.__setattr__(self, 'color_start', Color(self.color_start) if self.color_start is not None else Color(255, 255, 255, 255))
        object.__setattr__(self, 'color_end', Color(self.color_end) if self.color_end is not None else Color(255, 255, 255, 0))

        if __debug__:
            positive(self.lifetime[0])
            positive(self.lifetime[1])
            under(self.lifetime[0], self.lifetime[1], include=True)
            positive(self.speed[0])
            positive(self.speed[1])
            under(self.speed[0], self.speed[1], include=True)
            positive(self.size[0])
            positive(self.size[1])
            under(self.size[0], self.size[1])
            positive(self.size_end)
            expect_callable(self.easing)