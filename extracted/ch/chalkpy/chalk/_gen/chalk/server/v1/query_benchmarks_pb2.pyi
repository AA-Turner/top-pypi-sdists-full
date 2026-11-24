from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.flags.v1 import flags_pb2 as _flags_pb2
from chalk._gen.chalk.utils.v1 import sensitive_pb2 as _sensitive_pb2
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

class QueryBenchmarkStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    QUERY_BENCHMARK_STATUS_UNSPECIFIED: _ClassVar[QueryBenchmarkStatus]
    QUERY_BENCHMARK_STATUS_PENDING: _ClassVar[QueryBenchmarkStatus]
    QUERY_BENCHMARK_STATUS_RUNNING: _ClassVar[QueryBenchmarkStatus]
    QUERY_BENCHMARK_STATUS_SUCCEEDED: _ClassVar[QueryBenchmarkStatus]
    QUERY_BENCHMARK_STATUS_FAILED: _ClassVar[QueryBenchmarkStatus]

QUERY_BENCHMARK_STATUS_UNSPECIFIED: QueryBenchmarkStatus
QUERY_BENCHMARK_STATUS_PENDING: QueryBenchmarkStatus
QUERY_BENCHMARK_STATUS_RUNNING: QueryBenchmarkStatus
QUERY_BENCHMARK_STATUS_SUCCEEDED: QueryBenchmarkStatus
QUERY_BENCHMARK_STATUS_FAILED: QueryBenchmarkStatus

class QueryBenchmarkConfig(_message.Message):
    __slots__ = ("inputs", "outputs", "tags", "planner_options", "warmup_iterations", "duration_seconds", "sample_hz")
    class InputsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.ListValue
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.ListValue, _Mapping]] = ...
        ) -> None: ...

    class PlannerOptionsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...
        ) -> None: ...

    INPUTS_FIELD_NUMBER: _ClassVar[int]
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    PLANNER_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    WARMUP_ITERATIONS_FIELD_NUMBER: _ClassVar[int]
    DURATION_SECONDS_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_HZ_FIELD_NUMBER: _ClassVar[int]
    inputs: _containers.MessageMap[str, _struct_pb2.ListValue]
    outputs: _containers.RepeatedScalarFieldContainer[str]
    tags: _containers.RepeatedScalarFieldContainer[str]
    planner_options: _containers.MessageMap[str, _struct_pb2.Value]
    warmup_iterations: int
    duration_seconds: int
    sample_hz: int
    def __init__(
        self,
        inputs: _Optional[_Mapping[str, _struct_pb2.ListValue]] = ...,
        outputs: _Optional[_Iterable[str]] = ...,
        tags: _Optional[_Iterable[str]] = ...,
        planner_options: _Optional[_Mapping[str, _struct_pb2.Value]] = ...,
        warmup_iterations: _Optional[int] = ...,
        duration_seconds: _Optional[int] = ...,
        sample_hz: _Optional[int] = ...,
    ) -> None: ...

class QueryBenchmarkArtifacts(_message.Message):
    __slots__ = ("summary_url", "flamegraph_url", "folded_stacks_url", "report_url")
    SUMMARY_URL_FIELD_NUMBER: _ClassVar[int]
    FLAMEGRAPH_URL_FIELD_NUMBER: _ClassVar[int]
    FOLDED_STACKS_URL_FIELD_NUMBER: _ClassVar[int]
    REPORT_URL_FIELD_NUMBER: _ClassVar[int]
    summary_url: str
    flamegraph_url: str
    folded_stacks_url: str
    report_url: str
    def __init__(
        self,
        summary_url: _Optional[str] = ...,
        flamegraph_url: _Optional[str] = ...,
        folded_stacks_url: _Optional[str] = ...,
        report_url: _Optional[str] = ...,
    ) -> None: ...

class QueryBenchmark(_message.Message):
    __slots__ = (
        "id",
        "status",
        "config",
        "deployment_id",
        "created_at",
        "started_at",
        "completed_at",
        "error_message",
        "summary",
        "artifacts",
        "created_by",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_AT_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    ARTIFACTS_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    id: str
    status: QueryBenchmarkStatus
    config: QueryBenchmarkConfig
    deployment_id: str
    created_at: _timestamp_pb2.Timestamp
    started_at: _timestamp_pb2.Timestamp
    completed_at: _timestamp_pb2.Timestamp
    error_message: str
    summary: _struct_pb2.Struct
    artifacts: QueryBenchmarkArtifacts
    created_by: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        status: _Optional[_Union[QueryBenchmarkStatus, str]] = ...,
        config: _Optional[_Union[QueryBenchmarkConfig, _Mapping]] = ...,
        deployment_id: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        started_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        completed_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        error_message: _Optional[str] = ...,
        summary: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
        artifacts: _Optional[_Union[QueryBenchmarkArtifacts, _Mapping]] = ...,
        created_by: _Optional[str] = ...,
    ) -> None: ...

class StartQueryBenchmarkRequest(_message.Message):
    __slots__ = ("config",)
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    config: QueryBenchmarkConfig
    def __init__(self, config: _Optional[_Union[QueryBenchmarkConfig, _Mapping]] = ...) -> None: ...

class StartQueryBenchmarkResponse(_message.Message):
    __slots__ = ("benchmark",)
    BENCHMARK_FIELD_NUMBER: _ClassVar[int]
    benchmark: QueryBenchmark
    def __init__(self, benchmark: _Optional[_Union[QueryBenchmark, _Mapping]] = ...) -> None: ...

class GetQueryBenchmarkRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetQueryBenchmarkResponse(_message.Message):
    __slots__ = ("benchmark",)
    BENCHMARK_FIELD_NUMBER: _ClassVar[int]
    benchmark: QueryBenchmark
    def __init__(self, benchmark: _Optional[_Union[QueryBenchmark, _Mapping]] = ...) -> None: ...

class ListQueryBenchmarksRequest(_message.Message):
    __slots__ = ("limit", "cursor")
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    limit: int
    cursor: str
    def __init__(self, limit: _Optional[int] = ..., cursor: _Optional[str] = ...) -> None: ...

class ListQueryBenchmarksResponse(_message.Message):
    __slots__ = ("benchmarks", "next_cursor")
    BENCHMARKS_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    benchmarks: _containers.RepeatedCompositeFieldContainer[QueryBenchmark]
    next_cursor: str
    def __init__(
        self,
        benchmarks: _Optional[_Iterable[_Union[QueryBenchmark, _Mapping]]] = ...,
        next_cursor: _Optional[str] = ...,
    ) -> None: ...
