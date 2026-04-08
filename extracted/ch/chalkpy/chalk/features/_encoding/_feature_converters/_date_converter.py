from __future__ import annotations

from datetime import date, datetime, time
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
from chalk.features._encoding.pyarrow import pyarrow_to_polars

from ._primitive_converter import _FeatureConverterArrowProtoHelpers, PrimitiveFeatureConverter

# pyright: reportPrivateUsage=false, reportIncompatibleMethodOverride=false, reportReturnType=false, reportUnnecessaryCast=false, reportUnnecessaryComparison=false

try:
    import polars as pl
except ImportError:
    pl = None


def _coerce_date(x: Any) -> date:
    """Convert x to date, matching the structuring logic in rich.py/_structure_date.

    Used for rich-type inputs: rejects datetimes with non-zero time components.

    Note: this intentionally diverges from _coerce_date_from_json. The rich converter
    (rich.py/_structure_date) treats a datetime-to-date cast as lossy and raises if the
    time component is non-zero, whereas the JSON converter (json.py/_structure_date) simply
    truncates the time without checking. from_rich_to_* methods use this function;
    from_json_to_* methods use _coerce_date_from_json.
    """
    if type(x) is date:
        return x
    if isinstance(x, datetime):
        if x.time() != time():
            raise TypeError(f"Datetime '{x}' has a non-zero time component, which cannot be safely cast into a date")
        return x.date()
    if isinstance(x, str):
        return isodate.parse_date(x)
    raise TypeError(f"Cannot convert '{x}' to a date")


def _coerce_date_from_json(x: Any) -> date:
    """Convert x to date, matching the structuring logic in json.py/_structure_date.

    Used for JSON inputs: truncates datetimes without checking the time component.
    See the docstring on _coerce_date for the full explanation of the divergence.
    """
    if isinstance(x, datetime):
        return x.date()
    if isinstance(x, date):
        return x
    if isinstance(x, str):
        return isodate.parse_date(x)
    raise TypeError(
        f"Date values must be serialized as ISO strings. Instead, received value '{x}' of type `{type(x).__name__}`"
    )


_DATE32_PRIMITIVE_CONVERTER = PrimitiveFeatureConverter(name="", is_nullable=True, pyarrow_dtype=pa.date32())
_DATE64_PRIMITIVE_CONVERTER = PrimitiveFeatureConverter(name="", is_nullable=True, pyarrow_dtype=pa.date64())


class _DateFeatureConverterBase(
    _ScalarConverterBase[date, date],
    _FeatureConverterArrowProtoHelpers,
    FeatureConverter[date, date],
):
    _rich_type_value: ClassVar[Type[date]] = date
    _primitive_type_value: ClassVar[Type[date]] = date
    _primitive_converter: ClassVar[PrimitiveFeatureConverter]

    _coerce_fn = staticmethod(_coerce_date)
    _json_coerce_fn = staticmethod(_coerce_date_from_json)
    _use_fast_path = False

    def _serialize_to_json(self, x: Any) -> TJSON:
        return cast(date, x).isoformat()

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
        return cast(date, value).isoformat()

    def from_primitive_to_protobuf(self, value: date | pa.Scalar) -> pb.ScalarValue:
        pa_type = type(self)._pyarrow_dtype_value
        scalar_value = _unwrap_scalar_value(value)
        if scalar_value is None or scalar_value is ...:
            return pb.ScalarValue(null_value=self.convert_pa_dtype_to_proto_dtype(pa_type))
        return type(self)._primitive_converter.from_pyarrow_to_protobuf(
            pa.scalar(cast(date, scalar_value), type=pa_type)
        )

    def from_rich_to_protobuf(
        self,
        value: date | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pb.ScalarValue:
        pa_type = type(self)._pyarrow_dtype_value
        prim = cast(date | None, self.from_rich_to_primitive(value, missing_value_strategy))
        if prim is None or prim is ...:
            return pb.ScalarValue(null_value=self.convert_pa_dtype_to_proto_dtype(pa_type))
        return type(self)._primitive_converter.from_pyarrow_to_protobuf(
            pa.scalar(prim, type=pa_type)
        )

    def from_primitive_to_rich(self, value: date | None) -> date:
        if value is None:
            return cast(date, None)
        return cast(date, value)

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar:
        return type(self)._primitive_converter.from_protobuf_to_pyarrow(pb_value)

    def from_pyarrow_to_protobuf(self, value: pa.Scalar) -> pb.ScalarValue:
        return type(self)._primitive_converter.from_pyarrow_to_protobuf(value)


class Date32FeatureConverter(_DateFeatureConverterBase):
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.date32()
    _polars_dtype_value: ClassVar[Any] = pyarrow_to_polars(pa.date32(), "") if pl is not None else None
    _primitive_converter: ClassVar[PrimitiveFeatureConverter] = _DATE32_PRIMITIVE_CONVERTER


class Date64FeatureConverter(_DateFeatureConverterBase):
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.date64()
    _polars_dtype_value: ClassVar[Any] = pyarrow_to_polars(pa.date64(), "") if pl is not None else None
    _primitive_converter: ClassVar[PrimitiveFeatureConverter] = _DATE64_PRIMITIVE_CONVERTER
