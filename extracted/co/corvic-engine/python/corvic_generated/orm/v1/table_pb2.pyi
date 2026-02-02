from buf.validate import validate_pb2 as _validate_pb2
from corvic_generated.algorithm.graph.v1 import graph_pb2 as _graph_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class JoinType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    JOIN_TYPE_UNSPECIFIED: _ClassVar[JoinType]
    JOIN_TYPE_INNER: _ClassVar[JoinType]
    JOIN_TYPE_LEFT_OUTER: _ClassVar[JoinType]

class AggregationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AGGREGATION_TYPE_UNSPECIFIED: _ClassVar[AggregationType]
    AGGREGATION_TYPE_COUNT: _ClassVar[AggregationType]
    AGGREGATION_TYPE_AVG: _ClassVar[AggregationType]
    AGGREGATION_TYPE_MODE: _ClassVar[AggregationType]
    AGGREGATION_TYPE_MIN: _ClassVar[AggregationType]
    AGGREGATION_TYPE_MAX: _ClassVar[AggregationType]
    AGGREGATION_TYPE_SUM: _ClassVar[AggregationType]

class LogicalCombination(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LOGICAL_COMBINATION_UNSPECIFIED: _ClassVar[LogicalCombination]
    LOGICAL_COMBINATION_ANY: _ClassVar[LogicalCombination]
    LOGICAL_COMBINATION_ALL: _ClassVar[LogicalCombination]

class ComparisonType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    COMPARISON_TYPE_UNSPECIFIED: _ClassVar[ComparisonType]
    COMPARISON_TYPE_EQ: _ClassVar[ComparisonType]
    COMPARISON_TYPE_NE: _ClassVar[ComparisonType]
    COMPARISON_TYPE_LT: _ClassVar[ComparisonType]
    COMPARISON_TYPE_GT: _ClassVar[ComparisonType]
    COMPARISON_TYPE_LE: _ClassVar[ComparisonType]
    COMPARISON_TYPE_GE: _ClassVar[ComparisonType]

class FloatBitWidth(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FLOAT_BIT_WIDTH_UNSPECIFIED: _ClassVar[FloatBitWidth]
    FLOAT_BIT_WIDTH_32: _ClassVar[FloatBitWidth]
    FLOAT_BIT_WIDTH_64: _ClassVar[FloatBitWidth]
JOIN_TYPE_UNSPECIFIED: JoinType
JOIN_TYPE_INNER: JoinType
JOIN_TYPE_LEFT_OUTER: JoinType
AGGREGATION_TYPE_UNSPECIFIED: AggregationType
AGGREGATION_TYPE_COUNT: AggregationType
AGGREGATION_TYPE_AVG: AggregationType
AGGREGATION_TYPE_MODE: AggregationType
AGGREGATION_TYPE_MIN: AggregationType
AGGREGATION_TYPE_MAX: AggregationType
AGGREGATION_TYPE_SUM: AggregationType
LOGICAL_COMBINATION_UNSPECIFIED: LogicalCombination
LOGICAL_COMBINATION_ANY: LogicalCombination
LOGICAL_COMBINATION_ALL: LogicalCombination
COMPARISON_TYPE_UNSPECIFIED: ComparisonType
COMPARISON_TYPE_EQ: ComparisonType
COMPARISON_TYPE_NE: ComparisonType
COMPARISON_TYPE_LT: ComparisonType
COMPARISON_TYPE_GT: ComparisonType
COMPARISON_TYPE_LE: ComparisonType
COMPARISON_TYPE_GE: ComparisonType
FLOAT_BIT_WIDTH_UNSPECIFIED: FloatBitWidth
FLOAT_BIT_WIDTH_32: FloatBitWidth
FLOAT_BIT_WIDTH_64: FloatBitWidth

class TableComputeOp(_message.Message):
    __slots__ = ("empty", "select_from_staging", "rename_columns", "join", "select_columns", "limit_rows", "order_by", "filter_rows", "distinct_rows", "update_metadata", "set_metadata", "remove_from_metadata", "update_feature_types", "rollup_by_aggregation", "embed_node2vec_from_edge_lists", "embedding_metrics", "embedding_coordinates", "read_from_parquet", "select_from_vector_staging", "concat", "unnest_struct", "nest_into_struct", "add_literal_column", "combine_columns", "embed_column", "encode_column", "aggregate_columns", "correlate_columns", "histogram_column", "convert_column_string", "row_index", "output_csv", "truncate_list", "union", "embed_image_column", "add_decision_tree_summary", "unnest_list", "sample_rows")
    EMPTY_FIELD_NUMBER: _ClassVar[int]
    SELECT_FROM_STAGING_FIELD_NUMBER: _ClassVar[int]
    RENAME_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    JOIN_FIELD_NUMBER: _ClassVar[int]
    SELECT_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    LIMIT_ROWS_FIELD_NUMBER: _ClassVar[int]
    ORDER_BY_FIELD_NUMBER: _ClassVar[int]
    FILTER_ROWS_FIELD_NUMBER: _ClassVar[int]
    DISTINCT_ROWS_FIELD_NUMBER: _ClassVar[int]
    UPDATE_METADATA_FIELD_NUMBER: _ClassVar[int]
    SET_METADATA_FIELD_NUMBER: _ClassVar[int]
    REMOVE_FROM_METADATA_FIELD_NUMBER: _ClassVar[int]
    UPDATE_FEATURE_TYPES_FIELD_NUMBER: _ClassVar[int]
    ROLLUP_BY_AGGREGATION_FIELD_NUMBER: _ClassVar[int]
    EMBED_NODE2VEC_FROM_EDGE_LISTS_FIELD_NUMBER: _ClassVar[int]
    EMBEDDING_METRICS_FIELD_NUMBER: _ClassVar[int]
    EMBEDDING_COORDINATES_FIELD_NUMBER: _ClassVar[int]
    READ_FROM_PARQUET_FIELD_NUMBER: _ClassVar[int]
    SELECT_FROM_VECTOR_STAGING_FIELD_NUMBER: _ClassVar[int]
    CONCAT_FIELD_NUMBER: _ClassVar[int]
    UNNEST_STRUCT_FIELD_NUMBER: _ClassVar[int]
    NEST_INTO_STRUCT_FIELD_NUMBER: _ClassVar[int]
    ADD_LITERAL_COLUMN_FIELD_NUMBER: _ClassVar[int]
    COMBINE_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    EMBED_COLUMN_FIELD_NUMBER: _ClassVar[int]
    ENCODE_COLUMN_FIELD_NUMBER: _ClassVar[int]
    AGGREGATE_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    CORRELATE_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    HISTOGRAM_COLUMN_FIELD_NUMBER: _ClassVar[int]
    CONVERT_COLUMN_STRING_FIELD_NUMBER: _ClassVar[int]
    ROW_INDEX_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_CSV_FIELD_NUMBER: _ClassVar[int]
    TRUNCATE_LIST_FIELD_NUMBER: _ClassVar[int]
    UNION_FIELD_NUMBER: _ClassVar[int]
    EMBED_IMAGE_COLUMN_FIELD_NUMBER: _ClassVar[int]
    ADD_DECISION_TREE_SUMMARY_FIELD_NUMBER: _ClassVar[int]
    UNNEST_LIST_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_ROWS_FIELD_NUMBER: _ClassVar[int]
    empty: EmptyOp
    select_from_staging: SelectFromStagingOp
    rename_columns: RenameColumnsOp
    join: JoinOp
    select_columns: SelectColumnsOp
    limit_rows: LimitRowsOp
    order_by: OrderByOp
    filter_rows: FilterRowsOp
    distinct_rows: DistinctRowsOp
    update_metadata: UpdateMetadataOp
    set_metadata: SetMetadataOp
    remove_from_metadata: RemoveFromMetadataOp
    update_feature_types: UpdateFeatureTypesOp
    rollup_by_aggregation: RollupByAggregationOp
    embed_node2vec_from_edge_lists: EmbedNode2vecFromEdgeListsOp
    embedding_metrics: EmbeddingMetricsOp
    embedding_coordinates: EmbeddingCoordinatesOp
    read_from_parquet: ReadFromParquetOp
    select_from_vector_staging: SelectFromVectorStagingOp
    concat: ConcatOp
    unnest_struct: UnnestStructOp
    nest_into_struct: NestIntoStructOp
    add_literal_column: AddLiteralColumnOp
    combine_columns: CombineColumnsOp
    embed_column: EmbedColumnOp
    encode_column: EncodeColumnOp
    aggregate_columns: AggregateColumnsOp
    correlate_columns: CorrelateColumnsOp
    histogram_column: HistogramColumnOp
    convert_column_string: ConvertColumnToStringOp
    row_index: AddRowIndexOp
    output_csv: OutputCsvOp
    truncate_list: TruncateListOp
    union: UnionOp
    embed_image_column: EmbedImageColumnOp
    add_decision_tree_summary: AddDecisionTreeSummaryOp
    unnest_list: UnnestListOp
    sample_rows: SampleRowsOp
    def __init__(self, empty: _Optional[_Union[EmptyOp, _Mapping]] = ..., select_from_staging: _Optional[_Union[SelectFromStagingOp, _Mapping]] = ..., rename_columns: _Optional[_Union[RenameColumnsOp, _Mapping]] = ..., join: _Optional[_Union[JoinOp, _Mapping]] = ..., select_columns: _Optional[_Union[SelectColumnsOp, _Mapping]] = ..., limit_rows: _Optional[_Union[LimitRowsOp, _Mapping]] = ..., order_by: _Optional[_Union[OrderByOp, _Mapping]] = ..., filter_rows: _Optional[_Union[FilterRowsOp, _Mapping]] = ..., distinct_rows: _Optional[_Union[DistinctRowsOp, _Mapping]] = ..., update_metadata: _Optional[_Union[UpdateMetadataOp, _Mapping]] = ..., set_metadata: _Optional[_Union[SetMetadataOp, _Mapping]] = ..., remove_from_metadata: _Optional[_Union[RemoveFromMetadataOp, _Mapping]] = ..., update_feature_types: _Optional[_Union[UpdateFeatureTypesOp, _Mapping]] = ..., rollup_by_aggregation: _Optional[_Union[RollupByAggregationOp, _Mapping]] = ..., embed_node2vec_from_edge_lists: _Optional[_Union[EmbedNode2vecFromEdgeListsOp, _Mapping]] = ..., embedding_metrics: _Optional[_Union[EmbeddingMetricsOp, _Mapping]] = ..., embedding_coordinates: _Optional[_Union[EmbeddingCoordinatesOp, _Mapping]] = ..., read_from_parquet: _Optional[_Union[ReadFromParquetOp, _Mapping]] = ..., select_from_vector_staging: _Optional[_Union[SelectFromVectorStagingOp, _Mapping]] = ..., concat: _Optional[_Union[ConcatOp, _Mapping]] = ..., unnest_struct: _Optional[_Union[UnnestStructOp, _Mapping]] = ..., nest_into_struct: _Optional[_Union[NestIntoStructOp, _Mapping]] = ..., add_literal_column: _Optional[_Union[AddLiteralColumnOp, _Mapping]] = ..., combine_columns: _Optional[_Union[CombineColumnsOp, _Mapping]] = ..., embed_column: _Optional[_Union[EmbedColumnOp, _Mapping]] = ..., encode_column: _Optional[_Union[EncodeColumnOp, _Mapping]] = ..., aggregate_columns: _Optional[_Union[AggregateColumnsOp, _Mapping]] = ..., correlate_columns: _Optional[_Union[CorrelateColumnsOp, _Mapping]] = ..., histogram_column: _Optional[_Union[HistogramColumnOp, _Mapping]] = ..., convert_column_string: _Optional[_Union[ConvertColumnToStringOp, _Mapping]] = ..., row_index: _Optional[_Union[AddRowIndexOp, _Mapping]] = ..., output_csv: _Optional[_Union[OutputCsvOp, _Mapping]] = ..., truncate_list: _Optional[_Union[TruncateListOp, _Mapping]] = ..., union: _Optional[_Union[UnionOp, _Mapping]] = ..., embed_image_column: _Optional[_Union[EmbedImageColumnOp, _Mapping]] = ..., add_decision_tree_summary: _Optional[_Union[AddDecisionTreeSummaryOp, _Mapping]] = ..., unnest_list: _Optional[_Union[UnnestListOp, _Mapping]] = ..., sample_rows: _Optional[_Union[SampleRowsOp, _Mapping]] = ...) -> None: ...

class JoinOp(_message.Message):
    __slots__ = ("left_source", "left_join_columns", "right_source", "right_join_columns", "how")
    LEFT_SOURCE_FIELD_NUMBER: _ClassVar[int]
    LEFT_JOIN_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    RIGHT_SOURCE_FIELD_NUMBER: _ClassVar[int]
    RIGHT_JOIN_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    HOW_FIELD_NUMBER: _ClassVar[int]
    left_source: TableComputeOp
    left_join_columns: _containers.RepeatedScalarFieldContainer[str]
    right_source: TableComputeOp
    right_join_columns: _containers.RepeatedScalarFieldContainer[str]
    how: JoinType
    def __init__(self, left_source: _Optional[_Union[TableComputeOp, _Mapping]] = ..., left_join_columns: _Optional[_Iterable[str]] = ..., right_source: _Optional[_Union[TableComputeOp, _Mapping]] = ..., right_join_columns: _Optional[_Iterable[str]] = ..., how: _Optional[_Union[JoinType, str]] = ...) -> None: ...

class RenameColumnsOp(_message.Message):
    __slots__ = ("source", "old_names_to_new")
    class OldNamesToNewEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    OLD_NAMES_TO_NEW_FIELD_NUMBER: _ClassVar[int]
    source: TableComputeOp
    old_names_to_new: _containers.ScalarMap[str, str]
    def __init__(self, source: _Optional[_Union[TableComputeOp, _Mapping]] = ..., old_names_to_new: _Optional[_Mapping[str, str]] = ...) -> None: ...

class TextFeatureType(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CategoricalFeatureType(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class PrimaryKeyFeatureType(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ForeignKeyFeatureType(_message.Message):
    __slots__ = ("referenced_source_id",)
    REFERENCED_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    referenced_source_id: str
    def __init__(self, referenced_source_id: _Optional[str] = ...) -> None: ...

class IdentifierFeatureType(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class NumericalFeatureType(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MultiCategoricalFeatureType(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TimestampFeatureType(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class EmbeddingFeatureType(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class UnknownFeatureType(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ImageFeatureType(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class FeatureType(_message.Message):
    __slots__ = ("text", "categorical", "primary_key", "foreign_key", "identifier", "numerical", "multi_categorical", "timestamp", "embedding", "unknown", "image", "is_excluded")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    CATEGORICAL_FIELD_NUMBER: _ClassVar[int]
    PRIMARY_KEY_FIELD_NUMBER: _ClassVar[int]
    FOREIGN_KEY_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    NUMERICAL_FIELD_NUMBER: _ClassVar[int]
    MULTI_CATEGORICAL_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    EMBEDDING_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    IS_EXCLUDED_FIELD_NUMBER: _ClassVar[int]
    text: TextFeatureType
    categorical: CategoricalFeatureType
    primary_key: PrimaryKeyFeatureType
    foreign_key: ForeignKeyFeatureType
    identifier: IdentifierFeatureType
    numerical: NumericalFeatureType
    multi_categorical: MultiCategoricalFeatureType
    timestamp: TimestampFeatureType
    embedding: EmbeddingFeatureType
    unknown: UnknownFeatureType
    image: ImageFeatureType
    is_excluded: bool
    def __init__(self, text: _Optional[_Union[TextFeatureType, _Mapping]] = ..., categorical: _Optional[_Union[CategoricalFeatureType, _Mapping]] = ..., primary_key: _Optional[_Union[PrimaryKeyFeatureType, _Mapping]] = ..., foreign_key: _Optional[_Union[ForeignKeyFeatureType, _Mapping]] = ..., identifier: _Optional[_Union[IdentifierFeatureType, _Mapping]] = ..., numerical: _Optional[_Union[NumericalFeatureType, _Mapping]] = ..., multi_categorical: _Optional[_Union[MultiCategoricalFeatureType, _Mapping]] = ..., timestamp: _Optional[_Union[TimestampFeatureType, _Mapping]] = ..., embedding: _Optional[_Union[EmbeddingFeatureType, _Mapping]] = ..., unknown: _Optional[_Union[UnknownFeatureType, _Mapping]] = ..., image: _Optional[_Union[ImageFeatureType, _Mapping]] = ..., is_excluded: bool = ...) -> None: ...

class SelectFromStagingOp(_message.Message):
    __slots__ = ("blob_names", "expected_rows", "arrow_schema", "feature_types")
    BLOB_NAMES_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_ROWS_FIELD_NUMBER: _ClassVar[int]
    ARROW_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    FEATURE_TYPES_FIELD_NUMBER: _ClassVar[int]
    blob_names: _containers.RepeatedScalarFieldContainer[str]
    expected_rows: int
    arrow_schema: bytes
    feature_types: _containers.RepeatedCompositeFieldContainer[FeatureType]
    def __init__(self, blob_names: _Optional[_Iterable[str]] = ..., expected_rows: _Optional[int] = ..., arrow_schema: _Optional[bytes] = ..., feature_types: _Optional[_Iterable[_Union[FeatureType, _Mapping]]] = ...) -> None: ...

class SelectColumnsOp(_message.Message):
    __slots__ = ("source", "columns")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    source: TableComputeOp
    columns: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, source: _Optional[_Union[TableComputeOp, _Mapping]] = ..., columns: _Optional[_Iterable[str]] = ...) -> None: ...

class LimitRowsOp(_message.Message):
    __slots__ = ("source", "num_rows")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    NUM_ROWS_FIELD_NUMBER: _ClassVar[int]
    source: TableComputeOp
    num_rows: int
    def __init__(self, source: _Optional[_Union[TableComputeOp, _Mapping]] = ..., num_rows: _Optional[int] = ...) -> None: ...

class OrderByOp(_message.Message):
    __slots__ = ("source", "columns", "desc")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    DESC_FIELD_NUMBER: _ClassVar[int]
    source: TableComputeOp
    columns: _containers.RepeatedScalarFieldContainer[str]
    desc: bool
    def __init__(self, source: _Optional[_Union[TableComputeOp, _Mapping]] = ..., columns: _Optional[_Iterable[str]] = ..., desc: bool = ...) -> None: ...

class FilterRowsOp(_message.Message):
    __slots__ = ("source", "row_filter")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    ROW_FILTER_FIELD_NUMBER: _ClassVar[int]
    source: TableComputeOp
    row_filter: RowFilter
    def __init__(self, source: _Optional[_Union[TableComputeOp, _Mapping]] = ..., row_filter: _Optional[_Union[RowFilter, _Mapping]] = ...) -> None: ...

class DistinctRowsOp(_message.Message):
    __slots__ = ("source",)
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    source: TableComputeOp
    def __init__(self, source: _Optional[_Union[TableComputeOp, _Mapping]] = ...) -> None: ...

class UpdateMetadataOp(_message.Message):
    __slots__ = ("source", "metadata_updates")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    METADATA_UPDATES_FIELD_NUMBER: _ClassVar[int]
    source: TableComputeOp
    metadata_updates: _struct_pb2.Struct
    def __init__(self, source: _Optional[_Union[TableComputeOp, _Mapping]] = ..., metadata_updates: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class SetMetadataOp(_message.Message):
    __slots__ = ("source", "new_metadata")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    NEW_METADATA_FIELD_NUMBER: _ClassVar[int]
    source: TableComputeOp
    new_metadata: _struct_pb2.Struct
    def __init__(self, source: _Optional[_Union[TableComputeOp, _Mapping]] = ..., new_metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class RemoveFromMetadataOp(_message.Message):
    __slots__ = ("source", "keys_to_remove")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    KEYS_TO_REMOVE_FIELD_NUMBER: _ClassVar[int]
    source: TableComputeOp
    keys_to_remove: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, source: _Optional[_Union[TableComputeOp, _Mapping]] = ..., keys_to_remove: _Optional[_Iterable[str]] = ...) -> None: ...

class UpdateFeatureTypesOp(_message.Message):
    __slots__ = ("source", "new_feature_types")
    class NewFeatureTypesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: FeatureType
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[FeatureType, _Mapping]] = ...) -> None: ...
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    NEW_FEATURE_TYPES_FIELD_NUMBER: _ClassVar[int]
    source: TableComputeOp
    new_feature_types: _containers.MessageMap[str, FeatureType]
    def __init__(self, source: _Optional[_Union[TableComputeOp, _Mapping]] = ..., new_feature_types: _Optional[_Mapping[str, FeatureType]] = ...) -> None: ...

class RollupByAggregationOp(_message.Message):
    __slots__ = ("source", "group_by_column_names", "target_column_name", "aggregation_type")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    GROUP_BY_COLUMN_NAMES_FIELD_NUMBER: _ClassVar[int]
    TARGET_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    AGGREGATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    source: TableComputeOp
    group_by_column_names: _containers.RepeatedScalarFieldContainer[str]
    target_column_name: str
    aggregation_type: AggregationType
    def __init__(self, source: _Optional[_Union[TableComputeOp, _Mapping]] = ..., group_by_column_names: _Optional[_Iterable[str]] = ..., target_column_name: _Optional[str] = ..., aggregation_type: _Optional[_Union[AggregationType, str]] = ...) -> None: ...

class CombineFiltersRowFilter(_message.Message):
    __slots__ = ("row_filters", "logical_combination")
    ROW_FILTERS_FIELD_NUMBER: _ClassVar[int]
    LOGICAL_COMBINATION_FIELD_NUMBER: _ClassVar[int]
    row_filters: _containers.RepeatedCompositeFieldContainer[RowFilter]
    logical_combination: LogicalCombination
    def __init__(self, row_filters: _Optional[_Iterable[_Union[RowFilter, _Mapping]]] = ..., logical_combination: _Optional[_Union[LogicalCombination, str]] = ...) -> None: ...

class CompareColumnToLiteralRowFilter(_message.Message):
    __slots__ = ("column_name", "literal", "comparison_type", "column_arrow_schema")
    COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    LITERAL_FIELD_NUMBER: _ClassVar[int]
    COMPARISON_TYPE_FIELD_NUMBER: _ClassVar[int]
    COLUMN_ARROW_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    column_name: str
    literal: _struct_pb2.Value
    comparison_type: ComparisonType
    column_arrow_schema: bytes
    def __init__(self, column_name: _Optional[str] = ..., literal: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ..., comparison_type: _Optional[_Union[ComparisonType, str]] = ..., column_arrow_schema: _Optional[bytes] = ...) -> None: ...

class RowFilter(_message.Message):
    __slots__ = ("compare_column_to_literal", "combine_filters")
    COMPARE_COLUMN_TO_LITERAL_FIELD_NUMBER: _ClassVar[int]
    COMBINE_FILTERS_FIELD_NUMBER: _ClassVar[int]
    compare_column_to_literal: CompareColumnToLiteralRowFilter
    combine_filters: CombineFiltersRowFilter
    def __init__(self, compare_column_to_literal: _Optional[_Union[CompareColumnToLiteralRowFilter, _Mapping]] = ..., combine_filters: _Optional[_Union[CombineFiltersRowFilter, _Mapping]] = ...) -> None: ...

class EmptyOp(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class EdgeListTable(_message.Message):
    __slots__ = ("table", "start_column_name", "end_column_name", "start_entity_name", "end_entity_name")
    TABLE_FIELD_NUMBER: _ClassVar[int]
    START_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    END_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    START_ENTITY_NAME_FIELD_NUMBER: _ClassVar[int]
    END_ENTITY_NAME_FIELD_NUMBER: _ClassVar[int]
    table: TableComputeOp
    start_column_name: str
    end_column_name: str
    start_entity_name: str
    end_entity_name: str
    def __init__(self, table: _Optional[_Union[TableComputeOp, _Mapping]] = ..., start_column_name: _Optional[str] = ..., end_column_name: _Optional[str] = ..., start_entity_name: _Optional[str] = ..., end_entity_name: _Optional[str] = ...) -> None: ...

class EmbedNode2vecFromEdgeListsOp(_message.Message):
    __slots__ = ("edge_list_tables", "node2vec_parameters")
    EDGE_LIST_TABLES_FIELD_NUMBER: _ClassVar[int]
    NODE2VEC_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    edge_list_tables: _containers.RepeatedCompositeFieldContainer[EdgeListTable]
    node2vec_parameters: _graph_pb2.Node2VecParameters
    def __init__(self, edge_list_tables: _Optional[_Iterable[_Union[EdgeListTable, _Mapping]]] = ..., node2vec_parameters: _Optional[_Union[_graph_pb2.Node2VecParameters, _Mapping]] = ...) -> None: ...

class EmbeddingMetricsOp(_message.Message):
    __slots__ = ("table", "embedding_column_name")
    TABLE_FIELD_NUMBER: _ClassVar[int]
    EMBEDDING_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    table: TableComputeOp
    embedding_column_name: str
    def __init__(self, table: _Optional[_Union[TableComputeOp, _Mapping]] = ..., embedding_column_name: _Optional[str] = ...) -> None: ...

class EmbeddingCoordinatesOp(_message.Message):
    __slots__ = ("table", "n_components", "metric", "embedding_column_name")
    TABLE_FIELD_NUMBER: _ClassVar[int]
    N_COMPONENTS_FIELD_NUMBER: _ClassVar[int]
    METRIC_FIELD_NUMBER: _ClassVar[int]
    EMBEDDING_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    table: TableComputeOp
    n_components: int
    metric: str
    embedding_column_name: str
    def __init__(self, table: _Optional[_Union[TableComputeOp, _Mapping]] = ..., n_components: _Optional[int] = ..., metric: _Optional[str] = ..., embedding_column_name: _Optional[str] = ...) -> None: ...

class ReadFromParquetOp(_message.Message):
    __slots__ = ("blob_names", "expected_rows", "arrow_schema", "feature_types")
    BLOB_NAMES_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_ROWS_FIELD_NUMBER: _ClassVar[int]
    ARROW_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    FEATURE_TYPES_FIELD_NUMBER: _ClassVar[int]
    blob_names: _containers.RepeatedScalarFieldContainer[str]
    expected_rows: int
    arrow_schema: bytes
    feature_types: _containers.RepeatedCompositeFieldContainer[FeatureType]
    def __init__(self, blob_names: _Optional[_Iterable[str]] = ..., expected_rows: _Optional[int] = ..., arrow_schema: _Optional[bytes] = ..., feature_types: _Optional[_Iterable[_Union[FeatureType, _Mapping]]] = ...) -> None: ...

class SelectFromVectorStagingOp(_message.Message):
    __slots__ = ("input_vector", "blob_names", "similarity_metric", "vector_column_name", "arrow_schema", "feature_types", "expected_rows")
    INPUT_VECTOR_FIELD_NUMBER: _ClassVar[int]
    BLOB_NAMES_FIELD_NUMBER: _ClassVar[int]
    SIMILARITY_METRIC_FIELD_NUMBER: _ClassVar[int]
    VECTOR_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    ARROW_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    FEATURE_TYPES_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_ROWS_FIELD_NUMBER: _ClassVar[int]
    input_vector: _containers.RepeatedScalarFieldContainer[float]
    blob_names: _containers.RepeatedScalarFieldContainer[str]
    similarity_metric: str
    vector_column_name: str
    arrow_schema: bytes
    feature_types: _containers.RepeatedCompositeFieldContainer[FeatureType]
    expected_rows: int
    def __init__(self, input_vector: _Optional[_Iterable[float]] = ..., blob_names: _Optional[_Iterable[str]] = ..., similarity_metric: _Optional[str] = ..., vector_column_name: _Optional[str] = ..., arrow_schema: _Optional[bytes] = ..., feature_types: _Optional[_Iterable[_Union[FeatureType, _Mapping]]] = ..., expected_rows: _Optional[int] = ...) -> None: ...

class ConcatOp(_message.Message):
    __slots__ = ("tables", "how")
    TABLES_FIELD_NUMBER: _ClassVar[int]
    HOW_FIELD_NUMBER: _ClassVar[int]
    tables: _containers.RepeatedCompositeFieldContainer[TableComputeOp]
    how: str
    def __init__(self, tables: _Optional[_Iterable[_Union[TableComputeOp, _Mapping]]] = ..., how: _Optional[str] = ...) -> None: ...

class UnnestStructOp(_message.Message):
    __slots__ = ("source", "struct_column_name")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    STRUCT_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    source: TableComputeOp
    struct_column_name: str
    def __init__(self, source: _Optional[_Union[TableComputeOp, _Mapping]] = ..., struct_column_name: _Optional[str] = ...) -> None: ...

class UnnestListOp(_message.Message):
    __slots__ = ("source", "list_column_name", "column_names")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    LIST_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    COLUMN_NAMES_FIELD_NUMBER: _ClassVar[int]
    source: TableComputeOp
    list_column_name: str
    column_names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, source: _Optional[_Union[TableComputeOp, _Mapping]] = ..., list_column_name: _Optional[str] = ..., column_names: _Optional[_Iterable[str]] = ...) -> None: ...

class NestIntoStructOp(_message.Message):
    __slots__ = ("source", "struct_column_name", "column_names_to_nest")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    STRUCT_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    COLUMN_NAMES_TO_NEST_FIELD_NUMBER: _ClassVar[int]
    source: TableComputeOp
    struct_column_name: str
    column_names_to_nest: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, source: _Optional[_Union[TableComputeOp, _Mapping]] = ..., struct_column_name: _Optional[str] = ..., column_names_to_nest: _Optional[_Iterable[str]] = ...) -> None: ...

class AddLiteralColumnOp(_message.Message):
    __slots__ = ("source", "literal", "literals", "column_arrow_schema", "column_feature_type")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    LITERAL_FIELD_NUMBER: _ClassVar[int]
    LITERALS_FIELD_NUMBER: _ClassVar[int]
    COLUMN_ARROW_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    COLUMN_FEATURE_TYPE_FIELD_NUMBER: _ClassVar[int]
    source: TableComputeOp
    literal: _struct_pb2.Value
    literals: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Value]
    column_arrow_schema: bytes
    column_feature_type: FeatureType
    def __init__(self, source: _Optional[_Union[TableComputeOp, _Mapping]] = ..., literal: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ..., literals: _Optional[_Iterable[_Union[_struct_pb2.Value, _Mapping]]] = ..., column_arrow_schema: _Optional[bytes] = ..., column_feature_type: _Optional[_Union[FeatureType, _Mapping]] = ...) -> None: ...

class ConcatString(_message.Message):
    __slots__ = ("separator",)
    SEPARATOR_FIELD_NUMBER: _ClassVar[int]
    separator: str
    def __init__(self, separator: _Optional[str] = ...) -> None: ...

class ConcatList(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CombineColumnsOp(_message.Message):
    __slots__ = ("source", "column_names", "combined_column_name", "concat_string", "concat_list")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    COLUMN_NAMES_FIELD_NUMBER: _ClassVar[int]
    COMBINED_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    CONCAT_STRING_FIELD_NUMBER: _ClassVar[int]
    CONCAT_LIST_FIELD_NUMBER: _ClassVar[int]
    source: TableComputeOp
    column_names: _containers.RepeatedScalarFieldContainer[str]
    combined_column_name: str
    concat_string: ConcatString
    concat_list: ConcatList
    def __init__(self, source: _Optional[_Union[TableComputeOp, _Mapping]] = ..., column_names: _Optional[_Iterable[str]] = ..., combined_column_name: _Optional[str] = ..., concat_string: _Optional[_Union[ConcatString, _Mapping]] = ..., concat_list: _Optional[_Union[ConcatList, _Mapping]] = ...) -> None: ...

class OneHotEncoder(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MinMaxScaler(_message.Message):
    __slots__ = ("feature_range_min", "feature_range_max")
    FEATURE_RANGE_MIN_FIELD_NUMBER: _ClassVar[int]
    FEATURE_RANGE_MAX_FIELD_NUMBER: _ClassVar[int]
    feature_range_min: int
    feature_range_max: int
    def __init__(self, feature_range_min: _Optional[int] = ..., feature_range_max: _Optional[int] = ...) -> None: ...

class LabelBinarizer(_message.Message):
    __slots__ = ("neg_label", "pos_label")
    NEG_LABEL_FIELD_NUMBER: _ClassVar[int]
    POS_LABEL_FIELD_NUMBER: _ClassVar[int]
    neg_label: int
    pos_label: int
    def __init__(self, neg_label: _Optional[int] = ..., pos_label: _Optional[int] = ...) -> None: ...

class LabelEncoder(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class KBinsDiscretizer(_message.Message):
    __slots__ = ("n_bins", "encode_method", "strategy")
    N_BINS_FIELD_NUMBER: _ClassVar[int]
    ENCODE_METHOD_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_FIELD_NUMBER: _ClassVar[int]
    n_bins: int
    encode_method: str
    strategy: str
    def __init__(self, n_bins: _Optional[int] = ..., encode_method: _Optional[str] = ..., strategy: _Optional[str] = ...) -> None: ...

class Binarizer(_message.Message):
    __slots__ = ("threshold",)
    THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    threshold: float
    def __init__(self, threshold: _Optional[float] = ...) -> None: ...

class MaxAbsScaler(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class StandardScaler(_message.Message):
    __slots__ = ("with_mean", "with_std")
    WITH_MEAN_FIELD_NUMBER: _ClassVar[int]
    WITH_STD_FIELD_NUMBER: _ClassVar[int]
    with_mean: bool
    with_std: bool
    def __init__(self, with_mean: bool = ..., with_std: bool = ...) -> None: ...

class Encoder(_message.Message):
    __slots__ = ("one_hot_encoder", "min_max_scaler", "label_binarizer", "label_encoder", "k_bins_discretizer", "binarizer", "max_abs_scaler", "standard_scaler")
    ONE_HOT_ENCODER_FIELD_NUMBER: _ClassVar[int]
    MIN_MAX_SCALER_FIELD_NUMBER: _ClassVar[int]
    LABEL_BINARIZER_FIELD_NUMBER: _ClassVar[int]
    LABEL_ENCODER_FIELD_NUMBER: _ClassVar[int]
    K_BINS_DISCRETIZER_FIELD_NUMBER: _ClassVar[int]
    BINARIZER_FIELD_NUMBER: _ClassVar[int]
    MAX_ABS_SCALER_FIELD_NUMBER: _ClassVar[int]
    STANDARD_SCALER_FIELD_NUMBER: _ClassVar[int]
    one_hot_encoder: OneHotEncoder
    min_max_scaler: MinMaxScaler
    label_binarizer: LabelBinarizer
    label_encoder: LabelEncoder
    k_bins_discretizer: KBinsDiscretizer
    binarizer: Binarizer
    max_abs_scaler: MaxAbsScaler
    standard_scaler: StandardScaler
    def __init__(self, one_hot_encoder: _Optional[_Union[OneHotEncoder, _Mapping]] = ..., min_max_scaler: _Optional[_Union[MinMaxScaler, _Mapping]] = ..., label_binarizer: _Optional[_Union[LabelBinarizer, _Mapping]] = ..., label_encoder: _Optional[_Union[LabelEncoder, _Mapping]] = ..., k_bins_discretizer: _Optional[_Union[KBinsDiscretizer, _Mapping]] = ..., binarizer: _Optional[_Union[Binarizer, _Mapping]] = ..., max_abs_scaler: _Optional[_Union[MaxAbsScaler, _Mapping]] = ..., standard_scaler: _Optional[_Union[StandardScaler, _Mapping]] = ...) -> None: ...

class EncodeColumnOp(_message.Message):
    __slots__ = ("source", "column_name", "encoded_column_name", "encoder")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    ENCODED_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    ENCODER_FIELD_NUMBER: _ClassVar[int]
    source: TableComputeOp
    column_name: str
    encoded_column_name: str
    encoder: Encoder
    def __init__(self, source: _Optional[_Union[TableComputeOp, _Mapping]] = ..., column_name: _Optional[str] = ..., encoded_column_name: _Optional[str] = ..., encoder: _Optional[_Union[Encoder, _Mapping]] = ...) -> None: ...

class EmbedColumnOp(_message.Message):
    __slots__ = ("source", "column_name", "embedding_column_name", "model_name", "tokenizer_name", "expected_vector_length", "expected_coordinate_bitwidth")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    EMBEDDING_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    TOKENIZER_NAME_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_VECTOR_LENGTH_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_COORDINATE_BITWIDTH_FIELD_NUMBER: _ClassVar[int]
    source: TableComputeOp
    column_name: str
    embedding_column_name: str
    model_name: str
    tokenizer_name: str
    expected_vector_length: int
    expected_coordinate_bitwidth: FloatBitWidth
    def __init__(self, source: _Optional[_Union[TableComputeOp, _Mapping]] = ..., column_name: _Optional[str] = ..., embedding_column_name: _Optional[str] = ..., model_name: _Optional[str] = ..., tokenizer_name: _Optional[str] = ..., expected_vector_length: _Optional[int] = ..., expected_coordinate_bitwidth: _Optional[_Union[FloatBitWidth, str]] = ...) -> None: ...

class Min(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Max(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Mean(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Std(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Quantile(_message.Message):
    __slots__ = ("quantile",)
    QUANTILE_FIELD_NUMBER: _ClassVar[int]
    quantile: float
    def __init__(self, quantile: _Optional[float] = ...) -> None: ...

class Count(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class NullCount(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Aggregation(_message.Message):
    __slots__ = ("min", "max", "mean", "std", "quantile", "count", "null_count")
    MIN_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    MEAN_FIELD_NUMBER: _ClassVar[int]
    STD_FIELD_NUMBER: _ClassVar[int]
    QUANTILE_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    NULL_COUNT_FIELD_NUMBER: _ClassVar[int]
    min: Min
    max: Max
    mean: Mean
    std: Std
    quantile: Quantile
    count: Count
    null_count: NullCount
    def __init__(self, min: _Optional[_Union[Min, _Mapping]] = ..., max: _Optional[_Union[Max, _Mapping]] = ..., mean: _Optional[_Union[Mean, _Mapping]] = ..., std: _Optional[_Union[Std, _Mapping]] = ..., quantile: _Optional[_Union[Quantile, _Mapping]] = ..., count: _Optional[_Union[Count, _Mapping]] = ..., null_count: _Optional[_Union[NullCount, _Mapping]] = ...) -> None: ...

class AggregateColumnsOp(_message.Message):
    __slots__ = ("source", "column_names", "aggregation")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    COLUMN_NAMES_FIELD_NUMBER: _ClassVar[int]
    AGGREGATION_FIELD_NUMBER: _ClassVar[int]
    source: TableComputeOp
    column_names: _containers.RepeatedScalarFieldContainer[str]
    aggregation: Aggregation
    def __init__(self, source: _Optional[_Union[TableComputeOp, _Mapping]] = ..., column_names: _Optional[_Iterable[str]] = ..., aggregation: _Optional[_Union[Aggregation, _Mapping]] = ...) -> None: ...

class CorrelateColumnsOp(_message.Message):
    __slots__ = ("source", "column_names")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    COLUMN_NAMES_FIELD_NUMBER: _ClassVar[int]
    source: TableComputeOp
    column_names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, source: _Optional[_Union[TableComputeOp, _Mapping]] = ..., column_names: _Optional[_Iterable[str]] = ...) -> None: ...

class HistogramColumnOp(_message.Message):
    __slots__ = ("source", "column_name", "breakpoint_column_name", "count_column_name")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    BREAKPOINT_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    COUNT_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    source: TableComputeOp
    column_name: str
    breakpoint_column_name: str
    count_column_name: str
    def __init__(self, source: _Optional[_Union[TableComputeOp, _Mapping]] = ..., column_name: _Optional[str] = ..., breakpoint_column_name: _Optional[str] = ..., count_column_name: _Optional[str] = ...) -> None: ...

class AddRowIndexOp(_message.Message):
    __slots__ = ("source", "row_index_column_name", "offset")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    ROW_INDEX_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    source: TableComputeOp
    row_index_column_name: str
    offset: int
    def __init__(self, source: _Optional[_Union[TableComputeOp, _Mapping]] = ..., row_index_column_name: _Optional[str] = ..., offset: _Optional[int] = ...) -> None: ...

class ConvertColumnToStringOp(_message.Message):
    __slots__ = ("source", "column_name")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    source: TableComputeOp
    column_name: str
    def __init__(self, source: _Optional[_Union[TableComputeOp, _Mapping]] = ..., column_name: _Optional[str] = ...) -> None: ...

class OutputCsvOp(_message.Message):
    __slots__ = ("source", "csv_url", "include_header")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    CSV_URL_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_HEADER_FIELD_NUMBER: _ClassVar[int]
    source: TableComputeOp
    csv_url: str
    include_header: bool
    def __init__(self, source: _Optional[_Union[TableComputeOp, _Mapping]] = ..., csv_url: _Optional[str] = ..., include_header: bool = ...) -> None: ...

class TruncateListOp(_message.Message):
    __slots__ = ("source", "list_column_name", "target_column_length", "padding_value", "column_arrow_schema")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    LIST_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    TARGET_COLUMN_LENGTH_FIELD_NUMBER: _ClassVar[int]
    PADDING_VALUE_FIELD_NUMBER: _ClassVar[int]
    COLUMN_ARROW_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    source: TableComputeOp
    list_column_name: str
    target_column_length: int
    padding_value: _struct_pb2.Value
    column_arrow_schema: bytes
    def __init__(self, source: _Optional[_Union[TableComputeOp, _Mapping]] = ..., list_column_name: _Optional[str] = ..., target_column_length: _Optional[int] = ..., padding_value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ..., column_arrow_schema: _Optional[bytes] = ...) -> None: ...

class UnionOp(_message.Message):
    __slots__ = ("sources", "distinct")
    SOURCES_FIELD_NUMBER: _ClassVar[int]
    DISTINCT_FIELD_NUMBER: _ClassVar[int]
    sources: _containers.RepeatedCompositeFieldContainer[TableComputeOp]
    distinct: bool
    def __init__(self, sources: _Optional[_Iterable[_Union[TableComputeOp, _Mapping]]] = ..., distinct: bool = ...) -> None: ...

class EmbedImageColumnOp(_message.Message):
    __slots__ = ("source", "column_name", "embedding_column_name", "model_name", "expected_vector_length", "expected_coordinate_bitwidth")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    EMBEDDING_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_VECTOR_LENGTH_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_COORDINATE_BITWIDTH_FIELD_NUMBER: _ClassVar[int]
    source: TableComputeOp
    column_name: str
    embedding_column_name: str
    model_name: str
    expected_vector_length: int
    expected_coordinate_bitwidth: FloatBitWidth
    def __init__(self, source: _Optional[_Union[TableComputeOp, _Mapping]] = ..., column_name: _Optional[str] = ..., embedding_column_name: _Optional[str] = ..., model_name: _Optional[str] = ..., expected_vector_length: _Optional[int] = ..., expected_coordinate_bitwidth: _Optional[_Union[FloatBitWidth, str]] = ...) -> None: ...

class AddDecisionTreeSummaryOp(_message.Message):
    __slots__ = ("source", "feature_column_names", "label_column_name", "classes_names", "max_depth")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    FEATURE_COLUMN_NAMES_FIELD_NUMBER: _ClassVar[int]
    LABEL_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    CLASSES_NAMES_FIELD_NUMBER: _ClassVar[int]
    MAX_DEPTH_FIELD_NUMBER: _ClassVar[int]
    source: TableComputeOp
    feature_column_names: _containers.RepeatedScalarFieldContainer[str]
    label_column_name: str
    classes_names: _containers.RepeatedScalarFieldContainer[str]
    max_depth: int
    def __init__(self, source: _Optional[_Union[TableComputeOp, _Mapping]] = ..., feature_column_names: _Optional[_Iterable[str]] = ..., label_column_name: _Optional[str] = ..., classes_names: _Optional[_Iterable[str]] = ..., max_depth: _Optional[int] = ...) -> None: ...

class UniformRandom(_message.Message):
    __slots__ = ("seed",)
    SEED_FIELD_NUMBER: _ClassVar[int]
    seed: int
    def __init__(self, seed: _Optional[int] = ...) -> None: ...

class SampleStrategy(_message.Message):
    __slots__ = ("uniform_random",)
    UNIFORM_RANDOM_FIELD_NUMBER: _ClassVar[int]
    uniform_random: UniformRandom
    def __init__(self, uniform_random: _Optional[_Union[UniformRandom, _Mapping]] = ...) -> None: ...

class SampleRowsOp(_message.Message):
    __slots__ = ("source", "sample_strategy", "num_rows")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_STRATEGY_FIELD_NUMBER: _ClassVar[int]
    NUM_ROWS_FIELD_NUMBER: _ClassVar[int]
    source: TableComputeOp
    sample_strategy: SampleStrategy
    num_rows: int
    def __init__(self, source: _Optional[_Union[TableComputeOp, _Mapping]] = ..., sample_strategy: _Optional[_Union[SampleStrategy, _Mapping]] = ..., num_rows: _Optional[int] = ...) -> None: ...

class TableSliceArgs(_message.Message):
    __slots__ = ("offset", "length")
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    offset: int
    length: int
    def __init__(self, offset: _Optional[int] = ..., length: _Optional[int] = ...) -> None: ...

class TableComputeContext(_message.Message):
    __slots__ = ("table", "output_url_prefix", "sql_output_slice_args")
    TABLE_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_URL_PREFIX_FIELD_NUMBER: _ClassVar[int]
    SQL_OUTPUT_SLICE_ARGS_FIELD_NUMBER: _ClassVar[int]
    table: TableComputeOp
    output_url_prefix: str
    sql_output_slice_args: TableSliceArgs
    def __init__(self, table: _Optional[_Union[TableComputeOp, _Mapping]] = ..., output_url_prefix: _Optional[str] = ..., sql_output_slice_args: _Optional[_Union[TableSliceArgs, _Mapping]] = ...) -> None: ...

class TableComputeResult(_message.Message):
    __slots__ = ("result_urls", "metrics")
    RESULT_URLS_FIELD_NUMBER: _ClassVar[int]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    result_urls: _containers.RepeatedScalarFieldContainer[str]
    metrics: _struct_pb2.Struct
    def __init__(self, result_urls: _Optional[_Iterable[str]] = ..., metrics: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class ExecuteRequest(_message.Message):
    __slots__ = ("tables_to_compute",)
    TABLES_TO_COMPUTE_FIELD_NUMBER: _ClassVar[int]
    tables_to_compute: _containers.RepeatedCompositeFieldContainer[TableComputeContext]
    def __init__(self, tables_to_compute: _Optional[_Iterable[_Union[TableComputeContext, _Mapping]]] = ...) -> None: ...

class ExecuteResponse(_message.Message):
    __slots__ = ("table_results",)
    TABLE_RESULTS_FIELD_NUMBER: _ClassVar[int]
    table_results: _containers.RepeatedCompositeFieldContainer[TableComputeResult]
    def __init__(self, table_results: _Optional[_Iterable[_Union[TableComputeResult, _Mapping]]] = ...) -> None: ...

class StreamExecuteRequest(_message.Message):
    __slots__ = ("table_to_compute",)
    TABLE_TO_COMPUTE_FIELD_NUMBER: _ClassVar[int]
    table_to_compute: TableComputeContext
    def __init__(self, table_to_compute: _Optional[_Union[TableComputeContext, _Mapping]] = ...) -> None: ...

class StreamExecuteResponse(_message.Message):
    __slots__ = ("table_results",)
    TABLE_RESULTS_FIELD_NUMBER: _ClassVar[int]
    table_results: _containers.RepeatedCompositeFieldContainer[TableComputeResult]
    def __init__(self, table_results: _Optional[_Iterable[_Union[TableComputeResult, _Mapping]]] = ...) -> None: ...

class NamedTables(_message.Message):
    __slots__ = ("tables",)
    class TablesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: TableComputeOp
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[TableComputeOp, _Mapping]] = ...) -> None: ...
    TABLES_FIELD_NUMBER: _ClassVar[int]
    tables: _containers.MessageMap[str, TableComputeOp]
    def __init__(self, tables: _Optional[_Mapping[str, TableComputeOp]] = ...) -> None: ...
