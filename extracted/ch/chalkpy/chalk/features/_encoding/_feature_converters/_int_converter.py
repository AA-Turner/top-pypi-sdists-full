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


class Int32FeatureConverter(
    _ScalarConverterBase[int, int],
    FeatureConverter[int, int],
):
    _rich_type_value: ClassVar[Type[int]] = int
    _primitive_type_value: ClassVar[Type[int]] = int
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.int32()
    _proto_arrow_type: ClassVar[pb.ArrowType] = pb.ArrowType(int32=pb.EmptyMessage())
    _polars_dtype_value: ClassVar[Any] = pl.Int32() if pl is not None else None

    _coerce_fn = staticmethod(int)

    def from_primitive_to_rich(self, value: int | None) -> int:
        if value is None or value is ...:
            return cast(int, value)
        return int(cast(Any, value))

    def from_primitive_to_protobuf(self, value: int | pa.Scalar) -> pb.ScalarValue:
        scalar_value = _unwrap_scalar_value(value)
        if scalar_value is None or scalar_value is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(int32=pb.EmptyMessage()))
        return self.from_pyarrow_to_protobuf(pa.scalar(cast(int, scalar_value), type=pa.int32()))

    def from_rich_to_protobuf(
        self,
        value: int | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pb.ScalarValue:
        prim = cast(int | None, self.from_rich_to_primitive(value, missing_value_strategy))
        if prim is None or prim is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(int32=pb.EmptyMessage()))
        return self.from_pyarrow_to_protobuf(pa.scalar(prim, type=pa.int32()))

    def from_pyarrow_to_protobuf(self, value: pa.Scalar) -> pb.ScalarValue:
        if value.as_py() is None:
            return pb.ScalarValue(null_value=pb.ArrowType(int32=pb.EmptyMessage()))
        return pb.ScalarValue(int32_value=value.as_py())

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar:
        if pb_value.HasField("null_value"):
            return pa.nulls(1, type=pa.int32())[0]
        return pa.scalar(pb_value.int32_value, pa.int32())


class Int64FeatureConverter(
    _ScalarConverterBase[int, int],
    FeatureConverter[int, int],
):
    _rich_type_value: ClassVar[Type[int]] = int
    _primitive_type_value: ClassVar[Type[int]] = int
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.int64()
    _proto_arrow_type: ClassVar[pb.ArrowType] = pb.ArrowType(int64=pb.EmptyMessage())
    _polars_dtype_value: ClassVar[Any] = pl.Int64() if pl is not None else None

    _coerce_fn = staticmethod(int)

    def from_primitive_to_rich(self, value: int | None) -> int:
        if value is None or value is ...:
            return cast(int, value)
        return int(cast(Any, value))

    def from_primitive_to_protobuf(self, value: int | pa.Scalar) -> pb.ScalarValue:
        scalar_value = _unwrap_scalar_value(value)
        if scalar_value is None or scalar_value is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(int64=pb.EmptyMessage()))
        return self.from_pyarrow_to_protobuf(pa.scalar(cast(int, scalar_value), type=pa.int64()))

    def from_rich_to_protobuf(
        self,
        value: int | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pb.ScalarValue:
        prim = cast(int | None, self.from_rich_to_primitive(value, missing_value_strategy))
        if prim is None or prim is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(int64=pb.EmptyMessage()))
        return self.from_pyarrow_to_protobuf(pa.scalar(prim, type=pa.int64()))

    def from_pyarrow_to_protobuf(self, value: pa.Scalar) -> pb.ScalarValue:
        if value.as_py() is None:
            return pb.ScalarValue(null_value=pb.ArrowType(int64=pb.EmptyMessage()))
        return pb.ScalarValue(int64_value=value.as_py())

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar:
        if pb_value.HasField("null_value"):
            return pa.nulls(1, type=pa.int64())[0]
        return pa.scalar(pb_value.int64_value, pa.int64())
