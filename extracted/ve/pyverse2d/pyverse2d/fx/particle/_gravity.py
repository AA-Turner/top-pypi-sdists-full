# ======================================== IMPORTS ========================================
from __future__ import annotations

from ...abc import ParticleModifier

import numpy as np
from numbers import Real
import math

# ======================================== MODIFIER ========================================
class Gravity(ParticleModifier):
    """Modificateur de gravité

    Args:
        strength: intensité de l'accélération en unités monde/s²
        direction: direction en degrés (0 = droite, 90 = haut, 270 = bas)
    """
    __slots__ = ("_strength", "_direction", "_ax", "_ay")

    def __init__(self, strength: Real = 9.8, direction: Real = 270.0):
        self._strength  = float(strength)
        self._direction = float(direction)
        self._update_components()

    # ======================================== PROPERTIES ========================================
    @property
    def strength(self) -> float:
        return self._strength

    @strength.setter
    def strength(self, value: Real) -> None:
        self._strength = float(value)
        self._update_components()

    @property
    def direction(self) -> float:
        return self._direction

    @direction.setter
    def direction(self, value: Real) -> None:
        self._direction = float(value)
        self._update_components()

    # ======================================== INTERFACE ========================================
    def apply(self, dt: float, alive: np.ndarray, positions: np.ndarray, velocities: np.ndarray) -> None:
        velocities[alive, 0] += self._ax * dt
        velocities[alive, 1] += self._ay * dt

    # ======================================== INTERNALS ========================================
    def _update_components(self) -> None:
        """Calcul du vecteur directionnel"""
        rad = math.radians(self._direction)
        self._ax = self._strength * math.cos(rad)
        self._ay = self._strength * math.sin(rad)