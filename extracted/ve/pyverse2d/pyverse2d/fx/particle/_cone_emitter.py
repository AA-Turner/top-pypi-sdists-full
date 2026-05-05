# ======================================== IMPORTS ========================================
from __future__ import annotations

from ...abc import ParticleEmitter
from ...math import Point

from ._particle import Particle

import numpy as np
from numbers import Real

# ======================================== EMITTER ========================================
class ConeEmitter(ParticleEmitter):
    """Emetteur conique: émission dans un cône directionnel

    Args:
        position: position
        direction: angle de la direction principale en degrés
        spread: demi-angle du cône en degrés
        particle: pattern de particule
        max_particles: nombre maximum de particules simultanées
        rate: taux d'émission en particules/seconde
        active: état initial
    """
    __slots__ = ("_direction", "_spread")

    def __init__(
        self,
        position: Point = (0.0, 0.0),
        *,
        direction: Real = 90.0,
        spread: Real = 15.0,
        particle: Particle = None,
        max_particles: int = 500,
        rate: Real = 50.0,
        active: bool = False,
    ):
        # Transtypage
        direction = float(direction)
        spread = float(spread)

        # Initialisation de l'émetteur
        super().__init__(position, particle=particle, max_particles=max_particles, rate=rate, active=active)

        # Attributs publiques
        self._direction = direction
        self._spread = spread

    # ======================================== PROPERTIES ========================================
    @property
    def direction(self) -> float:
        """Angle directionnel du cône

        Cette propriété fixe l'angle du cône d'émissione.
        L'angle est *en degrés* et la rotation se fait dans le sens trigonométrique *(CCW)*.
        Mettre cette propriété à ``0.0`` pour orienter le cône vers ``(1.0, 0.0)``.
        """
        return self._direction
    
    @direction.setter
    def direction(self, value: Real) -> None:
        value = float(value)
        self._direction = value

    @property
    def spread(self) -> float:
        """Demi angle du cône

        Cette propriété règle la dispersion de l'émission.
        Metre cette propriété à ``0.0`` pour une émission en ligne droite.
        """
        return self._spread
    
    @spread.setter
    def spread(self, value: Real) -> None:
        value = float(value)
        self._spread = value

    # ======================================== INTERNALS ========================================
    def _emit(self, count: int) -> tuple[np.ndarray, np.ndarray]:
        p = self._particle

        angles = np.radians(self._direction + np.random.uniform(-self._spread, self._spread, count))
        speeds = np.random.uniform(p.speed[0], p.speed[1], count)

        positions = np.full((count, 2), self._position.to_tuple(), dtype=np.float32)
        velocities = np.stack([speeds * np.cos(angles), speeds * np.sin(angles)], axis=1).astype(np.float32)
        return positions, velocities