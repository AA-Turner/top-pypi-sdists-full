# ======================================== IMPORTS ========================================
from __future__ import annotations

from ...abc import ParticleEmitter
from ...math import Point

from ._particle import Particle

import numpy as np
import math
from numbers import Real

# ======================================== EMITTER ========================================
class LineEmitter(ParticleEmitter):
    """Emetteur linéaire: émission depuis un segment

    Args:
        p1: position du premier point
        p2: position du second point
        particle: pattern de particule
        max_particles: nombre maximum de particules simultanées
        rate: taux d'émission en particules/seconde
        normal: True pour émettre perpendiculairement au segment, False pour direction aléatoire
        active: état initial
    """
    __slots__ = ("_p1", "_p2", "_normal")

    def __init__(
        self,
        p1: Point = (0.0, 0.0),
        p2: Point = (1.0, 0.0),
        *,
        normal: bool = True,
        particle: Particle = None,
        max_particles: int = 500,
        rate: Real = 50.0,
        active: bool = False,
    ):
        # Transtypage
        p1 = Point(p1)
        p2 = Point(p2)
        normal = bool(normal)

        # Initialisation de l'émetteur
        super().__init__(p1, particle=particle, max_particles=max_particles, rate=rate, active=active)

        # Attributs publiques
        self._p1: Point = p1
        self._p2: Point = p2
        self._normal = normal

    # ======================================== PROPERTIES ========================================
    @property
    def p1(self) -> Point:
        """Position du premier point

        La position peut être un objet ``Point`` ou n'importe quel tuple ``(x, y)``.
        """
        return self._p1


    @p1.setter
    def p1(self, value: Point) -> None:
        value = Point(value)
        self._p1 = value
        self.position = value

    # ======================================== INTERNALS ========================================
    def _emit(self, count: int) -> tuple[np.ndarray, np.ndarray]:
        p = self._particle
        t = np.random.uniform(0.0, 1.0, count)
        x1, y1 = self._p1
        x2, y2 = self._p2

        px = x1 + t * (x2 - x1)
        py = y1 + t * (y2 - y1)
        positions = np.stack([px, py], axis=1).astype(np.float32)

        speeds = np.random.uniform(p.speed[0], p.speed[1], count)
        if self._normal:
            dx = x2 - x1
            dy = y2 - y1
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