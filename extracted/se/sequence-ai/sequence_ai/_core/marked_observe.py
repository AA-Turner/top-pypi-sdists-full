"""
The observation format on the robot: observe() data that holds markers
(sequence_ai.Video, Depth, Tactile) has each marked item replaced by the map its encoder writes
(sequence_base.codec.marked) before it is packed, so the worker can turn it back; data with no marker is packed as it
always was.

In one sentence: observe(x) → each marker in x, by its path (keys and indices from the top), goes to its encoder - one
an item of each worker-side episode, its stream's frames numbered, a keyframe every second - and the map it writes
takes the marker's place → the frame is packed and numbered as any other → what breaks a stream at the worker forces a
keyframe: a reconnect, a worker missing frames (frames_missing), frames it refused to keep (left out); frames encoded
before the refusal, which the worker could no longer decode, go as left out with it.

WHY one encoder set per worker-side episode: an episode the platform starts anew (a copy that stopped, another worker)
is a fresh decoder at the worker, whose first frame must be a keyframe - a new episode id, new encoders, so it is.
WHY imported only for a marker: sequence_base and the encoders need Python 3.10; a robot that marks
nothing needs neither, and this core stays 3.9 and httpx-only.
"""
from __future__ import annotations

import collections
import threading
import weakref
from typing import Any, Callable, Optional

from ..errors import InvalidRequest, MissingPackage
from ..markers import _Marked
from . import observe_stream as _observe
from .warn import warn

_EPISODES_KEPT = 8
_NEEDS = ("the observation format's markers (sequence_ai.Video, Depth, Tactile) need Python 3.10 or later and their "
          "encoders")
_INSTALL = "pip install -U sequence-ai, on Python 3.10 or later (3.11 or later on Windows on ARM)"


PICTURES = ("keyframes", "exact")
PICTURE_MIN_SIDE = 32


class _Picture(_Marked):
    """An unmarked camera picture (HxWx3 uint8, each side PICTURE_MIN_SIDE or more), as connect(pictures="keyframes")
    sends it: a video keyframe of its own, never a frame another is decoded from."""

    kind = "video"
    __slots__ = ()


def is_picture(value: Any) -> bool:
    """Whether `value` is an unmarked camera picture: a numpy array HxWx3 of uint8, each side PICTURE_MIN_SIDE or more."""
    shape = getattr(value, "shape", None)
    return (type(value).__name__ == "ndarray" and str(getattr(value, "dtype", "")) == "uint8" and shape is not None
            and len(shape) == 3 and shape[2] == 3 and min(shape[0], shape[1]) >= PICTURE_MIN_SIDE)


def _holds_picture(value: Any) -> bool:
    if is_picture(value):
        return True
    if isinstance(value, dict):
        return any(_holds_picture(v) for v in value.values())
    if isinstance(value, (list, tuple)):
        return any(_holds_picture(v) for v in value)
    return False


def _pictures_marked(value: Any) -> Any:
    """`value` with each unmarked picture in it - in dicts, lists and tuples - marked to go as a keyframe of its own."""
    if is_picture(value):
        return _Picture(value)
    if isinstance(value, dict):
        return {k: _pictures_marked(v) for k, v in value.items()} if _holds_picture(value) else value
    if isinstance(value, (list, tuple)):
        return [_pictures_marked(v) for v in value] if _holds_picture(value) else value
    return value


def _keyframes(conn: Any, inputs: Any) -> Any:
    """`inputs` as connect(pictures=) sends them: with "keyframes", the default, each unmarked picture marked to go as a
    keyframe of its own - as it is, said once a connection, where this machine has no encoder for it."""
    if getattr(conn, "pictures", "keyframes") != "keyframes" or not _holds_picture(inputs):
        return inputs
    if not _can_encode():
        if not conn.__dict__.get("_pictures_said"):
            conn.__dict__["_pictures_said"] = True
            warn("observe(): pictures go as they are, every byte of them: sending each as a video keyframe, "
                 f"connect()'s default, needs Python 3.10 or later and the encoders: {_INSTALL}")
        return inputs
    return _pictures_marked(inputs)


_ENCODES: list = []


def _can_encode() -> bool:
    """Whether a picture can go as video here: sequence-base's encoders and PyAV installed - looked up once, PyAV not
    imported (its first import takes seconds)."""
    if not _ENCODES:
        import importlib.util

        try:
            _codec()
            here = importlib.util.find_spec("av") is not None
        except (MissingPackage, ImportError, ValueError):
            here = False
        _ENCODES.append(here)
    return _ENCODES[0]


_WARM: list = []
_WARM_LOCK = threading.Lock()


def warm() -> threading.Event:
    """The encoders a first picture loads - sequence-base's codec, PyAV and the H.264 encoder it opens - loaded now, on a
    thread of their own, once a process: the event set when they are, or are found missing here (which that first
    picture then says, as it would have). wait_until_ready() waits for it, so the robot's first act does not.
    WHY: PyAV's first import after its install loads its own libraries for the first time, and a first observe() of a
    picture paid that inside the robot's first act - 20.8 s in a fresh venv on a Mac mini, 20.1 s installed with
    --compile-bytecode (so not the bytecode), 0.25 s in every process after.

"""
    with _WARM_LOCK:
        if _WARM:
            return _WARM[0]
        done = threading.Event()
        _WARM.append(done)

    def load() -> None:
        try:
            if _can_encode():
                import numpy as np

                _codec().encoder("video").encode(np.zeros((PICTURE_MIN_SIDE, PICTURE_MIN_SIDE, 3), np.uint8))
        except Exception:
            return
        finally:
            done.set()

    threading.Thread(target=load, daemon=True, name="seq-encoders").start()
    return done


def holds(value: Any) -> bool:
    """Whether `value` holds a marker, in dicts, lists and tuples at any depth."""
    if isinstance(value, _Marked):
        return True
    if isinstance(value, dict):
        return any(holds(v) for v in value.values())
    if isinstance(value, (list, tuple)):
        return any(holds(v) for v in value)
    return False


def _codec():
    try:
        from sequence_base.codec import marked
    except ImportError:
        raise MissingPackage(_NEEDS, hint=_INSTALL) from None
    return marked


class Marked:
    """One connection's encoders, by worker-side episode and item path, and which numbers of each episode hold video."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._encoders: "collections.OrderedDict[str, dict]" = collections.OrderedDict()
        self._epoch: dict = {}
        self._video: dict = {}

    def encode(self, episode: str, value: Any) -> "tuple[Any, bool, int]":
        """`value` with each marker replaced by its encoder's map; whether a video item is among them; and the
        episode's epoch it was encoded at, which current() checks."""
        marked = _codec()
        with self._lock:
            encoders = self._encoders.get(episode)
            if encoders is None:
                encoders = self._encoders[episode] = {}
                while len(self._encoders) > _EPISODES_KEPT:
                    gone, _ = self._encoders.popitem(last=False)
                    self._epoch.pop(gone, None)
                    self._video.pop(gone, None)
            else:
                self._encoders.move_to_end(episode)
            epoch = self._epoch.get(episode, 0)
        video = []

        def one(path: tuple, m: _Marked) -> Any:
            where = "/".join(str(p) for p in path) or "the observation"
            try:
                with self._lock:
                    enc = encoders.get(path)
                    if enc is None or enc.kind != m.kind:
                        enc = encoders[path] = marked.encoder(m.kind)
                if isinstance(m, _Picture):
                    enc.force_keyframe()
                wire = enc.encode(m.value)
            except marked.MarkedError as exc:
                raise InvalidRequest(f"observe(): {where}: {exc}") from None
            except ImportError as exc:


                raise MissingPackage(f"observe(): {where}: a {m.kind} item is encoded with {exc.name or exc}, which "
                                     "this machine lacks", hint=_INSTALL) from None
            if wire.get("codec") == "h264" and not isinstance(m, _Picture):
                video.append(path)
            return wire

        return _replaced(value, (), one), bool(video), epoch

    def current(self, episode: str, epoch: int) -> bool:
        """Whether no keyframe was forced for `episode` since `epoch`: a frame encoded before one goes again."""
        with self._lock:
            return self._epoch.get(episode, 0) == epoch

    def note(self, episode: str, number: int, video: bool) -> None:
        if video:
            with self._lock:
                self._video.setdefault(episode, set()).add(number)

    def has_video(self, episode: str) -> bool:
        """Whether `episode` has a frame that holds video: one its worker decodes from the frames before it."""
        with self._lock:
            return bool(self._video.get(episode))

    def force(self, episode: Optional[str] = None) -> None:
        """The next video frame of `episode` - of every episode, None - a keyframe."""
        with self._lock:
            for e in ([episode] if episode is not None else list(self._encoders)):
                for enc in (self._encoders.get(e) or {}).values():
                    enc.force_keyframe()
                self._epoch[e] = self._epoch.get(e, 0) + 1

    def left_out(self, episode: str, numbers: "set[int]") -> "set[int]":
        """The worker refused frames `numbers` of `episode`: its keyframes forced, and the numbers after them that hold
        video - encoded before the refusal, so following frames the worker never had - to go as left out as well."""
        self.force(episode)
        with self._lock:
            later = {n for n in self._video.get(episode, ()) if n > max(numbers)} if numbers else set()
        return later


def packed(conn: Any, inputs: Any, episode_id: str, squeeze: Any = None) -> "tuple[bytes, Optional[_Pending]]":
    """observe()'s packing: data with markers encoded for the episode's worker-side id and packed (and a _Pending to
    settle once it is numbered), anything else packed as it always was - its large arrays and bytes compressed where
    that pays, and its blocks cut (`squeeze`: blocks.Cut, compress.Squeeze); its unmarked pictures as connect(pictures=)
    says (_keyframes). ValueError (msgpack's) as _observe.packed."""
    inputs = _keyframes(conn, inputs)
    if not holds(inputs):
        return _observe.packed(inputs if squeeze is None else squeeze.apply(inputs)), None
    marks = of(conn)
    with conn._lock:
        episode = _worker_side(conn, episode_id)
    encoded, video, epoch = marks.encode(episode, inputs)
    return (_observe.packed(encoded if squeeze is None else squeeze.apply(encoded)),
            _Pending(marks, inputs, episode, video, epoch, squeeze, encoded))


class _Pending:
    """A marked observation encoded outside the connection's lock, settled under it once numbered (settle)."""

    def __init__(self, marks: Marked, inputs: Any, episode: str, video: bool, epoch: int, squeeze: Any = None,
                 encoded: Any = None) -> None:
        self._marks, self._inputs, self._episode, self._video, self._epoch = marks, inputs, episode, video, epoch
        self._squeeze = squeeze


        self.encoded = encoded

    def settle(self, conn: Any, episode_id: str, number: int, packed_frame: bytes) -> bytes:
        """Under the connection's lock: the frame as it goes - encoded again when its episode moved on to another id or
        had a keyframe forced while it was encoded (rare: its first frame there is then a keyframe) - its number
        noted."""
        episode = _worker_side(conn, episode_id)
        if episode != self._episode or not self._marks.current(episode, self._epoch):
            encoded, self._video, _ = self._marks.encode(episode, self._inputs)
            self.encoded = encoded
            packed_frame = _observe.packed(encoded if self._squeeze is None else self._squeeze.apply(encoded))
        self._marks.note(episode, number, self._video)
        return packed_frame


def of(conn: Any) -> Marked:
    """The connection's encoders, made at its first marked observation."""
    marks = conn.__dict__.get("_marked")
    if marks is None:
        marks = conn.__dict__.setdefault("_marked", Marked())
    return marks


def left_out_of(conn: Any) -> "Callable[[str, set], set]":
    """The stream's on_left_out for `conn`: nothing more left out for a connection that marked nothing. It holds `conn`
    weakly: the stream's thread holds it, and a connection the robot dropped without close() must still be collected,
    so its finalizer gives its seat back (seat._give_back)."""
    ref = weakref.ref(conn)

    def on_left_out(episode: str, numbers: "set[int]") -> "set[int]":
        held = ref()
        marks = held.__dict__.get("_marked") if held is not None else None
        return marks.left_out(episode, numbers) if marks is not None else set()
    return on_left_out


def video_of(conn: Any) -> "Callable[[str], bool]":
    """Whether an episode's frames hold video (Marked.has_video), for the robot's stream, which never leaves out a frame
    of one as stale (observe_stream._newest): the frames after it are decoded from it. `conn` held weakly, as
    left_out_of holds it."""
    ref = weakref.ref(conn)

    def video(episode: str) -> bool:
        held = ref()
        marks = held.__dict__.get("_marked") if held is not None else None
        return bool(marks is not None and marks.has_video(episode))
    return video


def force(conn: Any, episode: Optional[str] = None) -> None:
    """A reconnect (every episode), or a worker missing frames of `episode`: its next video frame a keyframe."""
    marks = conn.__dict__.get("_marked")
    if marks is not None:
        marks.force(episode)


def _worker_side(conn: Any, episode_id: str) -> str:
    return conn._worker_episode if episode_id == conn._caller_episode and conn._worker_episode else episode_id


def _replaced(value: Any, path: tuple, fn: "Callable[[tuple, _Marked], Any]") -> Any:
    if isinstance(value, _Marked):
        return fn(path, value)
    if isinstance(value, dict):
        return {k: _replaced(v, path + (k,), fn) for k, v in value.items()} if holds(value) else value
    if isinstance(value, (list, tuple)):
        return [_replaced(v, path + (i,), fn) for i, v in enumerate(value)] if holds(value) else value
    return value
