# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._internal import different_from
from ..math import Point

from ._transform import Transform

from numbers import Real

# ======================================== HANDLE ========================================
class Transformable:
    """Objet portant une transformation monde"""
    __slots__ = ("_transform",)

    def __init__(
        self,
        position: Point = (0.0, 0.0),
        anchor: Point = (0.5, 0.5),
        rotation: Real = 0.0,
        scale: Real = 1.0,
    ):
        # Transtypage et vérifications
        position = Point(position)
        anchor = Point(anchor)
        rotation = float(rotation)
        scale = float(scale)

        if __debug__:
            different_from(scale, 0.0)

        # Attributs publiques
        self._transform: Transform = Transform(position, anchor, rotation, scale)

    # ======================================== PROPERTIES ========================================
    @property
    def position(self) -> Point:
        """Position monde
        
        La position peut être un objet ``Point`` ou n'importe quel tuple ``(x, y)``.
        """
        return self._transform.position
    
    @position.setter
    def position(self, value: Point) -> None:
        self._transform.position = value
    
    @property
    def x(self) -> float:
        """Position monde horizontale
        
        La coordonnée doit être un ``Real``.
        """
        return self._transform.x
    
    @x.setter
    def x(self, value: Real) -> None:
        self._transform.x = value

    @property
    def y(self) -> float:
        """Position monde verticale
        
        La coordonnée doit être un ``Real``.
        """
        return self._transform.y
    
    @y.setter
    def y(self, value: Real) -> None:
        self._transform.y = value

    @property
    def anchor(self) -> Point:
        """Ancre relative locale

        L'ancre peut être un objet ``Point`` ou n'importe quel tuple ``(ax, ay)``.
        """
        return self._transform.anchor
    
    @anchor.setter
    def anchor(self, value: Point) -> None:
        self._transform.anchor = value
    
    @property
    def anchor_x(self) -> float:
        """Ancre relative locale horizontale

        L'ancre horizontale doit être un ``Real`` normalisé.
        """
        return self._transform.anchor_x
    
    @anchor_x.setter
    def anchor_x(self, value: Real) -> None:
        self._transform.anchor_x = value

    @property
    def anchor_y(self) -> float:
        """Ancre relative locale verticale

        L'ancre verticale doit être un ``Real`` normalisé.
        """
        return self._transform.anchor_y
    
    @anchor_y.setter
    def anchor_y(self, value: Real) -> None:
        self._transform.anchor_y = value

    @property
    def rotation(self) -> float:
        """Angle de rotation

        L'angle est *en degrés* et la rotation se fait dans le sens trigonométrique *(CCW)*
        """
        return self._transform.rotation
    
    @rotation.setter
    def rotation(self, value: Real) -> None:
        value = float(value)
        self._transform.rotation = value

    @property
    def scale(self) -> float:
        """Facteur de redimensionnement

        Le facteur doit être un ``Real`` non nul.
        """
        return self._transform.scale
    
    @scale.setter
    def scale(self, value: Real) -> None:
        value = float(value)
        if __debug__:
            different_from(value, 0.0)
        self._transform.scale = value

    @property
    def version(self) -> int:
        """Version du ``Transform``
        
        Cette propriété est incrémentée à chaque modification de la transformation monde.
        """
        return self._transform.version
    
# ======================================== EXPORTS ========================================
__all__ = [
    "Transformable",
]