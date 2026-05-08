# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._internal import expect

from numbers import Real

# ======================================== VIDEO ========================================
class Video:
    """Descripteur immuable de vidéo
    
    Args:
        path: chemin vers le fichier
        volume: volume spécifique
    """
    __slots__ = ("_path", "_volume")

    def __init__(self, path: str, volume: Real = 1.0):
        # Transtypage et vérifications
        volume = float(volume)

        if __debug__:
            expect(path, str)

        # Attributs publiques
        self._path: str = path
        self._volume: float = volume

    # ======================================== PROPERTIES ========================================
    @property
    def path(self) -> str:
        """Chemin vers le fichier
        
        Le chemin doit être un ``str``.
        """
        return self._path
    
    @property
    def volume(self) -> float:
        """Volume spécifique
        
        Le volume doit être un ``Real`` positif.
        """
        return self._volume