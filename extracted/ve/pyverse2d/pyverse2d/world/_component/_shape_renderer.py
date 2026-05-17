# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import expect, clamped, positive
from ...abc import RendererComponent, Shape
from ...asset import Color
from ...math import Vector
from ...typing import BorderAlign

from numbers import Real, Integral
from typing import ClassVar

# ======================================== COMPONENT ========================================
class ShapeRenderer(RendererComponent):
    """Composant gérant le rendu d'une forme

    Ce composant est manipulé par ``RenderSystem``.

    Args:
        shape: forme du rendu
        offset: décalage par rapport au Transform
        filling: activation du remplissage
        filling_color: couleur de remplissage
        border_width: épaisseur de la bordure
        border_color: couleur de la bordure
        opacity: facteur d'opacité
        z: ordre de rendu
        visible: visibilité
    """
    __slots__ = (
        "_shape", "_offset",
        "_filling", "_filling_color",
        "_border_width", "_border_align", "_border_color",
    )

    _REQUIRES: ClassVar[tuple[str, ...]] = ("Transform",)

    def __init__(
            self,
            shape: Shape,
            offset: Vector = (0.0, 0.0),
            filling: bool = True,
            filling_color: Color = (255, 255, 255, 1.0),
            border_width: Integral = 0,
            border_align: BorderAlign = "center",
            border_color: Color = (0, 0, 0, 1.0),
            opacity: Real = 1.0,
            z: Integral = 0,
            visible: bool = True,
        ):
        # Initialiastion du composant de rendu
        super().__init__(opacity, z, visible)

        # Transtypage et vérifications
        offset = Vector(offset)
        filling = bool(filling)
        filling_color = Color(filling_color)
        border_width = int(border_width)
        border_align = str(border_align)
        border_color = Color(border_color)

        if __debug__:
            expect(shape, Shape)
            positive(border_width)

        # Attributs publiques
        self._shape: Shape = shape
        self._offset: Vector = offset
        self._filling: bool = filling
        self._filling_color: Color = filling_color
        self._border_width: int = border_width
        self._border_align: BorderAlign = border_align
        self._border_color: Color = border_color
    
    # ======================================== CONTRACT ========================================
    def __repr__(self) -> str:
        """Renvoie une représentation du composant"""
        return f"ShapeRenderer(shape={self._shape}, z={self._z}, visible={self._visible})"
    
    def get_attributes(self) -> tuple:
        """Renvoie les attributs du composant"""
        return (self._shape, self._offset, self._filling, self._filling_color, self._border_width, self._border_align, self._border_color, self._opacity, self._z)
    
    def copy(self) -> ShapeRenderer:
        """Renvoie une copie du composant"""
        new = ShapeRenderer(self._shape, self._offset, self._filling, self._filling_color, self._border_width, self._border_align, self._border_color, self._opacity, self._z, self._visible)
        return new
    
    # ======================================== PROPERTIES ========================================
    @property
    def shape(self) -> Shape:
        """Forme du renderer *(lecture seule)*"""
        return self._shape
    
    @property
    def offset(self) -> Vector:
        """Décalage par rapport au Transform"""
        return self._offset
    
    @offset.setter
    def offset(self, value: Vector):
        self._offset.x, self._offset.y = value
    
    @property
    def offset_x(self) -> float:
        """Décalage horizontal"""
        return self._offset.x
    
    @offset_x.setter
    def offset_x(self, value: Real) -> None:
        self._offset.x = value
    
    @property
    def offset_y(self) -> float:
        """Décalage vertical"""
        return self._offset.y
    
    @offset_y.setter
    def offset_y(self, value: Real) -> None:
        self._offset.y = value
    
    @property
    def filling(self) -> bool:
        """Etat du remplissage"""
        return self._filling
    
    @filling.setter
    def filling(self, value: bool):
        value = bool(value)
        self._filling = value
    
    @property
    def filling_color(self) -> Color:
        """Couleur de remplissage"""
        return self._filling_color
    
    @filling_color.setter
    def filling_color(self, value: Color):
        value = Color(value)
        self._filling_color = value
    
    @property
    def border_width(self) -> int:
        """Epaisseur de la bordure"""
        return self._border_width
    
    @border_width.setter
    def border_width(self, value: Integral):
        value = int(value)
        if __debug__:
            positive(value)
        self._border_width = value
    
    @property
    def border_align(self) -> BorderAlign:
        """Alignement de la bordure"""
        return self._border_align
    
    @border_align.setter
    def border_align(self, value: BorderAlign):
        value = str(value)
        if __debug__:
            expect(value, BorderAlign)
        self._border_align = value
    
    @property
    def border_color(self) -> Color:
        """Couleur de la bordure"""
        return self._border_color
    
    @border_color.setter
    def border_color(self, value: Color):
        value = Color(value)
        self._border_color = value

# ======================================== EXPORTS ========================================
__all__ = [
    "ShapeRenderer",
]