from __future__ import annotations

from datetime import time
from typing import (
    Any,
    ClassVar,
    Sequence,
    Type,
    cast,
)

import pyarrow as pa
from chalk_rs import parse_iso_time as _parse_iso_time

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


def _coerce_time(x: Any) -> time:
    """Convert x to time, matching the structuring logic in rich.py/_structure_time and json.py/_structure_time.

    Both the rich and JSON converters for time behave identically: accept time objects
    (passthrough) and ISO strings (via chalk_rs.parse_iso_time), reject everything else.
    Unlike date/datetime, there is no divergence between the JSON and rich paths.
    """
    if isinstance(x, time):
        return x
    if isinstance(x, str):
        return _parse_iso_time(x)
    raise TypeError(f"Cannot convert '{x}' to a time")


class _TimeFeatureConverterBase(
    _ScalarConverterBase[time, time],
    FeatureConverter[time, time],
):
    _rich_type_value: ClassVar[Type[time]] = time
    _primitive_type_value: ClassVar[Type[time]] = time

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

    def from_primitive_to_rich(self, value: time | None) -> time:
        if value is None:
            return cast(time, None)
        return cast(time, value)


class Time32sFeatureConverter(_TimeFeatureConverterBase):
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.time32("s")
    _proto_arrow_type: ClassVar[pb.ArrowType] = pb.ArrowType(time32=pb.TIME_UNIT_SECOND)
    _polars_dtype_value: ClassVar[Any] = None

    def from_primitive_to_protobuf(self, value: time | pa.Scalar) -> pb.ScalarValue:
        scalar_value = _unwrap_scalar_value(value)
        if scalar_value is None or scalar_value is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(time32=pb.TIME_UNIT_SECOND))
        return self.from_pyarrow_to_protobuf(pa.scalar(cast(time, scalar_value), type=pa.time32("s")))

    def from_rich_to_protobuf(
        self,
        value: time | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pb.ScalarValue:
        prim = cast(time | None, self.from_rich_to_primitive(value, missing_value_strategy))
        if prim is None or prim is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(time32=pb.TIME_UNIT_SECOND))
        return self.from_pyarrow_to_protobuf(pa.scalar(prim, type=pa.time32("s")))

    def from_pyarrow_to_protobuf(self, value: pa.Scalar) -> pb.ScalarValue:
        time_val = value.as_py()
        if time_val is None:
            return pb.ScalarValue(null_value=pb.ArrowType(time32=pb.TIME_UNIT_SECOND))
        if not isinstance(time_val, time):
            raise TypeError(f"Expected Python `time`, but got `{type(time_val).__name__}`")
        ms_since_midnight = (
            time_val.hour * 3_600_000
            + time_val.minute * 60_000
            + time_val.second * 1_000
            + time_val.microsecond // 1_000
        )
        return pb.ScalarValue(time32_value=pb.ScalarTime32Value(time32_second_value=ms_since_midnight // 1_000))

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar:
        if pb_value.HasField("null_value"):
            return pa.nulls(1, type=pa.time32("s"))[0]
        seconds = pb_value.time32_value.time32_second_value
        return pa.scalar(
            time(
                hour=seconds // 3600,
                minute=(seconds % 3600) // 60,
                second=seconds % 60,
            ),
            pa.time32("s"),
        )


class Time32msFeatureConverter(_TimeFeatureConverterBase):
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.time32("ms")
    _proto_arrow_type: ClassVar[pb.ArrowType] = pb.ArrowType(time32=pb.TIME_UNIT_MILLISECOND)
    _polars_dtype_value: ClassVar[Any] = None

    def from_primitive_to_protobuf(self, value: time | pa.Scalar) -> pb.ScalarValue:
        scalar_value = _unwrap_scalar_value(value)
        if scalar_value is None or scalar_value is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(time32=pb.TIME_UNIT_MILLISECOND))
        return self.from_pyarrow_to_protobuf(pa.scalar(cast(time, scalar_value), type=pa.time32("ms")))

    def from_rich_to_protobuf(
        self,
        value: time | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pb.ScalarValue:
        prim = cast(time | None, self.from_rich_to_primitive(value, missing_value_strategy))
        if prim is None or prim is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(time32=pb.TIME_UNIT_MILLISECOND))
        return self.from_pyarrow_to_protobuf(pa.scalar(prim, type=pa.time32("ms")))

    def from_pyarrow_to_protobuf(self, value: pa.Scalar) -> pb.ScalarValue:
        time_val = value.as_py()
        if time_val is None:
            return pb.ScalarValue(null_value=pb.ArrowType(time32=pb.TIME_UNIT_MILLISECOND))
        if not isinstance(time_val, time):
            raise TypeError(f"Expected Python `time`, but got `{type(time_val).__name__}`")
        ms_since_midnight = (
            time_val.hour * 3_600_000
            + time_val.minute * 60_000
            + time_val.second * 1_000
            + time_val.microsecond // 1_000
        )
        return pb.ScalarValue(time32_value=pb.ScalarTime32Value(time32_millisecond_value=ms_since_midnight))

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar:
        if pb_value.HasField("null_value"):
            return pa.nulls(1, type=pa.time32("ms"))[0]
        milliseconds = pb_value.time32_value.time32_millisecond_value
        return pa.scalar(
            time(
                hour=milliseconds // 3_600_000,
                minute=(milliseconds % 3_600_000) // 60_000,
                second=(milliseconds % 60_000) // 1_000,
                microsecond=(milliseconds % 1_000) * 1_000,
            ),
            pa.time32("ms"),
        )


class Time64usFeatureConverter(_TimeFeatureConverterBase):
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.time64("us")
    _proto_arrow_type: ClassVar[pb.ArrowType] = pb.ArrowType(time64=pb.TIME_UNIT_MICROSECOND)
    _polars_dtype_value: ClassVar[Any] = None

    def from_primitive_to_protobuf(self, value: time | pa.Scalar) -> pb.ScalarValue:
        scalar_value = _unwrap_scalar_value(value)
        if scalar_value is None or scalar_value is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(time64=pb.TIME_UNIT_MICROSECOND))
        return self.from_pyarrow_to_protobuf(pa.scalar(cast(time, scalar_value), type=pa.time64("us")))

    def from_rich_to_protobuf(
        self,
        value: time | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pb.ScalarValue:
        prim = cast(time | None, self.from_rich_to_primitive(value, missing_value_strategy))
        if prim is None or prim is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(time64=pb.TIME_UNIT_MICROSECOND))
        return self.from_pyarrow_to_protobuf(pa.scalar(prim, type=pa.time64("us")))

    def from_pyarrow_to_protobuf(self, value: pa.Scalar) -> pb.ScalarValue:
        time_val = value.as_py()
        if time_val is None:
            return pb.ScalarValue(null_value=pb.ArrowType(time64=pb.TIME_UNIT_MICROSECOND))
        if not isinstance(time_val, time):
            raise TypeError(f"Expected Python `time`, but got `{type(time_val).__name__}`")
        ns_since_midnight = (
            time_val.hour * 3_600_000_000_000
            + time_val.minute * 60_000_000_000
            + time_val.second * 1_000_000_000
            + time_val.microsecond * 1_000
        )
        return pb.ScalarValue(time64_value=pb.ScalarTime64Value(time64_microsecond_value=ns_since_midnight // 1_000))

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar:
        if pb_value.HasField("null_value"):
            return pa.nulls(1, type=pa.time64("us"))[0]
        microseconds = pb_value.time64_value.time64_microsecond_value
        return pa.scalar(
            time(
                hour=microseconds // 3_600_000_000,
                minute=(microseconds % 3_600_000_000) // 60_000_000,
                second=(microseconds % 60_000_000) // 1_000_000,
                microsecond=microseconds % 1_000_000,
            ),
            pa.time64("us"),
        )


class Time64nsFeatureConverter(_TimeFeatureConverterBase):
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.time64("ns")
    _proto_arrow_type: ClassVar[pb.ArrowType] = pb.ArrowType(time64=pb.TIME_UNIT_NANOSECOND)
    _polars_dtype_value: ClassVar[Any] = None

    def from_primitive_to_protobuf(self, value: time | pa.Scalar) -> pb.ScalarValue:
        scalar_value = _unwrap_scalar_value(value)
        if scalar_value is None or scalar_value is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(time64=pb.TIME_UNIT_NANOSECOND))
        return self.from_pyarrow_to_protobuf(pa.scalar(cast(time, scalar_value), type=pa.time64("ns")))

    def from_rich_to_protobuf(
        self,
        value: time | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pb.ScalarValue:
        prim = cast(time | None, self.from_rich_to_primitive(value, missing_value_strategy))
        if prim is None or prim is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(time64=pb.TIME_UNIT_NANOSECOND))
        return self.from_pyarrow_to_protobuf(pa.scalar(prim, type=pa.time64("ns")))

    def from_pyarrow_to_protobuf(self, value: pa.Scalar) -> pb.ScalarValue:
        time_val = value.as_py()
        if time_val is None:
            return pb.ScalarValue(null_value=pb.ArrowType(time64=pb.TIME_UNIT_NANOSECOND))
        if not isinstance(time_val, time):
            raise TypeError(f"Expected Python `time`, but got `{type(time_val).__name__}`")
        ns_since_midnight = (
            time_val.hour * 3_600_000_000_000
            + time_val.minute * 60_000_000_000
            + time_val.second * 1_000_000_000
            + time_val.microsecond * 1_000
        )
        return pb.ScalarValue(time64_value=pb.ScalarTime64Value(time64_nanosecond_value=ns_since_midnight))

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar:
        if pb_value.HasField("null_value"):
            return pa.nulls(1, type=pa.time64("ns"))[0]
        nanoseconds = pb_value.time64_value.time64_nanosecond_value
        microseconds = nanoseconds // 1_000
        return pa.scalar(
            time(
                hour=microseconds // 3_600_000_000,
                minute=(microseconds % 3_600_000_000) // 60_000_000,
                second=(microseconds % 60_000_000) // 1_000_000,
                microsecond=microseconds % 1_000_000,
            ),
            pa.time64("ns"),
        )
