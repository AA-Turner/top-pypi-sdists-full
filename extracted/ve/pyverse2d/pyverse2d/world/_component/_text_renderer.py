# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import expect, clamped
from ...abc import Component
from ...asset import Text, Color
from ...math import Vector

from numbers import Real

# ======================================== COMPONENT ========================================
class TextRenderer(Component):
    """Composant gérant le rendu d'un texte

    Ce composant est manipulé par ``RenderSystem``.

    Args:
        text(Text): descripteur de texte
        offset(Vector, optional): décalage par rapport au Transform
        color(Color, optional): couleur RGBA
        opacity(Real, optional): opacité multiplicative [0.0 – 1.0]
        weight(bool, optional): épaisseur
        italic(bool, optional): italique
        multiline(bool, optional): active le retour à la ligne automatique
        align(str, optional): alignement du texte multiline ("left"|"center"|"right")
        width(int, optional): largeur max en pixels (requis pour multiline)
        z(int, optional): ordre de rendu
        visible(bool, optional): visibilité
    """
    __slots__ = ("_text", "_offset", "_color", "_opacity", "_bold", "_italic", "_multiline", "_align", "_width", "_z", "_visible")
    requires = ("Transform",)

    def __init__(
        self,
        text: Text = None,
        offset: Vector = (0.0, 0.0),
        color: Color = (255, 255, 255, 1.0),
        opacity: Real = 1.0,
        weight: str = "regular",
        italic: bool = False,
        multiline: bool = False,
        align: str = "left",
        width: int = None,
        z: int = 0,
        visible: bool = True,
    ):
        self._text: Text = expect(text, Text)
        self._offset: Vector = Vector(offset)
        self._color: Color = Color(color)
        self._opacity: float = float(clamped(expect(opacity, Real)))
        self._weight: bool = expect(weight, str)
        self._italic: bool = expect(italic, bool)
        self._multiline: bool = expect(multiline, bool)
        self._align: str = expect(align, str)
        self._width: int | None = expect(width, int) if width is not None else None
        self._z: int = expect(z, int)
        self._visible: bool = expect(visible, bool)

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
        """Renvoie le descripteur de texte"""
        return self._text

    @property
    def offset(self) -> Vector:
        """Renvoie le décalage par rapport au Transform"""
        return self._offset

    @property
    def color(self) -> Color:
        """Renvoie la couleur de rendu"""
        return self._color

    @property
    def opacity(self) -> float:
        """Renvoie le facteur d'opacité"""
        return self._opacity

    @property
    def weight(self) -> str:
        """Renvoie l'épaisseur du texte"""
        return self._weight

    @property
    def italic(self) -> bool:
        """Renvoie l'italique du texte"""
        return self._italic

    @property
    def multiline(self) -> bool:
        """Renvoie l'état du retour à la ligne automatique"""
        return self._multiline

    @property
    def align(self) -> str:
        """Renvoie l'alignement du texte multiline"""
        return self._align

    @property
    def width(self) -> int | None:
        """Renvoie la largeur maximale en pixels"""
        return self._width

    @property
    def z(self) -> int:
        """Renvoie l'ordre de rendu"""
        return self._z

    # ======================================== SETTERS ========================================
    @text.setter
    def text(self, value: Text) -> None:
        """Fixe le descripteur de texte"""
        self._text = expect(value, Text)

    @offset.setter
    def offset(self, value: Vector) -> None:
        """Fixe le décalage par rapport au Transform"""
        self._offset = Vector(value)

    @color.setter
    def color(self, value: Color) -> None:
        """Fixe la couleur de rendu"""
        self._color = Color(value)

    @opacity.setter
    def opacity(self, value: Real) -> None:
        """Fixe le facteur d'opacité"""
        self._opacity = float(clamped(expect(value, Real)))

    @weight.setter
    def weight(self, value: str) -> None:
        """Fixe l'épaisseur du texte"""
        self._weight = expect(value, str)

    @italic.setter
    def italic(self, value: bool) -> None:
        """Fixe l'italique du texte"""
        self._italic = expect(value, bool)

    @align.setter
    def align(self, value: str) -> None:
        """Fixe l'alignement du texte multiline"""
        self._align = expect(value, str)

    @width.setter
    def width(self, value: int | None) -> None:
        """Fixe la largeur maximale en pixels"""
        self._width = expect(value, int) if value is not None else None

    @z.setter
    def z(self, value: int):
        """Fixe l'ordre de rendu"""
        self._z = expect(value, int)

    # ======================================== PREDICATES ========================================
    def is_visible(self) -> bool:
        """Vérifie la visibilité"""
        return self._visible

    # ======================================== PUBLIC METHODS ========================================
    def show(self) -> None:
        """Montre le texte"""
        self._visible = True

    def hide(self) -> None:
        """Cache le texte"""
        self._visible = False