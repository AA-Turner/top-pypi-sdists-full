# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._internal import positive
from .._flag import AudioState
from ..abc import Asset

from typing import TYPE_CHECKING, Callable, Any
from numbers import Real
import threading

from pyglet import media as _media

if TYPE_CHECKING:
    from .._managers._audio import AudioManager, MusicHandle

# ======================================== ASSET ========================================
class Music(Asset):
    """Musique streamée depuis le disque *(BGM)*

    Args:
        path: chemin vers le fichier audio
        volume: volume propre [0, 1]
    """
    __slots__ = (
        "_path", "_volume",
        "_handle", "_state", "_loop",
        "_source", "_source_lock", "_loading_source",
    )

    _AUDIO_MANAGER: AudioManager = None

    @classmethod
    def _get_audio_manager(cls) -> AudioManager:
        """Renvoie l'instance du manager audio"""
        if cls._AUDIO_MANAGER is None:
            from .._managers._audio import AudioManager
            cls._AUDIO_MANAGER = AudioManager.get_instance()
        return cls._AUDIO_MANAGER

    def __init__(self, path: str, volume: Real = 1.0):
        # Transtypage et vérifications
        volume = float(volume)

        if __debug__:
            positive(volume)

        # Attributs publiques
        self._path: str = path
        self._volume: float = volume

        # Attributs internes
        self._handle: MusicHandle | None = None
        self._state: AudioState = AudioState.SLEEPING
        self._loop: bool = True
        self._source: _media.StreamingSource | None = None
        self._source_lock: threading.Lock = threading.Lock()
        self._loading_source: bool = False

    def __hash__(self) -> int:
        """Renvoie le hash de l'asset"""
        return hash((self._path, self._volume))

    # ======================================== PROPERTIES ========================================
    @property
    def path(self) -> str:
        """Chemin vers le fichier audio"""
        return self._path

    @property
    def volume(self) -> float:
        """Volume propre"""
        return self._volume

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
        """Précharge la source audio en arrière-plan"""
        with self._source_lock:
            if self._source is not None or self._loading_source:
                return
            self._loading_source = True

        def _worker():
            source = _media.load(self._path, streaming=True)
            with self._source_lock:
                if self._source is None:
                    self._source = source
                self._loading_source = False

        threading.Thread(target=_worker, daemon=True).start()

    def play(self, volume: Real = 1.0, loop: bool = True, fade_s: Real = 0.0, on_end: Callable[[MusicHandle], Any] = None, playlist_fallback: bool = True) -> MusicHandle | None:
        """Joue la musique

        Args:
            loop: boucle infinie si True
            fade_s: durée du fade-in en secondes
        """
        return self._get_audio_manager().play_music(self, volume=volume, loop=loop, fade_s=fade_s, on_end=on_end, playlist_fallback=playlist_fallback)

    def stop(self, fade_s: Real = 0.0) -> None:
        """Arrête la musique.

        Args:
            fade_s: durée du fade-out en secondes
        """
        if self._get_audio_manager().current_music is self:
            self._get_audio_manager().stop_music(fade_s=fade_s)

    # ======================================== INTERNALS ========================================
    def _set_volume(self, value: float) -> None:
        if self._handle is not None:
            self._handle._set_volume(value)

    def _set_state(self, value: AudioState) -> None:
        self._state = value

    def _set_loop(self, value: bool) -> None:
        self._loop = value

    def _set_handle(self, value: MusicHandle | None) -> None:
        self._handle = value

    def _get_source(self) -> _media.StreamingSource | None:
        """Consomme la source prête si disponible (thread-safe)"""
        with self._source_lock:
            source = self._source
            self._source = None
            return source