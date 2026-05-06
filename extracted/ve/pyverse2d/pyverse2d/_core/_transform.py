from __future__ import annotations

from .._internal import different_from
from ..math import Point, Vector

from numbers import Real

class Transform:
    """Objet possédant un positionnement monde
    
    Args:
        position: position
        anchor: ancre relative locale
        scale: facteur de redimensionnement
        rotation: angle de rotation *(en degrés)*
    """
    __slots__ = (
        "_position", "_anchor",
        "_scale", "_rotation",
        "_version",
    )

    def __init__(self, position: Point = (0.0, 0.0), anchor: Point = (0.5, 0.5), rotation: Real = 0.0, scale: Real = 1.0):
        # Transtypage et vérifications
        position = Point(position)
        anchor = Point(anchor)
        rotation = float(rotation)
        scale = float(scale)

        if __debug__:
            different_from(scale, 0.0)

        # Attributs publiques
        self._position: Point = position
        self._anchor: Point = anchor
        self._scale: float = scale
        self._rotation: float = rotation

        # Attributs internes
        self._version: int = 0

    # ======================================== PROPERTIES ========================================
    @property
    def position(self) -> Point:
        """Position

        La position peut être un objet ``Point`` ou un tuple ``(x, y)``.
        """
        return self._position
    
    @position.setter
    def position(self, value: Point) -> None:
        self._position.x, self._position.y = value
        self._version += 1

    @property
    def x(self) -> float:
        """Position horizontale
        
        La coordonnée doit être un ``Réel``.
        """
        return self._position.x
    
    @x.setter
    def x(self, value: Real) -> None:
        self._position.x = value
        self._version += 1
    
    @property
    def y(self) -> float:
        """Position verticale

        La coordonnée doit être un ``Réel``.
        """
        return self._position.y
    
    @y.setter
    def y(self, value: Real) -> None:
        self._position.y = value
        self._version += 1
    
    @property
    def anchor(self) -> Point:
        """Ancre locale normalisée
        
        L'ancre peut être un objet ``Point`` ou un tuple ``(ax, ay)``.
        Les coordonnées de l'ancre sont normalisées *([0, 1])*.
        """
        return self._anchor
    
    @anchor.setter
    def anchor(self, value: Point) -> None:
        self._anchor.x, self._anchor.y = value
        self._version += 1
    
    @property
    def anchor_x(self) -> float:
        """Ancre locale horizontale normalisée
        
        La coordonnée doit être un ``Réel`` normalisé *([0, 1])*.
        """
        return self._anchor.x
    
    @anchor_x.setter
    def anchor_x(self, value: Real) -> None:
        self._anchor.x = value
        self._version += 1
    
    @property
    def anchor_y(self) -> float:
        """Ancre locale verticale normalisée
        
        La coordonnée doit être un ``Réel`` normalisé *([0, 1])*.
        """
        return self._anchor.y
    
    @anchor_y.setter
    def anchor_y(self, value: Real) -> None:
        self._anchor.y = value
        self._version += 1
    
    @property
    def rotation(self) -> float:
        """Angle de rotation
        
        La rotation doit être un ``Réel``.
        L'angle est *en degrés*.
        La rotation se fait dans le sens trigonométrique *(CCW)*.
        """
        return self._rotation
    
    @rotation.setter
    def rotation(self, value: Real) -> None:
        self._rotation = float(value)
        self._version += 1
    
    @property
    def scale(self) -> float:
        """Facteur de redimensionnement
        
        Le facteur doit être un ``Réel`` positif non nul.
        """
        return self._scale
    
    @scale.setter
    def scale(self, value: Real) -> None:
        value = float(value)
        if __debug__:
            different_from(value, 0.0)
        self._scale = value
        self._version += 1

    @property
    def version(self) -> int:
        """Version du transform *(lecture seule)*"""
        return self._version

    # ======================================== INTERFACE ========================================
    def copy(self) -> Transform:
        """Renvoie une copie du composant"""
        return Transform(self._position, self._anchor, self._rotation, self._scale)
    
    def translate(self, vector: Vector) -> None:
        """Applique une translation

        Args:
            vector: vecteur de translation
        """
        tx, ty = vector
        self._position.x += tx
        self._position.y += ty
        self._version += 1

    def rotate(self, angle: Real) -> None:
        """Applique une rotation dans le sens trigonométrique *(CCW)*
        
        Args:
            angle: angle de rotation *en degrés*
        """
        self._rotation += float(angle)
        self._version += 1

    def resize(self, factor: Real) -> None:
        """Applique un redimensionnement
        
        Args:
            factor: facteur de redimensionnement
        """
        factor = float(factor)
        if __debug__:
            different_from(factor, 0.0)
        self._scale *= factor
        self._version += 1