# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
An observation's large arrays and bytes, compressed before upload: losslessly, and only where that saves more upload
time than it costs. The server decompresses each one as it arrives (compressed.py), so the policy receives the bytes the
robot built.

    from sequence_ai.network import compress, msgpack_io

    squeeze = compress.Squeeze()                                  # one per connection
    body = msgpack_io.pack(squeeze.apply(observation))            # large arrays compressed in place, if that saves time
    squeeze.uplink.note(len(body), seconds_the_upload_took)       # so it learns this link's upload rate

In one sentence: apply() → each numpy array or bytes of MIN_BYTES or more, identified by its path in the observation →
compressed with zstd level 1 (Python 3.14's compression.zstd, or zstandard where it is installed; else zlib level 1)
while the upload time it saves at the uplink's rate, measured from this connection's own uploads (Uplink), exceeds the
robot's time to compress it plus the server's time to decompress it → replaced by the map compressed.expand reads → a
path whose bytes compress by a factor below POOR is sent uncompressed for its next PAUSE observations, and so is one
where compression stopped saving time; then it is tried again.

WHY by path: whether data compresses depends on what it is (a camera's raw frames do, a JPEG's bytes do not), and a path
holds the same kind of data in every observation.
WHY only where it saves time: on a fast link, compressing and decompressing take longer than the upload time they save.
Camera frames of 172,800 bytes took 0.37 ms to compress with zstd level 1 and 0.21 ms to decompress, and came out about
1.9 times smaller.
"""
from __future__ import annotations

import sys
import threading
import time
import zlib
from typing import Any, Callable, Collection, Optional

MARK, KIND, VERSION = "__seq__", "compressed", 1   # the map compressed.expand reads
MIN_BYTES = 16 * 1024      # smaller values are sent uncompressed: compressing a few kilobytes costs more than it saves
POOR = 1.05                # a compression ratio below this is not worth sending compressed
PAUSE = 64                 # how many observations a path is sent uncompressed before it is tried again
RATE_S = 6e6               # the uplink's rate in bytes per second, until this connection has measured its own (about
                           # 6 MB/s, measured from a robot on a home connection)
SMALL, LARGE = 16 * 1024, 64 * 1024   # a POST this small measures the RTT alone; one this large, the cost per byte
# the server's time to decompress one byte, by codec (measured on real DROID frames of 172,800 bytes: 0.21 ms
# with zstd, 0.26 ms with zlib)
UNPACK_S = {"zstd": 1.3e-9, "zlib": 1.6e-9}
# the robot's time to compress one byte, until it has timed its own (the same frames: 0.37 ms with zstd level 1,
# 1.69 ms with zlib level 1)
PACK_S = {"zstd": 2.2e-9, "zlib": 1.0e-8}
_PATHS_KEPT = 1024         # paths remembered before the table is cleared: bounds keys that are new in every observation
# what a packed body that holds a compressed item contains: the str "compressed" as msgpack writes it
_SIGN = b"\xaa" + KIND.encode()


def _codec(allowed: "Optional[Collection[str]]" = None
           ) -> "Optional[tuple[str, Callable[[bytes], bytes], Callable[[bytes, int], bytes]]]":
    """The codec available on this robot, as (name, compress, decompress): zstd where Python or an installed package
    provides it, else zlib - of those in `allowed` (the codecs its server reads; None: either). None when none of them
    is available."""
    if allowed is None or "zstd" in allowed:
        try:
            from compression import zstd  # type: ignore[import-not-found]   # Python 3.14

            return "zstd", (lambda b: zstd.compress(b, level=1)), (lambda b, n: zstd.decompress(b))
        except ImportError:
            pass
        try:
            import zstandard  # type: ignore[import-not-found]

            return ("zstd", (lambda b: zstandard.ZstdCompressor(level=1).compress(b)),
                    (lambda b, n: zstandard.ZstdDecompressor().decompress(b, max_output_size=n)))
        except ImportError:
            pass
    if allowed is None or "zlib" in allowed:
        return "zlib", (lambda b: zlib.compress(b, 1)), (lambda b, n: zlib.decompress(b))
    return None


def codec_for(reads: "Collection[str]") -> Optional[str]:
    """The codec this robot would compress with for a server that reads the codecs in `reads` ("zstd", "zlib"): zstd
    where both have it, else zlib where the server reads it; None when they share none."""
    found = _codec(reads)
    return found[0] if found is not None else None


class Uplink:
    """This connection's upload rate in bytes per second, estimated from the sizes and times of its own POSTs (the
    module's docstring)."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._floor: Optional[float] = None       # the shortest time a small POST took: the RTT with almost no payload
        self._rate: Optional[float] = None        # a moving average of the upload rate measured on large POSTs

    def note(self, size: int, seconds: float) -> None:
        """Record that a POST of `size` bytes received its response `seconds` after it was sent."""
        with self._lock:
            if size < SMALL:
                self._floor = seconds if self._floor is None else min(self._floor, seconds)
            elif size >= LARGE:
                carried = seconds - (self._floor or 0.0)
                if carried > 1e-3:
                    sample = size / carried
                    self._rate = sample if self._rate is None else 0.7 * self._rate + 0.3 * sample

    def rate(self) -> float:
        """The link's upload rate in bytes per second: measured from its large POSTs, or RATE_S until one has been
        measured."""
        with self._lock:
            return self._rate if self._rate is not None else RATE_S


class _Path:
    __slots__ = ("ratio", "until")

    def __init__(self) -> None:
        self.ratio: Optional[float] = None    # its last compression ratio: bytes before / bytes after
        self.until = 0                        # the observation count before which it is sent uncompressed


class Squeeze:
    """Compression state for one connection's observations (the module's docstring): its codec, its uplink estimate, and
    each path's last result."""

    def __init__(self, codecs: "Optional[Collection[str]]" = None) -> None:
        """`codecs`: the codecs the server reads, as its X-Seq-Reads names them (None: either). ValueError when this
        robot has none of them."""
        found = _codec(codecs)
        if found is None:
            raise ValueError(f"no codec this robot has is one the server reads ({', '.join(sorted(codecs or ()))})")
        self.codec, self._pack, self._unpack = found
        self.uplink = Uplink()
        self._lock = threading.Lock()
        self._paths: "dict[tuple, _Path]" = {}
        self._seen = 0                        # observations so far
        self._pack_s = PACK_S[self.codec]     # a moving average of this robot's time to compress one byte
        self.used = False                     # whether any item has been sent compressed

    def apply(self, value: Any) -> Any:
        """Return `value`, an observation, with each large array or bytes that is worth compressing replaced by its
        compressed item. A map that already carries the reserved key is left unchanged, and where nothing is compressed
        the same objects are returned."""
        with self._lock:
            self._seen += 1
            if len(self._paths) > _PATHS_KEPT:
                self._paths.clear()
            return self._walk(value, ())

    def _walk(self, value: Any, path: tuple) -> Any:
        if isinstance(value, dict):
            if MARK in value:
                return value                  # a map that already carries the reserved key: left unchanged
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
        # compressed the first time, while it saves time, and once after each pause, which measures its ratio again
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

    def _pays(self, ratio: float) -> bool:
        """Whether data that compresses by a factor of `ratio` saves more upload time per byte than it takes to compress
        and decompress."""
        return (1.0 - 1.0 / ratio) / self.uplink.rate() > self._pack_s + UNPACK_S[self.codec]


def _raw(value: Any) -> "tuple[Optional[bytes], dict]":
    """The bytes a value holds and the fields needed to restore it: an array's data with its dtype string and shape, or
    bytes unchanged; (None, {}) for anything else."""
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
