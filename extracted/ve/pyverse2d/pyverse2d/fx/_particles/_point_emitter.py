# ======================================== IMPORTS ========================================
from __future__ import annotations

from ...abc import ParticleEmitter

from ._particle import Particle

import numpy as np
from numbers import Real

# ======================================== EMITTER ========================================
class PointEmitter(ParticleEmitter):
    """Emetteur ponctuel: émission depuis un point dans toutes les directions

    Args:
        x: position horizontale
        y: position verticale
        particle: pattern de particule
        max_particles: nombre maximum de particules simultanées
        rate: taux d'émission en particules/seconde
        angle: intervalle d'angle d'émission (min, max) en degrés
    """
    __slots__ = ("_angle_min", "_angle_max")

    def __init__(
        self,
        x: Real = 0.0,
        y: Real = 0.0,
        *,
        particle: Particle = None,
        max_particles: int = 500,
        rate: Real = 50.0,
        angle: tuple[Real, Real] = (0.0, 360.0),
    ):
        super().__init__(x, y, particle=particle, max_particles=max_particles, rate=rate)
        self._angle_min = float(angle[0])
        self._angle_max = float(angle[1])

    def _emit(self, count: int) -> tuple[np.ndarray, np.ndarray]:
        p = self._particle
        speeds = np.random.uniform(p.speed[0], p.speed[1], count)
        angles = np.radians(np.random.uniform(self._angle_min, self._angle_max, count))

        positions = np.full((count, 2), (self.x, self.y), dtype=np.float32)
        velocities = np.stack([speeds * np.cos(angles), speeds * np.sin(angles)], axis=1).astype(np.float32)
        return positions, velocities