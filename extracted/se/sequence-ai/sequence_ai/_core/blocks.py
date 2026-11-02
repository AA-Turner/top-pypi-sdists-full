"""
An observation's large arrays, bytes and text sent once an episode, at the robot (sequence-base codec.blocks is the
worker's half, byte for byte the same format; the SDK keeps its own, as it does msgpack_io: nothing of the platform's
packages on a robot's act path).


In one sentence: observe() cuts each unmarked numpy array, bytes or str of
MIN_BLOCK_BYTES or more into blocks - an array stacked along its first axis, 2 to SPLIT_MAX slices each of
MIN_BLOCK_BYTES or more, a block a slice - each named by the first ID_BYTES of its sha256, on the robot's own thread
(Cut) → its frame carries references in their place → its post (observe_stream) carries the content of each block its
worker does not hold, as both sides count it (Retention: what the last KEEP_OBSERVATIONS observations that used a block
used), each compressed where that pays (compress.Squeeze) → the worker turns each frame back as its turn comes; one that
lacks a block refuses the episode's next act from it (409 frames_missing), and the robot sends from there with every
block.

What a frame's references look like is codec.blocks': {"__seq__": "array", "v": 1, "type", "shape", "blocks": [id,
...]}, {"__seq__": "bytes", "v": 1, "blocks": [id]}, {"__seq__": "str", "v": 1, "blocks": [id]}.
"""
from __future__ import annotations

import hashlib
import sys
from collections import deque
from typing import Any, Iterable, Optional

from . import msgpack_io as _msgpack

MARK = "__seq__"
KINDS = ("array", "bytes", "str")
VERSION = 1
ID_BYTES = 16
MIN_BLOCK_BYTES = 16 * 1024
SPLIT_MAX = 64
KEEP_OBSERVATIONS = 8


def block_id(data: bytes) -> bytes:
    """A block's name: the first ID_BYTES of its content's sha256 (sequence-base codec.blocks.block_id)."""
    return hashlib.sha256(data).digest()[:ID_BYTES]


def cut(value: Any) -> "Optional[list[bytes]]":
    """The blocks a value is sent as - its content, or an array stacked along its first axis a slice each - or None for
    one that is no block (sequence-base codec.blocks.cut, the same rule)."""
    if isinstance(value, (bytes, bytearray, memoryview)):
        data = bytes(value)
        return [data] if len(data) >= MIN_BLOCK_BYTES else None
    if isinstance(value, str):
        data = value.encode("utf-8")
        return [data] if len(data) >= MIN_BLOCK_BYTES else None
    np = sys.modules.get("numpy")
    if np is None or not isinstance(value, np.ndarray) or value.dtype.hasobject or value.nbytes < MIN_BLOCK_BYTES:
        return None
    data = np.ascontiguousarray(value)
    if data.ndim >= 2 and 2 <= data.shape[0] <= SPLIT_MAX and data.nbytes // data.shape[0] >= MIN_BLOCK_BYTES:
        return [data[i].tobytes() for i in range(data.shape[0])]
    return [data.tobytes()]


def encode(value: Any) -> "tuple[Any, dict[bytes, bytes], list[bytes], dict[bytes, tuple]]":
    """`value` - an observation, its markers encoded - with every block it holds, in dicts, lists and tuples at any
    depth and never inside a map of the observation format's own (a marked or compressed item), put as its reference
    (tuples become lists, as msgpack writes them); the blocks' contents by id; every id it used, in order, once each;
    and each id's place in it (the path its compressing is decided by, compress.Squeeze). The same object where it
    holds none."""
    contents: dict[bytes, bytes] = {}
    used: list[bytes] = []
    paths: dict[bytes, tuple] = {}

    def walk(v: Any, path: tuple) -> Any:
        if isinstance(v, dict):
            if MARK in v:
                return v
            out = {k: walk(x, path + (k,)) for k, x in v.items()}
            return out if any(out[k] is not v[k] for k in v) else v
        if isinstance(v, (list, tuple)):
            out = [walk(x, path + (i,)) for i, x in enumerate(v)]
            return out if isinstance(v, tuple) or any(a is not b for a, b in zip(out, v)) else v
        parts = cut(v)
        if parts is None:
            return v
        ids = []
        for part in parts:
            bid = block_id(part)
            if bid not in contents:
                contents[bid] = part
                used.append(bid)
                paths[bid] = path
            ids.append(bid)
        if isinstance(v, str):
            return dict([(MARK, "str"), ("v", VERSION), ("blocks", ids)])
        if isinstance(v, (bytes, bytearray, memoryview)):
            return dict([(MARK, "bytes"), ("v", VERSION), ("blocks", ids)])
        return dict([(MARK, "array"), ("v", VERSION), ("type", v.dtype.str), ("shape", list(v.shape)),
                     ("blocks", ids)])

    return walk(value, ()), contents, used, paths


def decode(value: Any, contents: dict) -> Any:
    """`value` with every reference turned back from `contents` into what was cut (inline)."""
    if isinstance(value, dict):
        if value.get(MARK) in KINDS:
            data = b"".join(bytes(contents[bytes(b)]) for b in value["blocks"])
            if value[MARK] == "bytes":
                return data
            if value[MARK] == "str":
                return data.decode("utf-8")
            import numpy as np

            return np.frombuffer(data, dtype=np.dtype(value["type"])).reshape(value["shape"])
        if MARK in value:
            return value
        return {k: decode(v, contents) for k, v in value.items()}
    if isinstance(value, list):
        return [decode(v, contents) for v in value]
    return value


def inline(frame: bytes, contents: dict) -> bytes:
    """A packed frame ({"seq", "inputs"}) whose inputs hold references, packed again with each turned back: one kept
    for the episode's next act, as its worker went as it was cut, and no worker counts what it holds yet."""
    from . import observe_stream as _observe

    f = _msgpack.unpack(frame)
    return _observe.frame(f["seq"], _observe.packed(decode(f["inputs"], contents)))


class Cut:
    """One observation's cutting at observe(), in place of its compressing (marked_observe.packed's `squeeze`): its
    blocks put as references, then the rest compressed where that pays (`squeeze`); what it cut kept for the stream (`last`: used, contents, paths) - again if its observation is
    encoded again before it is numbered."""

    def __init__(self, squeeze: Any = None) -> None:
        self._squeeze = squeeze
        self.last: "Optional[tuple[list[bytes], dict[bytes, bytes], dict[bytes, tuple]]]" = None

    def apply(self, value: Any) -> Any:
        encoded, contents, used, paths = encode(value)
        self.last = (used, contents, paths) if used else None
        return encoded if self._squeeze is None else self._squeeze.apply(encoded)


class Retention:
    """The blocks an episode's worker holds, as the robot and the worker both count them (sequence-base
    codec.blocks.Retention, the same rule): those the last `keep` observations that used any block used, in their
    order; an observation of no block moves nothing."""

    def __init__(self, keep: int = KEEP_OBSERVATIONS) -> None:
        self._recent: deque = deque(maxlen=keep)

    def holds(self, bid: bytes) -> bool:
        return any(bid in used for used in self._recent)

    def held(self) -> set:
        return set().union(*self._recent) if self._recent else set()

    def use(self, ids: Iterable[bytes]) -> set:
        ids = frozenset(ids)
        if not ids:
            return set()
        before = self.held()
        self._recent.append(ids)
        return before - self.held()
