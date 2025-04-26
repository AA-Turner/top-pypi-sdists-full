from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DATA_TYPE_ARRAY: DataTypeEnum
DATA_TYPE_BOOL: DataTypeEnum
DATA_TYPE_FLOAT32: DataTypeEnum
DATA_TYPE_FLOAT64: DataTypeEnum
DATA_TYPE_INT32: DataTypeEnum
DATA_TYPE_INT64: DataTypeEnum
DATA_TYPE_MAP: DataTypeEnum
DATA_TYPE_STRING: DataTypeEnum
DATA_TYPE_STRUCT: DataTypeEnum
DATA_TYPE_TIMESTAMP: DataTypeEnum
DATA_TYPE_TIMESTAMP_INT96: DataTypeEnum
DATA_TYPE_UNKNOWN: DataTypeEnum
DESCRIPTOR: _descriptor.FileDescriptor

class DataType(_message.Message):
    __slots__ = ["array_element_type", "map_key_type", "map_value_type", "struct_fields", "type"]
    ARRAY_ELEMENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    MAP_KEY_TYPE_FIELD_NUMBER: _ClassVar[int]
    MAP_VALUE_TYPE_FIELD_NUMBER: _ClassVar[int]
    STRUCT_FIELDS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    array_element_type: DataType
    map_key_type: DataType
    map_value_type: DataType
    struct_fields: _containers.RepeatedCompositeFieldContainer[StructField]
    type: DataTypeEnum
    def __init__(self, type: _Optional[_Union[DataTypeEnum, str]] = ..., array_element_type: _Optional[_Union[DataType, _Mapping]] = ..., struct_fields: _Optional[_Iterable[_Union[StructField, _Mapping]]] = ..., map_key_type: _Optional[_Union[DataType, _Mapping]] = ..., map_value_type: _Optional[_Union[DataType, _Mapping]] = ...) -> None: ...

class StructField(_message.Message):
    __slots__ = ["data_type", "name"]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    data_type: DataType
    name: str
    def __init__(self, name: _Optional[str] = ..., data_type: _Optional[_Union[DataType, _Mapping]] = ...) -> None: ...

class DataTypeEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
