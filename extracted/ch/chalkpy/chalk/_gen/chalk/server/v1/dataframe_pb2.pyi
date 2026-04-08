from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.common.v1 import chalk_error_pb2 as _chalk_error_pb2
from chalk._gen.chalk.dataframe.v1 import dataframe_pb2 as _dataframe_pb2
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

class DataFrameRunStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DATA_FRAME_RUN_STATUS_UNSPECIFIED: _ClassVar[DataFrameRunStatus]
    DATA_FRAME_RUN_STATUS_QUEUED: _ClassVar[DataFrameRunStatus]
    DATA_FRAME_RUN_STATUS_WORKING: _ClassVar[DataFrameRunStatus]
    DATA_FRAME_RUN_STATUS_COMPLETED: _ClassVar[DataFrameRunStatus]
    DATA_FRAME_RUN_STATUS_FAILED: _ClassVar[DataFrameRunStatus]
    DATA_FRAME_RUN_STATUS_CANCELED: _ClassVar[DataFrameRunStatus]

DATA_FRAME_RUN_STATUS_UNSPECIFIED: DataFrameRunStatus
DATA_FRAME_RUN_STATUS_QUEUED: DataFrameRunStatus
DATA_FRAME_RUN_STATUS_WORKING: DataFrameRunStatus
DATA_FRAME_RUN_STATUS_COMPLETED: DataFrameRunStatus
DATA_FRAME_RUN_STATUS_FAILED: DataFrameRunStatus
DATA_FRAME_RUN_STATUS_CANCELED: DataFrameRunStatus

class ExecuteDataFramePlanRequest(_message.Message):
    __slots__ = ("plan", "compressed_plan_uri_prefix", "correlation_id", "resource_group")
    PLAN_FIELD_NUMBER: _ClassVar[int]
    COMPRESSED_PLAN_URI_PREFIX_FIELD_NUMBER: _ClassVar[int]
    CORRELATION_ID_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_GROUP_FIELD_NUMBER: _ClassVar[int]
    plan: _dataframe_pb2.DataFramePlan
    compressed_plan_uri_prefix: str
    correlation_id: str
    resource_group: str
    def __init__(
        self,
        plan: _Optional[_Union[_dataframe_pb2.DataFramePlan, _Mapping]] = ...,
        compressed_plan_uri_prefix: _Optional[str] = ...,
        correlation_id: _Optional[str] = ...,
        resource_group: _Optional[str] = ...,
    ) -> None: ...

class ExecuteDataFramePlanResponse(_message.Message):
    __slots__ = ("operation_id", "run", "errors")
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    RUN_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    run: DataFrameRun
    errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    def __init__(
        self,
        operation_id: _Optional[str] = ...,
        run: _Optional[_Union[DataFrameRun, _Mapping]] = ...,
        errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...,
    ) -> None: ...

class GetDataFramePlanUploadUrlRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetDataFramePlanUploadUrlResponse(_message.Message):
    __slots__ = ("upload_url", "compressed_plan_uri_prefix")
    UPLOAD_URL_FIELD_NUMBER: _ClassVar[int]
    COMPRESSED_PLAN_URI_PREFIX_FIELD_NUMBER: _ClassVar[int]
    upload_url: str
    compressed_plan_uri_prefix: str
    def __init__(self, upload_url: _Optional[str] = ..., compressed_plan_uri_prefix: _Optional[str] = ...) -> None: ...

class GetDataFrameRunRequest(_message.Message):
    __slots__ = ("operation_id",)
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    def __init__(self, operation_id: _Optional[str] = ...) -> None: ...

class GetDataFrameRunStatusRequest(_message.Message):
    __slots__ = ("operation_id",)
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    def __init__(self, operation_id: _Optional[str] = ...) -> None: ...

class GetDataFrameRunStatusResponse(_message.Message):
    __slots__ = ("status", "output_uri_prefix", "finalized_at")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_URI_PREFIX_FIELD_NUMBER: _ClassVar[int]
    FINALIZED_AT_FIELD_NUMBER: _ClassVar[int]
    status: DataFrameRunStatus
    output_uri_prefix: str
    finalized_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        status: _Optional[_Union[DataFrameRunStatus, str]] = ...,
        output_uri_prefix: _Optional[str] = ...,
        finalized_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class DataFrameRunShard(_message.Message):
    __slots__ = ("operation_id", "shard_id", "status", "finalized_at", "updated_at", "compressed_plan_uri_prefix")
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    SHARD_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    FINALIZED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    COMPRESSED_PLAN_URI_PREFIX_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    shard_id: int
    status: DataFrameRunStatus
    finalized_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    compressed_plan_uri_prefix: str
    def __init__(
        self,
        operation_id: _Optional[str] = ...,
        shard_id: _Optional[int] = ...,
        status: _Optional[_Union[DataFrameRunStatus, str]] = ...,
        finalized_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        compressed_plan_uri_prefix: _Optional[str] = ...,
    ) -> None: ...

class DataFrameRun(_message.Message):
    __slots__ = (
        "operation_id",
        "status",
        "output_uri_prefix",
        "agent_id",
        "finalized_at",
        "updated_at",
        "correlation_id",
        "external_id",
        "branch_name",
        "resource_group",
        "meta_data",
        "compressed_plan_uri_prefix",
    )
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_URI_PREFIX_FIELD_NUMBER: _ClassVar[int]
    AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    FINALIZED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    CORRELATION_ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    BRANCH_NAME_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_GROUP_FIELD_NUMBER: _ClassVar[int]
    META_DATA_FIELD_NUMBER: _ClassVar[int]
    COMPRESSED_PLAN_URI_PREFIX_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    status: DataFrameRunStatus
    output_uri_prefix: str
    agent_id: str
    finalized_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    correlation_id: str
    external_id: str
    branch_name: str
    resource_group: str
    meta_data: _struct_pb2.Struct
    compressed_plan_uri_prefix: str
    def __init__(
        self,
        operation_id: _Optional[str] = ...,
        status: _Optional[_Union[DataFrameRunStatus, str]] = ...,
        output_uri_prefix: _Optional[str] = ...,
        agent_id: _Optional[str] = ...,
        finalized_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        correlation_id: _Optional[str] = ...,
        external_id: _Optional[str] = ...,
        branch_name: _Optional[str] = ...,
        resource_group: _Optional[str] = ...,
        meta_data: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
        compressed_plan_uri_prefix: _Optional[str] = ...,
    ) -> None: ...

class GetDataFrameRunResponse(_message.Message):
    __slots__ = ("run", "errors")
    RUN_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    run: DataFrameRun
    errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    def __init__(
        self,
        run: _Optional[_Union[DataFrameRun, _Mapping]] = ...,
        errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...,
    ) -> None: ...
