# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._internal import expect
from ..abc import MathObject

from ._vector import Vector

from numbers import Real
from typing import Iterator
from math import sqrt

# ======================================== OBJECT ========================================
class Point(MathObject):
    """Objet mathématique 2D abstrait : Point

    Args:
        x: coordonnée horizontale, ou Point/tuple à coercer
        y: coordonnée verticale
    """
    __slots__ = ("_x", "_y")
    PRECISION = 8

    def __init__(self, x, y=None):
        if y is None:
            try:
                x, y = x
            except (TypeError, ValueError):
                raise TypeError("Expected Point or iterable of length 2")
        self._x: float = round(float(x), self.PRECISION)
        self._y: float = round(float(y), self.PRECISION)

    # ======================================== FACTORY INTERNE ========================================
    @classmethod
    def _make(cls, x: float, y: float) -> Point:
        """Création rapide sans validation (usage interne uniquement)"""
        obj = object.__new__(cls)
        obj._x = x
        obj._y = y
        return obj

    # ======================================== CONVERSIONS ========================================
    def __repr__(self) -> str:
        """Renvoie une représentation du point"""
        return f"Point({self._x}, {self._y})"

    def __iter__(self) -> Iterator[float]:
        """Renvoie les coordonnées dans un itérateur"""
        yield self._x
        yield self._y

    def __hash__(self) -> int:
        """Renvoie l'entier hashé du point"""
        return hash((self._x, self._y))

    def to_tuple(self) -> tuple[float]:
        """Renvoie le point sous forme de tuple"""
        return (self._x, self._y)

    def to_list(self) -> list[float]:
        """Renvoie le point sous forme de liste"""
        return [self._x, self._y]

    def to_vector(self) -> Vector:
        """Renvoie le vecteur origin -> self"""
        return Vector._make(self._x, self._y)

    # ======================================== GETTERS ========================================
    def __getitem__(self, i: int) -> float:
        """Renvoie une coordonnée du point"""
        return (self._x, self._y)[i]

    @property
    def x(self) -> float:
        """Renvoie la coordonnée horizontale du point"""
        return self._x

    @property
    def y(self) -> float:
        """Renvoie la coordonnée verticale du point"""
        return self._y

    def __len__(self) -> int:
        """Renvoie la dimension du point"""
        return 2

    # ======================================== SETTERS ========================================
    def __setitem__(self, i: int, value: Real):
        """Fixe une coordonnée du point"""
        setattr(self, ("x", "y")[i], round(float(value), self.PRECISION))

    @x.setter
    def x(self, value: Real):
        """Fixe la coordonnée horizontale du point"""
        self._x = round(float(value), self.PRECISION)

    @y.setter
    def y(self, value: Real):
        """Fixe la coordonnée verticale du point"""
        self._y = round(float(value), self.PRECISION)

    # ======================================== OPERATIONS ========================================
    def __add__(self, other: Vector | Point) -> Point:
        """Renvoie l'image du point par le vecteur donné"""
        if isinstance(other, (Vector, Point)):
            return Point._make(self._x + other._x, self._y + other._y)
        return NotImplemented

    def __radd__(self, other: Vector) -> Point:
        """Renvoie l'image du point par le vecteur donné"""
        if isinstance(other, Vector):
            return Point._make(self._x + other._x, self._y + other._y)
        return NotImplemented

    def __sub__(self, other: Point | Vector) -> Point | Vector:
        """Renvoie l'image du point par l'opposé du vecteur ou le vecteur other -> self"""
        if isinstance(other, Point):
            return Vector._make(self._x - other._x, self._y - other._y)
        if isinstance(other, Vector):
            return Point._make(self._x - other._x, self._y - other._y)
        return NotImplemented

    def __pos__(self) -> Point:
        """Renvoie une copie du point"""
        return Point._make(self._x, self._y)

    def __neg__(self) -> Point:
        """Renvoie l'opposé du point par rapport à l'origine"""
        return Point._make(-self._x, -self._y)

    def __abs__(self) -> Point:
        """Renvoie le point côté positif"""
        return Point._make(abs(self._x), abs(self._y))

    # ======================================== COMPARATORS ========================================
    def __eq__(self, other: Point) -> bool:
        """Vérifie la correspondance de deux points"""
        if isinstance(other, Point):
            return self._x == other._x and self._y == other._y
        return NotImplemented

    def __ne__(self, other: Point) -> bool:
        """Vérifie la non correspondance de deux points"""
        if isinstance(other, Point):
            return self._x != other._x or self._y != other._y
        return NotImplemented

    # ======================================== PREDICATES ========================================
    def is_origin(self) -> bool:
        """Vérifie que le point soit l'origine du repère"""
        return self._x == 0 and self._y == 0

    def is_aligned(self, *points: Point) -> bool:
        """
        Vérifie l'alignement avec un ensemble de points

        Args:
            points(Point): points à vérifier
        """
        if len(points) < 1:
            return True
        v0 = Vector._make(points[0]._x - self._x, points[0]._y - self._y)
        if v0.is_null():
            return all(
                Vector._make(p._x - points[0]._x, p._y - points[0]._y).is_null()
                for p in points[1:]
            )
        return all(
            v0._x * (p._y - points[0]._y) - v0._y * (p._x - points[0]._x) == 0
            for p in points[1:]
        )

    # ======================================== PUBLIC METHODS ========================================
    def copy(self) -> Point:
        """Renvoie une copie du point"""
        return Point._make(self._x, self._y)
    
    def homogeneous(self) -> tuple[float, float, float, float]:
        """Renvoie le vecteur homogène 4D"""
        return (self._x, self._y, 0, 1)

    def vector_to(self, point: Point) -> Vector:
        """
        Renvoie le vecteur self -> point

        Args:
            point(Point): point cible
        """
        x, y = point
        self._vector_to(x, y)

    def distance_to(self, point: Point) -> float:
        """
        Renvoie la distance euclidienne jusqu'à un autre point

        Args:
            point(Point): point cible
        """
        x, y = point
        return self._distance_to(x, y)

    def translate(self, vector: Vector) -> Point:
        """
        Renvoie la translation du point par un vecteur donné

        Args:
            vector(Vector): vecteur de translation
        """
        x, y = vector
        return self._translate(x, y)

    def midpoint(self, point: Point) -> Point:
        """
        Renvoie le point du milieu du segment à un autre point

        Args:
            point(Point): second point du segment
        """
        x, y = point
        return self._midpoint(x, y)

    def barycenter(self, *points: Point) -> Point:
        """
        Renvoie le barycentre à plusieurs autres points

        Args:
            points(Point): autres points
        """
        xs, ys = zip(*points)
        n = len(xs) + 1
        return Point._make(
            (self._x + sum(x for x in xs)) / n,
            (self._y + sum(y for y in ys)) / n,
        )

    # ======================================== INTERNAL METHODS ========================================
    def _vector_to(self, x: float, y: float) -> Vector:
        """Vecteur à un autre point"""
        return Vector._make(x - self._x, y - self._y)

    def _distance_to(self, x: float, y: float) -> float:
        """Distance à un autre point"""
        dx = x - self._x
        dy = y - self._y
        return sqrt(dx * dx + dy * dy)

    def _translate(self, x: float, y: float) -> Point:
        """Translation par un vecteur"""
        return Point._make(self._x + x, self._y + y)

    def _midpoint(self, x: float, y: float) -> Point:
        """Point du milieu à un autre point"""
        return Point._make((self._x + x) * 0.5, (self._y + y) * 0.5)