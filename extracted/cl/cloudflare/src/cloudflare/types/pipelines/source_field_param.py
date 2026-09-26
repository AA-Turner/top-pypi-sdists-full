# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .list_field_param import ListFieldParam
from .struct_field_param import StructFieldParam

__all__ = [
    "SourceFieldParam",
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


class Int32(TypedDict, total=False):
    type: Required[Literal["int32"]]

    metadata_key: Optional[str]

    name: str

    required: bool

    sql_name: str


class Int64(TypedDict, total=False):
    type: Required[Literal["int64"]]

    metadata_key: Optional[str]

    name: str

    required: bool

    sql_name: str


class Float32(TypedDict, total=False):
    type: Required[Literal["float32"]]

    metadata_key: Optional[str]

    name: str

    required: bool

    sql_name: str


class Float64(TypedDict, total=False):
    type: Required[Literal["float64"]]

    metadata_key: Optional[str]

    name: str

    required: bool

    sql_name: str


class Bool(TypedDict, total=False):
    type: Required[Literal["bool"]]

    metadata_key: Optional[str]

    name: str

    required: bool

    sql_name: str


class String(TypedDict, total=False):
    type: Required[Literal["string"]]

    metadata_key: Optional[str]

    name: str

    required: bool

    sql_name: str


class Binary(TypedDict, total=False):
    type: Required[Literal["binary"]]

    metadata_key: Optional[str]

    name: str

    required: bool

    sql_name: str


class Timestamp(TypedDict, total=False):
    type: Required[Literal["timestamp"]]

    metadata_key: Optional[str]

    name: str

    required: bool

    sql_name: str

    unit: Literal["second", "millisecond", "microsecond", "nanosecond"]


class Json(TypedDict, total=False):
    type: Required[Literal["json"]]

    metadata_key: Optional[str]

    name: str

    required: bool

    sql_name: str


class Struct(StructFieldParam, total=False):
    type: Required[Literal["struct"]]

    metadata_key: Optional[str]

    name: str  # type: ignore

    required: bool

    sql_name: str


class List(ListFieldParam, total=False):
    type: Required[Literal["list"]]

    metadata_key: Optional[str]

    name: str

    required: bool

    sql_name: str


SourceFieldParam: TypeAlias = Union[Int32, Int64, Float32, Float64, Bool, String, Binary, Timestamp, Json, Struct, List]
