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
    output = bytearray(_HEADER)
    _write_value(output, value)
    return bytes(output)


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


def _write_value(output: bytearray, value: Any) -> None:
    if isinstance(value, np.ndarray):
        _write_array(output, value)
    elif isinstance(value, str):
        _write_string(output, value)
    elif isinstance(value, Mapping):
        _write_dict(output, value)
    elif _is_sequence(value):
        _write_list(output, value)
    else:
        _write_array(output, np.asarray(value))


def _write_array(output: bytearray, array: np.ndarray) -> None:
    dtype_code, wire_dtype = _wire_dtype(array.dtype)
    wire_array = np.ascontiguousarray(array, dtype=wire_dtype)
    raw = wire_array.tobytes(order="C")
    checksum = xxhash.xxh64_intdigest(raw, seed=_CHECKSUM_SEED)

    if wire_array.ndim > 255:
        raise ValueError(f"too many nested array dimensions: {wire_array.ndim}")

    output.append(_TAG_ARRAY)
    output.append(dtype_code)
    output.append(wire_array.ndim)
    for dim in wire_array.shape:
        output.extend(struct.pack("<Q", int(dim)))
    output.extend(struct.pack("<Q", checksum))
    _pad_to_eight(output)
    output.extend(raw)


def _write_string(output: bytearray, value: str) -> None:
    raw = value.encode("utf-8")
    checksum = xxhash.xxh64_intdigest(raw, seed=_CHECKSUM_SEED)

    output.append(_TAG_ARRAY)
    output.append(_DTYPE_STRING)
    output.append(0)
    output.extend(struct.pack("<I", len(raw)))
    output.extend(struct.pack("<Q", checksum))
    _pad_to_eight(output)
    output.extend(raw)


def _write_dict(output: bytearray, value: Mapping[Any, Any]) -> None:
    output.append(_TAG_DICT)
    output.extend(struct.pack("<I", len(value)))
    for key, item in value.items():
        if not isinstance(key, str):
            raise TypeError("nested dict keys must be strings")
        encoded_key = key.encode("utf-8")
        if len(encoded_key) > 65535:
            raise ValueError("nested dict key is too long")
        output.extend(struct.pack("<H", len(encoded_key)))
        output.extend(encoded_key)
        _write_value(output, item)


def _write_list(output: bytearray, value: Sequence[Any]) -> None:
    output.append(_TAG_LIST)
    output.extend(struct.pack("<I", len(value)))
    for item in value:
        _write_value(output, item)


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


def _pad_to_eight(output: bytearray) -> None:
    output.extend(b"\0" * (_align_to_eight(len(output)) - len(output)))


def _align_to_eight(offset: int) -> int:
    return (offset + 7) & ~7


def _is_sequence(value: Any) -> bool:
    return isinstance(value, Sequence) and not isinstance(
        value, str | bytes | bytearray
    )
