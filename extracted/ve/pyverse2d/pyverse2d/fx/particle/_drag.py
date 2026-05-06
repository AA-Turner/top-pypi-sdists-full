# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import clamped
from ...abc import ParticleModifier

import numpy as np
from numbers import Real

# ======================================== MODIFIER ========================================
class Drag(ParticleModifier):
    """Modificateur de frottement: ralentit les particules proportionnellement à leur vitesse

    Args:
        coefficient: facteur de résistance [0, 1[
    """
    __slots__ = ("_coef",)

    def __init__(self, coefficient: Real = 0.05):
        # Transtypage et vérifications
        coefficient = float(coefficient)

        if __debug__:
            clamped(coefficient)

        # Attributs publiques
        self._coefficient = coefficient

    # ======================================== PROPERTIES ========================================
    @property
    def coefficient(self) -> float:
        """Facteur de résistance *[0, 1[*"""
        return self._coefficient

    @coefficient.setter
    def coefficient(self, value: Real) -> None:
        value = float(value)
        if __debug__:
            clamped(value)
        self._coefficient = value

    # ======================================== INTERFACE ========================================
    def apply(self, dt: float, alive: np.ndarray, positions: np.ndarray, velocities: np.ndarray) -> None:
        velocities[alive] *= max(0.0, 1.0 - self._coefficient * dt)