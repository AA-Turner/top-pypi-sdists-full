from __future__ import annotations

from datetime import date, datetime, time
from typing import (
    Any,
    ClassVar,
    Dict,
    Sequence,
    Tuple,
    Type,
    cast,
)

import pyarrow as pa
from chalk_rs import (
    parse_datetime as _parse_datetime,
    timezone_from_name as _timezone_from_name,
)

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

_DATETIME_PA_TYPE = pa.timestamp("us", "UTC")
_DATETIME_NULL_PROTO = pb.ArrowType(
    timestamp=pb.Timestamp(time_unit=pb.TIME_UNIT_MICROSECOND, timezone="UTC")
)
_NAIVE_DATETIME_PA_TYPE = pa.timestamp("us")
_NAIVE_DATETIME_NULL_PROTO = pb.ArrowType(
    timestamp=pb.Timestamp(time_unit=pb.TIME_UNIT_MICROSECOND)
)

_UNIT_TO_PB: dict[str, Any] = {
    "s": pb.TIME_UNIT_SECOND,
    "ms": pb.TIME_UNIT_MILLISECOND,
    "us": pb.TIME_UNIT_MICROSECOND,
    "ns": pb.TIME_UNIT_NANOSECOND,
}


def _pa_type_to_proto(pa_type: pa.TimestampType) -> pb.ArrowType:
    return pb.ArrowType(
        timestamp=pb.Timestamp(
            time_unit=_UNIT_TO_PB[pa_type.unit],
            timezone=pa_type.tz or "",
        )
    )


def _coerce_datetime(x: Any) -> datetime:
    """Convert x to datetime, matching the structuring logic in rich.py/_structure_datetime."""
    if isinstance(x, datetime):
        return x
    if isinstance(x, str):
        return _parse_datetime(x)
    if isinstance(x, date):
        return datetime.combine(x, time())
    raise TypeError(f"Cannot convert '{x}' to a datetime")


class DatetimeFeatureConverter(
    _ScalarConverterBase[datetime, datetime],
    FeatureConverter[datetime, datetime],
):
    _rich_type_value: ClassVar[Type[datetime]] = datetime
    _primitive_type_value: ClassVar[Type[datetime]] = datetime
    _pyarrow_dtype_value: ClassVar[pa.DataType] = _DATETIME_PA_TYPE
    _proto_arrow_type: ClassVar[pb.ArrowType] = _DATETIME_NULL_PROTO
    _polars_dtype_value: ClassVar[Any] = None

    _coerce_fn = staticmethod(_coerce_datetime)
    _use_fast_path = False

    # Cache keyed on (pa_type, default, is_nullable) to support non-standard timestamp types.
    _cache: ClassVar[Dict[Tuple[pa.DataType, Any, bool], "DatetimeFeatureConverter"]] = {}

    # Instance-level overrides set in new() to support non-standard timestamp types.
    _instance_pa_type: pa.DataType
    _instance_proto_arrow_type: pb.ArrowType
    _instance_polars_dtype: Any

    @classmethod
    def new(cls, default: Any = ..., is_nullable: bool = False, *, pa_type: "pa.DataType | None" = None) -> "DatetimeFeatureConverter":  # type: ignore[override]
        if pa_type is None:
            pa_type = cls._pyarrow_dtype_value
        key = (pa_type, default, is_nullable)
        cached = cls._cache.get(key)
        if cached is not None:
            return cached
        from ._base import _FROM_NEW
        inst = cls.__new__(cls)
        super(DatetimeFeatureConverter, inst).__init__(default, is_nullable, pa_type=pa_type, _from_new=_FROM_NEW)
        ts_pa_type = cast(pa.TimestampType, pa_type)
        inst._instance_pa_type = pa_type
        inst._instance_proto_arrow_type = _pa_type_to_proto(ts_pa_type)
        from chalk.features._encoding.pyarrow import pyarrow_to_polars
        try:
            inst._instance_polars_dtype = pyarrow_to_polars(pa_type)
        except (AssertionError, Exception):
            inst._instance_polars_dtype = None
        cls._cache[key] = inst
        return inst

    @property
    def pyarrow_dtype(self) -> pa.DataType:
        return self._instance_pa_type

    @property
    def protobuf_dtype(self) -> pb.ArrowType:
        return self._instance_proto_arrow_type

    @property
    def polars_dtype(self) -> Any:
        return self._instance_polars_dtype

    def _serialize_to_json(self, x: Any) -> TJSON:
        return cast(datetime, x).isoformat()

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
        return cast(datetime, value).isoformat()

    def from_primitive_to_rich(self, value: datetime | None) -> datetime:
        if value is None:
            return cast(datetime, None)
        return cast(datetime, value)

    def from_primitive_to_protobuf(self, value: datetime | pa.Scalar) -> pb.ScalarValue:
        scalar_value = _unwrap_scalar_value(value)
        if scalar_value is None or scalar_value is ...:
            return pb.ScalarValue(null_value=self.protobuf_dtype)
        return self.from_pyarrow_to_protobuf(pa.scalar(cast(datetime, scalar_value), type=self.pyarrow_dtype))

    def from_rich_to_protobuf(
        self,
        value: datetime | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pb.ScalarValue:
        prim = cast(datetime | None, self.from_rich_to_primitive(value, missing_value_strategy))
        if prim is None or prim is ...:
            return pb.ScalarValue(null_value=self.protobuf_dtype)
        return self.from_pyarrow_to_protobuf(pa.scalar(prim, type=self.pyarrow_dtype))

    def from_pyarrow_to_protobuf(self, value: pa.Scalar) -> pb.ScalarValue:
        dt_val = value.as_py()
        if dt_val is None:
            return pb.ScalarValue(null_value=self.protobuf_dtype)
        if not isinstance(dt_val, datetime):
            raise TypeError(f"Expected Python `datetime`, but got `{type(dt_val).__name__}`")
        float_s = dt_val.timestamp()
        # Use the IANA timezone name from the Arrow type rather than tzname(dt_val),
        # which returns DST abbreviations like "EDT" or "BST" that cannot be round-tripped.
        timezone = value.type.tz if isinstance(value.type, pa.TimestampType) else None
        unit = value.type.unit if isinstance(value.type, pa.TimestampType) else "us"
        if unit == "ms":
            return pb.ScalarValue(
                timestamp_value=pb.ScalarTimestampValue(time_millisecond_value=int(float_s * 1_000), timezone=timezone)
            )
        if unit == "ns":
            return pb.ScalarValue(
                timestamp_value=pb.ScalarTimestampValue(time_nanosecond_value=int(float_s * 1_000_000_000), timezone=timezone)
            )
        if unit == "s":
            return pb.ScalarValue(
                timestamp_value=pb.ScalarTimestampValue(time_second_value=int(float_s), timezone=timezone)
            )
        # Default: "us"
        return pb.ScalarValue(
            timestamp_value=pb.ScalarTimestampValue(time_microsecond_value=int(float_s * 1_000_000), timezone=timezone)
        )

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar:
        if pb_value.HasField("null_value"):
            return pa.nulls(1, type=self.pyarrow_dtype)[0]
        if pb_value.HasField("timestamp_value"):
            tz_str = pb_value.timestamp_value.timezone
            tz = _timezone_from_name(tz_str) if tz_str else None
            if pb_value.timestamp_value.HasField("time_second_value"):
                seconds = pb_value.timestamp_value.time_second_value
                return pa.scalar(datetime.fromtimestamp(seconds, tz=tz), pa.timestamp("s", tz=tz_str))
            if pb_value.timestamp_value.HasField("time_millisecond_value"):
                milliseconds = pb_value.timestamp_value.time_millisecond_value
                return pa.scalar(datetime.fromtimestamp(milliseconds / 1_000, tz=tz), pa.timestamp("ms", tz=tz_str))
            if pb_value.timestamp_value.HasField("time_microsecond_value"):
                microseconds = pb_value.timestamp_value.time_microsecond_value
                return pa.scalar(datetime.fromtimestamp(microseconds / 1_000_000, tz=tz), pa.timestamp("us", tz=tz_str))
            if pb_value.timestamp_value.HasField("time_nanosecond_value"):
                nanoseconds = pb_value.timestamp_value.time_nanosecond_value
                return pa.scalar(datetime.fromtimestamp(nanoseconds / 1_000_000_000, tz=tz), pa.timestamp("ns", tz=tz_str))
            raise ValueError(
                "Unsupported protobuf timestamp value - missing fields `time_second_value`, "
                + "`time_millisecond_value`, `time_microsecond_value`, and `time_nanosecond_value`"
            )
        raise ValueError(f"Unsupported Protobuf type for datetime: {pb_value}")

