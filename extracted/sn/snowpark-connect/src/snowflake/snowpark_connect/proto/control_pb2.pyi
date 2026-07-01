from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Config(_message.Message):
    __slots__ = ("log_ast",)
    LOG_AST_FIELD_NUMBER: _ClassVar[int]
    log_ast: bool
    def __init__(self, log_ast: bool = ...) -> None: ...

class PingRequest(_message.Message):
    __slots__ = ("payload",)
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    payload: str
    def __init__(self, payload: _Optional[str] = ...) -> None: ...

class PingResponse(_message.Message):
    __slots__ = ("payload",)
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    payload: str
    def __init__(self, payload: _Optional[str] = ...) -> None: ...

class GetRequestAstRequest(_message.Message):
    __slots__ = ("force_flush",)
    FORCE_FLUSH_FIELD_NUMBER: _ClassVar[int]
    force_flush: bool
    def __init__(self, force_flush: bool = ...) -> None: ...

class GetRequestAstResponse(_message.Message):
    __slots__ = ("spark_requests", "snowpark_ast_batches")
    SPARK_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    SNOWPARK_AST_BATCHES_FIELD_NUMBER: _ClassVar[int]
    spark_requests: _containers.RepeatedScalarFieldContainer[bytes]
    snowpark_ast_batches: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, spark_requests: _Optional[_Iterable[bytes]] = ..., snowpark_ast_batches: _Optional[_Iterable[str]] = ...) -> None: ...
