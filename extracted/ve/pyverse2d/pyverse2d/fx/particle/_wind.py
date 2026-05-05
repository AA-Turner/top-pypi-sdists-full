# ======================================== IMPORTS ========================================
from __future__ import annotations

from ...abc import ParticleModifier

import numpy as np
from numbers import Real

# ======================================== MODIFIER ========================================
class Wind(ParticleModifier):
    """Modificateur de vent — force constante directionnelle

    Args:
        x: force horizontale en unités monde/s²
        y: force verticale en unités monde/s²
    """
    __slots__ = ("_fx", "_fy")

    def __init__(self, x: Real = 10.0, y: Real = 0.0):
        self._fx = float(x)
        self._fy = float(y)

    @property
    def x(self) -> float:
        return self._fx

    @x.setter
    def x(self, value: Real) -> None:
        self._fx = float(value)

    @property
    def y(self) -> float:
        return self._fy

    @y.setter
    def y(self, value: Real) -> None:
        self._fy = float(value)

    def apply(self, dt: float, alive: np.ndarray, positions: np.ndarray, velocities: np.ndarray) -> None:
        velocities[alive, 0] += self._fx * dt
        velocities[alive, 1] += self._fy * dt