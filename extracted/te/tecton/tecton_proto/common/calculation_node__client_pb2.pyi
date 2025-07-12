from tecton_proto.common import data_type__client_pb2 as _data_type__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

ADDITION: OperationType
AND: OperationType
CENTURY: DatePart
COALESCE: OperationType
DATE_DIFF: OperationType
DATE_PART_UNSPECIFIED: DatePart
DAY: DatePart
DECADE: DatePart
DESCRIPTOR: _descriptor.FileDescriptor
DIVISION: OperationType
EQUALS: OperationType
GREATER_THAN: OperationType
GREATER_THAN_EQUALS: OperationType
HOUR: DatePart
LESS_THAN: OperationType
LESS_THAN_EQUALS: OperationType
MICROSECONDS: DatePart
MILLENNIUM: DatePart
MILLISECONDS: DatePart
MINUTE: DatePart
MONTH: DatePart
MULTIPLICATION: OperationType
NOT: OperationType
NOT_EQUALS: OperationType
OPERATION_UNSPECIFIED: OperationType
OR: OperationType
QUARTER: DatePart
SECOND: DatePart
SUBTRACTION: OperationType
TRY_STRPTIME: OperationType
WEEK: DatePart
YEAR: DatePart

class AbstractSyntaxTreeNode(_message.Message):
    __slots__ = ["case_statement", "column_reference", "date_part", "dtype", "literal_value", "operation"]
    CASE_STATEMENT_FIELD_NUMBER: _ClassVar[int]
    COLUMN_REFERENCE_FIELD_NUMBER: _ClassVar[int]
    DATE_PART_FIELD_NUMBER: _ClassVar[int]
    DTYPE_FIELD_NUMBER: _ClassVar[int]
    LITERAL_VALUE_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    case_statement: CaseStatement
    column_reference: str
    date_part: DatePart
    dtype: _data_type__client_pb2.DataType
    literal_value: LiteralValue
    operation: Operation
    def __init__(self, dtype: _Optional[_Union[_data_type__client_pb2.DataType, _Mapping]] = ..., literal_value: _Optional[_Union[LiteralValue, _Mapping]] = ..., column_reference: _Optional[str] = ..., operation: _Optional[_Union[Operation, _Mapping]] = ..., date_part: _Optional[_Union[DatePart, str]] = ..., case_statement: _Optional[_Union[CaseStatement, _Mapping]] = ...) -> None: ...

class CaseStatement(_message.Message):
    __slots__ = ["else_clause", "when_clauses"]
    ELSE_CLAUSE_FIELD_NUMBER: _ClassVar[int]
    WHEN_CLAUSES_FIELD_NUMBER: _ClassVar[int]
    else_clause: ElseClause
    when_clauses: _containers.RepeatedCompositeFieldContainer[WhenClause]
    def __init__(self, when_clauses: _Optional[_Iterable[_Union[WhenClause, _Mapping]]] = ..., else_clause: _Optional[_Union[ElseClause, _Mapping]] = ...) -> None: ...

class ElseClause(_message.Message):
    __slots__ = ["result"]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: AbstractSyntaxTreeNode
    def __init__(self, result: _Optional[_Union[AbstractSyntaxTreeNode, _Mapping]] = ...) -> None: ...

class LiteralValue(_message.Message):
    __slots__ = ["bool_value", "float32_value", "float64_value", "int64_value", "null_value", "string_value"]
    BOOL_VALUE_FIELD_NUMBER: _ClassVar[int]
    FLOAT32_VALUE_FIELD_NUMBER: _ClassVar[int]
    FLOAT64_VALUE_FIELD_NUMBER: _ClassVar[int]
    INT64_VALUE_FIELD_NUMBER: _ClassVar[int]
    NULL_VALUE_FIELD_NUMBER: _ClassVar[int]
    STRING_VALUE_FIELD_NUMBER: _ClassVar[int]
    bool_value: bool
    float32_value: float
    float64_value: float
    int64_value: int
    null_value: NullLiteralValue
    string_value: str
    def __init__(self, float32_value: _Optional[float] = ..., float64_value: _Optional[float] = ..., int64_value: _Optional[int] = ..., bool_value: bool = ..., string_value: _Optional[str] = ..., null_value: _Optional[_Union[NullLiteralValue, _Mapping]] = ...) -> None: ...

class NullLiteralValue(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class Operation(_message.Message):
    __slots__ = ["operands", "operation"]
    OPERANDS_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    operands: _containers.RepeatedCompositeFieldContainer[AbstractSyntaxTreeNode]
    operation: OperationType
    def __init__(self, operation: _Optional[_Union[OperationType, str]] = ..., operands: _Optional[_Iterable[_Union[AbstractSyntaxTreeNode, _Mapping]]] = ...) -> None: ...

class WhenClause(_message.Message):
    __slots__ = ["condition", "result"]
    CONDITION_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    condition: AbstractSyntaxTreeNode
    result: AbstractSyntaxTreeNode
    def __init__(self, condition: _Optional[_Union[AbstractSyntaxTreeNode, _Mapping]] = ..., result: _Optional[_Union[AbstractSyntaxTreeNode, _Mapping]] = ...) -> None: ...

class OperationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class DatePart(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
