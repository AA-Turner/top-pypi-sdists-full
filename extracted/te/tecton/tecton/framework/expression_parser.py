import re
from typing import Dict
from typing import List
from typing import Union

from tecton._internals.errors import ExpressionParsingError
from tecton.types import SdkDataType
from tecton.vendor.sql_expresssion_parser import Lark_StandAlone
from tecton.vendor.sql_expresssion_parser import LexError
from tecton.vendor.sql_expresssion_parser import ParseError
from tecton.vendor.sql_expresssion_parser import Token
from tecton.vendor.sql_expresssion_parser import Transformer
from tecton.vendor.sql_expresssion_parser import VisitError
from tecton_core.data_types import BoolType
from tecton_core.data_types import Float32Type
from tecton_core.data_types import Float64Type
from tecton_core.data_types import Int32Type
from tecton_core.data_types import Int64Type
from tecton_core.data_types import StringType
from tecton_core.data_types import data_type_from_proto
from tecton_core.errors import TectonInternalError
from tecton_core.errors import TectonValidationError
from tecton_proto.common.calculation_node__client_pb2 import AbstractSyntaxTreeNode
from tecton_proto.common.calculation_node__client_pb2 import CaseStatement
from tecton_proto.common.calculation_node__client_pb2 import DatePart
from tecton_proto.common.calculation_node__client_pb2 import ElseClause
from tecton_proto.common.calculation_node__client_pb2 import LiteralValue
from tecton_proto.common.calculation_node__client_pb2 import Operation
from tecton_proto.common.calculation_node__client_pb2 import OperationType
from tecton_proto.common.calculation_node__client_pb2 import WhenClause
from tecton_proto.common.data_type__client_pb2 import DataType
from tecton_proto.common.data_type__client_pb2 import DataType as proto_DataType
from tecton_proto.common.data_type__client_pb2 import DataTypeEnum


# Matches numericDatatypesPrecisionOrder in go/internal/featureservice/featureengines/calculations/arithmetic.go
# Matches DuckDB precision hierarchy:
# See https://duckdb.org/docs/sql/data_types/numeric.html
# Float64 = DOUBLE
# Float32 = FLOAT
# Int32 = INTEGER
# Int64 = BIGINT
# Float64 + Float32 -> `SELECT 8::DOUBLE + 8::FLOAT;` returns DOUBLE, so Float64 is more precise than Float32
# Float32 + Int64 -> `select 8::FLOAT + 8::BIGINT;` returns FLOAT so Float32 is more precise than Int64
# Int64 + Int32 -> `select 8::BIGINT + 8::INTEGER;` returns BIGINT so Int64 is more precise than Int32
NUMERIC_DATATYPES_PRECISION_ORDER = [Float64Type().proto, Float32Type().proto, Int64Type().proto, Int32Type().proto]


class _ToAbstractSyntaxTree(Transformer):
    def __init__(self, original_expression: str, schema: Dict[str, SdkDataType], calculation_name: str):
        self.original_expression = original_expression
        self.schema = schema
        self.calculation_name = calculation_name
        super().__init__()

    def _type_is_numeric(self, input_dtype: proto_DataType) -> bool:
        return input_dtype in [Int64Type().proto, Int32Type().proto, Float64Type().proto, Float32Type().proto]

    def _type_is_boolean(self, input_dtype: proto_DataType):
        return input_dtype == BoolType().proto

    def _resolve_dtypes(self, input_dtypes: List[proto_DataType], operation: str) -> proto_DataType:
        if len(input_dtypes) == 0:
            return None
        all_numeric = all(self._type_is_numeric(input_dtype) for input_dtype in input_dtypes)
        if all_numeric:
            # check for presence of each numeric dtype in order, and return first one found
            for dtype in NUMERIC_DATATYPES_PRECISION_ORDER:
                if dtype in input_dtypes:
                    return dtype

        first_type = input_dtypes[0]
        for dtype in input_dtypes:
            if first_type != dtype:
                msg = f"Cannot combine datatypes {data_type_from_proto(first_type)} and {data_type_from_proto(dtype)} in operation {operation}"
                raise ExpressionParsingError(msg, self.calculation_name)
        # All dtypes are equal
        return first_type

    def _types_are_comparable(self, nodes: List[AbstractSyntaxTreeNode]) -> bool:
        if not nodes:
            # let's assume empty lists are comparable
            return True
        elif all(self._type_is_numeric(node.dtype) for node in nodes):
            # All numeric types are comparable (might change this later)
            return True
        elif any(node.dtype.type == DataTypeEnum.DATA_TYPE_STRUCT for node in nodes):
            # structs are not comparable
            return False
        else:
            # if all types are the same
            first_node_type = nodes[0].dtype
            return all(node.dtype == first_node_type for node in nodes)

    def literal(self, value) -> AbstractSyntaxTreeNode:
        value = value[0]
        if isinstance(value, bool):
            literal_value = LiteralValue(bool_value=value)
            dtype = BoolType()
        elif isinstance(value, int):
            literal_value = LiteralValue(int64_value=value)
            dtype = Int64Type()
        elif isinstance(value, float):
            literal_value = LiteralValue(float64_value=value)
            dtype = Float64Type()
        elif isinstance(value, str):
            literal_value = LiteralValue(string_value=value)
            dtype = StringType()
        else:
            msg = f"Something went wrong while parsing: Unexpected Literal type {type(value)}, node: {value}"
            raise RuntimeError(msg)
        return AbstractSyntaxTreeNode(literal_value=literal_value, dtype=dtype.proto)

    def numeric_negative(self, child: List[Token]):
        return -1 * child[0]

    def INT(self, value: str):
        return int(value)

    def DECIMAL(self, value: str):
        return float(value)

    def FLOAT(self, value: str):
        return float(value)

    def ESCAPED_STRING(self, value: str):
        value = value[1:-1]  # strip parentheses
        return value

    def SINGLE_QUOTED_STRING(self, value: str):
        value = value[1:-1]
        return value

    def true(self, value: str):
        return True

    def false(self, value: str):
        return False

    def day(self, value: str):
        return AbstractSyntaxTreeNode(date_part=DatePart.DAY)

    def month(self, value: str):
        return AbstractSyntaxTreeNode(date_part=DatePart.MONTH)

    def week(self, value: str):
        return AbstractSyntaxTreeNode(date_part=DatePart.WEEK)

    def year(self, value: str):
        return AbstractSyntaxTreeNode(date_part=DatePart.YEAR)

    def second(self, value: str):
        return AbstractSyntaxTreeNode(date_part=DatePart.SECOND)

    def hour(self, value: str):
        return AbstractSyntaxTreeNode(date_part=DatePart.HOUR)

    def minute(self, value: str):
        return AbstractSyntaxTreeNode(date_part=DatePart.MINUTE)

    def millennium(self, value: str):
        return AbstractSyntaxTreeNode(date_part=DatePart.MILLENNIUM)

    def century(self, value: str):
        return AbstractSyntaxTreeNode(date_part=DatePart.CENTURY)

    def decade(self, value: str):
        return AbstractSyntaxTreeNode(date_part=DatePart.DECADE)

    def quarter(self, value: str):
        return AbstractSyntaxTreeNode(date_part=DatePart.QUARTER)

    def milliseconds(self, value: str):
        return AbstractSyntaxTreeNode(date_part=DatePart.MILLISECONDS)

    def microseconds(self, value: str):
        return AbstractSyntaxTreeNode(date_part=DatePart.MICROSECONDS)

    def COLUMN_REFERENCE(self, value: str):
        # handle case where column reference is wrapped in "
        if value.startswith('"'):
            value = value[1:-1]

        if value not in self.schema:
            msg = f"Invalid column reference: {value}, possible values: {list(self.schema.keys())}"
            raise ExpressionParsingError(msg, self.calculation_name)
        dtype = self.schema[value]
        return AbstractSyntaxTreeNode(column_reference=value, dtype=dtype.tecton_type.proto)

    def coalesce(self, values) -> AbstractSyntaxTreeNode:
        if not values:
            # This shouldn't be possible because the regex pattern for this rule requires at least 1 argument,
            # but adding as extra protection in case the rule changes in the future.
            msg = f"Error parsing expression for Calculation {self.calculation_name}: At least one value required for COALESCE, {self.original_expression}"
            raise ExpressionParsingError(msg, self.calculation_name)

        dtypes = {data_type_from_proto(value.dtype) for value in values}
        if len(dtypes) != 1:
            msg = f"Cannot mix values of types {dtypes} in COALESCE operator."
            raise ExpressionParsingError(msg, self.calculation_name)

        return AbstractSyntaxTreeNode(
            operation=Operation(operation=OperationType.COALESCE, operands=values), dtype=values[0].dtype
        )

    def datediff(self, values) -> AbstractSyntaxTreeNode:
        if not values or len(values) != 3:
            msg = f"Error parsing expression: Exactly three values required for DATEDIFF, {self.original_expression}"
            raise ExpressionParsingError(msg, self.calculation_name)

        date_part = values[0]
        start_date = values[1]
        end_date = values[2]
        if (
            start_date.dtype.type != DataTypeEnum.DATA_TYPE_TIMESTAMP
            or end_date.dtype.type != DataTypeEnum.DATA_TYPE_TIMESTAMP
        ):
            msg = "For DATEDIFF, both start_date and end_date must have type TIMESTAMP."
            raise ExpressionParsingError(msg, self.calculation_name)

        operands = [date_part, start_date, end_date]
        return AbstractSyntaxTreeNode(
            operation=Operation(operation=OperationType.DATE_DIFF, operands=operands), dtype=Int64Type().proto
        )

    def _comparison(self, values: List[AbstractSyntaxTreeNode], operation) -> AbstractSyntaxTreeNode:
        if len(values) != 2:
            # Shouldn't be possible due to regex patterns, so this is an internal error
            msg = f"Comparisons should have exactly 2 operands, found {len(values)}"
            raise TectonInternalError(msg)
        if not self._types_are_comparable(values):
            left_type = data_type_from_proto(values[0].dtype)
            right_type = data_type_from_proto(values[1].dtype)
            msg = f"Types {left_type} and {right_type} are not comparable"
            raise ExpressionParsingError(msg, self.calculation_name)
        return AbstractSyntaxTreeNode(operation=Operation(operation=operation, operands=values), dtype=BoolType().proto)

    def equals(self, values) -> AbstractSyntaxTreeNode:
        return self._comparison(values, OperationType.EQUALS)

    def not_equals(self, values) -> AbstractSyntaxTreeNode:
        return self._comparison(values, OperationType.NOT_EQUALS)

    def greater_than(self, values) -> AbstractSyntaxTreeNode:
        return self._comparison(values, OperationType.GREATER_THAN)

    def greater_than_or_equals(self, values) -> AbstractSyntaxTreeNode:
        return self._comparison(values, OperationType.GREATER_THAN_EQUALS)

    def less_than(self, values) -> AbstractSyntaxTreeNode:
        return self._comparison(values, OperationType.LESS_THAN)

    def less_than_or_equals(self, values) -> AbstractSyntaxTreeNode:
        return self._comparison(values, OperationType.LESS_THAN_EQUALS)

    def _determine_math_dtype(self, values: List[AbstractSyntaxTreeNode], operation: OperationType) -> DataType:
        for value in values:
            if not self._type_is_numeric(value.dtype):
                msg = f"Cannot perform {OperationType.Name(operation)} on non-numeric type {data_type_from_proto(value.dtype)}"
                raise ExpressionParsingError(msg, self.calculation_name)

        if operation == OperationType.DIVISION:
            return Float64Type().proto

        value_dtypes = [value.dtype for value in values]
        return self._resolve_dtypes(value_dtypes, OperationType.Name(operation))

    def _math_operation(self, values, operation):
        dtype_proto = self._determine_math_dtype(values, operation)
        return AbstractSyntaxTreeNode(operation=Operation(operation=operation, operands=values), dtype=dtype_proto)

    def addition(self, values) -> AbstractSyntaxTreeNode:
        return self._math_operation(values, OperationType.ADDITION)

    def subtraction(self, values) -> AbstractSyntaxTreeNode:
        return self._math_operation(values, OperationType.SUBTRACTION)

    def multiplication(self, values) -> AbstractSyntaxTreeNode:
        return self._math_operation(values, OperationType.MULTIPLICATION)

    def division(self, values) -> AbstractSyntaxTreeNode:
        return self._math_operation(values, OperationType.DIVISION)

    def negation(self, value):
        neg_1 = AbstractSyntaxTreeNode(literal_value=LiteralValue(int64_value=-1), dtype=Int32Type().proto)
        return self.multiplication([neg_1, value[0]])

    def searched_case_statement(self, clauses: Union[WhenClause, ElseClause]):
        if not clauses or not isinstance(clauses[0], WhenClause):
            msg = "Case statements require at least 1 WHEN clause."
            raise ExpressionParsingError(msg, self.calculation_name)
        statement_dtype_proto = self._resolve_dtypes([clause.result.dtype for clause in clauses], "CASE statement")

        if isinstance(clauses[-1], ElseClause):
            else_clause = clauses.pop()
        else:
            else_clause = None
        when_clauses = clauses
        for when_clause in when_clauses:
            condition_dtype = data_type_from_proto(when_clause.condition.dtype)
            # Only these types are acceptable types in a when-statement conditional
            if not isinstance(condition_dtype, (Int64Type, Int32Type, BoolType, Float64Type, Float32Type)):
                msg = f"Could not convert CASE STATEMENT predicate type {condition_dtype} to BOOL."
                raise ExpressionParsingError(msg, self.calculation_name)

        return AbstractSyntaxTreeNode(
            case_statement=CaseStatement(when_clauses=when_clauses, else_clause=else_clause),
            dtype=statement_dtype_proto,
        )

    def when_clause(self, values):
        return WhenClause(condition=values[0], result=values[1])

    def else_clause(self, value):
        return ElseClause(result=value[0])

    def logical_not(self, values) -> AbstractSyntaxTreeNode:
        return self._logical_operator(values, OperationType.NOT)

    def logical_and(self, values) -> AbstractSyntaxTreeNode:
        return self._logical_operator(values, OperationType.AND)

    def logical_or(self, values) -> AbstractSyntaxTreeNode:
        return self._logical_operator(values, OperationType.OR)

    def _logical_operator(
        self, values: List[AbstractSyntaxTreeNode], operation_type: OperationType
    ) -> AbstractSyntaxTreeNode:
        for value in values:
            if not (self._type_is_boolean(value.dtype) or self._type_is_numeric(value.dtype)):
                msg = f"{OperationType.Name(operation_type)} operator was evaluated with value of type {data_type_from_proto(value.dtype)} which could not be converted to bool."
                raise ExpressionParsingError(msg, self.calculation_name)
        return AbstractSyntaxTreeNode(
            operation=Operation(operation=operation_type, operands=values), dtype=BoolType().proto
        )


class CustomParseError(ParseError):
    def __init__(self, matching_regexes: []):
        super().__init__()
        self._regexes = matching_regexes

    @property
    def matching_regexes(self):
        return self._regexes

    @property
    def error_message(self):
        raise NotImplementedError


class DateDiffParseError(CustomParseError):
    def __init__(self):
        super().__init__(matching_regexes=[r"datediff\s*\(\s*\""])

    @property
    def error_message(self):
        return "The date part argument to DATEDIFF requires single quotes (') not double quotes (\"). For example, instead of datediff(\"day\",...), use datediff('day',...)."


CUSTOM_PARSE_ERRORS = [DateDiffParseError()]


def expression_to_proto(
    expression: str, schema: Dict[str, SdkDataType], calculation_name: str
) -> AbstractSyntaxTreeNode:
    # TODO: This class initialization should be top-level for better performance, but for not that causes
    #  issues with type-hint checking. We should fix that.
    lexer = Lark_StandAlone()
    try:
        lark_syntax_tree = lexer.parse(expression)
    except (LexError, ParseError) as e:
        for custom_parse_error in CUSTOM_PARSE_ERRORS:
            if any(re.search(matching_regex, expression) for matching_regex in custom_parse_error.matching_regexes):
                msg = custom_parse_error.error_message
                raise ExpressionParsingError(msg, calculation_name) from e
        msg = f"{expression}"
        raise ExpressionParsingError(msg, calculation_name) from e
    try:
        ast = _ToAbstractSyntaxTree(expression, schema, calculation_name).transform(lark_syntax_tree)
    except VisitError as e:
        if isinstance(e.orig_exc, TectonValidationError):
            raise e.orig_exc from None  # Re-raise the original TectonValidationError without chaining
        else:
            # This indicates an issue with our parsing logic, not a user error.
            msg = f"Error converting parse tree to AST for Calculation {calculation_name}: {lark_syntax_tree}"
            raise TectonInternalError(msg) from e
    return ast
