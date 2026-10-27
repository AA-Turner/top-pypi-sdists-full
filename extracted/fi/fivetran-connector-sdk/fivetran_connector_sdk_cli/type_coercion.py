"""Encoding of a row's values into the compact `row_data` form: one prefix byte plus a payload per column.

The bytes are the same as the ones Fivetran receives; timestamps use the same arithmetic.
"""
import json
import math
from datetime import date, datetime, timedelta
from calendar import timegm

from fivetran_connector_sdk_common.constants import (
    JAVA_LONG_MAX_VALUE, JAVA_LONG_MIN_VALUE, JAVA_INT_MAX_VALUE, JAVA_INT_MIN_VALUE,
)
from fivetran_connector_sdk_core.constants import CELL_BINARY, CELL_DOUBLE, CELL_FLOAT, CELL_JSON, CELL_NULL, CELL_SCALAR
from fivetran_connector_sdk_core.model import DataType  # the numbers are Fivetran's; the core reads what is written here


# The prefix byte of each kind of cell: the core defines them, as it is the one that reads them
_NULL_V     = bytes([CELL_NULL])
_PFX_SCALAR = bytes([CELL_SCALAR])
_PFX_JSON   = bytes([CELL_JSON])
_PFX_BINARY = bytes([CELL_BINARY])
_PFX_FLOAT  = bytes([CELL_FLOAT])
_PFX_DOUBLE = bytes([CELL_DOUBLE])

_EPOCH = datetime(1970, 1, 1)


def parse_utc_datetime(v):
    """
    Accepts a timezone-aware datetime object or a datetime string in one of the following formats:
    - '%Y-%m-%dT%H:%M:%S.%f%z' (e.g., '2025-08-12T15:00:00.123456+00:00')
    - '%Y-%m-%dT%H:%M:%S%z'    (e.g., '2025-08-12T15:00:00+00:00')
    - Same as above formats but with a space instead of 'T' as the separator (e.g., '2025-08-12 15:00:00+00:00')

    Returns a datetime.
    """
    if isinstance(v, datetime):
        return v
    v = v.strip().replace(' ', 'T', 1)
    return datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.%f%z" if '.' in v else "%Y-%m-%dT%H:%M:%S%z")


def parse_naive_datetime(v):
    """
    Accepts a datetime.datetime object or naive datetime string in one of the following formats:
    - '%Y-%m-%dT%H:%M:%S.%f'
    - '%Y-%m-%d %H:%M:%S.%f'
    Returns a datetime.
    """
    if isinstance(v, datetime):
        return v
    v = v.strip().replace(' ', 'T', 1)
    return datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.%f" if '.' in v else "%Y-%m-%dT%H:%M:%S")


def parse_naive_date(v):
    """
    Accepts a `datetime.date` object or a date string ('YYYY-MM-DD'),
    Returns a datetime at midnight.
    """
    if isinstance(v, str):
        return datetime.strptime(v, "%Y-%m-%d")
    if isinstance(v, (datetime, date)):
        return datetime.combine(v if isinstance(v, date) else v.date(), datetime.min.time())
    raise TypeError(f"Expected str, datetime.date, or datetime.datetime, got {type(v)}")


def _in_utc(dt):
    """The moment `dt` denotes as a naive UTC datetime; a naive `dt` is taken to be UTC (as `Timestamp.FromDatetime`)."""
    return _EPOCH + timedelta(seconds=timegm(dt.utctimetuple()), microseconds=dt.microsecond)


def _utc_json_string(dt):
    """RFC 3339 in UTC with 0, 3 or 6 fractional digits as needed (as `Timestamp.ToJsonString`)."""
    utc = _in_utc(dt)
    result = utc.replace(microsecond=0).isoformat()
    micros = utc.microsecond
    if micros == 0:
        return result + 'Z'
    if micros % 1000 == 0:
        return result + '.%03dZ' % (micros // 1000)
    return result + '.%06dZ' % micros


def _coerce_boolean(v):
    if isinstance(v, (bool, int, float)):
        return _PFX_SCALAR, b"true" if v else b"false"
    if isinstance(v, str) and v in ("0", "1"):
        return _PFX_SCALAR, b"false" if v == "0" else b"true"
    raise TypeError(f"BOOLEAN column does not accept {type(v).__name__}")


def _coerce_integer(v):
    if isinstance(v, float) and not v.is_integer():
        raise TypeError(f"Integer column requires int, got {type(v).__name__}")
    v = int(v)
    if v < JAVA_INT_MIN_VALUE or v > JAVA_INT_MAX_VALUE:
        raise ValueError(f"Value out of range: {v}")
    return _PFX_SCALAR, str(v).encode('utf-8')


def _coerce_long(v):
    if isinstance(v, float) and not v.is_integer():
        raise TypeError(f"Long column requires int, got {type(v).__name__}")
    v = int(v)
    if v < JAVA_LONG_MIN_VALUE or v > JAVA_LONG_MAX_VALUE:
        raise ValueError(f"Long value out of range: {v}")
    return _PFX_SCALAR, str(v).encode('utf-8')


def _coerce_float_type(v):
    fv = float(v)
    if math.isnan(fv):  return _PFX_FLOAT, b"NaN"
    if math.isinf(fv):  return _PFX_FLOAT, b"Infinity" if fv > 0 else b"-Infinity"
    return _PFX_FLOAT, str(fv).encode('utf-8')


def _coerce_double_type(v):
    fv = float(v)
    if math.isnan(fv):  return _PFX_DOUBLE, b"NaN"
    if math.isinf(fv):  return _PFX_DOUBLE, b"Infinity" if fv > 0 else b"-Infinity"
    return _PFX_DOUBLE, str(fv).encode('utf-8')


def _coerce_utc_datetime(v):
    if isinstance(v, date) and not isinstance(v, datetime):
        return _PFX_SCALAR, (v.isoformat() + "T00:00:00Z").encode('utf-8')
    return _PFX_SCALAR, _utc_json_string(parse_utc_datetime(v)).encode('utf-8')


def _coerce_naive_datetime(v):
    if isinstance(v, date) and not isinstance(v, datetime):
        return _PFX_SCALAR, (v.isoformat() + "T00:00:00").encode('utf-8')
    return _PFX_SCALAR, _in_utc(parse_naive_datetime(v)).isoformat().encode('utf-8')


def _coerce_naive_date(v):
    return _PFX_SCALAR, _in_utc(parse_naive_date(v)).date().isoformat().encode('utf-8')


def _raise_unsupported_type(v):
    raise ValueError("Unsupported data type encountered. Please use valid data types.")


def _coerce_json(v):
    return _PFX_JSON, json.dumps(v).encode('utf-8')


def _coerce_string(v):
    s = v if isinstance(v, str) else str(v)
    return _PFX_SCALAR, s.encode('utf-8')


def _coerce_decimal(v):
    if isinstance(v, bool):
        raise TypeError("DECIMAL column does not accept bool")
    if isinstance(v, (str, int)):
        return _PFX_SCALAR, str(v).encode('utf-8')
    raise TypeError(f"DECIMAL column requires str or int, got {type(v).__name__}")


def _coerce_xml(v):
    if not isinstance(v, str):
        raise TypeError(f"XML column requires str, got {type(v).__name__}")
    return _PFX_SCALAR, v.encode('utf-8')


def _coerce_binary_type(v):
    if isinstance(v, (bytes, bytearray)):
        return _PFX_BINARY, bytes(v)
    raise TypeError(f"BINARY column requires bytes or bytearray, got {type(v).__name__}")


def _coerce_inferred(v):
    if isinstance(v, str):
        return _PFX_SCALAR, v.encode('utf-8')
    if isinstance(v, bool):
        return _PFX_SCALAR, b"true" if v else b"false"
    if isinstance(v, int):
        if abs(v) > JAVA_LONG_MAX_VALUE:
            return _coerce_float_type(v)
        return _PFX_SCALAR, str(v).encode('utf-8')
    if isinstance(v, float):
        return _coerce_float_type(v)
    if isinstance(v, bytes):
        return _PFX_BINARY, v
    if isinstance(v, (dict, list)):
        return _PFX_JSON, json.dumps(v).encode('utf-8')
    return _PFX_SCALAR, str(v).encode('utf-8')


_COERCE_FN_BY_TYPE = {
    DataType.BOOLEAN:        _coerce_boolean,
    DataType.SHORT:          _coerce_integer,
    DataType.INT:            _coerce_integer,
    DataType.LONG:           _coerce_long,
    DataType.FLOAT:          _coerce_float_type,
    DataType.DOUBLE:         _coerce_double_type,
    DataType.DECIMAL:        _coerce_decimal,
    DataType.STRING:         _coerce_string,
    DataType.XML:            _coerce_xml,
    DataType.UTC_DATETIME:   _coerce_utc_datetime,
    DataType.NAIVE_DATETIME: _coerce_naive_datetime,
    DataType.NAIVE_DATE:     _coerce_naive_date,
    DataType.JSON:           _coerce_json,
    DataType.BINARY:         _coerce_binary_type,
    DataType.NAIVE_TIME:     _raise_unsupported_type,
}


def encode_row_data(column_types: dict, data: dict) -> dict:
    row_data = {}
    for key, v in data.items():
        if v is None:
            row_data[key] = _NULL_V
        else:
            pfx, val_b = _COERCE_FN_BY_TYPE.get(column_types.get(key), _coerce_inferred)(v)
            row_data[key] = pfx + val_b
    return row_data
