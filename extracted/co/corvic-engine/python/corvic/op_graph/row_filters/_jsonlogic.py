from collections.abc import Mapping, Sequence
from typing import Final, Literal

import more_itertools
import pyarrow as pa
from google.protobuf import json_format, struct_pb2

from corvic.op_graph.row_filters._row_filters import (
    CombineFilters,
    CompareColumnToLiteral,
    RowFilter,
    eq,
    ge,
    gt,
    le,
    lt,
    ne,
)
from corvic.pa_scalar import from_value
from corvic.result import Error, InvalidArgumentError, Ok


class _Error(Error):
    """Internal error type."""


def _validate_column_to_literal(row_filter: CompareColumnToLiteral):
    match from_value(row_filter.literal_value, row_filter.dtype):
        case Ok():
            pass
        case InvalidArgumentError() as err:
            raise _Error.from_(err)


def _validate_combine_filters(row_filter: CombineFilters):
    for f in row_filter.row_filters:
        _validate_row_filter(f)


def _validate_row_filter(row_filter: RowFilter):
    match row_filter:
        case CompareColumnToLiteral():
            _validate_column_to_literal(row_filter)
        case CombineFilters():
            _validate_combine_filters(row_filter)


def _validate(row_filter: RowFilter) -> Ok[RowFilter] | _Error:
    """Validate row_filter contains valid literals.

    Row filters are not validated on construction because (a) historically
    they have not been validated and (b) it would make building compound expressions
    tedious.

    validate_row_filter exists for cases where user input needs to be validated
    before continuing.
    """
    try:
        _validate_row_filter(row_filter)
    except _Error as exc:
        return exc

    return Ok(row_filter)


def _var_name(value: struct_pb2.Value) -> str:
    match value.WhichOneof("kind"):
        case "struct_value":
            name = value.struct_value.fields.get("var", None)
            if name is None or not name.HasField("string_value"):
                raise _Error("invalid var operation")
            return name.string_value
        case None:
            raise _Error("cannot parse value")
        case _:
            raise _Error("unexpected operation type")


def _simple_compare(
    op: Literal["==", "!=", "<=", ">=", "<", ">"],
    operands: Sequence[struct_pb2.Value],
    column_dtypes: Mapping[str, pa.DataType],
) -> RowFilter:
    expected_literal_operands: Final = 2
    if len(operands) != expected_literal_operands:
        raise _Error("unsupported literal expression passed")
    column_name = _var_name(operands[0])

    literal = operands[1]

    dtype = column_dtypes.get(column_name, None)
    if dtype is None:
        raise _Error("unknown literal type", column_name=column_name)

    match op:
        case "==":
            return eq(column_name, literal, dtype)
        case "!=":
            return ne(column_name, literal, dtype)
        case "<=":
            return le(column_name, literal, dtype)
        case ">=":
            return ge(column_name, literal, dtype)
        case "<":
            return lt(column_name, literal, dtype)
        case ">":
            return gt(column_name, literal, dtype)


def _compound_compare(
    op: Literal["and", "or"],
    operands: Sequence[struct_pb2.Value],
    column_dtypes: Mapping[str, pa.DataType],
) -> RowFilter:
    exprs = [_parse_jsonlogic(op, column_dtypes) for op in operands]

    if len(exprs) <= 1:
        raise _Error(
            "invalid compound operation, not enough sub operations",
            op=op,
            num_sub_ops=len(exprs),
        )
    compound_op = exprs[0]
    for sub_op in exprs[1:]:
        match op:
            case "and":
                compound_op = compound_op.and_(sub_op)
            case "or":
                compound_op = compound_op.or_(sub_op)
    return compound_op


def _parse_jsonlogic(
    value: struct_pb2.Value, column_dtypes: Mapping[str, pa.DataType]
) -> RowFilter:
    match value.WhichOneof("kind"):
        case "struct_value":
            if len(value.struct_value.fields) != 1:
                raise _Error("expecting operation as key")

            op, field = more_itertools.one(value.struct_value.fields.items())

            if not field.HasField("list_value"):
                raise _Error("expecting list of operands")
            operands = field.list_value.values  # noqa: PD011
        case None:
            raise _Error("cannot parse value")
        case _:
            raise _Error("unexpected operation type")

    match op:
        case "and" | "or":
            return _compound_compare(op, operands, column_dtypes)
        case "==" | "!=" | "<=" | ">=" | "<" | ">" as op:
            return _simple_compare(op, operands, column_dtypes)
        case _:
            raise _Error("unsupported row filter operation", op=op)


def parse_jsonlogic(
    expression_str: str, column_dtypes: Mapping[str, pa.DataType]
) -> Ok[RowFilter] | InvalidArgumentError:
    """Parses an expression in JsonLogic into a RowFilter.

    This function only supports the following portion of JsonLogic:

    - binary expressions only with the operators, ==, !=, >, >=, <, <= and only in the
      following form: {"<op">: [{"var": "..."}, "<literal>"].

      That is, var references are required and must be the first operand, and literals
      are required and must be the second operand.

    - n-ary operators only with the operators "and", "or" and only in the following
      form: {"<op>": [<expression>, <expression>, ...]}

    Note as a consequence of the above, "and" and "or" can only take binary expressions
    as operands.

    More information on the JsonLogic format can be found at https://jsonlogic.com

    Args:
      expression_str: Expression string to parse
      column_dtypes: Expected types of columns

    Returns:
      InvalidArgumentError: if the expression could not be parsed or is not supported
    """
    try:
        value = json_format.Parse(expression_str, struct_pb2.Value())
    except json_format.ParseError as exc:
        return InvalidArgumentError.from_(exc)
    try:
        row_filter = _parse_jsonlogic(value, column_dtypes)
    except _Error as exc:
        return InvalidArgumentError.from_(exc)

    return _validate(row_filter).or_else(lambda err: InvalidArgumentError.from_(err))
