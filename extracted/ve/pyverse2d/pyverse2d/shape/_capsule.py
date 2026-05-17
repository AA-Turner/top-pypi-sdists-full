# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._internal import over
from ..abc import Shape
from ..math import Point

import numpy as np
from numpy.typing import NDArray

from numbers import Real
from typing import Iterator, ClassVar
import math

# ======================================== SHAPE ========================================
class Capsule(Shape):
    """Forme géométrique 2D immuable : Capsule

    Args:
        radius: rayon des demi-cercles
        height: hauteur totale de la capsule
    """
    __slots__ = ("_radius", "_height")

    _ID: ClassVar[str] = "capsule"
    _IS_PRIMITIVE: ClassVar[bool] = True

    CIRCLE_SEGMENTS: ClassVar[int] = 64

    def __init__(self, radius: Real, height: Real):
        # Transtypage et vérifications
        radius = float(radius)
        height = float(height)

        if __debug__:
            over(height, 0, include=False)
            over(radius, 0, include=False)

        # Attributs publiques
        self._height: float = height
        self._radius: float = min(self._height * 0.5, radius)

        # Initialisation de la forme
        super().__init__()

    # ======================================== CONVERSIONS ========================================
    def __repr__(self) -> str:
        """Renvoie une représentation de la capsule"""
        return f"Capsule(radius={self._radius}, height={self._height})"

    def __str__(self) -> str:
        """Renvoie une description de la capsule"""
        return f"Capsule[r={self._radius} h={self._height} | area={self.get_area():.4g}]"

    def __iter__(self) -> Iterator[float]:
        """Renvoie les composants dans un itérateur"""
        yield self._radius
        yield self._height

    def __hash__(self) -> int:
        """Renvoie le hash de la capsule"""
        return hash((self._radius, self._height))

    # ======================================== PROPERTIES ========================================
    @property
    def radius(self) -> float:
        """Rayon des demi-cercles

        Le rayon doit être un ``Real`` *positif non nul*.
        """
        return self._radius

    @property
    def height(self) -> float:
        """Hauteur totale de la capsule

        La hauteut doit être un ``Real`` *positif non nul*.
        """
        return self._height

    @property
    def width(self) -> float:
        """Largeur de la capsule"""
        return 2.0 * self._radius

    @property
    def spine(self) -> float:
        """Longueur du segment central"""
        return self._height - 2.0 * self._radius

    # ======================================== GEOMETRY ========================================
    def get_perimeter(self) -> float:
        """Renvoie le périmètre de la capsule"""
        return 2.0 * self.spine + 2.0 * math.pi * self._radius

    def get_area(self) -> float:
        """Renvoie l'aire de la capsule"""
        return self.width * self.spine + math.pi * self._radius ** 2

    def get_bounding_box(self) -> tuple[float, float, float, float]:
        """Renvoie ``(x_min, y_min, x_max, y_max)`` en espace local"""
        r, hh = self._radius, self._height * 0.5
        return (-r, -hh, r, hh)

    def compute_vertices(self) -> NDArray[np.float32]:
        """Contour polygonal de la capsule orientée verticalement"""
        half = self.CIRCLE_SEGMENTS // 2
        half_spine = self.spine * 0.5
        r = self._radius

        # Arc supérieur
        top_angles = np.linspace(math.pi, 0.0, half, endpoint=False, dtype=np.float32)
        top_arc = np.stack([np.cos(top_angles) * r, np.sin(top_angles) * r + half_spine], axis=1)

        # Arc inférieur
        bot_angles = np.linspace(0.0, -math.pi, half, endpoint=False, dtype=np.float32)
        bot_arc = np.stack([np.cos(bot_angles) * r, np.sin(bot_angles) * r - half_spine], axis=1)

        return np.concatenate([top_arc, bot_arc], axis=0)

    # ======================================== COMPARATORS ========================================
    def __eq__(self, other: object) -> bool:
        """Vérifie la correspondance de deux capsules"""
        if isinstance(other, Capsule):
            return self._radius == other._radius and self._height == other._height
        return NotImplemented

    # ======================================== PREDICATES ========================================
    def contains(self, point: Point) -> bool:
        """Teste si un point est dans la capsule

        Args:
            point: ``Point`` à tester
        """
        px, py = float(point[0]), float(point[1])
        half_spine = self.spine * 0.5
        closest_y = max(-half_spine, min(half_spine, py))
        return px ** 2 + (py - closest_y) ** 2 <= self._radius ** 2
    
    def is_convex(self) -> bool:
        """Vérifie la convexité"""
        return True

    # ======================================== INTERFACE ========================================
    def copy(self) -> Capsule:
        """Renvoie une copie de la capsule"""
        return Capsule(self._radius, self._height)
    
# ======================================== EXPORTS ========================================
__all__ = [
    "Capsule",
]