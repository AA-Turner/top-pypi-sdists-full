import base64
import datetime
import decimal
from collections.abc import Callable, Iterable, Mapping
from typing import Final, TypeAlias, cast

import pyarrow as pa
from google.protobuf import struct_pb2

from corvic.pa_scalar._temporal import (
    MonthDayNanoFrac,
    duration_toisoformat,
    month_day_nano_toisoformat,
)
from corvic.pa_scalar._types import Scalar

_PyValue = (
    bool
    | int
    | str
    | float
    | bytes
    | None
    | datetime.date
    | datetime.time
    | datetime.datetime
    | datetime.timedelta
    | decimal.Decimal
    | pa.MonthDayNano
    | Iterable["_PyValue"]
    # Map
    | Iterable[tuple["_PyValue", "_PyValue"]]
    # Struct
    | Mapping[str, "_PyValue"]
)


_TypeObserver: TypeAlias = Callable[[pa.DataType], bool]
_DispatchFn: TypeAlias = Callable[[_PyValue, pa.DataType], struct_pb2.Value]


def _visit_null(
    value: _PyValue,
    dtype: pa.DataType,
) -> struct_pb2.Value:
    return struct_pb2.Value(null_value=struct_pb2.NULL_VALUE)


def _visit_boolean(
    value: _PyValue,
    dtype: pa.DataType,
) -> struct_pb2.Value:
    value = cast(bool, value)
    return struct_pb2.Value(bool_value=value)


def _visit_int8(
    value: _PyValue,
    dtype: pa.DataType,
) -> struct_pb2.Value:
    value = cast(int, value)
    return struct_pb2.Value(number_value=value)


def _visit_int16(
    value: _PyValue,
    dtype: pa.DataType,
) -> struct_pb2.Value:
    value = cast(int, value)
    return struct_pb2.Value(number_value=value)


def _visit_int32(
    value: _PyValue,
    dtype: pa.DataType,
) -> struct_pb2.Value:
    value = cast(int, value)
    return struct_pb2.Value(number_value=value)


def _visit_int64(
    value: _PyValue,
    dtype: pa.DataType,
) -> struct_pb2.Value:
    value = cast(int, value)
    return struct_pb2.Value(string_value=str(value))


def _visit_uint8(
    value: _PyValue,
    dtype: pa.DataType,
) -> struct_pb2.Value:
    value = cast(int, value)
    return struct_pb2.Value(number_value=value)


def _visit_uint16(
    value: _PyValue,
    dtype: pa.DataType,
) -> struct_pb2.Value:
    value = cast(int, value)
    return struct_pb2.Value(number_value=value)


def _visit_uint32(
    value: _PyValue,
    dtype: pa.DataType,
) -> struct_pb2.Value:
    value = cast(int, value)
    return struct_pb2.Value(string_value=str(value))


def _visit_uint64(
    value: _PyValue,
    dtype: pa.DataType,
) -> struct_pb2.Value:
    value = cast(int, value)
    return struct_pb2.Value(string_value=str(value))


def _visit_float16(
    value: _PyValue,
    dtype: pa.DataType,
) -> struct_pb2.Value:
    value = cast(float, value)
    return struct_pb2.Value(number_value=value)


def _visit_float32(
    value: _PyValue,
    dtype: pa.DataType,
) -> struct_pb2.Value:
    value = cast(float, value)
    return struct_pb2.Value(number_value=value)


def _visit_float64(
    value: _PyValue,
    dtype: pa.DataType,
) -> struct_pb2.Value:
    value = cast(float, value)
    return struct_pb2.Value(number_value=value)


def _visit_any_binary(
    value: bytes,
    dtype: pa.DataType,
) -> struct_pb2.Value:
    b64enc = base64.b64encode(value)

    return struct_pb2.Value(string_value=b64enc.decode("utf-8"))


def _visit_binary(
    value: _PyValue,
    dtype: pa.DataType,
) -> struct_pb2.Value:
    return _visit_any_binary(cast(bytes, value), dtype)


def _visit_fixed_size_binary(
    value: _PyValue,
    dtype: pa.DataType,
) -> struct_pb2.Value:
    return _visit_any_binary(cast(bytes, value), dtype)


def _visit_large_binary(
    value: _PyValue,
    dtype: pa.DataType,
) -> struct_pb2.Value:
    return _visit_any_binary(cast(bytes, value), dtype)


def _visit_string(
    value: _PyValue,
    dtype: pa.DataType,
) -> struct_pb2.Value:
    value = cast(str, value)
    return struct_pb2.Value(string_value=value)


def _visit_large_string(
    value: _PyValue,
    dtype: pa.DataType,
) -> struct_pb2.Value:
    value = cast(str, value)
    return struct_pb2.Value(string_value=value)


def _visit_time32(
    value: _PyValue,
    dtype: pa.DataType,
) -> struct_pb2.Value:
    value = cast(datetime.time, value)

    return struct_pb2.Value(string_value=value.isoformat())


def _visit_time64(
    value: _PyValue,
    dtype: pa.DataType,
) -> struct_pb2.Value:
    value = cast(datetime.time, value)

    return struct_pb2.Value(string_value=value.isoformat())


def _visit_date32(
    value: _PyValue,
    dtype: pa.DataType,
) -> struct_pb2.Value:
    value = cast(datetime.date, value)

    return struct_pb2.Value(string_value=value.isoformat())


def _visit_date64(
    value: _PyValue,
    dtype: pa.DataType,
) -> struct_pb2.Value:
    value = cast(datetime.date, value)

    return struct_pb2.Value(string_value=value.isoformat())


def _visit_timestamp(
    value: _PyValue,
    dtype: pa.DataType,
) -> struct_pb2.Value:
    value = cast(datetime.datetime, value)

    return struct_pb2.Value(string_value=value.isoformat())


def _visit_duration(
    value: _PyValue,
    dtype: pa.DataType,
) -> struct_pb2.Value:
    value = cast(datetime.timedelta, value)

    return struct_pb2.Value(string_value=duration_toisoformat(value))


def _visit_interval(
    value: _PyValue,
    dtype: pa.DataType,
) -> struct_pb2.Value:
    value = cast(pa.MonthDayNano, value)

    mdnf = MonthDayNanoFrac(
        month=value.months, day=value.days, nano=value.nanoseconds, second_frac=None
    )
    return struct_pb2.Value(string_value=month_day_nano_toisoformat(mdnf))


def _visit_decimal128(
    value: _PyValue,
    dtype: pa.DataType,
) -> struct_pb2.Value:
    value = cast(decimal.Decimal, value)
    return struct_pb2.Value(string_value=str(value))


def _visit_decimal256(
    value: _PyValue,
    dtype: pa.DataType,
) -> struct_pb2.Value:
    value = cast(decimal.Decimal, value)
    return struct_pb2.Value(string_value=str(value))


def _visit_any_list(
    values: Iterable[_PyValue],
    dtype: pa.DataType,
) -> struct_pb2.Value:
    return struct_pb2.Value(
        list_value=struct_pb2.ListValue(values=[_visit(x, dtype) for x in values])
    )


def _visit_list(
    value: _PyValue,
    dtype: pa.DataType,
) -> struct_pb2.Value:
    dtype = cast(pa.ListType, dtype)
    value = cast(Iterable[_PyValue], value)
    return _visit_any_list(value, dtype.value_type)


def _visit_fixed_size_list(
    value: _PyValue,
    dtype: pa.DataType,
) -> struct_pb2.Value:
    dtype = cast(pa.FixedSizeListType, dtype)
    value = cast(Iterable[_PyValue], value)
    return _visit_any_list(value, dtype.value_type)


def _visit_large_list(
    value: _PyValue,
    dtype: pa.DataType,
) -> struct_pb2.Value:
    dtype = cast(pa.LargeListType, dtype)
    value = cast(Iterable[_PyValue], value)
    return _visit_any_list(value, dtype.value_type)


def _visit_dictionary(
    value: _PyValue,
    dtype: pa.DataType,
) -> struct_pb2.Value:
    dtype = cast(pa.DictionaryType, dtype)
    return _visit(value, dtype.value_type)


def _visit_map(value: _PyValue, dtype: pa.DataType) -> struct_pb2.Value:
    dtype = cast(pa.MapType, dtype)
    values = cast(Iterable[tuple[_PyValue, _PyValue]], value)

    ret: list[struct_pb2.Value] = []
    for p1, p2 in values:
        k = _visit(p1, dtype.key_type)
        v = _visit(p2, dtype.item_type)
        ret.append(struct_pb2.Value(list_value=struct_pb2.ListValue(values=(k, v))))

    return struct_pb2.Value(list_value=struct_pb2.ListValue(values=ret))


def _visit_struct(
    value: _PyValue,
    dtype: pa.DataType,
) -> struct_pb2.Value:
    dtype = cast(pa.StructType, dtype)
    value = cast(Mapping[str, _PyValue], value)

    fields_by_name = {field.name: field for field in dtype}

    return struct_pb2.Value(
        struct_value=struct_pb2.Struct(
            fields={k: _visit(v, fields_by_name[k].type) for k, v in value.items()}
        )
    )


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
    value: _PyValue,
    dtype: pa.DataType,
) -> struct_pb2.Value:
    if value is None:
        return struct_pb2.Value(null_value=struct_pb2.NULL_VALUE)

    for is_type, dispatch in _DISPATCH_FUNCTIONS:
        if is_type(dtype):
            return dispatch(value, dtype)

    raise ValueError(f"unknown dtype: {dtype}")


def to_value(
    scalar: Scalar | float | str | bool | None | struct_pb2.Value,
) -> struct_pb2.Value:
    """Convert Scalar (or convenient Scalar equivalents) to struct_pb2.Value."""
    match scalar:
        # Order matters: bools are ints but ints are not bools
        case bool():
            return struct_pb2.Value(bool_value=scalar)
        case int():
            return struct_pb2.Value(string_value=str(scalar))
        case float():
            return struct_pb2.Value(number_value=scalar)
        case str():
            return struct_pb2.Value(string_value=scalar)
        case None:
            return struct_pb2.Value(null_value=struct_pb2.NULL_VALUE)
        case struct_pb2.Value():
            return scalar
        case _:
            value = cast(_PyValue, scalar.as_py())
            return _visit(value, scalar.type)


def batch_to_structs(
    batch: pa.RecordBatch,
) -> list[struct_pb2.Struct]:
    """Convert RecordBatch to list of struct_pb2.Struct."""
    schema = batch.schema
    field_by_name = {field.name: field for field in schema}

    ret: list[struct_pb2.Struct] = []
    for row in batch.to_pylist():
        fields = {
            col_name: _visit(v, field_by_name[col_name].type)
            for col_name, v in row.items()
        }
        ret.append(struct_pb2.Struct(fields=fields))

    return ret
