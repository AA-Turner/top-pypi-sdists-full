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

class RecomputeSettings(_message.Message):
    __slots__ = ("feature_fqns", "all_features")
    FEATURE_FQNS_FIELD_NUMBER: _ClassVar[int]
    ALL_FEATURES_FIELD_NUMBER: _ClassVar[int]
    feature_fqns: _containers.RepeatedScalarFieldContainer[str]
    all_features: bool
    def __init__(self, feature_fqns: _Optional[_Iterable[str]] = ..., all_features: bool = ...) -> None: ...

class CronQuery(_message.Message):
    __slots__ = (
        "name",
        "cron",
        "file_name",
        "output",
        "max_samples",
        "recompute",
        "lower_bound",
        "upper_bound",
        "tags",
        "required_resolver_tags",
        "store_online",
        "store_offline",
        "incremental_sources",
        "resource_group",
        "planner_options",
    )
    class PlannerOptionsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    NAME_FIELD_NUMBER: _ClassVar[int]
    CRON_FIELD_NUMBER: _ClassVar[int]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    MAX_SAMPLES_FIELD_NUMBER: _ClassVar[int]
    RECOMPUTE_FIELD_NUMBER: _ClassVar[int]
    LOWER_BOUND_FIELD_NUMBER: _ClassVar[int]
    UPPER_BOUND_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_RESOLVER_TAGS_FIELD_NUMBER: _ClassVar[int]
    STORE_ONLINE_FIELD_NUMBER: _ClassVar[int]
    STORE_OFFLINE_FIELD_NUMBER: _ClassVar[int]
    INCREMENTAL_SOURCES_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_GROUP_FIELD_NUMBER: _ClassVar[int]
    PLANNER_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    name: str
    cron: str
    file_name: str
    output: _containers.RepeatedScalarFieldContainer[str]
    max_samples: int
    recompute: RecomputeSettings
    lower_bound: _timestamp_pb2.Timestamp
    upper_bound: _timestamp_pb2.Timestamp
    tags: _containers.RepeatedScalarFieldContainer[str]
    required_resolver_tags: _containers.RepeatedScalarFieldContainer[str]
    store_online: bool
    store_offline: bool
    incremental_sources: _containers.RepeatedScalarFieldContainer[str]
    resource_group: str
    planner_options: _containers.ScalarMap[str, str]
    def __init__(
        self,
        name: _Optional[str] = ...,
        cron: _Optional[str] = ...,
        file_name: _Optional[str] = ...,
        output: _Optional[_Iterable[str]] = ...,
        max_samples: _Optional[int] = ...,
        recompute: _Optional[_Union[RecomputeSettings, _Mapping]] = ...,
        lower_bound: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        upper_bound: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        tags: _Optional[_Iterable[str]] = ...,
        required_resolver_tags: _Optional[_Iterable[str]] = ...,
        store_online: bool = ...,
        store_offline: bool = ...,
        incremental_sources: _Optional[_Iterable[str]] = ...,
        resource_group: _Optional[str] = ...,
        planner_options: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...
