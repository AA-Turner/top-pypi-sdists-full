# ======================================== IMPORTS ========================================
from __future__ import annotations

from ...abc import ParticleModifier

import numpy as np
from numbers import Real
import math
import random

# ======================================== MODIFIER ========================================
class Wind(ParticleModifier):
    """Modificateur de vent: force directionnelle avec rafales et turbulence

    Args:
        strength: intensité de base en unités monde/s²
        direction: direction en degrés (0 = droite, 90 = haut)
        variation: variation continue de fond
        gust_intensity: multiplicateur de force lors d'une bourrasque
        gust_duration: durée d'une bourrasque en secondes
        gust_interval: intervalle moyen entre bourrasques
        turbulence: variation aléatoire par particule
    """
    __slots__ = (
        "_strength", "_direction", "_variation",
        "_gust_intensity", "_gust_duration", "_gust_interval", "_turbulence",
        "_time", "_gust_timer", "_next_gust",
        "_fx", "_fy",
    )

    def __init__(
        self,
        strength: Real = 10.0,
        direction: Real = 0.0,
        variation: Real = 0.2,
        gust_intensity: Real = 3.0,
        gust_duration: Real = 0.4,
        gust_interval: Real = 3.0,
        turbulence: Real = 2.0,
    ):
        # Transtypage
        strength = float(strength)
        direction = float(direction)
        variation = float(variation)
        gust_intensity = float(gust_intensity)
        gust_duration = float(gust_duration)
        gust_interval = float(gust_interval)
        turbulence = float(turbulence)

        # Attributs publiques
        self._strength: float = strength
        self._direction: float = direction
        self._variation: float = variation
        self._gust_intensity: float = gust_intensity
        self._gust_duration: float = gust_duration
        self._gust_interval: float = gust_interval
        self._turbulence: float = turbulence

        # Attributs interne
        self._time: float = 0.0                 # horloge locale
        self._gust_timer: float = 0.0           # temps restant de la bourrasque active
        self._next_gust: float = gust_interval  # countdown avant prochaine

        # Calcul du vecteur directionnel
        self._update_components()

    # ======================================== PROPERTIES ========================================
    @property
    def strength(self) -> float:
        """Intensité du vent"""
        return self._strength

    @strength.setter
    def strength(self, value: Real) -> None:
        self._strength = float(value)
        self._update_components()

    @property
    def direction(self) -> float:
        """Direction du vent
        
        La direction est *en degrés* dans le sens trigonométrique *(CCW)*.
        Mettre cette propriété à ``0.0`` pour l'orienter vers ``(1, 0)``.
        """
        return self._direction

    @direction.setter
    def direction(self, value: Real) -> None:
        self._direction = float(value)
        self._update_components()

    # ======================================== INTERFACE ========================================
    def apply(self, dt: float, alive: np.ndarray, positions: np.ndarray, velocities: np.ndarray) -> None:
        self._time += dt

        # Variation continue de fond — plusieurs fréquences pour casser la périodicité
        base = (
            1.0
            + self._variation * 0.6 * math.sin(self._time * math.tau * 0.3)
            + self._variation * 0.4 * math.sin(self._time * math.tau * 0.7)
        )

        # Gestion des bourrasques
        if self._gust_timer > 0.0:
            self._gust_timer -= dt
            gust = self._gust_intensity * math.sin(math.pi * (1.0 - self._gust_timer / self._gust_duration))
        else:
            self._next_gust -= dt
            gust = 0.0
            if self._next_gust <= 0.0:
                self._gust_timer = self._gust_duration
                self._next_gust = self._gust_interval * random.uniform(0.5, 1.5)

        force = base + gust

        count = int(alive.sum())
        tx = np.random.uniform(-self._turbulence, self._turbulence, count)
        ty = np.random.uniform(-self._turbulence, self._turbulence, count)

        velocities[alive, 0] += (self._fx * force + tx) * dt
        velocities[alive, 1] += (self._fy * force + ty) * dt

    # ======================================== INTERNALS ========================================
    def _update_components(self) -> None:
        """Calcul du vecteur directionnel"""
        rad = math.radians(self._direction)
        self._fx = self._strength * math.cos(rad)
        self._fy = self._strength * math.sin(rad)