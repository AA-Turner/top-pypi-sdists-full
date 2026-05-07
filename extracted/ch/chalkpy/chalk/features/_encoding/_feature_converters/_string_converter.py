from __future__ import annotations

from typing import (
    Any,
    ClassVar,
    Type,
    cast,
)

import pyarrow as pa

from chalk._gen.chalk.arrow.v1 import arrow_pb2 as pb
from chalk.features._encoding.missing_value import MissingValueStrategy

from ._base import (
    _ScalarConverterBase,
    _unwrap_scalar_value,
    FeatureConverter,
)

# pyright: reportPrivateUsage=false, reportIncompatibleMethodOverride=false, reportReturnType=false, reportUnnecessaryCast=false, reportUnnecessaryComparison=false

try:
    import polars as pl
except ImportError:
    pl = None


def _coerce_str(x: Any) -> str:
    """Convert x to str, rejecting container types and bare object instances."""
    if type(x) is str:
        return x
    if isinstance(x, (dict, list, tuple)) or type(x) is object:
        raise TypeError(f"Object {x!r} of type {type(x).__name__} cannot be converted into a str")
    return str(x)


class StringFeatureConverter(
    _ScalarConverterBase[str, str],
    FeatureConverter[str, str],
):
    _rich_type_value: ClassVar[Type[str]] = str
    _primitive_type_value: ClassVar[Type[str]] = str
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.utf8()
    _proto_arrow_type: ClassVar[pb.ArrowType] = pb.ArrowType(utf8=pb.EmptyMessage())
    _polars_dtype_value: ClassVar[Any] = pl.Utf8() if pl is not None else None

    _coerce_fn = staticmethod(_coerce_str)

    def from_primitive_to_rich(self, value: str | None) -> str:
        if value is None:
            return cast(str, None)
        return str(value)

    def from_primitive_to_protobuf(self, value: str | pa.Scalar) -> pb.ScalarValue:
        scalar_value = _unwrap_scalar_value(value)
        if scalar_value is None or scalar_value is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(utf8=pb.EmptyMessage()))
        return self.from_pyarrow_to_protobuf(pa.scalar(cast(str, scalar_value), type=pa.utf8()))

    def from_rich_to_protobuf(
        self,
        value: str | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pb.ScalarValue:
        prim = cast(str | None, self.from_rich_to_primitive(value, missing_value_strategy))
        if prim is None or prim is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(utf8=pb.EmptyMessage()))
        return self.from_pyarrow_to_protobuf(pa.scalar(prim, type=pa.utf8()))

    def from_pyarrow_to_protobuf(self, value: pa.Scalar) -> pb.ScalarValue:
        if value.as_py() is None:
            return pb.ScalarValue(null_value=pb.ArrowType(utf8=pb.EmptyMessage()))
        return pb.ScalarValue(utf8_value=value.as_py())

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar:
        if pb_value.HasField("null_value"):
            return pa.nulls(1, type=pa.utf8())[0]
        return pa.scalar(pb_value.utf8_value, pa.utf8())


class LargeStringFeatureConverter(
    _ScalarConverterBase[str, str],
    FeatureConverter[str, str],
):
    _rich_type_value: ClassVar[Type[str]] = str
    _primitive_type_value: ClassVar[Type[str]] = str
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.large_string()
    _proto_arrow_type: ClassVar[pb.ArrowType] = pb.ArrowType(large_utf8=pb.EmptyMessage())
    _polars_dtype_value: ClassVar[Any] = pl.Utf8() if pl is not None else None

    _coerce_fn = staticmethod(_coerce_str)

    def from_primitive_to_rich(self, value: str | None) -> str:
        if value is None:
            return cast(str, None)
        return str(value)

    def from_primitive_to_protobuf(self, value: str | pa.Scalar) -> pb.ScalarValue:
        scalar_value = _unwrap_scalar_value(value)
        if scalar_value is None or scalar_value is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(large_utf8=pb.EmptyMessage()))
        return self.from_pyarrow_to_protobuf(pa.scalar(cast(str, scalar_value), type=pa.large_string()))

    def from_rich_to_protobuf(
        self,
        value: str | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pb.ScalarValue:
        prim = cast(str | None, self.from_rich_to_primitive(value, missing_value_strategy))
        if prim is None or prim is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(large_utf8=pb.EmptyMessage()))
        return self.from_pyarrow_to_protobuf(pa.scalar(prim, type=pa.large_string()))

    def from_pyarrow_to_protobuf(self, value: pa.Scalar) -> pb.ScalarValue:
        if value.as_py() is None:
            return pb.ScalarValue(null_value=pb.ArrowType(large_utf8=pb.EmptyMessage()))
        return pb.ScalarValue(large_utf8_value=value.as_py())

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar:
        if pb_value.HasField("null_value"):
            return pa.nulls(1, type=pa.large_string())[0]
        return pa.scalar(pb_value.large_utf8_value, pa.large_string())
