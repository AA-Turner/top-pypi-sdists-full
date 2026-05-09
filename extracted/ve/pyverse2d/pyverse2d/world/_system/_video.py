# ======================================== IMPORTS ========================================
from __future__ import annotations

import av
import queue
import threading
import time
import pyglet.image as _image

from ..._internal import expect, HasPosition, profile_section
from ..._rendering import PygletTextureRenderer, Pipeline
from ...abc import System
from .._world import World
from .._component import Transform, VideoPlayer

import pyglet.media as _media

# ======================================== CONSTANTS ========================================
_VIDEO_BUFFER: int = 8
_AUDIO_BUFFER: int = 16

_AUDIO_CHUNK_MS: float = 200.0

# ======================================== SYSTEM ========================================
class VideoSystem(System):
    """Système gérant les composants ``VideoPlayer``

    Args:
        origin: référentiel de position pour le falloff *(généralement la caméra)*
    """
    __slots__ = (
        "_origin",
        "_threads", "_sprites",
    )

    order = 95
    exclusive = True
    renderable = True

    def __init__(self, origin: HasPosition):
        # Vérifications
        if __debug__:
            expect(origin, HasPosition)
        
        # Attributs publiques
        self._origin: HasPosition = origin

        # Attributs internes
        self._threads: dict[int, threading.Thread] = {}
        self._sprites: dict[int, PygletTextureRenderer] = {}

    # ======================================== CONTRACT ========================================
    def __repr__(self) -> str:
        return f"VideoSystem(origin={(self._origin.x, self._origin.y)}, active={len(self._threads)})"

    # ======================================== LIFE CYCLE ========================================
    @profile_section("world.video.update")
    def update(self, world: World, dt: float) -> None:
        """Actualisation
        
        Args:
            world: ``World`` possesseur
            dt: delta-time
        """
        active_eids: set[int] = set()
        for entity in world.query(VideoPlayer):
            # Raccourcis
            vp: VideoPlayer = entity.video_player
            tr: Transform = entity.transform
            eid = entity.id
            active_eids.add(eid)

            # Démarrage du thread si nécessaire
            if vp._video and vp._initialized is False:
                self._load_player(eid, vp)

            # Vidéo chargée mais lecture non démarée
            if not vp.is_playing() or vp.is_paused():
                continue

            # Calcul du volume spatial
            distance = ((tr.x - self._origin.x) ** 2 + (tr.y - self._origin.y) ** 2) ** 0.5
            spatial_volume = self._compute_volume(vp, distance)

            # Audio OpenAL
            self._update_audio(vp, spatial_volume)

            # Consommation des frames vidéo
            self._consume_frames(vp)

            # Fin de lecture
            try:
                sentinel = vp._frame_queue.get_nowait()
                if sentinel is None:
                    # Fin réelle
                    if vp._on_end:
                        vp._on_end.trigger(vp, vp._video)
                    self._stop_player(eid, vp)
                else:
                    vp._frame_queue.put_nowait(sentinel)
            except queue.Empty:
                pass

        # Nettoyage des threads orphelins
        for eid in list(self._threads):
            if eid not in active_eids:
                thread = self._threads.pop(eid)
                thread.join(timeout=0.5)

    @profile_section("world.video.draw")
    def draw(self, world: World, pipeline: Pipeline) -> None:
        """Affichage
        
        Args:
            pipeline: ``Pipeline`` de rendu courant
        """
        for entity in world.query(VideoPlayer):
            # Raccourcis
            eid = entity.id
            vp = entity.video_player
            tr = entity.transform

            # Synchronisation des sprites
            renderer = self._sprites.get(eid)
            if renderer is None:
                self._sprites[eid] = PygletTextureRenderer(
                    texture = vp.texture,
                    transform = tr,
                    offset = vp.offset,
                    width = vp.width,
                    height = vp.height,
                    opacity = vp.opacity,
                    z = vp.z,
                    pipeline = pipeline,
                )
            
            else:
                renderer.update(
                    texture = vp.texture,
                    transform = tr,
                    offset = vp.offset,
                    width = vp.width,
                    height = vp.height,
                    opacity = vp.opacity,
                    z = vp.z,
                )

    # ======================================== INTERFACE ========================================
    def _load_player(self, eid: int, vp: VideoPlayer) -> None:
        """Initialise les queues et démarre le thread de décodage

        Args:
            eid: identifiant de l'entité
            vp: composant ``VideoPlayer``
        """
        # Nettoyage de l'ancien état si besoin
        was_playing = vp._playing
        self._stop_player(eid, vp)

        # Récupération de la durée
        try:
            with av.open(vp._video.path) as c:
                vs = next((s for s in c.streams if s.type == "video"), None)
                vp._duration = float(vs.duration * vs.time_base) if (vs and vs.duration) else None
        except Exception:
            vp._duration = None

        # Queues
        vp._frame_queue = queue.Queue(maxsize=_VIDEO_BUFFER)
        vp._audio_queue = queue.Queue(maxsize=_AUDIO_BUFFER)
        vp._audio_ready_queue = queue.Queue(maxsize=_AUDIO_BUFFER)

        # Events
        vp._stop_event = threading.Event()
        vp._pause_event = threading.Event()
        vp._pause_event.set()

        # Audio
        vp._audio_player = _media.Player()

        # Clock
        vp._pts_origin = 0.0
        vp._clock_origin = time.perf_counter()

        # Lancement du thread de décodage
        thread = threading.Thread(
            target=self._decode_loop,
            args=(vp._video.path, vp._frame_queue, vp._audio_queue, vp._stop_event, vp._pause_event, vp._loop),
            daemon=True,
        )
        thread.start()
        vp._decode_thread = thread
        self._threads[eid] = thread

        # Lancement du thread de construction audio
        audio_thread = threading.Thread(
            target=self._audio_build_loop,
            args=(vp._audio_queue, vp._audio_ready_queue, vp._stop_event),
            daemon=True,
        )
        audio_thread.start()
        vp._audio_thread = audio_thread

        # Fin d'initialisation
        vp._initialized = True
        vp._playing = was_playing

    def _stop_player(self, eid: int, vp: VideoPlayer) -> None:
        """Signale l'arrêt et join le thread

        Args:
            eid: identifiant de l'entité
            vp: composant ``VideoPlayer``
        """
        vp.stop()
        for thread in (vp._decode_thread, vp._audio_thread):
            if thread is not None:
                thread.join(timeout=1.0)
        vp._decode_thread = None
        vp._audio_thread = None
        vp._frame_queue = None
        vp._audio_queue = None
        vp._stop_event = None
        vp._pause_event = None
        self._threads.pop(eid, None)

    # ======================================== FRAMES ========================================
    def _consume_frames(self, vp: VideoPlayer) -> None:
        """Dépile les frames prêtes et met à jour la texture

        Args:
            vp: composant ``VideoPlayer``
        """
        # Fast exit
        if vp._frame_queue is None:
            return

        # Paramètres
        now = vp.time
        last_ready = None
        last_pts: float = 0.0
        last_size: tuple[int, int] = (0, 0)

        # Consommation des frames
        while True:
            try:
                pts, w, h, data = vp._frame_queue.get_nowait()
            except queue.Empty:
                break

            if pts <= now:
                last_ready = data
                last_pts = pts
                last_size = (w, h)
            else:
                try:
                    vp._frame_queue.put_nowait((pts, w, h, data))
                except queue.Full:
                    pass
                break

        # Pas de frame prête
        if last_ready is None:
            return

        # Création de la texture pyglet
        w, h = last_size
        img = _image.ImageData(w, h, "RGB", last_ready, pitch=-w * 3)
        vp._texture = img.get_texture()
        vp._pts_origin = last_pts
        vp._clock_origin = time.perf_counter()

    # ======================================== AUDIO ========================================
    def _update_audio(
        self,
        vp: VideoPlayer,
        spatial_volume: float,
    ) -> None:
        """Consomme la queue audio et joue via pyglet OpenAL avec volume spatial

        Args:
            vp: composant ``VideoPlayer``
            spatial_volume: volume calculé selon la distance
        """
        # Fast exit
        if vp._audio_queue is None:
            return

        # Mise à jour du lecteur audio
        player: _media.Player = vp._audio_player
        if spatial_volume != player.volume:
            player.volume = spatial_volume

        # Injecte les sources prêtes
        while True:
            try:
                source = vp._audio_ready_queue.get_nowait()
            except queue.Empty:
                break

            try:
                player.queue(source)
            except Exception:
                pass

        # Démarrage lazy
        try:
            if not player.playing:
                player.play()
        except Exception:
            pass

    # ======================================== VOLUME SPATIAL ========================================
    @staticmethod
    def _compute_volume(vp: VideoPlayer, distance: float) -> float:
        """Calcule le volume en fonction de la distance et du falloff

        Args:
            vp: composant ``VideoPlayer``
            distance: distance spatiale
        """
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
        audio_queue: queue.Queue,
        stop_event: threading.Event,
        pause_event: threading.Event,
        loop: bool,
    ) -> None:
        """Thread de décodage AV

        Args:
            path: chemin vers le fichier vidéo
            frame_queue: queue des frames RGB (pts, w, h, bytes)
            audio_queue: queue des chunks audio (pts, sample_rate, channels, bytes)
            stop_event: signal d'arrêt
            pause_event: signal de pause (set = lecture, clear = pause)
            loop: reboucle si True
        """
        while not stop_event.is_set():
            try:
                with av.open(path) as container:
                    # Avancement des générateurs
                    video_stream = next((s for s in container.streams if s.type == "video"), None)
                    audio_stream = next((s for s in container.streams if s.type == "audio"), None)

                    # Fin de lecture
                    if video_stream is None:
                        break

                    video_stream.thread_type = "AUTO"
                    streams = [video_stream]
                    if audio_stream is not None:
                        streams.append(audio_stream)

                    # Resampler audio (lazy init sur la vraie géométrie du flux)
                    audio_resampler = None

                    for packet in container.demux(*streams):
                        if stop_event.is_set():
                            return

                        pause_event.wait()
                        if stop_event.is_set():
                            return

                        for frame in packet.decode():
                            if stop_event.is_set():
                                return

                            if frame.__class__.__name__ == "VideoFrame":
                                if frame.pts is None:
                                    continue

                                pts = float(frame.pts * frame.time_base)
                                rgb = frame.to_ndarray(format="rgb24")
                                h, w, _ = rgb.shape
                                data = rgb.tobytes()

                                while not stop_event.is_set():
                                    try:
                                        frame_queue.put((pts, w, h, data), timeout=0.05)
                                        break
                                    except queue.Full:
                                        continue

                            elif frame.__class__.__name__ == "AudioFrame":
                                if frame.pts is None:
                                    continue

                                # Initialisation lazy du resampler
                                if audio_resampler is None:
                                    layout = (
                                        "stereo"
                                        if len(frame.layout.channels) >= 2
                                        else "mono"
                                    )

                                    audio_resampler = av.AudioResampler(
                                        format="s16",
                                        layout=layout,
                                        rate=frame.sample_rate,
                                    )

                                # resample() peut retourner plusieurs frames
                                for rf in audio_resampler.resample(frame):
                                    if rf.pts is None:
                                        continue

                                    pts = float(rf.pts * rf.time_base)
                                    data = bytes(rf.planes[0])

                                    try:
                                        audio_queue.put_nowait(
                                            (
                                                pts,
                                                rf.sample_rate,
                                                len(rf.layout.channels),
                                                data,
                                            )
                                        )
                                    except queue.Full:
                                        pass

            except Exception as e:
                print(f"[decode_loop] crash: {type(e).__name__}: {e}")
                break

            # Fin de lecture
            if not loop or stop_event.is_set():
                if not stop_event.is_set():
                    try:
                        frame_queue.put(None, timeout=1.0)
                    except queue.Full:
                        pass
                break
    
    @staticmethod
    def _audio_build_loop(
        audio_queue: queue.Queue,
        ready_queue: queue.Queue,
        stop_event: threading.Event,
    ) -> None:
        """Thread de préconstruction des sources audio pyglet
        
        Args:
            audio_queue: queue des chunks audio (pts, sample_rate, channels, bytes)
            ready_queue: queue des sources prêtes
            stop_event: signal d'arrêt
        """
        # Configuration de la construction
        pcm_buffer = bytearray()
        sample_rate = 48000
        channels = 2
        bytes_per_sample = 2
        bytes_per_second = sample_rate * channels * bytes_per_sample
        target_size = int(bytes_per_second * (_AUDIO_CHUNK_MS / 1000.0))

        # Boucle de construction
        while not stop_event.is_set():
            try:
                pts, sr, ch, data = audio_queue.get(timeout=0.05)
            except queue.Empty:
                continue

            # Recalcul si le format change
            if sr != sample_rate or ch != channels:
                sample_rate = sr
                channels = ch
                bytes_per_second = sample_rate * channels * bytes_per_sample
                target_size = int(bytes_per_second * (_AUDIO_CHUNK_MS / 1000.0))
                pcm_buffer.clear()

            pcm_buffer.extend(data)

            # Pas assez de PCM accumulé
            if len(pcm_buffer) < target_size:
                continue

            chunk = bytes(pcm_buffer[:target_size])
            del pcm_buffer[:target_size]

            try:
                audio_format = _media.codecs.AudioFormat(
                    channels=channels,
                    sample_size=16,
                    sample_rate=sample_rate,
                )
                source = _media.codecs.StaticMemorySource(
                    chunk,
                    audio_format,
                )
                ready_queue.put(source, timeout=0.1)

            except Exception:
                continue