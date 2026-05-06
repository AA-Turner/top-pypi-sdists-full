# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import over
from ...abc import Space

# ======================================== OBJET ========================================
class LogicalScreen(Space):
    """Espace de rendu de référence à résolution fixe

    Args:
        width: largeur de l'espace virtuel
        height: hauteur de l'espace virtuel
    """
    __slots__ = ("_width", "_height")

    def __init__(self, width: int = 1920, height: int = 1080):
        # Transtypage et vérifications
        width = int(width)
        height= int(height)

        if __debug__:
            over(width, 0, include=False)
            over(height, 0, include=False)

        self._width: int = width
        self._height: int = height

    # ======================================== CONVERSIONS ========================================
    def __repr__(self) -> str:
        """Renvoie une représentation """
        return f"Screen({self._width}x{self._height})"

    # ======================================== PROPERTIES ========================================
    @property
    def size(self) -> tuple[int, int]:
        """Taille """
        return self._width, self._height
    
    @property
    def width(self) -> int:
        """Largeur """
        return self._width

    @property
    def height(self) -> int:
        """Hauteur """
        return self._height    
    
    @property
    def half_width(self) -> float:
        """Renvoie la demi-largeur """
        return self._width * 0.5
    
    @property
    def half_height(self) -> float:
        """Renvoie la demi-hauteur """
        return self._height * 0.5

    @property
    def center(self) -> tuple[float, float]:
        """Renvoie la position du centre """
        return (self._width * 0.5, self._height * 0.5)
    
    @property
    def centerx(self) -> float:
        """Renvoie le centre ``x`` """
        return self._width * 0.5
    
    @property
    def centery(self) -> float:
        """Renvoie le centre ``y`` """
        return self._height * 0.5
    
    @property
    def ratio(self) -> float:
        """Ratio ``largeur / hauteur`` """
        return self._width / self._height