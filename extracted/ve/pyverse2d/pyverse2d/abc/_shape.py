from __future__ import annotations

from ..math import Point
from ..math.vertices import triangulate_ear_clipping, triangulate_triangle_fan

import numpy as np
from numpy.typing import NDArray

from abc import ABC, abstractmethod
from typing import Any, Self, ClassVar

# ======================================== ABSTRACT CLASS ========================================
class Shape(ABC):
    """Classe abstraite de base pour toutes les formes géométriques"""
    __slots__ = ("_vertices", "_indexes")

    _ID: ClassVar[str] = "shape"
    _IS_PRIMITIVE: ClassVar[bool] = False

    def __init__(self) -> None:
        # Attributs internes
        self._vertices: NDArray[np.float32] | None = None
        self._indexes: NDArray[np.float32] | None = None

    # ======================================== CONTRACT ========================================
    @abstractmethod
    def __repr__(self) -> str: ...

    @abstractmethod
    def __str__(self) -> str: ...

    @abstractmethod
    def __hash__(self) -> int: ...

    @abstractmethod
    def __eq__(self, other: Any) -> bool: ...

    @abstractmethod
    def get_perimeter(self) -> float: ...

    @abstractmethod
    def get_area(self) -> float: ...

    @abstractmethod
    def get_bounding_box(self) -> tuple[float, float, float, float]: ...

    @abstractmethod
    def compute_vertices(self) -> NDArray[np.float32]: ...

    @abstractmethod
    def contains(self, point: Point) -> bool: ...

    @abstractmethod
    def is_convex(self) -> bool: ...

    @abstractmethod
    def copy(self) -> Self: ...

    # ======================================== PREDICATES ========================================
    def is_primitive(self) -> bool:
        """Vérifie que la forme soit une ``PrimitiveShape``"""
        return self._IS_PRIMITIVE
    
    # ======================================== INTERFACE ========================================
    def id(self) -> str:
        """Renvoie l'identifiant de la forme"""
        return self._ID

    # ======================================== GPU SIDE ========================================
    def get_vertices(self) -> NDArray[np.float32]:
        """Renvoie les vertices locaux de la forme"""
        if self._vertices is None:
            self._vertices = self.compute_vertices()
        return self._vertices
    
    def get_indexes(self) -> NDArray[np.int32]:
        """Renvoie les indices des triangles de la forme"""
        if self._indexes is None:
            self._indexes = triangulate_triangle_fan(self.get_vertices()) if self.is_convex() else triangulate_ear_clipping(self.get_vertices())
        return self._indexes

    # ======================================== CACHE ========================================
    def _invalidate_geometry(self) -> None:
        """Invalide la géométrie locale et tous les caches dépendants"""
        self._vertices = None

# ======================================== EXPORTS ========================================
__all__ = [
    "Shape",
]