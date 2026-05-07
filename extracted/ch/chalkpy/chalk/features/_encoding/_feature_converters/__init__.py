from __future__ import annotations

# pyright: reportPrivateUsage=false

from chalk.utils.attrs_utils import get_attrs

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
from ._decimal_converter import DecimalFeatureConverter
from ._datetime_converter import DatetimeFeatureConverter
from ._enum_converter import EnumFeatureConverter
from ._dataclass_converter import (
    DataclassFeatureConverter,
    _build_dc_to_dict,
    _build_dict_to_dc,
    _build_to_primitive_converter,
    _build_to_rich_converter,
)
from ._factory import make_feature_converter, make_primitive_converter
from ._fixed_size_list_converter import FixedSizeListFeatureConverter
from ._float_converter import Float16FeatureConverter, Float32FeatureConverter, Float64FeatureConverter
from ._generic_converter import (
    JSONCodec,
    TDecoder,
    TEncoder,
    _decode_json,
    _encode_json,
    _to_old_style_type,
    canonicalize_typ,
)
from ._int_converter import (
    Int8FeatureConverter,
    Int16FeatureConverter,
    Int32FeatureConverter,
    Int64FeatureConverter,
    UInt8FeatureConverter,
    UInt16FeatureConverter,
    UInt32FeatureConverter,
    UInt64FeatureConverter,
)
from ._dict_converter import DictFeatureConverter
from ._list_converter import ListFeatureConverter
from ._set_converter import SetFeatureConverter
from ._named_tuple_converter import NamedTupleFeatureConverter
from ._primitive_converter import (
    PrimitiveFeatureConverter,
    pa_scalar_to_proto,
    proto_to_pa_scalar,
)
from ._string_converter import LargeStringFeatureConverter, StringFeatureConverter
from ._time_converter import Time32sFeatureConverter, Time32msFeatureConverter, Time64usFeatureConverter, Time64nsFeatureConverter
from ._timedelta_converter import TimedeltaFeatureConverter
from ._typed_dict_converter import TypedDictFeatureConverter
from ._uuid_ip_converters import UUIDFeatureConverter, IPv4FeatureConverter, IPv6FeatureConverter

_HAS_ATTRS = get_attrs() is not None

if _HAS_ATTRS:
    from ._attrs_converter import AttrsFeatureConverter

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
    # decimal_converter
    "DecimalFeatureConverter",
    # date_converter
    "Date32FeatureConverter",
    "Date64FeatureConverter",
    # datetime_converter
    "DatetimeFeatureConverter",
    # enum_converter
    "EnumFeatureConverter",
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
    "Float16FeatureConverter",
    "Float32FeatureConverter",
    "Float64FeatureConverter",
    # generic_converter
    "JSONCodec",
    "TDecoder",
    "TEncoder",
    "_decode_json",
    "_encode_json",
    "_to_old_style_type",
    "canonicalize_typ",
    # int_converter
    "Int8FeatureConverter",
    "Int16FeatureConverter",
    "Int32FeatureConverter",
    "Int64FeatureConverter",
    "UInt8FeatureConverter",
    "UInt16FeatureConverter",
    "UInt32FeatureConverter",
    "UInt64FeatureConverter",
    # fixed_size_list_converter
    "FixedSizeListFeatureConverter",
    # list_converter
    "ListFeatureConverter",
    # set_converter
    "SetFeatureConverter",
    # dict_converter
    "DictFeatureConverter",
    # namedtuple_converter
    "NamedTupleFeatureConverter",
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
    # typed_dict_converter
    "TypedDictFeatureConverter",
    # uuid_ip_converters
    "UUIDFeatureConverter",
    "IPv4FeatureConverter",
    "IPv6FeatureConverter",
]

if _HAS_ATTRS:
    __all__.append("AttrsFeatureConverter")
