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


_STR_PRIMITIVE_CONVERTER_UTF8 = PrimitiveFeatureConverter(name="", is_nullable=True, pyarrow_dtype=pa.utf8())
_STR_PRIMITIVE_CONVERTER_LARGE = PrimitiveFeatureConverter(name="", is_nullable=True, pyarrow_dtype=pa.large_string())


def _coerce_str(x: Any) -> str:
    """Convert x to str, rejecting container types and bare object instances."""
    if type(x) is str:
        return x
    if isinstance(x, (dict, list, tuple)) or type(x) is object:
        raise TypeError(f"Object {x!r} of type {type(x).__name__} cannot be converted into a str")
    return str(x)


class _StringFeatureConverterBase(
    _ScalarConverterBase[str, str],
    _FeatureConverterArrowProtoHelpers,
    FeatureConverter[str, str],
):
    _rich_type_value: ClassVar[Type[str]] = str
    _primitive_type_value: ClassVar[Type[str]] = str
    _primitive_converter: ClassVar[PrimitiveFeatureConverter]

    _coerce_fn = staticmethod(_coerce_str)

    def from_primitive_to_rich(self, value: str | None) -> str:
        if value is None:
            return cast(str, None)
        return str(value)

    def from_primitive_to_protobuf(self, value: str | pa.Scalar) -> pb.ScalarValue:
        pa_type = type(self)._pyarrow_dtype_value
        scalar_value = _unwrap_scalar_value(value)
        if scalar_value is None or scalar_value is ...:
            return pb.ScalarValue(null_value=self.convert_pa_dtype_to_proto_dtype(pa_type))
        return type(self)._primitive_converter.from_pyarrow_to_protobuf(
            pa.scalar(cast(str, scalar_value), type=pa_type)
        )

    def from_rich_to_protobuf(
        self,
        value: str | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pb.ScalarValue:
        pa_type = type(self)._pyarrow_dtype_value
        prim = cast(str | None, self.from_rich_to_primitive(value, missing_value_strategy))
        if prim is None or prim is ...:
            return pb.ScalarValue(null_value=self.convert_pa_dtype_to_proto_dtype(pa_type))
        return type(self)._primitive_converter.from_pyarrow_to_protobuf(
            pa.scalar(prim, type=pa_type)
        )

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar:
        return type(self)._primitive_converter.from_protobuf_to_pyarrow(pb_value)

    def from_pyarrow_to_protobuf(self, value: pa.Scalar) -> pb.ScalarValue:
        return type(self)._primitive_converter.from_pyarrow_to_protobuf(value)


class StringFeatureConverter(_StringFeatureConverterBase):
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.utf8()
    _polars_dtype_value: ClassVar[Any] = pl.Utf8() if pl is not None else None
    _primitive_converter: ClassVar[PrimitiveFeatureConverter] = _STR_PRIMITIVE_CONVERTER_UTF8


class LargeStringFeatureConverter(_StringFeatureConverterBase):
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.large_string()
    _polars_dtype_value: ClassVar[Any] = pl.Utf8() if pl is not None else None
    _primitive_converter: ClassVar[PrimitiveFeatureConverter] = _STR_PRIMITIVE_CONVERTER_LARGE
