from chalk._gen.chalk.aggregate.v1 import backfill_pb2 as _backfill_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.server.v1 import scheduled_query_run_pb2 as _scheduled_query_run_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
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

class GetActiveScheduledAggregateBackfillsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ScheduledAggregateBackfillControl(_message.Message):
    __slots__ = ("name", "status", "agent_id", "created_at", "updated_at", "job_config")
    NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    JOB_CONFIG_FIELD_NUMBER: _ClassVar[int]
    name: str
    status: _scheduled_query_run_pb2.CronControlStatus
    agent_id: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    job_config: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        status: _Optional[_Union[_scheduled_query_run_pb2.CronControlStatus, str]] = ...,
        agent_id: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        job_config: _Optional[str] = ...,
    ) -> None: ...

class ScheduledAggregateBackfillInfo(_message.Message):
    __slots__ = ("schedule", "control", "latest_run")
    SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    CONTROL_FIELD_NUMBER: _ClassVar[int]
    LATEST_RUN_FIELD_NUMBER: _ClassVar[int]
    schedule: _backfill_pb2.CronAggregateBackfill
    control: ScheduledAggregateBackfillControl
    latest_run: _backfill_pb2.AggregateBackfillJob
    def __init__(
        self,
        schedule: _Optional[_Union[_backfill_pb2.CronAggregateBackfill, _Mapping]] = ...,
        control: _Optional[_Union[ScheduledAggregateBackfillControl, _Mapping]] = ...,
        latest_run: _Optional[_Union[_backfill_pb2.AggregateBackfillJob, _Mapping]] = ...,
    ) -> None: ...

class GetActiveScheduledAggregateBackfillsResponse(_message.Message):
    __slots__ = ("scheduled_aggregate_backfills",)
    SCHEDULED_AGGREGATE_BACKFILLS_FIELD_NUMBER: _ClassVar[int]
    scheduled_aggregate_backfills: _containers.RepeatedCompositeFieldContainer[ScheduledAggregateBackfillInfo]
    def __init__(
        self,
        scheduled_aggregate_backfills: _Optional[_Iterable[_Union[ScheduledAggregateBackfillInfo, _Mapping]]] = ...,
    ) -> None: ...

class GetScheduledAggregateBackfillRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class GetScheduledAggregateBackfillResponse(_message.Message):
    __slots__ = ("scheduled_aggregate_backfill",)
    SCHEDULED_AGGREGATE_BACKFILL_FIELD_NUMBER: _ClassVar[int]
    scheduled_aggregate_backfill: ScheduledAggregateBackfillInfo
    def __init__(
        self, scheduled_aggregate_backfill: _Optional[_Union[ScheduledAggregateBackfillInfo, _Mapping]] = ...
    ) -> None: ...

class GetScheduledAggregateBackfillControlRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class GetScheduledAggregateBackfillControlResponse(_message.Message):
    __slots__ = ("control",)
    CONTROL_FIELD_NUMBER: _ClassVar[int]
    control: ScheduledAggregateBackfillControl
    def __init__(self, control: _Optional[_Union[ScheduledAggregateBackfillControl, _Mapping]] = ...) -> None: ...

class UpdateScheduledAggregateBackfillControlOperation(_message.Message):
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

class UpdateScheduledAggregateBackfillControlRequest(_message.Message):
    __slots__ = ("name", "update", "update_mask")
    NAME_FIELD_NUMBER: _ClassVar[int]
    UPDATE_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    name: str
    update: UpdateScheduledAggregateBackfillControlOperation
    update_mask: _field_mask_pb2.FieldMask
    def __init__(
        self,
        name: _Optional[str] = ...,
        update: _Optional[_Union[UpdateScheduledAggregateBackfillControlOperation, _Mapping]] = ...,
        update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class UpdateScheduledAggregateBackfillControlResponse(_message.Message):
    __slots__ = ("control",)
    CONTROL_FIELD_NUMBER: _ClassVar[int]
    control: ScheduledAggregateBackfillControl
    def __init__(self, control: _Optional[_Union[ScheduledAggregateBackfillControl, _Mapping]] = ...) -> None: ...
