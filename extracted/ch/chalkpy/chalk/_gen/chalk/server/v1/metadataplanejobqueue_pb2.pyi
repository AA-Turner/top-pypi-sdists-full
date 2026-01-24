from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf import struct_pb2 as _struct_pb2
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

class MetadataJobStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    METADATA_JOB_STATUS_UNSPECIFIED: _ClassVar[MetadataJobStatus]
    METADATA_JOB_STATUS_SCHEDULED: _ClassVar[MetadataJobStatus]
    METADATA_JOB_STATUS_WORKING: _ClassVar[MetadataJobStatus]
    METADATA_JOB_STATUS_RETRYABLE: _ClassVar[MetadataJobStatus]
    METADATA_JOB_STATUS_SUCCESS: _ClassVar[MetadataJobStatus]
    METADATA_JOB_STATUS_FAILED: _ClassVar[MetadataJobStatus]

METADATA_JOB_STATUS_UNSPECIFIED: MetadataJobStatus
METADATA_JOB_STATUS_SCHEDULED: MetadataJobStatus
METADATA_JOB_STATUS_WORKING: MetadataJobStatus
METADATA_JOB_STATUS_RETRYABLE: MetadataJobStatus
METADATA_JOB_STATUS_SUCCESS: MetadataJobStatus
METADATA_JOB_STATUS_FAILED: MetadataJobStatus

class MetadataScheduledJob(_message.Message):
    __slots__ = ("id", "metadata", "max_attempts", "created_at", "tag", "name", "custom_tags", "environment_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    MAX_ATTEMPTS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_TAGS_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    metadata: _struct_pb2.Struct
    max_attempts: int
    created_at: _timestamp_pb2.Timestamp
    tag: str
    name: str
    custom_tags: _containers.RepeatedScalarFieldContainer[str]
    environment_id: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
        max_attempts: _Optional[int] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        tag: _Optional[str] = ...,
        name: _Optional[str] = ...,
        custom_tags: _Optional[_Iterable[str]] = ...,
        environment_id: _Optional[str] = ...,
    ) -> None: ...

class MetadataJob(_message.Message):
    __slots__ = (
        "id",
        "status",
        "schedule_name",
        "attempt",
        "max_attempts",
        "created_at",
        "lease_start",
        "lease_end",
        "tag",
        "metadata",
        "attempts",
        "custom_tags",
        "environment_id",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SCHEDULE_NAME_FIELD_NUMBER: _ClassVar[int]
    ATTEMPT_FIELD_NUMBER: _ClassVar[int]
    MAX_ATTEMPTS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    LEASE_START_FIELD_NUMBER: _ClassVar[int]
    LEASE_END_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ATTEMPTS_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_TAGS_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    status: MetadataJobStatus
    schedule_name: str
    attempt: int
    max_attempts: int
    created_at: _timestamp_pb2.Timestamp
    lease_start: _timestamp_pb2.Timestamp
    lease_end: _timestamp_pb2.Timestamp
    tag: str
    metadata: _struct_pb2.Struct
    attempts: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Struct]
    custom_tags: _containers.RepeatedScalarFieldContainer[str]
    environment_id: str
    def __init__(
        self,
        id: _Optional[int] = ...,
        status: _Optional[_Union[MetadataJobStatus, str]] = ...,
        schedule_name: _Optional[str] = ...,
        attempt: _Optional[int] = ...,
        max_attempts: _Optional[int] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        lease_start: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        lease_end: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        tag: _Optional[str] = ...,
        metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
        attempts: _Optional[_Iterable[_Union[_struct_pb2.Struct, _Mapping]]] = ...,
        custom_tags: _Optional[_Iterable[str]] = ...,
        environment_id: _Optional[str] = ...,
    ) -> None: ...

class ListMetadataScheduledJobsRequest(_message.Message):
    __slots__ = ("environment_id", "tag", "name", "limit", "offset")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    tag: str
    name: str
    limit: int
    offset: int
    def __init__(
        self,
        environment_id: _Optional[str] = ...,
        tag: _Optional[str] = ...,
        name: _Optional[str] = ...,
        limit: _Optional[int] = ...,
        offset: _Optional[int] = ...,
    ) -> None: ...

class ListMetadataScheduledJobsResponse(_message.Message):
    __slots__ = ("scheduled_jobs", "total")
    SCHEDULED_JOBS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    scheduled_jobs: _containers.RepeatedCompositeFieldContainer[MetadataScheduledJob]
    total: int
    def __init__(
        self,
        scheduled_jobs: _Optional[_Iterable[_Union[MetadataScheduledJob, _Mapping]]] = ...,
        total: _Optional[int] = ...,
    ) -> None: ...

class GetMetadataScheduledJobRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetMetadataScheduledJobResponse(_message.Message):
    __slots__ = ("scheduled_job",)
    SCHEDULED_JOB_FIELD_NUMBER: _ClassVar[int]
    scheduled_job: MetadataScheduledJob
    def __init__(self, scheduled_job: _Optional[_Union[MetadataScheduledJob, _Mapping]] = ...) -> None: ...

class ListMetadataJobsRequest(_message.Message):
    __slots__ = ("environment_id", "status", "tag", "schedule_name", "limit", "offset")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    SCHEDULE_NAME_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    status: MetadataJobStatus
    tag: str
    schedule_name: str
    limit: int
    offset: int
    def __init__(
        self,
        environment_id: _Optional[str] = ...,
        status: _Optional[_Union[MetadataJobStatus, str]] = ...,
        tag: _Optional[str] = ...,
        schedule_name: _Optional[str] = ...,
        limit: _Optional[int] = ...,
        offset: _Optional[int] = ...,
    ) -> None: ...

class ListMetadataJobsResponse(_message.Message):
    __slots__ = ("jobs", "total")
    JOBS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    jobs: _containers.RepeatedCompositeFieldContainer[MetadataJob]
    total: int
    def __init__(
        self, jobs: _Optional[_Iterable[_Union[MetadataJob, _Mapping]]] = ..., total: _Optional[int] = ...
    ) -> None: ...

class GetMetadataJobRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class GetMetadataJobResponse(_message.Message):
    __slots__ = ("job",)
    JOB_FIELD_NUMBER: _ClassVar[int]
    job: MetadataJob
    def __init__(self, job: _Optional[_Union[MetadataJob, _Mapping]] = ...) -> None: ...
