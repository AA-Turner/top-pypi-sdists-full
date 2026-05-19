# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._internal import expect
from ..abc import Asset

from ._font import Font

from numbers import Real

# ======================================== OBJET ========================================
class Text(Asset):
    """Descripteur immuable de texte

    Args:
        text: contenu
        font: police
    """
    __slots__ = ("_text", "_font")

    def __init__(self, text: str, font: Font = None):
        # Transtypage et vérifications
        text = str(text)
        font = font if font is not None else Font()

        if __debug__:
            expect(font, Font)

        # Attributs publiques
        self._text: str = text
        self._font: Font = font

    # ======================================== CONVERSIONS ========================================
    def __repr__(self) -> str:
        return f"Text(text={self._text}, font={self._font})"

    # ======================================== GETTERS ========================================
    @property
    def text(self) -> str:
        """Renvoie le contenu du texte"""
        return self._text

    @property
    def font(self) -> Font:
        """Renvoie la police"""
        return self._font

    # ======================================== INTERFACE ========================================    
    def get_width(self) -> int:
        """Renvoie la largeur théorique du texte"""
        return self._font.text_width(self._text)

    def with_text(self, text: str) -> Text:
        """
        Renvoie un nouveau Text avec un contenu différent

        Args:
            text: nouveau texte
        """
        return Text(text, self._font)
 
    def with_font(self, font: Font) -> Text:
        """
        Renvoie un nouveau Text avec une police différente

        Args:
            font: nouvelle font
        """
        return Text(self._text, font)

    
    def with_clip(self, width: Real = 0.0, suffix: str = "") -> Text:
        """
        Limite le texte à une certaine largeur

        Args:
            width: largeur maximale *(0.0 pour largeur illimitée)*
            suffix: suffixe à ajouter pour indiquer que le texte est coupé
        """
        self._text = Text(self._font.clip_text(self._text, max_width=width, suffix=suffix), font=self._font)

# ======================================== EXPORTS ========================================
__all__ = [
    "Text",
]