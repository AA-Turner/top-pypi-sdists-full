# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import expect
from ...abc import Space

from numbers import Real

# ======================================== OBJET ========================================
class LogicalScreen(Space):
    """Espace de rendu de référence à résolution fixe

    Args:
        width: largeur de l'espace virtuel
        height: hauteur de l'espace virtuel
    """
    __slots__ = ("_width", "_height")

    def __init__(self, width: int = 1920, height: int = 1080):
        self._width: int = int(expect(width, Real))
        self._height: int = int(expect(height, Real))

    # ======================================== CONVERSIONS ========================================
    def __repr__(self) -> str:
        """Renvoie une représentation de l'espace logique"""
        return f"Screen({self._width}x{self._height})"

    # ======================================== PROPERTIES ========================================
    @property
    def size(self) -> tuple[int, int]:
        """Renvoie la taille de l'écran"""
        return self._width, self._height
    
    @property
    def width(self) -> int:
        """Largeur de l'espace logique"""
        return self._width

    @property
    def height(self) -> int:
        """Hauteur de l'espace logique"""
        return self._height    
    
    @property
    def half_width(self) -> float:
        """Renvoie la demi-largeur de l'écran"""
        return self._width * 0.5
    
    @property
    def half_height(self) -> float:
        """Renvoie la demi-hauteur de l'écran"""
        return self._height * 0.5

    @property
    def center(self) -> tuple[float, float]:
        """Renvoie la position du centre de l'écran"""
        return (self._width * 0.5, self._height * 0.5)
    
    @property
    def centerx(self) -> float:
        """Renvoie le centre x de l'écran"""
        return self._width * 0.5
    
    @property
    def centery(self) -> float:
        """Renvoie le centrey de l'écran"""
        return self._height * 0.5
    
    @property
    def ratio(self) -> float:
        """Ratio largeur/hauteur de l'espace logique"""
        return self._width / self._height