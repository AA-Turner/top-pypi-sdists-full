# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import positive
from ...abc import Bundle

from .._music import Music

from numbers import Real

# ======================================== BUNDLE ========================================
class MusicBundle(Bundle):
    """Paquet de musiques
    
    Args:
        paths: chemins vers les fichiers
        volume: volume par défaut
    """
    __slots__ = ("_volume",)

    def __init__(self, paths: dict[str, str], volume: Real = 1.0):
        # Initialisation du paquet
        super().__init__(paths)

        # Transtypage et vérifications
        volume = float(volume)

        if __debug__:
            positive(volume)

        # Attributs publiques
        self._volume: Real = volume

    # ======================================== PROPERTIES ========================================
    @property
    def volume(self) -> Real:
        """Volume de lecture des musiques du bundle par défaut

        Le volume doit être un ``Réel`` positif.
        Mettre cette propriété à ``1.0`` pour un volume normal.
        """
        return self._volume
    
    @volume.setter
    def volume(self, value: Real) -> None:
        value = float(value)
        if __debug__:
            positive(value)
        self._volume = value

    # ======================================== INTERFACE ========================================
    def get(self, key: str, volume: Real | None = None) -> Music:
        """Renvoie le chemin d'accès à une musique du bundle

        Args:
            key: clé de la musique à récupérer
            volume: volume (volume du Bundle si ``None``)
        """
        # Choix des paramètres du son
        volume = volume if volume is not None else self._volume

        # Génération de la clé de cache
        cache_key  = (key, volume)
        if cache_key not in self._cache:
            music = Music(
                path = self._paths[key],
                volume = volume,
            )
            music.preload()
            self._cache[cache_key] = music

        return self._cache[cache_key]