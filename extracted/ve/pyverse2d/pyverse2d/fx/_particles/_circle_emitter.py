# ======================================== IMPORTS ========================================
from __future__ import annotations

from ...abc import ParticleEmitter

from ._particle import Particle

import numpy as np
import math
from numbers import Real

# ======================================== EMITTER ========================================
class CircleEmitter(ParticleEmitter):
    """Emetteur circulaire: émission depuis le périmètre ou l'intérieur d'un cercle

    Args:
        x: position horizontale du centre
        y: position verticale du centre
        radius: rayon du cercle en unités monde
        fill: True pour émettre depuis l'intérieur, False pour le périmètre uniquement
        particle: pattern de particule
        max_particles: nombre maximum de particules simultanées
        rate: taux d'émission en particules/seconde
        outward: True pour émettre vers l'extérieur, False pour direction aléatoire
    """
    __slots__ = ("_radius", "_fill", "_outward")

    def __init__(
        self,
        x: Real = 0.0,
        y: Real = 0.0,
        *,
        radius: Real = 50.0,
        fill: bool = False,
        outward: bool = True,
        particle: Particle = None,
        max_particles: int = 500,
        rate: Real = 50.0,
    ):
        super().__init__(x, y, particle=particle, max_particles=max_particles, rate=rate)
        self._radius = float(radius)
        self._fill = bool(fill)
        self._outward = bool(outward)

    def _emit(self, count: int) -> tuple[np.ndarray, np.ndarray]:
        p = self._particle
        angles = np.random.uniform(0.0, 2.0 * math.pi, count)

        if self._fill:
            r = self._radius * np.sqrt(np.random.uniform(0.0, 1.0, count))
        else:
            r = np.full(count, self._radius)

        ox = r * np.cos(angles)
        oy = r * np.sin(angles)

        positions = np.stack([self.x + ox, self.y + oy], axis=1).astype(np.float32)

        speeds = np.random.uniform(p.speed[0], p.speed[1], count)
        if self._outward:
            norms = np.maximum(np.sqrt(ox**2 + oy**2), 1e-6)
            vx, vy = (ox / norms) * speeds, (oy / norms) * speeds
        else:
            va = np.random.uniform(0.0, 2.0 * math.pi, count)
            vx, vy = speeds * np.cos(va), speeds * np.sin(va)

        velocities = np.stack([vx, vy], axis=1).astype(np.float32)
        return positions, velocities