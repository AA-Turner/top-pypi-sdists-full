# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._internal import expect, not_null, positive
from ..abc import Shape
from ..math import Point

from numbers import Real
from typing import Iterator
import math
import numpy as np
from numpy.typing import NDArray

# ======================================== SHAPE ========================================
class Circle(Shape):
    """Forme géométrique 2D immuable : Cercle

    Args:
        radius: rayon du cercle
    """
    __slots__ = ("_radius",)

    CIRCLE_SEGMENTS: int = 64

    def __init__(self, radius: Real):
        self._radius: float = float(positive(not_null(expect(radius, Real))))
        super().__init__()

    # ======================================== CONVERSIONS ========================================
    def __repr__(self) -> str:
        """Renvoie une représentation du cercle"""
        return f"Circle(radius={self._radius})"

    def __str__(self) -> str:
        """Renvoie une description lisible du cercle"""
        return f"Circle[r={self._radius} | area={self.get_area():.4g}]"

    def __iter__(self) -> Iterator[float]:
        """Renvoie les composants dans un itérateur"""
        yield self._radius

    def __hash__(self) -> int:
        """Renvoie le hash du cercle"""
        return hash(self._radius)

    # ======================================== PROPERTIES ========================================
    @property
    def radius(self) -> float:
        """Rayon du cercle
        
        Le rayon doit être un *réel positif non nul*.
        """
        return self._radius

    @property
    def diameter(self) -> float:
        """Diamètre du cercle"""
        return 2.0 * self._radius
    
    # ======================================== GEOMETRY ========================================
    def get_perimeter(self) -> float:
        """Renvoie le périmètre du cercle"""
        return 2.0 * math.pi * self._radius

    def get_area(self) -> float:
        """Renvoie l'aire du cercle"""
        return math.pi * self._radius ** 2

    def get_bounding_box(self) -> tuple[float, float, float, float]:
        """Renvoie (x_min, y_min, x_max, y_max) en espace local"""
        r = self._radius
        return (-r, -r, r, r)

    def compute_vertices(self) -> NDArray[np.float32]:
        """Approximation polygonale du cercle"""
        angles = np.linspace(0.0, 2.0 * math.pi, self.CIRCLE_SEGMENTS, endpoint=False, dtype=np.float32)
        return np.stack([np.cos(angles) * self._radius, np.sin(angles) * self._radius], axis=1)

    # ======================================== COMPARATORS ========================================
    def __eq__(self, other: object) -> bool:
        """Vérifie la correspondance de deux cercles"""
        if isinstance(other, Circle):
            return self._radius == other._radius
        return NotImplemented

    # ======================================== PREDICATES ========================================
    def contains(self, point: Point) -> bool:
        """Teste si un point est dans le cercle

        Args:
            point: point à tester
        """
        return float(point[0]) ** 2 + float(point[1]) ** 2 <= self._radius ** 2
    
    def is_convex(self) -> bool:
        """Vérifie la convexité"""
        return True

    # ======================================== COLLECTIONS ========================================
    def copy(self) -> Circle:
        """Renvoie une copie du cercle"""
        return Circle(self._radius)