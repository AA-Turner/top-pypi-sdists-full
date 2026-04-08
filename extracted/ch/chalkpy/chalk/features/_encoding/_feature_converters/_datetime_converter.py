from __future__ import annotations

from datetime import date, datetime, time
from typing import (
    Any,
    ClassVar,
    Sequence,
    Type,
    cast,
)

import dateutil.parser
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

_DATETIME_PA_TYPE = pa.timestamp("us", "UTC")

# Used to delegate proto conversion, which is complex (handles multiple timestamp units/timezones).
_DATETIME_PRIMITIVE_CONVERTER = PrimitiveFeatureConverter(
    name="", is_nullable=True, pyarrow_dtype=_DATETIME_PA_TYPE
)


def _coerce_datetime(x: Any) -> datetime:
    """Convert x to datetime, matching the structuring logic in rich.py/_structure_datetime."""
    if isinstance(x, datetime):
        return x
    if isinstance(x, str):
        return dateutil.parser.parse(x)
    if isinstance(x, date):
        return datetime.combine(x, time())
    raise TypeError(f"Cannot convert '{x}' to a datetime")


class DatetimeFeatureConverter(
    _ScalarConverterBase[datetime, datetime],
    _FeatureConverterArrowProtoHelpers,
    FeatureConverter[datetime, datetime],
):
    _rich_type_value: ClassVar[Type[datetime]] = datetime
    _primitive_type_value: ClassVar[Type[datetime]] = datetime
    _pyarrow_dtype_value: ClassVar[pa.DataType] = _DATETIME_PA_TYPE
    _polars_dtype_value: ClassVar[Any] = pl.Datetime("us", "UTC") if pl is not None else None

    _coerce_fn = staticmethod(_coerce_datetime)
    _use_fast_path = False

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

    def from_primitive_to_protobuf(self, value: datetime | pa.Scalar) -> pb.ScalarValue:
        scalar_value = _unwrap_scalar_value(value)
        if scalar_value is None or scalar_value is ...:
            return pb.ScalarValue(null_value=self.convert_pa_dtype_to_proto_dtype(_DATETIME_PA_TYPE))
        return _DATETIME_PRIMITIVE_CONVERTER.from_pyarrow_to_protobuf(
            pa.scalar(cast(datetime, scalar_value), type=_DATETIME_PA_TYPE)
        )

    def from_rich_to_protobuf(
        self,
        value: datetime | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pb.ScalarValue:
        prim = cast(datetime | None, self.from_rich_to_primitive(value, missing_value_strategy))
        if prim is None or prim is ...:
            return pb.ScalarValue(null_value=self.convert_pa_dtype_to_proto_dtype(_DATETIME_PA_TYPE))
        return _DATETIME_PRIMITIVE_CONVERTER.from_pyarrow_to_protobuf(
            pa.scalar(prim, type=_DATETIME_PA_TYPE)
        )

    def from_primitive_to_rich(self, value: datetime | None) -> datetime:
        if value is None:
            return cast(datetime, None)
        return cast(datetime, value)

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar:
        return _DATETIME_PRIMITIVE_CONVERTER.from_protobuf_to_pyarrow(pb_value)

    def from_pyarrow_to_protobuf(self, value: pa.Scalar) -> pb.ScalarValue:
        return _DATETIME_PRIMITIVE_CONVERTER.from_pyarrow_to_protobuf(value)
