# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._internal import over, expect, positive
from ..math import Point

from ._video import Video

import pyglet.media as _media
from numbers import Real
from typing import Callable, Any

# ======================================== PLAYER ========================================
class VideoPlayer:
    """Lecteur vidéo monde"""
    __slots__ = (
        "_position", "_width", "_height",
        "_video", "_source", "_player",
        "_play_volume", "_playback_speed",
        "_loop", "_on_end",
    )

    def __init__(self, position: Point, width: int, height: int):
        # Transtypage et vérifications
        position = Point(position)
        width = int(width)
        height = int(height)

        if __debug__:
            over(width, 0, include=False)
            over(height, 0, include=False)

        # Attributs publiques
        self._position: Point = position
        self._width: int = width
        self._height: int = height

        # Attributs internes
        self._video: Video | None = None
        self._source: _media.Source | None = None
        self._player: _media.Player | None = None

        self._play_volume: float = 1.0
        self._playback_speed: float = 1.0
        self._loop: bool = False
        self._on_end: Callable[[VideoPlayer], Any] | None = None

    # ======================================== PROPERTIES ========================================
    @property
    def position(self) -> Point:
        return self._position

    @position.setter
    def position(self, value: Point) -> None:
        self._position.x, self._position.y = value

    @property
    def x(self) -> float:
        return self._position.x

    @x.setter
    def x(self, value: Real) -> None:
        self._position.x = float(value)

    @property
    def y(self) -> float:
        return self._position.y

    @y.setter
    def y(self, value: Real) -> None:
        self._position.y = float(value)

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, value: int) -> None:
        value = int(value)
        if __debug__:
            over(value, 0, include=False)
        self._width = value

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, value: int) -> None:
        value = int(value)
        if __debug__:
            over(value, 0, include=False)
        self._height = value

    @property
    def volume(self) -> float:
        return self._play_volume

    @volume.setter
    def volume(self, value: Real) -> None:
        value = float(value)
        if __debug__:
            positive(value)
        self._play_volume = value
        if self._player is not None:
            self._player.volume = self._effective_volume

    @property
    def on_end(self) -> Callable | None:
        return self._on_end

    @on_end.setter
    def on_end(self, value: Callable | None) -> None:
        self._on_end = value

    @property
    def texture(self):
        """Frame courante comme texture pyglet (None si inactif)"""
        if self._player is not None:
            return self._player.texture
        return None

    @property
    def time(self) -> float:
        if self._player is not None:
            return self._player.time
        return 0.0

    @property
    def duration(self) -> float | None:
        if self._source is not None:
            return self._source.duration
        return None

    @property
    def time_remaining(self) -> float | None:
        if self._source is not None and self._source.duration is not None:
            return max(0.0, self._source.duration - self.time)
        return None

    @property
    def _effective_volume(self) -> float:
        """Volume final player = volume player × volume asset"""
        if self._video is None:
            return self._play_volume
        return self._play_volume * self._video.volume

    # ======================================== PREDICATES ========================================
    def is_playing(self) -> bool:
        """Vérifie qu'une vidéo soit en cours de lecture"""
        return self._player is not None

    def is_paused(self) -> bool:
        """Vérifie que la lecture soit en pause"""
        return self._player is not None and self._player.paused

    def is_loaded(self) -> bool:
        """Vérifie qu'une vidéo soit chargée"""
        return self._video is not None

    # ======================================== INTERFACE ========================================
    def load(self, video: Video) -> None:
        """Charge une vidéo sans la lire
        
        Args:
            video: ``Video`` asset à charger
        """
        if __debug__:
            expect(video, Video)
        self.stop()
        self._video = video

    def play(
        self,
        video: Video | None = None,
        volume: Real = 1.0,
        loop: bool = False,
        on_end: Callable[[VideoPlayer], Any] | None = None,
    ) -> None:
        """Lance la lecture

        Args:
            video: ``Video`` à lire *(par défaut la vidéo chargée)*
            volume: volume ponctuel
            loop: boucle si True
            on_end: callback de fin de lecture
        """
        if __debug__:
            expect(video, (Video, None))
            positive(float(volume))

        if video is not None:
            self._video = video
        if self._video is None:
            return

        self.stop()

        self._play_volume = float(volume)
        self._loop = bool(loop)
        self._on_end = on_end

        self._source = _media.load(self._video.path, streaming=True)
        self._player = _media.Player()
        self._player.loop = self._loop
        self._player.volume = self._effective_volume
        self._player.queue(self._source)

        @self._player.event
        def on_player_eos():
            self._handle_eos()

        self._player.play()

    def pause(self) -> None:
        """Met en pause"""
        if self._player is not None and not self._player.paused:
            self._player.pause()

    def unpause(self) -> None:
        """Reprend la lecture"""
        if self._player is not None and self._player.paused:
            self._player.play()

    def stop(self) -> None:
        """Arrête la lecture et libère les ressources"""
        if self._player is not None:
            self._player.pause()
            self._player.delete()
            self._player = None
        self._source = None

    def clear(self) -> None:
        """Arrête et décharge la vidéo"""
        self.stop()
        self._video = None

    # ======================================== INTERNALS ========================================
    def _handle_eos(self) -> None:
        """Fin de lecture"""
        if self._on_end is not None:
            self._on_end(self)
        self.stop()