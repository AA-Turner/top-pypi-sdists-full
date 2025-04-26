from __future__ import annotations

import base64
import collections.abc
import dataclasses
import decimal
import enum
import ipaddress
import uuid
from datetime import date, datetime, time, timedelta
from typing import Any, FrozenSet, List, Set, Tuple, Type, TypeVar, Union, cast

import attrs
import cattrs
import dateutil.parser
import isodate

# Need the *real* BaseModel here (not the v1 one) so that we can register the right hook
from pydantic import BaseModel as BaseBaseModel

try:
    from pydantic.v1 import BaseModel as V1BaseModel
except ImportError:
    V1BaseModel = None

from typing_extensions import get_args, get_origin, is_typeddict

from chalk.features._encoding.primitive import ChalkStructType, TPrimitive
from chalk.utils.cached_type_hints import cached_get_type_hints
from chalk.utils.collections import is_namedtuple, unwrap_optional_and_annotated_if_needed
from chalk.utils.enum import get_enum_value_type
from chalk.utils.json import JSON
from chalk.utils.pydanticutil.pydantic_compat import is_pydantic_basemodel

TRich = TypeVar("TRich")
T = TypeVar("T")

# Converter to go from TPython to a TPrimitive
_rich_converter = cattrs.Converter()

#########
# Structs
#########

_rich_converter.register_unstructure_hook_func(
    is_namedtuple, lambda x: {k: _rich_converter.unstructure(v) for (k, v) in x._asdict().items()}
)
_rich_converter.register_unstructure_hook_func(
    dataclasses.is_dataclass,
    lambda x: {field.name: _rich_converter.unstructure(getattr(x, field.name)) for field in dataclasses.fields(x)},
)
_rich_converter.register_unstructure_hook(
    BaseBaseModel, lambda x: {k: _rich_converter.unstructure(v) for (k, v) in x.dict().items()}
)
if V1BaseModel is not None:
    _rich_converter.register_unstructure_hook(
        V1BaseModel, lambda x: {k: _rich_converter.unstructure(v) for (k, v) in x.dict().items()}
    )
_rich_converter.register_unstructure_hook_func(
    attrs.has,
    lambda x: {k: _rich_converter.unstructure(v) for (k, v) in attrs.asdict(x, recurse=False).items()},
)


def _is_struct(typ: Type):
    typ = unwrap_optional_and_annotated_if_needed(typ)
    return (
        is_namedtuple(typ)
        or dataclasses.is_dataclass(typ)
        or is_typeddict(typ)
        or (isinstance(typ, type) and is_pydantic_basemodel(typ))
        or attrs.has(typ)
    )


def _structure_struct(obj: Any, typ: Type):
    if not isinstance(obj, (collections.abc.Sequence, collections.abc.Mapping)):
        # If an already-constructed class is passed in, then we still need to restructure it
        # to ensure that any recursive fields are properly structured
        obj = _rich_converter.unstructure(obj)
    typ = unwrap_optional_and_annotated_if_needed(typ)
    type_hints = cached_get_type_hints(typ)
    if obj is None:
        obj = {k: None for k in type_hints}
    if isinstance(obj, collections.abc.Sequence):
        obj = {k: v for (k, v) in zip(type_hints.keys(), obj)}
    if not isinstance(obj, collections.abc.Mapping):
        raise TypeError(f"Unable to structure object `{obj}` into type `{typ}`. Only dictionaries are supported.")
    kwargs = {k: _rich_converter.structure(v, type_hints[k]) for (k, v) in obj.items()}
    if isinstance(typ, type) and is_pydantic_basemodel(typ):  # pyright: ignore[reportUnnecessaryIsInstance]
        # Using .construct to bypass pydantic validation, which could fail if there are null values in kwargs
        # and the field is not annotated as null
        return typ.construct(**kwargs)
    else:
        return typ(**kwargs)


def is_chalk_struct(typ: Type):
    return isinstance(typ, ChalkStructType)


def _structure_chalk_struct(obj: Any, typ: Type):
    if not isinstance(typ, ChalkStructType):
        raise TypeError(f"Expected ChalkStructType instead of {typ}")
    type_hints = typ.__chalk_type_hints__
    if obj is None:
        obj = {k: None for k in type_hints}
    if isinstance(obj, collections.abc.Sequence):
        obj = {k: v for (k, v) in zip(type_hints.keys(), obj)}
    if not isinstance(obj, collections.abc.Mapping):
        raise TypeError(f"Unable to structure object `{obj}` into type `{typ}`. Only dictionaries are supported.")
    return {k: _rich_converter.structure(v, type_hints[k]) for (k, v) in obj.items()}


_rich_converter.register_structure_hook_func(_is_struct, _structure_struct)
_rich_converter.register_structure_hook_func(is_chalk_struct, _structure_chalk_struct)

#############
# Collections
#############

# Unlike lists and tuples which are ordered, sets are unordered
# Thus, when converting to a list, the order must be consistent
# To do so, sort all the values
_rich_converter.register_unstructure_hook(set, lambda x: sorted(list(x)))
_rich_converter.register_unstructure_hook(frozenset, lambda x: sorted(list(x)))


# Lists and tuples do not need an unstructure hook -- the default is fine


def _structure_collection(
    obj: Any, typ: Union[Type[FrozenSet[T]], Type[Set[T]], Type[List[T]], Type[Tuple[T, ...]]]
) -> Union[FrozenSet[T], Set[T], List[T], Tuple[T, ...]]:
    origin = get_origin(typ)
    if origin in (set, Set):
        constructor = set
    elif origin in (frozenset, FrozenSet):
        constructor = frozenset
    elif origin in (list, List):
        constructor = list
    elif origin in (tuple, Tuple):
        constructor = tuple
    else:
        raise TypeError(f"Unsupported set type: {typ}")
    args = get_args(typ)
    if len(args) < 1:
        raise TypeError(
            f"{typ} types must be parameterized with the type of the contained value -- for example, `{typ}[int]`"
        )
    if len(args) > 1:
        if origin in (tuple, Tuple):
            if len(args) != 2 and args[1] != ...:
                raise TypeError(
                    (
                        "Tuple features must have a fixed type and be variable-length tuples (e.g. `Tuple[int, ...]`). "
                        " If you would like a fixed-length of potentially different types, used a NamedTuple."
                    )
                )
        else:
            raise TypeError(f"{typ} should be parameterized with only one type")

    inner_typ = args[0]
    if obj is None:
        return cast(Union[FrozenSet[T], Set[T], List[T], Tuple[T, ...]], None)
    if not isinstance(obj, (collections.abc.Set, collections.abc.Sequence)):
        raise TypeError(f"Cannot structure '{obj}' into a `{typ}`")
    return constructor(_rich_converter.structure(x, inner_typ) for x in obj)


def _is_collection(typ: Type):
    origin = get_origin(typ)
    return origin in (
        set,
        Set,
        frozenset,
        FrozenSet,
        list,
        List,
        tuple,
        Tuple,
    )


_rich_converter.register_structure_hook_func(_is_collection, _structure_collection)

#######
# Enums
#######

_rich_converter.register_unstructure_hook(enum.Enum, lambda x: _rich_converter.unstructure(x.value))


def _structure_enum(obj: Any, typ: Type[enum.Enum]) -> enum.Enum:
    if isinstance(obj, typ):
        return obj
    if obj is None:
        return cast(enum.Enum, None)
    enum_typ = get_enum_value_type(typ)
    try:
        return typ(_rich_converter.structure(obj, enum_typ))
    except (TypeError, ValueError):
        pass
    if isinstance(obj, str):
        try:
            return typ[obj]
        except KeyError:
            pass
    allowed_values = ", ".join(f"'{x}'" for x in typ.__members__.values())
    raise ValueError(f"Cannot convert '{obj}' to Enum `{typ}`. Possible values are: {allowed_values}")


_rich_converter.register_structure_hook(enum.Enum, _structure_enum)

##########
# Decimals
##########

_rich_converter.register_unstructure_hook(decimal.Decimal, lambda x: str(x.normalize()))


def _structure_decimal(obj: Any, typ: Type[decimal.Decimal]) -> decimal.Decimal:
    if obj is None:
        return cast(decimal.Decimal, None)
    if isinstance(obj, decimal.Decimal):
        return obj
    return decimal.Decimal(obj)


_rich_converter.register_structure_hook(decimal.Decimal, _structure_decimal)

#######
# Bytes
#######

_rich_converter.register_unstructure_hook(bytes, lambda x: x)


def _structure_bytes(x: Any, typ: Type[bytes]) -> bytes:
    if x is None:
        return cast(bytes, None)
    if isinstance(x, bytes):
        return x
    if isinstance(x, str):
        return base64.b64decode(x)
    raise TypeError(f"Cannot structure {x} into bytes")


_rich_converter.register_structure_hook(bytes, _structure_bytes)

##########
# Duration
##########

_rich_converter.register_unstructure_hook(timedelta, lambda x: x)


def _structure_timedelta(x: Any, typ: Type[timedelta]) -> timedelta:
    if x is None:
        return cast(timedelta, None)
    if isinstance(x, timedelta):
        return x
    if isinstance(x, str):
        return isodate.parse_duration(x)
    raise TypeError(f"Cannot structure {x} into a duration")


_rich_converter.register_structure_hook(timedelta, _structure_timedelta)

######
# Date
######

_rich_converter.register_unstructure_hook_func(
    lambda x: isinstance(x, date) and not isinstance(x, datetime), lambda x: x
)


def _structure_date(x: Any, typ: Type[date]) -> date:
    if x is None:
        return cast(date, None)
    if isinstance(x, datetime):
        if x.time() != time():
            raise TypeError(f"Datetime '{x}' has a non-zero time component, which cannot be safely cast into a date")
        return x.date()
    if isinstance(x, date):
        return x
    if isinstance(x, str):
        return isodate.parse_date(x)
    raise TypeError(f"Cannot structure {x} into a date")


_rich_converter.register_structure_hook_func(
    lambda x: isinstance(x, type)  # pyright: ignore[reportUnnecessaryIsInstance]
    and issubclass(x, date)  # pyright: ignore[reportUnnecessaryIsInstance]
    and not issubclass(x, datetime),
    _structure_date,
)

######
# Time
######

_rich_converter.register_unstructure_hook(time, lambda x: x)


def _structure_time(x: Any, typ: Type[time]) -> time:
    if x is None:
        return cast(time, None)
    if isinstance(x, time):
        return x
    if isinstance(x, str):
        return isodate.parse_time(x)
    raise TypeError(f"Cannot structure {x} into a time")


_rich_converter.register_structure_hook(time, _structure_time)

##########
# Datetime
##########

_rich_converter.register_unstructure_hook(datetime, lambda x: x)


def _structure_datetime(x: Any, typ: Type[datetime]) -> datetime:
    if x is None:
        return cast(datetime, None)
    if isinstance(x, str):
        x = dateutil.parser.parse(x)
    if isinstance(x, datetime):
        return x
    if isinstance(x, date):
        return datetime.combine(x, time())
    raise TypeError(f"Cannot structure {x} into a datetime")


_rich_converter.register_structure_hook(datetime, _structure_datetime)

##########
# UUID
##########

_rich_converter.register_unstructure_hook(uuid.UUID, lambda x: x)


def _structure_uuid(x: Any, typ: Type[uuid.UUID]) -> uuid.UUID:
    if x is None:
        return cast(uuid.UUID, None)
    if isinstance(x, uuid.UUID):
        return x
    if isinstance(x, str):
        return uuid.UUID(x)
    raise TypeError(f"Cannot structure {x} into a uuid.UUID")


_rich_converter.register_structure_hook(uuid.UUID, _structure_uuid)

"""
ipaddress.IPv4Network
"""
_rich_converter.register_unstructure_hook(ipaddress.IPv4Address, lambda x: x)


def _structure_ipv4(x: Any, typ: Type[ipaddress.IPv4Address]) -> ipaddress.IPv4Address:
    if x is None:
        return cast(ipaddress.IPv4Address, None)
    if isinstance(x, ipaddress.IPv4Address):
        return x
    if isinstance(x, str):
        return ipaddress.IPv4Address(x)
    if isinstance(x, int):
        return ipaddress.IPv4Address(x)
    raise TypeError(f"Cannot structure {x} into an ipaddress.IPv4Address")


_rich_converter.register_structure_hook(ipaddress.IPv4Address, _structure_ipv4)

"""
ipaddress.IPv6Network
"""
_rich_converter.register_unstructure_hook(ipaddress.IPv6Address, lambda x: x)


def _structure_ipv6(x: Any, typ: Type[ipaddress.IPv6Address]) -> ipaddress.IPv6Address:
    if x is None:
        return cast(ipaddress.IPv6Address, None)
    if isinstance(x, ipaddress.IPv6Address):
        return x
    if isinstance(x, str):
        return ipaddress.IPv6Address(x)
    if isinstance(x, int):
        return ipaddress.IPv6Address(x)
    raise TypeError(f"Cannot structure {x} into an ipaddress.IPv6Address")


_rich_converter.register_structure_hook(ipaddress.IPv6Address, _structure_ipv6)

#############
# Numpy types
#############
try:
    import numpy as np
except ImportError:
    pass
else:
    _rich_converter.register_unstructure_hook_func(lambda x: np.issubdtype(x, np.bool_), bool)
    _rich_converter.register_unstructure_hook_func(lambda x: np.issubdtype(x, np.integer), int)
    _rich_converter.register_unstructure_hook_func(lambda x: np.issubdtype(x, np.floating), float)


##############
# Rich types
##############


def _structure_rich(obj: Any, typ: Type):
    if obj is None:
        # Always allow None, even if the field is non-optional
        return None
    if issubclass(typ, enum.Enum):
        return _structure_enum(obj, typ)
    if isinstance(obj, typ):
        return obj
    if issubclass(typ, bool):
        # For booleans, we don't want to use the bool(...) constructor, as
        # that doesn't handle strings like y/yes/n/no/t/true/f/false
        if isinstance(obj, str):
            if obj.lower() in ("y", "yes", "t", "true", "1"):
                return True
            if obj.lower() in ("n", "no", "f", "false", "0"):
                return False
        if isinstance(obj, int):
            if obj == 0:
                return False
            if obj == 1:
                return True
        if np and isinstance(obj, np.bool_):
            return bool(obj)
        raise ValueError(
            f"Cannot convert {obj} to a boolean. Allowed values are y, yes, t, true, 1, n, no, f, false, 0."
        )

    if (
        isinstance(obj, (list, set, frozenset, dict, tuple, BaseBaseModel))
        or (V1BaseModel is not None and isinstance(obj, V1BaseModel))
        or dataclasses.is_dataclass(obj)
        or attrs.has(type(obj))
    ):
        raise ValueError(f"Object {obj} of type {type(obj).__name__} cannot be converted into a {typ.__name__}")

    return typ(obj)  # pyright: ignore[reportCallIssue]


_rich_converter.register_structure_hook(int, _structure_rich)
_rich_converter.register_structure_hook(float, _structure_rich)
_rich_converter.register_structure_hook(bytes, _structure_rich)
_rich_converter.register_structure_hook(str, _structure_rich)
_rich_converter.register_structure_hook(bool, _structure_rich)


def unstructure_rich_to_primitive(val: Any) -> TPrimitive:
    if val is None or type(val) in (str, int, float, bytes, time, datetime, date, timedelta, bool):
        # Short-circuit these rich types, as the primitive types are the same
        return val
    # Special case for enums, particularly enums that use a mixin
    # i.e. class MyEnum(str, enum.Enum)
    # cattrs seems unable to detect that the class inherits from Enum so doesn't call the correct serde hooks
    if isinstance(val, enum.Enum):
        return _rich_converter.unstructure(val.value)
    return _rich_converter.unstructure(val)


def structure_primitive_to_rich(val: TPrimitive, typ: Type[TRich]) -> TRich:
    if (
        (val is None or type(val) is typ)
        and typ
        in (
            str,
            int,
            bool,
            float,
            bytes,
            timedelta,
            decimal.Decimal,
            date,
            datetime,
            time,
        )
    ) or typ is JSON:  # pyright: ignore[reportUnnecessaryComparison]
        # Short circuit these rich types
        return cast(TRich, val)
    return _rich_converter.structure(val, typ)
