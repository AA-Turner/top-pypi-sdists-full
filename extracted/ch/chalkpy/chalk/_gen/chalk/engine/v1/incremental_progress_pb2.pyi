from chalk._gen.chalk.aggregate.v1 import backfill_pb2 as _backfill_pb2
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

class AggregateBackfillIncrementalProgressRequest(_message.Message):
    __slots__ = ("features", "store_offline", "store_online")
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    STORE_OFFLINE_FIELD_NUMBER: _ClassVar[int]
    STORE_ONLINE_FIELD_NUMBER: _ClassVar[int]
    features: _containers.RepeatedScalarFieldContainer[str]
    store_offline: bool
    store_online: bool
    def __init__(
        self, features: _Optional[_Iterable[str]] = ..., store_offline: bool = ..., store_online: bool = ...
    ) -> None: ...

class AggregateBackfillIncrementalProgressIdentifier(_message.Message):
    __slots__ = ("aggregate_groups",)
    AGGREGATE_GROUPS_FIELD_NUMBER: _ClassVar[int]
    aggregate_groups: _containers.RepeatedCompositeFieldContainer[AggregateBackfillIncrementalProgressRequest]
    def __init__(
        self,
        aggregate_groups: _Optional[_Iterable[_Union[AggregateBackfillIncrementalProgressRequest, _Mapping]]] = ...,
    ) -> None: ...

class MaterializedFeatureViewFillProgressIdentifier(_message.Message):
    __slots__ = ("feature_namespace",)
    FEATURE_NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    feature_namespace: str
    def __init__(self, feature_namespace: _Optional[str] = ...) -> None: ...

class GetIncrementalProgressRequest(_message.Message):
    __slots__ = ("resolver_fqn", "query_name", "aggregate_backfill", "materialized_feature_view_fill")
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    QUERY_NAME_FIELD_NUMBER: _ClassVar[int]
    AGGREGATE_BACKFILL_FIELD_NUMBER: _ClassVar[int]
    MATERIALIZED_FEATURE_VIEW_FILL_FIELD_NUMBER: _ClassVar[int]
    resolver_fqn: str
    query_name: str
    aggregate_backfill: AggregateBackfillIncrementalProgressIdentifier
    materialized_feature_view_fill: MaterializedFeatureViewFillProgressIdentifier
    def __init__(
        self,
        resolver_fqn: _Optional[str] = ...,
        query_name: _Optional[str] = ...,
        aggregate_backfill: _Optional[_Union[AggregateBackfillIncrementalProgressIdentifier, _Mapping]] = ...,
        materialized_feature_view_fill: _Optional[
            _Union[MaterializedFeatureViewFillProgressIdentifier, _Mapping]
        ] = ...,
    ) -> None: ...

class AggregateBackfillIncrementalProgress(_message.Message):
    __slots__ = ("features", "storage_targets", "max_ingested_timestamp", "last_execution_timestamp")
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    STORAGE_TARGETS_FIELD_NUMBER: _ClassVar[int]
    MAX_INGESTED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    LAST_EXECUTION_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    features: _containers.RepeatedScalarFieldContainer[str]
    storage_targets: _containers.RepeatedScalarFieldContainer[_backfill_pb2.AggregateBackfillTarget]
    max_ingested_timestamp: _timestamp_pb2.Timestamp
    last_execution_timestamp: _timestamp_pb2.Timestamp
    def __init__(
        self,
        features: _Optional[_Iterable[str]] = ...,
        storage_targets: _Optional[_Iterable[_Union[_backfill_pb2.AggregateBackfillTarget, str]]] = ...,
        max_ingested_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        last_execution_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class GetIncrementalProgressResponse(_message.Message):
    __slots__ = (
        "environment_id",
        "resolver_fqn",
        "query_name",
        "max_ingested_timestamp",
        "last_execution_timestamp",
        "aggregate_groups",
    )
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    QUERY_NAME_FIELD_NUMBER: _ClassVar[int]
    MAX_INGESTED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    LAST_EXECUTION_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    AGGREGATE_GROUPS_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    resolver_fqn: str
    query_name: str
    max_ingested_timestamp: _timestamp_pb2.Timestamp
    last_execution_timestamp: _timestamp_pb2.Timestamp
    aggregate_groups: _containers.RepeatedCompositeFieldContainer[AggregateBackfillIncrementalProgress]
    def __init__(
        self,
        environment_id: _Optional[str] = ...,
        resolver_fqn: _Optional[str] = ...,
        query_name: _Optional[str] = ...,
        max_ingested_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        last_execution_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        aggregate_groups: _Optional[_Iterable[_Union[AggregateBackfillIncrementalProgress, _Mapping]]] = ...,
    ) -> None: ...

class SetIncrementalProgressRequest(_message.Message):
    __slots__ = (
        "resolver_fqn",
        "query_name",
        "aggregate_backfill",
        "materialized_feature_view_fill",
        "max_ingested_timestamp",
        "last_execution_timestamp",
    )
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    QUERY_NAME_FIELD_NUMBER: _ClassVar[int]
    AGGREGATE_BACKFILL_FIELD_NUMBER: _ClassVar[int]
    MATERIALIZED_FEATURE_VIEW_FILL_FIELD_NUMBER: _ClassVar[int]
    MAX_INGESTED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    LAST_EXECUTION_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    resolver_fqn: str
    query_name: str
    aggregate_backfill: AggregateBackfillIncrementalProgressIdentifier
    materialized_feature_view_fill: MaterializedFeatureViewFillProgressIdentifier
    max_ingested_timestamp: _timestamp_pb2.Timestamp
    last_execution_timestamp: _timestamp_pb2.Timestamp
    def __init__(
        self,
        resolver_fqn: _Optional[str] = ...,
        query_name: _Optional[str] = ...,
        aggregate_backfill: _Optional[_Union[AggregateBackfillIncrementalProgressIdentifier, _Mapping]] = ...,
        materialized_feature_view_fill: _Optional[
            _Union[MaterializedFeatureViewFillProgressIdentifier, _Mapping]
        ] = ...,
        max_ingested_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        last_execution_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class SetIncrementalProgressResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DeleteIncrementalProgressRequest(_message.Message):
    __slots__ = ("resolver_fqn", "query_name", "aggregate_backfill", "materialized_feature_view_fill")
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    QUERY_NAME_FIELD_NUMBER: _ClassVar[int]
    AGGREGATE_BACKFILL_FIELD_NUMBER: _ClassVar[int]
    MATERIALIZED_FEATURE_VIEW_FILL_FIELD_NUMBER: _ClassVar[int]
    resolver_fqn: str
    query_name: str
    aggregate_backfill: AggregateBackfillIncrementalProgressIdentifier
    materialized_feature_view_fill: MaterializedFeatureViewFillProgressIdentifier
    def __init__(
        self,
        resolver_fqn: _Optional[str] = ...,
        query_name: _Optional[str] = ...,
        aggregate_backfill: _Optional[_Union[AggregateBackfillIncrementalProgressIdentifier, _Mapping]] = ...,
        materialized_feature_view_fill: _Optional[
            _Union[MaterializedFeatureViewFillProgressIdentifier, _Mapping]
        ] = ...,
    ) -> None: ...

class DeleteIncrementalProgressResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
