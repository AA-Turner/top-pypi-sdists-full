# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import different_from
from ..._core import Transform as _Transform
from ...abc import Component
from ...math import Point

from numbers import Real

# ======================================== COMPONENT ========================================
class Transform(_Transform, Component):
    """Composant gérant le positionnement

    Ce composant est manipulé par ``PhysicsSystem``, ``CollisionSystem`` et ``SteeringSystem``.

    Args:
        position: position
        anchor: ancre de positionnement
        rotation: angle de rotation en degrés
        scale: facteur de redimensionnement
    """
    __slots__ = (
        "_position", "_anchor",
        "_rotation", "_scale",
    )

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

        # Initialisation de la tranformation
        super().__init__(position, anchor, rotation, scale)

    # ======================================== CONTRACT ========================================
    def __repr__(self) -> str:
        """Renvoie une représentation du composant"""
        return f"Transform(position={self._position.to_tuple()}, anchor={self._anchor.to_tuple()}, rotation={self._rotation}, scale={self._scale})"
    
    def get_attributes(self) -> tuple:
        """Renvoie les attributs du composant"""
        return (self._position, self._anchor, self._rotation, self._scale)
    
    def copy(self) -> Transform:
        """Renvoie une copie du composant"""
        return Transform(self._position, self._anchor, self._rotation, self._scale)
    
    # ======================================== PROPERTIES ========================================        
    @_Transform.rotation.setter
    def rotation(self, value: Real) -> None:
        value = float(value)
        _Transform.rotation.fset(self, value)
    
    @_Transform.scale.setter
    def scale(self, value: Real) -> None:
        value = float(value)
        _Transform.scale.fset(self, value)
    
# ======================================== EXPORTS ========================================
__all__ = [
    "Transform",
]