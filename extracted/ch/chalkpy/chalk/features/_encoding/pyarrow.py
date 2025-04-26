from __future__ import annotations

import collections.abc
import dataclasses
import decimal
import enum
import ipaddress
import typing
import uuid
from datetime import date, datetime, time, timedelta
from typing import TYPE_CHECKING, Any, Dict, FrozenSet, List, Mapping, Set, Tuple, Type, cast

import attrs
import pyarrow as pa
from typing_extensions import Annotated, TypeGuard, get_args, get_origin, is_typeddict

from chalk.features._encoding.http import HttpResponse, get_http_response_as_pyarrow
from chalk.features._encoding.primitive import ChalkStructType, TPrimitive
from chalk.features.feature_set import Features
from chalk.utils.cached_type_hints import cached_get_type_hints
from chalk.utils.collections import is_namedtuple, is_optional, unwrap_optional_and_annotated_if_needed
from chalk.utils.enum import get_enum_value_type
from chalk.utils.json import JSON, is_pyarrow_json_type
from chalk.utils.missing_dependency import missing_dependency_exception
from chalk.utils.pl_helpers import is_new_polars
from chalk.utils.pydanticutil.pydantic_compat import is_pydantic_basemodel

if TYPE_CHECKING:
    import polars as pl

    from chalk.features.dataframe import DataFrame

try:
    import numpy as np
except ImportError:
    np = None

__all__ = ["pyarrow_to_primitive", "pyarrow_to_polars", "rich_to_pyarrow"]


def _is_features_cls(typ: Any) -> TypeGuard[type[Features]]:
    return getattr(typ, "__chalk_feature_set__", False)


def _is_chalk_dataframe(typ: Any) -> TypeGuard[type[DataFrame]]:
    from chalk.features.dataframe import DataFrame

    unwrapped = unwrap_optional_and_annotated_if_needed(typ)
    return isinstance(unwrapped, type) and issubclass(unwrapped, DataFrame)


def _is_chalk_http_response(typ: Any) -> TypeGuard[type[HttpResponse]]:
    from chalk.features._encoding.http import HttpResponse

    return isinstance(typ, type) and issubclass(typ, HttpResponse)


def rich_to_pyarrow(
    python_type: Type, name: str, in_struct: bool = False, respect_nullability: bool = False
) -> pa.DataType:
    """
    Recursively convert a python type to a PyArrow dtype.
    :param python_type:
    :param name:
    :param in_struct: Whether this function is being called recursively for a member of a struct type.
                      Certain datatypes need to be handled differently if nested inside a struct.
    :param respect_nullability: Whether this function should update pa.field() with correct nullability.
    """
    # Polars seems to allow optional for any dtype, so we ignore it when computing dtypes
    python_type = unwrap_optional_and_annotated_if_needed(python_type)
    origin = get_origin(python_type)
    if origin is not None:
        # Handling namedtuples above as structs before tuples, to ensure a namedtuple is not treated like
        # a list
        args = get_args(python_type)
        if origin in (Annotated, getattr(typing, "Annotated", Annotated)):
            if len(args) < 1:
                raise TypeError(
                    "Annotated types must contain the underlying type as the first argument -- e.g. Annotated[int, 'annotation']."
                )
            return rich_to_pyarrow(args[0], name, in_struct=in_struct, respect_nullability=respect_nullability)
        if origin in (list, List, set, Set, frozenset, FrozenSet):
            typ_name = origin.__name__
            if len(args) == 0:
                raise TypeError(
                    f"{typ_name} features must be annotated with the type of the element -- e.g. {typ_name}[int]."
                )
            if len(args) > 1:
                raise TypeError(
                    f"{typ_name} annotations should only take one argument -- e.g. {typ_name}[int]. Instead, got {typ_name}[{', '.join(args)}]."
                )
            arg = cast("tuple[Any, ...]", args)[0]
            return pa.large_list(
                rich_to_pyarrow(arg, name=f"{name}[]", in_struct=in_struct, respect_nullability=respect_nullability)
            )
        if origin in (tuple, Tuple):
            if len(args) == 0:
                raise TypeError(
                    "Tuple features must be annotated with the type of the tuple element -- e.g. `Tuple[int, ...]`."
                )
            if len(args) == 2 and args[1] is ...:
                # Treat a variable-sized, homogenous tuple like a list
                arg = args[0]
                return pa.large_list(
                    rich_to_pyarrow(arg, name=f"{name}[]", in_struct=in_struct, respect_nullability=respect_nullability)
                )
            raise TypeError(
                (
                    "Tuple features must have a fixed type and be variable-length tuples (e.g. `Tuple[int, ...]`). "
                    "If you would like a fixed-length of potentially different types, used a NamedTuple."
                )
            )

        if origin in (dict, Dict, Mapping, collections.abc.Mapping):
            # pydantic changes typing.Mapping into collections.abc.Mapping
            if len(args) != 2:
                raise TypeError(
                    "Dict features must be annotated with the type of the key and value -- e.g. `Dict[str, int]`."
                )

            key_type, value_type = args
            if is_optional(key_type):
                raise TypeError(f"Dict keys cannot be optional, found: `{key_type}`")
            if not isinstance(key_type, type):
                raise TypeError(f"Dict keys must be annotated with a `type`, found `{key_type}`")

            try:
                pa_value_type = rich_to_pyarrow(value_type, "value", respect_nullability=respect_nullability)
            except TypeError as e:
                raise TypeError(f"Failed to determine type of dict value from the annotation `{value_type}`") from e
            else:
                value_field = pa.field(name="value", type=pa_value_type, nullable=is_optional(value_type))

                return pa.map_(
                    key_type=rich_to_pyarrow(key_type, "key", respect_nullability=respect_nullability),
                    item_type=value_field,
                )

        if _is_chalk_http_response(origin):
            return get_http_response_as_pyarrow(python_type)

        raise TypeError(f"Unsupported varardic type annotation: {origin}")
    else:
        if python_type in (list, List, set, Set, frozenset, FrozenSet):
            typ_name = python_type.__name__
            raise TypeError(
                (
                    f"Unable to determine the PyArrow type for field '{name}' with type `{typ_name}`. "
                    f"{typ_name} features must be parameterized by their element type, e.g. {typ_name}[str]. "
                )
            )
        elif python_type in (tuple, Tuple, dict, Dict, Mapping, collections.abc.Mapping):
            typ_name = python_type.__name__
            raise TypeError(
                (
                    f"Unable to determine the PyArrow type for field '{name}' with type `{typ_name}`. "
                    f"{typ_name} features must be parameterized by their element type, e.g. {typ_name}[str, int]. "
                )
            )

    from chalk import Windowed

    if isinstance(python_type, Windowed):
        python_type = python_type.kind
    if not isinstance(python_type, type):  # pyright: ignore[reportUnnecessaryIsInstance]
        raise TypeError(f"Type annotations must be a type. Instead, got {python_type}.")
    if issubclass(python_type, enum.Enum):
        # For enums, require all members to have the same type
        return rich_to_pyarrow(
            get_enum_value_type(python_type), name, in_struct=in_struct, respect_nullability=respect_nullability
        )
    # First, handle the recursive types -- list, tuple, typeddict, namedtuple, dataclass, pydantic model
    if _is_features_cls(python_type):
        annotations = cached_get_type_hints(python_type)
        fields: List[pa.Field] = []
        for field_name, type_annotation in annotations.items():
            type_annotation_unwrapped = unwrap_optional_and_annotated_if_needed(type_annotation)
            if _is_features_cls(type_annotation_unwrapped) or _is_chalk_dataframe(type_annotation_unwrapped):
                continue
            features_cls = unwrap_optional_and_annotated_if_needed(python_type)
            feature_wrapper = getattr(features_cls, field_name)
            underlying_dtype = feature_wrapper._chalk_get_underlying().converter.pyarrow_dtype
            # For a @features class, struct field names should include the namespace (i.e. be the root FQN)
            fields.append(pa.field(f"{python_type.namespace}.{field_name}", underlying_dtype))

        return pa.struct(fields)
    elif (
        dataclasses.is_dataclass(python_type)
        or is_namedtuple(python_type)
        or is_typeddict(python_type)
        or attrs.has(python_type)
        or is_pydantic_basemodel(python_type)
    ):
        annotations = cached_get_type_hints(python_type)
        fields: List[pa.Field] = []
        for field_name, type_annotation in annotations.items():
            if field_name.startswith("__"):
                # Skip all dunders, like __slots__
                continue
            underlying_dtype = rich_to_pyarrow(
                type_annotation, name=f"{name}.{field_name}", in_struct=True, respect_nullability=respect_nullability
            )
            fields.append(
                pa.field(
                    field_name,
                    underlying_dtype,
                    not respect_nullability or type(None) in get_args(type_annotation),
                )
            )
        return pa.struct(fields)
    if _is_chalk_dataframe(python_type):
        if python_type.__pydantic_model__ is None:
            # `columns` is set to never contain has-ones or has-many's, so we don't need to worry about
            # infinite recursion when calling `Feature.converter.pyarrow_dtype`
            return pa.large_list(
                pa.struct([pa.field(col.root_fqn, col.converter.pyarrow_dtype) for col in python_type.columns])
            )
        else:
            return pa.large_list(
                rich_to_pyarrow(
                    python_type=python_type.__pydantic_model__, name="item", respect_nullability=respect_nullability
                )
            )
    if issubclass(python_type, type(None)):
        return pa.null()
    if issubclass(python_type, str):
        return pa.large_utf8()
    if issubclass(python_type, bool):
        return pa.bool_()
    if np and issubclass(python_type, np.bool_):
        return pa.bool_()
    if issubclass(python_type, int):
        return pa.int64()
    if issubclass(python_type, float):
        return pa.float64()
    if issubclass(python_type, datetime):
        return pa.timestamp("us", "UTC")
    if issubclass(python_type, date):
        if in_struct:
            return pa.date32()
        return pa.date64()
    if issubclass(python_type, time):
        return pa.time64("us")
    if issubclass(python_type, timedelta):
        return pa.duration("us")
    if issubclass(python_type, bytes):
        return pa.large_binary()
    if issubclass(python_type, decimal.Decimal):
        # Using a string for decimals, since polars
        # does not support decimal types
        return pa.large_utf8()
    if issubclass(python_type, uuid.UUID):
        return pa.large_utf8()
    if issubclass(python_type, ipaddress.IPv4Address):
        return pa.uint32()
    if issubclass(python_type, ipaddress.IPv6Address):
        return pa.large_utf8()

    raise TypeError(
        (
            f"Unable to determine the PyArrow type for field '{name}' with type `{python_type}`. "
            "Please set the `dtype` attribute when defining the feature."
        )
    )


def pyarrow_to_primitive(pyarrow_typ: pa.DataType, name: str) -> Type[TPrimitive]:
    if pa.types.is_null(pyarrow_typ):
        return type(None)
    elif pa.types.is_boolean(pyarrow_typ):
        return bool
    elif pa.types.is_unsigned_integer(pyarrow_typ) or pa.types.is_signed_integer(pyarrow_typ):
        return int
    elif pa.types.is_floating(pyarrow_typ):
        return float
    elif pa.types.is_time(pyarrow_typ):
        return time
    elif pa.types.is_timestamp(pyarrow_typ):
        return datetime
    elif pa.types.is_date(pyarrow_typ):
        return date
    elif pa.types.is_duration(pyarrow_typ):
        return timedelta
    elif (
        pa.types.is_binary(pyarrow_typ)
        or pa.types.is_fixed_size_binary(pyarrow_typ)
        or pa.types.is_large_binary(pyarrow_typ)
    ):
        return bytes
    elif pa.types.is_string(pyarrow_typ) or pa.types.is_large_string(pyarrow_typ):
        return str
    elif (
        pa.types.is_list(pyarrow_typ) or pa.types.is_large_list(pyarrow_typ) or pa.types.is_fixed_size_list(pyarrow_typ)
    ):
        assert isinstance(pyarrow_typ, (pa.ListType, pa.LargeListType, pa.FixedSizeListType))
        underlying = pyarrow_typ.value_type
        return List[pyarrow_to_primitive(underlying, name=f"{name}[]")]
    elif pa.types.is_struct(pyarrow_typ):
        assert isinstance(pyarrow_typ, pa.StructType)

        annotations: Dict[str, Type[TPrimitive]] = {}
        schema = pa.schema(pyarrow_typ)
        for sub_name, sub_typ in zip(schema.names, schema.types):
            field_type = pyarrow_to_primitive(sub_typ, name=f"{name}.{sub_name}")
            # TODO: CHA-2850
            # if pyarrow_typ.field(sub_name).nullable:
            #     field_type = typing.Optional[field_type]
            annotations[sub_name] = field_type
        struct_type = ChalkStructType(f"__chalk_struct__{name}", (object,), annotations)
        return cast("type[ChalkStructType]", struct_type)
    elif pa.types.is_map(pyarrow_typ):
        assert isinstance(pyarrow_typ, pa.MapType)
        value_typ = pyarrow_to_primitive(pyarrow_typ.item_type, name=f"{name}::value")
        if pyarrow_typ.item_field.nullable:
            value_typ = typing.Optional[value_typ]
        return Dict[
            pyarrow_to_primitive(pyarrow_typ.key_type, name=f"{name}::key"),
            value_typ,
        ]
    elif is_pyarrow_json_type(pyarrow_typ):
        return cast(Type[TPrimitive], JSON)
    raise TypeError(f"Unsupported PyArrow type '{pyarrow_typ}' for field '{name}'.")


def is_map_in_dtype_tree(dtype: pa.DataType) -> bool:
    if isinstance(dtype, pa.MapType):
        return True
    if isinstance(dtype, pa.StructType):
        return any(is_map_in_dtype_tree(x.type) for x in dtype)
    if isinstance(dtype, (pa.ListType, pa.LargeListType, pa.FixedSizeListType)):
        return is_map_in_dtype_tree(dtype.value_type)
    return False


def pyarrow_to_polars(
    pa_type: pa.DataType, name: str | None = None, use_fixed_size_list: bool = False
) -> pl.PolarsDataType:
    """Convert a PyArrow data type into a Polars DataType

    Args:
        pa_type: The PyArrow data type
        name: A name, which is printed in error messages
    """
    try:
        import polars as pl
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")
    if isinstance(pa_type, pa.ExtensionType):
        pa_type = pa_type.storage_type
    if pa.types.is_null(pa_type):
        return pl.Null()
    if is_pyarrow_json_type(pa_type):
        return pl.Utf8()
    if pa.types.is_boolean(pa_type):
        return pl.Boolean()
    if pa.types.is_int8(pa_type):
        return pl.Int8()
    if pa.types.is_int16(pa_type):
        return pl.Int16()
    if pa.types.is_int32(pa_type):
        return pl.Int32()
    if pa.types.is_int64(pa_type):
        return pl.Int64()
    if pa.types.is_uint8(pa_type):
        return pl.UInt8()
    if pa.types.is_uint16(pa_type):
        return pl.UInt16()
    if pa.types.is_uint32(pa_type):
        return pl.UInt32()
    if pa.types.is_uint64(pa_type):
        return pl.UInt64()
    if pa.types.is_float16(pa_type):
        return pl.Float32()
    if pa.types.is_float32(pa_type):
        return pl.Float32()
    if pa.types.is_float64(pa_type):
        return pl.Float64()
    if pa.types.is_time(pa_type):
        return pl.Time()
    if pa.types.is_timestamp(pa_type):
        assert isinstance(pa_type, pa.TimestampType)
        assert pa_type.unit in ("ms", "us", "ns")
        return pl.Datetime(pa_type.unit, pa_type.tz)
    if pa.types.is_date(pa_type):
        return pl.Date()
    if pa.types.is_duration(pa_type):
        assert isinstance(pa_type, pa.DurationType)
        assert pa_type.unit in ("ms", "us", "ns")
        return pl.Duration(pa_type.unit)
    if pa.types.is_binary(pa_type) or pa.types.is_fixed_size_binary(pa_type) or pa.types.is_large_binary(pa_type):
        return pl.Binary()
    if pa.types.is_string(pa_type) or pa.types.is_large_string(pa_type):
        return pl.Utf8()
    if pa.types.is_list(pa_type) or pa.types.is_large_list(pa_type):
        assert isinstance(pa_type, (pa.ListType, pa.LargeListType, pa.FixedSizeListType))
        underlying = pa_type.value_type
        return pl.List(pyarrow_to_polars(underlying, name=f"{name}[]"))
    if pa.types.is_fixed_size_list(pa_type):
        underlying = pa_type.value_type
        if is_new_polars and use_fixed_size_list:
            # pl.Array is only available in polars >=0.18
            return pl.Array(inner=pyarrow_to_polars(underlying, name=f"{name}[]"), width=pa_type.list_size)
        else:
            return pl.List(pyarrow_to_polars(underlying, name=f"{name}[]"))
    if pa.types.is_struct(pa_type):
        assert isinstance(pa_type, pa.StructType)
        schema = pa.schema(pa_type)
        fields = [
            pl.Field(sub_name, pyarrow_to_polars(sub_typ, name=f"{name}.{sub_name}"))
            for sub_name, sub_typ in zip(schema.names, schema.types)
        ]
        return pl.Struct(fields)
    if pa.types.is_decimal(pa_type):
        assert isinstance(pa_type, (pa.Decimal128Type, pa.Decimal256Type))
        return pl.Decimal(precision=pa_type.precision, scale=pa_type.scale)
    if pa.types.is_map(pa_type):
        assert isinstance(pa_type, pa.MapType)
        fields = [
            pl.Field("key", pyarrow_to_polars(pa_type.key_type, name=f"{name}::key")),
            pl.Field("value", pyarrow_to_polars(pa_type.item_type, name=f"{name}::value")),
        ]
        return pl.List(pl.Struct(fields))
    raise TypeError(f"Unsupported PyArrow type '{pa_type}'{name and f' for field {name}' or ''}.")
