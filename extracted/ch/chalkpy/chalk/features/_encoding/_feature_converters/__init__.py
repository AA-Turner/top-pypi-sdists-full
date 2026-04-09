from __future__ import annotations

# pyright: reportPrivateUsage=false

from ._base import (
    _DEFAULT_FEATURE_ENCODING_OPTIONS,
    _FROM_NEW,
    _TPrim,
    _TPrimCo,
    _TPrimCon,
    _TRich,
    _TRichCo,
    _TRichCon,
    _TScalar,
    _identity,
    _logger,
    _raise_unsupported_missing_value_strategy,
    _unwrap_scalar_value,
    _UNSUPPORTED_MISSING_VALUE_STRATEGY_MESSAGE,
    FeatureConverter,
    MissingValueError,
)
from ._bool_converter import BoolFeatureConverter
from ._bytes_converter import BytesFeatureConverter, LargeBinaryFeatureConverter
from ._date_converter import Date32FeatureConverter, Date64FeatureConverter
from ._datetime_converter import DatetimeFeatureConverter
from ._dataclass_converter import (
    DataclassFeatureConverter,
    _build_dc_to_dict,
    _build_dict_to_dc,
    _build_to_primitive_converter,
    _build_to_rich_converter,
)
from ._factory import make_feature_converter, make_primitive_converter
from ._float_converter import Float32FeatureConverter, Float64FeatureConverter
from ._generic_converter import (
    GenericFeatureConverter,
    JSONCodec,
    TDecoder,
    TEncoder,
    _decode_json,
    _encode_json,
    _to_old_style_type,
    canonicalize_typ,
)
from ._int_converter import Int32FeatureConverter, Int64FeatureConverter
from ._list_converter import ListFeatureConverter
from ._primitive_converter import (
    PrimitiveFeatureConverter,
    pa_scalar_to_proto,
    proto_to_pa_scalar,
)
from ._string_converter import LargeStringFeatureConverter, StringFeatureConverter
from ._time_converter import Time32sFeatureConverter, Time32msFeatureConverter, Time64usFeatureConverter, Time64nsFeatureConverter
from ._timedelta_converter import TimedeltaFeatureConverter

__all__ = [
    # _base
    "_DEFAULT_FEATURE_ENCODING_OPTIONS",
    "_FROM_NEW",
    "_TPrim",
    "_TPrimCo",
    "_TPrimCon",
    "_TRich",
    "_TRichCo",
    "_TRichCon",
    "_TScalar",
    "_identity",
    "_logger",
    "_raise_unsupported_missing_value_strategy",
    "_unwrap_scalar_value",
    "_UNSUPPORTED_MISSING_VALUE_STRATEGY_MESSAGE",
    "FeatureConverter",
    "MissingValueError",
    # bool_converter
    "BoolFeatureConverter",
    # bytes_converter
    "BytesFeatureConverter",
    "LargeBinaryFeatureConverter",
    # date_converter
    "Date32FeatureConverter",
    "Date64FeatureConverter",
    # datetime_converter
    "DatetimeFeatureConverter",
    # dataclass_converter
    "DataclassFeatureConverter",
    "_build_dc_to_dict",
    "_build_dict_to_dc",
    "_build_to_primitive_converter",
    "_build_to_rich_converter",
    # factory
    "make_feature_converter",
    "make_primitive_converter",
    # float_converters
    "Float32FeatureConverter",
    "Float64FeatureConverter",
    # generic_converter
    "GenericFeatureConverter",
    "JSONCodec",
    "TDecoder",
    "TEncoder",
    "_decode_json",
    "_encode_json",
    "_to_old_style_type",
    "canonicalize_typ",
    # int_converter
    "Int32FeatureConverter",
    "Int64FeatureConverter",
    # list_converter
    "ListFeatureConverter",
    # primitive_converter
    "PrimitiveFeatureConverter",
    "pa_scalar_to_proto",
    "proto_to_pa_scalar",

    # string_converter
    "LargeStringFeatureConverter",
    "StringFeatureConverter",
    # time_converter
    "Time32sFeatureConverter",
    "Time32msFeatureConverter",
    "Time64usFeatureConverter",
    "Time64nsFeatureConverter",
    # timedelta_converter
    "TimedeltaFeatureConverter",
]
