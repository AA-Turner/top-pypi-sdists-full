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
class RoundedRect(Shape):
    """Forme géométrique 2D immuable : Rectangle à coins arrondis

    Args:
        width:  largeur totale du rectangle
        height: hauteur totale du rectangle
        radius: rayon des coins arrondis
    """
    __slots__ = ("_width", "_height", "_radius")

    CIRCLE_SEGMENTS: int = 64

    def __init__(self, width: Real, height: Real, radius: Real):
        self._width:  float = float(positive(not_null(expect(width,  Real))))
        self._height: float = float(positive(not_null(expect(height, Real))))
        max_r = min(self._width, self._height) * 0.5
        self._radius: float = min(max_r, float(positive(not_null(expect(radius, Real)))))
        super().__init__()

    # ======================================== CONVERSIONS ========================================
    def __repr__(self) -> str:
        return f"RoundedRect(width={self._width}, height={self._height}, radius={self._radius})"

    def __str__(self) -> str:
        return f"RoundedRect[{self._width}x{self._height} r={self._radius} | area={self.get_area():.4g}]"

    def __iter__(self) -> Iterator[float]:
        yield self._width
        yield self._height
        yield self._radius

    def __hash__(self) -> int:
        return hash((self._width, self._height, self._radius))

    # ======================================== PROPERTIES ========================================
    @property
    def width(self) -> float:
        """Largeur totale
        
        La largeur doit être un *réel positif non nul*.
        """
        return self._width

    @property
    def height(self) -> float:
        """Hauteur totale
        
        La hauteur doit être un *réel positif non nul*.
        """
        return self._height

    @property
    def radius(self) -> float:
        """Rayon des coins

        Le rayon doit être un *réel positif non nul*.
        """
        return self._radius

    @property
    def inner_width(self) -> float:
        """Largeur du rectangle intérieur"""
        return self._width - 2.0 * self._radius

    @property
    def inner_height(self) -> float:
        """Hauteur du rectangle intérieur"""
        return self._height - 2.0 * self._radius

    # ======================================== GEOMETRY ========================================
    def get_perimeter(self) -> float:
        """Renvoie le périmètre du rectangle arrondi"""
        return 2.0 * (self.inner_width + self.inner_height) + 2.0 * math.pi * self._radius

    def get_area(self) -> float:
        """Renvoie l'aire du rectangle arrondi"""
        iw, ih, r = self.inner_width, self.inner_height, self._radius
        return iw * ih + 2.0 * r * iw + 2.0 * r * ih + math.pi * r ** 2

    def get_bounding_box(self) -> tuple[float, float, float, float]:
        """Renvoie ``(x_min, y_min, x_max, y_max)`` en espace local"""
        hw, hh = self._width * 0.5, self._height * 0.5
        return (-hw, -hh, hw, hh)

    def compute_vertices(self) -> NDArray[np.float32]:
        """Contour polygonal du rectangle arrondi"""
        quarter = self.CIRCLE_SEGMENTS // 4
        r   = self._radius
        hx  = self._width  * 0.5 - r   # centre x du coin
        hy  = self._height * 0.5 - r   # centre y du coin

        # Centres des 4 coins
        centers = np.array([
            ( hx,  hy),   # top-right
            ( hx, -hy),   # bottom-right
            (-hx, -hy),   # bottom-left
            (-hx,  hy),   # top-left
        ], dtype=np.float32)

        # Plages angulaires pour chaque coin
        starts = [0.0, -0.5 * math.pi, -math.pi, -1.5 * math.pi]

        arcs = []
        for (cx, cy), start in zip(centers, starts):
            angles = np.linspace(start, start - 0.5 * math.pi, quarter, endpoint=False, dtype=np.float32)
            arc = np.stack([cx + np.cos(angles) * r, cy + np.sin(angles) * r], axis=1)
            arcs.append(arc)

        return np.concatenate(arcs, axis=0)

    # ======================================== COMPARATORS ========================================
    def __eq__(self, other: object) -> bool:
        """Vérifie la correspondance de deux rectangles arrondis"""
        if isinstance(other, RoundedRect):
            return (self._width  == other._width and self._height == other._height and self._radius == other._radius)
        return NotImplemented

    # ======================================== PREDICATES ========================================
    def contains(self, point: Point) -> bool:
        """Teste si un point est dans le rectangle arrondi

        Args:
            point: point à tester
        """
        px, py = abs(float(point[0])), abs(float(point[1]))
        hw, hh, r = self._width * 0.5, self._height * 0.5, self._radius

        if px > hw or py > hh:
            return False
        if px <= hw - r or py <= hh - r:
            return True
        return (px - (hw - r)) ** 2 + (py - (hh - r)) ** 2 <= r ** 2
    
    def is_convex(self) -> bool:
        """Vérifie la convexité"""
        return True

    # ======================================== PUBLIC METHODS ========================================
    def copy(self) -> RoundedRect:
        """Renvoie une copie du rectangle arrondi"""
        return RoundedRect(self._width, self._height, self._radius)