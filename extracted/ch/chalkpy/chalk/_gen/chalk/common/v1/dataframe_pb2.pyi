from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DataFrameRunJobRequest(_message.Message):
    __slots__ = (
        "operation_id",
        "correlation_id",
        "compressed_plan_uri_prefix",
        "shard_operation_id",
        "update_performance_summary_interval_secs",
    )
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    CORRELATION_ID_FIELD_NUMBER: _ClassVar[int]
    COMPRESSED_PLAN_URI_PREFIX_FIELD_NUMBER: _ClassVar[int]
    SHARD_OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    UPDATE_PERFORMANCE_SUMMARY_INTERVAL_SECS_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    correlation_id: str
    compressed_plan_uri_prefix: str
    shard_operation_id: str
    update_performance_summary_interval_secs: float
    def __init__(
        self,
        operation_id: _Optional[str] = ...,
        correlation_id: _Optional[str] = ...,
        compressed_plan_uri_prefix: _Optional[str] = ...,
        shard_operation_id: _Optional[str] = ...,
        update_performance_summary_interval_secs: _Optional[float] = ...,
    ) -> None: ...
