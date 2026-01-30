from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.common.v1 import online_query_pb2 as _online_query_pb2
from chalk._gen.chalk.server.v1 import builder_pb2 as _builder_pb2
from google.protobuf import duration_pb2 as _duration_pb2
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

class BenchmarkStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BENCHMARK_STATUS_UNSPECIFIED: _ClassVar[BenchmarkStatus]
    BENCHMARK_STATUS_QUEUED: _ClassVar[BenchmarkStatus]
    BENCHMARK_STATUS_WORKING: _ClassVar[BenchmarkStatus]
    BENCHMARK_STATUS_COMPLETED: _ClassVar[BenchmarkStatus]
    BENCHMARK_STATUS_FAILED: _ClassVar[BenchmarkStatus]
    BENCHMARK_STATUS_SKIPPED: _ClassVar[BenchmarkStatus]
    BENCHMARK_STATUS_CANCELED: _ClassVar[BenchmarkStatus]

BENCHMARK_STATUS_UNSPECIFIED: BenchmarkStatus
BENCHMARK_STATUS_QUEUED: BenchmarkStatus
BENCHMARK_STATUS_WORKING: BenchmarkStatus
BENCHMARK_STATUS_COMPLETED: BenchmarkStatus
BENCHMARK_STATUS_FAILED: BenchmarkStatus
BENCHMARK_STATUS_SKIPPED: BenchmarkStatus
BENCHMARK_STATUS_CANCELED: BenchmarkStatus

class InputFeatures(_message.Message):
    __slots__ = ("input_features",)
    INPUT_FEATURES_FIELD_NUMBER: _ClassVar[int]
    input_features: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, input_features: _Optional[_Iterable[str]] = ...) -> None: ...

class NamedQueryRequest(_message.Message):
    __slots__ = ("query_name", "query_version")
    QUERY_NAME_FIELD_NUMBER: _ClassVar[int]
    QUERY_VERSION_FIELD_NUMBER: _ClassVar[int]
    query_name: str
    query_version: str
    def __init__(self, query_name: _Optional[str] = ..., query_version: _Optional[str] = ...) -> None: ...

class SimpleOnlineQueryBulkRequest(_message.Message):
    __slots__ = ("input_features", "input_features_list", "input_file", "output_features", "named_query_request")
    INPUT_FEATURES_FIELD_NUMBER: _ClassVar[int]
    INPUT_FEATURES_LIST_FIELD_NUMBER: _ClassVar[int]
    INPUT_FILE_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FEATURES_FIELD_NUMBER: _ClassVar[int]
    NAMED_QUERY_REQUEST_FIELD_NUMBER: _ClassVar[int]
    input_features: _containers.RepeatedScalarFieldContainer[str]
    input_features_list: InputFeatures
    input_file: str
    output_features: _containers.RepeatedScalarFieldContainer[str]
    named_query_request: NamedQueryRequest
    def __init__(
        self,
        input_features: _Optional[_Iterable[str]] = ...,
        input_features_list: _Optional[_Union[InputFeatures, _Mapping]] = ...,
        input_file: _Optional[str] = ...,
        output_features: _Optional[_Iterable[str]] = ...,
        named_query_request: _Optional[_Union[NamedQueryRequest, _Mapping]] = ...,
    ) -> None: ...

class ContainerSpec(_message.Message):
    __slots__ = ("request", "limit")
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    request: _builder_pb2.KubeResourceConfig
    limit: _builder_pb2.KubeResourceConfig
    def __init__(
        self,
        request: _Optional[_Union[_builder_pb2.KubeResourceConfig, _Mapping]] = ...,
        limit: _Optional[_Union[_builder_pb2.KubeResourceConfig, _Mapping]] = ...,
    ) -> None: ...

class CreateBenchmarkRequest(_message.Message):
    __slots__ = (
        "warmup_qps",
        "warmup_duration",
        "qps",
        "duration",
        "query_bulk",
        "simple_query_bulk",
        "percentiles",
        "image_override",
        "warmup_container_spec",
        "container_spec",
    )
    WARMUP_QPS_FIELD_NUMBER: _ClassVar[int]
    WARMUP_DURATION_FIELD_NUMBER: _ClassVar[int]
    QPS_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    QUERY_BULK_FIELD_NUMBER: _ClassVar[int]
    SIMPLE_QUERY_BULK_FIELD_NUMBER: _ClassVar[int]
    PERCENTILES_FIELD_NUMBER: _ClassVar[int]
    IMAGE_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    WARMUP_CONTAINER_SPEC_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_SPEC_FIELD_NUMBER: _ClassVar[int]
    warmup_qps: int
    warmup_duration: _duration_pb2.Duration
    qps: int
    duration: _duration_pb2.Duration
    query_bulk: _online_query_pb2.OnlineQueryBulkRequest
    simple_query_bulk: SimpleOnlineQueryBulkRequest
    percentiles: _containers.RepeatedScalarFieldContainer[int]
    image_override: str
    warmup_container_spec: ContainerSpec
    container_spec: ContainerSpec
    def __init__(
        self,
        warmup_qps: _Optional[int] = ...,
        warmup_duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        qps: _Optional[int] = ...,
        duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        query_bulk: _Optional[_Union[_online_query_pb2.OnlineQueryBulkRequest, _Mapping]] = ...,
        simple_query_bulk: _Optional[_Union[SimpleOnlineQueryBulkRequest, _Mapping]] = ...,
        percentiles: _Optional[_Iterable[int]] = ...,
        image_override: _Optional[str] = ...,
        warmup_container_spec: _Optional[_Union[ContainerSpec, _Mapping]] = ...,
        container_spec: _Optional[_Union[ContainerSpec, _Mapping]] = ...,
    ) -> None: ...

class CreateBenchmarkResponse(_message.Message):
    __slots__ = ("status", "benchmark_id")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    BENCHMARK_ID_FIELD_NUMBER: _ClassVar[int]
    status: BenchmarkStatus
    benchmark_id: str
    def __init__(
        self, status: _Optional[_Union[BenchmarkStatus, str]] = ..., benchmark_id: _Optional[str] = ...
    ) -> None: ...

class BenchmarkInputFile(_message.Message):
    __slots__ = ("name", "size", "updated_at")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    name: str
    size: int
    updated_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        name: _Optional[str] = ...,
        size: _Optional[int] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class GetAvailableInputFilesRequest(_message.Message):
    __slots__ = ("prefix",)
    PREFIX_FIELD_NUMBER: _ClassVar[int]
    prefix: str
    def __init__(self, prefix: _Optional[str] = ...) -> None: ...

class GetAvailableInputFilesResponse(_message.Message):
    __slots__ = ("input_files",)
    INPUT_FILES_FIELD_NUMBER: _ClassVar[int]
    input_files: _containers.RepeatedCompositeFieldContainer[BenchmarkInputFile]
    def __init__(self, input_files: _Optional[_Iterable[_Union[BenchmarkInputFile, _Mapping]]] = ...) -> None: ...

class GetInputFileUploadUrlsRequest(_message.Message):
    __slots__ = ("input_files",)
    INPUT_FILES_FIELD_NUMBER: _ClassVar[int]
    input_files: _containers.RepeatedCompositeFieldContainer[BenchmarkInputFile]
    def __init__(self, input_files: _Optional[_Iterable[_Union[BenchmarkInputFile, _Mapping]]] = ...) -> None: ...

class GetInputFileUploadUrlsResponse(_message.Message):
    __slots__ = ("presigned_urls",)
    PRESIGNED_URLS_FIELD_NUMBER: _ClassVar[int]
    presigned_urls: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, presigned_urls: _Optional[_Iterable[str]] = ...) -> None: ...

class GetAvailableResultFilesRequest(_message.Message):
    __slots__ = ("prefix",)
    PREFIX_FIELD_NUMBER: _ClassVar[int]
    prefix: str
    def __init__(self, prefix: _Optional[str] = ...) -> None: ...

class GetAvailableResultFilesResponse(_message.Message):
    __slots__ = ("result_files",)
    RESULT_FILES_FIELD_NUMBER: _ClassVar[int]
    result_files: _containers.RepeatedCompositeFieldContainer[BenchmarkInputFile]
    def __init__(self, result_files: _Optional[_Iterable[_Union[BenchmarkInputFile, _Mapping]]] = ...) -> None: ...

class GetResultFileUrlsRequest(_message.Message):
    __slots__ = ("file_names",)
    FILE_NAMES_FIELD_NUMBER: _ClassVar[int]
    file_names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, file_names: _Optional[_Iterable[str]] = ...) -> None: ...

class GetResultFileUrlsResponse(_message.Message):
    __slots__ = ("presigned_urls",)
    PRESIGNED_URLS_FIELD_NUMBER: _ClassVar[int]
    presigned_urls: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, presigned_urls: _Optional[_Iterable[str]] = ...) -> None: ...
