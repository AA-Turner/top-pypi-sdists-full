# ======================================== IMPORTS ========================================
from __future__ import annotations

from ...abc import ParticleModifier
from ...math import Point

import numpy as np
from numbers import Real

# ======================================== MODIFIER ========================================
class Attractor(ParticleModifier):
    """Modificateur d'attraction/répulsion: attire ou repousse les particules vers un point

    Args:
        position: position du point d'attraction
        strength: intensité de la force *(positif = attraction, négatif = répulsion)*
        radius: rayon d'influence en unités monde, 0 = infini
        falloff: atténuation de la force avec la distance *(True = linéaire, False = constante)*
    """
    __slots__ = (
        "_position",
        "_strength", "_radius", "_falloff",
    )

    def __init__(
        self,
        position: Point = (0.0, 0.0),
        strength: Real = 50.0,
        radius: Real = 0.0,
        falloff: bool = True,
    ):
        # Transtypage et vérifications
        position = Point(position)
        strength = float(strength)
        radius = abs(float(radius))
        falloff = bool(falloff)

        # Attributs publiques
        self._position = position
        self._strength = strength
        self._radius = radius
        self._falloff = falloff

    # ======================================== PROPERTIES ========================================
    @property
    def position(self) -> Point:
        """Position

        La position peut être un objet ``Point`` ou un tuple ``(x, y)``.
        """
        return self._position
    
    @position.setter
    def position(self, value: Point) -> None:
        self._position.x, self._position.y = value

    @property
    def x(self) -> float:
        """Position horizontale
        
        La coordonnée doit être un ``Réel``.
        """
        return self._position.x
    
    @x.setter
    def x(self, value: Real) -> None:
        self._position.x = value
    
    @property
    def y(self) -> float:
        """Position verticale

        La coordonnée doit être un ``Réel``.
        """
        return self._position.y
    
    @y.setter
    def y(self, value: Real) -> None:
        self._position.y = value

    @property
    def strength(self) -> float:
        """Intensité d'attraction
        
        Mettre cette propriété à une valeur positive pour une attraction.
        Mettre cette propriété à une valeur négative pour une répulsion.
        """
        return self._strength

    @strength.setter
    def strength(self, value: Real) -> None:
        value = float(value)
        self._strength = value

    @property
    def radius(self) -> float:
        """Rayon d'attraction
        
        Cette propriété est en *unités mondes*.
        """
        return self._radius

    @radius.setter
    def radius(self, value: Real) -> None:
        value = float(value)
        self._radius = value

    @property
    def falloff(self) -> bool:
        """Atténuation distantielle
        
        Mettre cette propriété à ``True`` pour une atténuation linéaire de la force d'attraction selon la distance.
        Mettre cette propriété à ``False`` pour une force constante dans le rayon d'attraction.
        """
        return self._falloff

    @falloff.setter
    def falloff(self, value: bool) -> None:
        value = bool(value)
        self._falloff = value

    # ======================================== INTERFACE ========================================
    def apply(self, dt: float, alive: np.ndarray, positions: np.ndarray, velocities: np.ndarray) -> None:
        dx = self._position.x - positions[alive, 0]
        dy = self._position.y - positions[alive, 1]

        dist = np.sqrt(dx ** 2 + dy ** 2)
        dist = np.maximum(dist, 0.0001)

        # Filtrage par rayon si défini
        if self._radius > 0.0:
            mask = dist <= self._radius
            dx, dy, dist = dx[mask], dy[mask], dist[mask]
            if not len(dx):
                return

        # Direction normalisée
        nx = dx / dist
        ny = dy / dist

        # Force — atténuation linéaire selon la distance si falloff activé
        if self._falloff and self._radius > 0.0:
            force = self._strength * (1.0 - dist / self._radius)
        else:
            force = self._strength

        if self._radius > 0.0:
            idx = np.where(alive)[0][mask]
        else:
            idx = np.where(alive)[0]

        velocities[idx, 0] += nx * force * dt
        velocities[idx, 1] += ny * force * dt