# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._internal import expect, not_null, positive
from ..abc import Asset

from numbers import Real

# ======================================== OBJET ========================================
class Image(Asset):
    """Descripteur d'image immuable

    Args:
        path: chemin du fichier
        width: largeur cible en pixels
        height: hauteur cible en pixels
        scale_factor: facteur de redimensionnement
    """
    __slots__ = ("_path", "_width", "_height", "_scale_factor")

    def __init__(
            self,
            path: str,
            width: Real = None,
            height: Real = None,
            scale_factor: Real = 1.0,
        ):
        self._path: str = expect(path, str)
        self._width: float | None = float(positive(expect(width, Real))) if width is not None else None
        self._height: float | None = float(positive(expect(height, Real))) if height is not None else None
        self._scale_factor: float = float(positive(not_null(expect(scale_factor, Real))))

    # ======================================== CONVERSIONS ========================================
    def __repr__(self) -> str:
        """Renvoie une représentation de l'image"""
        return f"Image(path={self._path}, width={self._width}, height={self._height}, scale={self._scale_factor})"

    # ======================================== GETTERS ========================================
    @property
    def path(self) -> str:
        """Renvoie le chemin du fichier"""
        return self._path

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