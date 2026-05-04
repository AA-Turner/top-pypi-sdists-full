# ======================================== IMPORTS ========================================
from __future__ import annotations

from ...abc import ParticleEmitter

from ._particle import Particle

import numpy as np
from numbers import Real

# ======================================== EMITTER ========================================
class ConeEmitter(ParticleEmitter):
    """Emetteur conique: émission dans un cône directionnel

    Args:
        x: position horizontale
        y: position verticale
        direction: angle de la direction principale en degrés
        spread: demi-angle du cône en degrés
        particle: pattern de particule
        max_particles: nombre maximum de particules simultanées
        rate: taux d'émission en particules/seconde
    """
    __slots__ = ("_direction", "_spread")

    def __init__(
        self,
        x: Real = 0.0,
        y: Real = 0.0,
        *,
        direction: Real = 90.0,
        spread: Real = 15.0,
        particle: Particle = None,
        max_particles: int = 500,
        rate: Real = 50.0,
    ):
        super().__init__(x, y, particle=particle, max_particles=max_particles, rate=rate)
        self._direction = float(direction)
        self._spread = float(spread)

    def _emit(self, count: int) -> tuple[np.ndarray, np.ndarray]:
        p = self._particle

        angles = np.radians(
            self._direction + np.random.uniform(-self._spread, self._spread, count)
        )
        speeds = np.random.uniform(p.speed[0], p.speed[1], count)

        positions = np.full((count, 2), (self.x, self.y), dtype=np.float32)
        velocities = np.stack([speeds * np.cos(angles), speeds * np.sin(angles)], axis=1).astype(np.float32)
        return positions, velocities