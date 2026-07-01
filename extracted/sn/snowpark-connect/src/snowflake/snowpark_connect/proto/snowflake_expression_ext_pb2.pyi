from pyspark.sql.connect.proto import expressions_pb2 as _expressions_pb2
from pyspark.sql.connect.proto import relations_pb2 as _relations_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ExpExtension(_message.Message):
    __slots__ = ("named_argument", "subquery_expression", "interval_literal")
    NAMED_ARGUMENT_FIELD_NUMBER: _ClassVar[int]
    SUBQUERY_EXPRESSION_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_LITERAL_FIELD_NUMBER: _ClassVar[int]
    named_argument: NamedArgumentExpression
    subquery_expression: SubqueryExpression
    interval_literal: IntervalLiteralExpression
    def __init__(self, named_argument: _Optional[_Union[NamedArgumentExpression, _Mapping]] = ..., subquery_expression: _Optional[_Union[SubqueryExpression, _Mapping]] = ..., interval_literal: _Optional[_Union[IntervalLiteralExpression, _Mapping]] = ...) -> None: ...

class NamedArgumentExpression(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: _expressions_pb2.Expression
    def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_expressions_pb2.Expression, _Mapping]] = ...) -> None: ...

class SubqueryExpression(_message.Message):
    __slots__ = ("input", "subquery_type", "table_arg_options", "in_subquery_values")
    class SubqueryType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUBQUERY_TYPE_UNKNOWN: _ClassVar[SubqueryExpression.SubqueryType]
        SUBQUERY_TYPE_SCALAR: _ClassVar[SubqueryExpression.SubqueryType]
        SUBQUERY_TYPE_EXISTS: _ClassVar[SubqueryExpression.SubqueryType]
        SUBQUERY_TYPE_TABLE_ARG: _ClassVar[SubqueryExpression.SubqueryType]
        SUBQUERY_TYPE_IN: _ClassVar[SubqueryExpression.SubqueryType]
    SUBQUERY_TYPE_UNKNOWN: SubqueryExpression.SubqueryType
    SUBQUERY_TYPE_SCALAR: SubqueryExpression.SubqueryType
    SUBQUERY_TYPE_EXISTS: SubqueryExpression.SubqueryType
    SUBQUERY_TYPE_TABLE_ARG: SubqueryExpression.SubqueryType
    SUBQUERY_TYPE_IN: SubqueryExpression.SubqueryType
    class TableArgOptions(_message.Message):
        __slots__ = ("partition_spec", "order_spec", "with_single_partition")
        PARTITION_SPEC_FIELD_NUMBER: _ClassVar[int]
        ORDER_SPEC_FIELD_NUMBER: _ClassVar[int]
        WITH_SINGLE_PARTITION_FIELD_NUMBER: _ClassVar[int]
        partition_spec: _containers.RepeatedCompositeFieldContainer[_expressions_pb2.Expression]
        order_spec: _containers.RepeatedCompositeFieldContainer[_expressions_pb2.Expression.SortOrder]
        with_single_partition: bool
        def __init__(self, partition_spec: _Optional[_Iterable[_Union[_expressions_pb2.Expression, _Mapping]]] = ..., order_spec: _Optional[_Iterable[_Union[_expressions_pb2.Expression.SortOrder, _Mapping]]] = ..., with_single_partition: bool = ...) -> None: ...
    INPUT_FIELD_NUMBER: _ClassVar[int]
    SUBQUERY_TYPE_FIELD_NUMBER: _ClassVar[int]
    TABLE_ARG_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    IN_SUBQUERY_VALUES_FIELD_NUMBER: _ClassVar[int]
    input: _relations_pb2.Relation
    subquery_type: SubqueryExpression.SubqueryType
    table_arg_options: SubqueryExpression.TableArgOptions
    in_subquery_values: _containers.RepeatedCompositeFieldContainer[_expressions_pb2.Expression]
    def __init__(self, input: _Optional[_Union[_relations_pb2.Relation, _Mapping]] = ..., subquery_type: _Optional[_Union[SubqueryExpression.SubqueryType, str]] = ..., table_arg_options: _Optional[_Union[SubqueryExpression.TableArgOptions, _Mapping]] = ..., in_subquery_values: _Optional[_Iterable[_Union[_expressions_pb2.Expression, _Mapping]]] = ...) -> None: ...

class IntervalLiteralExpression(_message.Message):
    __slots__ = ("literal", "start_field", "end_field")
    LITERAL_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_FIELD_NUMBER: _ClassVar[int]
    literal: _expressions_pb2.Expression.Literal
    start_field: int
    end_field: int
    def __init__(self, literal: _Optional[_Union[_expressions_pb2.Expression.Literal, _Mapping]] = ..., start_field: _Optional[int] = ..., end_field: _Optional[int] = ...) -> None: ...
