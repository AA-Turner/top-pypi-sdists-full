from chalk._gen.chalk.arrow.v1 import arrow_pb2 as _arrow_pb2
from chalk._gen.chalk.expression.v1 import expression_pb2 as _expression_pb2
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

class LogicalTableNodeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LOGICAL_TABLE_NODE_TYPE_UNSPECIFIED: _ClassVar[LogicalTableNodeType]
    LOGICAL_TABLE_NODE_TYPE_NAMED_TABLE: _ClassVar[LogicalTableNodeType]
    LOGICAL_TABLE_NODE_TYPE_TABLE_SCAN: _ClassVar[LogicalTableNodeType]
    LOGICAL_TABLE_NODE_TYPE_PROJECTION: _ClassVar[LogicalTableNodeType]
    LOGICAL_TABLE_NODE_TYPE_FILTER: _ClassVar[LogicalTableNodeType]
    LOGICAL_TABLE_NODE_TYPE_JOIN: _ClassVar[LogicalTableNodeType]
    LOGICAL_TABLE_NODE_TYPE_JOIN_AS_OF: _ClassVar[LogicalTableNodeType]
    LOGICAL_TABLE_NODE_TYPE_SEMI_JOIN: _ClassVar[LogicalTableNodeType]
    LOGICAL_TABLE_NODE_TYPE_CONCAT: _ClassVar[LogicalTableNodeType]
    LOGICAL_TABLE_NODE_TYPE_LIMIT: _ClassVar[LogicalTableNodeType]
    LOGICAL_TABLE_NODE_TYPE_SORT: _ClassVar[LogicalTableNodeType]
    LOGICAL_TABLE_NODE_TYPE_TOP_N: _ClassVar[LogicalTableNodeType]
    LOGICAL_TABLE_NODE_TYPE_AGGREGATION: _ClassVar[LogicalTableNodeType]
    LOGICAL_TABLE_NODE_TYPE_WINDOW: _ClassVar[LogicalTableNodeType]
    LOGICAL_TABLE_NODE_TYPE_EXPLODE: _ClassVar[LogicalTableNodeType]
    LOGICAL_TABLE_NODE_TYPE_PARTITION: _ClassVar[LogicalTableNodeType]
    LOGICAL_TABLE_NODE_TYPE_UNIQUE_ID: _ClassVar[LogicalTableNodeType]
    LOGICAL_TABLE_NODE_TYPE_BATCH_UDF: _ClassVar[LogicalTableNodeType]
    LOGICAL_TABLE_NODE_TYPE_VALUES: _ClassVar[LogicalTableNodeType]
    LOGICAL_TABLE_NODE_TYPE_RECHUNK: _ClassVar[LogicalTableNodeType]
    LOGICAL_TABLE_NODE_TYPE_REPLAY: _ClassVar[LogicalTableNodeType]
    LOGICAL_TABLE_NODE_TYPE_SPLIT: _ClassVar[LogicalTableNodeType]
    LOGICAL_TABLE_NODE_TYPE_CONDITIONAL: _ClassVar[LogicalTableNodeType]
    LOGICAL_TABLE_NODE_TYPE_ENSURE_DISTINCT: _ClassVar[LogicalTableNodeType]
    LOGICAL_TABLE_NODE_TYPE_TABLE_WRITE: _ClassVar[LogicalTableNodeType]
    LOGICAL_TABLE_NODE_TYPE_TIMELINE_TRACER: _ClassVar[LogicalTableNodeType]
    LOGICAL_TABLE_NODE_TYPE_SOURCE_OPERATOR_MARKER: _ClassVar[LogicalTableNodeType]
    LOGICAL_TABLE_NODE_TYPE_EMPTY_RELATION: _ClassVar[LogicalTableNodeType]

LOGICAL_TABLE_NODE_TYPE_UNSPECIFIED: LogicalTableNodeType
LOGICAL_TABLE_NODE_TYPE_NAMED_TABLE: LogicalTableNodeType
LOGICAL_TABLE_NODE_TYPE_TABLE_SCAN: LogicalTableNodeType
LOGICAL_TABLE_NODE_TYPE_PROJECTION: LogicalTableNodeType
LOGICAL_TABLE_NODE_TYPE_FILTER: LogicalTableNodeType
LOGICAL_TABLE_NODE_TYPE_JOIN: LogicalTableNodeType
LOGICAL_TABLE_NODE_TYPE_JOIN_AS_OF: LogicalTableNodeType
LOGICAL_TABLE_NODE_TYPE_SEMI_JOIN: LogicalTableNodeType
LOGICAL_TABLE_NODE_TYPE_CONCAT: LogicalTableNodeType
LOGICAL_TABLE_NODE_TYPE_LIMIT: LogicalTableNodeType
LOGICAL_TABLE_NODE_TYPE_SORT: LogicalTableNodeType
LOGICAL_TABLE_NODE_TYPE_TOP_N: LogicalTableNodeType
LOGICAL_TABLE_NODE_TYPE_AGGREGATION: LogicalTableNodeType
LOGICAL_TABLE_NODE_TYPE_WINDOW: LogicalTableNodeType
LOGICAL_TABLE_NODE_TYPE_EXPLODE: LogicalTableNodeType
LOGICAL_TABLE_NODE_TYPE_PARTITION: LogicalTableNodeType
LOGICAL_TABLE_NODE_TYPE_UNIQUE_ID: LogicalTableNodeType
LOGICAL_TABLE_NODE_TYPE_BATCH_UDF: LogicalTableNodeType
LOGICAL_TABLE_NODE_TYPE_VALUES: LogicalTableNodeType
LOGICAL_TABLE_NODE_TYPE_RECHUNK: LogicalTableNodeType
LOGICAL_TABLE_NODE_TYPE_REPLAY: LogicalTableNodeType
LOGICAL_TABLE_NODE_TYPE_SPLIT: LogicalTableNodeType
LOGICAL_TABLE_NODE_TYPE_CONDITIONAL: LogicalTableNodeType
LOGICAL_TABLE_NODE_TYPE_ENSURE_DISTINCT: LogicalTableNodeType
LOGICAL_TABLE_NODE_TYPE_TABLE_WRITE: LogicalTableNodeType
LOGICAL_TABLE_NODE_TYPE_TIMELINE_TRACER: LogicalTableNodeType
LOGICAL_TABLE_NODE_TYPE_SOURCE_OPERATOR_MARKER: LogicalTableNodeType
LOGICAL_TABLE_NODE_TYPE_EMPTY_RELATION: LogicalTableNodeType

class LogicalPlan(_message.Message):
    __slots__ = ("nodes",)
    NODES_FIELD_NUMBER: _ClassVar[int]
    nodes: _containers.RepeatedCompositeFieldContainer[LogicalTableNode]
    def __init__(self, nodes: _Optional[_Iterable[_Union[LogicalTableNode, _Mapping]]] = ...) -> None: ...

class LogicalTableNode(_message.Message):
    __slots__ = ("ltn_type", "node_id", "child_nodes", "arguments")
    class ArgumentsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: LogicalPlanArgument
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[LogicalPlanArgument, _Mapping]] = ...
        ) -> None: ...

    LTN_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    CHILD_NODES_FIELD_NUMBER: _ClassVar[int]
    ARGUMENTS_FIELD_NUMBER: _ClassVar[int]
    ltn_type: LogicalTableNodeType
    node_id: LogicalTableNodeId
    child_nodes: _containers.RepeatedCompositeFieldContainer[LogicalTableNodeId]
    arguments: _containers.MessageMap[str, LogicalPlanArgument]
    def __init__(
        self,
        ltn_type: _Optional[_Union[LogicalTableNodeType, str]] = ...,
        node_id: _Optional[_Union[LogicalTableNodeId, _Mapping]] = ...,
        child_nodes: _Optional[_Iterable[_Union[LogicalTableNodeId, _Mapping]]] = ...,
        arguments: _Optional[_Mapping[str, LogicalPlanArgument]] = ...,
    ) -> None: ...

class LogicalTableNodeId(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class LogicalPlanArgument(_message.Message):
    __slots__ = (
        "null_value",
        "string_value",
        "int64_value",
        "uint64_value",
        "bool_value",
        "bytes_value",
        "arrow_schema",
        "list_value",
        "unordered_dict_value",
        "expr_value",
    )
    NULL_VALUE_FIELD_NUMBER: _ClassVar[int]
    STRING_VALUE_FIELD_NUMBER: _ClassVar[int]
    INT64_VALUE_FIELD_NUMBER: _ClassVar[int]
    UINT64_VALUE_FIELD_NUMBER: _ClassVar[int]
    BOOL_VALUE_FIELD_NUMBER: _ClassVar[int]
    BYTES_VALUE_FIELD_NUMBER: _ClassVar[int]
    ARROW_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    LIST_VALUE_FIELD_NUMBER: _ClassVar[int]
    UNORDERED_DICT_VALUE_FIELD_NUMBER: _ClassVar[int]
    EXPR_VALUE_FIELD_NUMBER: _ClassVar[int]
    null_value: LogicalPlanArgumentNullOpt
    string_value: str
    int64_value: int
    uint64_value: int
    bool_value: bool
    bytes_value: bytes
    arrow_schema: _arrow_pb2.Schema
    list_value: LogicalPlanArgumentList
    unordered_dict_value: LogicalPlanUnorderedDict
    expr_value: _expression_pb2.LogicalExprNode
    def __init__(
        self,
        null_value: _Optional[_Union[LogicalPlanArgumentNullOpt, _Mapping]] = ...,
        string_value: _Optional[str] = ...,
        int64_value: _Optional[int] = ...,
        uint64_value: _Optional[int] = ...,
        bool_value: bool = ...,
        bytes_value: _Optional[bytes] = ...,
        arrow_schema: _Optional[_Union[_arrow_pb2.Schema, _Mapping]] = ...,
        list_value: _Optional[_Union[LogicalPlanArgumentList, _Mapping]] = ...,
        unordered_dict_value: _Optional[_Union[LogicalPlanUnorderedDict, _Mapping]] = ...,
        expr_value: _Optional[_Union[_expression_pb2.LogicalExprNode, _Mapping]] = ...,
    ) -> None: ...

class LogicalPlanArgumentList(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedCompositeFieldContainer[LogicalPlanArgument]
    def __init__(self, values: _Optional[_Iterable[_Union[LogicalPlanArgument, _Mapping]]] = ...) -> None: ...

class LogicalPlanUnorderedDict(_message.Message):
    __slots__ = ("items",)
    class ItemsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: LogicalPlanArgument
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[LogicalPlanArgument, _Mapping]] = ...
        ) -> None: ...

    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.MessageMap[str, LogicalPlanArgument]
    def __init__(self, items: _Optional[_Mapping[str, LogicalPlanArgument]] = ...) -> None: ...

class LogicalPlanArgumentNullOpt(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
