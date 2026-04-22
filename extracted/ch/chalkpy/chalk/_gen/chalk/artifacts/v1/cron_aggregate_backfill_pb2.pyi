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

class CronAggregateBackfillTarget(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CRON_AGGREGATE_BACKFILL_TARGET_UNSPECIFIED: _ClassVar[CronAggregateBackfillTarget]
    CRON_AGGREGATE_BACKFILL_TARGET_ONLINE: _ClassVar[CronAggregateBackfillTarget]
    CRON_AGGREGATE_BACKFILL_TARGET_OFFLINE: _ClassVar[CronAggregateBackfillTarget]

CRON_AGGREGATE_BACKFILL_TARGET_UNSPECIFIED: CronAggregateBackfillTarget
CRON_AGGREGATE_BACKFILL_TARGET_ONLINE: CronAggregateBackfillTarget
CRON_AGGREGATE_BACKFILL_TARGET_OFFLINE: CronAggregateBackfillTarget

class CronAggregateBackfill(_message.Message):
    __slots__ = (
        "name",
        "schedule",
        "file_name",
        "features",
        "resolvers",
        "query_tags",
        "target",
        "resource_group",
        "lower_bound",
        "upper_bound",
    )
    NAME_FIELD_NUMBER: _ClassVar[int]
    SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    RESOLVERS_FIELD_NUMBER: _ClassVar[int]
    QUERY_TAGS_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_GROUP_FIELD_NUMBER: _ClassVar[int]
    LOWER_BOUND_FIELD_NUMBER: _ClassVar[int]
    UPPER_BOUND_FIELD_NUMBER: _ClassVar[int]
    name: str
    schedule: str
    file_name: str
    features: _containers.RepeatedScalarFieldContainer[str]
    resolvers: _containers.RepeatedScalarFieldContainer[str]
    query_tags: _containers.RepeatedScalarFieldContainer[str]
    target: CronAggregateBackfillTarget
    resource_group: str
    lower_bound: _timestamp_pb2.Timestamp
    upper_bound: _timestamp_pb2.Timestamp
    def __init__(
        self,
        name: _Optional[str] = ...,
        schedule: _Optional[str] = ...,
        file_name: _Optional[str] = ...,
        features: _Optional[_Iterable[str]] = ...,
        resolvers: _Optional[_Iterable[str]] = ...,
        query_tags: _Optional[_Iterable[str]] = ...,
        target: _Optional[_Union[CronAggregateBackfillTarget, str]] = ...,
        resource_group: _Optional[str] = ...,
        lower_bound: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        upper_bound: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...
