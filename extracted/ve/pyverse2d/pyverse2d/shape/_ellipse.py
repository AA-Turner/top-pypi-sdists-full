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
class Ellipse(Shape):
    """Forme géométrique 2D immuable : Ellipse

    Args:
        rx: rayon horizontal de l'ellipse
        ry: rayon vertical de l'ellipse
    """
    __slots__ = ("_rx", "_ry")

    CIRCLE_SEGMENTS: int = 64

    def __init__(self, rx: Real, ry: Real):
        self._rx: float = float(positive(not_null(expect(rx, Real))))
        self._ry: float = float(positive(not_null(expect(ry, Real))))
        super().__init__()

    # ======================================== CONVERSIONS ========================================
    def __repr__(self) -> str:
        """Renvoie une représentation de l'ellipse"""
        return f"Ellipse(rx={self._rx}, ry={self._ry})"

    def __str__(self) -> str:
        """Renvoie une description lisible de l'ellipse"""
        return f"Ellipse[rx={self._rx} ry={self._ry} | area={self.get_area():.4g}]"

    def __iter__(self) -> Iterator[float]:
        """Renvoie les composants dans un itérateur"""
        yield self._rx
        yield self._ry

    def __hash__(self) -> int:
        """Renvoie le hash de l'ellipse"""
        return hash((self._rx, self._ry))

    # ======================================== PROPERTIES ========================================
    @property
    def rx(self) -> float:
        """Rayon horizontal de l'ellipse

        Le rayon doit être un *réel positif non nul*.
        """
        return self._rx

    @property
    def ry(self) -> float:
        """Rayon vertical de l'ellipse
        
        Le rayon doit être un *réel positif non nul*.
        """
        return self._ry

    # ======================================== GEOMETRY ========================================
    def get_perimeter(self) -> float:
        """Renvoie le périmètre de l'ellipse"""
        h = ((self._rx - self._ry) ** 2) / ((self._rx + self._ry) ** 2)
        return math.pi * (self._rx + self._ry) * (1.0 + (3.0 * h) / (10.0 + math.sqrt(4.0 - 3.0 * h)))

    def get_area(self) -> float:
        """Renvoie l'aire de l'ellipse"""
        return math.pi * self._rx * self._ry

    def get_bounding_box(self) -> tuple[float, float, float, float]:
        """Renvoie ``(x_min, y_min, x_max, y_max)`` en espace local"""
        return (-self._rx, -self._ry, self._rx, self._ry)

    def compute_vertices(self) -> NDArray[np.float32]:
        """Approximation polygonale de l'ellipse"""
        angles = np.linspace(0.0, 2.0 * math.pi, self.CIRCLE_SEGMENTS, endpoint=False, dtype=np.float32)
        return np.stack([np.cos(angles) * self._rx, np.sin(angles) * self._ry], axis=1)

    # ======================================== COMPARATORS ========================================
    def __eq__(self, other: object) -> bool:
        """Vérifie la correspondance de deux ellipses"""
        if isinstance(other, Ellipse):
            return self._rx == other._rx and self._ry == other._ry
        return NotImplemented

    # ======================================== PREDICATES ========================================
    def contains(self, point: Point) -> bool:
        """Teste si un point est dans l'ellipse

        Args:
            point: point à tester
        """
        px, py = float(point[0]), float(point[1])
        return (px / self._rx) ** 2 + (py / self._ry) ** 2 <= 1.0
    
    def is_convex(self) -> bool:
        """Vérifie la convexité"""
        return True

    # ======================================== COLLECTIONS ========================================
    def copy(self) -> Ellipse:
        """Renvoie une copie de l'ellipse"""
        return Ellipse(self._rx, self._ry)