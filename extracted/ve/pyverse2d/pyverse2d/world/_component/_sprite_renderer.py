# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import expect
from ...abc import RendererComponent
from ...asset import Image, Color
from ...math import Vector

from numbers import Real, Integral
from typing import ClassVar

# ======================================== COMPONENT ========================================
class SpriteRenderer(RendererComponent):
    """Composant gérant le rendu d'une image

    Ce composant est manipulé par ``RenderSystem``.

    Args:
        image: image de rendu
        offset: décalage par rapport au Transform
        tint: couleur de teinte
        flip_x: mirroir horizontal
        flip_y: mirroir vertical
        opacity: facteur d'opacité de l'image
        z: ordre de rendu
        visible: visibilité
    """
    __slots__ = (
        "_default_image", "_image", "_offset",
        "_tint", "_flip_x", "_flip_y",
    )

    _REQUIRES: ClassVar[tuple[str, ...]] = ("Transform",)

    def __init__(
            self,
            image: Image,
            offset: Vector = (0.0, 0.0),
            tint: Color = (255, 255, 255),
            flip_x: bool = False,
            flip_y: bool = False,
            opacity: Real = 1.0,
            z: Integral = 0,
            visible: bool = True,
        ):
        # Initialisation du composant de rendu
        super().__init__(opacity, z, visible)

        # Transtypage et vérifications
        offset = Vector(offset)
        tint = Color(tint)
        flip_x = bool(flip_x)
        flip_y = bool(flip_y)

        if __debug__:
            expect(image, Image)

        # Attributs publiques
        self._default_image: Image = image
        self._image: Image = None
        self._offset: Vector = offset
        self._tint: Color = tint
        self._flip_x: bool = flip_x
        self._flip_y: bool = flip_y
    
    # ======================================== CONTRACT ========================================
    def __repr__(self) -> str:
        """Renvoie une représentation du composant"""
        return f"SpriteRenderer(image={self._image}, z={self._z}, visible={self._visible})"
    
    def get_attributes(self) -> tuple:
        """Renvoie les attributs du composant"""
        return (self._image, self._offset, self._tint, self._opacity, self._flip_x, self._flip_y, self._z)
    
    def copy(self) -> SpriteRenderer:
        """Renvoie une copie du composant"""
        new = SpriteRenderer(self._default_image, self._offset, self._tint, self._opacity, self._flip_x, self._flip_y, self._z, self._visible)
        new._image = self._image
        return new
    
    # ======================================== GETTERS ========================================
    @property
    def image(self) -> Image:
        """Renvoie l'image du sprite"""
        return self._image if self._image is not None else self._default_image
    
    @image.setter
    def image(self, value: Image):
        """Fixe l'image du sprite"""
        if __debug__:
            expect(value, Image)
        self._default_image = value
    
    @property
    def offset(self) -> Vector:
        """Décalage par rapport au Transform"""
        return self._offset
    
    @offset.setter
    def offset(self, value: Vector):
        self._offset.x, self._offset.y = value
    
    @property
    def tint(self) -> Color:
        """Couleur de teinte"""
        return self._tint
    
    @tint.setter
    def tint(self, value: Color):
        """Fixe la couleur de teinte"""
        value = Color(value)
        self._tint = value
    
    @property
    def flip_x(self) -> bool:
        """Mirroir horizontal"""
        return self._flip_x
    
    @flip_x.setter
    def flip_x(self, value: bool):
        value = bool(value)
        self._flip_x = value
    
    @property
    def flip_y(self) -> bool:
        """Mirroir vertical"""
        return self._flip_y
    
    @flip_y.setter
    def flip_y(self, value: bool):
        """Fixe le mirroir vertical"""
        value = bool(value)
        self._flip_y = value

    # ======================================== INTERFACE ========================================
    def set_temporary(self, image: Image) -> None:
        """Fixe une image temporaire
        
        Args:
            image: ``Image`` asset temporaire
        """
        if __debug__:
            expect(image, Image)
        self._image = image

    def back_to_default(self) -> None:
        """Utilise l'image par défaut"""
        self._image = None

    def flip(self, horizontal: bool = False, vertical: bool = False) -> None:
        """Applique un effet mirroir

        Args:
            horizontal: mirroir horizontal
            vertical: mirroir vertical
        """
        self._flip_x ^= horizontal
        self._flip_y ^= vertical

# ======================================== EXPORTS ========================================
__all__ = [
    "SpriteRenderer",
]