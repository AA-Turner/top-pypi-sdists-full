from __future__ import annotations

from typing import (
    Any,
    ClassVar,
    Type,
    cast,
)

import pyarrow as pa

try:
    import polars as pl
except ImportError:
    pl = None  # type: ignore[assignment]

from chalk._gen.chalk.arrow.v1 import arrow_pb2 as pb
from chalk.features._encoding.missing_value import MissingValueStrategy

from ._base import (
    _ScalarConverterBase,
    _unwrap_scalar_value,
    FeatureConverter,
)

# pyright: reportPrivateUsage=false, reportIncompatibleMethodOverride=false, reportReturnType=false, reportUnnecessaryCast=false, reportUnnecessaryComparison=false

class _IntConverterBase(
    _ScalarConverterBase[int, int],
    FeatureConverter[int, int],
):
    """Shared base for all integer-width converters (int8–int64, uint8–uint64).

    Subclasses only need to set six ClassVars; all conversion logic is provided here:
      _rich_type_value, _primitive_type_value, _pyarrow_dtype_value,
      _proto_arrow_type, _proto_value_field, _polars_dtype_value
    """

    # Subclasses set this to e.g. "int32_value", "uint8_value"
    _proto_value_field: ClassVar[str]

    _coerce_fn = staticmethod(int)

    def from_primitive_to_rich(self, value: int | None) -> int:
        if value is None or value is ...:
            return cast(int, value)
        return int(cast(Any, value))

    def from_primitive_to_protobuf(self, value: int | pa.Scalar) -> pb.ScalarValue:
        scalar_value = _unwrap_scalar_value(value)
        if scalar_value is None or scalar_value is ...:
            return pb.ScalarValue(null_value=type(self)._proto_arrow_type)
        return self.from_pyarrow_to_protobuf(pa.scalar(int(scalar_value), type=type(self)._pyarrow_dtype_value))

    def from_rich_to_protobuf(
        self,
        value: int | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pb.ScalarValue:
        prim = cast(int | None, self.from_rich_to_primitive(value, missing_value_strategy))
        if prim is None or prim is ...:
            return pb.ScalarValue(null_value=type(self)._proto_arrow_type)
        return self.from_pyarrow_to_protobuf(pa.scalar(prim, type=type(self)._pyarrow_dtype_value))

    def from_pyarrow_to_protobuf(self, value: pa.Scalar) -> pb.ScalarValue:
        if value.as_py() is None:
            return pb.ScalarValue(null_value=type(self)._proto_arrow_type)
        return pb.ScalarValue(**{type(self)._proto_value_field: value.as_py()})

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar:
        pa_type = type(self)._pyarrow_dtype_value
        if pb_value.HasField("null_value"):
            return pa.nulls(1, type=pa_type)[0]
        return pa.scalar(getattr(pb_value, type(self)._proto_value_field), pa_type)


class Int8FeatureConverter(_IntConverterBase):
    _rich_type_value: ClassVar[Type[int]] = int
    _primitive_type_value: ClassVar[Type[int]] = int
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.int8()
    _proto_arrow_type: ClassVar[pb.ArrowType] = pb.ArrowType(int8=pb.EmptyMessage())
    _proto_value_field: ClassVar[str] = "int8_value"
    _polars_dtype_value: ClassVar[Any] = pl.Int8() if pl is not None else None


class Int16FeatureConverter(_IntConverterBase):
    _rich_type_value: ClassVar[Type[int]] = int
    _primitive_type_value: ClassVar[Type[int]] = int
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.int16()
    _proto_arrow_type: ClassVar[pb.ArrowType] = pb.ArrowType(int16=pb.EmptyMessage())
    _proto_value_field: ClassVar[str] = "int16_value"
    _polars_dtype_value: ClassVar[Any] = pl.Int16() if pl is not None else None


class Int32FeatureConverter(_IntConverterBase):
    _rich_type_value: ClassVar[Type[int]] = int
    _primitive_type_value: ClassVar[Type[int]] = int
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.int32()
    _proto_arrow_type: ClassVar[pb.ArrowType] = pb.ArrowType(int32=pb.EmptyMessage())
    _proto_value_field: ClassVar[str] = "int32_value"
    _polars_dtype_value: ClassVar[Any] = pl.Int32() if pl is not None else None


class Int64FeatureConverter(_IntConverterBase):
    _rich_type_value: ClassVar[Type[int]] = int
    _primitive_type_value: ClassVar[Type[int]] = int
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.int64()
    _proto_arrow_type: ClassVar[pb.ArrowType] = pb.ArrowType(int64=pb.EmptyMessage())
    _proto_value_field: ClassVar[str] = "int64_value"
    _polars_dtype_value: ClassVar[Any] = pl.Int64() if pl is not None else None


class UInt8FeatureConverter(_IntConverterBase):
    _rich_type_value: ClassVar[Type[int]] = int
    _primitive_type_value: ClassVar[Type[int]] = int
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.uint8()
    _proto_arrow_type: ClassVar[pb.ArrowType] = pb.ArrowType(uint8=pb.EmptyMessage())
    _proto_value_field: ClassVar[str] = "uint8_value"
    _polars_dtype_value: ClassVar[Any] = pl.UInt8() if pl is not None else None


class UInt16FeatureConverter(_IntConverterBase):
    _rich_type_value: ClassVar[Type[int]] = int
    _primitive_type_value: ClassVar[Type[int]] = int
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.uint16()
    _proto_arrow_type: ClassVar[pb.ArrowType] = pb.ArrowType(uint16=pb.EmptyMessage())
    _proto_value_field: ClassVar[str] = "uint16_value"
    _polars_dtype_value: ClassVar[Any] = pl.UInt16() if pl is not None else None


class UInt32FeatureConverter(_IntConverterBase):
    _rich_type_value: ClassVar[Type[int]] = int
    _primitive_type_value: ClassVar[Type[int]] = int
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.uint32()
    _proto_arrow_type: ClassVar[pb.ArrowType] = pb.ArrowType(uint32=pb.EmptyMessage())
    _proto_value_field: ClassVar[str] = "uint32_value"
    _polars_dtype_value: ClassVar[Any] = pl.UInt32() if pl is not None else None


class UInt64FeatureConverter(_IntConverterBase):
    _rich_type_value: ClassVar[Type[int]] = int
    _primitive_type_value: ClassVar[Type[int]] = int
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.uint64()
    _proto_arrow_type: ClassVar[pb.ArrowType] = pb.ArrowType(uint64=pb.EmptyMessage())
    _proto_value_field: ClassVar[str] = "uint64_value"
    _polars_dtype_value: ClassVar[Any] = pl.UInt64() if pl is not None else None
