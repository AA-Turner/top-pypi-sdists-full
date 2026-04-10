from chalk._gen.chalk.arrow.v1 import arrow_pb2 as _arrow_pb2
from chalk._gen.chalk.expression.v1 import expression_pb2 as _expression_pb2
from chalk._gen.chalk.graph.v1 import graph_pb2 as _graph_pb2
from chalk._gen.chalk.planner.v1 import feature_types_pb2 as _feature_types_pb2
from chalk._gen.chalk.planner.v1 import symbolic_value_pb2 as _symbolic_value_pb2
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

class OperatorType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OPERATOR_TYPE_UNSPECIFIED: _ClassVar[OperatorType]
    OPERATOR_TYPE_ADD_CHILD_INDEX_COL: _ClassVar[OperatorType]
    OPERATOR_TYPE_ADD_INDEX_COL: _ClassVar[OperatorType]
    OPERATOR_TYPE_BATCH_AGG_OPERATOR: _ClassVar[OperatorType]
    OPERATOR_TYPE_BATCH_DWHAGG_OPERATOR: _ClassVar[OperatorType]
    OPERATOR_TYPE_BATCH_RENAME: _ClassVar[OperatorType]
    OPERATOR_TYPE_BIGTABLE_CACHE_LOOKUP: _ClassVar[OperatorType]
    OPERATOR_TYPE_CACHE_LOOKUP: _ClassVar[OperatorType]
    OPERATOR_TYPE_CACHE_LOOKUP_HAS_MANY: _ClassVar[OperatorType]
    OPERATOR_TYPE_COMPUTE_CRON_OUTPUT_SUMMARY: _ClassVar[OperatorType]
    OPERATOR_TYPE_COMPUTE_RELEVANT_ROW_MASK: _ClassVar[OperatorType]
    OPERATOR_TYPE_CPP_CACHE_LOOKUP: _ClassVar[OperatorType]
    OPERATOR_TYPE_DATAFRAME_MERGE_OPERATOR: _ClassVar[OperatorType]
    OPERATOR_TYPE_DATASET_SCAN: _ClassVar[OperatorType]
    OPERATOR_TYPE_DEBUG_COMMENT_OPERATOR: _ClassVar[OperatorType]
    OPERATOR_TYPE_DEFAULT_INJECTOR: _ClassVar[OperatorType]
    OPERATOR_TYPE_DISTINCT_ON: _ClassVar[OperatorType]
    OPERATOR_TYPE_DROP_CHILD_INDEX_COL: _ClassVar[OperatorType]
    OPERATOR_TYPE_DROP_COLUMNS: _ClassVar[OperatorType]
    OPERATOR_TYPE_DYNAMO_DBCACHE_LOOKUP: _ClassVar[OperatorType]
    OPERATOR_TYPE_EXPLODE_HAS_MANY_OPERATOR: _ClassVar[OperatorType]
    OPERATOR_TYPE_EXTRA_TABLES_TO_SCALARS: _ClassVar[OperatorType]
    OPERATOR_TYPE_FILTER_MISSING: _ClassVar[OperatorType]
    OPERATOR_TYPE_FILTER_RELEVANT_ROWS: _ClassVar[OperatorType]
    OPERATOR_TYPE_FINAL_PROJECT: _ClassVar[OperatorType]
    OPERATOR_TYPE_GIVENS_SCAN: _ClassVar[OperatorType]
    OPERATOR_TYPE_HAS_MANY_INPUT_OPERATOR: _ClassVar[OperatorType]
    OPERATOR_TYPE_HAS_MANY_OUTPUT_JOIN_OPERATOR: _ClassVar[OperatorType]
    OPERATOR_TYPE_IGNORE_OUTPUT: _ClassVar[OperatorType]
    OPERATOR_TYPE_INTERMEDIATE_FEATURE_METRIC_RECORDING_OPERATOR: _ClassVar[OperatorType]
    OPERATOR_TYPE_JOIN_SINGLETONS_OPERATOR: _ClassVar[OperatorType]
    OPERATOR_TYPE_LATERAL_JOIN_INPUT_OPERATOR: _ClassVar[OperatorType]
    OPERATOR_TYPE_LATERAL_JOIN_OUTPUT_OPERATOR: _ClassVar[OperatorType]
    OPERATOR_TYPE_LATERAL_JOIN_RESOLVER: _ClassVar[OperatorType]
    OPERATOR_TYPE_LIFT_RESULT_TO_GROUP: _ClassVar[OperatorType]
    OPERATOR_TYPE_LIGHTNING_REDIS_CACHE_LOOKUP: _ClassVar[OperatorType]
    OPERATOR_TYPE_MERGE_JOIN_OPERATOR: _ClassVar[OperatorType]
    OPERATOR_TYPE_METRICS_PUBLISHER: _ClassVar[OperatorType]
    OPERATOR_TYPE_NARY_MERGE_JOIN_OPERATOR: _ClassVar[OperatorType]
    OPERATOR_TYPE_NEAREST_NEIGHBOR_SUB_PLAN_JOIN: _ClassVar[OperatorType]
    OPERATOR_TYPE_NEW_DATAFRAME_RESOLVER_OPERATOR: _ClassVar[OperatorType]
    OPERATOR_TYPE_NEW_OFFLINE_CACHE_LOOKUP: _ClassVar[OperatorType]
    OPERATOR_TYPE_NON_BUS_PERSIST_OPERATOR: _ClassVar[OperatorType]
    OPERATOR_TYPE_OFFLINE_CACHE_SAMPLER: _ClassVar[OperatorType]
    OPERATOR_TYPE_ONE_TO_ONE_SCALAR_RESOLVER: _ClassVar[OperatorType]
    OPERATOR_TYPE_ONLINE_STORE_AGG_WRITER: _ClassVar[OperatorType]
    OPERATOR_TYPE_ONLINE_VECTOR_SEARCH: _ClassVar[OperatorType]
    OPERATOR_TYPE_OPTIMISTIC_LOAD: _ClassVar[OperatorType]
    OPERATOR_TYPE_OUTPUT_UNDERSCORE_OPERATOR: _ClassVar[OperatorType]
    OPERATOR_TYPE_PACK_GROUPS_INTO_STRUCTS: _ClassVar[OperatorType]
    OPERATOR_TYPE_PARQUET_WRITER: _ClassVar[OperatorType]
    OPERATOR_TYPE_PRELOADED_TABLE_OPERATOR: _ClassVar[OperatorType]
    OPERATOR_TYPE_PROJECT: _ClassVar[OperatorType]
    OPERATOR_TYPE_PROMOTE_SPINE: _ClassVar[OperatorType]
    OPERATOR_TYPE_PUSH_DFTO_RESULT: _ClassVar[OperatorType]
    OPERATOR_TYPE_PUSH_HAS_MANY_TO_RESULT: _ClassVar[OperatorType]
    OPERATOR_TYPE_REMOVE_LARGE_LISTS_FROM_SCHEMA: _ClassVar[OperatorType]
    OPERATOR_TYPE_RENAME_INDEX_COLUMN_OPERATOR: _ClassVar[OperatorType]
    OPERATOR_TYPE_REPLAY: _ClassVar[OperatorType]
    OPERATOR_TYPE_RESULT_BUS_PERSIST_OPERATOR_V2: _ClassVar[OperatorType]
    OPERATOR_TYPE_RUN_IN_BACKGROUND: _ClassVar[OperatorType]
    OPERATOR_TYPE_SQLDATAFRAME_RESOLVER_OPERATOR: _ClassVar[OperatorType]
    OPERATOR_TYPE_SQLLATERAL_JOIN_RESOLVER_OPERATOR: _ClassVar[OperatorType]
    OPERATOR_TYPE_SQLSCALAR_RESOLVER_OPERATOR: _ClassVar[OperatorType]
    OPERATOR_TYPE_STATS_COLLECTOR: _ClassVar[OperatorType]
    OPERATOR_TYPE_STREAMING_AGG_WRITE_OPERATOR: _ClassVar[OperatorType]
    OPERATOR_TYPE_SUB_PLAN_FILTER: _ClassVar[OperatorType]
    OPERATOR_TYPE_SUB_PLAN_JOIN: _ClassVar[OperatorType]
    OPERATOR_TYPE_SYMBOLIC_EXPRESSION_FALLBACK: _ClassVar[OperatorType]
    OPERATOR_TYPE_UNDERSCORE_SCALAR_RESOLVER_OPERATOR: _ClassVar[OperatorType]
    OPERATOR_TYPE_UNION_OPERATOR: _ClassVar[OperatorType]
    OPERATOR_TYPE_UNLOADED_RESOLVER_SCAN: _ClassVar[OperatorType]
    OPERATOR_TYPE_VALUES_PERSISTER: _ClassVar[OperatorType]

OPERATOR_TYPE_UNSPECIFIED: OperatorType
OPERATOR_TYPE_ADD_CHILD_INDEX_COL: OperatorType
OPERATOR_TYPE_ADD_INDEX_COL: OperatorType
OPERATOR_TYPE_BATCH_AGG_OPERATOR: OperatorType
OPERATOR_TYPE_BATCH_DWHAGG_OPERATOR: OperatorType
OPERATOR_TYPE_BATCH_RENAME: OperatorType
OPERATOR_TYPE_BIGTABLE_CACHE_LOOKUP: OperatorType
OPERATOR_TYPE_CACHE_LOOKUP: OperatorType
OPERATOR_TYPE_CACHE_LOOKUP_HAS_MANY: OperatorType
OPERATOR_TYPE_COMPUTE_CRON_OUTPUT_SUMMARY: OperatorType
OPERATOR_TYPE_COMPUTE_RELEVANT_ROW_MASK: OperatorType
OPERATOR_TYPE_CPP_CACHE_LOOKUP: OperatorType
OPERATOR_TYPE_DATAFRAME_MERGE_OPERATOR: OperatorType
OPERATOR_TYPE_DATASET_SCAN: OperatorType
OPERATOR_TYPE_DEBUG_COMMENT_OPERATOR: OperatorType
OPERATOR_TYPE_DEFAULT_INJECTOR: OperatorType
OPERATOR_TYPE_DISTINCT_ON: OperatorType
OPERATOR_TYPE_DROP_CHILD_INDEX_COL: OperatorType
OPERATOR_TYPE_DROP_COLUMNS: OperatorType
OPERATOR_TYPE_DYNAMO_DBCACHE_LOOKUP: OperatorType
OPERATOR_TYPE_EXPLODE_HAS_MANY_OPERATOR: OperatorType
OPERATOR_TYPE_EXTRA_TABLES_TO_SCALARS: OperatorType
OPERATOR_TYPE_FILTER_MISSING: OperatorType
OPERATOR_TYPE_FILTER_RELEVANT_ROWS: OperatorType
OPERATOR_TYPE_FINAL_PROJECT: OperatorType
OPERATOR_TYPE_GIVENS_SCAN: OperatorType
OPERATOR_TYPE_HAS_MANY_INPUT_OPERATOR: OperatorType
OPERATOR_TYPE_HAS_MANY_OUTPUT_JOIN_OPERATOR: OperatorType
OPERATOR_TYPE_IGNORE_OUTPUT: OperatorType
OPERATOR_TYPE_INTERMEDIATE_FEATURE_METRIC_RECORDING_OPERATOR: OperatorType
OPERATOR_TYPE_JOIN_SINGLETONS_OPERATOR: OperatorType
OPERATOR_TYPE_LATERAL_JOIN_INPUT_OPERATOR: OperatorType
OPERATOR_TYPE_LATERAL_JOIN_OUTPUT_OPERATOR: OperatorType
OPERATOR_TYPE_LATERAL_JOIN_RESOLVER: OperatorType
OPERATOR_TYPE_LIFT_RESULT_TO_GROUP: OperatorType
OPERATOR_TYPE_LIGHTNING_REDIS_CACHE_LOOKUP: OperatorType
OPERATOR_TYPE_MERGE_JOIN_OPERATOR: OperatorType
OPERATOR_TYPE_METRICS_PUBLISHER: OperatorType
OPERATOR_TYPE_NARY_MERGE_JOIN_OPERATOR: OperatorType
OPERATOR_TYPE_NEAREST_NEIGHBOR_SUB_PLAN_JOIN: OperatorType
OPERATOR_TYPE_NEW_DATAFRAME_RESOLVER_OPERATOR: OperatorType
OPERATOR_TYPE_NEW_OFFLINE_CACHE_LOOKUP: OperatorType
OPERATOR_TYPE_NON_BUS_PERSIST_OPERATOR: OperatorType
OPERATOR_TYPE_OFFLINE_CACHE_SAMPLER: OperatorType
OPERATOR_TYPE_ONE_TO_ONE_SCALAR_RESOLVER: OperatorType
OPERATOR_TYPE_ONLINE_STORE_AGG_WRITER: OperatorType
OPERATOR_TYPE_ONLINE_VECTOR_SEARCH: OperatorType
OPERATOR_TYPE_OPTIMISTIC_LOAD: OperatorType
OPERATOR_TYPE_OUTPUT_UNDERSCORE_OPERATOR: OperatorType
OPERATOR_TYPE_PACK_GROUPS_INTO_STRUCTS: OperatorType
OPERATOR_TYPE_PARQUET_WRITER: OperatorType
OPERATOR_TYPE_PRELOADED_TABLE_OPERATOR: OperatorType
OPERATOR_TYPE_PROJECT: OperatorType
OPERATOR_TYPE_PROMOTE_SPINE: OperatorType
OPERATOR_TYPE_PUSH_DFTO_RESULT: OperatorType
OPERATOR_TYPE_PUSH_HAS_MANY_TO_RESULT: OperatorType
OPERATOR_TYPE_REMOVE_LARGE_LISTS_FROM_SCHEMA: OperatorType
OPERATOR_TYPE_RENAME_INDEX_COLUMN_OPERATOR: OperatorType
OPERATOR_TYPE_REPLAY: OperatorType
OPERATOR_TYPE_RESULT_BUS_PERSIST_OPERATOR_V2: OperatorType
OPERATOR_TYPE_RUN_IN_BACKGROUND: OperatorType
OPERATOR_TYPE_SQLDATAFRAME_RESOLVER_OPERATOR: OperatorType
OPERATOR_TYPE_SQLLATERAL_JOIN_RESOLVER_OPERATOR: OperatorType
OPERATOR_TYPE_SQLSCALAR_RESOLVER_OPERATOR: OperatorType
OPERATOR_TYPE_STATS_COLLECTOR: OperatorType
OPERATOR_TYPE_STREAMING_AGG_WRITE_OPERATOR: OperatorType
OPERATOR_TYPE_SUB_PLAN_FILTER: OperatorType
OPERATOR_TYPE_SUB_PLAN_JOIN: OperatorType
OPERATOR_TYPE_SYMBOLIC_EXPRESSION_FALLBACK: OperatorType
OPERATOR_TYPE_UNDERSCORE_SCALAR_RESOLVER_OPERATOR: OperatorType
OPERATOR_TYPE_UNION_OPERATOR: OperatorType
OPERATOR_TYPE_UNLOADED_RESOLVER_SCAN: OperatorType
OPERATOR_TYPE_VALUES_PERSISTER: OperatorType

class BatchPlan(_message.Message):
    __slots__ = ("operators", "symbolic_values", "feature_ref_info", "auxiliary_info")
    OPERATORS_FIELD_NUMBER: _ClassVar[int]
    SYMBOLIC_VALUES_FIELD_NUMBER: _ClassVar[int]
    FEATURE_REF_INFO_FIELD_NUMBER: _ClassVar[int]
    AUXILIARY_INFO_FIELD_NUMBER: _ClassVar[int]
    operators: _containers.RepeatedCompositeFieldContainer[BatchOperator]
    symbolic_values: _containers.RepeatedCompositeFieldContainer[_symbolic_value_pb2.SymbolicValue]
    feature_ref_info: FeatureReferenceInfo
    auxiliary_info: _feature_types_pb2.AuxiliaryInfo
    def __init__(
        self,
        operators: _Optional[_Iterable[_Union[BatchOperator, _Mapping]]] = ...,
        symbolic_values: _Optional[_Iterable[_Union[_symbolic_value_pb2.SymbolicValue, _Mapping]]] = ...,
        feature_ref_info: _Optional[_Union[FeatureReferenceInfo, _Mapping]] = ...,
        auxiliary_info: _Optional[_Union[_feature_types_pb2.AuxiliaryInfo, _Mapping]] = ...,
    ) -> None: ...

class BatchOperator(_message.Message):
    __slots__ = ("operator_type", "graph_info", "arguments")
    class ArgumentsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Argument
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Argument, _Mapping]] = ...) -> None: ...

    OPERATOR_TYPE_FIELD_NUMBER: _ClassVar[int]
    GRAPH_INFO_FIELD_NUMBER: _ClassVar[int]
    ARGUMENTS_FIELD_NUMBER: _ClassVar[int]
    operator_type: OperatorType
    graph_info: GraphInfo
    arguments: _containers.MessageMap[str, Argument]
    def __init__(
        self,
        operator_type: _Optional[_Union[OperatorType, str]] = ...,
        graph_info: _Optional[_Union[GraphInfo, _Mapping]] = ...,
        arguments: _Optional[_Mapping[str, Argument]] = ...,
    ) -> None: ...

class FeatureReferenceInfo(_message.Message):
    __slots__ = ("feature_refs", "data_frame_types", "filter_expressions")
    FEATURE_REFS_FIELD_NUMBER: _ClassVar[int]
    DATA_FRAME_TYPES_FIELD_NUMBER: _ClassVar[int]
    FILTER_EXPRESSIONS_FIELD_NUMBER: _ClassVar[int]
    feature_refs: _containers.RepeatedCompositeFieldContainer[FeatureReference]
    data_frame_types: _containers.RepeatedCompositeFieldContainer[DataFrameType]
    filter_expressions: _containers.RepeatedCompositeFieldContainer[FilterExpressionParsed]
    def __init__(
        self,
        feature_refs: _Optional[_Iterable[_Union[FeatureReference, _Mapping]]] = ...,
        data_frame_types: _Optional[_Iterable[_Union[DataFrameType, _Mapping]]] = ...,
        filter_expressions: _Optional[_Iterable[_Union[FilterExpressionParsed, _Mapping]]] = ...,
    ) -> None: ...

class GraphInfo(_message.Message):
    __slots__ = ("operator_id",)
    OPERATOR_ID_FIELD_NUMBER: _ClassVar[int]
    operator_id: int
    def __init__(self, operator_id: _Optional[int] = ...) -> None: ...

class Argument(_message.Message):
    __slots__ = (
        "none",
        "bool_value",
        "double_value",
        "int_value",
        "string_value",
        "timestamp",
        "duration",
        "operator_id",
        "feature_ref",
        "bytes_value",
        "tuple",
        "submap",
        "arrow_type",
        "underscore_expr",
        "filter_expr",
        "detached_column_feature_type",
        "output_underscore_feature_type",
        "data_frame_type",
        "feature_reference",
        "symbolic_value",
        "data_frame_type_id",
        "feature_ref_id",
        "data_frame_type_id_v2",
        "feature_ref_id_v2",
        "underscore_parsed",
        "ipc_arrow_table",
    )
    NONE_FIELD_NUMBER: _ClassVar[int]
    BOOL_VALUE_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_VALUE_FIELD_NUMBER: _ClassVar[int]
    INT_VALUE_FIELD_NUMBER: _ClassVar[int]
    STRING_VALUE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    OPERATOR_ID_FIELD_NUMBER: _ClassVar[int]
    FEATURE_REF_FIELD_NUMBER: _ClassVar[int]
    BYTES_VALUE_FIELD_NUMBER: _ClassVar[int]
    TUPLE_FIELD_NUMBER: _ClassVar[int]
    SUBMAP_FIELD_NUMBER: _ClassVar[int]
    ARROW_TYPE_FIELD_NUMBER: _ClassVar[int]
    UNDERSCORE_EXPR_FIELD_NUMBER: _ClassVar[int]
    FILTER_EXPR_FIELD_NUMBER: _ClassVar[int]
    DETACHED_COLUMN_FEATURE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_UNDERSCORE_FEATURE_TYPE_FIELD_NUMBER: _ClassVar[int]
    DATA_FRAME_TYPE_FIELD_NUMBER: _ClassVar[int]
    FEATURE_REFERENCE_FIELD_NUMBER: _ClassVar[int]
    SYMBOLIC_VALUE_FIELD_NUMBER: _ClassVar[int]
    DATA_FRAME_TYPE_ID_FIELD_NUMBER: _ClassVar[int]
    FEATURE_REF_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_FRAME_TYPE_ID_V2_FIELD_NUMBER: _ClassVar[int]
    FEATURE_REF_ID_V2_FIELD_NUMBER: _ClassVar[int]
    UNDERSCORE_PARSED_FIELD_NUMBER: _ClassVar[int]
    IPC_ARROW_TABLE_FIELD_NUMBER: _ClassVar[int]
    none: Void
    bool_value: bool
    double_value: float
    int_value: int
    string_value: str
    timestamp: _timestamp_pb2.Timestamp
    duration: _duration_pb2.Duration
    operator_id: int
    feature_ref: _graph_pb2.FeatureReference
    bytes_value: bytes
    tuple: ArgumentList
    submap: ArgumentMap
    arrow_type: _arrow_pb2.ArrowType
    underscore_expr: _expression_pb2.LogicalExprNode
    filter_expr: _expression_pb2.LogicalExprNode
    detached_column_feature_type: DetachedColumnFeatureType
    output_underscore_feature_type: OutputUnderscoreFeatureType
    data_frame_type: DataFrameType
    feature_reference: FeatureReference
    symbolic_value: _symbolic_value_pb2.SymbolicValue
    data_frame_type_id: DataFrameTypeId
    feature_ref_id: FeatureReferenceId
    data_frame_type_id_v2: _feature_types_pb2.DataFrameTypeIdV2
    feature_ref_id_v2: _feature_types_pb2.FeatureReferenceIdV2
    underscore_parsed: _feature_types_pb2.UnderscoreParsedId
    ipc_arrow_table: bytes
    def __init__(
        self,
        none: _Optional[_Union[Void, _Mapping]] = ...,
        bool_value: bool = ...,
        double_value: _Optional[float] = ...,
        int_value: _Optional[int] = ...,
        string_value: _Optional[str] = ...,
        timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        operator_id: _Optional[int] = ...,
        feature_ref: _Optional[_Union[_graph_pb2.FeatureReference, _Mapping]] = ...,
        bytes_value: _Optional[bytes] = ...,
        tuple: _Optional[_Union[ArgumentList, _Mapping]] = ...,
        submap: _Optional[_Union[ArgumentMap, _Mapping]] = ...,
        arrow_type: _Optional[_Union[_arrow_pb2.ArrowType, _Mapping]] = ...,
        underscore_expr: _Optional[_Union[_expression_pb2.LogicalExprNode, _Mapping]] = ...,
        filter_expr: _Optional[_Union[_expression_pb2.LogicalExprNode, _Mapping]] = ...,
        detached_column_feature_type: _Optional[_Union[DetachedColumnFeatureType, _Mapping]] = ...,
        output_underscore_feature_type: _Optional[_Union[OutputUnderscoreFeatureType, _Mapping]] = ...,
        data_frame_type: _Optional[_Union[DataFrameType, _Mapping]] = ...,
        feature_reference: _Optional[_Union[FeatureReference, _Mapping]] = ...,
        symbolic_value: _Optional[_Union[_symbolic_value_pb2.SymbolicValue, _Mapping]] = ...,
        data_frame_type_id: _Optional[_Union[DataFrameTypeId, _Mapping]] = ...,
        feature_ref_id: _Optional[_Union[FeatureReferenceId, _Mapping]] = ...,
        data_frame_type_id_v2: _Optional[_Union[_feature_types_pb2.DataFrameTypeIdV2, _Mapping]] = ...,
        feature_ref_id_v2: _Optional[_Union[_feature_types_pb2.FeatureReferenceIdV2, _Mapping]] = ...,
        underscore_parsed: _Optional[_Union[_feature_types_pb2.UnderscoreParsedId, _Mapping]] = ...,
        ipc_arrow_table: _Optional[bytes] = ...,
    ) -> None: ...

class ArgumentMapElement(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: Argument
    value: Argument
    def __init__(
        self, key: _Optional[_Union[Argument, _Mapping]] = ..., value: _Optional[_Union[Argument, _Mapping]] = ...
    ) -> None: ...

class ArgumentMap(_message.Message):
    __slots__ = ("arguments", "keys", "values", "ordered_arguments")
    class ArgumentsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Argument
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Argument, _Mapping]] = ...) -> None: ...

    ARGUMENTS_FIELD_NUMBER: _ClassVar[int]
    KEYS_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    ORDERED_ARGUMENTS_FIELD_NUMBER: _ClassVar[int]
    arguments: _containers.MessageMap[str, Argument]
    keys: _containers.RepeatedCompositeFieldContainer[Argument]
    values: _containers.RepeatedCompositeFieldContainer[Argument]
    ordered_arguments: _containers.RepeatedCompositeFieldContainer[ArgumentMapElement]
    def __init__(
        self,
        arguments: _Optional[_Mapping[str, Argument]] = ...,
        keys: _Optional[_Iterable[_Union[Argument, _Mapping]]] = ...,
        values: _Optional[_Iterable[_Union[Argument, _Mapping]]] = ...,
        ordered_arguments: _Optional[_Iterable[_Union[ArgumentMapElement, _Mapping]]] = ...,
    ) -> None: ...

class ArgumentList(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedCompositeFieldContainer[Argument]
    def __init__(self, values: _Optional[_Iterable[_Union[Argument, _Mapping]]] = ...) -> None: ...

class Void(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DetachedColumnFeatureType(_message.Message):
    __slots__ = ("arguments",)
    class ArgumentsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Argument
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Argument, _Mapping]] = ...) -> None: ...

    ARGUMENTS_FIELD_NUMBER: _ClassVar[int]
    arguments: _containers.MessageMap[str, Argument]
    def __init__(self, arguments: _Optional[_Mapping[str, Argument]] = ...) -> None: ...

class OutputUnderscoreFeatureType(_message.Message):
    __slots__ = ("arguments",)
    class ArgumentsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Argument
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Argument, _Mapping]] = ...) -> None: ...

    ARGUMENTS_FIELD_NUMBER: _ClassVar[int]
    arguments: _containers.MessageMap[str, Argument]
    def __init__(self, arguments: _Optional[_Mapping[str, Argument]] = ...) -> None: ...

class FilterExpressionParsed(_message.Message):
    __slots__ = ("this_id", "filter_expression", "expr")
    THIS_ID_FIELD_NUMBER: _ClassVar[int]
    FILTER_EXPRESSION_FIELD_NUMBER: _ClassVar[int]
    EXPR_FIELD_NUMBER: _ClassVar[int]
    this_id: FilterExpressionParsedId
    filter_expression: _expression_pb2.LogicalExprNode
    expr: UnderscoreValue
    def __init__(
        self,
        this_id: _Optional[_Union[FilterExpressionParsedId, _Mapping]] = ...,
        filter_expression: _Optional[_Union[_expression_pb2.LogicalExprNode, _Mapping]] = ...,
        expr: _Optional[_Union[UnderscoreValue, _Mapping]] = ...,
    ) -> None: ...

class FilterExpressionParsedId(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class DataFrameType(_message.Message):
    __slots__ = (
        "this_id",
        "df",
        "filter_expression",
        "filter_expression_id",
        "optional_columns",
        "optional_column_refs",
        "required_column_refs",
    )
    THIS_ID_FIELD_NUMBER: _ClassVar[int]
    DF_FIELD_NUMBER: _ClassVar[int]
    FILTER_EXPRESSION_FIELD_NUMBER: _ClassVar[int]
    FILTER_EXPRESSION_ID_FIELD_NUMBER: _ClassVar[int]
    OPTIONAL_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    OPTIONAL_COLUMN_REFS_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_COLUMN_REFS_FIELD_NUMBER: _ClassVar[int]
    this_id: DataFrameTypeId
    df: _graph_pb2.DataFrameType
    filter_expression: _expression_pb2.LogicalExprNode
    filter_expression_id: FilterExpressionParsedId
    optional_columns: _containers.RepeatedCompositeFieldContainer[FeatureReference]
    optional_column_refs: _containers.RepeatedCompositeFieldContainer[FeatureReferenceId]
    required_column_refs: _containers.RepeatedCompositeFieldContainer[FeatureReferenceId]
    def __init__(
        self,
        this_id: _Optional[_Union[DataFrameTypeId, _Mapping]] = ...,
        df: _Optional[_Union[_graph_pb2.DataFrameType, _Mapping]] = ...,
        filter_expression: _Optional[_Union[_expression_pb2.LogicalExprNode, _Mapping]] = ...,
        filter_expression_id: _Optional[_Union[FilterExpressionParsedId, _Mapping]] = ...,
        optional_columns: _Optional[_Iterable[_Union[FeatureReference, _Mapping]]] = ...,
        optional_column_refs: _Optional[_Iterable[_Union[FeatureReferenceId, _Mapping]]] = ...,
        required_column_refs: _Optional[_Iterable[_Union[FeatureReferenceId, _Mapping]]] = ...,
    ) -> None: ...

class DataFrameTypeId(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class FeatureReference(_message.Message):
    __slots__ = ("this_id", "feature_ref", "path", "path_ids", "df", "df_id")
    THIS_ID_FIELD_NUMBER: _ClassVar[int]
    FEATURE_REF_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    PATH_IDS_FIELD_NUMBER: _ClassVar[int]
    DF_FIELD_NUMBER: _ClassVar[int]
    DF_ID_FIELD_NUMBER: _ClassVar[int]
    this_id: FeatureReferenceId
    feature_ref: _graph_pb2.FeatureReference
    path: _containers.RepeatedCompositeFieldContainer[FeatureReference]
    path_ids: _containers.RepeatedCompositeFieldContainer[FeatureReferenceId]
    df: DataFrameType
    df_id: DataFrameTypeId
    def __init__(
        self,
        this_id: _Optional[_Union[FeatureReferenceId, _Mapping]] = ...,
        feature_ref: _Optional[_Union[_graph_pb2.FeatureReference, _Mapping]] = ...,
        path: _Optional[_Iterable[_Union[FeatureReference, _Mapping]]] = ...,
        path_ids: _Optional[_Iterable[_Union[FeatureReferenceId, _Mapping]]] = ...,
        df: _Optional[_Union[DataFrameType, _Mapping]] = ...,
        df_id: _Optional[_Union[DataFrameTypeId, _Mapping]] = ...,
    ) -> None: ...

class FeatureReferenceId(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class UnderscoreValue(_message.Message):
    __slots__ = ("original_underscore", "codec_info")
    ORIGINAL_UNDERSCORE_FIELD_NUMBER: _ClassVar[int]
    CODEC_INFO_FIELD_NUMBER: _ClassVar[int]
    original_underscore: _expression_pb2.LogicalExprNode
    codec_info: UnderscoreValueCodecInfo
    def __init__(
        self,
        original_underscore: _Optional[_Union[_expression_pb2.LogicalExprNode, _Mapping]] = ...,
        codec_info: _Optional[_Union[UnderscoreValueCodecInfo, _Mapping]] = ...,
    ) -> None: ...

class UnderscoreValueCodecInfo(_message.Message):
    __slots__ = ("for_feature", "root_namespace", "root_underscore_behavior")
    FOR_FEATURE_FIELD_NUMBER: _ClassVar[int]
    ROOT_NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    ROOT_UNDERSCORE_BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    for_feature: FeatureReferenceId
    root_namespace: str
    root_underscore_behavior: RootUnderscoreBehavior
    def __init__(
        self,
        for_feature: _Optional[_Union[FeatureReferenceId, _Mapping]] = ...,
        root_namespace: _Optional[str] = ...,
        root_underscore_behavior: _Optional[_Union[RootUnderscoreBehavior, _Mapping]] = ...,
    ) -> None: ...

class RootUnderscoreBehavior(_message.Message):
    __slots__ = ("resolver", "stream_resolver")
    RESOLVER_FIELD_NUMBER: _ClassVar[int]
    STREAM_RESOLVER_FIELD_NUMBER: _ClassVar[int]
    resolver: ResolverRootUnderscoreBehavior
    stream_resolver: StreamResolverRootUnderscoreBehavior
    def __init__(
        self,
        resolver: _Optional[_Union[ResolverRootUnderscoreBehavior, _Mapping]] = ...,
        stream_resolver: _Optional[_Union[StreamResolverRootUnderscoreBehavior, _Mapping]] = ...,
    ) -> None: ...

class ResolverRootUnderscoreBehavior(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class StreamResolverRootUnderscoreBehavior(_message.Message):
    __slots__ = ("message_dtype",)
    MESSAGE_DTYPE_FIELD_NUMBER: _ClassVar[int]
    message_dtype: _arrow_pb2.ArrowType
    def __init__(self, message_dtype: _Optional[_Union[_arrow_pb2.ArrowType, _Mapping]] = ...) -> None: ...
