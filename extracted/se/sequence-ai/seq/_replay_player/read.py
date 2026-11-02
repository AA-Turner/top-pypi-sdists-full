"""
`seq.read_replay` - one episode's 3D replay (.seqreplay, format version 2) read into numpy arrays, as the console's
player reads it (frontend/app/assets/replay-format.js readReplay): the same checks, the same numbers.

In one sentence: the file's bytes (gzip, as `seq eval report --replays` saves them) → "SEQRPLY1" | uint32 header length
| the JSON header | zeros to an 8-byte boundary | the arrays, little-endian, each at its header offset → a ReplayArrays: every
node's pose at frame 0 (pos0, quat0), the moving nodes' at every frame (pos, quat), the frames' times and steps, and
the sparse changes of colour and visibility (looks).

WHY one to one with the browser's reader: a replay read here and the same file drawn by `seq eval replay` must be the
same numbers - an int16 orientation is divided by its scale in float64 and kept as float32, then made unit length by
the algorithm the browser's Math.hypot uses, so each array is equal to the page's to the bit.

"""
from __future__ import annotations

import gzip
import json
import math
import os
import struct
from dataclasses import dataclass, field
from typing import Any

MAGIC = b"SEQRPLY1"
WIDTH = {"float32": 4, "int32": 4, "int16": 2}


@dataclass(frozen=True)
class ReplayArrays:
    """One episode's replay. Positions in metres, Z up; orientations x y z w, unit length.

    `t` float32[F] seconds since the reset; `step` int32[F]; `pos0` float32[N, 3] and `quat0` float32[N, 4] every node
    at frame 0; `pos` float32[F, M, 3] and `quat` float32[F, M, 4] the M nodes in `moving` at every frame (empty when
    none moves); `looks` {node: {"rgba": [(frame, [r, g, b, a]), ...], "visible": [(frame, bool), ...]}}, each event
    in force from its frame until that node's next one of its kind; `episode` and `scene` as the file's header has
    them."""

    fps: float | None
    frames: int
    nodes: list[str]
    moving: list[int]
    t: Any
    step: Any
    pos0: Any
    quat0: Any
    pos: Any
    quat: Any
    looks: dict[int, dict[str, list]] = field(default_factory=dict)
    stride: int = 1
    episode: dict = field(default_factory=dict)
    scene: dict = field(default_factory=dict)


def _numpy():
    try:
        import numpy as np
    except ImportError:
        raise ImportError("seq.read_replay needs numpy: pip install 'sequence-ai[data]'") from None
    return np


def _number(v: Any) -> float:
    """A JSON value as the browser's Number() reads it."""
    if v is None:
        return 0.0
    if isinstance(v, bool):
        return float(v)
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        s = v.strip()
        if not s:
            return 0.0
        try:
            return float(s)
        except ValueError:
            return math.nan
    return math.nan


def _is_int(x: float) -> bool:
    return math.isfinite(x) and x == math.floor(x)


def _or(x: float, default):
    """`x || default` in the browser: 0 and NaN give the default."""
    return default if x == 0 or math.isnan(x) else x


def _truthy(v: Any) -> bool:
    """Whether a JSON value is true in the browser: an empty object or list is."""
    if isinstance(v, (dict, list)):
        return True
    if isinstance(v, float) and math.isnan(v):
        return False
    return bool(v)


def _key(e: dict, k: str) -> float:
    """e[k] as Number() reads it - NaN when the key is missing (undefined), 0 for null."""
    return _number(e[k]) if k in e else math.nan


def _array(np, data: bytes, base: int, spec: Any, name: str, shape: list[int]):
    """One array of the header's `arrays`, from the array area: float32 and int32 as stored, int16 divided by its
    scale (in float64, kept as float32)."""
    if not isinstance(spec, dict) or spec.get("dtype") not in WIDTH:
        raise ValueError(f'replay: the header has no readable "{name}" array')
    want = math.prod(shape)
    got_shape = spec.get("shape") or []
    got = math.prod(_number(x) for x in got_shape) if got_shape else 1
    if got != want or len(got_shape) != len(shape):
        raise ValueError(f'replay: "{name}" is {json.dumps(spec.get("shape"))}, expected {json.dumps(shape)}')
    dtype = spec["dtype"]
    at = base + int(_number(spec.get("offset") or 0))
    if at + want * WIDTH[dtype] > len(data):
        raise ValueError(f'replay: the file ends inside "{name}"')
    raw = np.frombuffer(data, dtype={"float32": "<f4", "int32": "<i4", "int16": "<i2"}[dtype], count=want, offset=at)
    if dtype == "int32":
        out = raw.astype(np.int32)
    elif dtype == "float32":
        out = raw.astype(np.float32)
    else:
        scale = _or(_number(spec.get("scale")), 1.0)
        out = (raw.astype(np.float64) / scale).astype(np.float32)
    return out.reshape(shape)


def _unit(np, q):
    """Every orientation made unit length, as the browser does it: Math.hypot of the four (each over the largest's
    magnitude, summed with Kahan's compensation, the root times that magnitude) or 1, each divided in float64."""
    q64 = q.astype(np.float64)
    a = np.abs(q64)
    top = a.max(axis=-1, keepdims=True)
    safe = np.where(top == 0, 1.0, top)
    total = np.zeros(top.shape, dtype=np.float64)
    comp = np.zeros(top.shape, dtype=np.float64)
    for k in range(4):
        x = a[..., k:k + 1] / safe
        summand = x * x - comp
        pre = total + summand
        comp = (pre - total) - summand
        total = pre
    n = np.where(top == 0, 0.0, np.sqrt(total) * top)
    n = np.where((n == 0) | np.isnan(n), 1.0, n)
    return (q64 / n).astype(np.float32)


def _looks(events: Any, frames: int, nodes: int) -> dict[int, dict[str, list]]:
    """The header's `looks` → {node: {"rgba": [...], "visible": [...]}}, each in frame order. An event the file cannot
    mean refuses it."""
    out: dict[int, dict[str, list]] = {}
    if events is None:
        return out
    if not isinstance(events, list):
        raise ValueError('replay: "looks" is not a list')
    for e in events:
        f = _key(e, "f") if isinstance(e, dict) else math.nan
        n = _key(e, "n") if isinstance(e, dict) else math.nan
        if not _is_int(f) or f < 0 or f >= frames or not _is_int(n) or n < 0 or n >= nodes:
            raise ValueError("replay: a look names a frame or node the file does not have")
        at = out.setdefault(int(n), {"rgba": [], "visible": []})
        if isinstance(e, dict) and "rgba" in e:
            rgba = e["rgba"]
            if not isinstance(rgba, list) or len(rgba) != 4 or not all(math.isfinite(_number(v)) for v in rgba):
                raise ValueError("replay: a look's rgba is not four numbers")
            at["rgba"].append((int(f), [max(0.0, min(1.0, _number(v))) for v in rgba]))
        if isinstance(e, dict) and isinstance(e.get("visible"), bool):
            at["visible"].append((int(f), e["visible"]))
    for at in out.values():
        at["rgba"].sort(key=lambda x: x[0])
        at["visible"].sort(key=lambda x: x[0])
    return out


def _unpacked(source: str | os.PathLike | bytes) -> tuple[bytes, dict, int]:
    """The file's bytes (gunzipped), its header and the header's length."""
    if isinstance(source, (bytes, bytearray, memoryview)):
        data = bytes(source)
    else:
        with open(source, "rb") as f:
            data = f.read()
    if len(data) >= 2 and data[0] == 0x1F and data[1] == 0x8B:
        data = gzip.decompress(data)
    if len(data) < 12 or data[:8] != MAGIC:
        raise ValueError("replay: not a .seqreplay file")
    (length,) = struct.unpack_from("<I", data, 8)
    try:
        head = json.loads(data[12:12 + length].decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        raise ValueError("replay: its header is not JSON") from None
    if not isinstance(head, dict):
        raise ValueError("replay: its header is not JSON")
    return data, head, length


def header(source: str | os.PathLike | bytes) -> dict:
    """A .seqreplay's JSON header alone (its frames, nodes, episode and scene), read without numpy."""
    return _unpacked(source)[1]


def read_replay(source: str | os.PathLike | bytes) -> ReplayArrays:
    """An episode's .seqreplay - a path, or its bytes - as a ReplayArrays. Raises ValueError saying what is wrong with a file
    it cannot read."""
    np = _numpy()
    data, head, length = _unpacked(source)
    if head.get("format") != "seq-replay" or _number(head.get("version")) != 2:
        raise ValueError(f"replay: format {head.get('format')} version {head.get('version')}; "
                         "seq.read_replay reads seq-replay version 2")
    if (head.get("quat") or "xyzw") != "xyzw" or (head.get("up") or "+z") != "+z" or (head.get("units") or "m") != "m":
        raise ValueError("replay: only metres, +z up and x y z w orientations are read")
    frames = _number(head.get("frames"))
    nodes = [str(x) for x in head["nodes"]] if isinstance(head.get("nodes"), list) else []
    moving_raw = [_number(x) for x in head["moving"]] if isinstance(head.get("moving"), list) else []
    if not _is_int(frames) or frames < 1 or not nodes:
        raise ValueError("replay: the header needs frames and nodes")
    if any(not _is_int(m) or m < 0 or m >= len(nodes) for m in moving_raw):
        raise ValueError('replay: "moving" names a node the file does not have')
    F, N, M = int(frames), len(nodes), len(moving_raw)
    base = 12 + length
    base += (8 - base % 8) % 8
    arrays = head.get("arrays") or {}
    t = _array(np, data, base, arrays.get("t"), "t", [F])
    for i in range(1, F):
        if not t[i] >= t[i - 1]:
            raise ValueError("replay: its times go backwards")
    step = (_array(np, data, base, arrays.get("step"), "step", [F]) if _truthy(arrays.get("step"))
            else np.arange(F, dtype=np.int32))
    episode, scene = head.get("episode"), head.get("scene")
    return ReplayArrays(
        fps=_or(_number(head.get("fps")), None), frames=F, nodes=nodes, moving=[int(m) for m in moving_raw], t=t,
        step=step,
        pos0=_array(np, data, base, arrays.get("pos0"), "pos0", [N, 3]),
        quat0=_unit(np, _array(np, data, base, arrays.get("quat0"), "quat0", [N, 4])),
        pos=_array(np, data, base, arrays.get("pos"), "pos", [F, M, 3]) if M else np.zeros((F, 0, 3), np.float32),
        quat=(_unit(np, _array(np, data, base, arrays.get("quat"), "quat", [F, M, 4])) if M
              else np.zeros((F, 0, 4), np.float32)),
        looks=_looks(head.get("looks"), F, N),
        stride=_or(_number(head.get("stride")), 1),
        episode=episode if isinstance(episode, dict) else {},
        scene=scene if isinstance(scene, dict) else {},
    )
