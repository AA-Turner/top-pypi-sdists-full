from pyspark.sql.connect.proto import relations_pb2 as _relations_pb2
from pyspark.sql.connect.proto import expressions_pb2 as _expressions_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Extension(_message.Message):
    __slots__ = ("rdd_map", "rdd_reduce", "subquery_column_aliases", "lateral_join", "udtf_with_table_arguments", "aggregate")
    RDD_MAP_FIELD_NUMBER: _ClassVar[int]
    RDD_REDUCE_FIELD_NUMBER: _ClassVar[int]
    SUBQUERY_COLUMN_ALIASES_FIELD_NUMBER: _ClassVar[int]
    LATERAL_JOIN_FIELD_NUMBER: _ClassVar[int]
    UDTF_WITH_TABLE_ARGUMENTS_FIELD_NUMBER: _ClassVar[int]
    AGGREGATE_FIELD_NUMBER: _ClassVar[int]
    rdd_map: RddMap
    rdd_reduce: RddReduce
    subquery_column_aliases: SubqueryColumnAliases
    lateral_join: LateralJoin
    udtf_with_table_arguments: UDTFWithTableArguments
    aggregate: Aggregate
    def __init__(self, rdd_map: _Optional[_Union[RddMap, _Mapping]] = ..., rdd_reduce: _Optional[_Union[RddReduce, _Mapping]] = ..., subquery_column_aliases: _Optional[_Union[SubqueryColumnAliases, _Mapping]] = ..., lateral_join: _Optional[_Union[LateralJoin, _Mapping]] = ..., udtf_with_table_arguments: _Optional[_Union[UDTFWithTableArguments, _Mapping]] = ..., aggregate: _Optional[_Union[Aggregate, _Mapping]] = ...) -> None: ...

class RddMap(_message.Message):
    __slots__ = ("input", "func")
    INPUT_FIELD_NUMBER: _ClassVar[int]
    FUNC_FIELD_NUMBER: _ClassVar[int]
    input: _relations_pb2.Relation
    func: bytes
    def __init__(self, input: _Optional[_Union[_relations_pb2.Relation, _Mapping]] = ..., func: _Optional[bytes] = ...) -> None: ...

class RddReduce(_message.Message):
    __slots__ = ("input", "func")
    INPUT_FIELD_NUMBER: _ClassVar[int]
    FUNC_FIELD_NUMBER: _ClassVar[int]
    input: _relations_pb2.Relation
    func: bytes
    def __init__(self, input: _Optional[_Union[_relations_pb2.Relation, _Mapping]] = ..., func: _Optional[bytes] = ...) -> None: ...

class SubqueryColumnAliases(_message.Message):
    __slots__ = ("input", "aliases")
    INPUT_FIELD_NUMBER: _ClassVar[int]
    ALIASES_FIELD_NUMBER: _ClassVar[int]
    input: _relations_pb2.Relation
    aliases: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, input: _Optional[_Union[_relations_pb2.Relation, _Mapping]] = ..., aliases: _Optional[_Iterable[str]] = ...) -> None: ...

class LateralJoin(_message.Message):
    __slots__ = ("left", "right")
    LEFT_FIELD_NUMBER: _ClassVar[int]
    RIGHT_FIELD_NUMBER: _ClassVar[int]
    left: _relations_pb2.Relation
    right: _relations_pb2.Relation
    def __init__(self, left: _Optional[_Union[_relations_pb2.Relation, _Mapping]] = ..., right: _Optional[_Union[_relations_pb2.Relation, _Mapping]] = ...) -> None: ...

class UDTFWithTableArguments(_message.Message):
    __slots__ = ("function_name", "arguments", "table_arguments")
    FUNCTION_NAME_FIELD_NUMBER: _ClassVar[int]
    ARGUMENTS_FIELD_NUMBER: _ClassVar[int]
    TABLE_ARGUMENTS_FIELD_NUMBER: _ClassVar[int]
    function_name: str
    arguments: _containers.RepeatedCompositeFieldContainer[_expressions_pb2.Expression]
    table_arguments: _containers.RepeatedCompositeFieldContainer[TableArgumentInfo]
    def __init__(self, function_name: _Optional[str] = ..., arguments: _Optional[_Iterable[_Union[_expressions_pb2.Expression, _Mapping]]] = ..., table_arguments: _Optional[_Iterable[_Union[TableArgumentInfo, _Mapping]]] = ...) -> None: ...

class TableArgumentInfo(_message.Message):
    __slots__ = ("table_argument", "table_argument_idx")
    TABLE_ARGUMENT_FIELD_NUMBER: _ClassVar[int]
    TABLE_ARGUMENT_IDX_FIELD_NUMBER: _ClassVar[int]
    table_argument: _relations_pb2.Relation
    table_argument_idx: int
    def __init__(self, table_argument: _Optional[_Union[_relations_pb2.Relation, _Mapping]] = ..., table_argument_idx: _Optional[int] = ...) -> None: ...

class Aggregate(_message.Message):
    __slots__ = ("input", "group_type", "grouping_expressions", "aggregate_expressions", "pivot", "grouping_sets", "having_condition")
    class GroupType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        GROUP_TYPE_UNSPECIFIED: _ClassVar[Aggregate.GroupType]
        GROUP_TYPE_GROUPBY: _ClassVar[Aggregate.GroupType]
        GROUP_TYPE_ROLLUP: _ClassVar[Aggregate.GroupType]
        GROUP_TYPE_CUBE: _ClassVar[Aggregate.GroupType]
        GROUP_TYPE_PIVOT: _ClassVar[Aggregate.GroupType]
        GROUP_TYPE_GROUPING_SETS: _ClassVar[Aggregate.GroupType]
    GROUP_TYPE_UNSPECIFIED: Aggregate.GroupType
    GROUP_TYPE_GROUPBY: Aggregate.GroupType
    GROUP_TYPE_ROLLUP: Aggregate.GroupType
    GROUP_TYPE_CUBE: Aggregate.GroupType
    GROUP_TYPE_PIVOT: Aggregate.GroupType
    GROUP_TYPE_GROUPING_SETS: Aggregate.GroupType
    class Pivot(_message.Message):
        __slots__ = ("pivot_columns", "pivot_values")
        class PivotValue(_message.Message):
            __slots__ = ("values", "alias")
            VALUES_FIELD_NUMBER: _ClassVar[int]
            ALIAS_FIELD_NUMBER: _ClassVar[int]
            values: _containers.RepeatedCompositeFieldContainer[_expressions_pb2.Expression.Literal]
            alias: str
            def __init__(self, values: _Optional[_Iterable[_Union[_expressions_pb2.Expression.Literal, _Mapping]]] = ..., alias: _Optional[str] = ...) -> None: ...
        PIVOT_COLUMNS_FIELD_NUMBER: _ClassVar[int]
        PIVOT_VALUES_FIELD_NUMBER: _ClassVar[int]
        pivot_columns: _containers.RepeatedCompositeFieldContainer[_expressions_pb2.Expression]
        pivot_values: _containers.RepeatedCompositeFieldContainer[Aggregate.Pivot.PivotValue]
        def __init__(self, pivot_columns: _Optional[_Iterable[_Union[_expressions_pb2.Expression, _Mapping]]] = ..., pivot_values: _Optional[_Iterable[_Union[Aggregate.Pivot.PivotValue, _Mapping]]] = ...) -> None: ...
    class GroupingSets(_message.Message):
        __slots__ = ("grouping_set",)
        GROUPING_SET_FIELD_NUMBER: _ClassVar[int]
        grouping_set: _containers.RepeatedCompositeFieldContainer[_expressions_pb2.Expression]
        def __init__(self, grouping_set: _Optional[_Iterable[_Union[_expressions_pb2.Expression, _Mapping]]] = ...) -> None: ...
    INPUT_FIELD_NUMBER: _ClassVar[int]
    GROUP_TYPE_FIELD_NUMBER: _ClassVar[int]
    GROUPING_EXPRESSIONS_FIELD_NUMBER: _ClassVar[int]
    AGGREGATE_EXPRESSIONS_FIELD_NUMBER: _ClassVar[int]
    PIVOT_FIELD_NUMBER: _ClassVar[int]
    GROUPING_SETS_FIELD_NUMBER: _ClassVar[int]
    HAVING_CONDITION_FIELD_NUMBER: _ClassVar[int]
    input: _relations_pb2.Relation
    group_type: Aggregate.GroupType
    grouping_expressions: _containers.RepeatedCompositeFieldContainer[_expressions_pb2.Expression]
    aggregate_expressions: _containers.RepeatedCompositeFieldContainer[_expressions_pb2.Expression]
    pivot: Aggregate.Pivot
    grouping_sets: _containers.RepeatedCompositeFieldContainer[Aggregate.GroupingSets]
    having_condition: _expressions_pb2.Expression
    def __init__(self, input: _Optional[_Union[_relations_pb2.Relation, _Mapping]] = ..., group_type: _Optional[_Union[Aggregate.GroupType, str]] = ..., grouping_expressions: _Optional[_Iterable[_Union[_expressions_pb2.Expression, _Mapping]]] = ..., aggregate_expressions: _Optional[_Iterable[_Union[_expressions_pb2.Expression, _Mapping]]] = ..., pivot: _Optional[_Union[Aggregate.Pivot, _Mapping]] = ..., grouping_sets: _Optional[_Iterable[_Union[Aggregate.GroupingSets, _Mapping]]] = ..., having_condition: _Optional[_Union[_expressions_pb2.Expression, _Mapping]] = ...) -> None: ...
