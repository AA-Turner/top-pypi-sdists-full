# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import over
from ...abc import Bundle

from .._font import Font

from numbers import Integral

# ======================================== BUNDLE ========================================
class FontBundle(Bundle):
    """Paquet de polices
    
    Args:
        paths: dictionnaire des chemin vers les fichiers des polices
        size: taille par défaut des polices
    """
    __slots__ = ("_size",)

    def __init__(self, paths: dict[str, str], size: Integral = 16):
        # Initialisation du paquet
        super().__init__(paths)

        # Transtypage et vérifications
        size = int(size)

        if __debug__:
            over(size, 0, include=False)

        # Attributs publiques
        self._size: int = size

    # ======================================== PROPERTIES ========================================
    @property
    def size(self) -> int:
        """Taille de rendu des polices du bundle

        La taille doit être un entier positif.
        Mettre cette propriété à ``16`` pour une taille normale.
        """
        return self._size

    @size.setter
    def size(self, value: Integral) -> None:
        value = int(value)
        if __debug__:
            over(value, 0, include=False)
        self._size = value

    # ======================================== INTERFACE ========================================
    def get(self, key: str, size: int = None) -> Font:
        """Renvoie une police du bundle

        Args:
            key: clé de la police à récupérer
            size: taille de rendu (taille du Bundle si ``None``)
        """
        # Choix des paramètres de la police
        size = size if size is not None else self._size

        # Génération de la clé de cache
        cache_key = (key, size)
        if cache_key not in self._cache:
            self._cache[cache_key] = Font(
                name=self._paths[key],
                size=size,
            )

        return self._cache[cache_key]