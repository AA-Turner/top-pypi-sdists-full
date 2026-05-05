# ======================================== IMPORTS ========================================
from __future__ import annotations

from ...abc import ParticleModifier

import numpy as np
from numbers import Real

# ======================================== MODIFIER ========================================
class Gravity(ParticleModifier):
    """Modificateur de gravité

    Args:
        x: accélération horizontale en unités monde/s²
        y: accélération verticale en unités monde/s²
    """
    __slots__ = ("_ax", "_ay")

    def __init__(self, x: Real = 0.0, y: Real = -9.8):
        self._ax = float(x)
        self._ay = float(y)

    @property
    def x(self) -> float:
        return self._ax

    @x.setter
    def x(self, value: Real) -> None:
        self._ax = float(value)

    @property
    def y(self) -> float:
        return self._ay

    @y.setter
    def y(self, value: Real) -> None:
        self._ay = float(value)

    def apply(self, dt: float, alive: np.ndarray, positions: np.ndarray, velocities: np.ndarray) -> None:
        velocities[alive, 0] += self._ax * dt
        velocities[alive, 1] += self._ay * dt