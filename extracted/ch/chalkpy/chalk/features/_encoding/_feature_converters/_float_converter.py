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
from ._primitive_converter import _FeatureConverterArrowProtoHelpers, PrimitiveFeatureConverter

# pyright: reportPrivateUsage=false, reportIncompatibleMethodOverride=false, reportReturnType=false, reportUnnecessaryCast=false, reportUnnecessaryComparison=false

try:
    import polars as pl
except ImportError:
    pl = None


_FLOAT32_PRIMITIVE_CONVERTER = PrimitiveFeatureConverter(name="", is_nullable=True, pyarrow_dtype=pa.float32())
_FLOAT64_PRIMITIVE_CONVERTER = PrimitiveFeatureConverter(name="", is_nullable=True, pyarrow_dtype=pa.float64())


class _FloatFeatureConverterBase(
    _ScalarConverterBase[float, float],
    _FeatureConverterArrowProtoHelpers,
    FeatureConverter[float, float],
):
    _rich_type_value: ClassVar[Type[float]] = float
    _primitive_type_value: ClassVar[Type[float]] = float
    _primitive_converter: ClassVar[PrimitiveFeatureConverter]

    _coerce_fn = staticmethod(float)

    def from_primitive_to_rich(self, value: float | None) -> float:
        if value is None or value is ...:
            return cast(float, value)
        return float(cast(Any, value))

    def from_primitive_to_protobuf(self, value: float | pa.Scalar) -> pb.ScalarValue:
        pa_type = type(self)._pyarrow_dtype_value
        scalar_value = _unwrap_scalar_value(value)
        if scalar_value is None or scalar_value is ...:
            return pb.ScalarValue(null_value=self.convert_pa_dtype_to_proto_dtype(pa_type))
        return type(self)._primitive_converter.from_pyarrow_to_protobuf(
            pa.scalar(cast(float, scalar_value), type=pa_type)
        )

    def from_rich_to_protobuf(
        self,
        value: float | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pb.ScalarValue:
        pa_type = type(self)._pyarrow_dtype_value
        prim = cast(float | None, self.from_rich_to_primitive(value, missing_value_strategy))
        if prim is None or prim is ...:
            return pb.ScalarValue(null_value=self.convert_pa_dtype_to_proto_dtype(pa_type))
        return type(self)._primitive_converter.from_pyarrow_to_protobuf(
            pa.scalar(prim, type=pa_type)
        )

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar:
        return type(self)._primitive_converter.from_protobuf_to_pyarrow(pb_value)

    def from_pyarrow_to_protobuf(self, value: pa.Scalar) -> pb.ScalarValue:
        return type(self)._primitive_converter.from_pyarrow_to_protobuf(value)


class Float32FeatureConverter(_FloatFeatureConverterBase):
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.float32()
    _polars_dtype_value: ClassVar[Any] = pl.Float32() if pl is not None else None
    _primitive_converter: ClassVar[PrimitiveFeatureConverter] = _FLOAT32_PRIMITIVE_CONVERTER


class Float64FeatureConverter(_FloatFeatureConverterBase):
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.float64()
    _polars_dtype_value: ClassVar[Any] = pl.Float64() if pl is not None else None
    _primitive_converter: ClassVar[PrimitiveFeatureConverter] = _FLOAT64_PRIMITIVE_CONVERTER
