"""
An observation's large arrays and bytes compressed before they go up - losslessly, and only where that saves more upload
time than it costs - which its worker turns back as each post comes (sequence-base codec.compressed), so its policy is handed the bytes the robot built.




In one sentence: observe() → each unmarked numpy array or bytes of MIN_BYTES or more, by its path in the observation →
compressed with zstd level 1 (Python 3.14's compression.zstd, or zstandard where it is installed; else zlib level 1)
while what it saves at the uplink's rate - measured from this connection's own posts (Uplink) - is more than the robot's
time compressing it and the worker's turning it back → in its place the map codec.compressed reads → a path whose bytes
compress less than POOR times goes as it is for its next PAUSE observations, and so does one where compressing stopped
paying; then it is tried again.

WHY by path: whether something compresses is what it is - a camera's frames do, a JPEG's bytes never do - and a path is
the same thing every observation.
WHY measured from the posts: the link is the robot's own and changes as it moves; a post's time less the least time a
small post took is what its bytes cost to carry. Posts on their way at once share the link, so each looks slower than the
link is: a rate measured so errs towards compressing, which costs a robot about a millisecond a megabyte.
WHY tried again: a link speeds up and slows down, and a camera's scene changes; a path paused is looked at anew.
"""
from __future__ import annotations

import sys
import threading
import time
import zlib
from typing import Any, Callable, Optional


MARK, KIND, VERSION = "__seq__", "compressed", 1
MIN_BYTES = 16 * 1024
POOR = 1.05
PAUSE = 64
RATE_S = 6e6

SMALL, LARGE = 16 * 1024, 64 * 1024


UNPACK_S = {"zstd": 1.3e-9, "zlib": 1.6e-9}

PACK_S = {"zstd": 2.2e-9, "zlib": 1.0e-8}
_PATHS_KEPT = 1024

_SIGN = b"\xaa" + KIND.encode()


def _codec() -> "tuple[str, Callable[[bytes], bytes], Callable[[bytes, int], bytes]]":
    """The codec this robot has - (name, compress, decompress) - zstd where Python or an installed package has it."""
    try:
        from compression import zstd

        return "zstd", (lambda b: zstd.compress(b, level=1)), (lambda b, n: zstd.decompress(b))
    except ImportError:
        pass
    try:
        import zstandard

        return ("zstd", (lambda b: zstandard.ZstdCompressor(level=1).compress(b)),
                (lambda b, n: zstandard.ZstdDecompressor().decompress(b, max_output_size=n)))
    except ImportError:
        return "zlib", (lambda b: zlib.compress(b, 1)), (lambda b, n: zlib.decompress(b))


class Uplink:
    """This connection's upload rate, bytes a second, from its own posts' sizes and times (the module's docstring)."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._floor: Optional[float] = None
        self._rate: Optional[float] = None

    def note(self, size: int, seconds: float) -> None:
        """A post of `size` bytes was answered `seconds` after it went."""
        with self._lock:
            if size < SMALL:
                self._floor = seconds if self._floor is None else min(self._floor, seconds)
            elif size >= LARGE:
                carried = seconds - (self._floor or 0.0)
                if carried > 1e-3:
                    sample = size / carried
                    self._rate = sample if self._rate is None else 0.7 * self._rate + 0.3 * sample

    def rate(self) -> float:
        with self._lock:
            return self._rate if self._rate is not None else RATE_S


class _Path:
    __slots__ = ("ratio", "until")

    def __init__(self) -> None:
        self.ratio: Optional[float] = None
        self.until = 0


class Squeeze:
    """One connection's compressing of its observations (the module's docstring): its codec, its uplink, and what each
    path last did."""

    def __init__(self) -> None:
        self.codec, self._pack, self._unpack = _codec()
        self.uplink = Uplink()
        self._lock = threading.Lock()
        self._paths: "dict[tuple, _Path]" = {}
        self._seen = 0
        self._pack_s = PACK_S[self.codec]
        self.used = False

    def apply(self, value: Any) -> Any:
        """`value` - an observation, its markers encoded - with each large array or bytes that pays compressed: the
        same objects where nothing is."""
        with self._lock:
            self._seen += 1
            if len(self._paths) > _PATHS_KEPT:
                self._paths.clear()
            return self._walk(value, ())

    def _walk(self, value: Any, path: tuple) -> Any:
        if isinstance(value, dict):
            if MARK in value:
                return value
            out = {k: self._walk(v, path + (k,)) for k, v in value.items()}
            return out if any(out[k] is not value[k] for k in value) else value
        if isinstance(value, (list, tuple)):
            out = [self._walk(v, path + (i,)) for i, v in enumerate(value)]
            return out if any(a is not b for a, b in zip(out, value)) else value
        raw, extra = _raw(value)
        if raw is None or len(raw) < MIN_BYTES:
            return value
        return self._maybe(path, value, raw, extra)

    def _maybe(self, path: tuple, value: Any, raw: bytes, extra: dict) -> Any:
        state = self._paths.get(path)
        if state is None:
            state = self._paths[path] = _Path()
        if self._seen < state.until:
            return value
        if state.ratio is not None and not state.until and not self._pays(state.ratio):
            state.until = self._seen + PAUSE
            return value

        state.until = 0
        t0 = time.perf_counter()
        data = self._pack(raw)
        self._pack_s = 0.8 * self._pack_s + 0.2 * (time.perf_counter() - t0) / len(raw)
        state.ratio = len(raw) / max(1, len(data))
        if state.ratio < POOR:
            state.until = self._seen + PAUSE
            return value
        self.used = True
        return dict([(MARK, KIND), ("v", VERSION), ("codec", self.codec), ("n", len(raw)), *extra.items(),
                     ("data", data)])

    def content(self, path: tuple, data: bytes) -> Any:
        """A block's content as it goes on its post (blocks.py; observe_stream): compressed where that pays, as an
        item at `path` of its observation would be - its compressed item - else as it is."""
        with self._lock:
            return self._maybe(path, data, bytes(data), {})

    def _pays(self, ratio: float) -> bool:
        """Whether a byte that compresses `ratio` times saves more upload time than it costs to compress and to turn
        back."""
        return (1.0 - 1.0 / ratio) / self.uplink.rate() > self._pack_s + UNPACK_S[self.codec]


def _raw(value: Any) -> "tuple[Optional[bytes], dict]":
    """The bytes a value carries and what turns them back: an array's data with its type and shape, bytes as they are;
    (None, {}) for anything else."""
    if isinstance(value, (bytes, bytearray, memoryview)):
        return bytes(value), {}
    np = sys.modules.get("numpy")
    if np is not None and isinstance(value, np.ndarray) and not (value.dtype.hasobject or value.dtype.kind in "OV"):
        return np.ascontiguousarray(value).tobytes(), {"type": value.dtype.str, "shape": list(value.shape)}
    return None, {}


def _value(item: dict, raw: bytes) -> Any:
    if "type" not in item:
        return raw
    import numpy as np

    return np.frombuffer(raw, dtype=np.dtype(item["type"])).reshape(item["shape"])


def of(conn: Any) -> Squeeze:
    """The connection's Squeeze, made at first use."""
    squeeze = conn.__dict__.get("_squeeze")
    if squeeze is None:
        squeeze = conn.__dict__.setdefault("_squeeze", Squeeze())
    return squeeze
