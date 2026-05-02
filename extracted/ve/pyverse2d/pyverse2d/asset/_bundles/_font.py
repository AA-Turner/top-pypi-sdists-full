# ======================================== IMPORTS ========================================
from __future__ import annotations

from ...abc._bundle import Bundle

from .._font import Font

from numbers import Real

# ======================================== BUNDLE ========================================
class FontBundle(Bundle):
    """Paquet de polices"""
    __slots__ = ("_size",)

    def __init__(self, paths: dict[str, str], size: int = 16):
        super().__init__(paths)
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
    def size(self, value: int) -> None:
        value = int(value)
        assert value > 0, f"size ({value}) must be strictly positive"
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