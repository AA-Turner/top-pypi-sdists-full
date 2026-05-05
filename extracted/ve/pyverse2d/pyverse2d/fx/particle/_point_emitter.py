# ======================================== IMPORTS ========================================
from __future__ import annotations

from ...abc import ParticleEmitter
from ...math import Point

from ._particle import Particle

import numpy as np
from numbers import Real

# ======================================== EMITTER ========================================
class PointEmitter(ParticleEmitter):
    """Emetteur ponctuel: émission depuis un point dans toutes les directions

    Args:
        position: position
        particle: pattern de particule
        max_particles: nombre maximum de particules simultanées
        rate: taux d'émission en particules/seconde
        active: état initial
    """
    __slots__ = tuple()

    def __init__(
        self,
        position: Point = (0.0, 0.0),
        *,
        particle: Particle = None,
        max_particles: int = 500,
        rate: Real = 50.0,
        active: bool = False,
    ):
        # Initialisation de l'émetteur
        super().__init__(position, particle=particle, max_particles=max_particles, rate=rate)

    # ======================================== INTERNALS ========================================
    def _emit(self, count: int) -> tuple[np.ndarray, np.ndarray]:
        p = self._particle
        speeds = np.random.uniform(p.speed[0], p.speed[1], count)
        angles = np.radians(np.random.uniform(0, 360, count))

        positions = np.full((count, 2), self._position.to_tuple(), dtype=np.float32)
        velocities = np.stack([speeds * np.cos(angles), speeds * np.sin(angles)], axis=1).astype(np.float32)
        return positions, velocities