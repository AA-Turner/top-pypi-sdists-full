from __future__ import annotations

import base64
import collections.abc
import ipaddress
import math
import uuid
from datetime import date, datetime, time, timedelta
from typing import List, Type, Union, cast, get_args, get_origin

from chalk_rs import duration_isoformat as _duration_isoformat
from chalk_rs import parse_datetime as _parse_datetime
from chalk_rs import parse_iso_date as _parse_iso_date
from chalk_rs import parse_iso_duration as _parse_iso_duration
from chalk_rs import parse_iso_time as _parse_iso_time

try:
    from pydantic.v1 import BaseModel
except ImportError:
    from pydantic import BaseModel  # type: ignore[assignment]

from chalk.features._encoding.primitive import ChalkStructType, TPrimitive
from chalk.utils.json import TJSON

__all__ = ["unstructure_primitive_to_json", "structure_json_to_primitive"]


# ---------------------------------------------------------------------------
# Standalone implementations (no cattrs)
# ---------------------------------------------------------------------------


def unstructure_primitive_to_json(val: TPrimitive, encode_structs_as_objects: bool = False) -> TJSON:
    """Convert a Python primitive value to a JSON-compatible value.

    ``encode_structs_as_objects=False`` (default): struct dicts are encoded as
    positional lists of values (the historical wire format).
    ``encode_structs_as_objects=True``: struct dicts are encoded as objects.
    """
    if val is None:
        return None
    if isinstance(val, bool):
        return val
    # datetime must precede date — datetime is a subclass of date
    if isinstance(val, datetime):
        return val.isoformat()
    if isinstance(val, date):
        return val.isoformat()
    if isinstance(val, time):
        return val.isoformat()
    if isinstance(val, timedelta):
        return _duration_isoformat(val)
    if isinstance(val, bytes):
        return base64.b64encode(val).decode("utf8")
    if isinstance(val, dict):
        if encode_structs_as_objects:
            return {k: unstructure_primitive_to_json(v, encode_structs_as_objects) for k, v in val.items()}
        return [unstructure_primitive_to_json(v, encode_structs_as_objects) for v in val.values()]
    if isinstance(val, (list, tuple)):
        return [unstructure_primitive_to_json(v, encode_structs_as_objects) for v in val]
    # int, float, str, uuid.UUID, IPv4Address, IPv6Address — pass through
    return val  # type: ignore[return-value]


def structure_json_to_primitive(val: Union[TJSON, TPrimitive], typ: Type[TPrimitive]) -> TPrimitive:
    """Parse a JSON value back to a Python primitive given a type hint."""
    # Optional[T] / Union[T, None] — unwrap and recurse
    if get_origin(typ) is Union:
        inner_args = [a for a in get_args(typ) if a is not type(None)]
        if len(inner_args) == 1:
            if val is None:
                return cast(TPrimitive, None)
            return structure_json_to_primitive(val, inner_args[0])

    # ChalkStructType — positional list or dict → field dict
    if isinstance(typ, ChalkStructType):
        type_hints = typ.__chalk_type_hints__
        if val is None:
            return {field_name: structure_json_to_primitive(None, hint) for field_name, hint in type_hints.items()}
        if isinstance(val, collections.abc.Mapping):
            return {
                field_name: structure_json_to_primitive(val.get(field_name), hint)  # type: ignore[union-attr]
                for field_name, hint in type_hints.items()
            }
        if not isinstance(val, collections.abc.Sequence):
            raise TypeError(f"Expected structs to be serialized as lists. Object `{val}` is not a sequence.")
        if len(type_hints) != len(val):  # type: ignore[arg-type]
            raise TypeError(
                f"Unable to structure object `{val}` of size {len(val)} into type "  # type: ignore[arg-type]
                f"`{typ.__name__}` of size {len(type_hints)}. Size mismatch."
            )
        return {
            field_name: (None if x is None else structure_json_to_primitive(x, hint))
            for (x, field_name), hint in zip(zip(val, type_hints.keys()), type_hints.values())  # type: ignore[arg-type]
        }

    # Generic alias: List[X]
    origin = get_origin(typ)
    if origin is list:
        args = get_args(typ)
        if len(args) < 1:
            raise TypeError(
                f"{typ} types must be parameterized with the type of the contained value -- for example, `{typ}[int]`"
            )
        if len(args) > 1:
            raise TypeError(f"{typ} should be parameterized with only one type")
        if val is None:
            return cast(List, None)
        if not isinstance(val, (list, tuple)):
            raise TypeError(f"Expected a list, Object `{val}` is not a list.")
        inner_typ = args[0]
        return [structure_json_to_primitive(x, inner_typ) for x in val]  # type: ignore[return-value]

    # Generic alias: Dict[K, V]
    if origin is dict:
        args = get_args(typ)
        if len(args) == 0:
            raise TypeError(
                f"{typ} types must be parameterized with the key and value types -- for example, `{typ}[str, int]`"
            )
        if len(args) != 2:
            raise TypeError(f"{typ} should be parameterized with two types, found: {typ}")
        if val is None:
            return None
        if isinstance(val, list):
            val = dict(val)
        return {k: structure_json_to_primitive(v, args[1]) for k, v in val.items()}  # type: ignore[union-attr,return-value]

    # Scalar types — None passthrough for all
    if val is None:
        return None

    # datetime before date — datetime is a subclass of date
    if typ is datetime:
        if isinstance(val, datetime):
            return val
        if isinstance(val, date):
            return datetime.combine(val, time())
        if not isinstance(val, str):
            raise TypeError(
                f"Datetime values must be serialized as ISO strings. Instead, received value '{val}' of type `{type(val).__name__}`"
            )
        return _parse_datetime(val)

    if isinstance(typ, type) and issubclass(typ, date) and not issubclass(typ, datetime):
        if isinstance(val, datetime):
            return val.date()
        if isinstance(val, date):
            return val
        if not isinstance(val, str):
            raise TypeError(
                f"Date values must be serialized as ISO strings. Instead, received value '{val}' of type `{type(val).__name__}`"
            )
        return _parse_iso_date(val)

    if typ is time:
        if isinstance(val, time):
            return val
        if not isinstance(val, str):
            raise TypeError(
                f"Time values must be serialized as ISO strings. Instead, received value '{val}' of type `{type(val).__name__}`"
            )
        return _parse_iso_time(val)

    if typ is timedelta:
        if isinstance(val, timedelta):
            return val
        if not isinstance(val, str):
            raise TypeError(
                f"Timedelta values should be serialized as strings. Instead, received value '{val}' of type `{type(val).__name__}`"
            )
        return _parse_iso_duration(val)

    if typ is bytes:
        if isinstance(val, str):
            return base64.b64decode(val)
        if isinstance(val, bytes):
            return val
        raise TypeError(
            f"Byte values must be bytes objects or Base64-encoded strings. Instead, received value '{val}' of type `{type(val).__name__}`"
        )

    if typ is uuid.UUID:
        if isinstance(val, uuid.UUID):
            return val
        if not isinstance(val, str):
            raise TypeError(
                f"UUID values should be serialized as strings. Instead, received value '{val}' of type `{type(val).__name__}`"
            )
        return uuid.UUID(val)  # type: ignore[return-value]

    if typ is ipaddress.IPv4Address:
        if isinstance(val, ipaddress.IPv4Address):
            return val
        if isinstance(val, (int, str)):
            return ipaddress.IPv4Address(val)  # type: ignore[return-value]
        raise TypeError(f"IPv4Address values should be serialized as strings or integers. Received {val}")

    if typ is ipaddress.IPv6Address:
        if isinstance(val, ipaddress.IPv6Address):
            return val
        if isinstance(val, (int, str)):
            return ipaddress.IPv6Address(val)  # type: ignore[return-value]
        raise TypeError(f"IPv6Address values should be serialized as strings or integers. Received {val}")

    # bool before int — bool is a subclass of int
    if isinstance(typ, type) and issubclass(typ, bool):
        if val in (1, True):
            return True
        if val in (0, False):
            return False
        raise TypeError(f"Cannot convert '{val}' to a Boolean. Valid values are 1, True, 0, or False.")

    if isinstance(typ, type) and issubclass(typ, (int, float)):
        if not isinstance(val, str) and typ(val) != val and not math.isnan(val):  # type: ignore[arg-type]
            raise TypeError(f"Cannot cast '{val}' of type {type(val)} to a {typ} without losing precision")
        return typ(val)  # type: ignore[call-arg,return-value]

    if isinstance(typ, type) and issubclass(typ, str):
        return str(val)

    return val  # type: ignore[return-value]


class FeatureEncodingOptions(BaseModel, frozen=True):
    encode_structs_as_objects: bool = False
    """
    If 'True', a struct type will be encoded as a json object.
    If 'False', a struct type will be encoded as an array where the n-th element
    corresponds to the n-th field of the struct.
    """
