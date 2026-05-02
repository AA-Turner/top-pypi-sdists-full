from __future__ import annotations

from .._internal import positive
from .._flag import AudioState
from ..abc import Asset

from typing import TYPE_CHECKING, Callable, Any
from numbers import Real

from pyglet import media as _media

if TYPE_CHECKING:
    from .._managers._audio import AudioManager, MusicHandle

class Music(Asset):
    """Musique streamée depuis le disque *(BGM)*

    Args:
        path: chemin vers le fichier audio
        volume: volume propre [0, 1]
    """
    __slots__ = (
        "_path", "_volume",
        "_handle", "_state", "_loop",
        "_source",
    )

    _AUDIO_MANAGER: AudioManager = None

    @classmethod
    def _get_audio_manager(cls) -> AudioManager:
        """Renvoie le gestionnaire audio"""
        if cls._AUDIO_MANAGER is None:
            from .._managers._audio import AudioManager
            cls._AUDIO_MANAGER = AudioManager.get_instance()
        return cls._AUDIO_MANAGER

    def __init__(self, path: str, volume: Real = 1.0):
        self._path: str = path
        self._volume: float = float(volume)

        if __debug__:
            positive(self._volume)

        self._handle: MusicHandle | None = None
        self._state: AudioState = AudioState.SLEEPING
        self._loop: bool = True
        self._source: _media.Source | None = None

    def __hash__(self) -> int:
        """Renvoie le hash de la musique"""
        return hash((self._path, self._volume))

    # ======================================== PROPERTIES ========================================
    @property
    def path(self) -> str:
        """Chemin du fichier audio"""
        return self._path

    @path.setter
    def path(self, value: str) -> None:
        self._path = value

    @property
    def volume(self) -> float:
        """Volume propre
        
        Le volume doit être un ``Réel`` positif.
        """
        return self._volume

    @volume.setter
    def volume(self, value: Real) -> None:
        value = float(value)
        assert value >= 0.0, f"volume ({value}) must be positive"
        self._volume = value
        if self._handle is not None:
            self._handle._set_volume(value)

    # ======================================== PREDICATES ========================================
    def __eq__(self, other: object) -> bool:
        """Vérifie la correspondance de deux musiques"""
        if isinstance(other, Music):
            return self._path == other.path and self._volume == other.volume
        return NotImplemented

    def is_playing(self) -> bool:
        """Vérifie que la musique soit en cours de lecture"""
        return self._state == AudioState.PLAYING

    def is_paused(self) -> bool:
        """Vérifie que la musique soit en pause"""
        return self._state == AudioState.PAUSED

    # ======================================== INTERFACE ========================================
    def preload(self) -> None:
        """Précharge la source audio pour éviter le freeze au premier play"""
        if self._source is None:
            self._source = _media.load(self._path, streaming=True)

    def copy(self) -> Music:
        """Renvoie une copie de la musique"""
        return Music(path=self._path, volume=self._volume)

    def play(self, volume: Real = 1.0, loop: bool = True, fade_s: Real = 0.0, on_end: Callable[[MusicHandle], Any] = None, playlist_fallback: bool = True) -> MusicHandle | None:
        """Joue la musique

        Args:
            loop: boucle infinie si True
            fade_s: durée du fade-in en secondes
        """
        return self._get_audio_manager().play_music(self, loop=loop, fade_s=fade_s, on_end=on_end, playlist_fallback=playlist_fallback)

    def stop(self, fade_s: Real = 0.0) -> None:
        """Arrête la musique.

        Args:
            fade_s: durée du fade-out en secondes
        """
        if self._get_audio_manager().current_music is self:
            self._get_audio_manager().stop_music(fade_s=fade_s)

    # ======================================== INTERNALS ========================================
    def _set_volume(self, value: float) -> None:
        """Volume brut sur le handle"""
        if self._handle is not None:
            self._handle._set_volume(value)

    def _set_state(self, value: AudioState) -> None:
        """Fixe l'état"""
        self._state = value
    
    def _set_loop(self, value: bool) -> None:
        """Fixe la boucle"""
        self._loop = value

    def _set_handle(self, value: MusicHandle | None) -> None:
        """Fixe le handle"""
        self._handle = value