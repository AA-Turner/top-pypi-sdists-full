# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..math import Point

from numbers import Real

# ======================================== HANDLE ========================================
class Positionable:
    """Objet portant une position monde
    
    Args:
        position: position monde
    """
    __slots__ = ("_position",)

    def __init__(
        self,
        position: Point = (0.0, 0.0)
    ):
        # Transtypage
        position = Point(position)

        # Attributs publiques
        self._position: Point = position

    # ======================================== PROPERTIES ========================================
    @property
    def position(self) -> Point:
        """Position monde
        
        La position peut être un objet ``Point`` ou n'importe quel tuple ``(x, y)``.
        """
        return self._position
    
    @position.setter
    def position(self, value: Point) -> None:
        self._position.x, self._position.y = value
    
    @property
    def x(self) -> float:
        """Position monde horizontale
        
        La coordonnée doit être un ``Real``.
        """
        return self._position.x
    
    @x.setter
    def x(self, value: Real) -> None:
        self._position.x = value

    @property
    def y(self) -> float:
        """Position monde verticale
        
        La coordonnée doit être un ``Real``.
        """
        return self._position.y
    
    @y.setter
    def y(self, value: Real) -> None:
        self._position.y = value

# ======================================== EXPORTS ========================================
__all__ = [
    "Positionable",
]