from chalk._gen.chalk.arrow.v1 import arrow_pb2 as _arrow_pb2
from chalk._gen.chalk.expression.v1 import expression_pb2 as _expression_pb2
from chalk._gen.chalk.graph.v1 import sources_pb2 as _sources_pb2
from chalk._gen.chalk.graph.v2 import sources_pb2 as _sources_pb2_1
from chalk._gen.chalk.lsp.v1 import lsp_pb2 as _lsp_pb2
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

class CacheStrategy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CACHE_STRATEGY_UNSPECIFIED: _ClassVar[CacheStrategy]
    CACHE_STRATEGY_ALL: _ClassVar[CacheStrategy]
    CACHE_STRATEGY_NO_NULLS: _ClassVar[CacheStrategy]
    CACHE_STRATEGY_EVICT_NULLS: _ClassVar[CacheStrategy]
    CACHE_STRATEGY_NO_DEFAULTS: _ClassVar[CacheStrategy]
    CACHE_STRATEGY_EVICT_DEFAULTS: _ClassVar[CacheStrategy]
    CACHE_STRATEGY_NO_NULLS_OR_DEFAULTS: _ClassVar[CacheStrategy]
    CACHE_STRATEGY_EVICT_NULLS_AND_DEFAULTS: _ClassVar[CacheStrategy]

class ResolverKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RESOLVER_KIND_UNSPECIFIED: _ClassVar[ResolverKind]
    RESOLVER_KIND_ONLINE: _ClassVar[ResolverKind]
    RESOLVER_KIND_OFFLINE: _ClassVar[ResolverKind]

class ResourceHint(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RESOURCE_HINT_UNSPECIFIED: _ClassVar[ResourceHint]
    RESOURCE_HINT_CPU: _ClassVar[ResourceHint]
    RESOURCE_HINT_IO: _ClassVar[ResourceHint]

class Finalizer(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FINALIZER_UNSPECIFIED: _ClassVar[Finalizer]
    FINALIZER_ONE_OR_NONE: _ClassVar[Finalizer]
    FINALIZER_ONE: _ClassVar[Finalizer]
    FINALIZER_FIRST: _ClassVar[Finalizer]
    FINALIZER_ALL: _ClassVar[Finalizer]

class IncrementalMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INCREMENTAL_MODE_UNSPECIFIED: _ClassVar[IncrementalMode]
    INCREMENTAL_MODE_ROW: _ClassVar[IncrementalMode]
    INCREMENTAL_MODE_GROUP: _ClassVar[IncrementalMode]
    INCREMENTAL_MODE_PARAMETER: _ClassVar[IncrementalMode]

class IncrementalTimestampMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INCREMENTAL_TIMESTAMP_MODE_UNSPECIFIED: _ClassVar[IncrementalTimestampMode]
    INCREMENTAL_TIMESTAMP_MODE_FEATURE_TIME: _ClassVar[IncrementalTimestampMode]
    INCREMENTAL_TIMESTAMP_MODE_RESOLVER_EXECUTION_TIME: _ClassVar[IncrementalTimestampMode]

class WindowMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WINDOW_MODE_UNSPECIFIED: _ClassVar[WindowMode]
    WINDOW_MODE_CONTINUOUS: _ClassVar[WindowMode]
    WINDOW_MODE_TUMBLING: _ClassVar[WindowMode]
    WINDOW_MODE_CDC: _ClassVar[WindowMode]

CACHE_STRATEGY_UNSPECIFIED: CacheStrategy
CACHE_STRATEGY_ALL: CacheStrategy
CACHE_STRATEGY_NO_NULLS: CacheStrategy
CACHE_STRATEGY_EVICT_NULLS: CacheStrategy
CACHE_STRATEGY_NO_DEFAULTS: CacheStrategy
CACHE_STRATEGY_EVICT_DEFAULTS: CacheStrategy
CACHE_STRATEGY_NO_NULLS_OR_DEFAULTS: CacheStrategy
CACHE_STRATEGY_EVICT_NULLS_AND_DEFAULTS: CacheStrategy
RESOLVER_KIND_UNSPECIFIED: ResolverKind
RESOLVER_KIND_ONLINE: ResolverKind
RESOLVER_KIND_OFFLINE: ResolverKind
RESOURCE_HINT_UNSPECIFIED: ResourceHint
RESOURCE_HINT_CPU: ResourceHint
RESOURCE_HINT_IO: ResourceHint
FINALIZER_UNSPECIFIED: Finalizer
FINALIZER_ONE_OR_NONE: Finalizer
FINALIZER_ONE: Finalizer
FINALIZER_FIRST: Finalizer
FINALIZER_ALL: Finalizer
INCREMENTAL_MODE_UNSPECIFIED: IncrementalMode
INCREMENTAL_MODE_ROW: IncrementalMode
INCREMENTAL_MODE_GROUP: IncrementalMode
INCREMENTAL_MODE_PARAMETER: IncrementalMode
INCREMENTAL_TIMESTAMP_MODE_UNSPECIFIED: IncrementalTimestampMode
INCREMENTAL_TIMESTAMP_MODE_FEATURE_TIME: IncrementalTimestampMode
INCREMENTAL_TIMESTAMP_MODE_RESOLVER_EXECUTION_TIME: IncrementalTimestampMode
WINDOW_MODE_UNSPECIFIED: WindowMode
WINDOW_MODE_CONTINUOUS: WindowMode
WINDOW_MODE_TUMBLING: WindowMode
WINDOW_MODE_CDC: WindowMode

class Graph(_message.Message):
    __slots__ = (
        "feature_sets",
        "resolvers",
        "stream_resolvers",
        "sink_resolvers",
        "database_sources",
        "stream_sources",
        "named_queries",
        "database_sources_v2",
        "database_source_groups",
        "stream_sources_v2",
    )
    FEATURE_SETS_FIELD_NUMBER: _ClassVar[int]
    RESOLVERS_FIELD_NUMBER: _ClassVar[int]
    STREAM_RESOLVERS_FIELD_NUMBER: _ClassVar[int]
    SINK_RESOLVERS_FIELD_NUMBER: _ClassVar[int]
    DATABASE_SOURCES_FIELD_NUMBER: _ClassVar[int]
    STREAM_SOURCES_FIELD_NUMBER: _ClassVar[int]
    NAMED_QUERIES_FIELD_NUMBER: _ClassVar[int]
    DATABASE_SOURCES_V2_FIELD_NUMBER: _ClassVar[int]
    DATABASE_SOURCE_GROUPS_FIELD_NUMBER: _ClassVar[int]
    STREAM_SOURCES_V2_FIELD_NUMBER: _ClassVar[int]
    feature_sets: _containers.RepeatedCompositeFieldContainer[FeatureSet]
    resolvers: _containers.RepeatedCompositeFieldContainer[Resolver]
    stream_resolvers: _containers.RepeatedCompositeFieldContainer[StreamResolver]
    sink_resolvers: _containers.RepeatedCompositeFieldContainer[SinkResolver]
    database_sources: _containers.RepeatedCompositeFieldContainer[_sources_pb2.DatabaseSource]
    stream_sources: _containers.RepeatedCompositeFieldContainer[_sources_pb2.StreamSource]
    named_queries: _containers.RepeatedCompositeFieldContainer[NamedQuery]
    database_sources_v2: _containers.RepeatedCompositeFieldContainer[_sources_pb2_1.DatabaseSource]
    database_source_groups: _containers.RepeatedCompositeFieldContainer[_sources_pb2_1.DatabaseSourceGroup]
    stream_sources_v2: _containers.RepeatedCompositeFieldContainer[_sources_pb2_1.StreamSource]
    def __init__(
        self,
        feature_sets: _Optional[_Iterable[_Union[FeatureSet, _Mapping]]] = ...,
        resolvers: _Optional[_Iterable[_Union[Resolver, _Mapping]]] = ...,
        stream_resolvers: _Optional[_Iterable[_Union[StreamResolver, _Mapping]]] = ...,
        sink_resolvers: _Optional[_Iterable[_Union[SinkResolver, _Mapping]]] = ...,
        database_sources: _Optional[_Iterable[_Union[_sources_pb2.DatabaseSource, _Mapping]]] = ...,
        stream_sources: _Optional[_Iterable[_Union[_sources_pb2.StreamSource, _Mapping]]] = ...,
        named_queries: _Optional[_Iterable[_Union[NamedQuery, _Mapping]]] = ...,
        database_sources_v2: _Optional[_Iterable[_Union[_sources_pb2_1.DatabaseSource, _Mapping]]] = ...,
        database_source_groups: _Optional[_Iterable[_Union[_sources_pb2_1.DatabaseSourceGroup, _Mapping]]] = ...,
        stream_sources_v2: _Optional[_Iterable[_Union[_sources_pb2_1.StreamSource, _Mapping]]] = ...,
    ) -> None: ...

class NamedQuery(_message.Message):
    __slots__ = (
        "name",
        "query_version",
        "input",
        "output",
        "tags",
        "description",
        "owner",
        "meta",
        "staleness",
        "planner_options",
        "file_name",
        "deployment_id",
        "source_file_reference",
        "additional_logged_features",
        "valid_plan_not_required",
    )
    class MetaEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    class StalenessEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _duration_pb2.Duration
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...
        ) -> None: ...

    class PlannerOptionsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    NAME_FIELD_NUMBER: _ClassVar[int]
    QUERY_VERSION_FIELD_NUMBER: _ClassVar[int]
    INPUT_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    META_FIELD_NUMBER: _ClassVar[int]
    STALENESS_FIELD_NUMBER: _ClassVar[int]
    PLANNER_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FILE_REFERENCE_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_LOGGED_FEATURES_FIELD_NUMBER: _ClassVar[int]
    VALID_PLAN_NOT_REQUIRED_FIELD_NUMBER: _ClassVar[int]
    name: str
    query_version: str
    input: _containers.RepeatedScalarFieldContainer[str]
    output: _containers.RepeatedScalarFieldContainer[str]
    tags: _containers.RepeatedScalarFieldContainer[str]
    description: str
    owner: str
    meta: _containers.ScalarMap[str, str]
    staleness: _containers.MessageMap[str, _duration_pb2.Duration]
    planner_options: _containers.ScalarMap[str, str]
    file_name: str
    deployment_id: str
    source_file_reference: SourceFileReference
    additional_logged_features: _containers.RepeatedScalarFieldContainer[str]
    valid_plan_not_required: bool
    def __init__(
        self,
        name: _Optional[str] = ...,
        query_version: _Optional[str] = ...,
        input: _Optional[_Iterable[str]] = ...,
        output: _Optional[_Iterable[str]] = ...,
        tags: _Optional[_Iterable[str]] = ...,
        description: _Optional[str] = ...,
        owner: _Optional[str] = ...,
        meta: _Optional[_Mapping[str, str]] = ...,
        staleness: _Optional[_Mapping[str, _duration_pb2.Duration]] = ...,
        planner_options: _Optional[_Mapping[str, str]] = ...,
        file_name: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
        source_file_reference: _Optional[_Union[SourceFileReference, _Mapping]] = ...,
        additional_logged_features: _Optional[_Iterable[str]] = ...,
        valid_plan_not_required: bool = ...,
    ) -> None: ...

class FeatureSet(_message.Message):
    __slots__ = (
        "name",
        "features",
        "max_staleness_duration",
        "is_singleton",
        "tags",
        "owner",
        "doc",
        "etl_offline_to_online",
        "class_path",
    )
    NAME_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    MAX_STALENESS_DURATION_FIELD_NUMBER: _ClassVar[int]
    IS_SINGLETON_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    DOC_FIELD_NUMBER: _ClassVar[int]
    ETL_OFFLINE_TO_ONLINE_FIELD_NUMBER: _ClassVar[int]
    CLASS_PATH_FIELD_NUMBER: _ClassVar[int]
    name: str
    features: _containers.RepeatedCompositeFieldContainer[FeatureType]
    max_staleness_duration: _duration_pb2.Duration
    is_singleton: bool
    tags: _containers.RepeatedScalarFieldContainer[str]
    owner: str
    doc: str
    etl_offline_to_online: bool
    class_path: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        features: _Optional[_Iterable[_Union[FeatureType, _Mapping]]] = ...,
        max_staleness_duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        is_singleton: bool = ...,
        tags: _Optional[_Iterable[str]] = ...,
        owner: _Optional[str] = ...,
        doc: _Optional[str] = ...,
        etl_offline_to_online: bool = ...,
        class_path: _Optional[str] = ...,
    ) -> None: ...

class FeatureType(_message.Message):
    __slots__ = ("scalar", "has_one", "has_many", "feature_time", "windowed", "group_by")
    SCALAR_FIELD_NUMBER: _ClassVar[int]
    HAS_ONE_FIELD_NUMBER: _ClassVar[int]
    HAS_MANY_FIELD_NUMBER: _ClassVar[int]
    FEATURE_TIME_FIELD_NUMBER: _ClassVar[int]
    WINDOWED_FIELD_NUMBER: _ClassVar[int]
    GROUP_BY_FIELD_NUMBER: _ClassVar[int]
    scalar: ScalarFeatureType
    has_one: HasOneFeatureType
    has_many: HasManyFeatureType
    feature_time: FeatureTimeFeatureType
    windowed: WindowedFeatureType
    group_by: GroupByFeatureType
    def __init__(
        self,
        scalar: _Optional[_Union[ScalarFeatureType, _Mapping]] = ...,
        has_one: _Optional[_Union[HasOneFeatureType, _Mapping]] = ...,
        has_many: _Optional[_Union[HasManyFeatureType, _Mapping]] = ...,
        feature_time: _Optional[_Union[FeatureTimeFeatureType, _Mapping]] = ...,
        windowed: _Optional[_Union[WindowedFeatureType, _Mapping]] = ...,
        group_by: _Optional[_Union[GroupByFeatureType, _Mapping]] = ...,
    ) -> None: ...

class FeatureReference(_message.Message):
    __slots__ = ("name", "namespace", "path", "df")
    NAME_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    DF_FIELD_NUMBER: _ClassVar[int]
    name: str
    namespace: str
    path: _containers.RepeatedCompositeFieldContainer[FeatureReference]
    df: DataFrameType
    def __init__(
        self,
        name: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        path: _Optional[_Iterable[_Union[FeatureReference, _Mapping]]] = ...,
        df: _Optional[_Union[DataFrameType, _Mapping]] = ...,
    ) -> None: ...

class DataFrameType(_message.Message):
    __slots__ = ("root_namespace", "required_columns", "optional_columns", "filter", "limit")
    ROOT_NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    OPTIONAL_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    root_namespace: str
    required_columns: _containers.RepeatedCompositeFieldContainer[FeatureReference]
    optional_columns: _containers.RepeatedCompositeFieldContainer[FeatureReference]
    filter: _expression_pb2.LogicalExprNode
    limit: int
    def __init__(
        self,
        root_namespace: _Optional[str] = ...,
        required_columns: _Optional[_Iterable[_Union[FeatureReference, _Mapping]]] = ...,
        optional_columns: _Optional[_Iterable[_Union[FeatureReference, _Mapping]]] = ...,
        filter: _Optional[_Union[_expression_pb2.LogicalExprNode, _Mapping]] = ...,
        limit: _Optional[int] = ...,
    ) -> None: ...

class GroupByFeatureType(_message.Message):
    __slots__ = (
        "name",
        "namespace",
        "is_nullable",
        "internal_version",
        "arrow_type",
        "aggregation",
        "window_durations",
        "expression",
        "default_value",
        "tags",
        "description",
        "owner",
        "validations",
        "attribute_name",
    )
    NAME_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    IS_NULLABLE_FIELD_NUMBER: _ClassVar[int]
    INTERNAL_VERSION_FIELD_NUMBER: _ClassVar[int]
    ARROW_TYPE_FIELD_NUMBER: _ClassVar[int]
    AGGREGATION_FIELD_NUMBER: _ClassVar[int]
    WINDOW_DURATIONS_FIELD_NUMBER: _ClassVar[int]
    EXPRESSION_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_VALUE_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    VALIDATIONS_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    namespace: str
    is_nullable: bool
    internal_version: int
    arrow_type: _arrow_pb2.ArrowType
    aggregation: WindowAggregation
    window_durations: _containers.RepeatedCompositeFieldContainer[_duration_pb2.Duration]
    expression: _expression_pb2.LogicalExprNode
    default_value: _arrow_pb2.ScalarValue
    tags: _containers.RepeatedScalarFieldContainer[str]
    description: str
    owner: str
    validations: _containers.RepeatedCompositeFieldContainer[FeatureValidation]
    attribute_name: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        is_nullable: bool = ...,
        internal_version: _Optional[int] = ...,
        arrow_type: _Optional[_Union[_arrow_pb2.ArrowType, _Mapping]] = ...,
        aggregation: _Optional[_Union[WindowAggregation, _Mapping]] = ...,
        window_durations: _Optional[_Iterable[_Union[_duration_pb2.Duration, _Mapping]]] = ...,
        expression: _Optional[_Union[_expression_pb2.LogicalExprNode, _Mapping]] = ...,
        default_value: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...,
        tags: _Optional[_Iterable[str]] = ...,
        description: _Optional[str] = ...,
        owner: _Optional[str] = ...,
        validations: _Optional[_Iterable[_Union[FeatureValidation, _Mapping]]] = ...,
        attribute_name: _Optional[str] = ...,
    ) -> None: ...

class ScalarFeatureType(_message.Message):
    __slots__ = (
        "name",
        "namespace",
        "is_autogenerated",
        "no_display",
        "is_primary",
        "is_nullable",
        "internal_version",
        "max_staleness_duration",
        "offline_ttl_duration",
        "arrow_type",
        "version",
        "window_info",
        "default_value",
        "tags",
        "description",
        "owner",
        "expression",
        "validations",
        "last_for",
        "etl_offline_to_online",
        "is_distance_pseudofeature",
        "attribute_name",
        "is_deprecated",
        "cache_strategy",
        "store_online",
        "store_offline",
    )
    NAME_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    IS_AUTOGENERATED_FIELD_NUMBER: _ClassVar[int]
    NO_DISPLAY_FIELD_NUMBER: _ClassVar[int]
    IS_PRIMARY_FIELD_NUMBER: _ClassVar[int]
    IS_NULLABLE_FIELD_NUMBER: _ClassVar[int]
    INTERNAL_VERSION_FIELD_NUMBER: _ClassVar[int]
    MAX_STALENESS_DURATION_FIELD_NUMBER: _ClassVar[int]
    OFFLINE_TTL_DURATION_FIELD_NUMBER: _ClassVar[int]
    ARROW_TYPE_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    WINDOW_INFO_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_VALUE_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    EXPRESSION_FIELD_NUMBER: _ClassVar[int]
    VALIDATIONS_FIELD_NUMBER: _ClassVar[int]
    LAST_FOR_FIELD_NUMBER: _ClassVar[int]
    ETL_OFFLINE_TO_ONLINE_FIELD_NUMBER: _ClassVar[int]
    IS_DISTANCE_PSEUDOFEATURE_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_NAME_FIELD_NUMBER: _ClassVar[int]
    IS_DEPRECATED_FIELD_NUMBER: _ClassVar[int]
    CACHE_STRATEGY_FIELD_NUMBER: _ClassVar[int]
    STORE_ONLINE_FIELD_NUMBER: _ClassVar[int]
    STORE_OFFLINE_FIELD_NUMBER: _ClassVar[int]
    name: str
    namespace: str
    is_autogenerated: bool
    no_display: bool
    is_primary: bool
    is_nullable: bool
    internal_version: int
    max_staleness_duration: _duration_pb2.Duration
    offline_ttl_duration: _duration_pb2.Duration
    arrow_type: _arrow_pb2.ArrowType
    version: VersionInfo
    window_info: WindowInfo
    default_value: _arrow_pb2.ScalarValue
    tags: _containers.RepeatedScalarFieldContainer[str]
    description: str
    owner: str
    expression: _expression_pb2.LogicalExprNode
    validations: _containers.RepeatedCompositeFieldContainer[FeatureValidation]
    last_for: FeatureReference
    etl_offline_to_online: bool
    is_distance_pseudofeature: bool
    attribute_name: str
    is_deprecated: bool
    cache_strategy: CacheStrategy
    store_online: bool
    store_offline: bool
    def __init__(
        self,
        name: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        is_autogenerated: bool = ...,
        no_display: bool = ...,
        is_primary: bool = ...,
        is_nullable: bool = ...,
        internal_version: _Optional[int] = ...,
        max_staleness_duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        offline_ttl_duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        arrow_type: _Optional[_Union[_arrow_pb2.ArrowType, _Mapping]] = ...,
        version: _Optional[_Union[VersionInfo, _Mapping]] = ...,
        window_info: _Optional[_Union[WindowInfo, _Mapping]] = ...,
        default_value: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...,
        tags: _Optional[_Iterable[str]] = ...,
        description: _Optional[str] = ...,
        owner: _Optional[str] = ...,
        expression: _Optional[_Union[_expression_pb2.LogicalExprNode, _Mapping]] = ...,
        validations: _Optional[_Iterable[_Union[FeatureValidation, _Mapping]]] = ...,
        last_for: _Optional[_Union[FeatureReference, _Mapping]] = ...,
        etl_offline_to_online: bool = ...,
        is_distance_pseudofeature: bool = ...,
        attribute_name: _Optional[str] = ...,
        is_deprecated: bool = ...,
        cache_strategy: _Optional[_Union[CacheStrategy, str]] = ...,
        store_online: bool = ...,
        store_offline: bool = ...,
    ) -> None: ...

class HasOneFeatureType(_message.Message):
    __slots__ = (
        "name",
        "namespace",
        "foreign_namespace",
        "join",
        "is_nullable",
        "is_autogenerated",
        "tags",
        "description",
        "owner",
        "attribute_name",
    )
    NAME_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    FOREIGN_NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    JOIN_FIELD_NUMBER: _ClassVar[int]
    IS_NULLABLE_FIELD_NUMBER: _ClassVar[int]
    IS_AUTOGENERATED_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    namespace: str
    foreign_namespace: str
    join: _expression_pb2.LogicalExprNode
    is_nullable: bool
    is_autogenerated: bool
    tags: _containers.RepeatedScalarFieldContainer[str]
    description: str
    owner: str
    attribute_name: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        foreign_namespace: _Optional[str] = ...,
        join: _Optional[_Union[_expression_pb2.LogicalExprNode, _Mapping]] = ...,
        is_nullable: bool = ...,
        is_autogenerated: bool = ...,
        tags: _Optional[_Iterable[str]] = ...,
        description: _Optional[str] = ...,
        owner: _Optional[str] = ...,
        attribute_name: _Optional[str] = ...,
    ) -> None: ...

class HasManyFeatureType(_message.Message):
    __slots__ = (
        "name",
        "namespace",
        "foreign_namespace",
        "join",
        "is_autogenerated",
        "max_staleness_duration",
        "tags",
        "description",
        "owner",
        "attribute_name",
    )
    NAME_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    FOREIGN_NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    JOIN_FIELD_NUMBER: _ClassVar[int]
    IS_AUTOGENERATED_FIELD_NUMBER: _ClassVar[int]
    MAX_STALENESS_DURATION_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    namespace: str
    foreign_namespace: str
    join: _expression_pb2.LogicalExprNode
    is_autogenerated: bool
    max_staleness_duration: _duration_pb2.Duration
    tags: _containers.RepeatedScalarFieldContainer[str]
    description: str
    owner: str
    attribute_name: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        foreign_namespace: _Optional[str] = ...,
        join: _Optional[_Union[_expression_pb2.LogicalExprNode, _Mapping]] = ...,
        is_autogenerated: bool = ...,
        max_staleness_duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        tags: _Optional[_Iterable[str]] = ...,
        description: _Optional[str] = ...,
        owner: _Optional[str] = ...,
        attribute_name: _Optional[str] = ...,
    ) -> None: ...

class FeatureTimeFeatureType(_message.Message):
    __slots__ = ("name", "namespace", "is_autogenerated", "tags", "description", "owner", "attribute_name")
    NAME_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    IS_AUTOGENERATED_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    namespace: str
    is_autogenerated: bool
    tags: _containers.RepeatedScalarFieldContainer[str]
    description: str
    owner: str
    attribute_name: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        is_autogenerated: bool = ...,
        tags: _Optional[_Iterable[str]] = ...,
        description: _Optional[str] = ...,
        owner: _Optional[str] = ...,
        attribute_name: _Optional[str] = ...,
    ) -> None: ...

class WindowedFeatureType(_message.Message):
    __slots__ = ("name", "namespace", "is_autogenerated", "window_durations", "attribute_name")
    NAME_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    IS_AUTOGENERATED_FIELD_NUMBER: _ClassVar[int]
    WINDOW_DURATIONS_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    namespace: str
    is_autogenerated: bool
    window_durations: _containers.RepeatedCompositeFieldContainer[_duration_pb2.Duration]
    attribute_name: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        is_autogenerated: bool = ...,
        window_durations: _Optional[_Iterable[_Union[_duration_pb2.Duration, _Mapping]]] = ...,
        attribute_name: _Optional[str] = ...,
    ) -> None: ...

class WindowAggregation(_message.Message):
    __slots__ = (
        "namespace",
        "group_by",
        "bucket_duration",
        "aggregation",
        "aggregate_on",
        "arrow_type",
        "filters",
        "backfill_resolver",
        "backfill_lookback_duration",
        "backfill_start_time",
        "continuous_resolver",
        "continuous_buffer_duration",
        "backfill_schedule",
        "bucket_start",
    )
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    GROUP_BY_FIELD_NUMBER: _ClassVar[int]
    BUCKET_DURATION_FIELD_NUMBER: _ClassVar[int]
    AGGREGATION_FIELD_NUMBER: _ClassVar[int]
    AGGREGATE_ON_FIELD_NUMBER: _ClassVar[int]
    ARROW_TYPE_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    BACKFILL_RESOLVER_FIELD_NUMBER: _ClassVar[int]
    BACKFILL_LOOKBACK_DURATION_FIELD_NUMBER: _ClassVar[int]
    BACKFILL_START_TIME_FIELD_NUMBER: _ClassVar[int]
    CONTINUOUS_RESOLVER_FIELD_NUMBER: _ClassVar[int]
    CONTINUOUS_BUFFER_DURATION_FIELD_NUMBER: _ClassVar[int]
    BACKFILL_SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    BUCKET_START_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    group_by: _containers.RepeatedCompositeFieldContainer[FeatureReference]
    bucket_duration: _duration_pb2.Duration
    aggregation: str
    aggregate_on: FeatureReference
    arrow_type: _arrow_pb2.ArrowType
    filters: _containers.RepeatedCompositeFieldContainer[_expression_pb2.LogicalExprNode]
    backfill_resolver: str
    backfill_lookback_duration: _duration_pb2.Duration
    backfill_start_time: _timestamp_pb2.Timestamp
    continuous_resolver: str
    continuous_buffer_duration: _duration_pb2.Duration
    backfill_schedule: str
    bucket_start: _timestamp_pb2.Timestamp
    def __init__(
        self,
        namespace: _Optional[str] = ...,
        group_by: _Optional[_Iterable[_Union[FeatureReference, _Mapping]]] = ...,
        bucket_duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        aggregation: _Optional[str] = ...,
        aggregate_on: _Optional[_Union[FeatureReference, _Mapping]] = ...,
        arrow_type: _Optional[_Union[_arrow_pb2.ArrowType, _Mapping]] = ...,
        filters: _Optional[_Iterable[_Union[_expression_pb2.LogicalExprNode, _Mapping]]] = ...,
        backfill_resolver: _Optional[str] = ...,
        backfill_lookback_duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        backfill_start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        continuous_resolver: _Optional[str] = ...,
        continuous_buffer_duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        backfill_schedule: _Optional[str] = ...,
        bucket_start: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class WindowInfo(_message.Message):
    __slots__ = ("duration", "aggregation")
    DURATION_FIELD_NUMBER: _ClassVar[int]
    AGGREGATION_FIELD_NUMBER: _ClassVar[int]
    duration: _duration_pb2.Duration
    aggregation: WindowAggregation
    def __init__(
        self,
        duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        aggregation: _Optional[_Union[WindowAggregation, _Mapping]] = ...,
    ) -> None: ...

class FeatureInput(_message.Message):
    __slots__ = ("feature", "default_value")
    FEATURE_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_VALUE_FIELD_NUMBER: _ClassVar[int]
    feature: FeatureReference
    default_value: _arrow_pb2.ScalarValue
    def __init__(
        self,
        feature: _Optional[_Union[FeatureReference, _Mapping]] = ...,
        default_value: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...,
    ) -> None: ...

class ResolverInput(_message.Message):
    __slots__ = ("feature", "df", "state")
    FEATURE_FIELD_NUMBER: _ClassVar[int]
    DF_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    feature: FeatureInput
    df: DataFrameType
    state: ResolverState
    def __init__(
        self,
        feature: _Optional[_Union[FeatureInput, _Mapping]] = ...,
        df: _Optional[_Union[DataFrameType, _Mapping]] = ...,
        state: _Optional[_Union[ResolverState, _Mapping]] = ...,
    ) -> None: ...

class ResolverOutput(_message.Message):
    __slots__ = ("feature", "df")
    FEATURE_FIELD_NUMBER: _ClassVar[int]
    DF_FIELD_NUMBER: _ClassVar[int]
    feature: FeatureReference
    df: DataFrameType
    def __init__(
        self,
        feature: _Optional[_Union[FeatureReference, _Mapping]] = ...,
        df: _Optional[_Union[DataFrameType, _Mapping]] = ...,
    ) -> None: ...

class Resolver(_message.Message):
    __slots__ = (
        "fqn",
        "kind",
        "inputs",
        "outputs",
        "is_generator",
        "data_sources",
        "machine_type",
        "tags",
        "owner",
        "doc",
        "environments",
        "timeout_duration",
        "schedule",
        "when",
        "cron_filter",
        "function",
        "resource_hint",
        "is_static",
        "is_total",
        "unique_on",
        "partitioned_by",
        "data_sources_v2",
        "static_operation",
        "sql_settings",
    )
    FQN_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATOR_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCES_FIELD_NUMBER: _ClassVar[int]
    MACHINE_TYPE_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    DOC_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENTS_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_DURATION_FIELD_NUMBER: _ClassVar[int]
    SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    WHEN_FIELD_NUMBER: _ClassVar[int]
    CRON_FILTER_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_HINT_FIELD_NUMBER: _ClassVar[int]
    IS_STATIC_FIELD_NUMBER: _ClassVar[int]
    IS_TOTAL_FIELD_NUMBER: _ClassVar[int]
    UNIQUE_ON_FIELD_NUMBER: _ClassVar[int]
    PARTITIONED_BY_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCES_V2_FIELD_NUMBER: _ClassVar[int]
    STATIC_OPERATION_FIELD_NUMBER: _ClassVar[int]
    SQL_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    fqn: str
    kind: ResolverKind
    inputs: _containers.RepeatedCompositeFieldContainer[ResolverInput]
    outputs: _containers.RepeatedCompositeFieldContainer[ResolverOutput]
    is_generator: bool
    data_sources: _containers.RepeatedCompositeFieldContainer[_sources_pb2.DatabaseSourceReference]
    machine_type: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    owner: str
    doc: str
    environments: _containers.RepeatedScalarFieldContainer[str]
    timeout_duration: _duration_pb2.Duration
    schedule: Schedule
    when: _expression_pb2.LogicalExprNode
    cron_filter: CronFilterWithFeatureArgs
    function: FunctionReference
    resource_hint: ResourceHint
    is_static: bool
    is_total: bool
    unique_on: _containers.RepeatedScalarFieldContainer[str]
    partitioned_by: _containers.RepeatedScalarFieldContainer[str]
    data_sources_v2: _containers.RepeatedCompositeFieldContainer[_sources_pb2_1.DatabaseSourceReference]
    static_operation: _expression_pb2.LogicalExprNode
    sql_settings: SQLResolverSettings
    def __init__(
        self,
        fqn: _Optional[str] = ...,
        kind: _Optional[_Union[ResolverKind, str]] = ...,
        inputs: _Optional[_Iterable[_Union[ResolverInput, _Mapping]]] = ...,
        outputs: _Optional[_Iterable[_Union[ResolverOutput, _Mapping]]] = ...,
        is_generator: bool = ...,
        data_sources: _Optional[_Iterable[_Union[_sources_pb2.DatabaseSourceReference, _Mapping]]] = ...,
        machine_type: _Optional[str] = ...,
        tags: _Optional[_Iterable[str]] = ...,
        owner: _Optional[str] = ...,
        doc: _Optional[str] = ...,
        environments: _Optional[_Iterable[str]] = ...,
        timeout_duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        schedule: _Optional[_Union[Schedule, _Mapping]] = ...,
        when: _Optional[_Union[_expression_pb2.LogicalExprNode, _Mapping]] = ...,
        cron_filter: _Optional[_Union[CronFilterWithFeatureArgs, _Mapping]] = ...,
        function: _Optional[_Union[FunctionReference, _Mapping]] = ...,
        resource_hint: _Optional[_Union[ResourceHint, str]] = ...,
        is_static: bool = ...,
        is_total: bool = ...,
        unique_on: _Optional[_Iterable[str]] = ...,
        partitioned_by: _Optional[_Iterable[str]] = ...,
        data_sources_v2: _Optional[_Iterable[_Union[_sources_pb2_1.DatabaseSourceReference, _Mapping]]] = ...,
        static_operation: _Optional[_Union[_expression_pb2.LogicalExprNode, _Mapping]] = ...,
        sql_settings: _Optional[_Union[SQLResolverSettings, _Mapping]] = ...,
    ) -> None: ...

class SinkResolver(_message.Message):
    __slots__ = (
        "fqn",
        "inputs",
        "buffer_size",
        "debounce_duration",
        "max_delay_duration",
        "upsert",
        "stream_source",
        "database_source",
        "stream_source_v2",
        "database_source_v2",
        "machine_type",
        "doc",
        "owner",
        "environments",
        "timeout_duration",
        "function",
    )
    FQN_FIELD_NUMBER: _ClassVar[int]
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    BUFFER_SIZE_FIELD_NUMBER: _ClassVar[int]
    DEBOUNCE_DURATION_FIELD_NUMBER: _ClassVar[int]
    MAX_DELAY_DURATION_FIELD_NUMBER: _ClassVar[int]
    UPSERT_FIELD_NUMBER: _ClassVar[int]
    STREAM_SOURCE_FIELD_NUMBER: _ClassVar[int]
    DATABASE_SOURCE_FIELD_NUMBER: _ClassVar[int]
    STREAM_SOURCE_V2_FIELD_NUMBER: _ClassVar[int]
    DATABASE_SOURCE_V2_FIELD_NUMBER: _ClassVar[int]
    MACHINE_TYPE_FIELD_NUMBER: _ClassVar[int]
    DOC_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENTS_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_DURATION_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    fqn: str
    inputs: _containers.RepeatedCompositeFieldContainer[ResolverInput]
    buffer_size: int
    debounce_duration: _duration_pb2.Duration
    max_delay_duration: _duration_pb2.Duration
    upsert: bool
    stream_source: _sources_pb2.StreamSourceReference
    database_source: _sources_pb2.DatabaseSourceReference
    stream_source_v2: _sources_pb2_1.StreamSourceReference
    database_source_v2: _sources_pb2_1.DatabaseSourceReference
    machine_type: str
    doc: str
    owner: str
    environments: _containers.RepeatedScalarFieldContainer[str]
    timeout_duration: _duration_pb2.Duration
    function: FunctionReference
    def __init__(
        self,
        fqn: _Optional[str] = ...,
        inputs: _Optional[_Iterable[_Union[ResolverInput, _Mapping]]] = ...,
        buffer_size: _Optional[int] = ...,
        debounce_duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        max_delay_duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        upsert: bool = ...,
        stream_source: _Optional[_Union[_sources_pb2.StreamSourceReference, _Mapping]] = ...,
        database_source: _Optional[_Union[_sources_pb2.DatabaseSourceReference, _Mapping]] = ...,
        stream_source_v2: _Optional[_Union[_sources_pb2_1.StreamSourceReference, _Mapping]] = ...,
        database_source_v2: _Optional[_Union[_sources_pb2_1.DatabaseSourceReference, _Mapping]] = ...,
        machine_type: _Optional[str] = ...,
        doc: _Optional[str] = ...,
        owner: _Optional[str] = ...,
        environments: _Optional[_Iterable[str]] = ...,
        timeout_duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        function: _Optional[_Union[FunctionReference, _Mapping]] = ...,
    ) -> None: ...

class ParseInfo(_message.Message):
    __slots__ = (
        "parse_function",
        "parse_function_input_type",
        "parse_function_output_type",
        "is_parse_function_output_optional",
    )
    PARSE_FUNCTION_FIELD_NUMBER: _ClassVar[int]
    PARSE_FUNCTION_INPUT_TYPE_FIELD_NUMBER: _ClassVar[int]
    PARSE_FUNCTION_OUTPUT_TYPE_FIELD_NUMBER: _ClassVar[int]
    IS_PARSE_FUNCTION_OUTPUT_OPTIONAL_FIELD_NUMBER: _ClassVar[int]
    parse_function: FunctionReference
    parse_function_input_type: _arrow_pb2.ArrowType
    parse_function_output_type: _arrow_pb2.ArrowType
    is_parse_function_output_optional: bool
    def __init__(
        self,
        parse_function: _Optional[_Union[FunctionReference, _Mapping]] = ...,
        parse_function_input_type: _Optional[_Union[_arrow_pb2.ArrowType, _Mapping]] = ...,
        parse_function_output_type: _Optional[_Union[_arrow_pb2.ArrowType, _Mapping]] = ...,
        is_parse_function_output_optional: bool = ...,
    ) -> None: ...

class StreamResolver(_message.Message):
    __slots__ = (
        "fqn",
        "params",
        "outputs",
        "explicit_schema",
        "keys",
        "source",
        "parse_info",
        "mode",
        "environments",
        "timeout_duration",
        "timestamp_attribute_name",
        "owner",
        "doc",
        "machine_type",
        "function",
        "source_v2",
        "updates_materialized_aggregations",
    )
    FQN_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    EXPLICIT_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    KEYS_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    PARSE_INFO_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENTS_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_DURATION_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_ATTRIBUTE_NAME_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    DOC_FIELD_NUMBER: _ClassVar[int]
    MACHINE_TYPE_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    SOURCE_V2_FIELD_NUMBER: _ClassVar[int]
    UPDATES_MATERIALIZED_AGGREGATIONS_FIELD_NUMBER: _ClassVar[int]
    fqn: str
    params: _containers.RepeatedCompositeFieldContainer[StreamResolverParam]
    outputs: _containers.RepeatedCompositeFieldContainer[ResolverOutput]
    explicit_schema: _arrow_pb2.ArrowType
    keys: _containers.RepeatedCompositeFieldContainer[StreamKey]
    source: _sources_pb2.StreamSourceReference
    parse_info: ParseInfo
    mode: WindowMode
    environments: _containers.RepeatedScalarFieldContainer[str]
    timeout_duration: _duration_pb2.Duration
    timestamp_attribute_name: str
    owner: str
    doc: str
    machine_type: str
    function: FunctionReference
    source_v2: _sources_pb2_1.StreamSourceReference
    updates_materialized_aggregations: bool
    def __init__(
        self,
        fqn: _Optional[str] = ...,
        params: _Optional[_Iterable[_Union[StreamResolverParam, _Mapping]]] = ...,
        outputs: _Optional[_Iterable[_Union[ResolverOutput, _Mapping]]] = ...,
        explicit_schema: _Optional[_Union[_arrow_pb2.ArrowType, _Mapping]] = ...,
        keys: _Optional[_Iterable[_Union[StreamKey, _Mapping]]] = ...,
        source: _Optional[_Union[_sources_pb2.StreamSourceReference, _Mapping]] = ...,
        parse_info: _Optional[_Union[ParseInfo, _Mapping]] = ...,
        mode: _Optional[_Union[WindowMode, str]] = ...,
        environments: _Optional[_Iterable[str]] = ...,
        timeout_duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        timestamp_attribute_name: _Optional[str] = ...,
        owner: _Optional[str] = ...,
        doc: _Optional[str] = ...,
        machine_type: _Optional[str] = ...,
        function: _Optional[_Union[FunctionReference, _Mapping]] = ...,
        source_v2: _Optional[_Union[_sources_pb2_1.StreamSourceReference, _Mapping]] = ...,
        updates_materialized_aggregations: bool = ...,
    ) -> None: ...

class ResolverState(_message.Message):
    __slots__ = ("initial", "arrow_type")
    INITIAL_FIELD_NUMBER: _ClassVar[int]
    ARROW_TYPE_FIELD_NUMBER: _ClassVar[int]
    initial: _arrow_pb2.ScalarValue
    arrow_type: _arrow_pb2.ArrowType
    def __init__(
        self,
        initial: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...,
        arrow_type: _Optional[_Union[_arrow_pb2.ArrowType, _Mapping]] = ...,
    ) -> None: ...

class StreamResolverParam(_message.Message):
    __slots__ = ("message", "message_window", "state")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_WINDOW_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    message: StreamResolverParamMessage
    message_window: StreamResolverParamMessageWindow
    state: ResolverState
    def __init__(
        self,
        message: _Optional[_Union[StreamResolverParamMessage, _Mapping]] = ...,
        message_window: _Optional[_Union[StreamResolverParamMessageWindow, _Mapping]] = ...,
        state: _Optional[_Union[ResolverState, _Mapping]] = ...,
    ) -> None: ...

class StreamResolverParamMessageWindow(_message.Message):
    __slots__ = ("name", "arrow_type")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ARROW_TYPE_FIELD_NUMBER: _ClassVar[int]
    name: str
    arrow_type: _arrow_pb2.ArrowType
    def __init__(
        self, name: _Optional[str] = ..., arrow_type: _Optional[_Union[_arrow_pb2.ArrowType, _Mapping]] = ...
    ) -> None: ...

class StreamResolverParamMessage(_message.Message):
    __slots__ = ("name", "arrow_type")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ARROW_TYPE_FIELD_NUMBER: _ClassVar[int]
    name: str
    arrow_type: _arrow_pb2.ArrowType
    def __init__(
        self, name: _Optional[str] = ..., arrow_type: _Optional[_Union[_arrow_pb2.ArrowType, _Mapping]] = ...
    ) -> None: ...

class FunctionReference(_message.Message):
    __slots__ = ("name", "module", "file_name", "function_definition", "source_line", "captured_globals")
    NAME_FIELD_NUMBER: _ClassVar[int]
    MODULE_FIELD_NUMBER: _ClassVar[int]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_DEFINITION_FIELD_NUMBER: _ClassVar[int]
    SOURCE_LINE_FIELD_NUMBER: _ClassVar[int]
    CAPTURED_GLOBALS_FIELD_NUMBER: _ClassVar[int]
    name: str
    module: str
    file_name: str
    function_definition: str
    source_line: int
    captured_globals: _containers.RepeatedCompositeFieldContainer[FunctionReferenceCapturedGlobal]
    def __init__(
        self,
        name: _Optional[str] = ...,
        module: _Optional[str] = ...,
        file_name: _Optional[str] = ...,
        function_definition: _Optional[str] = ...,
        source_line: _Optional[int] = ...,
        captured_globals: _Optional[_Iterable[_Union[FunctionReferenceCapturedGlobal, _Mapping]]] = ...,
    ) -> None: ...

class FunctionReferenceCapturedGlobal(_message.Message):
    __slots__ = (
        "global_name",
        "builtin",
        "feature_class",
        "enum",
        "module",
        "module_member",
        "function",
        "struct",
        "variable",
        "source_reference",
    )
    GLOBAL_NAME_FIELD_NUMBER: _ClassVar[int]
    BUILTIN_FIELD_NUMBER: _ClassVar[int]
    FEATURE_CLASS_FIELD_NUMBER: _ClassVar[int]
    ENUM_FIELD_NUMBER: _ClassVar[int]
    MODULE_FIELD_NUMBER: _ClassVar[int]
    MODULE_MEMBER_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    STRUCT_FIELD_NUMBER: _ClassVar[int]
    VARIABLE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_REFERENCE_FIELD_NUMBER: _ClassVar[int]
    global_name: str
    builtin: FunctionGlobalCapturedBuiltin
    feature_class: FunctionGlobalCapturedFeatureClass
    enum: FunctionGlobalCapturedEnum
    module: FunctionGlobalCapturedModule
    module_member: FunctionGlobalCapturedModuleMember
    function: FunctionGlobalCapturedFunction
    struct: FunctionGlobalCapturedStruct
    variable: FunctionGlobalCapturedVariable
    source_reference: SourceFileReference
    def __init__(
        self,
        global_name: _Optional[str] = ...,
        builtin: _Optional[_Union[FunctionGlobalCapturedBuiltin, _Mapping]] = ...,
        feature_class: _Optional[_Union[FunctionGlobalCapturedFeatureClass, _Mapping]] = ...,
        enum: _Optional[_Union[FunctionGlobalCapturedEnum, _Mapping]] = ...,
        module: _Optional[_Union[FunctionGlobalCapturedModule, _Mapping]] = ...,
        module_member: _Optional[_Union[FunctionGlobalCapturedModuleMember, _Mapping]] = ...,
        function: _Optional[_Union[FunctionGlobalCapturedFunction, _Mapping]] = ...,
        struct: _Optional[_Union[FunctionGlobalCapturedStruct, _Mapping]] = ...,
        variable: _Optional[_Union[FunctionGlobalCapturedVariable, _Mapping]] = ...,
        source_reference: _Optional[_Union[SourceFileReference, _Mapping]] = ...,
    ) -> None: ...

class FunctionGlobalCapturedBuiltin(_message.Message):
    __slots__ = ("builtin_name",)
    BUILTIN_NAME_FIELD_NUMBER: _ClassVar[int]
    builtin_name: str
    def __init__(self, builtin_name: _Optional[str] = ...) -> None: ...

class FunctionGlobalCapturedVariable(_message.Message):
    __slots__ = ("module", "name")
    MODULE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    module: str
    name: str
    def __init__(self, module: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class FunctionGlobalCapturedStruct(_message.Message):
    __slots__ = ("module", "name", "pa_dtype")
    MODULE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PA_DTYPE_FIELD_NUMBER: _ClassVar[int]
    module: str
    name: str
    pa_dtype: _arrow_pb2.ArrowType
    def __init__(
        self,
        module: _Optional[str] = ...,
        name: _Optional[str] = ...,
        pa_dtype: _Optional[_Union[_arrow_pb2.ArrowType, _Mapping]] = ...,
    ) -> None: ...

class FunctionGlobalCapturedEnum(_message.Message):
    __slots__ = ("module", "name", "member_map", "bases")
    class MemberMapEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _arrow_pb2.ScalarValue
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...
        ) -> None: ...

    MODULE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    MEMBER_MAP_FIELD_NUMBER: _ClassVar[int]
    BASES_FIELD_NUMBER: _ClassVar[int]
    module: str
    name: str
    member_map: _containers.MessageMap[str, _arrow_pb2.ScalarValue]
    bases: _containers.RepeatedCompositeFieldContainer[_arrow_pb2.ArrowType]
    def __init__(
        self,
        module: _Optional[str] = ...,
        name: _Optional[str] = ...,
        member_map: _Optional[_Mapping[str, _arrow_pb2.ScalarValue]] = ...,
        bases: _Optional[_Iterable[_Union[_arrow_pb2.ArrowType, _Mapping]]] = ...,
    ) -> None: ...

class FunctionGlobalCapturedFeatureClass(_message.Message):
    __slots__ = ("feature_class_name",)
    FEATURE_CLASS_NAME_FIELD_NUMBER: _ClassVar[int]
    feature_class_name: str
    def __init__(self, feature_class_name: _Optional[str] = ...) -> None: ...

class FunctionGlobalCapturedModule(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class FunctionGlobalCapturedModuleMember(_message.Message):
    __slots__ = ("module_name", "qualname")
    MODULE_NAME_FIELD_NUMBER: _ClassVar[int]
    QUALNAME_FIELD_NUMBER: _ClassVar[int]
    module_name: str
    qualname: str
    def __init__(self, module_name: _Optional[str] = ..., qualname: _Optional[str] = ...) -> None: ...

class FunctionGlobalCapturedFunction(_message.Message):
    __slots__ = ("source", "captured_globals", "module", "name")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    CAPTURED_GLOBALS_FIELD_NUMBER: _ClassVar[int]
    MODULE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    source: str
    captured_globals: _containers.RepeatedCompositeFieldContainer[FunctionReferenceCapturedGlobal]
    module: str
    name: str
    def __init__(
        self,
        source: _Optional[str] = ...,
        captured_globals: _Optional[_Iterable[_Union[FunctionReferenceCapturedGlobal, _Mapping]]] = ...,
        module: _Optional[str] = ...,
        name: _Optional[str] = ...,
    ) -> None: ...

class SourceFileReference(_message.Message):
    __slots__ = ("range", "code", "file_name")
    RANGE_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    range: _lsp_pb2.Range
    code: str
    file_name: str
    def __init__(
        self,
        range: _Optional[_Union[_lsp_pb2.Range, _Mapping]] = ...,
        code: _Optional[str] = ...,
        file_name: _Optional[str] = ...,
    ) -> None: ...

class StreamKey(_message.Message):
    __slots__ = ("key", "feature")
    KEY_FIELD_NUMBER: _ClassVar[int]
    FEATURE_FIELD_NUMBER: _ClassVar[int]
    key: str
    feature: FeatureReference
    def __init__(
        self, key: _Optional[str] = ..., feature: _Optional[_Union[FeatureReference, _Mapping]] = ...
    ) -> None: ...

class SQLResolverSettings(_message.Message):
    __slots__ = ("finalizer", "incremental_settings", "fields_root_fqn")
    class FieldsRootFqnEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    FINALIZER_FIELD_NUMBER: _ClassVar[int]
    INCREMENTAL_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    FIELDS_ROOT_FQN_FIELD_NUMBER: _ClassVar[int]
    finalizer: Finalizer
    incremental_settings: IncrementalSettings
    fields_root_fqn: _containers.ScalarMap[str, str]
    def __init__(
        self,
        finalizer: _Optional[_Union[Finalizer, str]] = ...,
        incremental_settings: _Optional[_Union[IncrementalSettings, _Mapping]] = ...,
        fields_root_fqn: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...

class IncrementalSettings(_message.Message):
    __slots__ = ("mode", "lookback_period", "incremental_column", "timestamp_mode")
    MODE_FIELD_NUMBER: _ClassVar[int]
    LOOKBACK_PERIOD_FIELD_NUMBER: _ClassVar[int]
    INCREMENTAL_COLUMN_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_MODE_FIELD_NUMBER: _ClassVar[int]
    mode: IncrementalMode
    lookback_period: _duration_pb2.Duration
    incremental_column: str
    timestamp_mode: IncrementalTimestampMode
    def __init__(
        self,
        mode: _Optional[_Union[IncrementalMode, str]] = ...,
        lookback_period: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        incremental_column: _Optional[str] = ...,
        timestamp_mode: _Optional[_Union[IncrementalTimestampMode, str]] = ...,
    ) -> None: ...

class CronFilterWithFeatureArgs(_message.Message):
    __slots__ = ("filter", "args")
    FILTER_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    filter: FunctionReference
    args: _containers.RepeatedCompositeFieldContainer[FeatureReference]
    def __init__(
        self,
        filter: _Optional[_Union[FunctionReference, _Mapping]] = ...,
        args: _Optional[_Iterable[_Union[FeatureReference, _Mapping]]] = ...,
    ) -> None: ...

class Schedule(_message.Message):
    __slots__ = ("crontab", "duration", "filter", "sample")
    CRONTAB_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_FIELD_NUMBER: _ClassVar[int]
    crontab: str
    duration: _duration_pb2.Duration
    filter: FunctionReference
    sample: FunctionReference
    def __init__(
        self,
        crontab: _Optional[str] = ...,
        duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        filter: _Optional[_Union[FunctionReference, _Mapping]] = ...,
        sample: _Optional[_Union[FunctionReference, _Mapping]] = ...,
    ) -> None: ...

class FeatureValidation(_message.Message):
    __slots__ = (
        "min",
        "max",
        "min_length",
        "max_length",
        "min_arrow",
        "max_arrow",
        "min_length_arrow",
        "max_length_arrow",
        "contains",
        "strict",
    )
    MIN_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    MIN_LENGTH_FIELD_NUMBER: _ClassVar[int]
    MAX_LENGTH_FIELD_NUMBER: _ClassVar[int]
    MIN_ARROW_FIELD_NUMBER: _ClassVar[int]
    MAX_ARROW_FIELD_NUMBER: _ClassVar[int]
    MIN_LENGTH_ARROW_FIELD_NUMBER: _ClassVar[int]
    MAX_LENGTH_ARROW_FIELD_NUMBER: _ClassVar[int]
    CONTAINS_FIELD_NUMBER: _ClassVar[int]
    STRICT_FIELD_NUMBER: _ClassVar[int]
    min: float
    max: float
    min_length: int
    max_length: int
    min_arrow: _arrow_pb2.ScalarValue
    max_arrow: _arrow_pb2.ScalarValue
    min_length_arrow: _arrow_pb2.ScalarValue
    max_length_arrow: _arrow_pb2.ScalarValue
    contains: _arrow_pb2.ScalarValue
    strict: bool
    def __init__(
        self,
        min: _Optional[float] = ...,
        max: _Optional[float] = ...,
        min_length: _Optional[int] = ...,
        max_length: _Optional[int] = ...,
        min_arrow: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...,
        max_arrow: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...,
        min_length_arrow: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...,
        max_length_arrow: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...,
        contains: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...,
        strict: bool = ...,
    ) -> None: ...

class VersionInfo(_message.Message):
    __slots__ = ("default", "maximum")
    DEFAULT_FIELD_NUMBER: _ClassVar[int]
    MAXIMUM_FIELD_NUMBER: _ClassVar[int]
    default: int
    maximum: int
    def __init__(self, default: _Optional[int] = ..., maximum: _Optional[int] = ...) -> None: ...

class StrictValidation(_message.Message):
    __slots__ = ("feature", "validations")
    FEATURE_FIELD_NUMBER: _ClassVar[int]
    VALIDATIONS_FIELD_NUMBER: _ClassVar[int]
    feature: FeatureReference
    validations: _containers.RepeatedCompositeFieldContainer[FeatureValidation]
    def __init__(
        self,
        feature: _Optional[_Union[FeatureReference, _Mapping]] = ...,
        validations: _Optional[_Iterable[_Union[FeatureValidation, _Mapping]]] = ...,
    ) -> None: ...
