from __future__ import annotations

import decimal
import enum
import ipaddress
import uuid as _uuid_module
from types import FunctionType

import dataclasses as _dataclasses
from datetime import date, datetime, time, timedelta
from typing import (
    Any,
    List,
    Type,
    cast,
)

import pyarrow as pa
from typing_extensions import get_args, get_origin, is_typeddict

from chalk.features._encoding.pyarrow import pyarrow_to_primitive, rich_to_pyarrow
from chalk.features.feature_wrapper import UnresolvedFeature, FeatureWrapper
from chalk.utils.attrs_utils import attrs_fields, is_attrs_class
from chalk.utils.collections import is_namedtuple, unwrap_annotated_if_needed, unwrap_optional_and_annotated_if_needed

from ._base import FeatureConverter
from ._bool_converter import BoolFeatureConverter
from ._bytes_converter import BytesFeatureConverter, LargeBinaryFeatureConverter
from ._dataclass_converter import DataclassFeatureConverter
from ._decimal_converter import DecimalFeatureConverter
from ._typed_dict_converter import TypedDictFeatureConverter
from ._date_converter import Date32FeatureConverter, Date64FeatureConverter
from ._datetime_converter import DatetimeFeatureConverter
from ._float_converter import Float16FeatureConverter, Float32FeatureConverter, Float64FeatureConverter
from ._time_converter import Time32sFeatureConverter, Time32msFeatureConverter, Time64usFeatureConverter, Time64nsFeatureConverter
from ._timedelta_converter import TimedeltaFeatureConverter
from ._generic_converter import TDecoder, TEncoder
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
from ._fixed_size_list_converter import FixedSizeListFeatureConverter
from ._list_converter import ListFeatureConverter
from ._string_converter import LargeStringFeatureConverter, StringFeatureConverter
from ._uuid_ip_converters import UUIDFeatureConverter, IPv4FeatureConverter, IPv6FeatureConverter
from ._encoder_decoder_converter import EncoderDecoderFeatureConverter
from ._json_converter import JsonFeatureConverter

# pyright: reportPrivateUsage=false, reportIncompatibleMethodOverride=false, reportReturnType=false, reportUnnecessaryCast=false, reportUnnecessaryComparison=false, reportImplicitStringConcatenation=false

_TIME_CONVERTER_BY_PA_TYPE: dict[pa.DataType, type] = {
    pa.time32("s"): Time32sFeatureConverter,
    pa.time32("ms"): Time32msFeatureConverter,
    pa.time64("us"): Time64usFeatureConverter,
    pa.time64("ns"): Time64nsFeatureConverter,
}


def make_field_converters_for_dataclass(dc_class: type) -> "dict[str, FeatureConverter]":
    """Build a {field_name: FeatureConverter} mapping for every field of a dataclass.

    Called by make_feature_converter (for the struct branch) and lazily by
    DataclassFeatureConverter.new when field_converters are not injected by the caller.
    Nested dataclass fields get a DataclassFeatureConverter.for_class instance (cached,
    default=..., is_nullable=True) so that identity checks in tests still hold.

    Passes pyarrow_dtype explicitly so field converters use the same dtype as the parent struct.
    """
    import typing as _typing_mod
    field_names = tuple(f.name for f in _dataclasses.fields(dc_class))
    hints = _typing_mod.get_type_hints(dc_class)
    result: dict[str, FeatureConverter] = {}
    for name in field_names:
        typ = hints[name]
        inner = unwrap_optional_and_annotated_if_needed(typ)
        if _dataclasses.is_dataclass(inner) and isinstance(inner, type):
            result[name] = DataclassFeatureConverter.for_class(inner)
        else:
            pa_dtype = rich_to_pyarrow(typ, name, in_struct=True)
            result[name] = make_feature_converter(name=name, is_nullable=True, rich_type=typ, pyarrow_dtype=pa_dtype)
    return result


def make_field_converters_for_typed_dict(td_class: type) -> "dict[str, FeatureConverter]":
    """Build a {field_name: FeatureConverter} mapping for every field of a TypedDict.

    Passes pyarrow_dtype explicitly so field converters use the same dtype as the parent struct.
    """
    import typing as _typing_mod
    hints = _typing_mod.get_type_hints(td_class)
    result: dict[str, FeatureConverter] = {}
    for name, typ in hints.items():
        inner = unwrap_optional_and_annotated_if_needed(typ)
        if isinstance(inner, type) and is_typeddict(inner):
            result[name] = TypedDictFeatureConverter.for_class(inner)
        else:
            pa_dtype = pa.field(name, rich_to_pyarrow(typ, name, in_struct=True)).type
            result[name] = make_feature_converter(name=name, is_nullable=True, rich_type=typ, pyarrow_dtype=pa_dtype)
    return result


def make_field_converters_for_pydantic(model_class: type) -> "dict[str, FeatureConverter]":
    """Build a {field_name: FeatureConverter} mapping for every field of a Pydantic model.

    Passes pyarrow_dtype explicitly so field converters use the same dtype as the parent struct.
    """
    import typing as _typing_mod
    from ._pydantic_converter import PydanticFeatureConverter, _is_pydantic_model
    fields = getattr(model_class, "model_fields", None) or getattr(model_class, "__fields__", {})
    field_names = tuple(fields.keys())
    hints = _typing_mod.get_type_hints(model_class)
    result: dict[str, FeatureConverter] = {}
    for name in field_names:
        typ = hints[name]
        inner = unwrap_optional_and_annotated_if_needed(typ)
        if _is_pydantic_model(inner):
            result[name] = PydanticFeatureConverter.for_class(inner)
        else:
            pa_dtype = rich_to_pyarrow(typ, name, in_struct=True)
            result[name] = make_feature_converter(name=name, is_nullable=True, rich_type=typ, pyarrow_dtype=pa_dtype)
    return result


def make_field_converters_for_attrs(cls: type) -> "dict[str, FeatureConverter]":
    """Build a {field_name: FeatureConverter} mapping for every field of an attrs class.

    Passes pyarrow_dtype explicitly so field converters use the same dtype as the parent struct.
    """
    import typing as _typing_mod
    from ._attrs_converter import AttrsFeatureConverter
    field_names = tuple(f.name for f in attrs_fields(cls))
    hints = _typing_mod.get_type_hints(cls)
    result: dict[str, FeatureConverter] = {}
    for name in field_names:
        typ = hints[name]
        inner = unwrap_optional_and_annotated_if_needed(typ)
        if is_attrs_class(inner):
            result[name] = AttrsFeatureConverter.new(inner, ..., is_nullable=True)
        else:
            pa_dtype = rich_to_pyarrow(typ, name, in_struct=True)
            result[name] = make_feature_converter(name=name, is_nullable=True, rich_type=typ, pyarrow_dtype=pa_dtype)
    return result


def make_field_converters_for_namedtuple(nt_class: type) -> "dict[str, FeatureConverter]":
    """Build a {field_name: FeatureConverter} mapping for every field of a NamedTuple.

    Passes pyarrow_dtype explicitly so field converters use the same dtype as the parent struct.
    """
    import typing as _typing_mod
    from ._named_tuple_converter import NamedTupleFeatureConverter
    field_names: tuple[str, ...] = nt_class._fields
    hints = _typing_mod.get_type_hints(nt_class)
    result: dict[str, FeatureConverter] = {}
    for name in field_names:
        typ = hints[name]
        inner = unwrap_optional_and_annotated_if_needed(typ)
        if is_namedtuple(inner):
            result[name] = NamedTupleFeatureConverter.new(inner, ..., is_nullable=True)
        else:
            pa_dtype = rich_to_pyarrow(typ, name, in_struct=True)
            result[name] = make_feature_converter(name=name, is_nullable=True, rich_type=typ, pyarrow_dtype=pa_dtype)
    return result


def make_primitive_converter(
    name: str,
    is_nullable: bool,
    pyarrow_dtype: pa.DataType,
    primitive_default: Any = ...,
) -> FeatureConverter[Any, Any]:
    """Create a primitive-shaped feature converter, using a specialized implementation when possible."""
    return make_feature_converter(
        name=name,
        is_nullable=is_nullable,
        rich_type=...,
        primitive_default=primitive_default,
        pyarrow_dtype=pyarrow_dtype,
    )


def make_feature_converter(
    name: str | None,
    is_nullable: bool,
    rich_type: Type[Any] | ellipsis = ...,
    primitive_default: Any = ...,
    rich_default: Any = ...,
    pyarrow_dtype: pa.DataType | None = None,
    encoder: TEncoder[Any, Any] | None = None,
    decoder: TDecoder[Any, Any] | None = None,
) -> FeatureConverter[Any, Any]:
    """Create a feature converter, using a specialized implementation when possible."""
    rich_type = unwrap_annotated_if_needed(rich_type)

    if pyarrow_dtype is None:
        if rich_type is ...:
            raise ValueError("Either the `rich_type` or `pyarrow_dtype` must be provided")
        pyarrow_dtype = rich_to_pyarrow(rich_type, "" if name is None else name)
    assert pyarrow_dtype is not None, "pyarrow_dtype must be set by this point"

    specialized_default = primitive_default
    if rich_type is ...:
        if rich_default != ...:
            raise ValueError(
                "The `rich_default` cannot be used without the `rich_type`. Perhaps specify the `primitive_default` instead?"
            )
        if is_nullable and primitive_default is ...:
            specialized_default = None
    else:
        if primitive_default != ...:
            raise ValueError(
                "The `primitive_default` cannot be used when specifying the `rich_type`. Instead, specify the `rich_default`."
            )
        if is_nullable and rich_default is ...:
            rich_default = None
        if isinstance(rich_default, (UnresolvedFeature, FeatureWrapper, FunctionType)):
            rich_default = ...
        specialized_default = rich_default

    rich_primitive_type = ... if rich_type is ... else unwrap_optional_and_annotated_if_needed(rich_type)
    if encoder is None and decoder is None:
        # --- Scalar: bool ---
        if pa.types.is_boolean(pyarrow_dtype) and (rich_type is ... or rich_primitive_type is bool):
            return BoolFeatureConverter.new(default=specialized_default, is_nullable=is_nullable)

        # --- Scalar: integer ---
        if pa.types.is_int8(pyarrow_dtype) and (rich_type is ... or rich_primitive_type is int):
            return Int8FeatureConverter.new(default=specialized_default, is_nullable=is_nullable)
        if pa.types.is_int16(pyarrow_dtype) and (rich_type is ... or rich_primitive_type is int):
            return Int16FeatureConverter.new(default=specialized_default, is_nullable=is_nullable)
        if pa.types.is_int32(pyarrow_dtype) and (rich_type is ... or rich_primitive_type is int):
            return Int32FeatureConverter.new(default=specialized_default, is_nullable=is_nullable)
        if pa.types.is_int64(pyarrow_dtype) and (rich_type is ... or rich_primitive_type is int):
            return Int64FeatureConverter.new(default=specialized_default, is_nullable=is_nullable)
        if pa.types.is_uint8(pyarrow_dtype) and (rich_type is ... or rich_primitive_type is int):
            return UInt8FeatureConverter.new(default=specialized_default, is_nullable=is_nullable)
        if pa.types.is_uint16(pyarrow_dtype) and (rich_type is ... or rich_primitive_type is int):
            return UInt16FeatureConverter.new(default=specialized_default, is_nullable=is_nullable)
        if pa.types.is_uint32(pyarrow_dtype):
            # uint32 is used for both plain int and IPv4Address
            if rich_type is ... or rich_primitive_type is int:
                return UInt32FeatureConverter.new(default=specialized_default, is_nullable=is_nullable)
            if isinstance(rich_primitive_type, type) and issubclass(rich_primitive_type, ipaddress.IPv4Address):
                return IPv4FeatureConverter.new(default=specialized_default, is_nullable=is_nullable)
        if pa.types.is_uint64(pyarrow_dtype) and (rich_type is ... or rich_primitive_type is int):
            return UInt64FeatureConverter.new(default=specialized_default, is_nullable=is_nullable)

        # --- Scalar: float ---
        if pa.types.is_float16(pyarrow_dtype) and (rich_type is ... or rich_primitive_type is float):
            return Float16FeatureConverter.new(default=specialized_default, is_nullable=is_nullable)
        if pa.types.is_float32(pyarrow_dtype) and (rich_type is ... or rich_primitive_type is float):
            return Float32FeatureConverter.new(default=specialized_default, is_nullable=is_nullable)
        if pa.types.is_float64(pyarrow_dtype) and (rich_type is ... or rich_primitive_type is float):
            return Float64FeatureConverter.new(default=specialized_default, is_nullable=is_nullable)

        # --- Scalar: string (large_utf8 is also used for Decimal, UUID, IPv6) ---
        if pa.types.is_large_string(pyarrow_dtype):
            if rich_type is ... or rich_primitive_type is str:
                return LargeStringFeatureConverter.new(default=specialized_default, is_nullable=is_nullable)
            if isinstance(rich_primitive_type, type):
                if issubclass(rich_primitive_type, decimal.Decimal):
                    return DecimalFeatureConverter.new(default=specialized_default, is_nullable=is_nullable)
                if issubclass(rich_primitive_type, _uuid_module.UUID):
                    return UUIDFeatureConverter.new(default=specialized_default, is_nullable=is_nullable)
                if issubclass(rich_primitive_type, ipaddress.IPv6Address):
                    return IPv6FeatureConverter.new(default=specialized_default, is_nullable=is_nullable)
        if pa.types.is_string(pyarrow_dtype) and (rich_type is ... or rich_primitive_type is str):
            return StringFeatureConverter.new(default=specialized_default, is_nullable=is_nullable)

        # --- Scalar: binary ---
        if pa.types.is_large_binary(pyarrow_dtype) and (rich_type is ... or rich_primitive_type is bytes):
            return LargeBinaryFeatureConverter.new(default=specialized_default, is_nullable=is_nullable)
        if pa.types.is_binary(pyarrow_dtype) and (rich_type is ... or rich_primitive_type is bytes):
            return BytesFeatureConverter.new(default=specialized_default, is_nullable=is_nullable)

        # --- Scalar: temporal ---
        if pa.types.is_timestamp(pyarrow_dtype) and (rich_type is ... or rich_primitive_type is datetime):
            assert isinstance(pyarrow_dtype, pa.TimestampType), f"Expected pa.TimestampType, got {type(pyarrow_dtype)}"
            return DatetimeFeatureConverter.new(default=specialized_default, is_nullable=is_nullable, pa_type=pyarrow_dtype)
        if pa.types.is_date32(pyarrow_dtype) and (rich_type is ... or rich_primitive_type is date):
            return Date32FeatureConverter.new(default=specialized_default, is_nullable=is_nullable)
        if pa.types.is_date64(pyarrow_dtype) and (rich_type is ... or rich_primitive_type is date):
            return Date64FeatureConverter.new(default=specialized_default, is_nullable=is_nullable)
        if pa.types.is_time(pyarrow_dtype) and (rich_type is ... or rich_primitive_type is time):
            conv_cls = _TIME_CONVERTER_BY_PA_TYPE.get(pyarrow_dtype)
            if conv_cls is not None:
                return conv_cls.new(default=specialized_default, is_nullable=is_nullable)
        if pa.types.is_duration(pyarrow_dtype) and (rich_type is ... or rich_primitive_type is timedelta):
            return TimedeltaFeatureConverter.new(default=specialized_default, is_nullable=is_nullable)

        # --- Null ---
        if pa.types.is_null(pyarrow_dtype):
            from ._null_converter import NullFeatureConverter
            return NullFeatureConverter.new()

        # --- Enum ---
        if isinstance(rich_primitive_type, type) and issubclass(rich_primitive_type, enum.Enum):
            from ._enum_converter import EnumFeatureConverter
            return EnumFeatureConverter.new(rich_primitive_type, specialized_default, is_nullable)

        # --- Struct (dataclass / TypedDict / NamedTuple / attrs / pydantic / anonymous) ---
        if pa.types.is_struct(pyarrow_dtype):
            # For generic aliases like HttpResponse[bytes], resolve to the origin class.
            # TypeVar parameters can't be resolved statically, so use the pyarrow dtype
            # fields to drive field converters in that case.
            _struct_class: type | None = rich_primitive_type if isinstance(rich_primitive_type, type) else None
            if _struct_class is None:
                _origin = get_origin(rich_primitive_type)
                if isinstance(_origin, type):
                    _struct_class = _origin
            if _struct_class is not None:
                if is_namedtuple(_struct_class):
                    from ._named_tuple_converter import NamedTupleFeatureConverter
                    field_converters = make_field_converters_for_namedtuple(_struct_class)
                    return NamedTupleFeatureConverter.new(_struct_class, specialized_default, is_nullable, name=name or "", field_converters=field_converters)
                if _dataclasses.is_dataclass(_struct_class):
                    if isinstance(rich_primitive_type, type):
                        field_converters = make_field_converters_for_dataclass(_struct_class)
                        return DataclassFeatureConverter.new(_struct_class, specialized_default, is_nullable, field_converters=field_converters)
                    else:
                        # Generic alias (e.g. HttpResponse[bytes]): TypeVars are erased at
                        # runtime, so drive field converters from the pyarrow struct fields
                        # and pass the concrete pa_struct_type to bypass TypeVar resolution.
                        struct_dtype = cast(pa.StructType, pyarrow_dtype)
                        field_converters = {
                            struct_dtype.field(i).name: make_feature_converter(
                                name=struct_dtype.field(i).name,
                                is_nullable=True,
                                rich_type=...,
                                pyarrow_dtype=struct_dtype.field(i).type,
                            )
                            for i in range(struct_dtype.num_fields)
                        }
                        return DataclassFeatureConverter.new(_struct_class, specialized_default, is_nullable, field_converters=field_converters, pa_struct_type=pyarrow_dtype)
                if is_typeddict(_struct_class):
                    field_converters = make_field_converters_for_typed_dict(_struct_class)
                    return TypedDictFeatureConverter.new(_struct_class, specialized_default, is_nullable, field_converters=field_converters)
                if is_attrs_class(_struct_class):
                    from ._attrs_converter import AttrsFeatureConverter
                    field_converters = make_field_converters_for_attrs(_struct_class)
                    return AttrsFeatureConverter.new(_struct_class, specialized_default, is_nullable, name=name or "", field_converters=field_converters)
                from ._pydantic_converter import PydanticFeatureConverter, _is_pydantic_model
                if _is_pydantic_model(_struct_class):
                    field_converters = make_field_converters_for_pydantic(_struct_class)
                    return PydanticFeatureConverter.new(_struct_class, specialized_default, is_nullable, name=name or "", field_converters=field_converters)
            elif rich_type is ...:
                from ._anonymous_struct_converter import AnonymousStructFeatureConverter
                struct_dtype = cast(pa.StructType, pyarrow_dtype)
                field_converters = {
                    struct_dtype.field(i).name: make_feature_converter(
                        name=struct_dtype.field(i).name,
                        is_nullable=True,
                        rich_type=...,
                        pyarrow_dtype=struct_dtype.field(i).type,
                    )
                    for i in range(struct_dtype.num_fields)
                }
                return AnonymousStructFeatureConverter.new(struct_dtype, specialized_default, is_nullable, field_converters=field_converters)

        # --- Fixed-size list ---
        if pa.types.is_fixed_size_list(pyarrow_dtype) and (rich_primitive_type is ... or get_origin(rich_primitive_type) in (list, List)):
            assert isinstance(pyarrow_dtype, pa.FixedSizeListType), f"Expected pa.FixedSizeListType, got {type(pyarrow_dtype)}"
            inner_rich_type: Any = ...
            if rich_primitive_type is not ...:
                inner_args = get_args(rich_primitive_type)
                inner_rich_type = inner_args[0] if inner_args else ...
            item_conv = make_feature_converter(
                name=None,
                is_nullable=True,
                rich_type=inner_rich_type,
                pyarrow_dtype=pyarrow_dtype.value_type,
            )
            return FixedSizeListFeatureConverter.new(
                item_converter=item_conv,
                default=specialized_default,
                is_nullable=is_nullable,
                list_size=pyarrow_dtype.list_size,
                list_rich_type=rich_type if rich_type is not ... else None,
            )

        # --- List / large list (set, frozenset, homogeneous tuple, list, anonymous) ---
        if pa.types.is_list(pyarrow_dtype) or pa.types.is_large_list(pyarrow_dtype):
            if rich_primitive_type is not ...:
                origin = get_origin(rich_primitive_type)
                if origin in (set, frozenset):
                    inner_args = get_args(rich_primitive_type)
                    if inner_args:
                        item_conv = make_feature_converter(
                            name=None,
                            is_nullable=True,
                            rich_type=inner_args[0],
                            pyarrow_dtype=pyarrow_dtype.value_type,
                        )
                        from ._set_converter import SetFeatureConverter
                        return SetFeatureConverter.new(
                            rich_type=rich_type if rich_type is not ... else rich_primitive_type,
                            default=specialized_default,
                            is_nullable=is_nullable,
                            item_converter=item_conv,
                        )
                elif (
                    origin is tuple
                    and len(get_args(rich_primitive_type)) == 2
                    and get_args(rich_primitive_type)[1] is Ellipsis
                ):
                    inner_args = get_args(rich_primitive_type)
                    item_conv = make_feature_converter(
                        name=None,
                        is_nullable=True,
                        rich_type=inner_args[0],
                        pyarrow_dtype=pyarrow_dtype.value_type,
                    )
                    from ._set_converter import SetFeatureConverter
                    return SetFeatureConverter.new(
                        rich_type=rich_type if rich_type is not ... else rich_primitive_type,
                        default=specialized_default,
                        is_nullable=is_nullable,
                        item_converter=item_conv,
                    )
                elif origin in (list, List):
                    inner_args = get_args(rich_primitive_type)
                    if inner_args:
                        item_conv = make_feature_converter(
                            name=None,
                            is_nullable=True,
                            rich_type=inner_args[0],
                            pyarrow_dtype=pyarrow_dtype.value_type,
                        )
                        return ListFeatureConverter.new(
                            item_converter=item_conv,
                            default=specialized_default,
                            is_nullable=is_nullable,
                            list_rich_type=rich_type if rich_type is not ... else None,
                            pa_list_type=pyarrow_dtype,
                        )
            else:
                # rich_type is ...: anonymous list driven entirely by pyarrow dtype
                item_conv = make_feature_converter(
                    name=None,
                    is_nullable=True,
                    rich_type=...,
                    pyarrow_dtype=pyarrow_dtype.value_type,
                )
                return ListFeatureConverter.new(
                    item_converter=item_conv,
                    default=specialized_default,
                    is_nullable=is_nullable,
                    list_rich_type=None,
                    pa_list_type=pyarrow_dtype,
                )

        # --- Map ---
        if pa.types.is_map(pyarrow_dtype) and (rich_primitive_type is ... or get_origin(rich_primitive_type) in (dict,)):
            from ._dict_converter import DictFeatureConverter
            rt = rich_type if rich_type is not ... else pyarrow_to_primitive(pyarrow_dtype, name or "")
            value_rich_type: Any = ...
            if rich_primitive_type is not ...:
                _args = get_args(rich_primitive_type)
                if len(_args) == 2:
                    value_rich_type = _args[1]
            value_conv = make_feature_converter(
                name=None,
                is_nullable=True,
                rich_type=value_rich_type,
                pyarrow_dtype=pyarrow_dtype.item_type,
            )
            return DictFeatureConverter.new(
                rt, specialized_default, is_nullable, name=name or "", value_converter=value_conv,
                pyarrow_dtype=pyarrow_dtype,
            )

        # --- Extension types (JSON and unknown) ---
        if isinstance(pyarrow_dtype, pa.ExtensionType):
            from chalk.utils.json import is_pyarrow_json_type
            if is_pyarrow_json_type(pyarrow_dtype):
                return JsonFeatureConverter.new(default=specialized_default, is_nullable=is_nullable)
            # Unknown extension type: fall back to storage type so we still get a specialized converter.
            return make_feature_converter(
                name=name,
                is_nullable=is_nullable,
                rich_type=rich_type,
                primitive_default=specialized_default,
                pyarrow_dtype=pyarrow_dtype.storage_type,
            )

        # All known dispatch branches failed. If the rich type is a custom opaque class or
        # an abstract generic (Mapping, Sequence, Collection, etc.) with a reasonable pyarrow
        # dtype, re-dispatch with rich_type=... so the pyarrow dtype drives converter selection.
        if rich_type is not ...:
            return make_feature_converter(
                name=name,
                is_nullable=is_nullable,
                rich_type=...,
                primitive_default=specialized_default,
                pyarrow_dtype=pyarrow_dtype,
            )

        parts = [f"No specialized FeatureConverter found for feature {name!r}."]
        parts.append(f"  rich_type:    {rich_type}")
        parts.append(f"  pyarrow_dtype: {pyarrow_dtype}")
        if rich_type is not ...:
            try:
                expected_pa = rich_to_pyarrow(rich_type, name or "")
                if expected_pa != pyarrow_dtype:
                    parts.append(
                        f"  Note: the natural PyArrow dtype for {rich_type} is {expected_pa!r}, "
                        f"but {pyarrow_dtype!r} was provided — these are incompatible."
                    )
            except Exception:
                pass
        parts.append(
            "  Hint: if this is a custom type, provide an encoder/decoder pair "
            "or annotate the feature with a supported type."
        )
        raise ValueError("\n".join(parts))
    assert rich_type is not ... and pyarrow_dtype is not None, "encoder/decoder path requires rich_type and pyarrow_dtype"
    assert encoder is not None, "encoder must be set when decoder is provided"
    # Compute the primitive default by encoding the rich default.
    # For nullable with no explicit default, primitive_default is None.
    if rich_default is not ... and rich_default is not None:
        base_primitive_default = encoder(rich_default)
    elif rich_default is None or (rich_default is ... and is_nullable):
        base_primitive_default = None
    else:
        base_primitive_default = ...
    base_conv = make_feature_converter(
        name=name,
        is_nullable=is_nullable,
        rich_type=...,
        primitive_default=base_primitive_default,
        pyarrow_dtype=pyarrow_dtype,
    )
    resolved_rich_default = rich_default if rich_default is not ... else (None if is_nullable else ...)
    return EncoderDecoderFeatureConverter.new(
        rich_type=cast(type, unwrap_optional_and_annotated_if_needed(rich_type)),
        pyarrow_dtype=pyarrow_dtype,
        encoder=encoder,
        decoder=decoder,
        rich_default=resolved_rich_default,
        is_nullable=is_nullable,
        base_converter=base_conv,
    )
