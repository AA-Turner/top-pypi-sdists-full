from __future__ import annotations

import base64
from pyarrow import ArrowTypeError
from typing import (
    Any,
    ClassVar,
    Iterable,
    Sequence,
    Type,
    Union,
    cast,
)

import pyarrow as pa

from chalk._gen.chalk.arrow.v1 import arrow_pb2 as pb
from chalk.features._encoding.json import FeatureEncodingOptions
from chalk.features._encoding.missing_value import MissingValueStrategy
from chalk.features._encoding.primitive import TPrimitive
from chalk.utils.json import TJSON

from ._base import (
    _ScalarConverterBase,
    _DEFAULT_FEATURE_ENCODING_OPTIONS,
    _unwrap_scalar_value,
    FeatureConverter,
)

# pyright: reportPrivateUsage=false, reportIncompatibleMethodOverride=false, reportReturnType=false, reportUnnecessaryCast=false, reportUnnecessaryComparison=false

try:
    import polars as pl
except ImportError:
    pl = None


def _coerce_bytes(x: Any) -> bytes:
    """Convert x to bytes. Accepts bytes passthrough, pa.Buffer, and memoryview."""
    if isinstance(x, bytes):
        return x
    if isinstance(x, pa.Buffer):
        return x.to_pybytes()
    if isinstance(x, memoryview):
        return bytes(x)
    raise TypeError(f"Cannot convert '{type(x).__name__}' to bytes")


def _to_arrow_bytes(x: Any) -> "bytes | memoryview":
    """Like _coerce_bytes, but returns a zero-copy memoryview for pa.Buffer/memoryview instead of materializing."""
    if isinstance(x, bytes):
        return x
    if isinstance(x, pa.Buffer):
        return memoryview(x)
    if isinstance(x, memoryview):
        return x
    raise TypeError(f"Cannot convert '{type(x).__name__}' to bytes")


class BytesFeatureConverter(
    _ScalarConverterBase[bytes, bytes],
    FeatureConverter[bytes, bytes],
):
    _rich_type_value: ClassVar[Type[bytes]] = bytes
    _primitive_type_value: ClassVar[Type[bytes]] = bytes
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.binary()
    _proto_arrow_type: ClassVar[pb.ArrowType] = pb.ArrowType(binary=pb.EmptyMessage())
    _polars_dtype_value: ClassVar[Any] = pl.Binary() if pl is not None else None

    _coerce_fn = staticmethod(_coerce_bytes)
    _arrow_coerce_fn = staticmethod(_to_arrow_bytes)
    _use_fast_path = False

    def _serialize_to_json(self, x: Any) -> TJSON:
        return base64.b64encode(cast(bytes, x)).decode("utf-8")

    def from_pyarrow_to_json(
        self,
        values: pa.Array | pa.ChunkedArray,
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> Sequence[TJSON]:
        return [None if v is None else base64.b64encode(v).decode("utf-8") for v in values.to_pylist()]

    def from_primitive_to_pyarrow(self, value: Iterable[bytes]) -> Union[pa.Array, pa.ChunkedArray]:
        if isinstance(value, (tuple, list)):
            try:
                return pa.array(value, type=pa.binary())
            except ArrowTypeError:
                return pa.array([None if x is ... else (None if x is None else _to_arrow_bytes(x)) for x in value], type=pa.binary())
        return pa.array([None if x is ... else (None if x is None else _to_arrow_bytes(x)) for x in value], type=pa.binary())

    def from_primitive_to_json(
        self,
        value: TPrimitive,
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> TJSON:
        if value is None or value is ...:
            return None
        return base64.b64encode(cast(bytes, value)).decode("utf-8")

    def from_json_to_pyarrow(self, values: Sequence[TJSON]) -> Union[pa.Array, pa.ChunkedArray]:
        return pa.array(
            [
                None if x is None or x is ... else (x if isinstance(x, bytes) else base64.b64decode(cast(Any, x)))
                for x in values
            ],
            type=pa.binary(),
        )

    def from_json_to_primitive(self, value: TJSON | TPrimitive) -> bytes:
        if value is None or value is ...:
            return cast(bytes, None)
        if isinstance(value, bytes):
            return value
        return base64.b64decode(cast(Any, value))

    def from_primitive_to_rich(self, value: bytes | None) -> bytes:
        if value is None:
            return cast(bytes, None)
        return cast(bytes, value)

    def from_primitive_to_protobuf(self, value: bytes | pa.Scalar) -> pb.ScalarValue:
        scalar_value = _unwrap_scalar_value(value)
        if scalar_value is None or scalar_value is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(binary=pb.EmptyMessage()))
        return self.from_pyarrow_to_protobuf(pa.scalar(cast(bytes, scalar_value), type=pa.binary()))

    def from_rich_to_protobuf(
        self,
        value: bytes | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pb.ScalarValue:
        prim = cast(bytes | None, self.from_rich_to_primitive(value, missing_value_strategy))
        if prim is None or prim is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(binary=pb.EmptyMessage()))
        return self.from_pyarrow_to_protobuf(pa.scalar(prim, type=pa.binary()))

    def from_pyarrow_to_protobuf(self, value: pa.Scalar) -> pb.ScalarValue:
        if value.as_py() is None:
            return pb.ScalarValue(null_value=pb.ArrowType(binary=pb.EmptyMessage()))
        return pb.ScalarValue(binary_value=value.as_py())

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar:
        if pb_value.HasField("null_value"):
            return pa.nulls(1, type=pa.binary())[0]
        return pa.scalar(pb_value.binary_value, pa.binary())


class LargeBinaryFeatureConverter(
    _ScalarConverterBase[bytes, bytes],
    FeatureConverter[bytes, bytes],
):
    _rich_type_value: ClassVar[Type[bytes]] = bytes
    _primitive_type_value: ClassVar[Type[bytes]] = bytes
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.large_binary()
    _proto_arrow_type: ClassVar[pb.ArrowType] = pb.ArrowType(large_binary=pb.EmptyMessage())
    _polars_dtype_value: ClassVar[Any] = pl.Binary() if pl is not None else None

    _coerce_fn = staticmethod(_coerce_bytes)
    _arrow_coerce_fn = staticmethod(_to_arrow_bytes)
    _use_fast_path = False

    def _serialize_to_json(self, x: Any) -> TJSON:
        return base64.b64encode(cast(bytes, x)).decode("utf-8")

    def from_pyarrow_to_json(
        self,
        values: pa.Array | pa.ChunkedArray,
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> Sequence[TJSON]:
        return [None if v is None else base64.b64encode(v).decode("utf-8") for v in values.to_pylist()]

    def from_primitive_to_pyarrow(self, value: Iterable[bytes]) -> Union[pa.Array, pa.ChunkedArray]:
        if isinstance(value, (tuple, list)):
            try:
                return pa.array(value, type=pa.large_binary())
            except ArrowTypeError:
                return pa.array([None if x is ... else (None if x is None else _to_arrow_bytes(x)) for x in value], type=pa.large_binary())
        return pa.array([None if x is ... else (None if x is None else _to_arrow_bytes(x)) for x in value], type=pa.large_binary())

    def from_primitive_to_json(
        self,
        value: TPrimitive,
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> TJSON:
        if value is None or value is ...:
            return None
        return base64.b64encode(cast(bytes, value)).decode("utf-8")

    def from_json_to_pyarrow(self, values: Sequence[TJSON]) -> Union[pa.Array, pa.ChunkedArray]:
        return pa.array(
            [
                None if x is None or x is ... else (x if isinstance(x, bytes) else base64.b64decode(cast(Any, x)))
                for x in values
            ],
            type=pa.large_binary(),
        )

    def from_json_to_primitive(self, value: TJSON | TPrimitive) -> bytes:
        if value is None or value is ...:
            return cast(bytes, None)
        if isinstance(value, bytes):
            return value
        return base64.b64decode(cast(Any, value))

    def from_primitive_to_rich(self, value: bytes | None) -> bytes:
        if value is None:
            return cast(bytes, None)
        return cast(bytes, value)

    def from_primitive_to_protobuf(self, value: bytes | pa.Scalar) -> pb.ScalarValue:
        scalar_value = _unwrap_scalar_value(value)
        if scalar_value is None or scalar_value is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(large_binary=pb.EmptyMessage()))
        return self.from_pyarrow_to_protobuf(pa.scalar(cast(bytes, scalar_value), type=pa.large_binary()))

    def from_rich_to_protobuf(
        self,
        value: bytes | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pb.ScalarValue:
        prim = cast(bytes | None, self.from_rich_to_primitive(value, missing_value_strategy))
        if prim is None or prim is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(large_binary=pb.EmptyMessage()))
        return self.from_pyarrow_to_protobuf(pa.scalar(prim, type=pa.large_binary()))

    def from_pyarrow_to_protobuf(self, value: pa.Scalar) -> pb.ScalarValue:
        if value.as_py() is None:
            return pb.ScalarValue(null_value=pb.ArrowType(large_binary=pb.EmptyMessage()))
        return pb.ScalarValue(large_binary_value=value.as_py())

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar:
        if pb_value.HasField("null_value"):
            return pa.nulls(1, type=pa.large_binary())[0]
        return pa.scalar(pb_value.large_binary_value, pa.large_binary())
