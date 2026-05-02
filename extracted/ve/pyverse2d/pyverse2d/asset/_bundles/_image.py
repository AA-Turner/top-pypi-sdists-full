# ======================================== IMPORTS ========================================
from __future__ import annotations

from ...abc._bundle import Bundle

from .._image import Image

from typing import TYPE_CHECKING
from numbers import Real

if TYPE_CHECKING:
    from ..._managers._audio import SoundGroup

# ======================================== BUNDLE ========================================
class ImageBundle(Bundle):
    """Paquet d'images"""
    __slots__ = ("_width", "_height", "_scale_factor")

    def __init__(self, paths: dict[str, str], width: Real = None, height: Real = None, scale_factor: Real = 1.0):
        super().__init__(paths)
        self._width: Real | None = width
        self._height: Real | None = height
        self._scale_factor: Real = scale_factor

    # ======================================== PROPERTIES ========================================
    @property
    def width(self) -> Real | None:
        """Largeur de lecture des images du bundle

        La largeur doit être un ``Réel`` positif ou ``None``.
        Mettre cette propriété à ``None`` pour utiliser la largeur originale des images.
        """
        return self._width
    
    @width.setter
    def width(self, value: Real | None) -> None:
        if value is not None:
            value = float(value)
            assert value > 0.0, f"width ({value}) must be positive"
        self._width = value
    
    @property
    def height(self) -> Real | None:
        """Hauteur de lecture des images du bundle

        La hauteur doit être un ``Réel`` positif ou ``None``.
        Mettre cette propriété à ``None`` pour utiliser la hauteur originale des images.
        """
        return self._height

    @height.setter
    def height(self, value: Real | None) -> None:
        if value is not None:
            value = float(value)
            assert value > 0.0, f"height ({value}) must be positive"
        self._height = value
    
    @property
    def scale_factor(self) -> Real:
        """Facteur d'échelle de lecture des images du bundle

        Le facteur d'échelle doit être un ``Réel`` positif.
        Mettre cette propriété à ``1.0`` pour une échelle normale.
        """
        return self._scale_factor
    
    @scale_factor.setter
    def scale_factor(self, value: Real) -> None:
        value = float(value)
        assert value > 0.0, f"scale_factor ({value}) must be positive"
        self._scale_factor = value

    # ======================================== INTERFACE ========================================
    def get(self, key: str, width: Real = None, height: Real = None, scale_factor: Real = None) -> Image:
        """Renvoie le chemin d'accès à une image du bundle

        Args:
            key: clé de l'image à récupérer
            width: largeur (largeur du Bundle si ``None``)
            height: hauteur (hauteur du Bundle si ``None``)
            scale_factor: facteur d'échelle (facteur d'échelle du Bundle si ``None``)
        """
        # Choix des paramètres de l'image
        width = width if width is not None else self._width
        height = height if height is not None else self._height
        scale_factor = scale_factor if scale_factor is not None else self._scale_factor

        # Génération de la clé de cache
        cache_key = (key, width, height, scale_factor)
        if cache_key not in self._cache:
            self._cache[cache_key] = Image(
                path = self._paths[key],
                width = width,
                height = height,
                scale_factor = scale_factor,
            )

        return self._cache[cache_key]