from chalk._gen.chalk.aggregate.v1 import timeseries_pb2 as _timeseries_pb2
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

class TileFacetType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TILE_FACET_TYPE_UNSPECIFIED: _ClassVar[TileFacetType]
    TILE_FACET_TYPE_LIST: _ClassVar[TileFacetType]

class TileFeatureMappingStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TILE_FEATURE_MAPPING_STATUS_UNSPECIFIED: _ClassVar[TileFeatureMappingStatus]
    TILE_FEATURE_MAPPING_STATUS_AVAILABLE: _ClassVar[TileFeatureMappingStatus]
    TILE_FEATURE_MAPPING_STATUS_NO_ACTIVE_DEPLOYMENT: _ClassVar[TileFeatureMappingStatus]
    TILE_FEATURE_MAPPING_STATUS_ENGINE_UNSUPPORTED: _ClassVar[TileFeatureMappingStatus]

TILE_FACET_TYPE_UNSPECIFIED: TileFacetType
TILE_FACET_TYPE_LIST: TileFacetType
TILE_FEATURE_MAPPING_STATUS_UNSPECIFIED: TileFeatureMappingStatus
TILE_FEATURE_MAPPING_STATUS_AVAILABLE: TileFeatureMappingStatus
TILE_FEATURE_MAPPING_STATUS_NO_ACTIVE_DEPLOYMENT: TileFeatureMappingStatus
TILE_FEATURE_MAPPING_STATUS_ENGINE_UNSUPPORTED: TileFeatureMappingStatus

class MaterializedAggregateTileTimelineInterval(_message.Message):
    __slots__ = ("coverage_lower_bound", "coverage_upper_bound")
    COVERAGE_LOWER_BOUND_FIELD_NUMBER: _ClassVar[int]
    COVERAGE_UPPER_BOUND_FIELD_NUMBER: _ClassVar[int]
    coverage_lower_bound: _timestamp_pb2.Timestamp
    coverage_upper_bound: _timestamp_pb2.Timestamp
    def __init__(
        self,
        coverage_lower_bound: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        coverage_upper_bound: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class MaterializedAggregateTileTimeline(_message.Message):
    __slots__ = (
        "materialization_key_hash",
        "aggregation",
        "aggregate_on",
        "group_by",
        "bucket_on",
        "coverage",
        "intervals",
        "bucket_duration_ms",
        "reading_features",
    )
    MATERIALIZATION_KEY_HASH_FIELD_NUMBER: _ClassVar[int]
    AGGREGATION_FIELD_NUMBER: _ClassVar[int]
    AGGREGATE_ON_FIELD_NUMBER: _ClassVar[int]
    GROUP_BY_FIELD_NUMBER: _ClassVar[int]
    BUCKET_ON_FIELD_NUMBER: _ClassVar[int]
    COVERAGE_FIELD_NUMBER: _ClassVar[int]
    INTERVALS_FIELD_NUMBER: _ClassVar[int]
    BUCKET_DURATION_MS_FIELD_NUMBER: _ClassVar[int]
    READING_FEATURES_FIELD_NUMBER: _ClassVar[int]
    materialization_key_hash: str
    aggregation: str
    aggregate_on: str
    group_by: str
    bucket_on: str
    coverage: MaterializedAggregateTileTimelineInterval
    intervals: _containers.RepeatedCompositeFieldContainer[MaterializedAggregateTileTimelineInterval]
    bucket_duration_ms: int
    reading_features: _containers.RepeatedCompositeFieldContainer[TileReadingFeature]
    def __init__(
        self,
        materialization_key_hash: _Optional[str] = ...,
        aggregation: _Optional[str] = ...,
        aggregate_on: _Optional[str] = ...,
        group_by: _Optional[str] = ...,
        bucket_on: _Optional[str] = ...,
        coverage: _Optional[_Union[MaterializedAggregateTileTimelineInterval, _Mapping]] = ...,
        intervals: _Optional[_Iterable[_Union[MaterializedAggregateTileTimelineInterval, _Mapping]]] = ...,
        bucket_duration_ms: _Optional[int] = ...,
        reading_features: _Optional[_Iterable[_Union[TileReadingFeature, _Mapping]]] = ...,
    ) -> None: ...

class TileReadingFeature(_message.Message):
    __slots__ = ("fqn", "windowed_features", "series_count")
    FQN_FIELD_NUMBER: _ClassVar[int]
    WINDOWED_FEATURES_FIELD_NUMBER: _ClassVar[int]
    SERIES_COUNT_FIELD_NUMBER: _ClassVar[int]
    fqn: str
    windowed_features: _containers.RepeatedScalarFieldContainer[str]
    series_count: int
    def __init__(
        self,
        fqn: _Optional[str] = ...,
        windowed_features: _Optional[_Iterable[str]] = ...,
        series_count: _Optional[int] = ...,
    ) -> None: ...

class MaterializedAggregateTileTimelineGroup(_message.Message):
    __slots__ = ("aggregate_on", "timelines", "coverage")
    AGGREGATE_ON_FIELD_NUMBER: _ClassVar[int]
    TIMELINES_FIELD_NUMBER: _ClassVar[int]
    COVERAGE_FIELD_NUMBER: _ClassVar[int]
    aggregate_on: str
    timelines: _containers.RepeatedCompositeFieldContainer[MaterializedAggregateTileTimeline]
    coverage: MaterializedAggregateTileTimelineInterval
    def __init__(
        self,
        aggregate_on: _Optional[str] = ...,
        timelines: _Optional[_Iterable[_Union[MaterializedAggregateTileTimeline, _Mapping]]] = ...,
        coverage: _Optional[_Union[MaterializedAggregateTileTimelineInterval, _Mapping]] = ...,
    ) -> None: ...

class ListMaterializedAggregateTileTimelinesFilter(_message.Message):
    __slots__ = ("aggregate_on_prefix", "query")
    AGGREGATE_ON_PREFIX_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    aggregate_on_prefix: str
    query: str
    def __init__(self, aggregate_on_prefix: _Optional[str] = ..., query: _Optional[str] = ...) -> None: ...

class ListMaterializedAggregateTileTimelinesRequest(_message.Message):
    __slots__ = ("cursor", "limit", "filter")
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    cursor: str
    limit: int
    filter: ListMaterializedAggregateTileTimelinesFilter
    def __init__(
        self,
        cursor: _Optional[str] = ...,
        limit: _Optional[int] = ...,
        filter: _Optional[_Union[ListMaterializedAggregateTileTimelinesFilter, _Mapping]] = ...,
    ) -> None: ...

class ListMaterializedAggregateTileTimelinesResponse(_message.Message):
    __slots__ = ("timeline_groups", "next_cursor")
    TIMELINE_GROUPS_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    timeline_groups: _containers.RepeatedCompositeFieldContainer[MaterializedAggregateTileTimelineGroup]
    next_cursor: str
    def __init__(
        self,
        timeline_groups: _Optional[_Iterable[_Union[MaterializedAggregateTileTimelineGroup, _Mapping]]] = ...,
        next_cursor: _Optional[str] = ...,
    ) -> None: ...

class TileFacet(_message.Message):
    __slots__ = ("path", "name", "facet_type")
    PATH_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    FACET_TYPE_FIELD_NUMBER: _ClassVar[int]
    path: str
    name: str
    facet_type: TileFacetType
    def __init__(
        self,
        path: _Optional[str] = ...,
        name: _Optional[str] = ...,
        facet_type: _Optional[_Union[TileFacetType, str]] = ...,
    ) -> None: ...

class GetMaterializedAggregateTileFacetsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetMaterializedAggregateTileFacetsResponse(_message.Message):
    __slots__ = ("facets",)
    FACETS_FIELD_NUMBER: _ClassVar[int]
    facets: _containers.RepeatedCompositeFieldContainer[TileFacet]
    def __init__(self, facets: _Optional[_Iterable[_Union[TileFacet, _Mapping]]] = ...) -> None: ...

class GetMaterializedAggregateTileFacetValuesRequest(_message.Message):
    __slots__ = ("path", "limit", "filter", "value_search")
    PATH_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    VALUE_SEARCH_FIELD_NUMBER: _ClassVar[int]
    path: str
    limit: int
    filter: ListMaterializedAggregateTileTimelinesFilter
    value_search: str
    def __init__(
        self,
        path: _Optional[str] = ...,
        limit: _Optional[int] = ...,
        filter: _Optional[_Union[ListMaterializedAggregateTileTimelinesFilter, _Mapping]] = ...,
        value_search: _Optional[str] = ...,
    ) -> None: ...

class TileTimelineFacetValue(_message.Message):
    __slots__ = ("path", "value", "count")
    PATH_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    path: str
    value: str
    count: int
    def __init__(
        self, path: _Optional[str] = ..., value: _Optional[str] = ..., count: _Optional[int] = ...
    ) -> None: ...

class GetMaterializedAggregateTileFacetValuesResponse(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedCompositeFieldContainer[TileTimelineFacetValue]
    def __init__(self, values: _Optional[_Iterable[_Union[TileTimelineFacetValue, _Mapping]]] = ...) -> None: ...

class TileSeriesSummary(_message.Message):
    __slots__ = ("materialization_key_hash", "aggregations", "bucket_duration_ms", "reading_features")
    MATERIALIZATION_KEY_HASH_FIELD_NUMBER: _ClassVar[int]
    AGGREGATIONS_FIELD_NUMBER: _ClassVar[int]
    BUCKET_DURATION_MS_FIELD_NUMBER: _ClassVar[int]
    READING_FEATURES_FIELD_NUMBER: _ClassVar[int]
    materialization_key_hash: str
    aggregations: _containers.RepeatedScalarFieldContainer[str]
    bucket_duration_ms: int
    reading_features: _containers.RepeatedCompositeFieldContainer[TileReadingFeature]
    def __init__(
        self,
        materialization_key_hash: _Optional[str] = ...,
        aggregations: _Optional[_Iterable[str]] = ...,
        bucket_duration_ms: _Optional[int] = ...,
        reading_features: _Optional[_Iterable[_Union[TileReadingFeature, _Mapping]]] = ...,
    ) -> None: ...

class FeatureMaterializedAggregation(_message.Message):
    __slots__ = ("series", "tile_series")
    SERIES_FIELD_NUMBER: _ClassVar[int]
    TILE_SERIES_FIELD_NUMBER: _ClassVar[int]
    series: _timeseries_pb2.AggregateTimeSeries
    tile_series: _containers.RepeatedCompositeFieldContainer[TileSeriesSummary]
    def __init__(
        self,
        series: _Optional[_Union[_timeseries_pb2.AggregateTimeSeries, _Mapping]] = ...,
        tile_series: _Optional[_Iterable[_Union[TileSeriesSummary, _Mapping]]] = ...,
    ) -> None: ...

class GetFeatureMaterializedAggregationsRequest(_message.Message):
    __slots__ = ("feature_fqn",)
    FEATURE_FQN_FIELD_NUMBER: _ClassVar[int]
    feature_fqn: str
    def __init__(self, feature_fqn: _Optional[str] = ...) -> None: ...

class GetFeatureMaterializedAggregationsResponse(_message.Message):
    __slots__ = ("computing", "reading", "errors", "mapping_status")
    COMPUTING_FIELD_NUMBER: _ClassVar[int]
    READING_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    MAPPING_STATUS_FIELD_NUMBER: _ClassVar[int]
    computing: _containers.RepeatedCompositeFieldContainer[FeatureMaterializedAggregation]
    reading: _containers.RepeatedCompositeFieldContainer[FeatureMaterializedAggregation]
    errors: _containers.RepeatedScalarFieldContainer[str]
    mapping_status: TileFeatureMappingStatus
    def __init__(
        self,
        computing: _Optional[_Iterable[_Union[FeatureMaterializedAggregation, _Mapping]]] = ...,
        reading: _Optional[_Iterable[_Union[FeatureMaterializedAggregation, _Mapping]]] = ...,
        errors: _Optional[_Iterable[str]] = ...,
        mapping_status: _Optional[_Union[TileFeatureMappingStatus, str]] = ...,
    ) -> None: ...

class TileSeriesCoverage(_message.Message):
    __slots__ = ("materialization_key_hash", "bucket_duration_ms", "coverage", "gaps", "tile_count")
    MATERIALIZATION_KEY_HASH_FIELD_NUMBER: _ClassVar[int]
    BUCKET_DURATION_MS_FIELD_NUMBER: _ClassVar[int]
    COVERAGE_FIELD_NUMBER: _ClassVar[int]
    GAPS_FIELD_NUMBER: _ClassVar[int]
    TILE_COUNT_FIELD_NUMBER: _ClassVar[int]
    materialization_key_hash: str
    bucket_duration_ms: int
    coverage: MaterializedAggregateTileTimelineInterval
    gaps: _containers.RepeatedCompositeFieldContainer[MaterializedAggregateTileTimelineInterval]
    tile_count: int
    def __init__(
        self,
        materialization_key_hash: _Optional[str] = ...,
        bucket_duration_ms: _Optional[int] = ...,
        coverage: _Optional[_Union[MaterializedAggregateTileTimelineInterval, _Mapping]] = ...,
        gaps: _Optional[_Iterable[_Union[MaterializedAggregateTileTimelineInterval, _Mapping]]] = ...,
        tile_count: _Optional[int] = ...,
    ) -> None: ...

class TileFeatureCoverage(_message.Message):
    __slots__ = ("fqn", "windowed_features", "series")
    FQN_FIELD_NUMBER: _ClassVar[int]
    WINDOWED_FEATURES_FIELD_NUMBER: _ClassVar[int]
    SERIES_FIELD_NUMBER: _ClassVar[int]
    fqn: str
    windowed_features: _containers.RepeatedScalarFieldContainer[str]
    series: _containers.RepeatedCompositeFieldContainer[TileSeriesCoverage]
    def __init__(
        self,
        fqn: _Optional[str] = ...,
        windowed_features: _Optional[_Iterable[str]] = ...,
        series: _Optional[_Iterable[_Union[TileSeriesCoverage, _Mapping]]] = ...,
    ) -> None: ...

class ListTileFeatureCoverageFilters(_message.Message):
    __slots__ = ("fqn_search", "feature_fqns")
    FQN_SEARCH_FIELD_NUMBER: _ClassVar[int]
    FEATURE_FQNS_FIELD_NUMBER: _ClassVar[int]
    fqn_search: str
    feature_fqns: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, fqn_search: _Optional[str] = ..., feature_fqns: _Optional[_Iterable[str]] = ...) -> None: ...

class ListTileFeatureCoverageRequest(_message.Message):
    __slots__ = ("cursor", "limit", "filters")
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    cursor: str
    limit: int
    filters: ListTileFeatureCoverageFilters
    def __init__(
        self,
        cursor: _Optional[str] = ...,
        limit: _Optional[int] = ...,
        filters: _Optional[_Union[ListTileFeatureCoverageFilters, _Mapping]] = ...,
    ) -> None: ...

class ListTileFeatureCoverageResponse(_message.Message):
    __slots__ = ("features", "next_cursor", "mapping_status")
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    MAPPING_STATUS_FIELD_NUMBER: _ClassVar[int]
    features: _containers.RepeatedCompositeFieldContainer[TileFeatureCoverage]
    next_cursor: str
    mapping_status: TileFeatureMappingStatus
    def __init__(
        self,
        features: _Optional[_Iterable[_Union[TileFeatureCoverage, _Mapping]]] = ...,
        next_cursor: _Optional[str] = ...,
        mapping_status: _Optional[_Union[TileFeatureMappingStatus, str]] = ...,
    ) -> None: ...
