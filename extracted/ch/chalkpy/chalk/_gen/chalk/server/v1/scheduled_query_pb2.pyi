from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.server.v1 import scheduled_query_run_pb2 as _scheduled_query_run_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
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

class GetActiveScheduledQueriesRequest(_message.Message):
    __slots__ = ("deployment_id",)
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    def __init__(self, deployment_id: _Optional[str] = ...) -> None: ...

class ScheduledQueryRunInfo(_message.Message):
    __slots__ = ("id", "offline_query_id", "workflow_execution_id", "status", "has_errors")
    ID_FIELD_NUMBER: _ClassVar[int]
    OFFLINE_QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    WORKFLOW_EXECUTION_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    HAS_ERRORS_FIELD_NUMBER: _ClassVar[int]
    id: int
    offline_query_id: str
    workflow_execution_id: str
    status: _scheduled_query_run_pb2.ScheduledQueryRunStatus
    has_errors: bool
    def __init__(
        self,
        id: _Optional[int] = ...,
        offline_query_id: _Optional[str] = ...,
        workflow_execution_id: _Optional[str] = ...,
        status: _Optional[_Union[_scheduled_query_run_pb2.ScheduledQueryRunStatus, str]] = ...,
        has_errors: bool = ...,
    ) -> None: ...

class ScheduledQueryInfo(_message.Message):
    __slots__ = ("schedule", "control", "latest_run")
    SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    CONTROL_FIELD_NUMBER: _ClassVar[int]
    LATEST_RUN_FIELD_NUMBER: _ClassVar[int]
    schedule: _scheduled_query_run_pb2.ScheduledQuerySchedule
    control: _scheduled_query_run_pb2.ScheduledQueryControl
    latest_run: ScheduledQueryRunInfo
    def __init__(
        self,
        schedule: _Optional[_Union[_scheduled_query_run_pb2.ScheduledQuerySchedule, _Mapping]] = ...,
        control: _Optional[_Union[_scheduled_query_run_pb2.ScheduledQueryControl, _Mapping]] = ...,
        latest_run: _Optional[_Union[ScheduledQueryRunInfo, _Mapping]] = ...,
    ) -> None: ...

class GetActiveScheduledQueriesResponse(_message.Message):
    __slots__ = ("scheduled_queries",)
    SCHEDULED_QUERIES_FIELD_NUMBER: _ClassVar[int]
    scheduled_queries: _containers.RepeatedCompositeFieldContainer[ScheduledQueryInfo]
    def __init__(self, scheduled_queries: _Optional[_Iterable[_Union[ScheduledQueryInfo, _Mapping]]] = ...) -> None: ...

class GetScheduledQueryControlRequest(_message.Message):
    __slots__ = ("cron_query_id", "cron_query_name")
    CRON_QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    CRON_QUERY_NAME_FIELD_NUMBER: _ClassVar[int]
    cron_query_id: int
    cron_query_name: str
    def __init__(self, cron_query_id: _Optional[int] = ..., cron_query_name: _Optional[str] = ...) -> None: ...

class GetScheduledQueryControlResponse(_message.Message):
    __slots__ = ("control",)
    CONTROL_FIELD_NUMBER: _ClassVar[int]
    control: _scheduled_query_run_pb2.ScheduledQueryControl
    def __init__(
        self, control: _Optional[_Union[_scheduled_query_run_pb2.ScheduledQueryControl, _Mapping]] = ...
    ) -> None: ...

class UpdateScheduledQueryControlOperation(_message.Message):
    __slots__ = ("status", "job_config")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    JOB_CONFIG_FIELD_NUMBER: _ClassVar[int]
    status: _scheduled_query_run_pb2.CronControlStatus
    job_config: str
    def __init__(
        self,
        status: _Optional[_Union[_scheduled_query_run_pb2.CronControlStatus, str]] = ...,
        job_config: _Optional[str] = ...,
    ) -> None: ...

class UpdateScheduledQueryControlRequest(_message.Message):
    __slots__ = ("cron_query_id", "update", "update_mask")
    CRON_QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    UPDATE_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    cron_query_id: int
    update: UpdateScheduledQueryControlOperation
    update_mask: _field_mask_pb2.FieldMask
    def __init__(
        self,
        cron_query_id: _Optional[int] = ...,
        update: _Optional[_Union[UpdateScheduledQueryControlOperation, _Mapping]] = ...,
        update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class UpdateScheduledQueryControlResponse(_message.Message):
    __slots__ = ("control",)
    CONTROL_FIELD_NUMBER: _ClassVar[int]
    control: _scheduled_query_run_pb2.ScheduledQueryControl
    def __init__(
        self, control: _Optional[_Union[_scheduled_query_run_pb2.ScheduledQueryControl, _Mapping]] = ...
    ) -> None: ...

class GetScheduledQueryScheduleRequest(_message.Message):
    __slots__ = ("schedule_id", "cron_query_id")
    SCHEDULE_ID_FIELD_NUMBER: _ClassVar[int]
    CRON_QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    schedule_id: int
    cron_query_id: int
    def __init__(self, schedule_id: _Optional[int] = ..., cron_query_id: _Optional[int] = ...) -> None: ...

class GetScheduledQueryScheduleResponse(_message.Message):
    __slots__ = ("schedule",)
    SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    schedule: _scheduled_query_run_pb2.ScheduledQuerySchedule
    def __init__(
        self, schedule: _Optional[_Union[_scheduled_query_run_pb2.ScheduledQuerySchedule, _Mapping]] = ...
    ) -> None: ...
