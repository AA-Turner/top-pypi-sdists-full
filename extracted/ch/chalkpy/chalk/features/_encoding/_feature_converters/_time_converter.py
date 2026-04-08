from __future__ import annotations

from datetime import time
from typing import (
    Any,
    ClassVar,
    Sequence,
    Type,
    cast,
)

import isodate
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

from ._primitive_converter import _FeatureConverterArrowProtoHelpers, PrimitiveFeatureConverter

# pyright: reportPrivateUsage=false, reportIncompatibleMethodOverride=false, reportReturnType=false, reportUnnecessaryCast=false, reportUnnecessaryComparison=false

try:
    import polars as pl
except ImportError:
    pl = None


def _coerce_time(x: Any) -> time:
    """Convert x to time, matching the structuring logic in rich.py/_structure_time and json.py/_structure_time.

    Both the rich and JSON converters for time behave identically: accept time objects
    (passthrough) and ISO strings (via isodate.parse_time), reject everything else.
    Unlike date/datetime, there is no divergence between the JSON and rich paths.
    """
    if isinstance(x, time):
        return x
    if isinstance(x, str):
        return isodate.parse_time(x)
    raise TypeError(f"Cannot convert '{x}' to a time")


_TIME32_S_PRIMITIVE_CONVERTER = PrimitiveFeatureConverter(name="", is_nullable=True, pyarrow_dtype=pa.time32("s"))
_TIME32_MS_PRIMITIVE_CONVERTER = PrimitiveFeatureConverter(name="", is_nullable=True, pyarrow_dtype=pa.time32("ms"))
_TIME64_US_PRIMITIVE_CONVERTER = PrimitiveFeatureConverter(name="", is_nullable=True, pyarrow_dtype=pa.time64("us"))
_TIME64_NS_PRIMITIVE_CONVERTER = PrimitiveFeatureConverter(name="", is_nullable=True, pyarrow_dtype=pa.time64("ns"))


class _TimeFeatureConverterBase(
    _ScalarConverterBase[time, time],
    _FeatureConverterArrowProtoHelpers,
    FeatureConverter[time, time],
):
    _rich_type_value: ClassVar[Type[time]] = time
    _primitive_type_value: ClassVar[Type[time]] = time
    _primitive_converter: ClassVar[PrimitiveFeatureConverter]

    _coerce_fn = staticmethod(_coerce_time)
    _use_fast_path = False

    def _serialize_to_json(self, x: Any) -> TJSON:
        return cast(time, x).isoformat()

    def from_pyarrow_to_json(
        self,
        values: pa.Array | pa.ChunkedArray,
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> Sequence[TJSON]:
        return [None if v is None else v.isoformat() for v in values.to_pylist()]

    def from_primitive_to_json(
        self,
        value: TPrimitive,
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> TJSON:
        if value is ...:
            return cast(TJSON, ...)
        if value is None:
            return None
        return cast(time, value).isoformat()

    def from_primitive_to_protobuf(self, value: time | pa.Scalar) -> pb.ScalarValue:
        pa_type = type(self)._pyarrow_dtype_value
        scalar_value = _unwrap_scalar_value(value)
        if scalar_value is None or scalar_value is ...:
            return pb.ScalarValue(null_value=self.convert_pa_dtype_to_proto_dtype(pa_type))
        return type(self)._primitive_converter.from_pyarrow_to_protobuf(
            pa.scalar(cast(time, scalar_value), type=pa_type)
        )

    def from_rich_to_protobuf(
        self,
        value: time | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pb.ScalarValue:
        pa_type = type(self)._pyarrow_dtype_value
        prim = cast(time | None, self.from_rich_to_primitive(value, missing_value_strategy))
        if prim is None or prim is ...:
            return pb.ScalarValue(null_value=self.convert_pa_dtype_to_proto_dtype(pa_type))
        return type(self)._primitive_converter.from_pyarrow_to_protobuf(
            pa.scalar(prim, type=pa_type)
        )

    def from_primitive_to_rich(self, value: time | None) -> time:
        if value is None:
            return cast(time, None)
        return cast(time, value)

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar:
        return type(self)._primitive_converter.from_protobuf_to_pyarrow(pb_value)

    def from_pyarrow_to_protobuf(self, value: pa.Scalar) -> pb.ScalarValue:
        return type(self)._primitive_converter.from_pyarrow_to_protobuf(value)


class Time32sFeatureConverter(_TimeFeatureConverterBase):
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.time32("s")
    _polars_dtype_value: ClassVar[Any] = pl.Time() if pl is not None else None
    _primitive_converter: ClassVar[PrimitiveFeatureConverter] = _TIME32_S_PRIMITIVE_CONVERTER


class Time32msFeatureConverter(_TimeFeatureConverterBase):
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.time32("ms")
    _polars_dtype_value: ClassVar[Any] = pl.Time() if pl is not None else None
    _primitive_converter: ClassVar[PrimitiveFeatureConverter] = _TIME32_MS_PRIMITIVE_CONVERTER


class Time64usFeatureConverter(_TimeFeatureConverterBase):
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.time64("us")
    _polars_dtype_value: ClassVar[Any] = pl.Time() if pl is not None else None
    _primitive_converter: ClassVar[PrimitiveFeatureConverter] = _TIME64_US_PRIMITIVE_CONVERTER


class Time64nsFeatureConverter(_TimeFeatureConverterBase):
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.time64("ns")
    _polars_dtype_value: ClassVar[Any] = pl.Time() if pl is not None else None
    _primitive_converter: ClassVar[PrimitiveFeatureConverter] = _TIME64_NS_PRIMITIVE_CONVERTER
