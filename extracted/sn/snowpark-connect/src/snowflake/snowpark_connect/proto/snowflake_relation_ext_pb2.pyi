from pyspark.sql.connect.proto import relations_pb2 as _relations_pb2
from pyspark.sql.connect.proto import expressions_pb2 as _expressions_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Aggregate(_message.Message):
    __slots__ = ["aggregate_expressions", "group_type", "grouping_expressions", "grouping_sets", "having_condition", "input", "pivot"]
    class GroupType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class GroupingSets(_message.Message):
        __slots__ = ["grouping_set"]
        GROUPING_SET_FIELD_NUMBER: _ClassVar[int]
        grouping_set: _containers.RepeatedCompositeFieldContainer[_expressions_pb2.Expression]
        def __init__(self, grouping_set: _Optional[_Iterable[_Union[_expressions_pb2.Expression, _Mapping]]] = ...) -> None: ...
    class Pivot(_message.Message):
        __slots__ = ["pivot_columns", "pivot_values"]
        class PivotValue(_message.Message):
            __slots__ = ["alias", "values"]
            ALIAS_FIELD_NUMBER: _ClassVar[int]
            VALUES_FIELD_NUMBER: _ClassVar[int]
            alias: str
            values: _containers.RepeatedCompositeFieldContainer[_expressions_pb2.Expression.Literal]
            def __init__(self, values: _Optional[_Iterable[_Union[_expressions_pb2.Expression.Literal, _Mapping]]] = ..., alias: _Optional[str] = ...) -> None: ...
        PIVOT_COLUMNS_FIELD_NUMBER: _ClassVar[int]
        PIVOT_VALUES_FIELD_NUMBER: _ClassVar[int]
        pivot_columns: _containers.RepeatedCompositeFieldContainer[_expressions_pb2.Expression]
        pivot_values: _containers.RepeatedCompositeFieldContainer[Aggregate.Pivot.PivotValue]
        def __init__(self, pivot_columns: _Optional[_Iterable[_Union[_expressions_pb2.Expression, _Mapping]]] = ..., pivot_values: _Optional[_Iterable[_Union[Aggregate.Pivot.PivotValue, _Mapping]]] = ...) -> None: ...
    AGGREGATE_EXPRESSIONS_FIELD_NUMBER: _ClassVar[int]
    GROUPING_EXPRESSIONS_FIELD_NUMBER: _ClassVar[int]
    GROUPING_SETS_FIELD_NUMBER: _ClassVar[int]
    GROUP_TYPE_CUBE: Aggregate.GroupType
    GROUP_TYPE_FIELD_NUMBER: _ClassVar[int]
    GROUP_TYPE_GROUPBY: Aggregate.GroupType
    GROUP_TYPE_GROUPING_SETS: Aggregate.GroupType
    GROUP_TYPE_PIVOT: Aggregate.GroupType
    GROUP_TYPE_ROLLUP: Aggregate.GroupType
    GROUP_TYPE_UNSPECIFIED: Aggregate.GroupType
    HAVING_CONDITION_FIELD_NUMBER: _ClassVar[int]
    INPUT_FIELD_NUMBER: _ClassVar[int]
    PIVOT_FIELD_NUMBER: _ClassVar[int]
    aggregate_expressions: _containers.RepeatedCompositeFieldContainer[_expressions_pb2.Expression]
    group_type: Aggregate.GroupType
    grouping_expressions: _containers.RepeatedCompositeFieldContainer[_expressions_pb2.Expression]
    grouping_sets: _containers.RepeatedCompositeFieldContainer[Aggregate.GroupingSets]
    having_condition: _expressions_pb2.Expression
    input: _relations_pb2.Relation
    pivot: Aggregate.Pivot
    def __init__(self, input: _Optional[_Union[_relations_pb2.Relation, _Mapping]] = ..., group_type: _Optional[_Union[Aggregate.GroupType, str]] = ..., grouping_expressions: _Optional[_Iterable[_Union[_expressions_pb2.Expression, _Mapping]]] = ..., aggregate_expressions: _Optional[_Iterable[_Union[_expressions_pb2.Expression, _Mapping]]] = ..., pivot: _Optional[_Union[Aggregate.Pivot, _Mapping]] = ..., grouping_sets: _Optional[_Iterable[_Union[Aggregate.GroupingSets, _Mapping]]] = ..., having_condition: _Optional[_Union[_expressions_pb2.Expression, _Mapping]] = ...) -> None: ...

class Extension(_message.Message):
    __slots__ = ["aggregate", "lateral_join", "qualify_leading_columns", "rdd_map", "rdd_reduce", "subquery_column_aliases", "udtf_with_table_arguments"]
    AGGREGATE_FIELD_NUMBER: _ClassVar[int]
    LATERAL_JOIN_FIELD_NUMBER: _ClassVar[int]
    QUALIFY_LEADING_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    RDD_MAP_FIELD_NUMBER: _ClassVar[int]
    RDD_REDUCE_FIELD_NUMBER: _ClassVar[int]
    SUBQUERY_COLUMN_ALIASES_FIELD_NUMBER: _ClassVar[int]
    UDTF_WITH_TABLE_ARGUMENTS_FIELD_NUMBER: _ClassVar[int]
    aggregate: Aggregate
    lateral_join: LateralJoin
    qualify_leading_columns: QualifyLeadingColumns
    rdd_map: RddMap
    rdd_reduce: RddReduce
    subquery_column_aliases: SubqueryColumnAliases
    udtf_with_table_arguments: UDTFWithTableArguments
    def __init__(self, rdd_map: _Optional[_Union[RddMap, _Mapping]] = ..., rdd_reduce: _Optional[_Union[RddReduce, _Mapping]] = ..., subquery_column_aliases: _Optional[_Union[SubqueryColumnAliases, _Mapping]] = ..., lateral_join: _Optional[_Union[LateralJoin, _Mapping]] = ..., udtf_with_table_arguments: _Optional[_Union[UDTFWithTableArguments, _Mapping]] = ..., aggregate: _Optional[_Union[Aggregate, _Mapping]] = ..., qualify_leading_columns: _Optional[_Union[QualifyLeadingColumns, _Mapping]] = ...) -> None: ...

class LateralJoin(_message.Message):
    __slots__ = ["left", "right"]
    LEFT_FIELD_NUMBER: _ClassVar[int]
    RIGHT_FIELD_NUMBER: _ClassVar[int]
    left: _relations_pb2.Relation
    right: _relations_pb2.Relation
    def __init__(self, left: _Optional[_Union[_relations_pb2.Relation, _Mapping]] = ..., right: _Optional[_Union[_relations_pb2.Relation, _Mapping]] = ...) -> None: ...

class QualifyLeadingColumns(_message.Message):
    __slots__ = ["input", "num_trailing_unqualified_columns", "qualifier"]
    INPUT_FIELD_NUMBER: _ClassVar[int]
    NUM_TRAILING_UNQUALIFIED_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    QUALIFIER_FIELD_NUMBER: _ClassVar[int]
    input: _relations_pb2.Relation
    num_trailing_unqualified_columns: int
    qualifier: str
    def __init__(self, input: _Optional[_Union[_relations_pb2.Relation, _Mapping]] = ..., num_trailing_unqualified_columns: _Optional[int] = ..., qualifier: _Optional[str] = ...) -> None: ...

class RddMap(_message.Message):
    __slots__ = ["func", "input"]
    FUNC_FIELD_NUMBER: _ClassVar[int]
    INPUT_FIELD_NUMBER: _ClassVar[int]
    func: bytes
    input: _relations_pb2.Relation
    def __init__(self, input: _Optional[_Union[_relations_pb2.Relation, _Mapping]] = ..., func: _Optional[bytes] = ...) -> None: ...

class RddReduce(_message.Message):
    __slots__ = ["func", "input"]
    FUNC_FIELD_NUMBER: _ClassVar[int]
    INPUT_FIELD_NUMBER: _ClassVar[int]
    func: bytes
    input: _relations_pb2.Relation
    def __init__(self, input: _Optional[_Union[_relations_pb2.Relation, _Mapping]] = ..., func: _Optional[bytes] = ...) -> None: ...

class SubqueryColumnAliases(_message.Message):
    __slots__ = ["aliases", "input"]
    ALIASES_FIELD_NUMBER: _ClassVar[int]
    INPUT_FIELD_NUMBER: _ClassVar[int]
    aliases: _containers.RepeatedScalarFieldContainer[str]
    input: _relations_pb2.Relation
    def __init__(self, input: _Optional[_Union[_relations_pb2.Relation, _Mapping]] = ..., aliases: _Optional[_Iterable[str]] = ...) -> None: ...

class TableArgumentInfo(_message.Message):
    __slots__ = ["table_argument", "table_argument_idx"]
    TABLE_ARGUMENT_FIELD_NUMBER: _ClassVar[int]
    TABLE_ARGUMENT_IDX_FIELD_NUMBER: _ClassVar[int]
    table_argument: _relations_pb2.Relation
    table_argument_idx: int
    def __init__(self, table_argument: _Optional[_Union[_relations_pb2.Relation, _Mapping]] = ..., table_argument_idx: _Optional[int] = ...) -> None: ...

class UDTFWithTableArguments(_message.Message):
    __slots__ = ["arguments", "function_name", "table_arguments"]
    ARGUMENTS_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_NAME_FIELD_NUMBER: _ClassVar[int]
    TABLE_ARGUMENTS_FIELD_NUMBER: _ClassVar[int]
    arguments: _containers.RepeatedCompositeFieldContainer[_expressions_pb2.Expression]
    function_name: str
    table_arguments: _containers.RepeatedCompositeFieldContainer[TableArgumentInfo]
    def __init__(self, function_name: _Optional[str] = ..., arguments: _Optional[_Iterable[_Union[_expressions_pb2.Expression, _Mapping]]] = ..., table_arguments: _Optional[_Iterable[_Union[TableArgumentInfo, _Mapping]]] = ...) -> None: ...
