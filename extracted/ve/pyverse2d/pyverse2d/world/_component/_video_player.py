# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import over, expect, expect_callable, positive, clamped, CallbackList
from ...asset import Video
from ...abc import Component
from ...math import Vector
from ...math.easing import EasingFunc, linear

import threading
import queue
from numbers import Real

import pyglet.media as _media

# ======================================== COMPONENT ========================================
class VideoPlayer(Component):
    """Composant permettant la lecture de vidéos

    Ce composant est manipulé par ``VideoSystem``.

    Args:
        width: largeur d'affichage du lecteur, en pixels
        height: hauteur d'affichage du lecteur, en pixels
        offset: décalage (dx, dy) par rapport au ``Transform`` frère
        volume: volume de base du lecteur ; doit être un réel positif
        inner_radius: rayon (en unités monde) dans lequel le son est au volume plein
        outer_radius: rayon au-delà duquel le son est inaudible ; ``0.0`` = infini
        falloff: fonction d'atténuation appliquée entre ``inner_radius`` et ``outer_radius``
        opacity: opacité d'affichage, dans l'intervalle *[0, 1]*
        z: z-order d'affichage (ordre de superposition)
    """
    __slots__ = (
        "_width", "_height", "_offset",
        "_volume", "_inner_radius", "_outer_radius", "_falloff",
        "_opacity", "_z",
        "_video", "_loop", "_ready",
        "_on_start", "_on_end",
        "_texture", "_pending_frame",
        "_frame_queue", "_decode_thread",
        "_stop_event", "_pause_event",
        "_end_event", "_loop_event",
        "_audio_player", "_audio_feed", "_audio_started",
        "_prev_audio_feed",
        "_paused_time",
        "_loop_time_offset",
        "_duration",
        "_playing", "_paused", "_initialized",
        "_frames_ready", "_audio_ready", "_audio_start_time",
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
        width = int(width)
        height = int(height)
        offset = Vector(offset)
        volume = float(volume)
        inner_radius = abs(float(inner_radius))
        outer_radius = abs(float(outer_radius))
        opacity = float(opacity)
        z = int(z)

        if __debug__:
            over(width, 0, include=False)
            over(height, 0, include=False)
            positive(volume)
            expect_callable(falloff)
            clamped(opacity)

        self._width: int = width
        self._height: int = height
        self._offset: Vector = offset

        self._volume: float = volume
        self._inner_radius: float = inner_radius
        self._outer_radius: float = outer_radius
        self._falloff: EasingFunc = falloff

        self._opacity: float = opacity
        self._z: int = z

        self._video: Video | None = None
        self._loop: bool = False

        self._on_start: CallbackList | None = None
        self._on_end: CallbackList | None = None

        self._texture = None
        self._pending_frame: tuple | None = None

        self._frame_queue: queue.Queue | None = None
        self._decode_thread: threading.Thread | None = None
        self._stop_event: threading.Event | None = None
        self._pause_event: threading.Event | None = None

        self._end_event: threading.Event | None = None
        self._loop_event: threading.Event | None = None

        self._audio_player: _media.Player | None = None
        self._audio_feed = None
        self._audio_started: bool = False
        self._prev_audio_feed = None

        self._paused_time: float = 0.0
        self._loop_time_offset: float = 0.0

        self._duration: float | None = None

        self._playing: bool = False
        self._paused: bool = False
        self._initialized: bool = False

        self._frames_ready: bool = False
        self._audio_ready: bool = False
        self._audio_start_time: float = 0.0

    # ======================================== CONTRACT ========================================
    def __repr__(self) -> str:
        """Renvoie une représentation lisible du lecteur"""
        if self.is_playing():
            status = "playing"
        elif self.is_paused():
            status = "paused"
        else:
            status = "stopped"
        return (
            f"VideoPlayer(width={self._width}, height={self._height}, "
            f"volume={self._volume}, status={status})"
        )

    def get_attributes(self) -> tuple:
        """Renvoie le tuple d'attributs publics du composant"""
        return (
            self._width, self._height, self._offset,
            self._volume, self._inner_radius, self._outer_radius, self._falloff,
            self._opacity, self._z,
        )

    def copy(self) -> VideoPlayer:
        """Renvoie une copie indépendante du composant (sans état de lecture)"""
        return VideoPlayer(
            width=self._width, height=self._height, offset=self._offset,
            volume=self._volume, inner_radius=self._inner_radius,
            outer_radius=self._outer_radius, falloff=self._falloff,
            opacity=self._opacity, z=self._z,
        )

    # ======================================== PROPERTIES ========================================
    @property
    def width(self) -> int:
        """Largeur d'affichage du lecteur, en unités monde"""
        return self._width

    @width.setter
    def width(self, value: int) -> None:
        value = int(value)
        if __debug__:
            over(value, 0, include=False)
        self._width = value

    @property
    def height(self) -> int:
        """Hauteur d'affichage du lecteur, en unités monde"""
        return self._height

    @height.setter
    def height(self, value: int) -> None:
        value = int(value)
        if __debug__:
            over(value, 0, include=False)
        self._height = value

    @property
    def offset(self) -> Vector:
        """Décalage ``(dx, dy)`` par rapport au ``Transform``

        Accepte un ``Vector`` ou tout tuple ``(dx, dy)``.
        """
        return self._offset

    @offset.setter
    def offset(self, value: Vector) -> None:
        self._offset.x, self._offset.y = value

    @property
    def volume(self) -> float:
        """Volume de base du lecteur

        Doit être un réel positif ou nul. Multiplié par le volume de l'asset ``Video`` et l'atténuation spatiale pour donner le volume final.
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
        """Rayon (en unités monde) dans lequel le son est au volume plein

        Au-delà de ce rayon, aucune atténuation n'est appliquée.
        """
        return self._inner_radius

    @inner_radius.setter
    def inner_radius(self, value: Real) -> None:
        self._inner_radius = abs(float(value))

    @property
    def outer_radius(self) -> float:
        """Rayon maximal d'audibilité (en unités monde)

        Au-delà de ce rayon, le volume est nul. Mettre à ``0.0`` pour une portée infinie.
        """
        return self._outer_radius

    @outer_radius.setter
    def outer_radius(self, value: Real) -> None:
        self._outer_radius = abs(float(value))

    @property
    def falloff(self) -> EasingFunc:
        """Fonction d'atténuation spatiale

        Appliquée uniquement entre ``inner_radius`` et ``outer_radius``.
        Sans effet si ``outer_radius == 0.0`` *(portée infinie)*.
        """
        return self._falloff

    @falloff.setter
    def falloff(self, value: EasingFunc | None) -> None:
        if __debug__:
            expect_callable(value)
        self._falloff = value or linear

    @property
    def opacity(self) -> float:
        """Opacité d'affichage du lecteur, dans l'intervalle *[0, 1]*"""
        return self._opacity

    @opacity.setter
    def opacity(self, value: Real) -> None:
        value = float(value)
        if __debug__:
            clamped(value)
        self._opacity = value

    @property
    def z(self) -> int:
        """Z-order d'affichage (ordre de superposition des rendus)"""
        return self._z

    @z.setter
    def z(self, value: int) -> None:
        self._z = int(value)

    @property
    def texture(self):
        """Texture pyglet de la frame courante (``None`` si inactif ou non initialisé)"""
        return self._texture

    @property
    def time(self) -> float:
        """Position temporelle courante de la lecture, en secondes

        Basée sur le ``playback_time`` du feed audio courant (monotonic ancré
        au premier sample réel consommé par OpenAL) + offset cumulé des loops
        précédents. Retourne la position dans le fichier vidéo courant.
        """
        if not self._playing:
            return 0.0
        if self._paused:
            return self._paused_time
        if self._audio_feed is not None:
            return self._loop_time_offset + self._audio_feed.playback_time
        return 0.0

    @property
    def duration(self) -> float | None:
        """Durée totale de la vidéo chargée, en secondes (``None`` si inconnue)"""
        return self._duration

    @property
    def time_remaining(self) -> float | None:
        """Temps restant avant la fin de la vidéo, en secondes

        Retourne ``None`` si la durée est inconnue.
        """
        if self._duration is None:
            return None
        return max(0.0, self._duration - self.time)

    # ======================================== PREDICATES ========================================
    def is_loaded(self) -> bool:
        """Retourne ``True`` si une vidéo est chargée"""
        return self._video is not None

    def is_playing(self) -> bool:
        """Retourne ``True`` si la lecture est active (y compris en pause)"""
        return self._playing

    def is_paused(self) -> bool:
        """Retourne ``True`` si la lecture est en pause"""
        return self._paused

    def is_initialized(self) -> bool:
        """Retourne ``True`` si le système a initialisé les ressources de décodage"""
        return self._initialized

    # ======================================== HOOKS ========================================
    @property
    def on_start(self) -> CallbackList:
        """Hook déclenché au démarrage de la lecture

        Les callbacks reçoivent ``(player: VideoPlayer, video: Video)``.
        """
        if self._on_start is None:
            self._on_start = CallbackList()
        return self._on_start

    @property
    def on_end(self) -> CallbackList:
        """Hook déclenché à la fin de la lecture (hors boucle)

        Les callbacks reçoivent ``(player: VideoPlayer, video: Video)``.
        """
        if self._on_end is None:
            self._on_end = CallbackList()
        return self._on_end

    # ======================================== INTERFACE ========================================
    def load(self, video: Video) -> None:
        """Charge une vidéo et arrête toute lecture en cours

        Args:
            video: asset ``Video`` à charger
        """
        if __debug__:
            expect(video, Video)
        self.stop()
        self._video = video
        self._initialized = False

    def play(self, loop: bool = False) -> None:
        """Démarre la lecture de la vidéo chargée

        Si une lecture est déjà en cours, elle est arrêtée avant de redémarrer.
        Sans effet si aucune vidéo n'est chargée.

        Args:
            loop: si ``True``, la vidéo repart automatiquement à la fin
        """
        if self._video is None:
            return
        if self._playing:
            self.stop()
        self._loop = bool(loop)
        self._paused = False
        self._playing = True
        if self._on_start:
            self._on_start.trigger(self, self._video)

    def pause(self) -> None:
        """Met la lecture en pause

        Fige la clock audio à la position courante et suspend OpenAL.
        Sans effet si la lecture est arrêtée ou déjà en pause.
        """
        if not self._playing or self._paused:
            return
        self._paused_time = self.time
        self._pause_event.clear()
        self._paused = True
        if self._audio_player is not None:
            try:
                self._audio_player.pause()
            except Exception:
                pass

    def unpause(self) -> None:
        """Reprend la lecture depuis la position de pause

        Sans effet si la lecture est arrêtée ou non en pause.
        """
        if not self._playing or not self._paused:
            return
        self._pause_event.set()
        self._paused = False
        if self._audio_player is not None:
            try:
                self._audio_player.play()
            except Exception:
                pass

    def stop(self) -> None:
        """Arrête la lecture et signale le thread de décodage

        Le nettoyage complet des ressources est délégué à ``VideoSystem._stop_player()``.
        """
        if not self._playing:
            return
        if self._stop_event is not None:
            self._stop_event.set()
        if self._pause_event is not None:
            self._pause_event.set()
        self._paused = False
        self._playing = False

    def clear(self) -> None:
        """Arrête la lecture et décharge la vidéo courante"""
        self.stop()
        self._video = None
        self._texture = None
        self._pending_frame = None
        self._duration = None
        self._audio_started = False
        self._prev_audio_feed = None
        self._loop_time_offset = 0.0
        self._initialized = False