# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
Compressed items and their decompression: what a robot puts in place of a large array or bytes of its observation when
sending it compressed saves more upload time than compressing it costs (compress.py), and what a server restores,
losslessly, so every reader after it receives the bytes the robot built.

    from sequence_ai.network import compressed, msgpack_io

    observation, grew = compressed.expand(msgpack_io.unpack(body), limit=64 << 20)

In one sentence: the robot compresses a numpy array or bytes of 16 KiB or more with zstd level 1 (zlib level 1 where it
has no zstd) and puts the map below in its place → on arrival, before anything stores it, expand() restores every map to
the array or bytes it was (np.frombuffer: read-only, as msgpack_io reads an array) and returns how many bytes that
added.

The map, version 1 (`data` is bytes):
  {"__seq__": "compressed", "v": 1, "codec": "zstd" | "zlib", "n": <bytes before>, "data": <compressed>}
      for bytes
  ... plus "type": numpy's dtype string, and "shape": the array's shape, for an array (its data in C order)
`n` is checked against the number of bytes the data decompresses to, and against `limit`, the most one item may
hold: a map whose `n` is smaller than what its data holds is refused, and nothing is decompressed past `n`.

WHY one reserved key: a map with "__seq__" is one this format wrote. A map that carries the key with another kind is
left unchanged, and expand() does not look inside it.

    wire = compress(frame, "zstd")                       # a reference encoder (compress.Squeeze has its own rule)
    value, grew = expand(observation, limit=64 << 20)    # on the server, on arrival
"""
from __future__ import annotations

import zlib
from typing import Any

MARK = "__seq__"

__all__ = ["CODECS", "KIND", "VERSION", "CompressedError", "compress", "expand", "holds", "is_compressed"]

KIND = "compressed"
VERSION = 1
CODECS = ("zstd", "zlib")
_LEVEL = 1


class CompressedError(ValueError):
    """A compressed item that cannot be read: an unknown codec, data that does not decompress to the `n` bytes it
    declares, an `n` past the limit, or an array's type or shape that does not match them."""


def is_compressed(value: Any) -> bool:
    """Whether `value` is the map compress() writes for one compressed item."""
    return isinstance(value, dict) and value.get(MARK) == KIND


def is_marked(value: Any) -> bool:
    """Whether `value` is a map that carries the reserved key with another kind: left unchanged, and never looked
    inside."""
    return isinstance(value, dict) and MARK in value and value.get(MARK) != KIND


def _zstd():
    """zstd's (compress, decompress): zstandard's, else Python 3.14's compression.zstd. The decompress function takes
    the number of bytes the item declares and refuses a frame whose header declares another: the header is what sizes
    the buffer."""
    try:
        import zstandard

        def unzstd(b: bytes, n: int) -> bytes:
            declared = zstandard.frame_content_size(b)
            if declared not in (-1, n):
                raise CompressedError(f"a zstd item whose frame declares {declared} bytes and whose map declares {n}")
            return zstandard.ZstdDecompressor().decompress(b, max_output_size=n)

        return (lambda b: zstandard.ZstdCompressor(level=_LEVEL).compress(b), unzstd)
    except ImportError:
        from compression import zstd

        def unzstd(b: bytes, n: int) -> bytes:
            declared = zstd.get_frame_info(b).decompressed_size
            if declared not in (None, n):
                raise CompressedError(f"a zstd item whose frame declares {declared} bytes and whose map declares {n}")
            d = zstd.ZstdDecompressor()
            raw = d.decompress(b, max_length=n)
            if not d.eof:
                raise CompressedError(f"a zstd item that holds more than the {n} bytes it declares")
            return raw

        return (lambda b: zstd.compress(b, level=_LEVEL), unzstd)


def compress(value: Any, codec: str = "zstd") -> dict:
    """`value` (a numpy array or bytes) as its compressed item. This is a reference encoder, for tests and for a server
    that sends compressed items itself; a robot decides what to compress by its own rule (compress.Squeeze)."""
    import numpy as np

    if isinstance(value, np.ndarray):
        raw = np.ascontiguousarray(value).tobytes()
        extra = {"type": value.dtype.str, "shape": list(value.shape)}
    else:
        raw, extra = bytes(value), {}
    if codec == "zstd":
        data = _zstd()[0](raw)
    elif codec == "zlib":
        data = zlib.compress(raw, _LEVEL)
    else:
        raise CompressedError(f"unknown codec {codec!r}: expected one of {', '.join(CODECS)}")
    return dict([(MARK, KIND), ("v", VERSION), ("codec", codec), ("n", len(raw)), *extra.items(), ("data", data)])


def _raw(item: dict, limit: int) -> bytes:
    codec, n, data = item.get("codec"), item.get("n"), item.get("data")
    if codec not in CODECS:
        raise CompressedError(f"a compressed item with codec {codec!r}: only {', '.join(CODECS)} are supported")
    if isinstance(n, bool) or not isinstance(n, int) or not 0 <= n <= limit:
        raise CompressedError(f"a compressed item of {n!r} bytes: the limit is {limit} bytes")
    if not isinstance(data, (bytes, bytearray)):
        raise CompressedError("a compressed item whose data is not bytes")
    try:
        if codec == "zstd":
            raw = _zstd()[1](bytes(data), n)
        else:
            d = zlib.decompressobj()
            raw = d.decompress(bytes(data), n)
            if d.unconsumed_tail or not d.eof:
                raise CompressedError(f"a zlib item that holds more than the {n} bytes it declares")
    except CompressedError:
        raise
    except Exception as exc:  # noqa: BLE001 (any error from zstandard or zlib: data that cannot be decompressed)
        raise CompressedError(f"a {codec} item that cannot be decompressed: {exc}") from None
    if len(raw) != n:
        raise CompressedError(f"a {codec} item that decompressed to {len(raw)} bytes and declares {n}")
    return raw


def _value(item: dict, limit: int) -> Any:
    raw = _raw(item, limit)
    if "type" not in item and "shape" not in item:
        return raw
    import numpy as np

    from sequence_ai.network.msgpack_io import MsgpackError, _dtype

    shape = item.get("shape")
    if not isinstance(shape, list) or not all(isinstance(d, int) and not isinstance(d, bool) and d >= 0 for d in shape):
        raise CompressedError("a compressed array whose shape is not a list of non-negative ints")
    try:
        dtype = _dtype(item.get("type"))
    except MsgpackError as exc:
        raise CompressedError(f"a compressed array: {exc}") from None
    if dtype.itemsize * int(np.prod(shape, dtype=np.int64)) != len(raw):
        raise CompressedError(f"a compressed {dtype} array of shape {shape} that holds {len(raw)} bytes")
    return np.frombuffer(raw, dtype=dtype).reshape(shape)


def expand(value: Any, *, limit: int) -> "tuple[Any, int]":
    """Return `value` with every compressed item in it (in dicts and lists at any depth, never inside a map of another
    kind) restored to the array or bytes it was, and the number of bytes that added. Where it holds no compressed item,
    the same objects are returned. `limit`: the most bytes one item may decompress to. Raises CompressedError for an
    item that cannot be read."""
    grew = [0]

    def walk(v: Any) -> Any:
        if isinstance(v, dict):
            if is_compressed(v):
                out = _value(v, limit)
                grew[0] += max(0, int(v["n"]) - len(v["data"]))
                return out
            if is_marked(v) or not holds(v):
                return v
            return {k: walk(x) for k, x in v.items()}
        if isinstance(v, list):
            return [walk(x) for x in v] if holds(v) else v
        return v

    return walk(value), grew[0]


def holds(value: Any) -> bool:
    """Whether `value` holds a compressed item: in dicts and lists at any depth, not inside a map of another kind."""
    if isinstance(value, dict):
        return is_compressed(value) or (not is_marked(value) and any(holds(v) for v in value.values()))
    if isinstance(value, list):
        return any(holds(v) for v in value)
    return False
