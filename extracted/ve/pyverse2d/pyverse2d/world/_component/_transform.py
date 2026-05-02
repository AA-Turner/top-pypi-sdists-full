# ======================================== IMPORTS ========================================
from __future__ import annotations

from ...abc import Component
from ...math import Point
from ..._core import Transform as _Transform

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
    __slots__ = ("_position", "_anchor", "_rotation", "_scale")

    def __init__(
            self,
            position: Point = (0.0, 0.0),
            anchor: Point = (0.5, 0.5),
            rotation: float = 0.0,
            scale: float = 1.0,
        ):
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