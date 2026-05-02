# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._internal import expect
from ..abc import MathObject

from numbers import Real
from typing import Iterator
from math import acos, sqrt

# ======================================== OBJET ========================================
class Vector(MathObject):
    """Objet mathématique 2D abstrait : Vecteur

    Args:
        x(Real): composante x, ou Vector/tuple à coercer
        y(Real): composante y (optionnel si x est un Vector ou tuple)
    """
    __slots__ = ("_x", "_y")
    PRECISION = 9

    def __init__(self, x, y=None):
        if y is None:
            try:
                x, y = x
            except (TypeError, ValueError):
                raise TypeError("Expected Vector or iterable of length 2")
        self._x: float = round(float(x), self.PRECISION)
        self._y: float = round(float(y), self.PRECISION)

    # ======================================== FACTORY INTERNE ========================================
    @classmethod
    def _make(cls, x: float, y: float) -> Vector:
        """Création rapide sans validation (usage interne uniquement)"""
        obj = object.__new__(cls)
        obj._x = x
        obj._y = y
        return obj

    # ======================================== CONVERSIONS ========================================
    def __repr__(self) -> str:
        """Renvoie une représentation du vecteur"""
        return f"Vector({self._x}, {self._y})"

    def __iter__(self) -> Iterator[float]:
        """Renvoie les composantes dans un itérateur"""
        yield self._x
        yield self._y

    def __hash__(self) -> int:
        """Renvoie l'entier hashé du vecteur"""
        return hash((self._x, self._y))

    def to_tuple(self) -> tuple[float]:
        """Renvoie le vecteur sous forme de tuple"""
        return (self._x, self._y)

    def to_list(self) -> list[float]:
        """Renvoie le vecteur sous forme de liste"""
        return [self._x, self._y]

    # ======================================== GETTERS ========================================
    def __getitem__(self, i: int) -> float:
        """Renvoie une composante du vecteur"""
        return (self._x, self._y)[i]

    @property
    def x(self) -> float:
        """Renvoie la composante horizontale du vecteur"""
        return self._x

    @property
    def y(self) -> float:
        """Renvoie la composante verticale du vecteur"""
        return self._y

    def __len__(self) -> int:
        """Renvoie la dimension du vecteur"""
        return 2

    @property
    def norm(self) -> float:
        """Renvoie la norme du vecteur"""
        return sqrt(self._x * self._x + self._y * self._y)

    def __abs__(self) -> float:
        """Renvoie la norme du vecteur"""
        return sqrt(self._x * self._x + self._y * self._y)

    @property
    def normalized(self) -> Vector:
        """Renvoie le vecteur normalisé"""
        n = sqrt(self._x * self._x + self._y * self._y)
        if n == 0:
            raise ZeroDivisionError("Cannot normalize null vector")
        inv = 1.0 / n
        return Vector._make(self._x * inv, self._y * inv)

    # ======================================== SETTERS ========================================
    def __setitem__(self, i: int, value: Real):
        """Fixe une composante du vecteur"""
        setattr(self, ("x", "y")[i], round(float(value), self.PRECISION))

    @x.setter
    def x(self, value: Real):
        """Fixe la composante x du vecteur"""
        self._x = round(float(value), self.PRECISION)

    @y.setter
    def y(self, value: Real):
        """Fixe la composante y du vecteur"""
        self._y = round(float(value), self.PRECISION)

    @norm.setter
    def norm(self, value: Real):
        """Fixe la norme du vecteur"""
        n = sqrt(self._x * self._x + self._y * self._y)
        if n == 0:
            raise ZeroDivisionError("Cannot scale null vector")
        scale = float(value) / n
        self._x = round(self._x * scale, self.PRECISION)
        self._y = round(self._y * scale, self.PRECISION)

    # ======================================== OPERATIONS ========================================
    def __add__(self, other: Vector) -> Vector:
        """Somme de vecteurs"""
        if isinstance(other, Vector):
            return Vector._make(self._x + other._x, self._y + other._y)
        return NotImplemented

    def __sub__(self, other: Vector) -> Vector:
        """Différence de vecteurs"""
        if isinstance(other, Vector):
            return Vector._make(self._x - other._x, self._y - other._y)
        return NotImplemented

    def __mul__(self, other: Real) -> Vector:
        """Multiplication par un scalaire"""
        if isinstance(other, Real):
            return Vector._make(self._x * float(other), self._y * float(other))
        return NotImplemented

    def __rmul__(self, other: Real) -> Vector:
        """Multiplication par un scalaire (inversée)"""
        if isinstance(other, Real):
            return Vector._make(self._x * float(other), self._y * float(other))
        return NotImplemented

    def __truediv__(self, other: Real) -> Vector:
        """Division par un scalaire"""
        if isinstance(other, Real):
            if other == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            inv = 1.0 / float(other)
            return Vector._make(self._x * inv, self._y * inv)
        if isinstance(other, Vector):
            return other.__rtruediv__(self)
        return NotImplemented

    def __rtruediv__(self, other: Vector) -> float:
        """Rapport scalaire entre deux vecteurs colinéaires"""
        if isinstance(other, Vector):
            if self._x == 0 and self._y == 0:
                raise ZeroDivisionError("Cannot divide by null vector")
            if not self._is_collinear(other):
                raise RuntimeError("Cannot divide by a non-collinear vector")
            if self._x != 0:
                return other._x / self._x
            return other._y / self._y
        return NotImplemented

    def __matmul__(self, other: Vector) -> float:
        """Produit scalaire"""
        if isinstance(other, Vector):
            return self._x * other._x + self._y * other._y
        return NotImplemented

    def __xor__(self, other: Vector) -> float:
        """Produit vectoriel"""
        if isinstance(other, Vector):
            return self._x * other._y - self._y * other._x
        return NotImplemented

    def __pos__(self) -> Vector:
        """Renvoie une copie du vecteur"""
        return Vector._make(self._x, self._y)

    def __neg__(self) -> Vector:
        """Renvoie le vecteur opposé"""
        return Vector._make(-self._x, -self._y)

    # ======================================== COMPARATORS ========================================
    def __eq__(self, other: Vector) -> bool:
        """Vérifie la correspondance de deux vecteurs"""
        if isinstance(other, Vector):
            return self._x == other._x and self._y == other._y
        return False

    # ======================================== PREDICATES ========================================
    def is_null(self) -> bool:
        """Vérifie que le vecteur soit nul"""
        return self._x == 0 and self._y == 0

    def __bool__(self) -> bool:
        """Vérifie que le vecteur ne soit pas nul"""
        return self._x != 0 or self._y != 0

    def is_orthogonal(self, vector: Vector) -> bool:
        """
        Vérifie l'orthogonalité avec un autre vecteur

        Args:
            vector(Vector): vecteur à tester
        """
        x, y = vector
        return self._is_orthogonal(x, y)

    def is_collinear(self, vector: Vector) -> bool:
        """
        Vérifie la colinéarité avec un autre vecteur

        Args:
            vector(Vector): vecteur à tester
        """
        x, y = vector
        return self._is_collinear(x, y)

    # ======================================== PUBLIC METHODS ========================================
    def copy(self) -> Vector:
        """Renvoie une copie"""
        return Vector._make(self._x, self._y)
    
    def homogeneous(self) -> tuple[float, float, float, float]:
        """Renvoie le vecteur homogène 4D"""
        return (self._x, self._y, 0, 0)

    def normalize(self):
        """Normalise le vecteur en place"""
        n = sqrt(self._x * self._x + self._y * self._y)
        if n == 0:
            raise ZeroDivisionError("Cannot normalize null vector")
        inv = 1.0 / n
        self._x = round(self._x * inv, self.PRECISION)
        self._y = round(self._y * inv, self.PRECISION)

    def dot(self, vector: Vector) -> float:
        """
        Renvoie le produit scalaire avec un autre vecteur

        Args:
            vector(Vector): second vecteur
        """
        x, y = vector
        return self._dot(x, y)

    def cross(self, vector: Vector) -> float:
        """
        Renvoie le produit vectoriel avec un autre vecteur

        Args:
            vector(Vector): second vecteur
        """
        x, y = vector
        return self._cross(x, y)

    def angle_with(self, vector: Vector) -> float:
        """
        Renvoie l'angle avec un autre vecteur en radians

        Args:
            vector(Vector): second vecteur
        """
        x, y = vector
        return self._angle_with(x, y)

    def projection(self, vector: Vector) -> Vector:
        """
        Renvoie le projeté vectoriel sur le vecteur donné

        Args:
            vector(Vector): vecteur de projection
        """
        x, y = vector
        return self._projection(x, y)

    def distance(self, vector: Vector) -> float:
        """
        Renvoie la distance euclidienne à un autre vecteur

        Args:
            vector(Vector): vecteur cible
        """
        x, y = vector
        return self._distance(x, y)

    # ======================================== INTERNAL METHODS ========================================
    def _is_collinear(self, x: float, y: float) -> bool:
        """Vérifie la colinéarité"""
        return self._x * y - self._y * x == 0

    def _is_orthogonal(self, x: float, y: float) -> bool:
        """Vérifie l'orthogonalité"""
        return self._x * x + self._y * y == 0

    def _dot(self, x: float, y: float) -> float:
        """Produit scalaire"""
        return self._x * x + self._y * y

    def _cross(self, x: float, y: float) -> float:
        """Produit vectoriel"""
        return self._x * y - self._y * x

    def _angle_with(self, x: float, y: float) -> float:
        """Distance angulaire"""
        n1 = sqrt(self._x * self._x + self._y * self._y)
        n2 = sqrt(x * x + y * y)
        return acos(max(-1.0, min(1.0, (self._x * x + self._y * y) / (n1 * n2))))

    def _projection(self, x: float, y: float) -> Vector:
        """Projeté vectoriel"""
        denom = x * x + y * y
        t = (self._x * x + self._y * y) / denom
        return Vector._make(x * t, y * t)

    def _distance(self, x: float, y: float) -> float:
        """Distance euclidienne"""
        dx = self._x - x
        dy = self._y - y
        return sqrt(dx * dx + dy * dy)