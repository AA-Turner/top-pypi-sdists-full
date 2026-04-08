from __future__ import annotations

from types import FunctionType

import dataclasses as _dataclasses
from datetime import date, datetime, time, timedelta
from typing import (
    Any,
    List,
    Type,
)

import pyarrow as pa
from typing_extensions import get_args, get_origin

from chalk.features._encoding.pyarrow import rich_to_pyarrow
from chalk.features.feature_wrapper import UnresolvedFeature, FeatureWrapper
from chalk.utils.collections import unwrap_annotated_if_needed, unwrap_optional_and_annotated_if_needed

from ._base import FeatureConverter
from ._bool_converter import BoolFeatureConverter
from ._bytes_converter import BytesFeatureConverter, LargeBinaryFeatureConverter
from ._dataclass_converter import DataclassFeatureConverter
from ._date_converter import Date32FeatureConverter, Date64FeatureConverter
from ._datetime_converter import DatetimeFeatureConverter, _DATETIME_PA_TYPE
from ._float_converter import Float32FeatureConverter, Float64FeatureConverter
from ._time_converter import Time32sFeatureConverter, Time32msFeatureConverter, Time64usFeatureConverter, Time64nsFeatureConverter
from ._timedelta_converter import TimedeltaFeatureConverter
from ._generic_converter import GenericFeatureConverter, TDecoder, TEncoder
from ._int_converter import Int32FeatureConverter, Int64FeatureConverter
from ._list_converter import ListFeatureConverter
from ._string_converter import LargeStringFeatureConverter, StringFeatureConverter

# pyright: reportPrivateUsage=false, reportIncompatibleMethodOverride=false, reportReturnType=false, reportUnnecessaryCast=false, reportUnnecessaryComparison=false, reportImplicitStringConcatenation=false

_TIME_CONVERTER_BY_PA_TYPE: dict[pa.DataType, type] = {
    pa.time32("s"): Time32sFeatureConverter,
    pa.time32("ms"): Time32msFeatureConverter,
    pa.time64("us"): Time64usFeatureConverter,
    pa.time64("ns"): Time64nsFeatureConverter,
}


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
        if pa.types.is_boolean(pyarrow_dtype) and (rich_type is ... or rich_primitive_type is bool):
            return BoolFeatureConverter.new(default=specialized_default, is_nullable=is_nullable)
        if pa.types.is_int64(pyarrow_dtype) and (rich_type is ... or rich_primitive_type is int):
            return Int64FeatureConverter.new(default=specialized_default, is_nullable=is_nullable)
        if pa.types.is_int32(pyarrow_dtype) and (rich_type is ... or rich_primitive_type is int):
            return Int32FeatureConverter.new(default=specialized_default, is_nullable=is_nullable)
        if pa.types.is_float64(pyarrow_dtype) and (rich_type is ... or rich_primitive_type is float):
            return Float64FeatureConverter.new(default=specialized_default, is_nullable=is_nullable)
        if pa.types.is_float32(pyarrow_dtype) and (rich_type is ... or rich_primitive_type is float):
            return Float32FeatureConverter.new(default=specialized_default, is_nullable=is_nullable)
        if pa.types.is_large_string(pyarrow_dtype) and (rich_type is ... or rich_primitive_type is str):
            return LargeStringFeatureConverter.new(default=specialized_default, is_nullable=is_nullable)
        if pa.types.is_string(pyarrow_dtype) and (rich_type is ... or rich_primitive_type is str):
            return StringFeatureConverter.new(default=specialized_default, is_nullable=is_nullable)
        if pa.types.is_large_binary(pyarrow_dtype) and (rich_type is ... or rich_primitive_type is bytes):
            return LargeBinaryFeatureConverter.new(default=specialized_default, is_nullable=is_nullable)
        if pa.types.is_binary(pyarrow_dtype) and (rich_type is ... or rich_primitive_type is bytes):
            return BytesFeatureConverter.new(default=specialized_default, is_nullable=is_nullable)
        if pyarrow_dtype == _DATETIME_PA_TYPE and (rich_type is ... or rich_primitive_type is datetime):
            return DatetimeFeatureConverter.new(default=specialized_default, is_nullable=is_nullable)
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
        if (
            pa.types.is_struct(pyarrow_dtype)
            and isinstance(rich_primitive_type, type)
            and _dataclasses.is_dataclass(rich_primitive_type)
        ):
            return DataclassFeatureConverter.new(rich_primitive_type, specialized_default, is_nullable)
        if (
            (pyarrow_dtype is not None and (pa.types.is_list(pyarrow_dtype) or pa.types.is_large_list(pyarrow_dtype)))
            and rich_primitive_type is not ...
            and get_origin(rich_primitive_type) in (list, List)
        ):
            inner_args = get_args(rich_primitive_type)
            if inner_args:
                item_conv = make_feature_converter(
                    name=None,
                    is_nullable=True,
                    rich_type=inner_args[0],
                    pyarrow_dtype=pyarrow_dtype.value_type,
                )
                if not isinstance(item_conv, GenericFeatureConverter):
                    return ListFeatureConverter.new(
                        item_converter=item_conv,
                        default=specialized_default,
                        is_nullable=is_nullable,
                        list_rich_type=rich_type if rich_type is not ... else None,
                    )

    return GenericFeatureConverter(
        name="" if name is None else name,
        is_nullable=is_nullable,
        rich_type=rich_type,
        primitive_default=primitive_default,
        rich_default=rich_default,
        pyarrow_dtype=pyarrow_dtype,
        encoder=encoder,
        decoder=decoder,
    )
