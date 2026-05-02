# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..abc import Shape
from ..math import Point
from ..math.vertices import is_convex, center_bbox, order_ccw

import numpy as np
from numpy.typing import NDArray

# ======================================== SHAPE ========================================
class Polygon(Shape):
    """Forme géométrique 2D immuable : Polygone quelconque

    Args:
        points: sommets du polygone (minimum 3, sans doublons)
    """
    __slots__ = ("_source_vertices", "_convex")

    def __init__(self, *points: Point):
        self._source_vertices: NDArray[np.float32] = np.asarray(points, dtype=np.float32)

        if __debug__:
            if len(points) < 3:
                raise ValueError("Polygon must have at least 3 points")
            if np.unique(self._source_vertices, axis=0).shape[0] != len(self._source_vertices):
                raise ValueError("Polygon must not have duplicate points")
        
        self._source_vertices = center_bbox(order_ccw(self._source_vertices))
        self._convex: bool = is_convex(self._source_vertices)
        super().__init__()

    # ======================================== CONVERSIONS ========================================
    def __repr__(self) -> str:
        pts = [tuple(v) for v in self._source_vertices]
        return f"Polygon(points={pts})"

    def __str__(self) -> str:
        return f"Polygon[{len(self._source_vertices)} pts | area={self.get_area():.4g} | perimeter={self.get_perimeter():.4g}]"

    def __len__(self) -> int:
        return len(self._source_vertices)

    def __hash__(self) -> int:
        return hash(tuple(map(tuple, self._source_vertices)))

    # ======================================== GEOMETRY ========================================
    def get_perimeter(self) -> float:
        """Renvoie le périmètre du polygone"""
        v = self._source_vertices
        diff = np.roll(v, -1, axis=0) - v
        return float(np.linalg.norm(diff, axis=1).sum())

    def get_area(self) -> float:
        """Renvoie l'aire du polygone"""
        v = self._source_vertices
        x, y = v[:, 0], v[:, 1]
        return float(abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1))) * 0.5)

    def get_bounding_box(self) -> tuple[float, float, float, float]:
        """Renvoie (x_min, y_min, x_max, y_max) en espace local"""
        v = self._source_vertices
        return (float(v[:, 0].min()), float(v[:, 1].min()),
                float(v[:, 0].max()), float(v[:, 1].max()))

    def compute_vertices(self) -> NDArray[np.float32]:
        """Renvoie les sommets du polygone (copie des sources)"""
        return self._source_vertices.copy()

    # ======================================== COMPARATORS ========================================
    def __eq__(self, other: object) -> bool:
        """Vérifie la correspondance de deux polygones"""
        if isinstance(other, Polygon) and len(self) == len(other):
            n = len(self)
            sv = self._source_vertices
            ov = other._source_vertices
            return any(np.allclose(sv, np.roll(ov, offset, axis=0)) for offset in range(n))
        return NotImplemented

    # ======================================== PREDICATES ========================================
    def contains(self, point: Point) -> bool:
        """Teste si un point est dans le polygone

        Args:
            point: point à tester
        """
        v   = self._source_vertices
        px, py = float(point[0]), float(point[1])
        n   = len(v)
        inside = False
        j = n - 1
        for i in range(n):
            xi, yi = float(v[i][0]), float(v[i][1])
            xj, yj = float(v[j][0]), float(v[j][1])
            if ((yi > py) != (yj > py)) and (px < (xj - xi) * (py - yi) / (yj - yi) + xi):
                inside = not inside
            j = i
        return inside
    
    def is_convex(self) -> bool:
        """Vérifie la convexité"""
        return self._convex

    # ======================================== PUBLIC METHODS ========================================
    def copy(self) -> Polygon:
        """Renvoie une copie du polygone"""
        return Polygon(*[Point(float(v[0]), float(v[1])) for v in self._source_vertices])