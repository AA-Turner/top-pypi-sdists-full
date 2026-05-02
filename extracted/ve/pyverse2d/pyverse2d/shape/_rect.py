# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._internal import expect, not_null, positive
from ..abc import Shape
from ..math import Point

from numbers import Real
from typing import Iterator
import numpy as np
from numpy.typing import NDArray

# ======================================== SHAPE ========================================
class Rect(Shape):
    """Forme géométrique 2D immuable : Rectangle

    Args:
        width:  largeur du rectangle
        height: hauteur du rectangle
    """
    __slots__ = ("_width", "_height")

    def __init__(self, width: Real, height: Real):
        self._width:  float = float(positive(not_null(expect(width,  Real))))
        self._height: float = float(positive(not_null(expect(height, Real))))
        super().__init__()

    # ======================================== CONVERSIONS ========================================
    def __repr__(self) -> str:
        """Renvoie une représentation du rectangle"""
        return f"Rect(width={self._width}, height={self._height})"

    def __str__(self) -> str:
        """Renvoie une description lisible du rectangle"""
        return f"Rect[{self._width}x{self._height} | area={self.get_area():.4g} | perimeter={self.get_perimeter():.4g}]"

    def __iter__(self) -> Iterator[float]:
        """Renvoie les composants dans un itérateur"""
        yield self._width
        yield self._height

    def __hash__(self) -> int:
        """Renvoie le hash du rectangle"""
        return hash((self._width, self._height))

    # ======================================== GETTERS ========================================
    @property
    def width(self) -> float:
        """Largeur du rectangle

        La largeur doit être un *réel positif non nul*.
        """
        return self._width

    @property
    def height(self) -> float:
        """Hauteur du rectangle
        
        La hauteur doit être un *réel positif non nul*.
        """
        return self._height

    @property
    def half_width(self) -> float:
        """Demi-largeur du rectangle"""
        return 0.5 * self._width

    @property
    def half_height(self) -> float:
        """Demi-hauteur du rectangle"""
        return 0.5 * self._height

    @property
    def diagonal(self) -> float:
        """Renvoie la longueur de la diagonale"""
        return (self._width ** 2 + self._height ** 2) ** 0.5

    # ======================================== GEOMETRY ========================================
    def get_perimeter(self) -> float:
        """Renvoie le périmètre du rectangle"""
        return 2.0 * (self._width + self._height)

    def get_area(self) -> float:
        """Renvoie l'aire du rectangle"""
        return self._width * self._height

    def get_bounding_box(self) -> tuple[float, float, float, float]:
        """Renvoie  ``(x_min, y_min, x_max, y_max)`` en espace local"""
        hw, hh = 0.5 * self._width, 0.5 * self._height
        return (-hw, -hh, hw, hh)

    def compute_vertices(self) -> NDArray[np.float32]:
        """Renvoie les 4 sommets du rectangle centré à l'origine"""
        hw = 0.5 * self._width
        hh = 0.5 * self._height
        return np.array([
            (-hw, -hh),
            ( hw, -hh),
            ( hw,  hh),
            (-hw,  hh),
        ], dtype=np.float32)

    # ======================================== COMPARATORS ========================================
    def __eq__(self, other: object) -> bool:
        """Vérifie l'égalité de deux rectangles

        Args:
            other(object): objet à comparer
        """
        if isinstance(other, Rect):
            return self._width == other._width and self._height == other._height
        return NotImplemented

    # ======================================== PREDICATES ========================================
    def contains(self, point: Point) -> bool:
        """Teste si un point est dans le rectangle

        Args:
            point: point à tester
        """
        return abs(float(point[0])) <= 0.5 * self._width and abs(float(point[1])) <= 0.5 * self._height
    
    def is_convex(self) -> bool:
        """Vérifie la convexité"""
        return True

    # ======================================== PUBLIC METHODS ========================================
    def copy(self) -> Rect:
        """Renvoie une copie du rectangle"""
        return Rect(self._width, self._height)