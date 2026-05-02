from buf.validate import validate_pb2 as _validate_pb2
from corvic_generated.orm.v1 import table_pb2 as _table_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ColumnSchema(_message.Message):
    __slots__ = ("name", "dtype", "ftype", "feature_type", "possible_feature_types")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DTYPE_FIELD_NUMBER: _ClassVar[int]
    FTYPE_FIELD_NUMBER: _ClassVar[int]
    FEATURE_TYPE_FIELD_NUMBER: _ClassVar[int]
    POSSIBLE_FEATURE_TYPES_FIELD_NUMBER: _ClassVar[int]
    name: str
    dtype: str
    ftype: str
    feature_type: _table_pb2.FeatureType
    possible_feature_types: _containers.RepeatedCompositeFieldContainer[_table_pb2.FeatureType]
    def __init__(self, name: _Optional[str] = ..., dtype: _Optional[str] = ..., ftype: _Optional[str] = ..., feature_type: _Optional[_Union[_table_pb2.FeatureType, _Mapping]] = ..., possible_feature_types: _Optional[_Iterable[_Union[_table_pb2.FeatureType, _Mapping]]] = ...) -> None: ...

class TableSchema(_message.Message):
    __slots__ = ("columns",)
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    columns: _containers.RepeatedCompositeFieldContainer[ColumnSchema]
    def __init__(self, columns: _Optional[_Iterable[_Union[ColumnSchema, _Mapping]]] = ...) -> None: ...

class TableEntry(_message.Message):
    __slots__ = ("id", "resource_id", "name", "num_rows", "schema")
    ID_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NUM_ROWS_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    id: str
    resource_id: str
    name: str
    num_rows: int
    schema: TableSchema
    def __init__(self, id: _Optional[str] = ..., resource_id: _Optional[str] = ..., name: _Optional[str] = ..., num_rows: _Optional[int] = ..., schema: _Optional[_Union[TableSchema, _Mapping]] = ...) -> None: ...

class TableData(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Struct]
    def __init__(self, rows: _Optional[_Iterable[_Union[_struct_pb2.Struct, _Mapping]]] = ...) -> None: ...

class DeleteTableRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteTableResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetTableRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetTableResponse(_message.Message):
    __slots__ = ("entry",)
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    entry: TableEntry
    def __init__(self, entry: _Optional[_Union[TableEntry, _Mapping]] = ...) -> None: ...

class ListTablesRequest(_message.Message):
    __slots__ = ("room_id", "resource_id")
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    room_id: str
    resource_id: str
    def __init__(self, room_id: _Optional[str] = ..., resource_id: _Optional[str] = ...) -> None: ...

class ListTablesResponse(_message.Message):
    __slots__ = ("entry",)
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    entry: TableEntry
    def __init__(self, entry: _Optional[_Union[TableEntry, _Mapping]] = ...) -> None: ...

class GetTableHeadRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetTableHeadResponse(_message.Message):
    __slots__ = ("entry", "head")
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    HEAD_FIELD_NUMBER: _ClassVar[int]
    entry: TableEntry
    head: TableData
    def __init__(self, entry: _Optional[_Union[TableEntry, _Mapping]] = ..., head: _Optional[_Union[TableData, _Mapping]] = ...) -> None: ...
