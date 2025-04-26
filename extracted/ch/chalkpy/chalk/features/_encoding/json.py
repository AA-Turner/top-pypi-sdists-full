from __future__ import annotations

import base64
import collections.abc
import ipaddress
import math
import uuid
from datetime import date, datetime, time, timedelta
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, Union, cast

import cattrs
import dateutil.parser
import isodate
from typing_extensions import get_args, get_origin

from chalk.features._encoding.primitive import ChalkStructType, TPrimitive
from chalk.features._encoding.rich import is_chalk_struct
from chalk.utils.json import TJSON

if TYPE_CHECKING:
    import pydantic
else:
    try:
        import pydantic.v1 as pydantic
    except ImportError:
        import pydantic

__all__ = ["unstructure_primitive_to_json", "structure_json_to_primitive"]


def unstructure_primitive_to_json(val: TPrimitive) -> TJSON:
    return _default_feature_json_converter.unstructure_primitive_to_json(val)


def structure_json_to_primitive(val: Union[TJSON, TPrimitive], typ: Type[TPrimitive]) -> TPrimitive:
    return _default_feature_json_converter.structure_json_to_primitive(val, typ)


class FeatureJsonConverter:
    def __init__(self, options: FeatureEncodingOptions):
        super().__init__()
        self._json_converter = cattrs.Converter()
        self._options = options
        #######
        # Dicts
        #######

        # All structs get mapped to a typeddict primitive type
        # However, on the wire, we serialize typedicts as lists by field order, similar
        # to how structs are commonly serialized by values
        # Hence, the JSON converter needs to convert all dicts into lists of the values
        # In py3.7+, all dicts are ordered. So, simply iterating over the dict values is sufficient

        if self._options.encode_structs_as_objects:
            self._json_converter.register_unstructure_hook(
                dict, lambda x: {k: self._json_converter.unstructure(v) for k, v in x.items()}
            )
        else:
            self._json_converter.register_unstructure_hook(
                dict, lambda x: [self._json_converter.unstructure(y) for y in x.values()]
            )

        def _structure_dicts(obj: Any, typ: Type):
            # try to treat the incoming 'val' as a dict if typ is a dict
            # ie: if typ == typing.Dict[str, typing.Optional[str]], treat value of [["a","b"],["c","d"]] as {"a": "b", "c": "d"}
            if isinstance(obj, list):
                obj = dict(obj)

            args = get_args(typ)
            if len(args) == 0:
                raise TypeError(
                    f"{typ} types must be parameterized with the key and value types -- for example, `{typ}[str, int]`"
                )
            elif len(args) != 2:
                raise TypeError(f"{typ} should be parameterized with two types, found: {typ}")

            return {k: self._json_converter.structure(v, args[1]) for k, v in obj.items()}

        def _is_dict(typ: Type):
            origin = get_origin(typ)
            return origin in (dict, Dict)

        self._json_converter.register_structure_hook_func(_is_dict, _structure_dicts)

        def _structure_chalk_struct(obj: Any, typ: Type):
            if not isinstance(typ, ChalkStructType):
                raise TypeError(f"Expected ChalkStructType instead of {typ}")
            type_hints = typ.__chalk_type_hints__
            if obj is None:
                return {
                    field_name: self._json_converter.structure(None, type_hint)
                    for (field_name, type_hint) in type_hints.items()
                }
            if isinstance(obj, collections.abc.Mapping):
                # If given a dict, assume it is the primitive type being passed in as the json type
                return {
                    field_name: self._json_converter.structure(obj.get(field_name), type_hint)
                    for (field_name, type_hint) in type_hints.items()
                }
            if not isinstance(obj, collections.abc.Sequence):
                raise TypeError(f"Expected structs to be serialized as lists. Object `{obj}` is not a sequence.")

            if len(type_hints) != len(obj):
                raise TypeError(
                    f"Unable to structure object `{obj}` of size {len(obj)} into type `{typ.__name__}` of size {len(type_hints)}. Size mismatch."
                )

            kwargs = {
                field_name: None if x is None else self._json_converter.structure(x, type_hints[field_name])
                for (x, field_name) in zip(obj, type_hints.keys())
            }
            return kwargs

        self._json_converter.register_structure_hook_func(is_chalk_struct, _structure_chalk_struct)

        #######
        # Lists
        #######

        # The default unstructure hook is fine
        # However, when structuring, we want to allow None for annotations of list[...]

        def _structure_list(obj: Optional[List], typ: Type[List]) -> List:
            args = get_args(typ)

            if len(args) < 1:
                raise TypeError(
                    f"{typ} types must be parameterized with the type of the contained value -- for example, `{typ}[int]`"
                )
            if len(args) > 1:
                raise TypeError(f"{typ} should be parameterized with only one type")
            if obj is None:
                return cast(List, None)
            if not isinstance(obj, (list, tuple)):  # pyright: ignore[reportUnnecessaryIsInstance]
                raise TypeError(f"Expected a list, Object `{obj}` is not a list.")

            inner_typ = args[0]
            return [self._json_converter.structure(x, inner_typ) for x in obj]

        def _is_list(typ: Type):
            origin = get_origin(typ)
            return origin in (list, List)

        self._json_converter.register_structure_hook_func(_is_list, _structure_list)

        ######
        # Date
        ######
        def _is_date(x: Type):
            return (
                isinstance(x, type)  # pyright: ignore[reportUnnecessaryIsInstance]
                and issubclass(x, date)
                and not issubclass(x, datetime)  # pyright: ignore[reportUnnecessaryIsInstance]
            )

        self._json_converter.register_unstructure_hook_func(
            _is_date,
            lambda x: x.isoformat(),
        )

        def _structure_date(obj: Any, typ: Type):
            if obj is None:
                return None
            if isinstance(obj, datetime):
                return obj.date()
            if isinstance(obj, date):
                return obj
            if not isinstance(obj, str):
                raise TypeError(
                    f"Date values must be serialized as ISO strings. Instead, received value '{obj}' of type `{type(obj).__name__}`"
                )
            return isodate.parse_date(obj)

        self._json_converter.register_structure_hook_func(
            _is_date,
            _structure_date,
        )

        ##########
        # Datetime
        ##########

        self._json_converter.register_unstructure_hook(datetime, lambda x: x.isoformat())

        def _structure_datetime(obj: Any, typ: Type):
            if obj is None:
                return None
            if isinstance(obj, datetime):
                return obj
            if isinstance(obj, date):
                # Upgrade to a datetime
                return datetime.combine(obj, time())
            if not isinstance(obj, str):
                raise TypeError(
                    f"Datetime values must be serialized as ISO strings. Instead, received value '{obj}' of type `{type(obj).__name__}`"
                )
            return dateutil.parser.parse(obj)

        self._json_converter.register_structure_hook(datetime, _structure_datetime)

        ######
        # Time
        ######

        self._json_converter.register_unstructure_hook(time, lambda x: x.isoformat())

        def _structure_time(obj: Any, typ: Type):
            if obj is None:
                return None
            if isinstance(obj, time):
                return obj
            if not isinstance(obj, str):
                raise TypeError(
                    f"Time values must be serialized as ISO strings. Instead, received value '{obj}' of type `{type(obj).__name__}`"
                )
            return isodate.parse_time(obj)

        self._json_converter.register_structure_hook(time, _structure_time)

        ########
        # Binary
        ########

        self._json_converter.register_unstructure_hook(bytes, lambda x: base64.b64encode(x).decode("utf8"))

        def _structure_bytes(obj: Any, typ: Type):
            if obj is None:
                return None
            if isinstance(obj, str):
                return base64.b64decode(obj)
            if isinstance(obj, bytes):
                return obj
            raise TypeError(
                f"Byte values must be bytes objects or Base64-encoded strings. Instead, received value '{obj}' of type `{type(obj).__name__}`"
            )

        self._json_converter.register_structure_hook(bytes, _structure_bytes)

        self._json_converter.register_unstructure_hook(timedelta, isodate.duration_isoformat)

        ###########
        # Timedelta
        ###########

        def _structure_timedelta(obj: Any, typ: Type):
            if obj is None:
                return None
            if isinstance(obj, timedelta):
                return obj
            if not isinstance(obj, str):
                raise TypeError(
                    f"Timedelta values should be serialized as strings. Instead, received value '{obj}' of type `{type(obj).__name__}`"
                )
            return isodate.parse_duration(obj)

        self._json_converter.register_structure_hook(timedelta, _structure_timedelta)

        ###########
        # uuid.UUID
        ###########

        def _structure_uuid(obj: Any, typ: Type):
            if obj is None:
                return None
            if isinstance(obj, uuid.UUID):
                return obj
            if not isinstance(obj, str):
                raise TypeError(
                    f"UUID values should be serialized as strings. Instead, received value '{obj}' of type `{type(obj).__name__}`"
                )
            return uuid.UUID(obj)

        self._json_converter.register_structure_hook(uuid.UUID, _structure_uuid)

        ###########
        # ipaddress.IPv4Address
        ###########

        def _structure_ipv4(obj: Any, typ: Type):
            if obj is None:
                return None
            if isinstance(obj, ipaddress.IPv4Address):
                return obj
            if isinstance(obj, (int, str)):
                return ipaddress.IPv4Address(obj)
            raise TypeError(f"IPv4Address values should be serialized as strings or integers. Received {obj}")

        self._json_converter.register_structure_hook(ipaddress.IPv4Address, _structure_ipv4)

        ###########
        # ipaddress.IPv6Address
        ###########

        def _structure_ipv6(obj: Any, typ: Type):
            if obj is None:
                return None
            if isinstance(obj, ipaddress.IPv6Address):
                return obj
            if isinstance(obj, (int, str)):
                return ipaddress.IPv6Address(obj)
            raise TypeError(f"IPv6Address values should be serialized as strings or integers. Received {obj}")

        self._json_converter.register_structure_hook(ipaddress.IPv6Address, _structure_ipv6)

        ####################
        # Int/float/str/bool
        ####################

        def _structure_basic(obj: Any, typ: Type):
            if obj is None:
                # Always allow None, even if the field is non-optional
                return None
            if issubclass(typ, bool):
                # For booleans, we are more strict than just doing a simple cast, since
                # bool("random string") or bool(100) should raise an exception, not be True
                if obj in (1, True):
                    return True
                if obj in (0, False):
                    return False
                raise TypeError(f"Cannot convert '{obj}' to a Boolean. Valid values are 1, True, 0, or False.")
            if issubclass(typ, (int, float)):
                if not isinstance(obj, str) and typ(obj) != obj and not math.isnan(obj):
                    raise TypeError(f"Cannot cast '{obj}' of type {type(obj)} to a {typ} without losing precision")
            return typ(obj)  # pyright: ignore[reportCallIssue]

        self._json_converter.register_structure_hook(int, _structure_basic)
        self._json_converter.register_structure_hook(float, _structure_basic)
        self._json_converter.register_structure_hook(str, _structure_basic)
        self._json_converter.register_structure_hook(bool, _structure_basic)

    def unstructure_primitive_to_json(self, val: TPrimitive) -> TJSON:
        return self._json_converter.unstructure(val)

    def structure_json_to_primitive(self, val: Union[TJSON, TPrimitive], typ: Type[TPrimitive]) -> TPrimitive:
        return self._json_converter.structure(val, typ)


######
# Options
######


class FeatureEncodingOptions(pydantic.BaseModel, frozen=True):
    encode_structs_as_objects: bool = False
    """
    If 'True', a struct type will be encoded as a json object.
    If 'False', a struct type will be encoded as an array where the n-th element
    corresponds to the n-th field of the struct.
    """


_default_feature_json_converter = FeatureJsonConverter(options=FeatureEncodingOptions())
structs_as_objects_feature_json_converter = FeatureJsonConverter(
    options=FeatureEncodingOptions(encode_structs_as_objects=True)
)
