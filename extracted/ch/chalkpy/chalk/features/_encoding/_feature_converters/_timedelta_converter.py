from __future__ import annotations

from datetime import timedelta
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

# pyright: reportPrivateUsage=false, reportIncompatibleMethodOverride=false, reportReturnType=false, reportUnnecessaryCast=false, reportUnnecessaryComparison=false

try:
    import polars as pl
except ImportError:
    pl = None

_TIMEDELTA_PA_TYPE = pa.duration("us")
_TIMEDELTA_NULL_PROTO = pb.ArrowType(duration=pb.TIME_UNIT_MICROSECOND)


def _coerce_timedelta(x: Any) -> timedelta:
    """Convert x to timedelta, matching the structuring logic in rich.py and json.py.

    Both the rich and JSON converters for timedelta behave identically: accept timedelta
    objects (passthrough) and ISO 8601 duration strings (via isodate.parse_duration),
    reject everything else. There is no divergence between the JSON and rich paths.

    Note: JSON encoding uses isodate.duration_isoformat, not timedelta.isoformat(), since
    isoformat() is not defined on timedelta and the wire format is ISO 8601 duration strings.
    """
    if isinstance(x, timedelta):
        return x
    if isinstance(x, str):
        result = isodate.parse_duration(x)
        if not isinstance(result, timedelta):
            raise TypeError(
                f"ISO 8601 duration '{x}' contains year/month components that cannot be represented as a fixed timedelta"
            )
        return result
    raise TypeError(f"Cannot convert '{x}' to a timedelta")


class TimedeltaFeatureConverter(
    _ScalarConverterBase[timedelta, timedelta],
    FeatureConverter[timedelta, timedelta],
):
    _rich_type_value: ClassVar[Type[timedelta]] = timedelta
    _primitive_type_value: ClassVar[Type[timedelta]] = timedelta
    _pyarrow_dtype_value: ClassVar[pa.DataType] = _TIMEDELTA_PA_TYPE
    _proto_arrow_type: ClassVar[pb.ArrowType] = _TIMEDELTA_NULL_PROTO
    _polars_dtype_value: ClassVar[Any] = pl.Duration("us") if pl is not None else None

    _coerce_fn = staticmethod(_coerce_timedelta)
    _use_fast_path = False

    def _serialize_to_json(self, x: Any) -> TJSON:
        return isodate.duration_isoformat(cast(timedelta, x))

    def from_pyarrow_to_json(
        self,
        values: pa.Array | pa.ChunkedArray,
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> Sequence[TJSON]:
        return [None if v is None else isodate.duration_isoformat(v) for v in values.to_pylist()]

    def from_primitive_to_json(
        self,
        value: TPrimitive,
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> TJSON:
        if value is ...:
            return cast(TJSON, ...)
        if value is None:
            return None
        return isodate.duration_isoformat(cast(timedelta, value))

    def from_primitive_to_rich(self, value: timedelta | None) -> timedelta:
        if value is None:
            return cast(timedelta, None)
        return cast(timedelta, value)

    def from_primitive_to_protobuf(self, value: timedelta | pa.Scalar) -> pb.ScalarValue:
        scalar_value = _unwrap_scalar_value(value)
        if scalar_value is None or scalar_value is ...:
            return pb.ScalarValue(null_value=_TIMEDELTA_NULL_PROTO)
        return self.from_pyarrow_to_protobuf(pa.scalar(cast(timedelta, scalar_value), type=_TIMEDELTA_PA_TYPE))

    def from_rich_to_protobuf(
        self,
        value: timedelta | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pb.ScalarValue:
        prim = cast(timedelta | None, self.from_rich_to_primitive(value, missing_value_strategy))
        if prim is None or prim is ...:
            return pb.ScalarValue(null_value=_TIMEDELTA_NULL_PROTO)
        return self.from_pyarrow_to_protobuf(pa.scalar(prim, type=_TIMEDELTA_PA_TYPE))

    def from_pyarrow_to_protobuf(self, value: pa.Scalar) -> pb.ScalarValue:
        duration_val = value.as_py()
        if duration_val is None:
            return pb.ScalarValue(null_value=_TIMEDELTA_NULL_PROTO)
        if not isinstance(duration_val, timedelta):
            raise TypeError(
                f"Expected a `timedelta` as the Python equivalent of a PyArrow Duration, but got: {type(duration_val).__name__}"
            )
        return pb.ScalarValue(duration_microsecond_value=int(duration_val.total_seconds() * 1_000_000))

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar:
        if pb_value.HasField("null_value"):
            return pa.nulls(1, type=_TIMEDELTA_PA_TYPE)[0]
        return pa.scalar(timedelta(microseconds=pb_value.duration_microsecond_value), _TIMEDELTA_PA_TYPE)
