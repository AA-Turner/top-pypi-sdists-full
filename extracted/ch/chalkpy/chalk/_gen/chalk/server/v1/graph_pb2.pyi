from chalk._gen.chalk.arrow.v1 import arrow_pb2 as _arrow_pb2
from chalk._gen.chalk.artifacts.v1 import diff_pb2 as _diff_pb2
from chalk._gen.chalk.artifacts.v1 import export_pb2 as _export_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.common.v1 import chalk_error_pb2 as _chalk_error_pb2
from chalk._gen.chalk.graph.v1 import graph_pb2 as _graph_pb2
from chalk._gen.chalk.graph.v1 import source_file_reference_pb2 as _source_file_reference_pb2
from chalk._gen.chalk.graph.v1 import sql_resolver_retry_policy_pb2 as _sql_resolver_retry_policy_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
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

class DiffMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DIFF_MODE_UNSPECIFIED: _ClassVar[DiffMode]
    DIFF_MODE_FULL: _ClassVar[DiffMode]
    DIFF_MODE_SIMPLE: _ClassVar[DiffMode]

DIFF_MODE_UNSPECIFIED: DiffMode
DIFF_MODE_FULL: DiffMode
DIFF_MODE_SIMPLE: DiffMode

class FeatureSQL(_message.Message):
    __slots__ = (
        "id",
        "environment_id",
        "deployment_id",
        "fqn",
        "name",
        "namespace",
        "max_staleness",
        "etl_offline_to_online",
        "description",
        "owner",
        "tags",
        "kind_enum",
        "kind",
        "was_reset",
        "internal_version",
        "is_singleton",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    FQN_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    MAX_STALENESS_FIELD_NUMBER: _ClassVar[int]
    ETL_OFFLINE_TO_ONLINE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    KIND_ENUM_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    WAS_RESET_FIELD_NUMBER: _ClassVar[int]
    INTERNAL_VERSION_FIELD_NUMBER: _ClassVar[int]
    IS_SINGLETON_FIELD_NUMBER: _ClassVar[int]
    id: int
    environment_id: str
    deployment_id: str
    fqn: str
    name: str
    namespace: str
    max_staleness: str
    etl_offline_to_online: bool
    description: str
    owner: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    kind_enum: str
    kind: str
    was_reset: bool
    internal_version: int
    is_singleton: bool
    def __init__(
        self,
        id: _Optional[int] = ...,
        environment_id: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
        fqn: _Optional[str] = ...,
        name: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        max_staleness: _Optional[str] = ...,
        etl_offline_to_online: bool = ...,
        description: _Optional[str] = ...,
        owner: _Optional[str] = ...,
        tags: _Optional[_Iterable[str]] = ...,
        kind_enum: _Optional[str] = ...,
        kind: _Optional[str] = ...,
        was_reset: bool = ...,
        internal_version: _Optional[int] = ...,
        is_singleton: bool = ...,
    ) -> None: ...

class GetFeatureSQLResponse(_message.Message):
    __slots__ = ("features",)
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    features: _containers.RepeatedCompositeFieldContainer[FeatureSQL]
    def __init__(self, features: _Optional[_Iterable[_Union[FeatureSQL, _Mapping]]] = ...) -> None: ...

class GetFeatureSQLRequest(_message.Message):
    __slots__ = ("deployment_id",)
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    def __init__(self, deployment_id: _Optional[str] = ...) -> None: ...

class FeatureMetadata(_message.Message):
    __slots__ = (
        "fqn",
        "name",
        "namespace",
        "description",
        "owner",
        "tags",
        "max_staleness",
        "etl_offline_to_online",
        "pa_dtype",
        "nullable",
    )
    FQN_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    MAX_STALENESS_FIELD_NUMBER: _ClassVar[int]
    ETL_OFFLINE_TO_ONLINE_FIELD_NUMBER: _ClassVar[int]
    PA_DTYPE_FIELD_NUMBER: _ClassVar[int]
    NULLABLE_FIELD_NUMBER: _ClassVar[int]
    fqn: str
    name: str
    namespace: str
    description: str
    owner: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    max_staleness: str
    etl_offline_to_online: bool
    pa_dtype: _arrow_pb2.ArrowType
    nullable: bool
    def __init__(
        self,
        fqn: _Optional[str] = ...,
        name: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        description: _Optional[str] = ...,
        owner: _Optional[str] = ...,
        tags: _Optional[_Iterable[str]] = ...,
        max_staleness: _Optional[str] = ...,
        etl_offline_to_online: bool = ...,
        pa_dtype: _Optional[_Union[_arrow_pb2.ArrowType, _Mapping]] = ...,
        nullable: bool = ...,
    ) -> None: ...

class GetFeaturesMetadataResponse(_message.Message):
    __slots__ = ("features", "environment_id", "deployment_id")
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    features: _containers.RepeatedCompositeFieldContainer[FeatureMetadata]
    environment_id: str
    deployment_id: str
    def __init__(
        self,
        features: _Optional[_Iterable[_Union[FeatureMetadata, _Mapping]]] = ...,
        environment_id: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
    ) -> None: ...

class GetFeaturesMetadataRequest(_message.Message):
    __slots__ = ("fqns_filter",)
    FQNS_FILTER_FIELD_NUMBER: _ClassVar[int]
    fqns_filter: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, fqns_filter: _Optional[_Iterable[str]] = ...) -> None: ...

class UpdateGraphRequest(_message.Message):
    __slots__ = ("deployment_id", "graph", "chalkpy_version", "tag", "export")
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    GRAPH_FIELD_NUMBER: _ClassVar[int]
    CHALKPY_VERSION_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    EXPORT_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    graph: _graph_pb2.Graph
    chalkpy_version: str
    tag: str
    export: _export_pb2.Export
    def __init__(
        self,
        deployment_id: _Optional[str] = ...,
        graph: _Optional[_Union[_graph_pb2.Graph, _Mapping]] = ...,
        chalkpy_version: _Optional[str] = ...,
        tag: _Optional[str] = ...,
        export: _Optional[_Union[_export_pb2.Export, _Mapping]] = ...,
    ) -> None: ...

class UpdateGraphResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GraphFetchOptions(_message.Message):
    __slots__ = ("exclude_resolver_postprocessing", "exclude_stream_resolver_parse_info")
    EXCLUDE_RESOLVER_POSTPROCESSING_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_STREAM_RESOLVER_PARSE_INFO_FIELD_NUMBER: _ClassVar[int]
    exclude_resolver_postprocessing: bool
    exclude_stream_resolver_parse_info: bool
    def __init__(
        self, exclude_resolver_postprocessing: bool = ..., exclude_stream_resolver_parse_info: bool = ...
    ) -> None: ...

class GetGraphRequest(_message.Message):
    __slots__ = ("deployment_id", "fetch_options")
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    FETCH_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    fetch_options: GraphFetchOptions
    def __init__(
        self, deployment_id: _Optional[str] = ..., fetch_options: _Optional[_Union[GraphFetchOptions, _Mapping]] = ...
    ) -> None: ...

class GetGraphResponse(_message.Message):
    __slots__ = ("graph", "chalkpy_version", "tag", "export", "deployment_id")
    GRAPH_FIELD_NUMBER: _ClassVar[int]
    CHALKPY_VERSION_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    EXPORT_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    graph: _graph_pb2.Graph
    chalkpy_version: str
    tag: str
    export: _export_pb2.Export
    deployment_id: str
    def __init__(
        self,
        graph: _Optional[_Union[_graph_pb2.Graph, _Mapping]] = ...,
        chalkpy_version: _Optional[str] = ...,
        tag: _Optional[str] = ...,
        export: _Optional[_Union[_export_pb2.Export, _Mapping]] = ...,
        deployment_id: _Optional[str] = ...,
    ) -> None: ...

class GetResolverRequest(_message.Message):
    __slots__ = ("deployment_id", "resolver_fqn", "read_mask")
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    READ_MASK_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    resolver_fqn: str
    read_mask: _field_mask_pb2.FieldMask
    def __init__(
        self,
        deployment_id: _Optional[str] = ...,
        resolver_fqn: _Optional[str] = ...,
        read_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class GetResolverResponse(_message.Message):
    __slots__ = ("resolver",)
    RESOLVER_FIELD_NUMBER: _ClassVar[int]
    resolver: _graph_pb2.Resolver
    def __init__(self, resolver: _Optional[_Union[_graph_pb2.Resolver, _Mapping]] = ...) -> None: ...

class GetStreamResolverRequest(_message.Message):
    __slots__ = ("deployment_id", "resolver_fqn", "read_mask")
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    READ_MASK_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    resolver_fqn: str
    read_mask: _field_mask_pb2.FieldMask
    def __init__(
        self,
        deployment_id: _Optional[str] = ...,
        resolver_fqn: _Optional[str] = ...,
        read_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class GetStreamResolverResponse(_message.Message):
    __slots__ = ("stream_resolver",)
    STREAM_RESOLVER_FIELD_NUMBER: _ClassVar[int]
    stream_resolver: _graph_pb2.StreamResolver
    def __init__(self, stream_resolver: _Optional[_Union[_graph_pb2.StreamResolver, _Mapping]] = ...) -> None: ...

class PythonVersion(_message.Message):
    __slots__ = ("major", "minor", "patch")
    MAJOR_FIELD_NUMBER: _ClassVar[int]
    MINOR_FIELD_NUMBER: _ClassVar[int]
    PATCH_FIELD_NUMBER: _ClassVar[int]
    major: int
    minor: int
    patch: int
    def __init__(
        self, major: _Optional[int] = ..., minor: _Optional[int] = ..., patch: _Optional[int] = ...
    ) -> None: ...

class GetCodegenFeaturesFromGraphRequest(_message.Message):
    __slots__ = ("deployment_id", "branch", "python_version")
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    BRANCH_FIELD_NUMBER: _ClassVar[int]
    PYTHON_VERSION_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    branch: str
    python_version: PythonVersion
    def __init__(
        self,
        deployment_id: _Optional[str] = ...,
        branch: _Optional[str] = ...,
        python_version: _Optional[_Union[PythonVersion, _Mapping]] = ...,
    ) -> None: ...

class GetCodegenFeaturesFromGraphResponse(_message.Message):
    __slots__ = ("codegen", "errors")
    CODEGEN_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    codegen: str
    errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    def __init__(
        self,
        codegen: _Optional[str] = ...,
        errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...,
    ) -> None: ...

class GraphMutation(_message.Message):
    __slots__ = (
        "add_streaming_resolver",
        "update_streaming_resolver",
        "delete_streaming_resolver",
        "add_feature",
        "update_feature",
        "delete_feature",
        "add_feature_set",
        "update_feature_set",
        "delete_feature_set",
        "add_resolver",
        "update_resolver",
        "delete_resolver",
    )
    ADD_STREAMING_RESOLVER_FIELD_NUMBER: _ClassVar[int]
    UPDATE_STREAMING_RESOLVER_FIELD_NUMBER: _ClassVar[int]
    DELETE_STREAMING_RESOLVER_FIELD_NUMBER: _ClassVar[int]
    ADD_FEATURE_FIELD_NUMBER: _ClassVar[int]
    UPDATE_FEATURE_FIELD_NUMBER: _ClassVar[int]
    DELETE_FEATURE_FIELD_NUMBER: _ClassVar[int]
    ADD_FEATURE_SET_FIELD_NUMBER: _ClassVar[int]
    UPDATE_FEATURE_SET_FIELD_NUMBER: _ClassVar[int]
    DELETE_FEATURE_SET_FIELD_NUMBER: _ClassVar[int]
    ADD_RESOLVER_FIELD_NUMBER: _ClassVar[int]
    UPDATE_RESOLVER_FIELD_NUMBER: _ClassVar[int]
    DELETE_RESOLVER_FIELD_NUMBER: _ClassVar[int]
    add_streaming_resolver: AddStreamingResolver
    update_streaming_resolver: UpdateStreamingResolver
    delete_streaming_resolver: DeleteStreamingResolver
    add_feature: AddFeature
    update_feature: UpdateFeature
    delete_feature: DeleteFeature
    add_feature_set: AddFeatureSet
    update_feature_set: UpdateFeatureSet
    delete_feature_set: DeleteFeatureSet
    add_resolver: AddResolver
    update_resolver: UpdateResolver
    delete_resolver: DeleteResolver
    def __init__(
        self,
        add_streaming_resolver: _Optional[_Union[AddStreamingResolver, _Mapping]] = ...,
        update_streaming_resolver: _Optional[_Union[UpdateStreamingResolver, _Mapping]] = ...,
        delete_streaming_resolver: _Optional[_Union[DeleteStreamingResolver, _Mapping]] = ...,
        add_feature: _Optional[_Union[AddFeature, _Mapping]] = ...,
        update_feature: _Optional[_Union[UpdateFeature, _Mapping]] = ...,
        delete_feature: _Optional[_Union[DeleteFeature, _Mapping]] = ...,
        add_feature_set: _Optional[_Union[AddFeatureSet, _Mapping]] = ...,
        update_feature_set: _Optional[_Union[UpdateFeatureSet, _Mapping]] = ...,
        delete_feature_set: _Optional[_Union[DeleteFeatureSet, _Mapping]] = ...,
        add_resolver: _Optional[_Union[AddResolver, _Mapping]] = ...,
        update_resolver: _Optional[_Union[UpdateResolver, _Mapping]] = ...,
        delete_resolver: _Optional[_Union[DeleteResolver, _Mapping]] = ...,
    ) -> None: ...

class AddStreamingResolver(_message.Message):
    __slots__ = ("resolver",)
    RESOLVER_FIELD_NUMBER: _ClassVar[int]
    resolver: _graph_pb2.StreamResolver
    def __init__(self, resolver: _Optional[_Union[_graph_pb2.StreamResolver, _Mapping]] = ...) -> None: ...

class UpdateStreamingResolver(_message.Message):
    __slots__ = ("resolver_name", "resolver")
    RESOLVER_NAME_FIELD_NUMBER: _ClassVar[int]
    RESOLVER_FIELD_NUMBER: _ClassVar[int]
    resolver_name: str
    resolver: _graph_pb2.StreamResolver
    def __init__(
        self,
        resolver_name: _Optional[str] = ...,
        resolver: _Optional[_Union[_graph_pb2.StreamResolver, _Mapping]] = ...,
    ) -> None: ...

class DeleteStreamingResolver(_message.Message):
    __slots__ = ("resolver_name",)
    RESOLVER_NAME_FIELD_NUMBER: _ClassVar[int]
    resolver_name: str
    def __init__(self, resolver_name: _Optional[str] = ...) -> None: ...

class AddResolver(_message.Message):
    __slots__ = ("resolver",)
    RESOLVER_FIELD_NUMBER: _ClassVar[int]
    resolver: _graph_pb2.Resolver
    def __init__(self, resolver: _Optional[_Union[_graph_pb2.Resolver, _Mapping]] = ...) -> None: ...

class UpdateResolver(_message.Message):
    __slots__ = ("resolver_name", "resolver")
    RESOLVER_NAME_FIELD_NUMBER: _ClassVar[int]
    RESOLVER_FIELD_NUMBER: _ClassVar[int]
    resolver_name: str
    resolver: _graph_pb2.Resolver
    def __init__(
        self, resolver_name: _Optional[str] = ..., resolver: _Optional[_Union[_graph_pb2.Resolver, _Mapping]] = ...
    ) -> None: ...

class DeleteResolver(_message.Message):
    __slots__ = ("resolver_name",)
    RESOLVER_NAME_FIELD_NUMBER: _ClassVar[int]
    resolver_name: str
    def __init__(self, resolver_name: _Optional[str] = ...) -> None: ...

class AddFeature(_message.Message):
    __slots__ = ("feature_set_name", "feature")
    FEATURE_SET_NAME_FIELD_NUMBER: _ClassVar[int]
    FEATURE_FIELD_NUMBER: _ClassVar[int]
    feature_set_name: str
    feature: _graph_pb2.FeatureType
    def __init__(
        self, feature_set_name: _Optional[str] = ..., feature: _Optional[_Union[_graph_pb2.FeatureType, _Mapping]] = ...
    ) -> None: ...

class UpdateFeature(_message.Message):
    __slots__ = ("fqn", "feature")
    FQN_FIELD_NUMBER: _ClassVar[int]
    FEATURE_FIELD_NUMBER: _ClassVar[int]
    fqn: str
    feature: _graph_pb2.FeatureType
    def __init__(
        self, fqn: _Optional[str] = ..., feature: _Optional[_Union[_graph_pb2.FeatureType, _Mapping]] = ...
    ) -> None: ...

class DeleteFeature(_message.Message):
    __slots__ = ("fqn",)
    FQN_FIELD_NUMBER: _ClassVar[int]
    fqn: str
    def __init__(self, fqn: _Optional[str] = ...) -> None: ...

class AddFeatureSet(_message.Message):
    __slots__ = ("feature_set",)
    FEATURE_SET_FIELD_NUMBER: _ClassVar[int]
    feature_set: _graph_pb2.FeatureSet
    def __init__(self, feature_set: _Optional[_Union[_graph_pb2.FeatureSet, _Mapping]] = ...) -> None: ...

class UpdateFeatureSet(_message.Message):
    __slots__ = ("feature_set_name", "feature_set")
    FEATURE_SET_NAME_FIELD_NUMBER: _ClassVar[int]
    FEATURE_SET_FIELD_NUMBER: _ClassVar[int]
    feature_set_name: str
    feature_set: _graph_pb2.FeatureSet
    def __init__(
        self,
        feature_set_name: _Optional[str] = ...,
        feature_set: _Optional[_Union[_graph_pb2.FeatureSet, _Mapping]] = ...,
    ) -> None: ...

class DeleteFeatureSet(_message.Message):
    __slots__ = ("feature_set_name",)
    FEATURE_SET_NAME_FIELD_NUMBER: _ClassVar[int]
    feature_set_name: str
    def __init__(self, feature_set_name: _Optional[str] = ...) -> None: ...

class ApplyGraphUpdatesRequest(_message.Message):
    __slots__ = ("deployment_id", "mutations")
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    MUTATIONS_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    mutations: _containers.RepeatedCompositeFieldContainer[GraphMutation]
    def __init__(
        self,
        deployment_id: _Optional[str] = ...,
        mutations: _Optional[_Iterable[_Union[GraphMutation, _Mapping]]] = ...,
    ) -> None: ...

class ApplyGraphUpdatesResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TestGraphMutationsRequest(_message.Message):
    __slots__ = ("deployment_id", "mutations")
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    MUTATIONS_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    mutations: _containers.RepeatedCompositeFieldContainer[GraphMutation]
    def __init__(
        self,
        deployment_id: _Optional[str] = ...,
        mutations: _Optional[_Iterable[_Union[GraphMutation, _Mapping]]] = ...,
    ) -> None: ...

class TestGraphMutationsResponse(_message.Message):
    __slots__ = ("export", "errors")
    EXPORT_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    export: _export_pb2.Export
    errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    def __init__(
        self,
        export: _Optional[_Union[_export_pb2.Export, _Mapping]] = ...,
        errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...,
    ) -> None: ...

class ColumnList(_message.Message):
    __slots__ = ("columns",)
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    columns: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, columns: _Optional[_Iterable[str]] = ...) -> None: ...

class TableLineage(_message.Message):
    __slots__ = ("features",)
    class FeaturesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ColumnList
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ColumnList, _Mapping]] = ...) -> None: ...

    FEATURES_FIELD_NUMBER: _ClassVar[int]
    features: _containers.MessageMap[str, ColumnList]
    def __init__(self, features: _Optional[_Mapping[str, ColumnList]] = ...) -> None: ...

class DataSourceLineage(_message.Message):
    __slots__ = ("tables",)
    class TablesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: TableLineage
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[TableLineage, _Mapping]] = ...
        ) -> None: ...

    TABLES_FIELD_NUMBER: _ClassVar[int]
    tables: _containers.MessageMap[str, TableLineage]
    def __init__(self, tables: _Optional[_Mapping[str, TableLineage]] = ...) -> None: ...

class ResolverDataLineage(_message.Message):
    __slots__ = ("data_sources",)
    class DataSourcesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: DataSourceLineage
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[DataSourceLineage, _Mapping]] = ...
        ) -> None: ...

    DATA_SOURCES_FIELD_NUMBER: _ClassVar[int]
    data_sources: _containers.MessageMap[str, DataSourceLineage]
    def __init__(self, data_sources: _Optional[_Mapping[str, DataSourceLineage]] = ...) -> None: ...

class GetDataLineageIndexRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetDataLineageIndexResponse(_message.Message):
    __slots__ = ("resolver_data_lineage",)
    class ResolverDataLineageEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ResolverDataLineage
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[ResolverDataLineage, _Mapping]] = ...
        ) -> None: ...

    RESOLVER_DATA_LINEAGE_FIELD_NUMBER: _ClassVar[int]
    resolver_data_lineage: _containers.MessageMap[str, ResolverDataLineage]
    def __init__(self, resolver_data_lineage: _Optional[_Mapping[str, ResolverDataLineage]] = ...) -> None: ...

class ScheduledQueryLineage(_message.Message):
    __slots__ = ("cron_query_id", "name", "cron", "resolver_fqns", "feature_fqns", "query_plan_id")
    CRON_QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CRON_FIELD_NUMBER: _ClassVar[int]
    RESOLVER_FQNS_FIELD_NUMBER: _ClassVar[int]
    FEATURE_FQNS_FIELD_NUMBER: _ClassVar[int]
    QUERY_PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    cron_query_id: int
    name: str
    cron: str
    resolver_fqns: _containers.RepeatedScalarFieldContainer[str]
    feature_fqns: _containers.RepeatedScalarFieldContainer[str]
    query_plan_id: str
    def __init__(
        self,
        cron_query_id: _Optional[int] = ...,
        name: _Optional[str] = ...,
        cron: _Optional[str] = ...,
        resolver_fqns: _Optional[_Iterable[str]] = ...,
        feature_fqns: _Optional[_Iterable[str]] = ...,
        query_plan_id: _Optional[str] = ...,
    ) -> None: ...

class GetScheduledQueryLineageIndexRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetScheduledQueryLineageIndexResponse(_message.Message):
    __slots__ = ("scheduled_queries", "names_without_plan")
    class ScheduledQueriesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ScheduledQueryLineage
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[ScheduledQueryLineage, _Mapping]] = ...
        ) -> None: ...

    SCHEDULED_QUERIES_FIELD_NUMBER: _ClassVar[int]
    NAMES_WITHOUT_PLAN_FIELD_NUMBER: _ClassVar[int]
    scheduled_queries: _containers.MessageMap[str, ScheduledQueryLineage]
    names_without_plan: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        scheduled_queries: _Optional[_Mapping[str, ScheduledQueryLineage]] = ...,
        names_without_plan: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class OfflineTable(_message.Message):
    __slots__ = ("internal_version", "table_name", "fqn")
    INTERNAL_VERSION_FIELD_NUMBER: _ClassVar[int]
    TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    FQN_FIELD_NUMBER: _ClassVar[int]
    internal_version: int
    table_name: str
    fqn: str
    def __init__(
        self, internal_version: _Optional[int] = ..., table_name: _Optional[str] = ..., fqn: _Optional[str] = ...
    ) -> None: ...

class GetOfflineStoreTableRequest(_message.Message):
    __slots__ = ("fqn", "branch_id")
    FQN_FIELD_NUMBER: _ClassVar[int]
    BRANCH_ID_FIELD_NUMBER: _ClassVar[int]
    fqn: str
    branch_id: str
    def __init__(self, fqn: _Optional[str] = ..., branch_id: _Optional[str] = ...) -> None: ...

class GetOfflineStoreTableResponse(_message.Message):
    __slots__ = ("tables",)
    TABLES_FIELD_NUMBER: _ClassVar[int]
    tables: _containers.RepeatedCompositeFieldContainer[OfflineTable]
    def __init__(self, tables: _Optional[_Iterable[_Union[OfflineTable, _Mapping]]] = ...) -> None: ...

class GetAllOfflineStoreTablesPageToken(_message.Message):
    __slots__ = ("fqn", "internal_version")
    FQN_FIELD_NUMBER: _ClassVar[int]
    INTERNAL_VERSION_FIELD_NUMBER: _ClassVar[int]
    fqn: str
    internal_version: int
    def __init__(self, fqn: _Optional[str] = ..., internal_version: _Optional[int] = ...) -> None: ...

class GetAllOfflineStoreTablesRequest(_message.Message):
    __slots__ = ("deployment_id", "branch_id", "limit", "page_token")
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    BRANCH_ID_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    branch_id: str
    limit: int
    page_token: str
    def __init__(
        self,
        deployment_id: _Optional[str] = ...,
        branch_id: _Optional[str] = ...,
        limit: _Optional[int] = ...,
        page_token: _Optional[str] = ...,
    ) -> None: ...

class GetAllOfflineStoreTablesResponse(_message.Message):
    __slots__ = ("tables", "next_page_token")
    TABLES_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    tables: _containers.RepeatedCompositeFieldContainer[OfflineTable]
    next_page_token: str
    def __init__(
        self, tables: _Optional[_Iterable[_Union[OfflineTable, _Mapping]]] = ..., next_page_token: _Optional[str] = ...
    ) -> None: ...

class DiffDeploymentsRequest(_message.Message):
    __slots__ = ("deployment_id_before", "deployment_id_after", "diff_mode")
    DEPLOYMENT_ID_BEFORE_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_AFTER_FIELD_NUMBER: _ClassVar[int]
    DIFF_MODE_FIELD_NUMBER: _ClassVar[int]
    deployment_id_before: str
    deployment_id_after: str
    diff_mode: DiffMode
    def __init__(
        self,
        deployment_id_before: _Optional[str] = ...,
        deployment_id_after: _Optional[str] = ...,
        diff_mode: _Optional[_Union[DiffMode, str]] = ...,
    ) -> None: ...

class DiffDeploymentsResponse(_message.Message):
    __slots__ = ("deploy_id_before", "deploy_id_after", "diff")
    DEPLOY_ID_BEFORE_FIELD_NUMBER: _ClassVar[int]
    DEPLOY_ID_AFTER_FIELD_NUMBER: _ClassVar[int]
    DIFF_FIELD_NUMBER: _ClassVar[int]
    deploy_id_before: str
    deploy_id_after: str
    diff: _diff_pb2.ExportDiff
    def __init__(
        self,
        deploy_id_before: _Optional[str] = ...,
        deploy_id_after: _Optional[str] = ...,
        diff: _Optional[_Union[_diff_pb2.ExportDiff, _Mapping]] = ...,
    ) -> None: ...

class SmartDiffDeploymentRequest(_message.Message):
    __slots__ = ("deployment_id", "diff_mode")
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    DIFF_MODE_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    diff_mode: DiffMode
    def __init__(
        self, deployment_id: _Optional[str] = ..., diff_mode: _Optional[_Union[DiffMode, str]] = ...
    ) -> None: ...

class SmartDiffDeploymentResponse(_message.Message):
    __slots__ = ("deploy_id_before", "deploy_id_after", "diff")
    DEPLOY_ID_BEFORE_FIELD_NUMBER: _ClassVar[int]
    DEPLOY_ID_AFTER_FIELD_NUMBER: _ClassVar[int]
    DIFF_FIELD_NUMBER: _ClassVar[int]
    deploy_id_before: str
    deploy_id_after: str
    diff: _diff_pb2.ExportDiff
    def __init__(
        self,
        deploy_id_before: _Optional[str] = ...,
        deploy_id_after: _Optional[str] = ...,
        diff: _Optional[_Union[_diff_pb2.ExportDiff, _Mapping]] = ...,
    ) -> None: ...

class DiffCandidateRequest(_message.Message):
    __slots__ = ("candidate", "diff_mode")
    CANDIDATE_FIELD_NUMBER: _ClassVar[int]
    DIFF_MODE_FIELD_NUMBER: _ClassVar[int]
    candidate: _export_pb2.Export
    diff_mode: DiffMode
    def __init__(
        self,
        candidate: _Optional[_Union[_export_pb2.Export, _Mapping]] = ...,
        diff_mode: _Optional[_Union[DiffMode, str]] = ...,
    ) -> None: ...

class DiffCandidateResponse(_message.Message):
    __slots__ = ("deploy_id_before", "diff")
    DEPLOY_ID_BEFORE_FIELD_NUMBER: _ClassVar[int]
    DIFF_FIELD_NUMBER: _ClassVar[int]
    deploy_id_before: str
    diff: _diff_pb2.ExportDiff
    def __init__(
        self, deploy_id_before: _Optional[str] = ..., diff: _Optional[_Union[_diff_pb2.ExportDiff, _Mapping]] = ...
    ) -> None: ...
