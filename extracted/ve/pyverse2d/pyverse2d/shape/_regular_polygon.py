# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._internal import positive, not_null, over
from ..math.vertices import center_bbox
from ..abc import Shape
from ..math import Point

from numbers import Real, Integral
import numpy as np
from numpy.typing import NDArray
import math

# ======================================== SHAPE ========================================
class RegularPolygon(Shape):
    """Forme géométrique 2D immuable : Polygone régulier

    Args:
        sides: nombre de côtés (minimum 3)
        radius: rayon du cercle circonscrit
    """
    __slots__ = ("_sides", "_radius")

    def __init__(self, sides: Integral, radius: Real):
        # Attributs publiques
        self._sides: int = int(sides)
        self._radius: float = float(radius)

        if __debug__:
            over(self._sides, 3)
            positive(not_null(self._radius))

        super().__init__()

    # ======================================== CONVERSIONS ========================================
    def __repr__(self) -> str:
        """Renvoie une représentation du polygone régulier"""
        return f"RegularPolygon(sides={self._sides}, radius={self._radius})"

    def __str__(self) -> str:
        """Renvoie une description lisible du polygone régulier"""
        return f"RegularPolygon[{self._sides} sides | r={self._radius} | area={self.get_area():.4g}]"

    def __iter__(self):
        yield self._sides
        yield self._radius

    def __hash__(self) -> int:
        """Renvoie le hash du polygone régulier"""
        return hash((self._sides, self._radius))

    # ======================================== PROPERTIES ========================================
    @property
    def radius(self) -> float:
        """Rayon du cercle circonscrit

        Le rayon doit être un *réel positif non nul*.
        """
        return self._radius

    @property
    def sides(self) -> int:
        """Nombre de côtés"""
        return self._sides

    @property
    def side_length(self) -> float:
        """Longueur d'un côté"""
        return 2.0 * self._radius * math.sin(math.pi / self._sides)

    # ======================================== GEOMETRY ========================================
    def get_perimeter(self) -> float:
        """Renvoie le périmètre du polygone régulier"""
        return self._sides * self.side_length

    def get_area(self) -> float:
        """Renvoie l'aire du polygone régulier"""
        return 0.5 * self._sides * self._radius ** 2 * math.sin(2.0 * math.pi / self._sides)

    def get_bounding_box(self) -> tuple[float, float, float, float]:
        """Renvoie ``(x_min, y_min, x_max, y_max)`` en espace local"""
        v = self.get_vertices()
        return (float(v[:, 0].min()), float(v[:, 1].min()), float(v[:, 0].max()), float(v[:, 1].max()))

    def compute_vertices(self) -> NDArray[np.float32]:
        """Renvoie les N sommets du polygone régulier"""
        angles = np.linspace(0.0, 2.0 * math.pi, self._sides, endpoint=False, dtype=np.float32)
        verts = np.stack([np.cos(angles) * self._radius, np.sin(angles) * self._radius], axis=1)
        return center_bbox(verts)

    # ======================================== COMPARATORS ========================================
    def __eq__(self, other: object) -> bool:
        """Vérifie la correspondance de deux polygones réguliers"""
        if isinstance(other, RegularPolygon):
            return self._sides == other._sides and math.isclose(self._radius, other._radius)
        return NotImplemented

    # ======================================== PREDICATES ========================================
    def contains(self, point: Point) -> bool:
        """Teste si un point est dans le polygone régulier

        Args:
            point: point à tester
        """
        if self._vertices is None:
            self._vertices = self.get_vertices()
        px, py = float(point[0]), float(point[1])
        n = len(self._vertices)
        inside = False
        j = n - 1
        for i in range(n):
            xi, yi = float(self._vertices[i][0]), float(self._vertices[i][1])
            xj, yj = float(self._vertices[j][0]), float(self._vertices[j][1])
            if ((yi > py) != (yj > py)) and (px < (xj - xi) * (py - yi) / (yj - yi) + xi):
                inside = not inside
            j = i
        return inside
    
    def is_convex(self) -> bool:
        """Vérifie la convexité"""
        return True

    # ======================================== PUBLIC METHODS ========================================
    def copy(self) -> RegularPolygon:
        """Renvoie une copie du polygone régulier"""
        return RegularPolygon(self._sides, self._radius)

# ======================================== FAÇADES ========================================
class RegularTriangle(RegularPolygon):
    """Forme géométrique 2D : Triangle équilatéral"""
    __slots__ = ()

    def __init__(self, radius: Real):
        super().__init__(3, radius)

    def __repr__(self) -> str:
        return f"Triangle(radius={self._radius})"

    def copy(self) -> RegularTriangle:
        return RegularTriangle(self._radius)


class RegularPentagon(RegularPolygon):
    """Forme géométrique 2D : Pentagone régulier"""
    __slots__ = ()

    def __init__(self, radius: Real):
        super().__init__(5, radius)

    def __repr__(self) -> str:
        return f"Pentagon(radius={self._radius})"

    def copy(self) -> RegularPentagon:
        return RegularPentagon(self._radius)


class RegularHexagon(RegularPolygon):
    """Forme géométrique 2D : Hexagone régulier"""
    __slots__ = ()

    def __init__(self, radius: Real):
        super().__init__(6, radius)

    def __repr__(self) -> str:
        return f"Hexagon(radius={self._radius})"

    def copy(self) -> RegularHexagon:
        return RegularHexagon(self._radius)


class RegularOctagon(RegularPolygon):
    """Forme géométrique 2D : Octogone régulier"""
    __slots__ = ()

    def __init__(self, radius: Real):
        super().__init__(8, radius)

    def __repr__(self) -> str:
        return f"Octagon(radius={self._radius})"

    def copy(self) -> RegularOctagon:
        return RegularOctagon(self._radius)