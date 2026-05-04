# ======================================== IMPORTS ========================================
from __future__ import annotations

from ...abc import ParticleEmitter

from ._particle import Particle

import numpy as np
import math
from numbers import Real

# ======================================== EMITTER ========================================
class LineEmitter(ParticleEmitter):
    """Emetteur linéaire: émission depuis un segment

    Args:
        x1: x du premier point
        y1: y du premier point
        x2: x du second point
        y2: y du second point
        particle: pattern de particule
        max_particles: nombre maximum de particules simultanées
        rate: taux d'émission en particules/seconde
        normal: True pour émettre perpendiculairement au segment, False pour direction aléatoire
    """
    __slots__ = ("x1", "y1", "x2", "y2", "_normal")

    def __init__(
        self,
        x1: Real = 0.0,
        y1: Real = 0.0,
        x2: Real = 100.0,
        y2: Real = 0.0,
        *,
        normal: bool = True,
        particle: Particle = None,
        max_particles: int = 500,
        rate: Real = 50.0,
    ):
        super().__init__(x1, y1, particle=particle, max_particles=max_particles, rate=rate)
        self.x1 = float(x1)
        self.y1 = float(y1)
        self.x2 = float(x2)
        self.y2 = float(y2)
        self._normal = bool(normal)

    def _emit(self, count: int) -> tuple[np.ndarray, np.ndarray]:
        p = self._particle
        t = np.random.uniform(0.0, 1.0, count)

        px = self.x1 + t * (self.x2 - self.x1)
        py = self.y1 + t * (self.y2 - self.y1)
        positions = np.stack([px, py], axis=1).astype(np.float32)

        speeds = np.random.uniform(p.speed[0], p.speed[1], count)
        if self._normal:
            dx  = self.x2 - self.x1
            dy  = self.y2 - self.y1
            lng = math.sqrt(dx**2 + dy**2) or 1.0
            nx, ny = -dy / lng, dx / lng
            velocities = np.stack([
                np.full(count, nx) * speeds,
                np.full(count, ny) * speeds,
            ], axis=1).astype(np.float32)
        else:
            angles = np.random.uniform(0.0, 2.0 * math.pi, count)
            velocities = np.stack([speeds * np.cos(angles), speeds * np.sin(angles)], axis=1).astype(np.float32)

        return positions, velocities