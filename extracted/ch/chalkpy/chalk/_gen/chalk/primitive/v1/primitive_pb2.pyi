from chalk._gen.chalk.arrow.v1 import arrow_pb2 as _arrow_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class Primitive(_message.Message):
    __slots__ = (
        "null_value",
        "bool_value",
        "int64_value",
        "uint64_value",
        "double_value",
        "string_value",
        "bytes_value",
        "duration_value",
        "timestamp_value",
        "arrow_schema",
        "arrow_field",
        "arrow_type",
        "list_value",
        "unordered_dict_value",
    )
    NULL_VALUE_FIELD_NUMBER: _ClassVar[int]
    BOOL_VALUE_FIELD_NUMBER: _ClassVar[int]
    INT64_VALUE_FIELD_NUMBER: _ClassVar[int]
    UINT64_VALUE_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_VALUE_FIELD_NUMBER: _ClassVar[int]
    STRING_VALUE_FIELD_NUMBER: _ClassVar[int]
    BYTES_VALUE_FIELD_NUMBER: _ClassVar[int]
    DURATION_VALUE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_VALUE_FIELD_NUMBER: _ClassVar[int]
    ARROW_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    ARROW_FIELD_FIELD_NUMBER: _ClassVar[int]
    ARROW_TYPE_FIELD_NUMBER: _ClassVar[int]
    LIST_VALUE_FIELD_NUMBER: _ClassVar[int]
    UNORDERED_DICT_VALUE_FIELD_NUMBER: _ClassVar[int]
    null_value: PrimitiveNullOpt
    bool_value: bool
    int64_value: int
    uint64_value: int
    double_value: float
    string_value: str
    bytes_value: bytes
    duration_value: _duration_pb2.Duration
    timestamp_value: _timestamp_pb2.Timestamp
    arrow_schema: _arrow_pb2.Schema
    arrow_field: _arrow_pb2.Field
    arrow_type: _arrow_pb2.ArrowType
    list_value: PrimitiveList
    unordered_dict_value: PrimitiveUnorderedDict
    def __init__(
        self,
        null_value: _Optional[_Union[PrimitiveNullOpt, _Mapping]] = ...,
        bool_value: bool = ...,
        int64_value: _Optional[int] = ...,
        uint64_value: _Optional[int] = ...,
        double_value: _Optional[float] = ...,
        string_value: _Optional[str] = ...,
        bytes_value: _Optional[bytes] = ...,
        duration_value: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        timestamp_value: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        arrow_schema: _Optional[_Union[_arrow_pb2.Schema, _Mapping]] = ...,
        arrow_field: _Optional[_Union[_arrow_pb2.Field, _Mapping]] = ...,
        arrow_type: _Optional[_Union[_arrow_pb2.ArrowType, _Mapping]] = ...,
        list_value: _Optional[_Union[PrimitiveList, _Mapping]] = ...,
        unordered_dict_value: _Optional[_Union[PrimitiveUnorderedDict, _Mapping]] = ...,
    ) -> None: ...

class PrimitiveNullOpt(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class PrimitiveList(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedCompositeFieldContainer[Primitive]
    def __init__(self, values: _Optional[_Iterable[_Union[Primitive, _Mapping]]] = ...) -> None: ...

class PrimitiveUnorderedDict(_message.Message):
    __slots__ = ("items",)
    class ItemsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Primitive
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Primitive, _Mapping]] = ...) -> None: ...

    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.MessageMap[str, Primitive]
    def __init__(self, items: _Optional[_Mapping[str, Primitive]] = ...) -> None: ...
