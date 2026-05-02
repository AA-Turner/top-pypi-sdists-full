# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._internal import expect
from ..abc import MathObject

from ._vector import Vector
from ._point import Point

from typing import Iterator
from numbers import Real

# ======================================== OBJET ========================================
class Line(MathObject):
    """Objet mathématique 2D abstrait : Droite"""
    __slots__ = ("_origin", "_vector")
    def __init__(
            self,
            point: Point,
            vector: Vector
        ):
        """
        Args:
            point(Point): origine de la droite
            vector(Vector): Vecteur directeur de la droite
        """
        super().__init__()
        self._origin: Point = Point(point)
        self._vector: Vector = Vector(vector)
        
        if not self._vector:
            raise ValueError("Null vector cannot be direction vector")

    # ======================================== CONVERSIONS ========================================
    def __repr__(self) -> str:
        """Renvoie une réprésentation de la droite"""
        return f"Line({self._origin}, {self._vector})"
    
    def __iter__(self) -> Iterator[Point]:
        """Renvoie les points de la droite dans un itérateur"""
        t = -1
        while True:
            t += 1
            yield self._point(float(t))

    def __hash__(self) -> int:
        """Renvoie l'entier hashé de la droite"""
        return hash((self.unique_point, self.unique_vector))
    
    def to_tuple(self) -> tuple[Point, Vector]:
        """Renvoie la droite sous forme de tuple"""
        return (self._origin, self._vector)
    
    def to_list(self) -> list[MathObject]:
        """Renvoie la droite sous forme de liste"""
        return [self._origin, self._vector]
    
    # ======================================== GETTERS ========================================
    def __len__(self) -> int:
        """Renvoie la dimension de la droite"""
        return 2
        
    def __getitem__(self, t: Real) -> Point:
        """Renvoie le point de paramètre t"""
        if isinstance(t, Real):
            return self._point(float(t))
        return NotImplemented
    
    @property
    def origin(self) -> Point:
        """Renvoie l'origine de la droite"""
        return self._origin
    
    @property
    def vector(self) -> Vector:
        """Renvoie un vecteur directeur de la droite"""
        return self._vector
    
    @property
    def unique_point(self) -> Point:
        """Renvoie le point unique de la droite"""
        return self._project(Point(0, 0))
    
    @property
    def unique_vector(self) -> Vector:
        """Renvoie le vecteur directeur unique de la droite"""
        sign = 1
        for component in self._vector:
            if component != 0:
                sign = 1 if component > 0 else -1
                break
        return sign * self._vector.normalized
    
    def get_cartesian_equation(self) -> dict[str, float]:
        """Renvoie l'équation cartésienne de la droite : ax + by + c = 0"""
        a = -self._vector.y
        b = self._vector.x
        c = -(a * self._origin.x + b * self._origin.y)
        return {"a": a, "b": b, "c": c}
    
    # ======================================== SETTERS ========================================
    @origin.setter
    def origin(self, point: Point):
        """Fixe l'origine de la droite"""
        self._origin = Point(point)
    
    @vector.setter
    def vector(self, vector: Vector):
        """Fixe le vecteur directeur de la droite"""
        self._vector = Vector(vector)
        if not self._vector:
            raise ValueError("Null vector cannot be direction vector")

    # ======================================== OPERATIONS ========================================
    def __add__(self, other: Vector) -> Line:
        """Translation par le vecteur"""
        if isinstance(other, Vector):
            return self._translate(other)
        return NotImplemented
    
    def __sub__(self, other:Vector) -> Line:
        """Translation par le vecteur opposé"""
        if isinstance(other, Vector):
            return self._translate(-other)
        return NotImplemented

    # ======================================== COMPARATORS ========================================
    def __eq__(self, other: Line) -> bool:
        """Vérifie la correspondance avec une autre droite"""
        if isinstance(other, Line):
            return self.unique_point == other.unique_point and self.unique_vector == other.unique_vector
        return NotImplemented
    
    def __contains__(self, other: Point) -> bool:
        """Vérifie qu'un point soit compris dans la droite"""
        if isinstance(other, Point):
            return self._contains(other)
        return False
    
    # ======================================== PREDICATES ========================================
    def contains(self, point: Point) -> bool:
        """
        Vérifie qu'un point soit compris dans la droite

        Args:
            point(Point): point à vérifier
        """
        return self._contains(Point(point))
    
    def is_orthogonal(self, line: Line) -> bool:
        """
        Vérifie l'orthogonalité avec une seconde droite

        Args:
            line(Line): droite à vérifier
        """
        return self._is_orthogonal(expect(line, Line))
    
    def is_parallel(self, line: Line) -> bool:
        """
        Vérifie que la droite soit parallèle à une autre droite

        Args:
            line(Line): droite à vérifier
        """
        return self._is_parallel(expect(line, Line))
    
    def is_secant(self, line: Line) -> bool:
        """
        Vérifie que la droite soit sécant à une autre droite
        
        Args:
            line(Line): droite à vérifier
        """
        return self._is_secant(expect(line, Line))
    
    # ======================================== COLLISIONS ========================================
    def collidepoint(self, point: Point) -> bool:
        """
        Vérifie la collision avec un point

        Args:
            point(Point): point à vérifier
        """
        return self._collidepoint(Point(point))
    
    def collideline(self, line: Line) -> bool:
        """
        Vérifie la collision avec une droite

        Args:
            line(Line): droite à vérifier
        """
        return self._collideline(expect(line, Line))
    
    # ======================================== PUBLIC METHODS ========================================
    def copy(self) -> Line:
        """Renvoie une copie de la droite"""
        return Line(self._origin, self._vector)
    
    def translate(self, vector: Vector) -> Line:
        """
        Renvoie l'image de la droite par la translation du vecteur donné

        Args:
            vector(Vector): vecteur de translation
        """
        return self._translate(Vector(vector))
    
    def point(self, t: Real) -> Point:
        """
        Renvoie le point de paramètre t

        Args:
            t(Real): paramètre de la droite
        """
        return self._point(expect(t, Real))
    
    def project(self, point: Point) -> Point:
        """
        Renvoie le projeté orthogonal d'un point sur la droite

        Args:
            point(Point): point à projeter
        """
        return self._project(Point(point))
    
    def distance(self, point: Point) -> float:
        """
        Renvoie la distance d'un point à la droite

        Args:
            point(Point): point à vérifier
        """
        return self._distance(Point(point))
    
    def intersection(self, line: Line) -> None | Point | Line:
        """
        Renvoie le(s) point(s) d'intersection avec une autre droite

        Args:
            line(Line): seconde droite
        """
        return self._intersection(expect(line, Line))
    
    def symmetric(self, point: Point) -> Point:
        """
        Renvoie le symétrique d'un point par rapport à la droite

        Args:
            point(Point): point original
        """
        return self._symmetric(Point(point))

    # ======================================== INTERNAL METHODS ========================================
    def _contains(self, point: Point) -> bool:
        """Point compris dans la droite"""
        return self._vector.is_collinear(point - self._origin)
    
    def _is_orthogonal(self, line: Line) -> bool:
        """Vérifie l'orthogonalité"""
        return self._vector.is_orthogonal(line._vector)
    
    def _is_parallel(self, line: Line) -> bool:
        """Droites parallèles"""
        return self._vector.is_collinear(line._vector)
    
    def _is_secant(self, line: Line) -> bool:
        """Droites sécantes"""
        return not self._is_parallel(line)
    
    def _collidepoint(self, point: Point) -> bool:
        """Collision avec un point"""
        return self._contains(point)
    
    def _collideline(self, line: Line) -> bool:
        """Collision avec une droite"""
        return self._is_secant(line) or self == line
    
    def _translate(self, vector: Vector) -> Line:
        """Translation vectorielle"""
        return Line(self._origin + vector, self._vector)
    
    def _point(self, t: Real) -> Point:
        """Point de paramètre t"""
        return self._origin + float(t) * self._vector
    
    def _project(self, point: Point) -> Point:
        """Projection d'un point sur la droite"""
        return self._origin + ((point - self._origin)._dot(self._vector) / self._vector._dot(self._vector)) * self._vector

    def _distance(self, point: Point) -> float:
        """Distance d'un point à la droite"""
        return (point - self._project(point)).norm
    
    def _intersection(self, line: Line) -> None | Point | Line:
        """Intersection(s) avec une autre droite"""
        if self == line:
            return self.copy()
        det = self._vector._cross(line._vector)
        if det == 0:
            return None
        return self._origin + ((line._origin - self._origin)._cross(line._vector) / det) * self._vector
    
    def _symmetric(self, point: Point) -> Point:
        """Symétrique d'un point par rapport à la droite"""
        H = self._project(point)
        return H + (H - point)