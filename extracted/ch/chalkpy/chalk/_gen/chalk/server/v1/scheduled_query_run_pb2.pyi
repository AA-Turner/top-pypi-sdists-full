from chalk._gen.chalk.server.v1 import offline_queries_pb2 as _offline_queries_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ScheduledQueryRun(_message.Message):
    __slots__ = (
        "id",
        "environment_id",
        "deployment_id",
        "run_id",
        "cron_query_id",
        "cron_query_schedule_id",
        "cron_name",
        "gcr_execution_id",
        "gcr_job_name",
        "offline_query_id",
        "created_at",
        "updated_at",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    CRON_QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    CRON_QUERY_SCHEDULE_ID_FIELD_NUMBER: _ClassVar[int]
    CRON_NAME_FIELD_NUMBER: _ClassVar[int]
    GCR_EXECUTION_ID_FIELD_NUMBER: _ClassVar[int]
    GCR_JOB_NAME_FIELD_NUMBER: _ClassVar[int]
    OFFLINE_QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: int
    environment_id: str
    deployment_id: str
    run_id: str
    cron_query_id: int
    cron_query_schedule_id: int
    cron_name: str
    gcr_execution_id: str
    gcr_job_name: str
    offline_query_id: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[int] = ...,
        environment_id: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
        run_id: _Optional[str] = ...,
        cron_query_id: _Optional[int] = ...,
        cron_query_schedule_id: _Optional[int] = ...,
        cron_name: _Optional[str] = ...,
        gcr_execution_id: _Optional[str] = ...,
        gcr_job_name: _Optional[str] = ...,
        offline_query_id: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class GetScheduledQueryRunRequest(_message.Message):
    __slots__ = ("run_id", "offline_query_id", "get_mask")
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    OFFLINE_QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    GET_MASK_FIELD_NUMBER: _ClassVar[int]
    run_id: int
    offline_query_id: str
    get_mask: _field_mask_pb2.FieldMask
    def __init__(
        self,
        run_id: _Optional[int] = ...,
        offline_query_id: _Optional[str] = ...,
        get_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class GetScheduledQueryRunResponse(_message.Message):
    __slots__ = ("scheduled_query_run", "offline_query")
    SCHEDULED_QUERY_RUN_FIELD_NUMBER: _ClassVar[int]
    OFFLINE_QUERY_FIELD_NUMBER: _ClassVar[int]
    scheduled_query_run: ScheduledQueryRun
    offline_query: _offline_queries_pb2.OfflineQueryMeta
    def __init__(
        self,
        scheduled_query_run: _Optional[_Union[ScheduledQueryRun, _Mapping]] = ...,
        offline_query: _Optional[_Union[_offline_queries_pb2.OfflineQueryMeta, _Mapping]] = ...,
    ) -> None: ...
