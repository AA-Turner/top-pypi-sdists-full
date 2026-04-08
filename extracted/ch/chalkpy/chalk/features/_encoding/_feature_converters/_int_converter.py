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


_INT32_PRIMITIVE_CONVERTER = PrimitiveFeatureConverter(name="", is_nullable=True, pyarrow_dtype=pa.int32())
_INT64_PRIMITIVE_CONVERTER = PrimitiveFeatureConverter(name="", is_nullable=True, pyarrow_dtype=pa.int64())


class _IntFeatureConverterBase(
    _ScalarConverterBase[int, int],
    _FeatureConverterArrowProtoHelpers,
    FeatureConverter[int, int],
):
    _rich_type_value: ClassVar[Type[int]] = int
    _primitive_type_value: ClassVar[Type[int]] = int
    _primitive_converter: ClassVar[PrimitiveFeatureConverter]

    _coerce_fn = staticmethod(int)

    def from_primitive_to_rich(self, value: int | None) -> int:
        if value is None or value is ...:
            return cast(int, value)
        return int(cast(Any, value))

    def from_primitive_to_protobuf(self, value: int | pa.Scalar) -> pb.ScalarValue:
        pa_type = type(self)._pyarrow_dtype_value
        scalar_value = _unwrap_scalar_value(value)
        if scalar_value is None or scalar_value is ...:
            return pb.ScalarValue(null_value=self.convert_pa_dtype_to_proto_dtype(pa_type))
        return type(self)._primitive_converter.from_pyarrow_to_protobuf(
            pa.scalar(cast(int, scalar_value), type=pa_type)
        )

    def from_rich_to_protobuf(
        self,
        value: int | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pb.ScalarValue:
        pa_type = type(self)._pyarrow_dtype_value
        prim = cast(int | None, self.from_rich_to_primitive(value, missing_value_strategy))
        if prim is None or prim is ...:
            return pb.ScalarValue(null_value=self.convert_pa_dtype_to_proto_dtype(pa_type))
        return type(self)._primitive_converter.from_pyarrow_to_protobuf(
            pa.scalar(prim, type=pa_type)
        )

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar:
        return type(self)._primitive_converter.from_protobuf_to_pyarrow(pb_value)

    def from_pyarrow_to_protobuf(self, value: pa.Scalar) -> pb.ScalarValue:
        return type(self)._primitive_converter.from_pyarrow_to_protobuf(value)


class Int32FeatureConverter(_IntFeatureConverterBase):
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.int32()
    _polars_dtype_value: ClassVar[Any] = pl.Int32() if pl is not None else None
    _primitive_converter: ClassVar[PrimitiveFeatureConverter] = _INT32_PRIMITIVE_CONVERTER


class Int64FeatureConverter(_IntFeatureConverterBase):
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.int64()
    _polars_dtype_value: ClassVar[Any] = pl.Int64() if pl is not None else None
    _primitive_converter: ClassVar[PrimitiveFeatureConverter] = _INT64_PRIMITIVE_CONVERTER
