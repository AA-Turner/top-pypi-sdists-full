# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._internal import over, different_from
from ..abc import Asset

from numbers import Real

# ======================================== ASSET ========================================
class Image(Asset):
    """Descripteur d'image immuable

    Args:
        path: chemin du fichier
        width: largeur cible en pixels
        height: hauteur cible en pixels
        scale_factor: facteur de redimensionnement
    """
    __slots__ = (
        "_path",
        "_width", "_height", "_scale_factor",
    )

    def __init__(
            self,
            path: str,
            width: Real = None,
            height: Real = None,
            scale_factor: Real = 1.0,
        ):
        # Transtypage et véririfications
        path = str(path)
        width = float(width) if width is not None else None
        height = float(height) if height is not None else None
        scale_factor = float(scale_factor)

        if __debug__:
            if width is not None: over(width, 0, include=False)
            if height is not None: over(height, 0, include=False)
            different_from(scale_factor, 0)

        # Attributs publiques
        self._path: str = path
        self._width: float | None = width
        self._height: float | None = height
        self._scale_factor: float = scale_factor

    # ======================================== CONVERSIONS ========================================
    def __repr__(self) -> str:
        """Renvoie une représentation de l'image"""
        return f"Image(path={self._path}, width={self._width}, height={self._height}, scale={self._scale_factor})"

    # ======================================== PROPERTIES ========================================
    @property
    def path(self) -> str:
        """Renvoie le chemin du fichier"""
        return self._path
    
    @property
    def size(self) -> tuple[float, float] | None:
        """Renvoie la taille de l'image ou ``None`` si non définie"""
        return (self._width, self._width) if self._width and self._height else None

    @property
    def width(self) -> float | None:
        """Renvoie la largeur cible"""
        return self._width

    @property
    def height(self) -> float | None:
        """Renvoie la hauteur cible"""
        return self._height
    
    @property
    def scale_factor(self) -> float:
        """Renvoie le facteur de redimensionnement"""
        return self._scale_factor

# ======================================== EXPORTS ========================================
__all__ = [
    "Image",
]