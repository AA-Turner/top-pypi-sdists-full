from __future__ import annotations

import math
import struct
from collections.abc import Mapping, Sequence
from typing import Any

import numpy as np
import xxhash

_MAGIC = b"NEST"
_VERSION = 1
_HEADER = _MAGIC + bytes([_VERSION, 0, 0, 0])
_CHECKSUM_SEED = 0x4E455354

_TAG_ARRAY = 0
_TAG_DICT = 1
_TAG_LIST = 2

_DTYPE_BOOL = 0
_DTYPE_INT8 = 1
_DTYPE_INT16 = 2
_DTYPE_INT32 = 3
_DTYPE_INT64 = 4
_DTYPE_UINT8 = 5
_DTYPE_UINT16 = 6
_DTYPE_UINT32 = 7
_DTYPE_UINT64 = 8
_DTYPE_FLOAT32 = 9
_DTYPE_FLOAT64 = 10
_DTYPE_STRING = 11

_ENCODABLE_DTYPES: dict[np.dtype[Any], tuple[int, np.dtype[Any]]] = {
    np.dtype(np.bool_): (_DTYPE_BOOL, np.dtype(np.bool_)),
    np.dtype(np.int8): (_DTYPE_INT8, np.dtype(np.int8)),
    np.dtype(np.int16): (_DTYPE_INT16, np.dtype("<i2")),
    np.dtype(np.int32): (_DTYPE_INT32, np.dtype("<i4")),
    np.dtype(np.int64): (_DTYPE_INT64, np.dtype("<i8")),
    np.dtype(np.uint8): (_DTYPE_UINT8, np.dtype(np.uint8)),
    np.dtype(np.uint16): (_DTYPE_UINT16, np.dtype("<u2")),
    np.dtype(np.uint32): (_DTYPE_UINT32, np.dtype("<u4")),
    np.dtype(np.uint64): (_DTYPE_UINT64, np.dtype("<u8")),
    np.dtype(np.float32): (_DTYPE_FLOAT32, np.dtype("<f4")),
    np.dtype(np.float64): (_DTYPE_FLOAT64, np.dtype("<f8")),
}

_DECODABLE_DTYPES: dict[int, np.dtype[Any]] = {
    _DTYPE_BOOL: np.dtype(np.bool_),
    _DTYPE_INT8: np.dtype(np.int8),
    _DTYPE_INT16: np.dtype("<i2"),
    _DTYPE_INT32: np.dtype("<i4"),
    _DTYPE_INT64: np.dtype("<i8"),
    _DTYPE_UINT8: np.dtype(np.uint8),
    _DTYPE_UINT16: np.dtype("<u2"),
    _DTYPE_UINT32: np.dtype("<u4"),
    _DTYPE_UINT64: np.dtype("<u8"),
    _DTYPE_FLOAT32: np.dtype("<f4"),
    _DTYPE_FLOAT64: np.dtype("<f8"),
}


class _Reader:
    def __init__(self, data: bytes) -> None:
        self._data = data
        self._offset = 0

    @property
    def offset(self) -> int:
        return self._offset

    def align_to_eight(self) -> None:
        self._offset = _align_to_eight(self._offset)
        if self._offset > len(self._data):
            raise ValueError("nested payload ended before alignment padding")

    def read(self, size: int) -> bytes:
        end = self._offset + size
        if end > len(self._data):
            raise ValueError("nested payload ended unexpectedly")
        value = self._data[self._offset : end]
        self._offset = end
        return value

    def read_u8(self) -> int:
        return self.read(1)[0]

    def read_u16(self) -> int:
        return struct.unpack("<H", self.read(2))[0]

    def read_u32(self) -> int:
        return struct.unpack("<I", self.read(4))[0]

    def read_u64(self) -> int:
        return struct.unpack("<Q", self.read(8))[0]

    def read_key(self) -> str:
        length = self.read_u16()
        return self.read(length).decode("utf-8")


def to_bytes(value: Any) -> bytes:
    output = bytearray(encoded_size(value))
    write_into(output, 0, value)
    return bytes(output)


def encoded_size(value: Any) -> int:
    """Return the exact size of ``to_bytes(value)`` without encoding it."""
    return _measure(len(_HEADER), value)


def write_into(output: bytearray | memoryview, offset: int, value: Any) -> int:
    """Encode ``value`` into ``output`` at ``offset`` and return the end offset.

    ``output`` must have ``encoded_size(value)`` bytes free at ``offset``.
    Alignment padding is relative to ``offset``, as in a standalone payload.
    """
    view = memoryview(output)
    end = offset + len(_HEADER)
    view[offset:end] = _HEADER
    return offset + _write_value(view, offset, end - offset, value)


def from_bytes(data: bytes | bytearray | memoryview) -> Any:
    payload = bytes(data)
    reader = _Reader(payload)
    header = reader.read(len(_HEADER))
    if not header.startswith(_MAGIC):
        raise ValueError("invalid nested payload magic")
    version = header[len(_MAGIC)]
    if version != _VERSION:
        raise ValueError(f"unsupported nested payload version: {version}")

    value = _read_value(reader)
    if reader.offset != len(payload):
        raise ValueError("nested payload has trailing bytes")
    return value


def _measure(position: int, value: Any) -> int:
    """Return the payload position after ``value``, starting at ``position``."""
    if isinstance(value, np.ndarray):
        _, dtype = _wire_dtype(value.dtype)
        # Scalars are written as one-element vectors (np.ascontiguousarray).
        position += 3 + 8 * max(value.ndim, 1) + 8
        return _align_to_eight(position) + value.size * dtype.itemsize
    if isinstance(value, str):
        position = _align_to_eight(position + 3 + 4 + 8)
        return position + len(value.encode("utf-8"))
    if isinstance(value, Mapping):
        position += 1 + 4
        for key in value:
            if not isinstance(key, str):
                raise TypeError("nested dict keys must be strings")
            position = _measure(position + 2 + len(key.encode("utf-8")), value[key])
        return position
    if _is_sequence(value):
        position += 1 + 4
        for item in value:
            position = _measure(position, item)
        return position
    return _measure(position, np.asarray(value))


def _write_value(view: memoryview, base: int, position: int, value: Any) -> int:
    """Write ``value`` at payload ``position``; ``base`` is the payload start."""
    if isinstance(value, np.ndarray):
        return _write_array(view, base, position, value)
    if isinstance(value, str):
        return _write_string(view, base, position, value)
    if isinstance(value, Mapping):
        return _write_dict(view, base, position, value)
    if _is_sequence(value):
        return _write_list(view, base, position, value)
    return _write_array(view, base, position, np.asarray(value))


def _put(view: memoryview, base: int, position: int, raw) -> int:
    end = position + len(raw)
    view[base + position : base + end] = raw
    return end


def _pad(view: memoryview, base: int, position: int) -> int:
    end = _align_to_eight(position)
    view[base + position : base + end] = bytes(end - position)
    return end


def _write_array(view: memoryview, base: int, position: int, array: np.ndarray) -> int:
    dtype_code, wire_dtype = _wire_dtype(array.dtype)
    # Scalars become one-element vectors here. Raw bytes come straight from
    # the contiguous little-endian array; no intermediate bytes object is made.
    wire_array = np.ascontiguousarray(array, dtype=wire_dtype)
    if wire_array.ndim > 255:
        raise ValueError(f"too many nested array dimensions: {wire_array.ndim}")
    raw = wire_array.reshape(-1).view(np.uint8)
    checksum = xxhash.xxh64_intdigest(raw, seed=_CHECKSUM_SEED)
    header = struct.pack(
        f"<BBB{wire_array.ndim}QQ",
        _TAG_ARRAY,
        dtype_code,
        wire_array.ndim,
        *wire_array.shape,
        checksum,
    )
    position = _pad(view, base, _put(view, base, position, header))
    return _put(view, base, position, raw)


def _write_string(view: memoryview, base: int, position: int, value: str) -> int:
    raw = value.encode("utf-8")
    checksum = xxhash.xxh64_intdigest(raw, seed=_CHECKSUM_SEED)
    header = struct.pack("<BBBIQ", _TAG_ARRAY, _DTYPE_STRING, 0, len(raw), checksum)
    position = _pad(view, base, _put(view, base, position, header))
    return _put(view, base, position, raw)


def _write_dict(
    view: memoryview, base: int, position: int, value: Mapping[Any, Any]
) -> int:
    position = _put(view, base, position, struct.pack("<BI", _TAG_DICT, len(value)))
    for key, item in value.items():
        if not isinstance(key, str):
            raise TypeError("nested dict keys must be strings")
        encoded_key = key.encode("utf-8")
        if len(encoded_key) > 65535:
            raise ValueError("nested dict key is too long")
        position = _put(
            view, base, position, struct.pack("<H", len(encoded_key)) + encoded_key
        )
        position = _write_value(view, base, position, item)
    return position


def _write_list(
    view: memoryview, base: int, position: int, value: Sequence[Any]
) -> int:
    position = _put(view, base, position, struct.pack("<BI", _TAG_LIST, len(value)))
    for item in value:
        position = _write_value(view, base, position, item)
    return position


def _read_value(reader: _Reader) -> Any:
    tag = reader.read_u8()
    if tag == _TAG_ARRAY:
        return _read_array(reader)
    if tag == _TAG_DICT:
        return _read_dict(reader)
    if tag == _TAG_LIST:
        return _read_list(reader)
    raise ValueError(f"unknown nested payload tag: {tag}")


def _read_array(reader: _Reader) -> np.ndarray[Any, Any] | str:
    dtype_code = reader.read_u8()
    ndim = reader.read_u8()
    shape = tuple(reader.read_u64() for _ in range(ndim))

    if dtype_code == _DTYPE_STRING:
        if ndim != 0:
            raise ValueError("nested string payload must be scalar")
        length = reader.read_u32()
        checksum = reader.read_u64()
        reader.align_to_eight()
        raw = reader.read(length)
        _verify_checksum(raw, checksum)
        return raw.decode("utf-8")

    dtype = _DECODABLE_DTYPES.get(dtype_code)
    if dtype is None:
        raise ValueError(f"unknown nested dtype code: {dtype_code}")

    checksum = reader.read_u64()
    reader.align_to_eight()
    item_count = math.prod(shape) if shape else 1
    raw = reader.read(item_count * dtype.itemsize)
    _verify_checksum(raw, checksum)
    array = np.frombuffer(raw, dtype=dtype).copy()
    return array.reshape(shape)


def _read_dict(reader: _Reader) -> dict[str, Any]:
    count = reader.read_u32()
    return {reader.read_key(): _read_value(reader) for _ in range(count)}


def _read_list(reader: _Reader) -> list[Any]:
    count = reader.read_u32()
    return [_read_value(reader) for _ in range(count)]


def _wire_dtype(dtype: np.dtype[Any]) -> tuple[int, np.dtype[Any]]:
    normalized = np.dtype(dtype).newbyteorder("=")
    try:
        return _ENCODABLE_DTYPES[normalized]
    except KeyError as exc:
        raise TypeError(f"unsupported nested dtype: {dtype}") from exc


def _verify_checksum(data: bytes, checksum: int) -> None:
    actual = xxhash.xxh64_intdigest(data, seed=_CHECKSUM_SEED)
    if actual != checksum:
        raise ValueError("nested payload checksum mismatch")


def _align_to_eight(offset: int) -> int:
    return (offset + 7) & ~7


def _is_sequence(value: Any) -> bool:
    return isinstance(value, Sequence) and not isinstance(
        value, str | bytes | bytearray
    )
