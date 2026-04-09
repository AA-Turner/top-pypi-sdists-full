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


class Float32FeatureConverter(
    _ScalarConverterBase[float, float],
    FeatureConverter[float, float],
):
    _rich_type_value: ClassVar[Type[float]] = float
    _primitive_type_value: ClassVar[Type[float]] = float
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.float32()
    _proto_arrow_type: ClassVar[pb.ArrowType] = pb.ArrowType(float32=pb.EmptyMessage())
    _polars_dtype_value: ClassVar[Any] = pl.Float32() if pl is not None else None

    _coerce_fn = staticmethod(float)

    def from_primitive_to_rich(self, value: float | None) -> float:
        if value is None or value is ...:
            return cast(float, value)
        return float(cast(Any, value))

    def from_primitive_to_protobuf(self, value: float | pa.Scalar) -> pb.ScalarValue:
        scalar_value = _unwrap_scalar_value(value)
        if scalar_value is None or scalar_value is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(float32=pb.EmptyMessage()))
        return self.from_pyarrow_to_protobuf(pa.scalar(cast(float, scalar_value), type=pa.float32()))

    def from_rich_to_protobuf(
        self,
        value: float | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pb.ScalarValue:
        prim = cast(float | None, self.from_rich_to_primitive(value, missing_value_strategy))
        if prim is None or prim is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(float32=pb.EmptyMessage()))
        return self.from_pyarrow_to_protobuf(pa.scalar(prim, type=pa.float32()))

    def from_pyarrow_to_protobuf(self, value: pa.Scalar) -> pb.ScalarValue:
        if value.as_py() is None:
            return pb.ScalarValue(null_value=pb.ArrowType(float32=pb.EmptyMessage()))
        return pb.ScalarValue(float32_value=value.as_py())

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar:
        if pb_value.HasField("null_value"):
            return pa.nulls(1, type=pa.float32())[0]
        return pa.scalar(pb_value.float32_value, pa.float32())


class Float64FeatureConverter(
    _ScalarConverterBase[float, float],
    FeatureConverter[float, float],
):
    _rich_type_value: ClassVar[Type[float]] = float
    _primitive_type_value: ClassVar[Type[float]] = float
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.float64()
    _proto_arrow_type: ClassVar[pb.ArrowType] = pb.ArrowType(float64=pb.EmptyMessage())
    _polars_dtype_value: ClassVar[Any] = pl.Float64() if pl is not None else None

    _coerce_fn = staticmethod(float)

    def from_primitive_to_rich(self, value: float | None) -> float:
        if value is None or value is ...:
            return cast(float, value)
        return float(cast(Any, value))

    def from_primitive_to_protobuf(self, value: float | pa.Scalar) -> pb.ScalarValue:
        scalar_value = _unwrap_scalar_value(value)
        if scalar_value is None or scalar_value is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(float64=pb.EmptyMessage()))
        return self.from_pyarrow_to_protobuf(pa.scalar(cast(float, scalar_value), type=pa.float64()))

    def from_rich_to_protobuf(
        self,
        value: float | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pb.ScalarValue:
        prim = cast(float | None, self.from_rich_to_primitive(value, missing_value_strategy))
        if prim is None or prim is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(float64=pb.EmptyMessage()))
        return self.from_pyarrow_to_protobuf(pa.scalar(prim, type=pa.float64()))

    def from_pyarrow_to_protobuf(self, value: pa.Scalar) -> pb.ScalarValue:
        if value.as_py() is None:
            return pb.ScalarValue(null_value=pb.ArrowType(float64=pb.EmptyMessage()))
        return pb.ScalarValue(float64_value=value.as_py())

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar:
        if pb_value.HasField("null_value"):
            return pa.nulls(1, type=pa.float64())[0]
        return pa.scalar(pb_value.float64_value, pa.float64())
