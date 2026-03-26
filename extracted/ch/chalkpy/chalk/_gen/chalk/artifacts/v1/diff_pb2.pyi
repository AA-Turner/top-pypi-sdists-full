from chalk._gen.chalk.artifacts.v1 import cdc_pb2 as _cdc_pb2
from chalk._gen.chalk.artifacts.v1 import chart_pb2 as _chart_pb2
from chalk._gen.chalk.artifacts.v1 import cron_query_pb2 as _cron_query_pb2
from chalk._gen.chalk.graph.v1 import graph_pb2 as _graph_pb2
from chalk._gen.chalk.graph.v2 import sources_pb2 as _sources_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
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

class ExportDiff(_message.Message):
    __slots__ = (
        "feature_sets",
        "resolvers",
        "stream_resolvers",
        "sink_resolvers",
        "named_queries",
        "database_sources_v2",
        "stream_sources_v2",
        "model_references",
        "online_store_configs",
        "database_source_groups",
        "crons",
        "charts",
        "cdc_sources",
    )
    FEATURE_SETS_FIELD_NUMBER: _ClassVar[int]
    RESOLVERS_FIELD_NUMBER: _ClassVar[int]
    STREAM_RESOLVERS_FIELD_NUMBER: _ClassVar[int]
    SINK_RESOLVERS_FIELD_NUMBER: _ClassVar[int]
    NAMED_QUERIES_FIELD_NUMBER: _ClassVar[int]
    DATABASE_SOURCES_V2_FIELD_NUMBER: _ClassVar[int]
    STREAM_SOURCES_V2_FIELD_NUMBER: _ClassVar[int]
    MODEL_REFERENCES_FIELD_NUMBER: _ClassVar[int]
    ONLINE_STORE_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    DATABASE_SOURCE_GROUPS_FIELD_NUMBER: _ClassVar[int]
    CRONS_FIELD_NUMBER: _ClassVar[int]
    CHARTS_FIELD_NUMBER: _ClassVar[int]
    CDC_SOURCES_FIELD_NUMBER: _ClassVar[int]
    feature_sets: FeatureSetCollectionDiff
    resolvers: ResolverCollectionDiff
    stream_resolvers: StreamResolverCollectionDiff
    sink_resolvers: SinkResolverCollectionDiff
    named_queries: NamedQueryCollectionDiff
    database_sources_v2: DatabaseSourceCollectionDiff
    stream_sources_v2: StreamSourceCollectionDiff
    model_references: ModelReferenceCollectionDiff
    online_store_configs: OnlineStoreConfigCollectionDiff
    database_source_groups: DatabaseSourceGroupCollectionDiff
    crons: CronQueryCollectionDiff
    charts: ChartCollectionDiff
    cdc_sources: CDCSourceCollectionDiff
    def __init__(
        self,
        feature_sets: _Optional[_Union[FeatureSetCollectionDiff, _Mapping]] = ...,
        resolvers: _Optional[_Union[ResolverCollectionDiff, _Mapping]] = ...,
        stream_resolvers: _Optional[_Union[StreamResolverCollectionDiff, _Mapping]] = ...,
        sink_resolvers: _Optional[_Union[SinkResolverCollectionDiff, _Mapping]] = ...,
        named_queries: _Optional[_Union[NamedQueryCollectionDiff, _Mapping]] = ...,
        database_sources_v2: _Optional[_Union[DatabaseSourceCollectionDiff, _Mapping]] = ...,
        stream_sources_v2: _Optional[_Union[StreamSourceCollectionDiff, _Mapping]] = ...,
        model_references: _Optional[_Union[ModelReferenceCollectionDiff, _Mapping]] = ...,
        online_store_configs: _Optional[_Union[OnlineStoreConfigCollectionDiff, _Mapping]] = ...,
        database_source_groups: _Optional[_Union[DatabaseSourceGroupCollectionDiff, _Mapping]] = ...,
        crons: _Optional[_Union[CronQueryCollectionDiff, _Mapping]] = ...,
        charts: _Optional[_Union[ChartCollectionDiff, _Mapping]] = ...,
        cdc_sources: _Optional[_Union[CDCSourceCollectionDiff, _Mapping]] = ...,
    ) -> None: ...

class FeatureSetCollectionDiff(_message.Message):
    __slots__ = ("added", "removed", "modified")
    ADDED_FIELD_NUMBER: _ClassVar[int]
    REMOVED_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_FIELD_NUMBER: _ClassVar[int]
    added: _containers.RepeatedCompositeFieldContainer[_graph_pb2.FeatureSet]
    removed: _containers.RepeatedCompositeFieldContainer[_graph_pb2.FeatureSet]
    modified: _containers.RepeatedCompositeFieldContainer[FeatureSetModified]
    def __init__(
        self,
        added: _Optional[_Iterable[_Union[_graph_pb2.FeatureSet, _Mapping]]] = ...,
        removed: _Optional[_Iterable[_Union[_graph_pb2.FeatureSet, _Mapping]]] = ...,
        modified: _Optional[_Iterable[_Union[FeatureSetModified, _Mapping]]] = ...,
    ) -> None: ...

class FeatureSetModified(_message.Message):
    __slots__ = ("before", "after", "changed_fields", "features")
    BEFORE_FIELD_NUMBER: _ClassVar[int]
    AFTER_FIELD_NUMBER: _ClassVar[int]
    CHANGED_FIELDS_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    before: _graph_pb2.FeatureSet
    after: _graph_pb2.FeatureSet
    changed_fields: _field_mask_pb2.FieldMask
    features: FeatureTypeCollectionDiff
    def __init__(
        self,
        before: _Optional[_Union[_graph_pb2.FeatureSet, _Mapping]] = ...,
        after: _Optional[_Union[_graph_pb2.FeatureSet, _Mapping]] = ...,
        changed_fields: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
        features: _Optional[_Union[FeatureTypeCollectionDiff, _Mapping]] = ...,
    ) -> None: ...

class FeatureTypeCollectionDiff(_message.Message):
    __slots__ = ("added", "removed", "modified")
    ADDED_FIELD_NUMBER: _ClassVar[int]
    REMOVED_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_FIELD_NUMBER: _ClassVar[int]
    added: _containers.RepeatedCompositeFieldContainer[_graph_pb2.FeatureType]
    removed: _containers.RepeatedCompositeFieldContainer[_graph_pb2.FeatureType]
    modified: _containers.RepeatedCompositeFieldContainer[FeatureTypeModified]
    def __init__(
        self,
        added: _Optional[_Iterable[_Union[_graph_pb2.FeatureType, _Mapping]]] = ...,
        removed: _Optional[_Iterable[_Union[_graph_pb2.FeatureType, _Mapping]]] = ...,
        modified: _Optional[_Iterable[_Union[FeatureTypeModified, _Mapping]]] = ...,
    ) -> None: ...

class FeatureTypeModified(_message.Message):
    __slots__ = ("before", "after", "changed_fields")
    BEFORE_FIELD_NUMBER: _ClassVar[int]
    AFTER_FIELD_NUMBER: _ClassVar[int]
    CHANGED_FIELDS_FIELD_NUMBER: _ClassVar[int]
    before: _graph_pb2.FeatureType
    after: _graph_pb2.FeatureType
    changed_fields: _field_mask_pb2.FieldMask
    def __init__(
        self,
        before: _Optional[_Union[_graph_pb2.FeatureType, _Mapping]] = ...,
        after: _Optional[_Union[_graph_pb2.FeatureType, _Mapping]] = ...,
        changed_fields: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class ResolverCollectionDiff(_message.Message):
    __slots__ = ("added", "removed", "modified")
    ADDED_FIELD_NUMBER: _ClassVar[int]
    REMOVED_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_FIELD_NUMBER: _ClassVar[int]
    added: _containers.RepeatedCompositeFieldContainer[_graph_pb2.Resolver]
    removed: _containers.RepeatedCompositeFieldContainer[_graph_pb2.Resolver]
    modified: _containers.RepeatedCompositeFieldContainer[ResolverModified]
    def __init__(
        self,
        added: _Optional[_Iterable[_Union[_graph_pb2.Resolver, _Mapping]]] = ...,
        removed: _Optional[_Iterable[_Union[_graph_pb2.Resolver, _Mapping]]] = ...,
        modified: _Optional[_Iterable[_Union[ResolverModified, _Mapping]]] = ...,
    ) -> None: ...

class ResolverModified(_message.Message):
    __slots__ = ("before", "after", "changed_fields")
    BEFORE_FIELD_NUMBER: _ClassVar[int]
    AFTER_FIELD_NUMBER: _ClassVar[int]
    CHANGED_FIELDS_FIELD_NUMBER: _ClassVar[int]
    before: _graph_pb2.Resolver
    after: _graph_pb2.Resolver
    changed_fields: _field_mask_pb2.FieldMask
    def __init__(
        self,
        before: _Optional[_Union[_graph_pb2.Resolver, _Mapping]] = ...,
        after: _Optional[_Union[_graph_pb2.Resolver, _Mapping]] = ...,
        changed_fields: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class StreamResolverCollectionDiff(_message.Message):
    __slots__ = ("added", "removed", "modified")
    ADDED_FIELD_NUMBER: _ClassVar[int]
    REMOVED_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_FIELD_NUMBER: _ClassVar[int]
    added: _containers.RepeatedCompositeFieldContainer[_graph_pb2.StreamResolver]
    removed: _containers.RepeatedCompositeFieldContainer[_graph_pb2.StreamResolver]
    modified: _containers.RepeatedCompositeFieldContainer[StreamResolverModified]
    def __init__(
        self,
        added: _Optional[_Iterable[_Union[_graph_pb2.StreamResolver, _Mapping]]] = ...,
        removed: _Optional[_Iterable[_Union[_graph_pb2.StreamResolver, _Mapping]]] = ...,
        modified: _Optional[_Iterable[_Union[StreamResolverModified, _Mapping]]] = ...,
    ) -> None: ...

class StreamResolverModified(_message.Message):
    __slots__ = ("before", "after", "changed_fields")
    BEFORE_FIELD_NUMBER: _ClassVar[int]
    AFTER_FIELD_NUMBER: _ClassVar[int]
    CHANGED_FIELDS_FIELD_NUMBER: _ClassVar[int]
    before: _graph_pb2.StreamResolver
    after: _graph_pb2.StreamResolver
    changed_fields: _field_mask_pb2.FieldMask
    def __init__(
        self,
        before: _Optional[_Union[_graph_pb2.StreamResolver, _Mapping]] = ...,
        after: _Optional[_Union[_graph_pb2.StreamResolver, _Mapping]] = ...,
        changed_fields: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class SinkResolverCollectionDiff(_message.Message):
    __slots__ = ("added", "removed", "modified")
    ADDED_FIELD_NUMBER: _ClassVar[int]
    REMOVED_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_FIELD_NUMBER: _ClassVar[int]
    added: _containers.RepeatedCompositeFieldContainer[_graph_pb2.SinkResolver]
    removed: _containers.RepeatedCompositeFieldContainer[_graph_pb2.SinkResolver]
    modified: _containers.RepeatedCompositeFieldContainer[SinkResolverModified]
    def __init__(
        self,
        added: _Optional[_Iterable[_Union[_graph_pb2.SinkResolver, _Mapping]]] = ...,
        removed: _Optional[_Iterable[_Union[_graph_pb2.SinkResolver, _Mapping]]] = ...,
        modified: _Optional[_Iterable[_Union[SinkResolverModified, _Mapping]]] = ...,
    ) -> None: ...

class SinkResolverModified(_message.Message):
    __slots__ = ("before", "after", "changed_fields")
    BEFORE_FIELD_NUMBER: _ClassVar[int]
    AFTER_FIELD_NUMBER: _ClassVar[int]
    CHANGED_FIELDS_FIELD_NUMBER: _ClassVar[int]
    before: _graph_pb2.SinkResolver
    after: _graph_pb2.SinkResolver
    changed_fields: _field_mask_pb2.FieldMask
    def __init__(
        self,
        before: _Optional[_Union[_graph_pb2.SinkResolver, _Mapping]] = ...,
        after: _Optional[_Union[_graph_pb2.SinkResolver, _Mapping]] = ...,
        changed_fields: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class NamedQueryCollectionDiff(_message.Message):
    __slots__ = ("added", "removed", "modified")
    ADDED_FIELD_NUMBER: _ClassVar[int]
    REMOVED_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_FIELD_NUMBER: _ClassVar[int]
    added: _containers.RepeatedCompositeFieldContainer[_graph_pb2.NamedQuery]
    removed: _containers.RepeatedCompositeFieldContainer[_graph_pb2.NamedQuery]
    modified: _containers.RepeatedCompositeFieldContainer[NamedQueryModified]
    def __init__(
        self,
        added: _Optional[_Iterable[_Union[_graph_pb2.NamedQuery, _Mapping]]] = ...,
        removed: _Optional[_Iterable[_Union[_graph_pb2.NamedQuery, _Mapping]]] = ...,
        modified: _Optional[_Iterable[_Union[NamedQueryModified, _Mapping]]] = ...,
    ) -> None: ...

class NamedQueryModified(_message.Message):
    __slots__ = ("before", "after", "changed_fields")
    BEFORE_FIELD_NUMBER: _ClassVar[int]
    AFTER_FIELD_NUMBER: _ClassVar[int]
    CHANGED_FIELDS_FIELD_NUMBER: _ClassVar[int]
    before: _graph_pb2.NamedQuery
    after: _graph_pb2.NamedQuery
    changed_fields: _field_mask_pb2.FieldMask
    def __init__(
        self,
        before: _Optional[_Union[_graph_pb2.NamedQuery, _Mapping]] = ...,
        after: _Optional[_Union[_graph_pb2.NamedQuery, _Mapping]] = ...,
        changed_fields: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class DatabaseSourceCollectionDiff(_message.Message):
    __slots__ = ("added", "removed", "modified")
    ADDED_FIELD_NUMBER: _ClassVar[int]
    REMOVED_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_FIELD_NUMBER: _ClassVar[int]
    added: _containers.RepeatedCompositeFieldContainer[_sources_pb2.DatabaseSource]
    removed: _containers.RepeatedCompositeFieldContainer[_sources_pb2.DatabaseSource]
    modified: _containers.RepeatedCompositeFieldContainer[DatabaseSourceModified]
    def __init__(
        self,
        added: _Optional[_Iterable[_Union[_sources_pb2.DatabaseSource, _Mapping]]] = ...,
        removed: _Optional[_Iterable[_Union[_sources_pb2.DatabaseSource, _Mapping]]] = ...,
        modified: _Optional[_Iterable[_Union[DatabaseSourceModified, _Mapping]]] = ...,
    ) -> None: ...

class DatabaseSourceModified(_message.Message):
    __slots__ = ("before", "after", "changed_fields")
    BEFORE_FIELD_NUMBER: _ClassVar[int]
    AFTER_FIELD_NUMBER: _ClassVar[int]
    CHANGED_FIELDS_FIELD_NUMBER: _ClassVar[int]
    before: _sources_pb2.DatabaseSource
    after: _sources_pb2.DatabaseSource
    changed_fields: _field_mask_pb2.FieldMask
    def __init__(
        self,
        before: _Optional[_Union[_sources_pb2.DatabaseSource, _Mapping]] = ...,
        after: _Optional[_Union[_sources_pb2.DatabaseSource, _Mapping]] = ...,
        changed_fields: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class StreamSourceCollectionDiff(_message.Message):
    __slots__ = ("added", "removed", "modified")
    ADDED_FIELD_NUMBER: _ClassVar[int]
    REMOVED_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_FIELD_NUMBER: _ClassVar[int]
    added: _containers.RepeatedCompositeFieldContainer[_sources_pb2.StreamSource]
    removed: _containers.RepeatedCompositeFieldContainer[_sources_pb2.StreamSource]
    modified: _containers.RepeatedCompositeFieldContainer[StreamSourceModified]
    def __init__(
        self,
        added: _Optional[_Iterable[_Union[_sources_pb2.StreamSource, _Mapping]]] = ...,
        removed: _Optional[_Iterable[_Union[_sources_pb2.StreamSource, _Mapping]]] = ...,
        modified: _Optional[_Iterable[_Union[StreamSourceModified, _Mapping]]] = ...,
    ) -> None: ...

class StreamSourceModified(_message.Message):
    __slots__ = ("before", "after", "changed_fields")
    BEFORE_FIELD_NUMBER: _ClassVar[int]
    AFTER_FIELD_NUMBER: _ClassVar[int]
    CHANGED_FIELDS_FIELD_NUMBER: _ClassVar[int]
    before: _sources_pb2.StreamSource
    after: _sources_pb2.StreamSource
    changed_fields: _field_mask_pb2.FieldMask
    def __init__(
        self,
        before: _Optional[_Union[_sources_pb2.StreamSource, _Mapping]] = ...,
        after: _Optional[_Union[_sources_pb2.StreamSource, _Mapping]] = ...,
        changed_fields: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class ModelReferenceCollectionDiff(_message.Message):
    __slots__ = ("added", "removed", "modified")
    ADDED_FIELD_NUMBER: _ClassVar[int]
    REMOVED_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_FIELD_NUMBER: _ClassVar[int]
    added: _containers.RepeatedCompositeFieldContainer[_graph_pb2.ModelReference]
    removed: _containers.RepeatedCompositeFieldContainer[_graph_pb2.ModelReference]
    modified: _containers.RepeatedCompositeFieldContainer[ModelReferenceModified]
    def __init__(
        self,
        added: _Optional[_Iterable[_Union[_graph_pb2.ModelReference, _Mapping]]] = ...,
        removed: _Optional[_Iterable[_Union[_graph_pb2.ModelReference, _Mapping]]] = ...,
        modified: _Optional[_Iterable[_Union[ModelReferenceModified, _Mapping]]] = ...,
    ) -> None: ...

class ModelReferenceModified(_message.Message):
    __slots__ = ("before", "after", "changed_fields")
    BEFORE_FIELD_NUMBER: _ClassVar[int]
    AFTER_FIELD_NUMBER: _ClassVar[int]
    CHANGED_FIELDS_FIELD_NUMBER: _ClassVar[int]
    before: _graph_pb2.ModelReference
    after: _graph_pb2.ModelReference
    changed_fields: _field_mask_pb2.FieldMask
    def __init__(
        self,
        before: _Optional[_Union[_graph_pb2.ModelReference, _Mapping]] = ...,
        after: _Optional[_Union[_graph_pb2.ModelReference, _Mapping]] = ...,
        changed_fields: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class DatabaseSourceGroupCollectionDiff(_message.Message):
    __slots__ = ("added", "removed", "modified")
    ADDED_FIELD_NUMBER: _ClassVar[int]
    REMOVED_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_FIELD_NUMBER: _ClassVar[int]
    added: _containers.RepeatedCompositeFieldContainer[_sources_pb2.DatabaseSourceGroup]
    removed: _containers.RepeatedCompositeFieldContainer[_sources_pb2.DatabaseSourceGroup]
    modified: _containers.RepeatedCompositeFieldContainer[DatabaseSourceGroupModified]
    def __init__(
        self,
        added: _Optional[_Iterable[_Union[_sources_pb2.DatabaseSourceGroup, _Mapping]]] = ...,
        removed: _Optional[_Iterable[_Union[_sources_pb2.DatabaseSourceGroup, _Mapping]]] = ...,
        modified: _Optional[_Iterable[_Union[DatabaseSourceGroupModified, _Mapping]]] = ...,
    ) -> None: ...

class DatabaseSourceGroupModified(_message.Message):
    __slots__ = ("before", "after", "changed_fields")
    BEFORE_FIELD_NUMBER: _ClassVar[int]
    AFTER_FIELD_NUMBER: _ClassVar[int]
    CHANGED_FIELDS_FIELD_NUMBER: _ClassVar[int]
    before: _sources_pb2.DatabaseSourceGroup
    after: _sources_pb2.DatabaseSourceGroup
    changed_fields: _field_mask_pb2.FieldMask
    def __init__(
        self,
        before: _Optional[_Union[_sources_pb2.DatabaseSourceGroup, _Mapping]] = ...,
        after: _Optional[_Union[_sources_pb2.DatabaseSourceGroup, _Mapping]] = ...,
        changed_fields: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class OnlineStoreConfigCollectionDiff(_message.Message):
    __slots__ = ("added", "removed", "modified")
    ADDED_FIELD_NUMBER: _ClassVar[int]
    REMOVED_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_FIELD_NUMBER: _ClassVar[int]
    added: _containers.RepeatedCompositeFieldContainer[_graph_pb2.OnlineStoreConfig]
    removed: _containers.RepeatedCompositeFieldContainer[_graph_pb2.OnlineStoreConfig]
    modified: _containers.RepeatedCompositeFieldContainer[OnlineStoreConfigModified]
    def __init__(
        self,
        added: _Optional[_Iterable[_Union[_graph_pb2.OnlineStoreConfig, _Mapping]]] = ...,
        removed: _Optional[_Iterable[_Union[_graph_pb2.OnlineStoreConfig, _Mapping]]] = ...,
        modified: _Optional[_Iterable[_Union[OnlineStoreConfigModified, _Mapping]]] = ...,
    ) -> None: ...

class OnlineStoreConfigModified(_message.Message):
    __slots__ = ("before", "after", "changed_fields")
    BEFORE_FIELD_NUMBER: _ClassVar[int]
    AFTER_FIELD_NUMBER: _ClassVar[int]
    CHANGED_FIELDS_FIELD_NUMBER: _ClassVar[int]
    before: _graph_pb2.OnlineStoreConfig
    after: _graph_pb2.OnlineStoreConfig
    changed_fields: _field_mask_pb2.FieldMask
    def __init__(
        self,
        before: _Optional[_Union[_graph_pb2.OnlineStoreConfig, _Mapping]] = ...,
        after: _Optional[_Union[_graph_pb2.OnlineStoreConfig, _Mapping]] = ...,
        changed_fields: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class CronQueryCollectionDiff(_message.Message):
    __slots__ = ("added", "removed", "modified")
    ADDED_FIELD_NUMBER: _ClassVar[int]
    REMOVED_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_FIELD_NUMBER: _ClassVar[int]
    added: _containers.RepeatedCompositeFieldContainer[_cron_query_pb2.CronQuery]
    removed: _containers.RepeatedCompositeFieldContainer[_cron_query_pb2.CronQuery]
    modified: _containers.RepeatedCompositeFieldContainer[CronQueryModified]
    def __init__(
        self,
        added: _Optional[_Iterable[_Union[_cron_query_pb2.CronQuery, _Mapping]]] = ...,
        removed: _Optional[_Iterable[_Union[_cron_query_pb2.CronQuery, _Mapping]]] = ...,
        modified: _Optional[_Iterable[_Union[CronQueryModified, _Mapping]]] = ...,
    ) -> None: ...

class CronQueryModified(_message.Message):
    __slots__ = ("before", "after", "changed_fields")
    BEFORE_FIELD_NUMBER: _ClassVar[int]
    AFTER_FIELD_NUMBER: _ClassVar[int]
    CHANGED_FIELDS_FIELD_NUMBER: _ClassVar[int]
    before: _cron_query_pb2.CronQuery
    after: _cron_query_pb2.CronQuery
    changed_fields: _field_mask_pb2.FieldMask
    def __init__(
        self,
        before: _Optional[_Union[_cron_query_pb2.CronQuery, _Mapping]] = ...,
        after: _Optional[_Union[_cron_query_pb2.CronQuery, _Mapping]] = ...,
        changed_fields: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class ChartCollectionDiff(_message.Message):
    __slots__ = ("added", "removed", "modified")
    ADDED_FIELD_NUMBER: _ClassVar[int]
    REMOVED_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_FIELD_NUMBER: _ClassVar[int]
    added: _containers.RepeatedCompositeFieldContainer[_chart_pb2.Chart]
    removed: _containers.RepeatedCompositeFieldContainer[_chart_pb2.Chart]
    modified: _containers.RepeatedCompositeFieldContainer[ChartModified]
    def __init__(
        self,
        added: _Optional[_Iterable[_Union[_chart_pb2.Chart, _Mapping]]] = ...,
        removed: _Optional[_Iterable[_Union[_chart_pb2.Chart, _Mapping]]] = ...,
        modified: _Optional[_Iterable[_Union[ChartModified, _Mapping]]] = ...,
    ) -> None: ...

class ChartModified(_message.Message):
    __slots__ = ("before", "after", "changed_fields")
    BEFORE_FIELD_NUMBER: _ClassVar[int]
    AFTER_FIELD_NUMBER: _ClassVar[int]
    CHANGED_FIELDS_FIELD_NUMBER: _ClassVar[int]
    before: _chart_pb2.Chart
    after: _chart_pb2.Chart
    changed_fields: _field_mask_pb2.FieldMask
    def __init__(
        self,
        before: _Optional[_Union[_chart_pb2.Chart, _Mapping]] = ...,
        after: _Optional[_Union[_chart_pb2.Chart, _Mapping]] = ...,
        changed_fields: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class CDCSourceCollectionDiff(_message.Message):
    __slots__ = ("added", "removed", "modified")
    ADDED_FIELD_NUMBER: _ClassVar[int]
    REMOVED_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_FIELD_NUMBER: _ClassVar[int]
    added: _containers.RepeatedCompositeFieldContainer[_cdc_pb2.CDCSource]
    removed: _containers.RepeatedCompositeFieldContainer[_cdc_pb2.CDCSource]
    modified: _containers.RepeatedCompositeFieldContainer[CDCSourceModified]
    def __init__(
        self,
        added: _Optional[_Iterable[_Union[_cdc_pb2.CDCSource, _Mapping]]] = ...,
        removed: _Optional[_Iterable[_Union[_cdc_pb2.CDCSource, _Mapping]]] = ...,
        modified: _Optional[_Iterable[_Union[CDCSourceModified, _Mapping]]] = ...,
    ) -> None: ...

class CDCSourceModified(_message.Message):
    __slots__ = ("before", "after", "changed_fields")
    BEFORE_FIELD_NUMBER: _ClassVar[int]
    AFTER_FIELD_NUMBER: _ClassVar[int]
    CHANGED_FIELDS_FIELD_NUMBER: _ClassVar[int]
    before: _cdc_pb2.CDCSource
    after: _cdc_pb2.CDCSource
    changed_fields: _field_mask_pb2.FieldMask
    def __init__(
        self,
        before: _Optional[_Union[_cdc_pb2.CDCSource, _Mapping]] = ...,
        after: _Optional[_Union[_cdc_pb2.CDCSource, _Mapping]] = ...,
        changed_fields: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...
