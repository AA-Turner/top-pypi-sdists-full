from chalk._gen.chalk.arrow.v1 import arrow_pb2 as _arrow_pb2
from chalk._gen.chalk.common.v1 import chalk_error_pb2 as _chalk_error_pb2
from chalk._gen.chalk.expression.v1 import expression_pb2 as _expression_pb2
from chalk._gen.chalk.graph.v1 import graph_pb2 as _graph_pb2
from google.protobuf import duration_pb2 as _duration_pb2
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

class FeatureKeySource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FEATURE_KEY_SOURCE_UNSPECIFIED: _ClassVar[FeatureKeySource]
    FEATURE_KEY_SOURCE_INFERRED: _ClassVar[FeatureKeySource]
    FEATURE_KEY_SOURCE_EXPLICIT: _ClassVar[FeatureKeySource]

FEATURE_KEY_SOURCE_UNSPECIFIED: FeatureKeySource
FEATURE_KEY_SOURCE_INFERRED: FeatureKeySource
FEATURE_KEY_SOURCE_EXPLICIT: FeatureKeySource

class FeatureType(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class AuxiliaryInfo(_message.Message):
    __slots__ = ("feature_ref_info", "underscore_info")
    FEATURE_REF_INFO_FIELD_NUMBER: _ClassVar[int]
    UNDERSCORE_INFO_FIELD_NUMBER: _ClassVar[int]
    feature_ref_info: FeatureReferenceInfoV2
    underscore_info: UnderscoreInfo
    def __init__(
        self,
        feature_ref_info: _Optional[_Union[FeatureReferenceInfoV2, _Mapping]] = ...,
        underscore_info: _Optional[_Union[UnderscoreInfo, _Mapping]] = ...,
    ) -> None: ...

class FeatureReferenceInfoV2(_message.Message):
    __slots__ = ("feature_refs", "data_frame_types", "filter_expressions")
    FEATURE_REFS_FIELD_NUMBER: _ClassVar[int]
    DATA_FRAME_TYPES_FIELD_NUMBER: _ClassVar[int]
    FILTER_EXPRESSIONS_FIELD_NUMBER: _ClassVar[int]
    feature_refs: _containers.RepeatedCompositeFieldContainer[FeatureReferenceV2]
    data_frame_types: _containers.RepeatedCompositeFieldContainer[DataFrameTypeV2]
    filter_expressions: _containers.RepeatedCompositeFieldContainer[FilterExpressionParsedV2]
    def __init__(
        self,
        feature_refs: _Optional[_Iterable[_Union[FeatureReferenceV2, _Mapping]]] = ...,
        data_frame_types: _Optional[_Iterable[_Union[DataFrameTypeV2, _Mapping]]] = ...,
        filter_expressions: _Optional[_Iterable[_Union[FilterExpressionParsedV2, _Mapping]]] = ...,
    ) -> None: ...

class UnderscoreInfo(_message.Message):
    __slots__ = ("constants", "parsed", "operations", "chalkpy_underscore")
    CONSTANTS_FIELD_NUMBER: _ClassVar[int]
    PARSED_FIELD_NUMBER: _ClassVar[int]
    OPERATIONS_FIELD_NUMBER: _ClassVar[int]
    CHALKPY_UNDERSCORE_FIELD_NUMBER: _ClassVar[int]
    constants: _containers.RepeatedCompositeFieldContainer[UnderscoreConstant]
    parsed: _containers.RepeatedCompositeFieldContainer[UnderscoreParsed]
    operations: _containers.RepeatedCompositeFieldContainer[UnderscoreOperation]
    chalkpy_underscore: _containers.RepeatedCompositeFieldContainer[ChalkpyUnderscore]
    def __init__(
        self,
        constants: _Optional[_Iterable[_Union[UnderscoreConstant, _Mapping]]] = ...,
        parsed: _Optional[_Iterable[_Union[UnderscoreParsed, _Mapping]]] = ...,
        operations: _Optional[_Iterable[_Union[UnderscoreOperation, _Mapping]]] = ...,
        chalkpy_underscore: _Optional[_Iterable[_Union[ChalkpyUnderscore, _Mapping]]] = ...,
    ) -> None: ...

class FeatureReferenceV2(_message.Message):
    __slots__ = ("this_id", "feature_ref", "path_ids", "df_id")
    THIS_ID_FIELD_NUMBER: _ClassVar[int]
    FEATURE_REF_FIELD_NUMBER: _ClassVar[int]
    PATH_IDS_FIELD_NUMBER: _ClassVar[int]
    DF_ID_FIELD_NUMBER: _ClassVar[int]
    this_id: FeatureReferenceIdV2
    feature_ref: _graph_pb2.FeatureReference
    path_ids: _containers.RepeatedCompositeFieldContainer[FeatureReferenceIdV2]
    df_id: DataFrameTypeIdV2
    def __init__(
        self,
        this_id: _Optional[_Union[FeatureReferenceIdV2, _Mapping]] = ...,
        feature_ref: _Optional[_Union[_graph_pb2.FeatureReference, _Mapping]] = ...,
        path_ids: _Optional[_Iterable[_Union[FeatureReferenceIdV2, _Mapping]]] = ...,
        df_id: _Optional[_Union[DataFrameTypeIdV2, _Mapping]] = ...,
    ) -> None: ...

class FeatureReferenceIdV2(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class DataFrameTypeV2(_message.Message):
    __slots__ = ("this_id", "df", "filter_expression_id", "optional_column_refs", "required_column_refs")
    THIS_ID_FIELD_NUMBER: _ClassVar[int]
    DF_FIELD_NUMBER: _ClassVar[int]
    FILTER_EXPRESSION_ID_FIELD_NUMBER: _ClassVar[int]
    OPTIONAL_COLUMN_REFS_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_COLUMN_REFS_FIELD_NUMBER: _ClassVar[int]
    this_id: DataFrameTypeIdV2
    df: _graph_pb2.DataFrameType
    filter_expression_id: FilterExpressionParsedIdV2
    optional_column_refs: _containers.RepeatedCompositeFieldContainer[FeatureReferenceIdV2]
    required_column_refs: _containers.RepeatedCompositeFieldContainer[FeatureReferenceIdV2]
    def __init__(
        self,
        this_id: _Optional[_Union[DataFrameTypeIdV2, _Mapping]] = ...,
        df: _Optional[_Union[_graph_pb2.DataFrameType, _Mapping]] = ...,
        filter_expression_id: _Optional[_Union[FilterExpressionParsedIdV2, _Mapping]] = ...,
        optional_column_refs: _Optional[_Iterable[_Union[FeatureReferenceIdV2, _Mapping]]] = ...,
        required_column_refs: _Optional[_Iterable[_Union[FeatureReferenceIdV2, _Mapping]]] = ...,
    ) -> None: ...

class DataFrameTypeIdV2(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class FilterExpressionParsedV2(_message.Message):
    __slots__ = ("this_id", "expr")
    THIS_ID_FIELD_NUMBER: _ClassVar[int]
    EXPR_FIELD_NUMBER: _ClassVar[int]
    this_id: FilterExpressionParsedIdV2
    expr: UnderscoreParsedId
    def __init__(
        self,
        this_id: _Optional[_Union[FilterExpressionParsedIdV2, _Mapping]] = ...,
        expr: _Optional[_Union[UnderscoreParsedId, _Mapping]] = ...,
    ) -> None: ...

class FilterExpressionParsedIdV2(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class UnderscoreConstant(_message.Message):
    __slots__ = ("this_id", "value", "default_pa_type")
    THIS_ID_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_PA_TYPE_FIELD_NUMBER: _ClassVar[int]
    this_id: UnderscoreConstantId
    value: _expression_pb2.LogicalExprNode
    default_pa_type: _arrow_pb2.ArrowType
    def __init__(
        self,
        this_id: _Optional[_Union[UnderscoreConstantId, _Mapping]] = ...,
        value: _Optional[_Union[_expression_pb2.LogicalExprNode, _Mapping]] = ...,
        default_pa_type: _Optional[_Union[_arrow_pb2.ArrowType, _Mapping]] = ...,
    ) -> None: ...

class UnderscoreConstantId(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class UnderscoreParsed(_message.Message):
    __slots__ = (
        "this_id",
        "original_underscore",
        "original_underscore_id",
        "namespace",
        "table",
        "windowed",
        "materialized_state",
        "value",
    )
    THIS_ID_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_UNDERSCORE_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_UNDERSCORE_ID_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    TABLE_FIELD_NUMBER: _ClassVar[int]
    WINDOWED_FIELD_NUMBER: _ClassVar[int]
    MATERIALIZED_STATE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    this_id: UnderscoreParsedId
    original_underscore: _expression_pb2.LogicalExprNode
    original_underscore_id: ChalkpyUnderscoreId
    namespace: UnderscoreNamespace
    table: UnderscoreTable
    windowed: UnderscoreWindowed
    materialized_state: UnderscoreMaterializedState
    value: UnderscoreValueV2
    def __init__(
        self,
        this_id: _Optional[_Union[UnderscoreParsedId, _Mapping]] = ...,
        original_underscore: _Optional[_Union[_expression_pb2.LogicalExprNode, _Mapping]] = ...,
        original_underscore_id: _Optional[_Union[ChalkpyUnderscoreId, _Mapping]] = ...,
        namespace: _Optional[_Union[UnderscoreNamespace, _Mapping]] = ...,
        table: _Optional[_Union[UnderscoreTable, _Mapping]] = ...,
        windowed: _Optional[_Union[UnderscoreWindowed, _Mapping]] = ...,
        materialized_state: _Optional[_Union[UnderscoreMaterializedState, _Mapping]] = ...,
        value: _Optional[_Union[UnderscoreValueV2, _Mapping]] = ...,
    ) -> None: ...

class UnderscoreParsedId(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class UnderscoreNamespace(_message.Message):
    __slots__ = ("path", "root_namespace")
    PATH_FIELD_NUMBER: _ClassVar[int]
    ROOT_NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    path: _containers.RepeatedCompositeFieldContainer[FeatureReferenceIdV2]
    root_namespace: str
    def __init__(
        self,
        path: _Optional[_Iterable[_Union[FeatureReferenceIdV2, _Mapping]]] = ...,
        root_namespace: _Optional[str] = ...,
    ) -> None: ...

class UnderscoreTable(_message.Message):
    __slots__ = ("schema",)
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    schema: _arrow_pb2.Schema
    def __init__(self, schema: _Optional[_Union[_arrow_pb2.Schema, _Mapping]] = ...) -> None: ...

class UnderscoreWindowed(_message.Message):
    __slots__ = ("path", "underlying", "root_namespace")
    PATH_FIELD_NUMBER: _ClassVar[int]
    UNDERLYING_FIELD_NUMBER: _ClassVar[int]
    ROOT_NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    path: _containers.RepeatedCompositeFieldContainer[FeatureReferenceIdV2]
    underlying: FeatureReferenceIdV2
    root_namespace: str
    def __init__(
        self,
        path: _Optional[_Iterable[_Union[FeatureReferenceIdV2, _Mapping]]] = ...,
        underlying: _Optional[_Union[FeatureReferenceIdV2, _Mapping]] = ...,
        root_namespace: _Optional[str] = ...,
    ) -> None: ...

class UnderscoreMaterializedState(_message.Message):
    __slots__ = ("mat_agg_definition", "window_feature", "scalar_feature")
    MAT_AGG_DEFINITION_FIELD_NUMBER: _ClassVar[int]
    WINDOW_FEATURE_FIELD_NUMBER: _ClassVar[int]
    SCALAR_FEATURE_FIELD_NUMBER: _ClassVar[int]
    mat_agg_definition: UnderscoreParsedId
    window_feature: UnderscoreParsedId
    scalar_feature: FeatureReferenceIdV2
    def __init__(
        self,
        mat_agg_definition: _Optional[_Union[UnderscoreParsedId, _Mapping]] = ...,
        window_feature: _Optional[_Union[UnderscoreParsedId, _Mapping]] = ...,
        scalar_feature: _Optional[_Union[FeatureReferenceIdV2, _Mapping]] = ...,
    ) -> None: ...

class UnderscoreValueV2(_message.Message):
    __slots__ = (
        "expression_id",
        "feature",
        "column",
        "us_lambda",
        "lambda_parameter",
        "item_parsed",
        "operation_expression",
        "never",
        "materialized_aggregation",
        "materialized_state_operation",
        "incomplete_group_by_aggregation",
        "outer_feature",
        "grouped_dataframe",
        "aggregated_dataframe",
        "dataframe_column",
        "dataframe_item_parsed",
    )
    EXPRESSION_ID_FIELD_NUMBER: _ClassVar[int]
    FEATURE_FIELD_NUMBER: _ClassVar[int]
    COLUMN_FIELD_NUMBER: _ClassVar[int]
    US_LAMBDA_FIELD_NUMBER: _ClassVar[int]
    LAMBDA_PARAMETER_FIELD_NUMBER: _ClassVar[int]
    ITEM_PARSED_FIELD_NUMBER: _ClassVar[int]
    OPERATION_EXPRESSION_FIELD_NUMBER: _ClassVar[int]
    NEVER_FIELD_NUMBER: _ClassVar[int]
    MATERIALIZED_AGGREGATION_FIELD_NUMBER: _ClassVar[int]
    MATERIALIZED_STATE_OPERATION_FIELD_NUMBER: _ClassVar[int]
    INCOMPLETE_GROUP_BY_AGGREGATION_FIELD_NUMBER: _ClassVar[int]
    OUTER_FEATURE_FIELD_NUMBER: _ClassVar[int]
    GROUPED_DATAFRAME_FIELD_NUMBER: _ClassVar[int]
    AGGREGATED_DATAFRAME_FIELD_NUMBER: _ClassVar[int]
    DATAFRAME_COLUMN_FIELD_NUMBER: _ClassVar[int]
    DATAFRAME_ITEM_PARSED_FIELD_NUMBER: _ClassVar[int]
    expression_id: str
    feature: UnderscoreFeature
    column: UnderscoreColumn
    us_lambda: UnderscoreLambda
    lambda_parameter: UnderscoreLambdaParameter
    item_parsed: UnderscoreItemParsed
    operation_expression: UnderscoreOperationExpression
    never: UnderscoreNever
    materialized_aggregation: UnderscoreMaterializedAggregation
    materialized_state_operation: UnderscoreMaterializedStateOperation
    incomplete_group_by_aggregation: UnderscoreIncompleteGroupByAggregation
    outer_feature: UnderscoreOuterFeature
    grouped_dataframe: UnderscoreGroupedDataFrame
    aggregated_dataframe: UnderscoreAggregatedDataFrame
    dataframe_column: UnderscoreDataFrameColumn
    dataframe_item_parsed: UnderscoreDataFrameItemParsed
    def __init__(
        self,
        expression_id: _Optional[str] = ...,
        feature: _Optional[_Union[UnderscoreFeature, _Mapping]] = ...,
        column: _Optional[_Union[UnderscoreColumn, _Mapping]] = ...,
        us_lambda: _Optional[_Union[UnderscoreLambda, _Mapping]] = ...,
        lambda_parameter: _Optional[_Union[UnderscoreLambdaParameter, _Mapping]] = ...,
        item_parsed: _Optional[_Union[UnderscoreItemParsed, _Mapping]] = ...,
        operation_expression: _Optional[_Union[UnderscoreOperationExpression, _Mapping]] = ...,
        never: _Optional[_Union[UnderscoreNever, _Mapping]] = ...,
        materialized_aggregation: _Optional[_Union[UnderscoreMaterializedAggregation, _Mapping]] = ...,
        materialized_state_operation: _Optional[_Union[UnderscoreMaterializedStateOperation, _Mapping]] = ...,
        incomplete_group_by_aggregation: _Optional[_Union[UnderscoreIncompleteGroupByAggregation, _Mapping]] = ...,
        outer_feature: _Optional[_Union[UnderscoreOuterFeature, _Mapping]] = ...,
        grouped_dataframe: _Optional[_Union[UnderscoreGroupedDataFrame, _Mapping]] = ...,
        aggregated_dataframe: _Optional[_Union[UnderscoreAggregatedDataFrame, _Mapping]] = ...,
        dataframe_column: _Optional[_Union[UnderscoreDataFrameColumn, _Mapping]] = ...,
        dataframe_item_parsed: _Optional[_Union[UnderscoreDataFrameItemParsed, _Mapping]] = ...,
    ) -> None: ...

class UnderscoreFeature(_message.Message):
    __slots__ = ("underlying", "path")
    UNDERLYING_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    underlying: FeatureReferenceIdV2
    path: _containers.RepeatedCompositeFieldContainer[FeatureReferenceIdV2]
    def __init__(
        self,
        underlying: _Optional[_Union[FeatureReferenceIdV2, _Mapping]] = ...,
        path: _Optional[_Iterable[_Union[FeatureReferenceIdV2, _Mapping]]] = ...,
    ) -> None: ...

class UnderscoreColumn(_message.Message):
    __slots__ = ("column_name", "field")
    COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    FIELD_FIELD_NUMBER: _ClassVar[int]
    column_name: str
    field: _arrow_pb2.Field
    def __init__(
        self, column_name: _Optional[str] = ..., field: _Optional[_Union[_arrow_pb2.Field, _Mapping]] = ...
    ) -> None: ...

class UnderscoreLambda(_message.Message):
    __slots__ = ("parameters", "lambda_body")
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    LAMBDA_BODY_FIELD_NUMBER: _ClassVar[int]
    parameters: _containers.RepeatedCompositeFieldContainer[UnderscoreLambdaParameter]
    lambda_body: UnderscoreParsedId
    def __init__(
        self,
        parameters: _Optional[_Iterable[_Union[UnderscoreLambdaParameter, _Mapping]]] = ...,
        lambda_body: _Optional[_Union[UnderscoreParsedId, _Mapping]] = ...,
    ) -> None: ...

class UnderscoreLambdaParameter(_message.Message):
    __slots__ = ("parameter_name", "parameter_type")
    PARAMETER_NAME_FIELD_NUMBER: _ClassVar[int]
    PARAMETER_TYPE_FIELD_NUMBER: _ClassVar[int]
    parameter_name: str
    parameter_type: _arrow_pb2.ArrowType
    def __init__(
        self,
        parameter_name: _Optional[str] = ...,
        parameter_type: _Optional[_Union[_arrow_pb2.ArrowType, _Mapping]] = ...,
    ) -> None: ...

class UnderscoreItemParsed(_message.Message):
    __slots__ = ("parent", "feature_key", "feature_keys", "feature_key_source", "filters")
    PARENT_FIELD_NUMBER: _ClassVar[int]
    FEATURE_KEY_FIELD_NUMBER: _ClassVar[int]
    FEATURE_KEYS_FIELD_NUMBER: _ClassVar[int]
    FEATURE_KEY_SOURCE_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    parent: UnderscoreParsedId
    feature_key: UnderscoreParsedId
    feature_keys: _containers.RepeatedCompositeFieldContainer[UnderscoreParsedId]
    feature_key_source: FeatureKeySource
    filters: _containers.RepeatedCompositeFieldContainer[UnderscoreParsedId]
    def __init__(
        self,
        parent: _Optional[_Union[UnderscoreParsedId, _Mapping]] = ...,
        feature_key: _Optional[_Union[UnderscoreParsedId, _Mapping]] = ...,
        feature_keys: _Optional[_Iterable[_Union[UnderscoreParsedId, _Mapping]]] = ...,
        feature_key_source: _Optional[_Union[FeatureKeySource, str]] = ...,
        filters: _Optional[_Iterable[_Union[UnderscoreParsedId, _Mapping]]] = ...,
    ) -> None: ...

class UnderscoreOperationExpression(_message.Message):
    __slots__ = ("positional_operands", "named_operands", "operation", "args", "kwarg_keys", "kwarg_values")
    class NamedOperandsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: UnderscoreOperand
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[UnderscoreOperand, _Mapping]] = ...
        ) -> None: ...

    POSITIONAL_OPERANDS_FIELD_NUMBER: _ClassVar[int]
    NAMED_OPERANDS_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    KWARG_KEYS_FIELD_NUMBER: _ClassVar[int]
    KWARG_VALUES_FIELD_NUMBER: _ClassVar[int]
    positional_operands: _containers.RepeatedCompositeFieldContainer[UnderscoreOperand]
    named_operands: _containers.MessageMap[str, UnderscoreOperand]
    operation: UnderscoreOperationId
    args: _containers.RepeatedCompositeFieldContainer[_expression_pb2.LogicalExprNode]
    kwarg_keys: _containers.RepeatedScalarFieldContainer[str]
    kwarg_values: _containers.RepeatedCompositeFieldContainer[_expression_pb2.LogicalExprNode]
    def __init__(
        self,
        positional_operands: _Optional[_Iterable[_Union[UnderscoreOperand, _Mapping]]] = ...,
        named_operands: _Optional[_Mapping[str, UnderscoreOperand]] = ...,
        operation: _Optional[_Union[UnderscoreOperationId, _Mapping]] = ...,
        args: _Optional[_Iterable[_Union[_expression_pb2.LogicalExprNode, _Mapping]]] = ...,
        kwarg_keys: _Optional[_Iterable[str]] = ...,
        kwarg_values: _Optional[_Iterable[_Union[_expression_pb2.LogicalExprNode, _Mapping]]] = ...,
    ) -> None: ...

class UnderscoreOperands(_message.Message):
    __slots__ = ("positional", "named")
    class NamedEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: UnderscoreOperand
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[UnderscoreOperand, _Mapping]] = ...
        ) -> None: ...

    POSITIONAL_FIELD_NUMBER: _ClassVar[int]
    NAMED_FIELD_NUMBER: _ClassVar[int]
    positional: _containers.RepeatedCompositeFieldContainer[UnderscoreOperand]
    named: _containers.MessageMap[str, UnderscoreOperand]
    def __init__(
        self,
        positional: _Optional[_Iterable[_Union[UnderscoreOperand, _Mapping]]] = ...,
        named: _Optional[_Mapping[str, UnderscoreOperand]] = ...,
    ) -> None: ...

class UnderscoreOperand(_message.Message):
    __slots__ = ("value", "constant")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    CONSTANT_FIELD_NUMBER: _ClassVar[int]
    value: UnderscoreParsedId
    constant: UnderscoreConstantId
    def __init__(
        self,
        value: _Optional[_Union[UnderscoreParsedId, _Mapping]] = ...,
        constant: _Optional[_Union[UnderscoreConstantId, _Mapping]] = ...,
    ) -> None: ...

class UnderscoreNever(_message.Message):
    __slots__ = ("error", "root_namespace")
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ROOT_NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    error: _chalk_error_pb2.ChalkError
    root_namespace: str
    def __init__(
        self,
        error: _Optional[_Union[_chalk_error_pb2.ChalkError, _Mapping]] = ...,
        root_namespace: _Optional[str] = ...,
    ) -> None: ...

class UnderscoreMaterializedAggregation(_message.Message):
    __slots__ = (
        "unmaterialized_underscore",
        "materialization",
        "window_duration",
        "source_aggregation_namespace",
        "group_by_keys",
        "has_many",
    )
    UNMATERIALIZED_UNDERSCORE_FIELD_NUMBER: _ClassVar[int]
    MATERIALIZATION_FIELD_NUMBER: _ClassVar[int]
    WINDOW_DURATION_FIELD_NUMBER: _ClassVar[int]
    SOURCE_AGGREGATION_NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    GROUP_BY_KEYS_FIELD_NUMBER: _ClassVar[int]
    HAS_MANY_FIELD_NUMBER: _ClassVar[int]
    unmaterialized_underscore: UnderscoreParsedId
    materialization: MaterializationWindowConfigParsed
    window_duration: _duration_pb2.Duration
    source_aggregation_namespace: str
    group_by_keys: _containers.RepeatedCompositeFieldContainer[FeatureReferenceIdV2]
    has_many: FeatureReferenceIdV2
    def __init__(
        self,
        unmaterialized_underscore: _Optional[_Union[UnderscoreParsedId, _Mapping]] = ...,
        materialization: _Optional[_Union[MaterializationWindowConfigParsed, _Mapping]] = ...,
        window_duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        source_aggregation_namespace: _Optional[str] = ...,
        group_by_keys: _Optional[_Iterable[_Union[FeatureReferenceIdV2, _Mapping]]] = ...,
        has_many: _Optional[_Union[FeatureReferenceIdV2, _Mapping]] = ...,
    ) -> None: ...

class MaterializationWindowConfigParsed(_message.Message):
    __slots__ = (
        "base",
        "group_by",
        "aggregate_on",
        "aggregation_kwarg_keys",
        "aggregation_kwarg_values",
        "bucket_feature",
        "approximate_offline_query",
        "aggregate_on_features",
    )
    BASE_FIELD_NUMBER: _ClassVar[int]
    GROUP_BY_FIELD_NUMBER: _ClassVar[int]
    AGGREGATE_ON_FIELD_NUMBER: _ClassVar[int]
    AGGREGATION_KWARG_KEYS_FIELD_NUMBER: _ClassVar[int]
    AGGREGATION_KWARG_VALUES_FIELD_NUMBER: _ClassVar[int]
    BUCKET_FEATURE_FIELD_NUMBER: _ClassVar[int]
    APPROXIMATE_OFFLINE_QUERY_FIELD_NUMBER: _ClassVar[int]
    AGGREGATE_ON_FEATURES_FIELD_NUMBER: _ClassVar[int]
    base: _graph_pb2.WindowAggregation
    group_by: _containers.RepeatedCompositeFieldContainer[FeatureReferenceIdV2]
    aggregate_on: FeatureReferenceIdV2
    aggregation_kwarg_keys: _containers.RepeatedScalarFieldContainer[str]
    aggregation_kwarg_values: _containers.RepeatedCompositeFieldContainer[_expression_pb2.LogicalExprNode]
    bucket_feature: FeatureReferenceIdV2
    approximate_offline_query: bool
    aggregate_on_features: _containers.RepeatedCompositeFieldContainer[FeatureReferenceIdV2]
    def __init__(
        self,
        base: _Optional[_Union[_graph_pb2.WindowAggregation, _Mapping]] = ...,
        group_by: _Optional[_Iterable[_Union[FeatureReferenceIdV2, _Mapping]]] = ...,
        aggregate_on: _Optional[_Union[FeatureReferenceIdV2, _Mapping]] = ...,
        aggregation_kwarg_keys: _Optional[_Iterable[str]] = ...,
        aggregation_kwarg_values: _Optional[_Iterable[_Union[_expression_pb2.LogicalExprNode, _Mapping]]] = ...,
        bucket_feature: _Optional[_Union[FeatureReferenceIdV2, _Mapping]] = ...,
        approximate_offline_query: bool = ...,
        aggregate_on_features: _Optional[_Iterable[_Union[FeatureReferenceIdV2, _Mapping]]] = ...,
    ) -> None: ...

class UnderscoreMaterializedStateOperation(_message.Message):
    __slots__ = ("mat_agg_definition", "for_offline_resolver")
    MAT_AGG_DEFINITION_FIELD_NUMBER: _ClassVar[int]
    FOR_OFFLINE_RESOLVER_FIELD_NUMBER: _ClassVar[int]
    mat_agg_definition: UnderscoreParsedId
    for_offline_resolver: bool
    def __init__(
        self,
        mat_agg_definition: _Optional[_Union[UnderscoreParsedId, _Mapping]] = ...,
        for_offline_resolver: bool = ...,
    ) -> None: ...

class UnderscoreIncompleteGroupByAggregation(_message.Message):
    __slots__ = (
        "has_many",
        "materialization",
        "group_features",
        "window_duration",
        "allowed_window_values",
        "source_aggregation_namespace",
    )
    class GroupFeaturesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: FeatureReferenceIdV2
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[FeatureReferenceIdV2, _Mapping]] = ...
        ) -> None: ...

    HAS_MANY_FIELD_NUMBER: _ClassVar[int]
    MATERIALIZATION_FIELD_NUMBER: _ClassVar[int]
    GROUP_FEATURES_FIELD_NUMBER: _ClassVar[int]
    WINDOW_DURATION_FIELD_NUMBER: _ClassVar[int]
    ALLOWED_WINDOW_VALUES_FIELD_NUMBER: _ClassVar[int]
    SOURCE_AGGREGATION_NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    has_many: FeatureReferenceIdV2
    materialization: MaterializationWindowConfigParsed
    group_features: _containers.MessageMap[str, FeatureReferenceIdV2]
    window_duration: _duration_pb2.Duration
    allowed_window_values: _containers.RepeatedCompositeFieldContainer[_duration_pb2.Duration]
    source_aggregation_namespace: str
    def __init__(
        self,
        has_many: _Optional[_Union[FeatureReferenceIdV2, _Mapping]] = ...,
        materialization: _Optional[_Union[MaterializationWindowConfigParsed, _Mapping]] = ...,
        group_features: _Optional[_Mapping[str, FeatureReferenceIdV2]] = ...,
        window_duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        allowed_window_values: _Optional[_Iterable[_Union[_duration_pb2.Duration, _Mapping]]] = ...,
        source_aggregation_namespace: _Optional[str] = ...,
    ) -> None: ...

class UnderscoreOuterFeature(_message.Message):
    __slots__ = ("outer_depth", "nested_root_namespace", "outer_feature")
    OUTER_DEPTH_FIELD_NUMBER: _ClassVar[int]
    NESTED_ROOT_NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    OUTER_FEATURE_FIELD_NUMBER: _ClassVar[int]
    outer_depth: int
    nested_root_namespace: str
    outer_feature: UnderscoreParsedId
    def __init__(
        self,
        outer_depth: _Optional[int] = ...,
        nested_root_namespace: _Optional[str] = ...,
        outer_feature: _Optional[_Union[UnderscoreParsedId, _Mapping]] = ...,
    ) -> None: ...

class UnderscoreGroupedDataFrame(_message.Message):
    __slots__ = ("source", "group_keys", "filters")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    GROUP_KEYS_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    source: UnderscoreParsedId
    group_keys: _containers.RepeatedCompositeFieldContainer[UnderscoreParsedId]
    filters: _containers.RepeatedCompositeFieldContainer[UnderscoreParsedId]
    def __init__(
        self,
        source: _Optional[_Union[UnderscoreParsedId, _Mapping]] = ...,
        group_keys: _Optional[_Iterable[_Union[UnderscoreParsedId, _Mapping]]] = ...,
        filters: _Optional[_Iterable[_Union[UnderscoreParsedId, _Mapping]]] = ...,
    ) -> None: ...

class UnderscoreDataFrameAggregation(_message.Message):
    __slots__ = (
        "operation_name",
        "operands",
        "output_column_name",
        "output_type",
        "original_underscore_id",
        "option_keys",
        "option_values",
        "filters",
    )
    OPERATION_NAME_FIELD_NUMBER: _ClassVar[int]
    OPERANDS_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_UNDERSCORE_ID_FIELD_NUMBER: _ClassVar[int]
    OPTION_KEYS_FIELD_NUMBER: _ClassVar[int]
    OPTION_VALUES_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    operation_name: str
    operands: UnderscoreOperands
    output_column_name: str
    output_type: _arrow_pb2.ArrowType
    original_underscore_id: ChalkpyUnderscoreId
    option_keys: _containers.RepeatedScalarFieldContainer[str]
    option_values: _containers.RepeatedCompositeFieldContainer[_expression_pb2.LogicalExprNode]
    filters: _containers.RepeatedCompositeFieldContainer[UnderscoreParsedId]
    def __init__(
        self,
        operation_name: _Optional[str] = ...,
        operands: _Optional[_Union[UnderscoreOperands, _Mapping]] = ...,
        output_column_name: _Optional[str] = ...,
        output_type: _Optional[_Union[_arrow_pb2.ArrowType, _Mapping]] = ...,
        original_underscore_id: _Optional[_Union[ChalkpyUnderscoreId, _Mapping]] = ...,
        option_keys: _Optional[_Iterable[str]] = ...,
        option_values: _Optional[_Iterable[_Union[_expression_pb2.LogicalExprNode, _Mapping]]] = ...,
        filters: _Optional[_Iterable[_Union[UnderscoreParsedId, _Mapping]]] = ...,
    ) -> None: ...

class UnderscoreAggregatedDataFrame(_message.Message):
    __slots__ = ("grouped", "aggregations", "filters")
    GROUPED_FIELD_NUMBER: _ClassVar[int]
    AGGREGATIONS_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    grouped: UnderscoreParsedId
    aggregations: _containers.RepeatedCompositeFieldContainer[UnderscoreDataFrameAggregation]
    filters: _containers.RepeatedCompositeFieldContainer[UnderscoreParsedId]
    def __init__(
        self,
        grouped: _Optional[_Union[UnderscoreParsedId, _Mapping]] = ...,
        aggregations: _Optional[_Iterable[_Union[UnderscoreDataFrameAggregation, _Mapping]]] = ...,
        filters: _Optional[_Iterable[_Union[UnderscoreParsedId, _Mapping]]] = ...,
    ) -> None: ...

class UnderscoreDataFrameColumn(_message.Message):
    __slots__ = ("parent", "column_name", "column_type")
    PARENT_FIELD_NUMBER: _ClassVar[int]
    COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    COLUMN_TYPE_FIELD_NUMBER: _ClassVar[int]
    parent: UnderscoreParsedId
    column_name: str
    column_type: _arrow_pb2.ArrowType
    def __init__(
        self,
        parent: _Optional[_Union[UnderscoreParsedId, _Mapping]] = ...,
        column_name: _Optional[str] = ...,
        column_type: _Optional[_Union[_arrow_pb2.ArrowType, _Mapping]] = ...,
    ) -> None: ...

class UnderscoreDataFrameItemParsed(_message.Message):
    __slots__ = ("parent", "columns", "filters")
    PARENT_FIELD_NUMBER: _ClassVar[int]
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    parent: UnderscoreParsedId
    columns: _containers.RepeatedCompositeFieldContainer[UnderscoreParsedId]
    filters: _containers.RepeatedCompositeFieldContainer[UnderscoreParsedId]
    def __init__(
        self,
        parent: _Optional[_Union[UnderscoreParsedId, _Mapping]] = ...,
        columns: _Optional[_Iterable[_Union[UnderscoreParsedId, _Mapping]]] = ...,
        filters: _Optional[_Iterable[_Union[UnderscoreParsedId, _Mapping]]] = ...,
    ) -> None: ...

class UnderscoreOperation(_message.Message):
    __slots__ = ("this_id", "cpp_reg", "python_reg")
    THIS_ID_FIELD_NUMBER: _ClassVar[int]
    CPP_REG_FIELD_NUMBER: _ClassVar[int]
    PYTHON_REG_FIELD_NUMBER: _ClassVar[int]
    this_id: UnderscoreOperationId
    cpp_reg: CppRegUnderscoreOp
    python_reg: PythonRegUnderscoreOp
    def __init__(
        self,
        this_id: _Optional[_Union[UnderscoreOperationId, _Mapping]] = ...,
        cpp_reg: _Optional[_Union[CppRegUnderscoreOp, _Mapping]] = ...,
        python_reg: _Optional[_Union[PythonRegUnderscoreOp, _Mapping]] = ...,
    ) -> None: ...

class UnderscoreOperationId(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class CppRegUnderscoreOp(_message.Message):
    __slots__ = ("function_name", "positional_input_types", "named_input_types")
    class NamedInputTypesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ArgumentType
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[ArgumentType, _Mapping]] = ...
        ) -> None: ...

    FUNCTION_NAME_FIELD_NUMBER: _ClassVar[int]
    POSITIONAL_INPUT_TYPES_FIELD_NUMBER: _ClassVar[int]
    NAMED_INPUT_TYPES_FIELD_NUMBER: _ClassVar[int]
    function_name: str
    positional_input_types: _containers.RepeatedCompositeFieldContainer[ArgumentType]
    named_input_types: _containers.MessageMap[str, ArgumentType]
    def __init__(
        self,
        function_name: _Optional[str] = ...,
        positional_input_types: _Optional[_Iterable[_Union[ArgumentType, _Mapping]]] = ...,
        named_input_types: _Optional[_Mapping[str, ArgumentType]] = ...,
    ) -> None: ...

class ArgumentType(_message.Message):
    __slots__ = ("arrow_type", "callback_type", "df_param_type")
    ARROW_TYPE_FIELD_NUMBER: _ClassVar[int]
    CALLBACK_TYPE_FIELD_NUMBER: _ClassVar[int]
    DF_PARAM_TYPE_FIELD_NUMBER: _ClassVar[int]
    arrow_type: _arrow_pb2.ArrowType
    callback_type: CallbackType
    df_param_type: DataFrameParameterType
    def __init__(
        self,
        arrow_type: _Optional[_Union[_arrow_pb2.ArrowType, _Mapping]] = ...,
        callback_type: _Optional[_Union[CallbackType, _Mapping]] = ...,
        df_param_type: _Optional[_Union[DataFrameParameterType, _Mapping]] = ...,
    ) -> None: ...

class CallbackType(_message.Message):
    __slots__ = ("input_types", "output_type")
    INPUT_TYPES_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_TYPE_FIELD_NUMBER: _ClassVar[int]
    input_types: _containers.RepeatedCompositeFieldContainer[_arrow_pb2.ArrowType]
    output_type: _arrow_pb2.ArrowType
    def __init__(
        self,
        input_types: _Optional[_Iterable[_Union[_arrow_pb2.ArrowType, _Mapping]]] = ...,
        output_type: _Optional[_Union[_arrow_pb2.ArrowType, _Mapping]] = ...,
    ) -> None: ...

class DataFrameParameterType(_message.Message):
    __slots__ = ("columns",)
    class ColumnsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _arrow_pb2.ArrowType
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_arrow_pb2.ArrowType, _Mapping]] = ...
        ) -> None: ...

    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    columns: _containers.MessageMap[str, _arrow_pb2.ArrowType]
    def __init__(self, columns: _Optional[_Mapping[str, _arrow_pb2.ArrowType]] = ...) -> None: ...

class PythonRegUnderscoreOp(_message.Message):
    __slots__ = ("function_name", "params")
    class ParamsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: PythonArgument
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[PythonArgument, _Mapping]] = ...
        ) -> None: ...

    FUNCTION_NAME_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    function_name: str
    params: _containers.MessageMap[str, PythonArgument]
    def __init__(
        self, function_name: _Optional[str] = ..., params: _Optional[_Mapping[str, PythonArgument]] = ...
    ) -> None: ...

class PythonArgument(_message.Message):
    __slots__ = ("arrow_type", "string_value", "tuple")
    ARROW_TYPE_FIELD_NUMBER: _ClassVar[int]
    STRING_VALUE_FIELD_NUMBER: _ClassVar[int]
    TUPLE_FIELD_NUMBER: _ClassVar[int]
    arrow_type: _arrow_pb2.ArrowType
    string_value: str
    tuple: PythonArgumentList
    def __init__(
        self,
        arrow_type: _Optional[_Union[_arrow_pb2.ArrowType, _Mapping]] = ...,
        string_value: _Optional[str] = ...,
        tuple: _Optional[_Union[PythonArgumentList, _Mapping]] = ...,
    ) -> None: ...

class PythonArgumentList(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedCompositeFieldContainer[PythonArgument]
    def __init__(self, values: _Optional[_Iterable[_Union[PythonArgument, _Mapping]]] = ...) -> None: ...

class ChalkpyUnderscore(_message.Message):
    __slots__ = ("this_id", "underscore")
    THIS_ID_FIELD_NUMBER: _ClassVar[int]
    UNDERSCORE_FIELD_NUMBER: _ClassVar[int]
    this_id: ChalkpyUnderscoreId
    underscore: _expression_pb2.LogicalExprNode
    def __init__(
        self,
        this_id: _Optional[_Union[ChalkpyUnderscoreId, _Mapping]] = ...,
        underscore: _Optional[_Union[_expression_pb2.LogicalExprNode, _Mapping]] = ...,
    ) -> None: ...

class ChalkpyUnderscoreId(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...
