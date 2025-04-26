from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ExecuteSqlQueryRequest(_message.Message):
    __slots__ = ("query",)
    QUERY_FIELD_NUMBER: _ClassVar[int]
    query: str
    def __init__(self, query: _Optional[str] = ...) -> None: ...

class ExecuteSqlQueryResponse(_message.Message):
    __slots__ = ("query_id", "parquet")
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    PARQUET_FIELD_NUMBER: _ClassVar[int]
    query_id: str
    parquet: bytes
    def __init__(self, query_id: _Optional[str] = ..., parquet: _Optional[bytes] = ...) -> None: ...

class PlanSqlQueryRequest(_message.Message):
    __slots__ = ("query",)
    QUERY_FIELD_NUMBER: _ClassVar[int]
    query: str
    def __init__(self, query: _Optional[str] = ...) -> None: ...

class PlanSqlQueryResponse(_message.Message):
    __slots__ = ("logical_plan",)
    LOGICAL_PLAN_FIELD_NUMBER: _ClassVar[int]
    logical_plan: str
    def __init__(self, logical_plan: _Optional[str] = ...) -> None: ...
