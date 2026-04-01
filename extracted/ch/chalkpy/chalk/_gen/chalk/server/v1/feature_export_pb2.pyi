from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
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

class SnowpipeFile(_message.Message):
    __slots__ = (
        "file_name",
        "stage_location",
        "last_load_time",
        "row_count",
        "row_parsed",
        "file_size",
        "first_error_message",
        "first_error_line_number",
        "first_error_character_pos",
        "first_error_column_name",
        "error_count",
        "error_limit",
        "status",
        "pipe_received_time",
    )
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    STAGE_LOCATION_FIELD_NUMBER: _ClassVar[int]
    LAST_LOAD_TIME_FIELD_NUMBER: _ClassVar[int]
    ROW_COUNT_FIELD_NUMBER: _ClassVar[int]
    ROW_PARSED_FIELD_NUMBER: _ClassVar[int]
    FILE_SIZE_FIELD_NUMBER: _ClassVar[int]
    FIRST_ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    FIRST_ERROR_LINE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    FIRST_ERROR_CHARACTER_POS_FIELD_NUMBER: _ClassVar[int]
    FIRST_ERROR_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    ERROR_COUNT_FIELD_NUMBER: _ClassVar[int]
    ERROR_LIMIT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PIPE_RECEIVED_TIME_FIELD_NUMBER: _ClassVar[int]
    file_name: str
    stage_location: str
    last_load_time: _timestamp_pb2.Timestamp
    row_count: float
    row_parsed: float
    file_size: float
    first_error_message: str
    first_error_line_number: float
    first_error_character_pos: float
    first_error_column_name: str
    error_count: int
    error_limit: int
    status: str
    pipe_received_time: _timestamp_pb2.Timestamp
    def __init__(
        self,
        file_name: _Optional[str] = ...,
        stage_location: _Optional[str] = ...,
        last_load_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        row_count: _Optional[float] = ...,
        row_parsed: _Optional[float] = ...,
        file_size: _Optional[float] = ...,
        first_error_message: _Optional[str] = ...,
        first_error_line_number: _Optional[float] = ...,
        first_error_character_pos: _Optional[float] = ...,
        first_error_column_name: _Optional[str] = ...,
        error_count: _Optional[int] = ...,
        error_limit: _Optional[int] = ...,
        status: _Optional[str] = ...,
        pipe_received_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class SnowpipeFileSummary(_message.Message):
    __slots__ = (
        "folder",
        "row_count",
        "row_parsed",
        "file_count",
        "file_size",
        "error_count",
        "pipe_received_time",
        "status",
    )
    FOLDER_FIELD_NUMBER: _ClassVar[int]
    ROW_COUNT_FIELD_NUMBER: _ClassVar[int]
    ROW_PARSED_FIELD_NUMBER: _ClassVar[int]
    FILE_COUNT_FIELD_NUMBER: _ClassVar[int]
    FILE_SIZE_FIELD_NUMBER: _ClassVar[int]
    ERROR_COUNT_FIELD_NUMBER: _ClassVar[int]
    PIPE_RECEIVED_TIME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    folder: str
    row_count: float
    row_parsed: float
    file_count: float
    file_size: float
    error_count: int
    pipe_received_time: _timestamp_pb2.Timestamp
    status: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        folder: _Optional[str] = ...,
        row_count: _Optional[float] = ...,
        row_parsed: _Optional[float] = ...,
        file_count: _Optional[float] = ...,
        file_size: _Optional[float] = ...,
        error_count: _Optional[int] = ...,
        pipe_received_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        status: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class FeatureExportRunSummary(_message.Message):
    __slots__ = (
        "id",
        "job_id",
        "environment_id",
        "output_directory",
        "min_timestamp_inclusive",
        "max_timestamp_exclusive",
        "completed_at",
        "submitted_at",
        "processed",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_DIRECTORY_FIELD_NUMBER: _ClassVar[int]
    MIN_TIMESTAMP_INCLUSIVE_FIELD_NUMBER: _ClassVar[int]
    MAX_TIMESTAMP_EXCLUSIVE_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_AT_FIELD_NUMBER: _ClassVar[int]
    SUBMITTED_AT_FIELD_NUMBER: _ClassVar[int]
    PROCESSED_FIELD_NUMBER: _ClassVar[int]
    id: str
    job_id: str
    environment_id: str
    output_directory: str
    min_timestamp_inclusive: _timestamp_pb2.Timestamp
    max_timestamp_exclusive: _timestamp_pb2.Timestamp
    completed_at: _timestamp_pb2.Timestamp
    submitted_at: _timestamp_pb2.Timestamp
    processed: SnowpipeFileSummary
    def __init__(
        self,
        id: _Optional[str] = ...,
        job_id: _Optional[str] = ...,
        environment_id: _Optional[str] = ...,
        output_directory: _Optional[str] = ...,
        min_timestamp_inclusive: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        max_timestamp_exclusive: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        completed_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        submitted_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        processed: _Optional[_Union[SnowpipeFileSummary, _Mapping]] = ...,
    ) -> None: ...

class FeatureExportJob(_message.Message):
    __slots__ = (
        "id",
        "environment_id",
        "schedule",
        "bucket",
        "destination_table",
        "view_format_string",
        "include_tags",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_TABLE_FIELD_NUMBER: _ClassVar[int]
    VIEW_FORMAT_STRING_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_TAGS_FIELD_NUMBER: _ClassVar[int]
    id: str
    environment_id: str
    schedule: str
    bucket: str
    destination_table: str
    view_format_string: str
    include_tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        id: _Optional[str] = ...,
        environment_id: _Optional[str] = ...,
        schedule: _Optional[str] = ...,
        bucket: _Optional[str] = ...,
        destination_table: _Optional[str] = ...,
        view_format_string: _Optional[str] = ...,
        include_tags: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class GetFeatureExportJobRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetFeatureExportJobResponse(_message.Message):
    __slots__ = ("job",)
    JOB_FIELD_NUMBER: _ClassVar[int]
    job: FeatureExportJob
    def __init__(self, job: _Optional[_Union[FeatureExportJob, _Mapping]] = ...) -> None: ...

class ListFeatureExportRunsPageToken(_message.Message):
    __slots__ = ("submitted_at",)
    SUBMITTED_AT_FIELD_NUMBER: _ClassVar[int]
    submitted_at: _timestamp_pb2.Timestamp
    def __init__(self, submitted_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ListFeatureExportRunsRequest(_message.Message):
    __slots__ = ("limit", "page_token")
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    limit: int
    page_token: str
    def __init__(self, limit: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class ListFeatureExportRunsResponse(_message.Message):
    __slots__ = ("runs", "next_page_token")
    RUNS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    runs: _containers.RepeatedCompositeFieldContainer[FeatureExportRunSummary]
    next_page_token: str
    def __init__(
        self,
        runs: _Optional[_Iterable[_Union[FeatureExportRunSummary, _Mapping]]] = ...,
        next_page_token: _Optional[str] = ...,
    ) -> None: ...

class GetFeatureExportRunRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetFeatureExportRunResponse(_message.Message):
    __slots__ = ("job", "summary", "processed")
    JOB_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    PROCESSED_FIELD_NUMBER: _ClassVar[int]
    job: FeatureExportJob
    summary: FeatureExportRunSummary
    processed: _containers.RepeatedCompositeFieldContainer[SnowpipeFile]
    def __init__(
        self,
        job: _Optional[_Union[FeatureExportJob, _Mapping]] = ...,
        summary: _Optional[_Union[FeatureExportRunSummary, _Mapping]] = ...,
        processed: _Optional[_Iterable[_Union[SnowpipeFile, _Mapping]]] = ...,
    ) -> None: ...

class UpsertExportFeatureScheduleRequest(_message.Message):
    __slots__ = ("schedule", "destination_table", "view_format_string", "include_tags")
    SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_TABLE_FIELD_NUMBER: _ClassVar[int]
    VIEW_FORMAT_STRING_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_TAGS_FIELD_NUMBER: _ClassVar[int]
    schedule: str
    destination_table: str
    view_format_string: str
    include_tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        schedule: _Optional[str] = ...,
        destination_table: _Optional[str] = ...,
        view_format_string: _Optional[str] = ...,
        include_tags: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class UpsertExportFeatureScheduleResponse(_message.Message):
    __slots__ = ("job",)
    JOB_FIELD_NUMBER: _ClassVar[int]
    job: FeatureExportJob
    def __init__(self, job: _Optional[_Union[FeatureExportJob, _Mapping]] = ...) -> None: ...
