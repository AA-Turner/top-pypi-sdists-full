from abc import ABC
from typing import List
from typing import Optional
from typing import Union

from tecton_core.data_types import DataType
from tecton_core.data_types import data_type_from_proto
from tecton_core.errors import TectonInternalError
from tecton_core.specs import utils
from tecton_proto.common import calculation_node__client_pb2 as calculation_node_pb2


@utils.frozen_strict
class AbstractSyntaxTreeNodeSpec(ABC):
    dtype: Optional[DataType]

    @classmethod
    def from_proto(cls, node: calculation_node_pb2.AbstractSyntaxTreeNode) -> "AbstractSyntaxTreeNodeSpec":
        value_type = node.WhichOneof("value")
        if value_type == "literal_value":
            return LiteralValueNodeSpec.from_proto(node)
        elif value_type == "column_reference":
            return ColumnReferenceNodeSpec.from_proto(node)
        elif value_type == "operation":
            return OperationNodeSpec.from_proto(node)
        elif value_type == "date_part":
            return DatePartNodeSpec.from_proto(node)
        elif value_type == "case_statement":
            return CaseStatementNodeSpec.from_proto(node)
        else:
            msg = f"Unknown AbstractSyntaxTreeNode Type {value_type}"
            raise TectonInternalError(msg)


@utils.frozen_strict
class OperationNodeSpec(AbstractSyntaxTreeNodeSpec):
    dtype: DataType
    operation: calculation_node_pb2.OperationType
    operands: List[AbstractSyntaxTreeNodeSpec]

    @classmethod
    def from_proto(cls, proto: calculation_node_pb2.AbstractSyntaxTreeNode) -> "OperationNodeSpec":
        operation_proto = proto.operation
        return cls(
            dtype=data_type_from_proto(proto.dtype),
            operation=operation_proto.operation,
            operands=[AbstractSyntaxTreeNodeSpec.from_proto(operand) for operand in operation_proto.operands],
        )


@utils.frozen_strict
class LiteralValueNodeSpec(AbstractSyntaxTreeNodeSpec):
    dtype: Optional[DataType]
    value: Optional[Union[float, int, bool, str]]

    @classmethod
    def from_proto(cls, proto: calculation_node_pb2.AbstractSyntaxTreeNode) -> "LiteralValueNodeSpec":
        literal_value_proto = proto.literal_value
        value_type = literal_value_proto.WhichOneof("value")
        if value_type == "null_value":
            return cls(dtype=None, value=None)
        else:
            return cls(dtype=data_type_from_proto(proto.dtype), value=getattr(literal_value_proto, value_type))


@utils.frozen_strict
class ColumnReferenceNodeSpec(AbstractSyntaxTreeNodeSpec):
    dtype: DataType
    value: str

    @classmethod
    def from_proto(cls, proto: calculation_node_pb2.AbstractSyntaxTreeNode) -> "ColumnReferenceNodeSpec":
        return cls(dtype=data_type_from_proto(proto.dtype), value=proto.column_reference)


@utils.frozen_strict
class DatePartNodeSpec(AbstractSyntaxTreeNodeSpec):
    value: calculation_node_pb2.DatePart.ValueType

    @classmethod
    def from_proto(cls, proto: calculation_node_pb2.AbstractSyntaxTreeNode) -> "DatePartNodeSpec":
        return cls(value=proto.date_part, dtype=None)


@utils.frozen_strict
class WhenClauseSpec:
    condition: AbstractSyntaxTreeNodeSpec
    result: AbstractSyntaxTreeNodeSpec

    @classmethod
    def from_proto(cls, proto: calculation_node_pb2.WhenClause) -> "WhenClauseSpec":
        return cls(
            condition=AbstractSyntaxTreeNodeSpec.from_proto(proto.condition),
            result=AbstractSyntaxTreeNodeSpec.from_proto(proto.result),
        )


@utils.frozen_strict
class ElseClauseSpec:
    result: AbstractSyntaxTreeNodeSpec

    @classmethod
    def from_proto(cls, proto: calculation_node_pb2.ElseClause) -> "ElseClauseSpec":
        if proto.HasField("result"):
            return cls(result=AbstractSyntaxTreeNodeSpec.from_proto(proto.result))


@utils.frozen_strict
class CaseStatementNodeSpec(AbstractSyntaxTreeNodeSpec):
    dtype: DataType
    when_clauses: List[WhenClauseSpec]
    else_clause: Optional[ElseClauseSpec] = None

    @classmethod
    def from_proto(cls, proto: calculation_node_pb2.AbstractSyntaxTreeNode) -> "CaseStatementNodeSpec":
        return cls(
            data_type_from_proto(proto.dtype),
            when_clauses=[
                WhenClauseSpec.from_proto(when_clause_proto) for when_clause_proto in proto.case_statement.when_clauses
            ],
            else_clause=ElseClauseSpec.from_proto(proto.case_statement.else_clause),
        )
