from __future__ import annotations

import enum
import json
from typing import TYPE_CHECKING, List, Literal, Optional, Union

import pyarrow as pa
from typing_extensions import Annotated

from chalk.utils.json import is_pyarrow_json_type, pyarrow_json_type

if TYPE_CHECKING:
    from pydantic import BaseModel, Field
else:
    try:
        from pydantic.v1 import BaseModel, Field
    except ImportError:
        from pydantic import BaseModel, Field

__all__ = [
    "deserialize_dtype",
    "serialize_dtype",
]


class _DTypeCode(enum.IntEnum):
    # NULL = 1
    BOOL = 2
    INT8 = 3
    INT16 = 4
    INT32 = 5
    INT64 = 6
    UINT8 = 7
    UINT16 = 8
    UINT32 = 9
    UINT64 = 10
    FLOAT16 = 11
    FLOAT32 = 12
    FLOAT64 = 13
    TIME32 = 14  # time unit
    TIME64 = 15  # time unit
    TIMESTAMP = 16  # time unit, time zone
    DATE32 = 17
    DATE64 = 18
    DURATION = 19  # time unit
    """UNSUPPORTED -- Some database backends do not support duration columns."""

    BINARY = 20  # length
    """DEPRECATED -- use LARGE_BINARY

    BINARY does not support more than 2GB of data, which significantly limits the maximum chunk size.
    """
    STRING = 21
    """Deprecated -- use LARGE_STRING

    STRING does not support more than 2GB of data, which significantly limits the maximum chunk size.
    """
    LARGE_BINARY = 22
    LARGE_STRING = 23
    # Decimal is not yet supported by chalk
    # DECIMAL128 = 24  # precision, scale
    LIST = 25  # value type, size
    """Deprecated -- use LARGE_LIST

    LIST does not support more than 2GB of data, which significantly limits the maximum chunk size.
    """
    LARGE_LIST = 26  # value type
    STRUCT = 27  # fields
    MAP = 28  # key field, item field
    JSON = 29


_TimeUnitCode = Literal["s", "ms", "us", "ns"]


class _BaseSerializedDType(BaseModel, frozen=True, use_enum_values=True):
    type_code: _DTypeCode

    def to_pyarrow_dtype(self) -> pa.DataType:
        raise NotImplementedError


class _SingletonDType(_BaseSerializedDType, frozen=True):
    type_code: Literal[
        _DTypeCode.BOOL,
        _DTypeCode.INT8,
        _DTypeCode.INT16,
        _DTypeCode.INT32,
        _DTypeCode.INT64,
        _DTypeCode.UINT8,
        _DTypeCode.UINT16,
        _DTypeCode.UINT32,
        _DTypeCode.UINT64,
        _DTypeCode.FLOAT16,
        _DTypeCode.FLOAT32,
        _DTypeCode.FLOAT64,
        _DTypeCode.DATE32,
        _DTypeCode.DATE64,
        _DTypeCode.STRING,
        _DTypeCode.LARGE_STRING,
        _DTypeCode.LARGE_BINARY,
        _DTypeCode.JSON,
    ]

    def to_pyarrow_dtype(self) -> pa.DataType:
        if self.type_code == _DTypeCode.BOOL:
            return pa.bool_()
        if self.type_code == _DTypeCode.STRING:
            # String is deprecated; automatically replacing with LargeString
            return pa.large_utf8()
        if self.type_code == _DTypeCode.JSON:
            return pyarrow_json_type()
        try:
            return getattr(pa, self.type_code.name.lower())()
        except AttributeError:
            raise ValueError(f"Unsupported dtype: {self.type_code}") from None


class _TimeUnitDType(_BaseSerializedDType, frozen=True):
    type_code: Literal[_DTypeCode.TIME32, _DTypeCode.TIME64, _DTypeCode.DURATION]
    time_unit: _TimeUnitCode

    def to_pyarrow_dtype(self) -> pa.DataType:
        return getattr(pa, self.type_code.name.lower())(self.time_unit)


class _TimestampDType(_BaseSerializedDType, frozen=True):
    type_code: Literal[_DTypeCode.TIMESTAMP]
    time_unit: _TimeUnitCode
    timezone: Optional[str]

    def to_pyarrow_dtype(self) -> pa.DataType:
        return pa.timestamp(self.time_unit, self.timezone)


class _BinaryDType(_BaseSerializedDType, frozen=True):
    type_code: Literal[_DTypeCode.BINARY]
    length: int

    def to_pyarrow_dtype(self) -> pa.DataType:
        # Binary is deprecated; automatically upgrading to LargeBinary
        return pa.large_binary()
        # return pa.binary(self.length)


class _ListDType(_BaseSerializedDType, frozen=True):
    type_code: Literal[_DTypeCode.LIST]
    inner_dtype: _SerializedDType
    length: int

    def to_pyarrow_dtype(self) -> pa.DataType:
        if self.length >= 0:
            return pa.list_(self.inner_dtype.to_pyarrow_dtype(), self.length)
        # List is deprecated; automatically upgrading to LargeList
        return pa.large_list(self.inner_dtype.to_pyarrow_dtype())


class _LargeListDType(_BaseSerializedDType, frozen=True):
    type_code: Literal[_DTypeCode.LARGE_LIST]
    inner_dtype: _SerializedDType

    def to_pyarrow_dtype(self) -> pa.DataType:
        return pa.large_list(self.inner_dtype.to_pyarrow_dtype())


class _Field(BaseModel):
    name: str
    dtype: _SerializedDType
    nullable: bool = True

    def to_pyarrow_dtype(self) -> pa.Field:
        return pa.field(self.name, self.dtype.to_pyarrow_dtype(), self.nullable)


class _StructDType(_BaseSerializedDType, frozen=True):
    type_code: Literal[_DTypeCode.STRUCT]
    fields: List[_Field]

    def to_pyarrow_dtype(self) -> pa.DataType:
        return pa.struct([x.to_pyarrow_dtype() for x in self.fields])


class _MapDType(_BaseSerializedDType, frozen=True):
    type_code: Literal[_DTypeCode.MAP]
    key_field: _Field
    item_field: _Field

    def to_pyarrow_dtype(self) -> pa.DataType:
        return pa.map_(self.key_field.to_pyarrow_dtype(), self.item_field.to_pyarrow_dtype())


_SerializedDType = Annotated[
    Union[
        _SingletonDType,
        _TimeUnitDType,
        _TimestampDType,
        _BinaryDType,
        _ListDType,
        _LargeListDType,
        _StructDType,
        _MapDType,
    ],
    Field(discriminator="type_code"),
]

_Field.update_forward_refs()
_ListDType.update_forward_refs()
_LargeListDType.update_forward_refs()
_MapDType.update_forward_refs()


class _Deserializer(BaseModel):
    dtype: _SerializedDType


def deserialize_dtype(serialized_dtype: str) -> pa.DataType:
    deserializer = _Deserializer(dtype=json.loads(serialized_dtype))
    pa_dtype = deserializer.dtype.to_pyarrow_dtype()
    return pa_dtype


def serialize_dtype(pa_dtype: pa.DataType) -> str:
    return _serialize_pyarrow_dtype(pa_dtype).json()


def _serialize_pyarrow_dtype(pa_dtype: pa.DataType) -> _SerializedDType:
    if is_pyarrow_json_type(pa_dtype):
        return _SingletonDType(type_code=_DTypeCode.JSON)
    if pa.types.is_boolean(pa_dtype):
        return _SingletonDType(type_code=_DTypeCode.BOOL)
    if pa.types.is_uint8(pa_dtype):
        return _SingletonDType(type_code=_DTypeCode.UINT8)
    if pa.types.is_uint16(pa_dtype):
        return _SingletonDType(type_code=_DTypeCode.UINT16)
    if pa.types.is_uint32(pa_dtype):
        return _SingletonDType(type_code=_DTypeCode.UINT32)
    if pa.types.is_uint64(pa_dtype):
        return _SingletonDType(type_code=_DTypeCode.UINT64)
    if pa.types.is_int8(pa_dtype):
        return _SingletonDType(type_code=_DTypeCode.INT8)
    if pa.types.is_int16(pa_dtype):
        return _SingletonDType(type_code=_DTypeCode.INT16)
    if pa.types.is_int32(pa_dtype):
        return _SingletonDType(type_code=_DTypeCode.INT32)
    if pa.types.is_int64(pa_dtype):
        return _SingletonDType(type_code=_DTypeCode.INT64)
    if pa.types.is_float16(pa_dtype):
        return _SingletonDType(type_code=_DTypeCode.FLOAT16)
    if pa.types.is_float32(pa_dtype):
        return _SingletonDType(type_code=_DTypeCode.FLOAT32)
    if pa.types.is_float64(pa_dtype):
        return _SingletonDType(type_code=_DTypeCode.FLOAT64)
    if pa.types.is_time32(pa_dtype):
        assert isinstance(pa_dtype, pa.Time32Type)
        return _TimeUnitDType(type_code=_DTypeCode.TIME32, time_unit=pa_dtype.unit)

    if pa.types.is_time64(pa_dtype):
        assert isinstance(pa_dtype, pa.Time64Type)
        return _TimeUnitDType(type_code=_DTypeCode.TIME64, time_unit=pa_dtype.unit)

    if pa.types.is_timestamp(pa_dtype):
        assert isinstance(pa_dtype, pa.TimestampType)
        return _TimestampDType(
            type_code=_DTypeCode.TIMESTAMP,
            time_unit=pa_dtype.unit,
            timezone=pa_dtype.tz,
        )

    if pa.types.is_date32(pa_dtype):
        return _SingletonDType(type_code=_DTypeCode.DATE32)
    if pa.types.is_date64(pa_dtype):
        return _SingletonDType(type_code=_DTypeCode.DATE64)
    if pa.types.is_duration(pa_dtype):
        assert isinstance(pa_dtype, pa.DurationType)
        return _TimeUnitDType(type_code=_DTypeCode.DURATION, time_unit=pa_dtype.unit)

    if pa.types.is_large_string(pa_dtype):
        return _SingletonDType(type_code=_DTypeCode.LARGE_STRING)
    if pa.types.is_large_binary(pa_dtype):
        return _SingletonDType(type_code=_DTypeCode.LARGE_BINARY)
    if pa.types.is_fixed_size_binary(pa_dtype):
        assert isinstance(pa_dtype, pa.FixedSizeBinaryType)
        return _BinaryDType(type_code=_DTypeCode.BINARY, length=pa_dtype.byte_width)
    if pa.types.is_binary(pa_dtype):
        raise ValueError("The `Binary` data type is not supported. Instead, use `LargeBinary`")
    #     return _BinaryDType(type_code=_DTypeCode.BINARY, length=-1)
    if pa.types.is_string(pa_dtype):
        raise ValueError("The `String` data type is not supported. Instead, use `LargeString`")
    #     return _SingletonDType(type_code=_DTypeCode.STRING)

    if pa.types.is_large_list(pa_dtype):
        assert isinstance(pa_dtype, pa.LargeListType)
        return _LargeListDType(
            type_code=_DTypeCode.LARGE_LIST, inner_dtype=_serialize_pyarrow_dtype(pa_dtype.value_type)
        )
    if pa.types.is_fixed_size_list(pa_dtype):
        assert isinstance(pa_dtype, pa.FixedSizeListType)
        return _ListDType(
            type_code=_DTypeCode.LIST,
            inner_dtype=_serialize_pyarrow_dtype(pa_dtype.value_type),
            length=pa_dtype.list_size,
        )

    if pa.types.is_list(pa_dtype):
        assert isinstance(pa_dtype, pa.ListType)
        return _ListDType(
            type_code=_DTypeCode.LIST,
            inner_dtype=_serialize_pyarrow_dtype(pa_dtype.value_type),
            length=-1,
        )

    if pa.types.is_struct(pa_dtype):
        assert isinstance(pa_dtype, pa.StructType)
        schema = pa.schema(pa_dtype)
        return _StructDType(
            type_code=_DTypeCode.STRUCT,
            fields=[
                _Field(name=name, dtype=_serialize_pyarrow_dtype(dtype))
                for (name, dtype) in zip(schema.names, schema.types)
            ],
        )

    if pa.types.is_map(pa_dtype):
        assert isinstance(pa_dtype, pa.MapType)
        return _MapDType(
            type_code=_DTypeCode.MAP,
            key_field=_Field(
                name=pa_dtype.key_field.name,
                dtype=_serialize_pyarrow_dtype(pa_dtype.key_field.type),
                nullable=pa_dtype.key_field.nullable,
            ),
            item_field=_Field(
                name=pa_dtype.item_field.name,
                dtype=_serialize_pyarrow_dtype(pa_dtype.item_field.type),
                nullable=pa_dtype.item_field.nullable,
            ),
        )

    raise ValueError(f"Unsupported dtype: {pa_dtype}")
