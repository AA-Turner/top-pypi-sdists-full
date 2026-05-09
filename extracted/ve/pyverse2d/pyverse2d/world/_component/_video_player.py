# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import over, expect, expect_callable, positive, clamped, CallbackList
from ...asset import Video
from ...abc import Component
from ...math import Vector
from ...math.easing import EasingFunc, linear

import threading
import queue
import time
from numbers import Real

import pyglet.media as _media

# ======================================== PROPERTIES ========================================
class VideoPlayer(Component):
    """Composant permettant la lecture de vidéos

    Ce composant est manipulé par ``VideoSystem``.
    
    Args:
        width: largeur du lecteur
        height: hauteur du lecteur
        offset: décalage par rapport au ``Transform``
        volume: volume du lecteur
        inner_radius: portée du son à plein volume
        outer_radius: portée absolue du son
        falloff: fonction d'atténuation du son
        opacity: opacité du lecteur
        z: z-order
    """
    __slots__ = (
        "_width", "_height", "_offset",
        "_volume", "_inner_radius", "_outer_radius", "_falloff",
        "_opacity", "_z",
        "_video", "_loop", "_ready",
        "_on_start", "_on_end",
        "_texture", "_frame_queue", "_audio_queue", "_decode_thread", "_stop_event", "_pause_event",
        "_audio_player", "_audio_ready_queue", "_audio_thread", "_audio_stop_event",
        "_pts_origin", "_clock_origin", "_duration",
        "_playing", "_paused", "_initialized",
    )

    requires = ("Transform",)

    def __init__(
            self, 
            width: int,
            height: int,
            offset: Vector = (0.0, 0.0),
            volume: Real = 1.0,
            inner_radius: Real = 0.0,
            outer_radius: Real = 0.0,
            falloff: EasingFunc = linear,
            opacity: Real = 1.0,
            z: int = 0,
        ):
        # Transtypage et vérifications
        width = int(width)
        height = int(height)
        offset = Vector(offset)
        volume = float(volume)
        inner_radius = abs(float(inner_radius))
        outer_radius = abs(float(outer_radius))
        opacity: float = float(opacity)
        z = int(z)

        if __debug__:
            over(width, 0, include=False)
            over(height, 0, include=False)
            positive(volume)
            expect_callable(falloff)
            clamped(opacity)

        # Attributs publiques
        self._width: int = width
        self._height: int = height
        self._offset: Vector = offset

        self._volume: float = volume
        self._inner_radius: float = inner_radius
        self._outer_radius: float = outer_radius
        self._falloff: EasingFunc = falloff

        self._opacity: float = opacity
        self._z: int = z

        # Attributs internes
        self._video: Video | None = None
        self._loop: bool = False

        # Hooks
        self._on_start: CallbackList | None = None
        self._on_end: CallbackList | None = None

        # Décodage
        self._texture = None
        self._frame_queue: queue.Queue | None = None
        self._audio_queue: queue.Queue | None = None
        self._decode_thread: threading.Thread | None = None
        self._stop_event: threading.Event | None = None
        self._pause_event: threading.Event | None = None

        # Audio
        self._audio_player: _media.Player | None = None
        self._audio_ready_queue: queue.Queue | None = None
        self._audio_thread: threading.Thread | None = None

        # Clock
        self._pts_origin: float = 0.0
        self._clock_origin: float = 0.0
        self._duration: float | None = None

        # Etat
        self._playing: bool = False
        self._paused: bool = False
        self._initialized: bool = False
    
    # ======================================== CONTRACT ========================================
    def __repr__(self) -> str:
        """Renvoie une représentation de l'animateur"""
        status = "playing" if self.is_playing() else ("paused" if self.is_paused() else "stopped")
        return f"VideoPlayer(width={self._width}, height={self._height}, volume={self._volume}, status={status})"
    
    def get_attributes(self) -> tuple:
        """Renvoie les attributs du composant"""
        return (
            self._width, self._height, self._offset,
            self._volume, self._inner_radius, self._outer_radius, self._falloff,
            self._opacity, self._z,
        )
    
    def copy(self) -> VideoPlayer:
        """Renvoie une copie du composant"""
        new = VideoPlayer(
            width=self._width, height=self._height, offset=self._offset,
            volume=self._volume, inner_radius=self._inner_radius, outer_radius=self._outer_radius, falloff=self._falloff,
            opacity=self._opacity, z=self._z,
        )
        return new

    # ======================================== PROPERTIES ========================================
    @property
    def width(self) -> int:
        """Largeur du lecteur"""
        return self._width

    @width.setter
    def width(self, value: int) -> None:
        value = int(value)
        if __debug__:
            over(value, 0, include=False)
        self._width = value

    @property
    def height(self) -> int:
        """Hauteur du lecteur"""
        return self._height

    @height.setter
    def height(self, value: int) -> None:
        value = int(value)
        if __debug__:
            over(value, 0, include=False)
        self._height = value

    @property
    def offset(self) -> Vector:
        """Décalage au ``Transform``
        
        Le décalage peut être un objet ``Vector`` ou n'importe quel tuple ```(dx, dy)``.
        """
        return self._offset
    
    @offset.setter
    def offset(self, value: Vector) -> None:
        self._offset.x, self._offset.y = value

    @property
    def volume(self) -> float:
        """Volume du lecteur
        
        Le volume doit être un ``Real`` positif.
        """
        return self._volume

    @volume.setter
    def volume(self, value: Real) -> None:
        value = float(value)
        if __debug__:
            positive(value)
        self._volume = value

    @property
    def inner_radius(self) -> float:
        """Portée du son à plein volume

        Cette propriété fixe un rayon dans lequel le son est au volume normal.
        """
        return self._inner_radius
    
    @inner_radius.setter
    def inner_radius(self, value: Real) -> None:
        value = abs(float(value))
        self._inner_radius = value

    @property
    def outer_radius(self) -> float:
        """Portée maximale du son

        Cette propriété fixe un rayon au-delà duquel le son n'est pas audible.
        Mettre cette propriété à ``0.0`` pour une portée infinie.
        """
        return self._outer_radius
    
    @outer_radius.setter
    def outer_radius(self, value: Real) -> None:
        value = abs(float(value))
        self._outer_radius = value

    @property
    def falloff(self) -> EasingFunc:
        """Fonction d'atténuation

        L'atténuation se fait uniquement en inner_radius et outer_radius.
        Ne fonctionne pas avec un rayon infinie.
        """
        return self._falloff
    
    @falloff.setter
    def falloff(self, value: EasingFunc | None) -> None:
        if __debug__:
            expect_callable(value)
        self._falloff = value or linear

    @property
    def opacity(self) -> float:
        """Renvoie l'opacité du lecteur
        
        L'opacité doit être un ``Real`` compris dans l'intervalle *[0, 1]*.
        """
        return self._opacity
    
    @opacity.setter
    def opacity(self, value: Real) -> None:
        value = float(value)
        if __debug__:
            clamped(value)
        self._opacity = value

    @property
    def z(self) -> int:
        """z-order
        
        Cette propriété définie l'ordre de superposition de l'affichage.
        """
        return self._z
    
    @z.setter
    def z(self, value: int) -> None:
        value = int(value)
        self._z = value

    @property
    def texture(self):
        """Frame courante comme texture pyglet (None si inactif)"""
        return self._texture

    @property
    def time(self) -> float:
        """Curseur temporelle de lecture"""
        if not self.is_playing():
            return 0.0
        if self._paused:
            return self._pts_origin
        return self._pts_origin + (time.perf_counter() - self._clock_origin)

    @property
    def duration(self) -> float | None:
        """Durée de la vidéo chargée"""
        return self._duration

    @property
    def time_remaining(self) -> float | None:
        """Temps restant de la vidéo chargée"""
        if self._duration is None:
            return None
        return max(0.0, self._duration - self.time)

    # ======================================== PREDICATES ========================================
    def is_loaded(self) -> bool:
        """Vérifie qu'une vidéo soit chargée"""
        return self._video is not None

    def is_playing(self) -> bool:
        """Vérifie qu'une vidéo soit en cours de lecture"""
        return self._playing

    def is_paused(self) -> bool:
        """Vérifie que la lecture soit en pause"""
        return self._paused
    
    def is_initialized(self) -> bool:
        """Vérifie que la lecture soit initialisée par le système"""
        return self._initialized
    
    # ======================================== HOOKS ========================================
    @property
    def on_start(self) -> CallbackList:
        """Hook de début de lecture
        
        Le callback reçoit deux arguments: ``VideoPlayer`` et ``Video``
        """
        if self._on_start is None:
            self._on_start = CallbackList()
        return self._on_start

    @property
    def on_end(self) -> CallbackList:
        """Hook de fin de lecture
        
        Le callback reçoit deux arguments: ``VideoPlayer`` et ``Video``
        """
        if self._on_end is None:
            self._on_end = CallbackList()
        return self._on_end

    # ======================================== INTERFACE ========================================
    def load(self, video: Video) -> None:
        """Charge une vidéo
        
        Args:
            video: ``Video`` à charger 
        """
        if __debug__:
            expect(video, Video)
        self.stop()
        self._video = video
        self._initialized = False

    def play(
        self,
        loop: bool = False,
    ) -> None:
        """Lance la lecture
        
        Args:
            loop: relancement automatique de la vidéo
        """
        # Pas de vidéo chargée
        if self._video is None:
            return
    
        # Nettoyage si nécessaire
        if self._playing:
            self.stop()

        # Transtypage et vérifications
        loop = bool(loop)

        # Configuration
        self._loop = loop
        self._paused = False
        self._playing = True

        # Appel des callbacks
        if self._on_start:
            self._on_start.trigger(self, self._video)

    def pause(self) -> None:
        """Mise en pause de la lecture"""
        if not self._playing or self._paused:
            return
        self._pts_origin = self.time 
        self._pause_event.clear()
        self._paused = True

    def unpause(self) -> None:
        """Reprends la lecture"""
        if not self._playing or not self._paused:
            return
        self._clock_origin = time.perf_counter()
        self._pause_event.set()
        self._paused = False

    def stop(self) -> None:
        """Arrête la lecture"""
        if not self._playing:
            return
        if self._stop_event is not None:
            self._stop_event.set()
        if self._pause_event is not None:
            self._pause_event.set()
        self._paused = False
        self._playing = False

    def clear(self) -> None:
        """Nettoie l'état courant"""
        self.stop()
        self._video = None
        self._texture = None
        self._duration = None
        self._initialized = False