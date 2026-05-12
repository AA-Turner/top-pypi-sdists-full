import datetime

from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from nominal_api_protos.nominal.gen.v1 import error_pb2 as _error_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CompactionStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    COMPACTION_STATUS_UNSPECIFIED: _ClassVar[CompactionStatus]
    COMPACTION_STATUS_PENDING: _ClassVar[CompactionStatus]
    COMPACTION_STATUS_RUNNING: _ClassVar[CompactionStatus]
    COMPACTION_STATUS_SUCCEEDED: _ClassVar[CompactionStatus]
    COMPACTION_STATUS_FAILED: _ClassVar[CompactionStatus]
    COMPACTION_STATUS_NOT_FOUND: _ClassVar[CompactionStatus]

class CompactionErrors(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    COMPACTION_ERRORS_UNSPECIFIED: _ClassVar[CompactionErrors]
    COMPACTION_ERRORS_TABLE_NOT_FOUND: _ClassVar[CompactionErrors]
COMPACTION_STATUS_UNSPECIFIED: CompactionStatus
COMPACTION_STATUS_PENDING: CompactionStatus
COMPACTION_STATUS_RUNNING: CompactionStatus
COMPACTION_STATUS_SUCCEEDED: CompactionStatus
COMPACTION_STATUS_FAILED: CompactionStatus
COMPACTION_STATUS_NOT_FOUND: CompactionStatus
COMPACTION_ERRORS_UNSPECIFIED: CompactionErrors
COMPACTION_ERRORS_TABLE_NOT_FOUND: CompactionErrors

class Namespace(_message.Message):
    __slots__ = ("levels",)
    LEVELS_FIELD_NUMBER: _ClassVar[int]
    levels: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, levels: _Optional[_Iterable[str]] = ...) -> None: ...

class TableName(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class TableTarget(_message.Message):
    __slots__ = ("namespace", "table_name")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    namespace: Namespace
    table_name: TableName
    def __init__(self, namespace: _Optional[_Union[Namespace, _Mapping]] = ..., table_name: _Optional[_Union[TableName, _Mapping]] = ...) -> None: ...

class CompactionRun(_message.Message):
    __slots__ = ("target", "status", "started_at", "finished_at")
    TARGET_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    FINISHED_AT_FIELD_NUMBER: _ClassVar[int]
    target: TableTarget
    status: CompactionStatus
    started_at: _timestamp_pb2.Timestamp
    finished_at: _timestamp_pb2.Timestamp
    def __init__(self, target: _Optional[_Union[TableTarget, _Mapping]] = ..., status: _Optional[_Union[CompactionStatus, str]] = ..., started_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., finished_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class CompactTableRequest(_message.Message):
    __slots__ = ("target",)
    TARGET_FIELD_NUMBER: _ClassVar[int]
    target: TableTarget
    def __init__(self, target: _Optional[_Union[TableTarget, _Mapping]] = ...) -> None: ...

class CompactTableResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetCompactionRunRequest(_message.Message):
    __slots__ = ("target",)
    TARGET_FIELD_NUMBER: _ClassVar[int]
    target: TableTarget
    def __init__(self, target: _Optional[_Union[TableTarget, _Mapping]] = ...) -> None: ...

class GetCompactionRunResponse(_message.Message):
    __slots__ = ("run",)
    RUN_FIELD_NUMBER: _ClassVar[int]
    run: CompactionRun
    def __init__(self, run: _Optional[_Union[CompactionRun, _Mapping]] = ...) -> None: ...
