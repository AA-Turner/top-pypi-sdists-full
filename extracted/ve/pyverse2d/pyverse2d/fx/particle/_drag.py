# ======================================== IMPORTS ========================================
from __future__ import annotations

from ...abc import ParticleModifier

import numpy as np
from numbers import Real

# ======================================== MODIFIER ========================================
class Drag(ParticleModifier):
    """Modificateur de frottement — ralentit les particules proportionnellement à leur vitesse

    Args:
        coefficient: facteur de résistance [0, 1[ — 0 = aucun frottement
    """
    __slots__ = ("_coef",)

    def __init__(self, coefficient: Real = 0.05):
        self._coef = float(coefficient)

        if __debug__:
            if not 0.0 <= self._coef < 1.0:
                raise ValueError(f"coefficient must be within [0, 1[, got {self._coef}")

    @property
    def coefficient(self) -> float:
        return self._coef

    @coefficient.setter
    def coefficient(self, value: Real) -> None:
        value = float(value)
        if __debug__:
            if not 0.0 <= value < 1.0:
                raise ValueError(f"coefficient must be within [0, 1[, got {value}")
        self._coef = value

    def apply(self, dt: float, alive: np.ndarray, positions: np.ndarray, velocities: np.ndarray) -> None:
        velocities[alive] *= max(0.0, 1.0 - self._coef * dt)