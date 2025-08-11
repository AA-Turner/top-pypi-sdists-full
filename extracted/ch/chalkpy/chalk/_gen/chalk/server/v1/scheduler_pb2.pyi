from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.server.v1 import scheduled_query_run_pb2 as _scheduled_query_run_pb2
from google.protobuf import struct_pb2 as _struct_pb2
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

class ManualTriggerScheduledQueryRequest(_message.Message):
    __slots__ = ("cron_query_id", "planner_options", "incremental_resolvers", "max_samples", "env_overrides")
    class PlannerOptionsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...
        ) -> None: ...

    class EnvOverridesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    CRON_QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    PLANNER_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    INCREMENTAL_RESOLVERS_FIELD_NUMBER: _ClassVar[int]
    MAX_SAMPLES_FIELD_NUMBER: _ClassVar[int]
    ENV_OVERRIDES_FIELD_NUMBER: _ClassVar[int]
    cron_query_id: int
    planner_options: _containers.MessageMap[str, _struct_pb2.Value]
    incremental_resolvers: _containers.RepeatedScalarFieldContainer[str]
    max_samples: int
    env_overrides: _containers.ScalarMap[str, str]
    def __init__(
        self,
        cron_query_id: _Optional[int] = ...,
        planner_options: _Optional[_Mapping[str, _struct_pb2.Value]] = ...,
        incremental_resolvers: _Optional[_Iterable[str]] = ...,
        max_samples: _Optional[int] = ...,
        env_overrides: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...

class ManualTriggerScheduledQueryResponse(_message.Message):
    __slots__ = ("scheduled_query_run",)
    SCHEDULED_QUERY_RUN_FIELD_NUMBER: _ClassVar[int]
    scheduled_query_run: _scheduled_query_run_pb2.ScheduledQueryRun
    def __init__(
        self, scheduled_query_run: _Optional[_Union[_scheduled_query_run_pb2.ScheduledQueryRun, _Mapping]] = ...
    ) -> None: ...
