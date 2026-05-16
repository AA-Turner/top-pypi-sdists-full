# ======================================== IMPORTS ========================================
from __future__ import annotations

import av
import queue
import threading
import time as _time
import pyglet.image as _image
import pyglet.media as _media
import pyglet.media.codecs as _codecs

from ..._internal import expect, HasPosition, profile_section
from ..._rendering import PygletTextureRenderer, Pipeline
from ...abc import System
from .._world import World
from .._component import Transform, VideoPlayer

# ======================================== CONSTANTS ========================================
_VIDEO_BUFFER: int = 16
_AUDIO_RATE: int = 44100
_AUDIO_CH: int = 2
_AUDIO_BUFFER_MAX: int = 4 * _AUDIO_RATE * _AUDIO_CH * 2
_AUDIO_PREBUFFER: float = 0.6

# ======================================== NO-SEEK PLAYER ========================================
class _NoSeekPlayer(_media.Player):
    """Player pyglet qui ne tente pas de seek() à la fin d'un StreamingSource"""

    def __init__(self) -> None:
        super().__init__()
        self.loop = False

    def on_eos(self) -> None:
        pass


# ======================================== AUDIO FEED ========================================
class _AudioFeed(_media.StreamingSource):
    """Source PCM streaming thread-safe pour pyglet/OpenAL"""

    def __init__(self, sample_rate: int = _AUDIO_RATE, channels: int = _AUDIO_CH) -> None:
        self.audio_format = _codecs.AudioFormat(
            channels=channels,
            sample_size=16,
            sample_rate=sample_rate,
        )
        self._buf:               bytearray         = bytearray()
        self._lock:              threading.Lock    = threading.Lock()
        self._done:              bool              = False
        self._start_mono:        float | None      = None
        self._play_requested_at: float | None      = None
        self._loop_offset:       float             = 0.0
        self._queued:            bool              = False
        # Positionné à True sur les passes de loop : le buffer est déjà plein
        # au moment du démarrage, pas besoin d'attendre _AUDIO_PREBUFFER.
        self._skip_prebuffer:    bool              = False

    # ------------------------------------------------------------------
    def push(self, data: bytes) -> None:
        with self._lock:
            if len(self._buf) + len(data) <= _AUDIO_BUFFER_MAX:
                self._buf.extend(data)

    def mark_done(self) -> None:
        with self._lock:
            self._done = True

    # ------------------------------------------------------------------
    @property
    def started(self) -> bool:
        """``True`` dès que le premier sample réel a été consommé par OpenAL."""
        with self._lock:
            return self._start_mono is not None

    @property
    def playback_time(self) -> float:
        """Secondes écoulées depuis le premier vrai sample consommé par OpenAL."""
        with self._lock:
            if self._start_mono is None:
                return 0.0
            return _time.monotonic() - self._start_mono

    @property
    def buffered_seconds(self) -> float:
        bps = self.audio_format.sample_rate * self.audio_format.channels * 2
        with self._lock:
            return len(self._buf) / bps

    # ------------------------------------------------------------------
    def get_audio_data(self, num_bytes: int, compensation_time: float = 0.0):
        with self._lock:
            available = len(self._buf)

            if available == 0 and self._done:
                return None

            if available == 0:
                sr  = self.audio_format.sample_rate
                ch  = self.audio_format.channels
                dur = num_bytes / (sr * ch * 2)
                return _codecs.AudioData(b"\x00" * num_bytes, num_bytes, 0.0, dur, [])

            if self._start_mono is None:
                self._start_mono = _time.monotonic()

            n    = min(num_bytes, available)
            data = bytes(self._buf[:n])
            del self._buf[:n]

        sr  = self.audio_format.sample_rate
        ch  = self.audio_format.channels
        dur = n / (sr * ch * 2)
        return _codecs.AudioData(data, n, 0.0, dur, [])


# ======================================== SYSTEM ========================================
class VideoSystem(System):
    """Système gérant les composants ``VideoPlayer``.

    ## Clock de synchro vidéo

    ``_AudioFeed.playback_time`` — monotonic ancré au moment où OpenAL consomme
    le premier sample réel (pas au play(), pas aux bytes théoriques). Aucun drift
    lié à la latence driver. Le temps absolu est ``_loop_time_offset + feed.playback_time``.

    ## Stratégie loop

    À chaque loop :
    1. Thread décodeur finit, pose ``loop_event``, s'arrête sans mark_done.
    2. Main thread recrée un ``_NoSeekPlayer`` propre, accumule ``_loop_time_offset``.
    3. Un nouveau thread démarre avec ``pts_offset = _loop_time_offset`` pour que
       les PTS vidéo soient continus sur toute la durée de vie du player.
    4. Le prebuffer est ignoré (``_skip_prebuffer=True``) car le thread a déjà
       eu le temps de remplir le buffer pendant que l'ancien audio se terminait.
    """

    __slots__ = ("_origin", "_threads", "_sprites")

    order      = 95
    exclusive  = True
    renderable = True

    def __init__(self, origin: HasPosition) -> None:
        if __debug__:
            expect(origin, HasPosition)
        self._origin:  HasPosition                      = origin
        self._threads: dict[int, threading.Thread]      = {}
        self._sprites: dict[int, PygletTextureRenderer] = {}

    # ======================================== CONTRACT ========================================
    def __repr__(self) -> str:
        return (
            f"VideoSystem(origin={(self._origin.x, self._origin.y)}, "
            f"active={len(self._threads)})"
        )

    # ======================================== PROPERTIES ========================================
    @property
    def origin(self) -> HasPosition:
        return self._origin

    @origin.setter
    def origin(self, value: HasPosition) -> None:
        if __debug__:
            expect(value, HasPosition)
        self._origin = value

    def _video_time(self, vp: VideoPlayer) -> float:
        if vp._audio_feed is None:
            return vp._loop_time_offset
        return vp._loop_time_offset + vp._audio_feed.playback_time

    # ======================================== LIFE CYCLE ========================================
    @profile_section("world.video.update")
    def update(self, world: World, dt: float) -> None:
        active_eids: set[int] = set()

        for entity in world.query(VideoPlayer):
            vp:  VideoPlayer = entity.video_player
            tr:  Transform   = entity.transform
            eid: int         = entity.id
            active_eids.add(eid)

            if vp._video and not vp._initialized:
                self._load_player(eid, vp)

            if not vp.is_playing() or vp.is_paused():
                continue

            dist = ((tr.x - self._origin.x) ** 2 + (tr.y - self._origin.y) ** 2) ** 0.5
            spatial_volume = self._compute_volume(vp, dist)

            self._update_audio(vp, spatial_volume)
            self._check_signals(eid, vp)

            feed = vp._audio_feed
            if not vp._audio_started or feed is None or not feed.started:
                continue
            self._consume_frames(vp)

        for eid in list(self._threads):
            if eid not in active_eids:
                thread = self._threads.pop(eid)
                thread.join(timeout=1.0)

    @profile_section("world.video.draw")
    def draw(self, world: World, pipeline: Pipeline) -> None:
        for entity in world.query(VideoPlayer):
            eid = entity.id
            vp  = entity.video_player
            tr  = entity.transform

            renderer = self._sprites.get(eid)
            if renderer is None:
                self._sprites[eid] = PygletTextureRenderer(
                    texture=vp.texture, transform=tr, offset=vp.offset,
                    width=vp.width, height=vp.height,
                    opacity=vp.opacity, z=vp.z, pipeline=pipeline,
                )
            else:
                renderer.update(
                    texture=vp.texture, transform=tr, offset=vp.offset,
                    width=vp.width, height=vp.height,
                    opacity=vp.opacity, z=vp.z,
                )

    # ======================================== PLAYER LIFECYCLE ========================================
    def _load_player(self, eid: int, vp: VideoPlayer) -> None:
        was_playing = vp._playing
        self._stop_player(eid, vp)

        try:
            with av.open(vp._video.path) as c:
                vs = next((s for s in c.streams if s.type == "video"), None)
                vp._duration = float(vs.duration * vs.time_base) if (vs and vs.duration) else None
        except Exception:
            vp._duration = None

        vp._audio_player = _NoSeekPlayer()

        self._start_decode_pass(eid, vp, first=True)

        vp._initialized = True
        vp._playing     = was_playing

    def _start_decode_pass(self, eid: int, vp: VideoPlayer, *, first: bool) -> None:
        """Lance une passe de décodage (première ou loop).

        first=True  → initialise aussi la queue vidéo et les events globaux.
        first=False → réutilise queue et stop/pause events ; crée juste
                      un nouveau feed et thread pour cette passe.

        Note : le feed N'EST PAS queué ici sur le player. C'est _update_audio
        qui s'en charge au moment du prebuffer, pour éviter le double-queue.
        """
        if first:
            vp._frame_queue      = queue.Queue(maxsize=_VIDEO_BUFFER)
            vp._pending_frame    = None
            vp._stop_event       = threading.Event()
            vp._pause_event      = threading.Event()
            vp._pause_event.set()
            vp._audio_started    = False
            vp._loop_time_offset = 0.0
            vp._prev_audio_feed  = None
            vp._frames_ready     = False
            vp._audio_ready      = False

        feed = _AudioFeed(_AUDIO_RATE, _AUDIO_CH)
        feed._loop_offset    = vp._loop_time_offset
        feed._skip_prebuffer = not first
        vp._audio_feed       = feed
        # Le queue sur le player est délégué à _update_audio (via _queued flag)
        # pour éviter le double-queue qui causait le décalage aux loops.

        vp._end_event  = threading.Event()
        vp._loop_event = threading.Event()

        thread = threading.Thread(
            target=self._decode_loop,
            args=(
                vp._video.path,
                vp._frame_queue,
                feed,
                vp._stop_event,
                vp._pause_event,
                vp._end_event,
                vp._loop_event,
                vp._loop,
            ),
            daemon=True,
        )
        thread.start()
        vp._decode_thread  = thread
        self._threads[eid] = thread

    def _stop_player(self, eid: int, vp: VideoPlayer) -> None:
        vp.stop()

        if vp._decode_thread is not None:
            vp._decode_thread.join(timeout=1.0)
            vp._decode_thread = None

        for feed in (getattr(vp, "_prev_audio_feed", None), vp._audio_feed):
            if feed is not None:
                feed.mark_done()

        if vp._audio_player is not None:
            try:
                vp._audio_player.pause()
                vp._audio_player.delete()
            except Exception:
                pass
            vp._audio_player = None

        vp._audio_feed      = None
        vp._prev_audio_feed = None
        vp._decode_thread   = None
        vp._frame_queue     = None
        vp._pending_frame   = None
        vp._stop_event      = None
        vp._pause_event     = None
        vp._end_event       = None
        vp._loop_event      = None
        vp._audio_started   = False
        self._threads.pop(eid, None)

    # ======================================== SIGNALS ========================================
    def _check_signals(self, eid: int, vp: VideoPlayer) -> None:
        if vp._loop_event is not None and vp._loop_event.is_set():
            vp._loop_event.clear()
            self._prepare_loop(eid, vp)
            return

        if vp._end_event is not None and vp._end_event.is_set():
            vp._end_event.clear()
            if vp._on_end:
                vp._on_end.trigger(vp, vp._video)
            self._stop_player(eid, vp)

    def _prepare_loop(self, eid: int, vp: VideoPlayer) -> None:
        """Prépare la transition seamless vers la passe suivante."""
        if vp._decode_thread is not None:
            vp._decode_thread.join(timeout=1.0)
            vp._decode_thread = None

        # Calcul de l'offset AVANT de tuer le feed.
        # On utilise _duration (temps réel du fichier) plutôt que playback_time
        # qui est toujours en retard sur le buffer non encore consommé par OpenAL.
        if vp._duration is not None:
            vp._loop_time_offset += vp._duration
        else:
            vp._loop_time_offset = self._video_time(vp)

        if vp._audio_feed is not None:
            vp._audio_feed.mark_done()
            vp._audio_feed = None

        while True:
            try:
                vp._frame_queue.get_nowait()
            except queue.Empty:
                break
        vp._pending_frame = None

        try:
            vp._audio_player.pause()
            vp._audio_player.delete()
        except Exception:
            pass
        vp._audio_player    = _NoSeekPlayer()
        vp._audio_started   = False
        vp._prev_audio_feed = None

        vp._frames_ready = False
        vp._audio_ready  = False
        self._start_decode_pass(eid, vp, first=False)

    # ======================================== AUDIO ========================================
    def _update_audio(self, vp: VideoPlayer, spatial_volume: float) -> None:
        player = vp._audio_player
        if player is None:
            return

        if player.volume != spatial_volume:
            player.volume = spatial_volume

        if not vp._audio_started:
            if vp._audio_feed is None:
                return
            # Sur une passe de loop, le thread a déjà eu le temps de remplir
            # le buffer pendant que l'ancien audio se terminait — on démarre
            # immédiatement sans attendre _AUDIO_PREBUFFER.
            if not vp._audio_feed._skip_prebuffer:
                if vp._audio_feed.buffered_seconds < _AUDIO_PREBUFFER:
                    return
            try:
                if not vp._audio_feed._queued:
                    player.queue(vp._audio_feed)
                    vp._audio_feed._queued = True
                player.play()
                vp._audio_started = True
            except Exception:
                pass
            return

        if vp._prev_audio_feed is not None:
            vp._prev_audio_feed.mark_done()
            vp._prev_audio_feed = None

    # ======================================== FRAMES ========================================
    def _consume_frames(self, vp: VideoPlayer) -> None:
        if vp._frame_queue is None or vp._audio_feed is None:
            return

        now = self._video_time(vp)

        if vp._pending_frame is not None:
            pts, w, h, data = vp._pending_frame
            if pts > now:
                return
            self._blit_frame(vp, w, h, data)
            vp._pending_frame = None

        last_eligible: tuple | None = None
        while True:
            try:
                item = vp._frame_queue.get_nowait()
            except queue.Empty:
                break
            pts, w, h, data = item
            if pts <= now:
                last_eligible = (pts, w, h, data)
            else:
                vp._pending_frame = item
                break

        if last_eligible is not None:
            _, w, h, data = last_eligible
            self._blit_frame(vp, w, h, data)

    @staticmethod
    def _blit_frame(vp: VideoPlayer, w: int, h: int, data: bytes) -> None:
        if not vp.visible:
            return
        img = _image.ImageData(w, h, "RGB", data, pitch=-w * 3)
        if vp._texture is not None and vp._texture.width == w and vp._texture.height == h:
            vp._texture.blit_into(img, 0, 0, 0)
        else:
            vp._texture = img.get_texture()

    # ======================================== SPATIAL VOLUME ========================================
    @staticmethod
    def _compute_volume(vp: VideoPlayer, distance: float) -> float:
        base = vp.volume * vp._video.volume
        if vp.outer_radius == 0.0 or distance <= vp.inner_radius:
            return base
        if distance > vp.outer_radius:
            return 0.0
        t = (distance - vp.inner_radius) / (vp.outer_radius - vp.inner_radius)
        return base * (1.0 - vp.falloff(t))

    # ======================================== DECODE ========================================
    @staticmethod
    def _decode_loop(
        path: str,
        frame_queue: queue.Queue,
        audio_feed: _AudioFeed,
        stop_event: threading.Event,
        pause_event: threading.Event,
        end_event: threading.Event,
        loop_event: threading.Event,
        loop: bool,
    ) -> None:
        """Thread de décodage AV — une seule passe par instance.

        En mode loop : pose ``loop_event`` et s'arrête SANS mark_done.
        Le main thread appellera mark_done sur ce feed plus tard, quand
        le nouveau feed suivant sera prêt (transition seamless).

        En mode non-loop : mark_done puis end_event.
        """
        pts_offset      = audio_feed._loop_offset
        audio_resampler = av.AudioResampler(
            format="s16",
            layout="stereo",
            rate=_AUDIO_RATE,
        )

        try:
            with av.open(path) as container:
                video_stream = next((s for s in container.streams if s.type == "video"), None)
                audio_stream = next((s for s in container.streams if s.type == "audio"), None)

                if video_stream is None:
                    end_event.set()
                    return

                video_stream.thread_type = "AUTO"
                streams = [video_stream]
                if audio_stream is not None:
                    streams.append(audio_stream)

                for packet in container.demux(*streams):
                    if stop_event.is_set():
                        return
                    pause_event.wait()
                    if stop_event.is_set():
                        return

                    for frame in packet.decode():
                        if stop_event.is_set():
                            return

                        if isinstance(frame, av.VideoFrame):
                            if frame.pts is None:
                                continue
                            pts     = float(frame.pts * frame.time_base) + pts_offset
                            rgb     = frame.to_ndarray(format="rgb24")
                            h, w, _ = rgb.shape
                            data    = rgb.tobytes()
                            while not stop_event.is_set():
                                try:
                                    frame_queue.put((pts, w, h, data), timeout=0.05)
                                    break
                                except queue.Full:
                                    continue

                        elif isinstance(frame, av.AudioFrame):
                            if frame.pts is None:
                                continue
                            for rf in audio_resampler.resample(frame):
                                if rf.pts is None:
                                    continue
                                audio_feed.push(rf.to_ndarray().tobytes())

        except Exception as e:
            print(f"[decode_loop] crash: {type(e).__name__}: {e}")
            audio_feed.mark_done()
            end_event.set()
            return

        if stop_event.is_set():
            return

        if loop:
            loop_event.set()
        else:
            audio_feed.mark_done()
            end_event.set()