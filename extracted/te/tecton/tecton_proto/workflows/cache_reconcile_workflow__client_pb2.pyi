from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CacheReconcileTaskAttemptWorkflow(_message.Message):
    __slots__ = ["cache_id", "parent_workflow_id", "status"]
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    CACHE_ID_FIELD_NUMBER: _ClassVar[int]
    FAILED: CacheReconcileTaskAttemptWorkflow.Status
    PARENT_WORKFLOW_ID_FIELD_NUMBER: _ClassVar[int]
    RUNNING: CacheReconcileTaskAttemptWorkflow.Status
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STATUS_UNSPECIFIED: CacheReconcileTaskAttemptWorkflow.Status
    SUCCEEDED: CacheReconcileTaskAttemptWorkflow.Status
    cache_id: str
    parent_workflow_id: str
    status: CacheReconcileTaskAttemptWorkflow.Status
    def __init__(self, cache_id: _Optional[str] = ..., parent_workflow_id: _Optional[str] = ..., status: _Optional[_Union[CacheReconcileTaskAttemptWorkflow.Status, str]] = ...) -> None: ...

class CacheReconcileTaskWorkflow(_message.Message):
    __slots__ = ["attempt_workflow_ids", "cache_id", "last_attempt_num", "requested_at_millis"]
    ATTEMPT_WORKFLOW_IDS_FIELD_NUMBER: _ClassVar[int]
    CACHE_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_ATTEMPT_NUM_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_AT_MILLIS_FIELD_NUMBER: _ClassVar[int]
    attempt_workflow_ids: _containers.RepeatedScalarFieldContainer[str]
    cache_id: str
    last_attempt_num: int
    requested_at_millis: int
    def __init__(self, cache_id: _Optional[str] = ..., requested_at_millis: _Optional[int] = ..., attempt_workflow_ids: _Optional[_Iterable[str]] = ..., last_attempt_num: _Optional[int] = ...) -> None: ...
