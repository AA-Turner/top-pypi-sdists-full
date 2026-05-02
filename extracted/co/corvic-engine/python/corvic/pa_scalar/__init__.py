"""Conversions to and from Arrow scalar values.

Arrow Data Type | JSON Type (format)
----------------+-------------------
(large_)binary  | string (base64 encoded)
bool            | bool
date{32,64}     | string (ISO 8601 date, e.g., 2012-01-02)
decimal128      | string (rational number)
dictionary      | <JSON representation of Arrow value type>
duration        | string (ISO 8601 duration, e.g., PT3.4S)
float{16,32,64} | number
interval        | string (ISO 8601 duration, e.g., P1MT2D3.4S)
int{8,16,32}    | number
list            | list
map             | list of key-value tuples
null            | null
(large_)string  | string
struct          | object
timestamp       | string (RFC 3339, e.g., 2012-01-02T13:01:02.34Z)
uint{8,16,32}   | number
"""

from corvic.pa_scalar._from_value import from_value
from corvic.pa_scalar._to_value import batch_to_structs, to_value
from corvic.pa_scalar._types import PyValue, Scalar

__all__ = [
    "PyValue",
    "Scalar",
    "batch_to_structs",
    "from_value",
    "to_value",
]
