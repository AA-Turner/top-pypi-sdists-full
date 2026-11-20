# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
Observations and responses as msgpack: bytes as bytes and numpy arrays as their raw data, where JSON carries bytes as
base64 (a third larger on the wire) and arrays as lists of numbers. Written in plain Python, so neither side installs a
msgpack package for it.

    from sequence_ai.network import msgpack_io

    body = msgpack_io.pack({"image": frame, "state": joints})     # MsgpackError: a value msgpack cannot carry
    observation = msgpack_io.unpack(body)                          # MsgpackError: not one msgpack value, or one refused

In one sentence: `pack` writes a value as msgpack, each numpy array as the map msgpack-numpy writes ({"nd": True,
"type", "kind", "shape", "data"}) → `unpack` reads it back to the same value, with arrays as read-only arrays or, on a
machine without numpy, as the lists their tolist() returns, which is what the same value holds in JSON.

WHY both array layouts are read: the two ecosystems that send numpy over msgpack write arrays differently (msgpack-numpy
as {"nd", "type", "kind", "shape", "data"}, openpi as {"__ndarray__", "data", "dtype", "shape"}), and a policy's own
client may use either. A server that reads with this module accepts both, and msgpack-numpy reads what this module
writes.
WHY no array that holds objects: msgpack-numpy writes one with pickle, and reading that back runs code the sender chose.
A dtype that holds objects, a structured dtype and every msgpack extension type are refused, so reading a body never
executes anything.
"""
from __future__ import annotations

import re
import struct
import sys
from typing import Any, NamedTuple

__all__ = ["MAX_DEPTH", "MEDIA_TYPE", "MsgpackError", "pack", "unpack"]

MEDIA_TYPE = "application/x-seq-msgpack"
# The deepest that lists and maps may nest. A request's body nests a few levels; a deeper body is refused, not
# recursed into.
MAX_DEPTH = 64


class MsgpackError(ValueError):
    """A value msgpack cannot carry (packing), or a body that is not exactly one supported msgpack value (unpacking)."""


# ── packing ───────────────────────────────────────────────────────────────────────────────────────────────────────
def pack(obj: Any) -> bytes:
    """`obj` as msgpack: None, bools, ints (-2**63 to 2**64 - 1), floats, str, bytes, lists and tuples, dicts (keys str,
    bytes or int), and numpy arrays and scalars (as msgpack-numpy writes them) inside any of those; a PIL image is sent
    as its numpy array."""
    out: list[bytes] = []
    _pack(obj, out, 0)
    return b"".join(out)


def _pack(obj: Any, out: list, depth: int) -> None:
    if depth > MAX_DEPTH:
        raise MsgpackError(f"nested deeper than {MAX_DEPTH} levels")
    if obj is None:
        out.append(b"\xc0")
    elif obj is True:
        out.append(b"\xc3")
    elif obj is False:
        out.append(b"\xc2")
    elif isinstance(obj, int):
        _pack_int(obj, out)
    elif isinstance(obj, float):
        out.append(struct.pack(">Bd", 0xCB, obj))
    elif isinstance(obj, str):
        try:
            raw = obj.encode("utf-8")
        except UnicodeEncodeError as exc:
            raise MsgpackError(f"a string that is not UTF-8: {exc.reason}") from None
        _pack_head(len(raw), out, fix=(0xA0, 31), sizes=((0xD9, ">BB", 0xFF), (0xDA, ">BH", 0xFFFF),
                                                           (0xDB, ">BI", 0xFFFFFFFF)), what="string")
        out.append(raw)
    elif isinstance(obj, (bytes, bytearray, memoryview)):
        raw = bytes(obj)
        _pack_head(len(raw), out, fix=None, sizes=((0xC4, ">BB", 0xFF), (0xC5, ">BH", 0xFFFF),
                                                    (0xC6, ">BI", 0xFFFFFFFF)), what="bytes")
        out.append(raw)
    elif isinstance(obj, (list, tuple)):
        _pack_head(len(obj), out, fix=(0x90, 15), sizes=((0xDC, ">BH", 0xFFFF), (0xDD, ">BI", 0xFFFFFFFF)),
                   what="list")
        for item in obj:
            _pack(item, out, depth + 1)
    elif isinstance(obj, dict):
        _pack_head(len(obj), out, fix=(0x80, 15), sizes=((0xDE, ">BH", 0xFFFF), (0xDF, ">BI", 0xFFFFFFFF)),
                   what="dict")
        for key, value in obj.items():
            if not isinstance(key, (str, bytes, int)) or isinstance(key, bool):
                raise MsgpackError(f"a dict key that is not str, bytes or int: {type(key).__name__}")
            _pack(key, out, depth + 1)
            _pack(value, out, depth + 1)
    else:
        arr = _numpy_map(_pil_as_array(obj))
        if arr is None:
            raise MsgpackError(f"{type(obj).__name__} cannot be sent as msgpack (JSON values, bytes and numpy arrays "
                               "can)")
        _pack(arr, out, depth)


def _pil_as_array(obj: Any) -> Any:
    """A PIL image as the numpy array its pixels are (np.asarray: HxWx3 uint8 for an RGB one), so a frame fitted with
    frames.resize_image is sent as the picture it is; anything else as it is. A PIL.Image still being imported - by
    another thread, while this one packs - has no Image class yet, and nothing made from one: every value packed then
    is packed as it would be without Pillow."""
    cls = getattr(sys.modules.get("PIL.Image"), "Image", None)
    if not isinstance(cls, type) or not isinstance(obj, cls):
        return obj
    try:
        import numpy as np
    except ImportError as missing:  # pragma: no cover - depends on the install
        raise MsgpackError("a PIL image is sent as its numpy array, and numpy is not installed: pip install numpy") \
            from missing
    return np.asarray(obj)


def _pack_int(n: int, out: list) -> None:
    if 0 <= n <= 0x7F:
        out.append(bytes((n,)))
    elif -32 <= n < 0:
        out.append(struct.pack(">b", n))
    elif n > 0:
        for code, fmt, top in ((0xCC, ">BB", 0xFF), (0xCD, ">BH", 0xFFFF), (0xCE, ">BI", 0xFFFFFFFF),
                               (0xCF, ">BQ", 0xFFFFFFFFFFFFFFFF)):
            if n <= top:
                out.append(struct.pack(fmt, code, n))
                return
        raise MsgpackError(f"an int outside msgpack's 64-bit range: {n}")
    else:
        for code, fmt, low in ((0xD0, ">Bb", -0x80), (0xD1, ">Bh", -0x8000), (0xD2, ">Bi", -0x80000000),
                               (0xD3, ">Bq", -0x8000000000000000)):
            if n >= low:
                out.append(struct.pack(fmt, code, n))
                return
        raise MsgpackError(f"an int outside msgpack's 64-bit range: {n}")


def _pack_head(n: int, out: list, *, fix: tuple | None, sizes: tuple, what: str) -> None:
    if fix is not None and n <= fix[1]:
        out.append(bytes((fix[0] | n,)))
        return
    for code, fmt, top in sizes:
        if n <= top:
            out.append(struct.pack(fmt, code, n))
            return
    raise MsgpackError(f"a {what} of length {n}: longer than msgpack's 32-bit lengths allow")


def _numpy_map(obj: Any) -> dict | None:
    """A numpy array or scalar as the map msgpack-numpy writes for it, or None for anything else. If numpy has not been
    imported by this process, `obj` cannot be one."""
    import sys

    np = sys.modules.get("numpy")
    if np is None:
        return None
    if isinstance(obj, np.ndarray):
        _readable_dtype(obj.dtype)
        return {b"nd": True, b"type": obj.dtype.str, b"kind": b"", b"shape": list(obj.shape),
                b"data": np.ascontiguousarray(obj).tobytes()}
    if isinstance(obj, (np.bool_, np.number)):
        _readable_dtype(obj.dtype)
        return {b"nd": False, b"type": obj.dtype.str, b"data": np.asarray(obj).tobytes()}
    return None


def _readable_dtype(dtype) -> None:
    if dtype.hasobject or dtype.kind in ("O", "V"):
        raise MsgpackError(f"a numpy array of dtype {dtype} is not supported: only plain numeric, bool and string "
                           "dtypes are")


# ── unpacking ─────────────────────────────────────────────────────────────────────────────────────────────────────
def unpack(data: bytes) -> Any:
    """The one msgpack value `data` holds, with numpy arrays (in msgpack-numpy's or openpi's layout) returned as
    read-only arrays or, where numpy is not installed, as the nested lists of plain values their tolist() returns, which
    is what a JSON response holds. Raises MsgpackError for a truncated body, more than one value, an extension type,
    nesting past MAX_DEPTH, a length past the end of the body, or an array whose dtype holds objects."""
    view = memoryview(bytes(data)) if not isinstance(data, bytes) else memoryview(data)
    value, at = _Reader(view).read(0, 0)
    if at != len(view):
        raise MsgpackError(f"{len(view) - at} bytes follow the msgpack value")
    return value


class _Reader:
    __slots__ = ("buf", "size")

    def __init__(self, buf: memoryview) -> None:
        self.buf, self.size = buf, len(buf)

    def _take(self, at: int, n: int) -> int:
        if n < 0 or at + n > self.size:
            raise MsgpackError(f"the body ends inside a value: {n} bytes needed at offset {at} of {self.size}")
        return at + n

    def _unpack(self, fmt: str, at: int) -> tuple:
        end = self._take(at, struct.calcsize(fmt))
        return struct.unpack_from(fmt, self.buf, at), end

    def read(self, at: int, depth: int) -> tuple[Any, int]:
        if depth > MAX_DEPTH:
            raise MsgpackError(f"nested deeper than {MAX_DEPTH} levels")
        self._take(at, 1)
        code = self.buf[at]
        at += 1
        if code <= 0x7F:
            return code, at
        if code >= 0xE0:
            return code - 0x100, at
        if 0xA0 <= code <= 0xBF:
            return self._str(at, code & 0x1F)
        if 0x90 <= code <= 0x9F:
            return self._list(at, code & 0x0F, depth)
        if 0x80 <= code <= 0x8F:
            return self._map(at, code & 0x0F, depth)
        if code == 0xC0:
            return None, at
        if code == 0xC2:
            return False, at
        if code == 0xC3:
            return True, at
        fixed = _FIXED.get(code)
        if fixed is not None:
            (value,), end = self._unpack(fixed, at)
            return value, end
        sized = _SIZED.get(code)
        if sized is not None:
            kind, fmt = sized
            (n,), at = self._unpack(fmt, at)
            if kind == "str":
                return self._str(at, n)
            if kind == "bin":
                end = self._take(at, n)
                return bytes(self.buf[at:end]), end
            if kind == "list":
                return self._list(at, n, depth)
            return self._map(at, n, depth)
        if code in _EXT or code == 0xC1:
            raise MsgpackError(f"msgpack type 0x{code:02x} is not supported (extension types and the unused code 0xc1)")
        raise MsgpackError(f"not a msgpack type: 0x{code:02x}")         # unreachable: every byte is covered above

    def _str(self, at: int, n: int) -> tuple[str, int]:
        end = self._take(at, n)
        try:
            return str(self.buf[at:end], "utf-8"), end
        except UnicodeDecodeError:
            raise MsgpackError("a string that is not UTF-8") from None

    def _list(self, at: int, n: int, depth: int) -> tuple[list, int]:
        if n > self.size - at:                  # each element takes at least one byte
            raise MsgpackError(f"a list of {n} items where {self.size - at} bytes are left")
        out = []
        for _ in range(n):
            value, at = self.read(at, depth + 1)
            out.append(value)
        return out, at

    def _map(self, at: int, n: int, depth: int) -> tuple[Any, int]:
        if 2 * n > self.size - at:
            raise MsgpackError(f"a map of {n} entries where {self.size - at} bytes are left")
        out: dict = {}
        for _ in range(n):
            key, at = self.read(at, depth + 1)
            value, at = self.read(at, depth + 1)
            try:
                out[key] = value
            except TypeError:
                raise MsgpackError(f"a map key that cannot be a dict key: {type(key).__name__}") from None
        return _array_of(out), at


_FIXED = {0xCA: ">f", 0xCB: ">d", 0xCC: ">B", 0xCD: ">H", 0xCE: ">I", 0xCF: ">Q", 0xD0: ">b", 0xD1: ">h", 0xD2: ">i",
          0xD3: ">q"}
_SIZED = {0xD9: ("str", ">B"), 0xDA: ("str", ">H"), 0xDB: ("str", ">I"), 0xC4: ("bin", ">B"), 0xC5: ("bin", ">H"),
          0xC6: ("bin", ">I"), 0xDC: ("list", ">H"), 0xDD: ("list", ">I"), 0xDE: ("map", ">H"), 0xDF: ("map", ">I")}
_EXT = {0xC7, 0xC8, 0xC9, 0xD4, 0xD5, 0xD6, 0xD7, 0xD8}


def _field(m: dict, name: str):
    """A field of an array's map, whose key is bytes (as msgpack-numpy writes it) or str (as a packer without bin types
    writes it)."""
    return m[name.encode()] if name.encode() in m else m.get(name)


def _text(value) -> str:
    return value.decode("ascii", "replace") if isinstance(value, bytes) else str(value)


def _array_of(m: dict) -> Any:
    """`m` as the numpy array or scalar it represents when it has every field of one in msgpack-numpy's or openpi's
    layout; otherwise `m` unchanged, so a dict of the caller's that happens to have a key "nd" stays a dict."""
    nd, openpi, generic = _field(m, "nd"), _field(m, "__ndarray__"), _field(m, "__npgeneric__")
    has = lambda *names: all(n.encode() in m or n in m for n in names)          # noqa: E731
    if nd is True and has("type", "shape", "data"):
        _dtype(_field(m, "type"))               # an object dtype is refused as such, before the kind is checked
        if _field(m, "kind") not in (None, b"", ""):
            raise MsgpackError("a structured numpy array is not supported: only plain numeric, bool and string dtypes "
                               "are")
        return _array(_field(m, "type"), _field(m, "shape"), _field(m, "data"))
    if openpi is True and has("dtype", "shape", "data"):
        return _array(_field(m, "dtype"), _field(m, "shape"), _field(m, "data"))
    if nd is False and has("type", "data"):
        dtype, data = _dtype(_field(m, "type")), _field(m, "data")
        if not isinstance(data, bytes) or len(data) != dtype.itemsize:
            raise MsgpackError(f"a numpy {dtype} scalar whose data is not {dtype.itemsize} bytes")
        np = _numpy()
        return _plain_items(dtype, data, 1)[0] if np is None else np.frombuffer(data, dtype=dtype, count=1)[0]
    if generic is True and has("dtype", "data"):
        dtype, value = _dtype(_field(m, "dtype")), _field(m, "data")
        if not isinstance(value, (bool, int, float, str, bytes)):
            raise MsgpackError("a numpy scalar's map whose data is not a plain value")
        return value if _numpy() is None else dtype.type(value)
    return m


def _array(descr, shape, data):
    dtype = _dtype(descr)
    if not isinstance(shape, list) or not all(isinstance(d, int) and not isinstance(d, bool) and d >= 0
                                              for d in shape) or not isinstance(data, bytes):
        raise MsgpackError("a numpy array's map without a shape of non-negative ints or its data as bytes")
    if len(shape) > _MAX_DIMS:
        raise MsgpackError(f"a numpy array of {len(shape)} dimensions: numpy allows {_MAX_DIMS} at most")
    count = 1
    for d in shape:
        count *= d
    if len(data) != count * dtype.itemsize:
        raise MsgpackError(f"a numpy array of shape {shape} and dtype {dtype} is {count * dtype.itemsize} bytes; its "
                           f"data is {len(data)}")
    np = _numpy()
    if np is None:
        return _nested(_plain_items(dtype, data, count), shape)
    return np.frombuffer(data, dtype=dtype, count=count).reshape(shape)


# numpy's NPY_MAXDIMS: numpy creates no array with more, so a longer shape is refused before it is read
_MAX_DIMS = 64


def _numpy():
    """numpy, or None where it is not installed: arrays are then read as plain values (_Plain)."""
    try:
        import numpy
    except ImportError:
        return None
    return numpy


def _dtype(descr):
    """`descr`, an array's type string, as a numpy dtype or, where numpy is not installed, as a _Plain parsed here.
    Raises MsgpackError for a dtype that holds objects, a structured dtype, and a value that is not a type string."""
    if not isinstance(descr, (str, bytes)):
        raise MsgpackError("a numpy array's dtype is not a type string: a structured array is not supported, only "
                           "plain numeric, bool and string dtypes are")
    np = _numpy()
    if np is None:
        return _plain(_text(descr))
    try:
        dtype = np.dtype(_text(descr))
    except TypeError:
        raise MsgpackError(f"not a numpy dtype: {_text(descr)!r}") from None
    _readable_dtype(dtype)
    return dtype


# ── without numpy ─────────────────────────────────────────────────────────────────────────────────────────────────────
# WHY: a client does not have to install numpy, yet a server responds in msgpack with the arrays its policy returned.
# Without numpy, an array is read as the nested lists of plain values its tolist() returns, which is what the same
# response holds in JSON, instead of raising an error.
class _Plain(NamedTuple):
    """An array's type string ('<f4', '|u1', '<U5': numpy's dtype.str) parsed without numpy: the byte order as struct
    writes it, the kind (numpy's letter) and the size of one item in bytes."""
    text: str
    order: str
    kind: str
    itemsize: int

    def __str__(self) -> str:
        return self.text


# The struct format of one item, by (kind, size): bool, signed and unsigned ints, half, single and double floats,
# and a complex as its two floats. Strings ('S' bytes, 'U' UTF-32) are sliced directly; any other type needs numpy.
_STRUCT = {("b", 1): "?", ("i", 1): "b", ("i", 2): "h", ("i", 4): "i", ("i", 8): "q", ("u", 1): "B", ("u", 2): "H",
           ("u", 4): "I", ("u", 8): "Q", ("f", 2): "e", ("f", 4): "f", ("f", 8): "d", ("c", 8): "f", ("c", 16): "d"}
_TYPE = re.compile(r"([<>|=]?)([A-Za-z])(.*)", re.DOTALL)


def _plain(text: str) -> _Plain:
    """Parse a type string. Raises MsgpackError for one that holds objects or is structured (refused as with numpy), one
    whose items are 0 bytes, and one that only numpy can read (a long double, a datetime, a timedelta)."""
    match = _TYPE.fullmatch(text)
    order, kind, size = match.groups() if match else ("", "", "")
    if kind in ("O", "V"):
        raise MsgpackError(f"a numpy array of dtype {text} is not supported: only plain numeric, bool and string "
                           "dtypes are")
    n = int(size) if size.isascii() and size.isdigit() else -1
    if kind in ("S", "U") and n == 0:
        raise MsgpackError(f"a numpy array of dtype {text}, whose items are 0 bytes")
    itemsize = 4 * n if kind == "U" else n
    if not ((kind in ("S", "U") and n > 0) or (kind, itemsize) in _STRUCT):
        raise MsgpackError(f"this body holds a numpy array of dtype {text}, which only numpy can read, and numpy is "
                           "not installed")
    return _Plain(text, "<" if order in ("", "|") else order, kind, itemsize)


def _plain_items(t: _Plain, data: bytes, count: int) -> list:
    """`count` items of type `t` from `data`, as tolist() returns them: ints, floats, complex numbers and bools; bytes
    and strs with their trailing NULs stripped, as numpy strips them."""
    size = t.itemsize
    if t.kind == "S":
        return [data[i:i + size].rstrip(b"\x00") for i in range(0, count * size, size)]
    if t.kind == "U":
        big = t.order == ">" or (t.order == "=" and sys.byteorder == "big")
        try:
            return [str(data[i:i + size], "utf-32-be" if big else "utf-32-le").rstrip("\x00")
                    for i in range(0, count * size, size)]
        except UnicodeDecodeError:
            raise MsgpackError(f"a numpy array of dtype {t} whose data is not UTF-32") from None
    code = _STRUCT[(t.kind, size)]
    if t.kind == "c":
        parts = struct.unpack_from(f"{t.order}{2 * count}{code}", data)
        return [complex(parts[i], parts[i + 1]) for i in range(0, 2 * count, 2)]
    return list(struct.unpack_from(f"{t.order}{count}{code}", data))


def _nested(flat: list, shape: list) -> Any:
    """`flat`, in C order, as nested lists of `shape`, nested as tolist() nests them; a 0-d array's value is returned as
    itself."""
    if not shape:
        return flat[0]
    if len(shape) == 1:
        return flat
    step = len(flat) // shape[0] if shape[0] else 0
    return [_nested(flat[i * step:(i + 1) * step], shape[1:]) for i in range(shape[0])]
