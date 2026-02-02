import base64
import decimal
from abc import abstractmethod
from collections.abc import Callable
from datetime import date
from typing import Final, Literal, TypeAlias, cast, overload

import pyarrow as pa
from google.protobuf import struct_pb2

from corvic.pa_scalar._const import (
    signed_limits,
    unit_to_frac_digits,
    unit_to_seconds,
    unsigned_limits,
)
from corvic.pa_scalar._temporal import (
    datetime_fromisoformat,
    month_day_nano_fromisoformat,
    month_day_nano_fromlaxformat,
    time_fromisoformat,
    validate_second_frac_resolution,
)
from corvic.pa_scalar._types import Scalar
from corvic.result import InvalidArgumentError, Ok

_TypeObserver: TypeAlias = Callable[[pa.DataType], bool]
_INT_LIMITS: Final[dict[Literal[8, 16, 32, 64], tuple[int, int]]] = {
    nbits: signed_limits(nbits) for nbits in (8, 16, 32, 64)
}
_UINT_LIMITS: Final[dict[Literal[8, 16, 32, 64], tuple[int, int]]] = {
    nbits: unsigned_limits(nbits) for nbits in (8, 16, 32, 64)
}


class _ErrorHandler:
    @abstractmethod
    def handle(self, msg: str) -> object:
        pass

    @abstractmethod
    def check(self, msg: str) -> bool:
        pass


_DispatchFn: TypeAlias = Callable[
    [struct_pb2.Value, pa.DataType, _ErrorHandler], object
]


def _extract_error_message(exc: Exception) -> str:
    if len(exc.args) > 0:
        return exc.args[0]
    return str(exc)


class _Error(Exception):
    message: str

    def __init__(self, msg: str):
        self.message = msg
        super().__init__(msg)


class _StrictErrorHandler(_ErrorHandler):
    def handle(self, msg: str) -> object:
        raise _Error(msg)

    def check(self, msg: str) -> bool:
        raise _Error(msg)


class _UseNoneErrorHandler(_ErrorHandler):
    def handle(self, msg: str) -> object:
        return None

    def check(self, msg: str) -> bool:
        return True


def _visit_null(  # noqa: C901
    value: struct_pb2.Value, dtype: pa.DataType, error_handler: _ErrorHandler
) -> object:
    match value.WhichOneof("kind"):
        case "null_value":
            return None
        case "bool_value":
            if not value.bool_value:
                return None
            return error_handler.handle("expected coerce non-false boolean to null")
        case "list_value":
            return error_handler.handle("expected null found list")
        case "number_value":
            if value.number_value == 0:
                return None
            return error_handler.handle("cannot coerce non-zero number to null")
        case "string_value":
            if value.string_value == "":
                return None
            return error_handler.handle("cannot coerce non-empty string to null")
        case "struct_value":
            return error_handler.handle("expected null found struct")
        case None:
            return error_handler.handle("cannot determine value kind")


def _visit_boolean(
    value: struct_pb2.Value, dtype: pa.DataType, error_handler: _ErrorHandler
) -> object:
    match value.WhichOneof("kind"):
        case "null_value":
            return None
        case "bool_value":
            return value.bool_value
        case "list_value":
            return error_handler.handle("expected boolean found list")
        case "number_value":
            return value.number_value != 0
        case "string_value":
            if value.string_value.lower() == "true" or value.string_value == "1":
                return True
            if value.string_value.lower() == "false" or value.string_value == "0":
                return False
            return error_handler.handle("cannot coerce non-empty string to null")
        case "struct_value":
            return error_handler.handle("expected boolean found struct")
        case None:
            return error_handler.handle("cannot determine value kind")


def _check_range(
    value: float, error_handler: _ErrorHandler, min_value: int, max_value: int
) -> object:
    if min_value <= value <= max_value:
        return value
    return error_handler.handle("value out of range")


def _visit_int(
    value: struct_pb2.Value,
    error_handler: _ErrorHandler,
    min_value: int,
    max_value: int,
) -> object:
    match value.WhichOneof("kind"):
        case "null_value":
            return None
        case "bool_value":
            return error_handler.handle("cannot coerce boolean to int")
        case "list_value":
            return error_handler.handle("expected number found list")
        case "number_value":
            int_value = int(value.number_value)
            if int_value != value.number_value:
                return error_handler.handle("expected integer number found non-integer")
            return _check_range(int_value, error_handler, min_value, max_value)
        case "string_value":
            try:
                number_value = int(value.string_value)
            except ValueError:
                return error_handler.handle("cannot coerce non-digit string to int")
            return _check_range(number_value, error_handler, min_value, max_value)
        case "struct_value":
            return error_handler.handle("expected number found struct")
        case None:
            return error_handler.handle("cannot determine value kind")


def _visit_int8(
    value: struct_pb2.Value, dtype: pa.DataType, error_handler: _ErrorHandler
) -> object:
    return _visit_int(value, error_handler, *_INT_LIMITS[8])


def _visit_int16(
    value: struct_pb2.Value, dtype: pa.DataType, error_handler: _ErrorHandler
) -> object:
    return _visit_int(value, error_handler, *_INT_LIMITS[16])


def _visit_int32(
    value: struct_pb2.Value, dtype: pa.DataType, error_handler: _ErrorHandler
) -> object:
    return _visit_int(value, error_handler, *_INT_LIMITS[32])


def _visit_int64(
    value: struct_pb2.Value, dtype: pa.DataType, error_handler: _ErrorHandler
) -> object:
    return _visit_int(value, error_handler, *_INT_LIMITS[64])


def _visit_uint8(
    value: struct_pb2.Value, dtype: pa.DataType, error_handler: _ErrorHandler
) -> object:
    return _visit_int(value, error_handler, *_UINT_LIMITS[8])


def _visit_uint16(
    value: struct_pb2.Value, dtype: pa.DataType, error_handler: _ErrorHandler
) -> object:
    return _visit_int(value, error_handler, *_UINT_LIMITS[16])


def _visit_uint32(
    value: struct_pb2.Value, dtype: pa.DataType, error_handler: _ErrorHandler
) -> object:
    return _visit_int(value, error_handler, *_UINT_LIMITS[32])


def _visit_uint64(
    value: struct_pb2.Value, dtype: pa.DataType, error_handler: _ErrorHandler
) -> object:
    return _visit_int(value, error_handler, *_UINT_LIMITS[64])


def _visit_float(
    value: struct_pb2.Value,
    dtype: pa.DataType,
    error_handler: _ErrorHandler,
    make_float: Callable[[float], object],
) -> object:
    match value.WhichOneof("kind"):
        case "null_value":
            return None
        case "bool_value":
            return error_handler.handle("cannot coerce boolean to float")
        case "list_value":
            return error_handler.handle("expected number found list")
        case "number_value":
            return make_float(value.number_value)
        case "string_value":
            try:
                number_value = float(value.string_value)
            except ValueError:
                return error_handler.handle("cannot coerce non-number string to float")
            return make_float(number_value)
        case "struct_value":
            return error_handler.handle("expected number found struct")
        case None:
            return error_handler.handle("cannot determine value kind")


def _visit_float16(
    value: struct_pb2.Value, dtype: pa.DataType, error_handler: _ErrorHandler
) -> object:
    import numpy as np

    return _visit_float(value, dtype, error_handler, np.float16)


def _visit_float32(
    value: struct_pb2.Value, dtype: pa.DataType, error_handler: _ErrorHandler
) -> object:
    return _visit_float(value, dtype, error_handler, lambda x: x)


def _visit_float64(
    value: struct_pb2.Value, dtype: pa.DataType, error_handler: _ErrorHandler
) -> object:
    return _visit_float(value, dtype, error_handler, lambda x: x)


def _visit_any_binary(value: struct_pb2.Value, error_handler: _ErrorHandler) -> object:
    match value.WhichOneof("kind"):
        case "null_value":
            return None
        case "bool_value":
            return error_handler.handle("expected string found boolean")
        case "list_value":
            return error_handler.handle("expected string found list")
        case "number_value":
            return error_handler.handle("expected string found number")
        case "string_value":
            remainder = len(value.string_value) % 4
            missing_padding = ""
            if remainder:
                missing_padding = "=" * (4 - remainder)

            return base64.b64decode(value.string_value + missing_padding)
        case "struct_value":
            return error_handler.handle("expected string found struct")
        case None:
            return error_handler.handle("cannot determine value kind")


def _visit_binary(
    value: struct_pb2.Value, dtype: pa.DataType, error_handler: _ErrorHandler
) -> object:
    return _visit_any_binary(value, error_handler)


def _visit_fixed_size_binary(
    value: struct_pb2.Value, dtype: pa.DataType, error_handler: _ErrorHandler
) -> object:
    return _visit_any_binary(value, error_handler)


def _visit_large_binary(
    value: struct_pb2.Value, dtype: pa.DataType, error_handler: _ErrorHandler
) -> object:
    return _visit_any_binary(value, error_handler)


def _visit_any_string(value: struct_pb2.Value, error_handler: _ErrorHandler) -> object:
    match value.WhichOneof("kind"):
        case "null_value":
            return None
        case "bool_value":
            return error_handler.handle("expected string found boolean")
        case "list_value":
            return error_handler.handle("expected string found list")
        case "number_value":
            return str(int(value.number_value))
        case "string_value":
            return value.string_value
        case "struct_value":
            return error_handler.handle("expected string found struct")
        case None:
            return error_handler.handle("cannot determine value kind")


def _visit_string(
    value: struct_pb2.Value, dtype: pa.DataType, error_handler: _ErrorHandler
) -> object:
    return _visit_any_string(value, error_handler)


def _visit_large_string(
    value: struct_pb2.Value, dtype: pa.DataType, error_handler: _ErrorHandler
) -> object:
    return _visit_any_string(value, error_handler)


def _check_frac_digits(
    temporal: object,
    error_handler: _ErrorHandler,
    iso_string: str,
    max_frac_digits: int,
) -> object:
    # If iso_string is a valid ISO 8601 string then the fractional seconds
    # portion is uniquely identified as the digits after "." and before the
    # end of the string or offset information if a timestamp.
    point_start = iso_string.find(".")
    if point_start < 0:
        return temporal

    frac_end = max(
        iso_string.find("Z", point_start),
        iso_string.find("+", point_start),
        iso_string.find("-", point_start),
    )
    if frac_end < 0:
        frac_end = len(iso_string)

    if validate_second_frac_resolution(
        iso_string[point_start + 1 : frac_end], max_frac_digits
    ):
        return temporal

    return error_handler.handle("seconds resolution exceeds target type")


def _make_from_iso8601(
    value: struct_pb2.Value,
    error_handler: _ErrorHandler,
    make_temporal: Callable[[str], object],
    max_frac_digits: int,
) -> object:
    match value.WhichOneof("kind"):
        case "null_value":
            return None
        case "bool_value":
            return error_handler.handle("expected string found boolean")
        case "list_value":
            return error_handler.handle("expected string found list")
        case "number_value":
            return error_handler.handle("expected string found number")
        case "string_value":
            try:
                temporal = make_temporal(value.string_value)
            except ValueError as exc:
                return error_handler.handle(_extract_error_message(exc))

            # Python only supports us (microseconds) natively. If the input
            # value indicates a finer granularity, treat it as an information
            # losing conversion.
            max_frac_digits = min(max_frac_digits, 6)

            return _check_frac_digits(
                temporal, error_handler, value.string_value, max_frac_digits
            )
        case "struct_value":
            return error_handler.handle("expected string found struct")
        case None:
            return error_handler.handle("cannot determine value kind")


def _visit_time32(
    value: struct_pb2.Value, dtype: pa.DataType, error_handler: _ErrorHandler
) -> object:
    dtype = cast(pa.Time32Type, dtype)
    return _make_from_iso8601(
        value, error_handler, time_fromisoformat, unit_to_frac_digits(dtype.unit)
    )


def _visit_time64(
    value: struct_pb2.Value, dtype: pa.DataType, error_handler: _ErrorHandler
) -> object:
    dtype = cast(pa.Time64Type, dtype)
    return _make_from_iso8601(
        value, error_handler, time_fromisoformat, unit_to_frac_digits(dtype.unit)
    )


def _visit_date32(
    value: struct_pb2.Value, dtype: pa.DataType, error_handler: _ErrorHandler
) -> object:
    return _make_from_iso8601(value, error_handler, date.fromisoformat, 0)


def _visit_date64(
    value: struct_pb2.Value, dtype: pa.DataType, error_handler: _ErrorHandler
) -> object:
    return _make_from_iso8601(value, error_handler, date.fromisoformat, 0)


def _check_datetime_timezone(s: str, dtype: pa.TimestampType) -> object:
    dt = datetime_fromisoformat(s)
    dt_has_tz = dt.tzinfo is not None
    type_has_tz = dtype.tz is not None
    if dt_has_tz and not type_has_tz:
        raise ValueError("unexpected timezone")
    if not dt_has_tz and type_has_tz:
        raise ValueError("expected timezone but none found")

    return dt


def _visit_timestamp(
    value: struct_pb2.Value, dtype: pa.DataType, error_handler: _ErrorHandler
) -> object:
    dtype = cast(pa.TimestampType, dtype)
    return _make_from_iso8601(
        value,
        error_handler,
        lambda x: _check_datetime_timezone(x, dtype),
        unit_to_frac_digits(dtype.unit),
    )


def _visit_duration(  # noqa: C901
    value: struct_pb2.Value, dtype: pa.DataType, error_handler: _ErrorHandler
) -> object:
    dtype = cast(pa.DurationType, dtype)
    match value.WhichOneof("kind"):
        case "null_value":
            return None
        case "bool_value":
            return error_handler.handle("expected string found boolean")
        case "list_value":
            return error_handler.handle("expected string found list")
        case "number_value":
            return value.number_value * unit_to_seconds(dtype.unit)
        case "string_value":
            try:
                mdnf = month_day_nano_fromlaxformat(value.string_value)
            except ValueError as exc:
                return error_handler.handle(_extract_error_message(exc))
            if mdnf.month or mdnf.day:
                return error_handler.handle("duration cannot include month or day")
            if not validate_second_frac_resolution(
                mdnf.second_frac or "", unit_to_frac_digits(dtype.unit)
            ):
                return error_handler.handle("seconds resolution exceeds target type")

            rescale = unit_to_seconds("ns") / unit_to_seconds(dtype.unit)
            return mdnf.nano / rescale
        case "struct_value":
            return error_handler.handle("expected string found struct")
        case None:
            return error_handler.handle("cannot determine value kind")


def _visit_interval(
    value: struct_pb2.Value, dtype: pa.DataType, error_handler: _ErrorHandler
) -> object:
    match value.WhichOneof("kind"):
        case "null_value":
            return None
        case "bool_value":
            return error_handler.handle("expected string found boolean")
        case "list_value":
            return error_handler.handle("expected string found list")
        case "number_value":
            return (0, 0, value.number_value * unit_to_seconds("ns"))
        case "string_value":
            try:
                mdnf = month_day_nano_fromisoformat(value.string_value)
            except ValueError as exc:
                return error_handler.handle(_extract_error_message(exc))
            return (mdnf.month, mdnf.day, mdnf.nano)
        case "struct_value":
            return error_handler.handle("expected string found struct")
        case None:
            return error_handler.handle("cannot determine value kind")


def _visit_decimal(value: struct_pb2.Value, error_handler: _ErrorHandler) -> object:
    match value.WhichOneof("kind"):
        case "null_value":
            return None
        case "bool_value":
            return error_handler.handle("expected number found boolean")
        case "list_value":
            return error_handler.handle("expected number found list")
        case "number_value":
            return decimal.Decimal(value.number_value)
        case "string_value":
            return decimal.Decimal(value.string_value)
        case "struct_value":
            return error_handler.handle("expected number found struct")
        case None:
            return error_handler.handle("cannot determine value kind")


def _visit_decimal128(
    value: struct_pb2.Value, dtype: pa.DataType, error_handler: _ErrorHandler
) -> object:
    return _visit_decimal(value, error_handler)


def _visit_decimal256(
    value: struct_pb2.Value, dtype: pa.DataType, error_handler: _ErrorHandler
) -> object:
    return _visit_decimal(value, error_handler)


def _visit_any_list(
    value: struct_pb2.Value, value_dtype: pa.DataType, error_handler: _ErrorHandler
) -> object:
    match value.WhichOneof("kind"):
        case "null_value":
            return None
        case "bool_value":
            return error_handler.handle("expected list found boolean")
        case "list_value":
            return [
                _visit(x, value_dtype, error_handler)
                for x in value.list_value.values  # noqa: PD011
            ]
        case "number_value":
            return error_handler.handle("expected list found number")
        case "string_value":
            return error_handler.handle("expected list found string")
        case "struct_value":
            return error_handler.handle("expected list found struct")
        case None:
            return error_handler.handle("cannot determine value kind")


def _visit_list(
    value: struct_pb2.Value, dtype: pa.DataType, error_handler: _ErrorHandler
) -> object:
    dtype = cast(pa.ListType, dtype)
    return _visit_any_list(value, dtype.value_type, error_handler)


def _visit_fixed_size_list(
    value: struct_pb2.Value, dtype: pa.DataType, error_handler: _ErrorHandler
) -> object:
    dtype = cast(pa.FixedSizeListType, dtype)
    return _visit_any_list(value, dtype.value_type, error_handler)


def _visit_large_list(
    value: struct_pb2.Value, dtype: pa.DataType, error_handler: _ErrorHandler
) -> object:
    dtype = cast(pa.LargeListType, dtype)
    return _visit_any_list(value, dtype.value_type, error_handler)


def _visit_dictionary(
    value: struct_pb2.Value, dtype: pa.DataType, error_handler: _ErrorHandler
) -> object:
    dtype = cast(pa.DictionaryType, dtype)
    return _visit(value, dtype.value_type, error_handler)


def _visit_map(  # noqa: C901
    value: struct_pb2.Value, dtype: pa.DataType, error_handler: _ErrorHandler
) -> object:
    dtype = cast(pa.MapType, dtype)
    match value.WhichOneof("kind"):
        case "null_value":
            return None
        case "bool_value":
            return error_handler.handle("expected object found boolean")
        case "list_value":
            ret: list[tuple[object, object]] = []
            for elem in value.list_value.values:  # noqa: PD011
                if not elem.HasField("list_value") and error_handler.check(
                    "expected tuple"
                ):
                    continue
                if (
                    len(elem.list_value.values) != 2  # noqa: PLR2004
                    and error_handler.check("expected tuple")
                ):
                    continue
                k = _visit(elem.list_value.values[0], dtype.key_type, error_handler)  # noqa: PD011
                v = _visit(elem.list_value.values[1], dtype.item_type, error_handler)  # noqa: PD011
                ret.append((k, v))
            return ret
        case "number_value":
            return error_handler.handle("expected object found number")
        case "string_value":
            return error_handler.handle("expected object found string")
        case "struct_value":
            ret: list[tuple[object, object]] = []
            for key, struct_value in value.struct_value.fields.items():
                k = _visit(
                    struct_pb2.Value(string_value=key), dtype.key_type, error_handler
                )
                if k is None and error_handler.check("expected string key found null"):
                    continue
                v = _visit(struct_value, dtype.item_type, error_handler)
                ret.append((k, v))
            return ret
        case None:
            return error_handler.handle("cannot determine value kind")


def _visit_struct(
    value: struct_pb2.Value, dtype: pa.DataType, error_handler: _ErrorHandler
) -> object:
    dtype = cast(pa.StructType, dtype)

    fields_by_name = {field.name: field for field in dtype}

    match value.WhichOneof("kind"):
        case "null_value":
            return None
        case "bool_value":
            return error_handler.handle("expected object found boolean")
        case "list_value":
            return error_handler.handle("expected object found list")
        case "number_value":
            return error_handler.handle("expected object found number")
        case "string_value":
            return error_handler.handle("expected object found string")
        case "struct_value":
            ret: dict[str, object] = {}
            for key, struct_value in value.struct_value.fields.items():
                k = key
                if key not in fields_by_name and error_handler.check(
                    f"unknown object key: {key}"
                ):
                    continue
                ret[k] = _visit(struct_value, fields_by_name[key].type, error_handler)
            return ret
        case None:
            return error_handler.handle("cannot determine value kind")


_DISPATCH_FUNCTIONS: Final[list[tuple[_TypeObserver, _DispatchFn]]] = [
    # Null
    (pa.types.is_null, _visit_null),
    # Integral
    (pa.types.is_boolean, _visit_boolean),
    (pa.types.is_int8, _visit_int8),
    (pa.types.is_int16, _visit_int16),
    (pa.types.is_int32, _visit_int32),
    (pa.types.is_int64, _visit_int64),
    (pa.types.is_uint8, _visit_uint8),
    (pa.types.is_uint16, _visit_uint16),
    (pa.types.is_uint32, _visit_uint32),
    (pa.types.is_uint64, _visit_uint64),
    (pa.types.is_decimal128, _visit_decimal128),
    (pa.types.is_decimal256, _visit_decimal256),
    # Floating point
    (pa.types.is_float16, _visit_float16),
    (pa.types.is_float32, _visit_float32),
    (pa.types.is_float64, _visit_float64),
    # Binary
    (pa.types.is_binary, _visit_binary),
    (pa.types.is_fixed_size_binary, _visit_fixed_size_binary),
    (pa.types.is_large_binary, _visit_large_binary),
    # String
    (pa.types.is_string, _visit_string),
    (pa.types.is_large_string, _visit_large_string),
    # Temporal
    (pa.types.is_time32, _visit_time32),
    (pa.types.is_time64, _visit_time64),
    (pa.types.is_date32, _visit_date32),
    (pa.types.is_date64, _visit_date64),
    (pa.types.is_timestamp, _visit_timestamp),
    (pa.types.is_duration, _visit_duration),
    (pa.types.is_interval, _visit_interval),
    # Containers
    (pa.types.is_dictionary, _visit_dictionary),
    (pa.types.is_list, _visit_list),
    (pa.types.is_large_list, _visit_large_list),
    (pa.types.is_fixed_size_list, _visit_fixed_size_list),
    (pa.types.is_map, _visit_map),
    (pa.types.is_struct, _visit_struct),
]


def _visit(
    value: struct_pb2.Value,
    dtype: pa.DataType,
    error_handler: _ErrorHandler,
) -> object:
    for is_type, dispatch in _DISPATCH_FUNCTIONS:
        if is_type(dtype):
            return dispatch(value, dtype, error_handler)

    return error_handler.handle(f"unknown dtype: {dtype}")


@overload
def from_value(
    value: struct_pb2.Value,
    dtype: pa.DataType,
    *,
    errors: Literal["strict"],
) -> Ok[Scalar] | InvalidArgumentError: ...


@overload
def from_value(
    value: struct_pb2.Value,
    dtype: pa.DataType,
) -> Ok[Scalar] | InvalidArgumentError: ...


@overload
def from_value(
    value: struct_pb2.Value,
    dtype: pa.DataType,
    *,
    errors: Literal["use_none"],
) -> Ok[Scalar]: ...


def from_value(
    value: struct_pb2.Value,
    dtype: pa.DataType,
    *,
    errors: Literal["strict", "use_none"] = "strict",
) -> Ok[Scalar] | InvalidArgumentError:
    """Convert value to Scalar.

    Conversions will coerce values to the expected type if possible. For example,
    a JSON "1" with expected data type pa.int32 will return the Python value 1.

    The behavior when this conversion would lose information
    (e.g., convert("a", pa.int32) => ...) is governed by the errors argument in the
    conversion functions. As a special case, conversions between different floating
    point representations (e.g., float64 to float16) are not considered information
    losing conversions.

    - strict: Return an error if the conversion would lose information
    - use_none: If the conversion would lose information, use null/None instead
    """
    match errors:
        case "strict":
            error_handler = _StrictErrorHandler()
        case "use_none":
            error_handler = _UseNoneErrorHandler()

    try:
        obj = _visit(value, dtype, error_handler)
    except _Error as exc:
        # Only happens with _strict_error_handler
        return InvalidArgumentError(exc.message)

    try:
        return Ok(pa.scalar(obj, dtype))
    except (pa.ArrowTypeError, pa.ArrowInvalid, OverflowError) as exc:
        if errors == "strict":
            return InvalidArgumentError(_extract_error_message(exc))
        return Ok(pa.NA)
