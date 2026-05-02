# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import expect, clamped
from ...abc import Component
from ...asset import Image, Color
from ...math import Vector

from numbers import Real

# ======================================== COMPONENT ========================================
class SpriteRenderer(Component):
    """Composant gérant le rendu d'une image

    Ce composant est manipulé par ``RenderSystem``.

    Args:
        image(Image): image de rendu
        offset(Vector, optional): décalage par rapport au Transform
        tint(Color, optional): couleur de teinte
        opacity(float, optional): facteur d'opacité de l'image
        flip_x(bool, optional): mirroir horizontal
        flip_y(bool, optional): mirroir vertical
        z(int, optional): ordre de rendu
        visible(bool, optional): visibilité
    """
    __slots__ = ("_default_image", "_image", "_offset", "_tint", "_opacity", "_flip_x", "_flip_y", "_z", "_visible")
    requires = ("Transform",)

    def __init__(
            self,
            image: Image,
            offset: Vector = (0.0, 0.0),
            tint: Color = (255, 255, 255),
            opacity: Real = 1.0,
            flip_x: bool = False,
            flip_y: bool = False,
            z: int = 0,
            visible: bool = True,
        ):
        self._default_image: Image = expect(image, Image)
        self._image: Image = None
        self._offset: Vector = Vector(offset)
        self._tint: Color = Color(tint)
        self._opacity: float = clamped(expect(opacity, Real))
        self._flip_x: bool = expect(flip_x, bool)
        self._flip_y: bool = expect(flip_y, bool)
        self._z: int = expect(z, int)
        self._visible: bool = expect(visible, bool)
    
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
        return self._image if self._image else self._default_image
    
    @property
    def offset(self) -> Vector:
        """Renvoie le décalage par rapport au Transform"""
        return self._offset
    
    @property
    def tint(self) -> Color:
        """Renvoie la couleur de teinte"""
        return self._tint
    
    @property
    def opacity(self) -> float:
        """Renvoie le facteur d'opacité"""
        return self._opacity
    
    @property
    def flip_x(self) -> bool:
        """Vérifie le mirroir horizontal"""
        return self._flip_x
    
    @property
    def flip_y(self) -> bool:
        """Vérifie le mirroir vertical"""
        return self._flip_y
    
    @property
    def z(self) -> int:
        """Renvoie l'ordre de rendu"""
        return self._z
    
    # ======================================== SETTERS ========================================
    @image.setter
    def image(self, image: Image):
        """Fixe l'image du sprite"""
        self._image = expect(image, Image)

    @offset.setter
    def offset(self, value: Vector):
        """Fixe le décalage par rapport au Transform"""
        self._offset = Vector(value)

    @tint.setter
    def tint(self, value: Color):
        """Fixe la couleur de teinte"""
        self._tint = Color(value)

    @opacity.setter
    def opacity(self, value: Real):
        """Fixe le facteur d'opacité"""
        self._opacity = float(clamped(expect(value, Real)))

    @flip_x.setter
    def flip_x(self, value: bool):
        """Fixe le mirroir horizontal"""
        self._flip_x = expect(value, bool)

    @flip_y.setter
    def flip_y(self, value: bool):
        """Fixe le mirroir vertical"""
        self._flip_y = expect(value, bool)

    @z.setter
    def z(self, value: int):
        """Fixe l'ordre de rendu"""
        self._z = expect(value, int)
    
    # ======================================== PREDICATES ========================================
    def is_visible(self) -> bool:
        """Vérifie la visibilité"""
        return self._visible

    # ======================================== PUBLIC METHODS ========================================
    def set_to_default(self) -> None:
        """Utilise l'image par défaut"""
        self._image = None

    def flip(self, horizontal: bool = False, vertical: bool = False) -> None:
        """
        Applique un effet mirroir

        Args:
            horizontal(bool, optional): mirroir horizontal
            vertical(bool, optional): mirroir vertical
        """
        self._flip_x ^= horizontal
        self._flip_y ^= vertical
    
    def show(self) -> None:
        """Montre le sprite"""
        self._visible = True

    def hide(self) -> None:
        """Cache le sprite"""
        self._visible = False