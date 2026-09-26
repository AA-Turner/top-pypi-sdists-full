# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel
from .list_field import ListField
from .struct_field import StructField

__all__ = [
    "SourceField",
    "Int32",
    "Int64",
    "Float32",
    "Float64",
    "Bool",
    "String",
    "Binary",
    "Timestamp",
    "Json",
    "Struct",
    "List",
]


class Int32(BaseModel):
    type: Literal["int32"]

    metadata_key: Optional[str] = None

    name: Optional[str] = None

    required: Optional[bool] = None

    sql_name: Optional[str] = None


class Int64(BaseModel):
    type: Literal["int64"]

    metadata_key: Optional[str] = None

    name: Optional[str] = None

    required: Optional[bool] = None

    sql_name: Optional[str] = None


class Float32(BaseModel):
    type: Literal["float32"]

    metadata_key: Optional[str] = None

    name: Optional[str] = None

    required: Optional[bool] = None

    sql_name: Optional[str] = None


class Float64(BaseModel):
    type: Literal["float64"]

    metadata_key: Optional[str] = None

    name: Optional[str] = None

    required: Optional[bool] = None

    sql_name: Optional[str] = None


class Bool(BaseModel):
    type: Literal["bool"]

    metadata_key: Optional[str] = None

    name: Optional[str] = None

    required: Optional[bool] = None

    sql_name: Optional[str] = None


class String(BaseModel):
    type: Literal["string"]

    metadata_key: Optional[str] = None

    name: Optional[str] = None

    required: Optional[bool] = None

    sql_name: Optional[str] = None


class Binary(BaseModel):
    type: Literal["binary"]

    metadata_key: Optional[str] = None

    name: Optional[str] = None

    required: Optional[bool] = None

    sql_name: Optional[str] = None


class Timestamp(BaseModel):
    type: Literal["timestamp"]

    metadata_key: Optional[str] = None

    name: Optional[str] = None

    required: Optional[bool] = None

    sql_name: Optional[str] = None

    unit: Optional[Literal["second", "millisecond", "microsecond", "nanosecond"]] = None


class Json(BaseModel):
    type: Literal["json"]

    metadata_key: Optional[str] = None

    name: Optional[str] = None

    required: Optional[bool] = None

    sql_name: Optional[str] = None


class Struct(StructField):
    type: Literal["struct"]

    metadata_key: Optional[str] = None

    name: Optional[str] = None  # type: ignore

    required: Optional[bool] = None

    sql_name: Optional[str] = None


class List(ListField):
    type: Literal["list"]

    metadata_key: Optional[str] = None

    name: Optional[str] = None

    required: Optional[bool] = None

    sql_name: Optional[str] = None


SourceField: TypeAlias = Annotated[
    Union[Int32, Int64, Float32, Float64, Bool, String, Binary, Timestamp, Json, Struct, List],
    PropertyInfo(discriminator="type"),
]
