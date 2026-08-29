from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
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

class OfflineWideTableRunKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OFFLINE_WIDE_TABLE_RUN_KIND_UNSPECIFIED: _ClassVar[OfflineWideTableRunKind]
    OFFLINE_WIDE_TABLE_RUN_KIND_FILL: _ClassVar[OfflineWideTableRunKind]

class OfflineWideTableRunStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OFFLINE_WIDE_TABLE_RUN_STATUS_UNSPECIFIED: _ClassVar[OfflineWideTableRunStatus]
    OFFLINE_WIDE_TABLE_RUN_STATUS_QUEUED: _ClassVar[OfflineWideTableRunStatus]
    OFFLINE_WIDE_TABLE_RUN_STATUS_RUNNING: _ClassVar[OfflineWideTableRunStatus]
    OFFLINE_WIDE_TABLE_RUN_STATUS_COMPLETED: _ClassVar[OfflineWideTableRunStatus]
    OFFLINE_WIDE_TABLE_RUN_STATUS_FAILED: _ClassVar[OfflineWideTableRunStatus]
    OFFLINE_WIDE_TABLE_RUN_STATUS_CANCELED: _ClassVar[OfflineWideTableRunStatus]

OFFLINE_WIDE_TABLE_RUN_KIND_UNSPECIFIED: OfflineWideTableRunKind
OFFLINE_WIDE_TABLE_RUN_KIND_FILL: OfflineWideTableRunKind
OFFLINE_WIDE_TABLE_RUN_STATUS_UNSPECIFIED: OfflineWideTableRunStatus
OFFLINE_WIDE_TABLE_RUN_STATUS_QUEUED: OfflineWideTableRunStatus
OFFLINE_WIDE_TABLE_RUN_STATUS_RUNNING: OfflineWideTableRunStatus
OFFLINE_WIDE_TABLE_RUN_STATUS_COMPLETED: OfflineWideTableRunStatus
OFFLINE_WIDE_TABLE_RUN_STATUS_FAILED: OfflineWideTableRunStatus
OFFLINE_WIDE_TABLE_RUN_STATUS_CANCELED: OfflineWideTableRunStatus

class OfflineWideTableRun(_message.Message):
    __slots__ = (
        "id",
        "environment_id",
        "deployment_id",
        "kind",
        "namespace",
        "status",
        "watermark_before_micros",
        "watermark_after_micros",
        "rows_filled",
        "error_message",
        "created_at",
        "started_at",
        "finished_at",
        "job_queue_id",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    WATERMARK_BEFORE_MICROS_FIELD_NUMBER: _ClassVar[int]
    WATERMARK_AFTER_MICROS_FIELD_NUMBER: _ClassVar[int]
    ROWS_FILLED_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    FINISHED_AT_FIELD_NUMBER: _ClassVar[int]
    JOB_QUEUE_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    environment_id: str
    deployment_id: str
    kind: OfflineWideTableRunKind
    namespace: str
    status: OfflineWideTableRunStatus
    watermark_before_micros: int
    watermark_after_micros: int
    rows_filled: int
    error_message: str
    created_at: _timestamp_pb2.Timestamp
    started_at: _timestamp_pb2.Timestamp
    finished_at: _timestamp_pb2.Timestamp
    job_queue_id: int
    def __init__(
        self,
        id: _Optional[str] = ...,
        environment_id: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
        kind: _Optional[_Union[OfflineWideTableRunKind, str]] = ...,
        namespace: _Optional[str] = ...,
        status: _Optional[_Union[OfflineWideTableRunStatus, str]] = ...,
        watermark_before_micros: _Optional[int] = ...,
        watermark_after_micros: _Optional[int] = ...,
        rows_filled: _Optional[int] = ...,
        error_message: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        started_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        finished_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        job_queue_id: _Optional[int] = ...,
    ) -> None: ...

class ListOfflineWideTableRunsRequest(_message.Message):
    __slots__ = ("cursor", "limit", "namespace", "status", "kind")
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    cursor: str
    limit: int
    namespace: str
    status: OfflineWideTableRunStatus
    kind: OfflineWideTableRunKind
    def __init__(
        self,
        cursor: _Optional[str] = ...,
        limit: _Optional[int] = ...,
        namespace: _Optional[str] = ...,
        status: _Optional[_Union[OfflineWideTableRunStatus, str]] = ...,
        kind: _Optional[_Union[OfflineWideTableRunKind, str]] = ...,
    ) -> None: ...

class ListOfflineWideTableRunsResponse(_message.Message):
    __slots__ = ("runs", "cursor")
    RUNS_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    runs: _containers.RepeatedCompositeFieldContainer[OfflineWideTableRun]
    cursor: str
    def __init__(
        self, runs: _Optional[_Iterable[_Union[OfflineWideTableRun, _Mapping]]] = ..., cursor: _Optional[str] = ...
    ) -> None: ...

class GetOfflineWideTableRunRequest(_message.Message):
    __slots__ = ("run_id",)
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    run_id: str
    def __init__(self, run_id: _Optional[str] = ...) -> None: ...

class GetOfflineWideTableRunResponse(_message.Message):
    __slots__ = ("run",)
    RUN_FIELD_NUMBER: _ClassVar[int]
    run: OfflineWideTableRun
    def __init__(self, run: _Optional[_Union[OfflineWideTableRun, _Mapping]] = ...) -> None: ...

class OfflineWideTableSchedule(_message.Message):
    __slots__ = ("id", "name", "namespace", "crontab", "kind")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    CRONTAB_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    namespace: str
    crontab: str
    kind: OfflineWideTableRunKind
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        crontab: _Optional[str] = ...,
        kind: _Optional[_Union[OfflineWideTableRunKind, str]] = ...,
    ) -> None: ...

class OfflineWideTableScheduleInfo(_message.Message):
    __slots__ = ("schedule", "latest_run")
    SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    LATEST_RUN_FIELD_NUMBER: _ClassVar[int]
    schedule: OfflineWideTableSchedule
    latest_run: OfflineWideTableRun
    def __init__(
        self,
        schedule: _Optional[_Union[OfflineWideTableSchedule, _Mapping]] = ...,
        latest_run: _Optional[_Union[OfflineWideTableRun, _Mapping]] = ...,
    ) -> None: ...

class GetActiveOfflineWideTableSchedulesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetActiveOfflineWideTableSchedulesResponse(_message.Message):
    __slots__ = ("schedules",)
    SCHEDULES_FIELD_NUMBER: _ClassVar[int]
    schedules: _containers.RepeatedCompositeFieldContainer[OfflineWideTableScheduleInfo]
    def __init__(
        self, schedules: _Optional[_Iterable[_Union[OfflineWideTableScheduleInfo, _Mapping]]] = ...
    ) -> None: ...

class TriggerOfflineWideTableFillRequest(_message.Message):
    __slots__ = ("namespace",)
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    def __init__(self, namespace: _Optional[str] = ...) -> None: ...

class TriggerOfflineWideTableFillResponse(_message.Message):
    __slots__ = ("run",)
    RUN_FIELD_NUMBER: _ClassVar[int]
    run: OfflineWideTableRun
    def __init__(self, run: _Optional[_Union[OfflineWideTableRun, _Mapping]] = ...) -> None: ...

class TriggerOfflineWideTableCompactionRequest(_message.Message):
    __slots__ = ("namespace",)
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    def __init__(self, namespace: _Optional[str] = ...) -> None: ...

class TriggerOfflineWideTableCompactionResponse(_message.Message):
    __slots__ = ("operation_id",)
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    def __init__(self, operation_id: _Optional[str] = ...) -> None: ...
