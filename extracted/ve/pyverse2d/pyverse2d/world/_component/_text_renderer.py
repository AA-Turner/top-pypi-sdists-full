# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import expect, over
from ...abc import RendererComponent
from ...asset import Text, Color
from ...math import Vector
from ...typing import HorizontalAlign

from numbers import Real, Integral
from typing import ClassVar

# ======================================== COMPONENT ========================================
class TextRenderer(RendererComponent):
    """Composant gérant le rendu d'un texte

    Ce composant est manipulé par ``RenderSystem``.

    Args:
        text: descripteur de texte
        offset: décalage par rapport au Transform
        color: couleur RGBA
        weight: épaisseur
        italic: italique
        multiline: active le retour à la ligne automatique
        align: alignement du texte multiline *("left"|"center"|"right")*
        width: largeur max *(requis pour multiline)*
        opacity: facteur d'opacité *[0, 1]*
        z: ordre de rendu
        visible: visibilité
    """
    __slots__ = (
        "_text", "_offset",
        "_color", "_weight", "_italic",
        "_multiline", "_align", "_width",
    )
    
    _REQUIRES: ClassVar[tuple[str, ...]] = ("Transform",)

    def __init__(
        self,
        text: Text,
        offset: Vector = (0.0, 0.0),
        color: Color = (255, 255, 255, 1.0),
        weight: str = "regular",
        italic: bool = False,
        multiline: bool = False,
        align: HorizontalAlign = "left",
        width: Integral | None = None,
        opacity: Real = 1.0,
        z: Integral = 0,
        visible: bool = True,
    ):
        # Initialisation du composant de rendu
        super().__init__(opacity, z, visible)

        # Transtypage et vérifications
        offset = Vector(offset)
        color = Color(color)
        weight = str(weight)
        italic = bool(italic)
        multiline = bool(multiline)
        align = str(align)
        width = int(width) if width is not None else None

        if __debug__:
            expect(text, Text)
            expect(align, HorizontalAlign)
            if width is not None: over(width, 0, include=False)

        # Attributs publiques
        self._text: Text = text
        self._offset: Vector = offset
        self._color: Color = color
        self._weight: bool = weight
        self._italic: bool = italic
        self._multiline: bool = multiline
        self._align: str = align
        self._width: int | None = width

    # ======================================== CONTRACT ========================================
    def __repr__(self) -> str:
        """Renvoie une représentation du composant"""
        return (f"TextRenderer(text={self._text}, z={self._z}, visible={self._visible})")

    def get_attributes(self) -> tuple:
        """Renvoie les attributs du composant"""
        return (self._text, self._offset, self._color, self._opacity, self._weight, self._italic, self._multiline, self._align, self._width, self._z)
    
    def copy(self) -> TextRenderer:
        """Renvoie une copie du composant"""
        new = TextRenderer(self._text, self._offset, self._color, self._opacity, self._weight, self._italic, self._multiline, self._align, self._width, self._z, self._visible)
        return new

    # ======================================== GETTERS ========================================
    @property
    def text(self) -> Text:
        """Descripteur de texte"""
        return self._text
    
    @text.setter
    def text(self, value: Text) -> None:
        value = expect(value, Text)
        self._text = value

    @property
    def offset(self) -> Vector:
        """Décalage par rapport au Transform"""
        return self._offset
    
    @offset.setter
    def offset(self, value: Vector) -> None:
        self._offset.x, self._offset.y = value

    @property
    def color(self) -> Color:
        """Couleur de rendu"""
        return self._color
    
    @color.setter
    def color(self, value: Color) -> None:
        value = Color(value)
        self._color = value

    @property
    def weight(self) -> str:
        """Epaisseur du texte"""
        return self._weight
    
    @weight.setter
    def weight(self, value: str) -> None:
        value = str(value)
        self._weight = value

    @property
    def italic(self) -> bool:
        """Italique"""
        return self._italic
    
    @italic.setter
    def italic(self, value: bool) -> None:
        value = bool(value)
        self._italic = value

    @property
    def multiline(self) -> bool:
        """Renvoie l'état du retour à la ligne automatique"""
        return self._multiline
    
    @multiline.setter
    def multiline(self, value: bool) -> None:
        value = bool(value)
        self._multiline = value

    @property
    def align(self) -> HorizontalAlign:
        """Alignement du texte multiline"""
        return self._align
    
    @align.setter
    def align(self, value: HorizontalAlign) -> None:
        value = str(value)
        if __debug__:
            expect(value, HorizontalAlign)
        self._align = value

    @property
    def width(self) -> int | None:
        """Largeur maximale en pixels"""
        return self._width
    
    @width.setter
    def width(self, value: Integral | None) -> None:
        if value is not None:
            value = int(value)
            if __debug__:
                over(value, 0, include=False)
        self._width = value

# ======================================== EXPORTS ========================================
__all__ = [
    "TextRenderer",
]