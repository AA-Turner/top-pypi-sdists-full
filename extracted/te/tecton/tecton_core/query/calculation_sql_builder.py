from abc import ABC
from abc import abstractmethod
from typing import Dict
from typing import Set
from typing import Tuple

import attrs
import pypika.functions as fn
from pypika import NULL
from pypika.enums import Arithmetic
from pypika.enums import Equality
from pypika.terms import ArithmeticExpression
from pypika.terms import BasicCriterion
from pypika.terms import Case
from pypika.terms import LiteralValue
from pypika.terms import Not
from pypika.terms import Term
from pypika.terms import ValueWrapper

from tecton_core import data_types
from tecton_core.compute_mode import ComputeMode
from tecton_core.errors import TectonInternalError
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.query.column_reference_resolver import ColumnReferenceResolver
from tecton_core.specs.calculation_node_spec import AbstractSyntaxTreeNodeSpec
from tecton_core.specs.calculation_node_spec import CaseStatementNodeSpec
from tecton_core.specs.calculation_node_spec import ColumnReferenceNodeSpec
from tecton_core.specs.calculation_node_spec import LiteralValueNodeSpec
from tecton_core.specs.calculation_node_spec import OperationNodeSpec
from tecton_proto.common import calculation_node__client_pb2 as calculation_node_pb2
from tecton_proto.common.calculation_node__client_pb2 import OperationType


COMPARISON_OPERATION_TYPE_TO_PYPIKA_EQUALITY: Dict[calculation_node_pb2.OperationType.ValueType, Equality] = {
    calculation_node_pb2.OperationType.EQUALS: Equality.eq,
    calculation_node_pb2.OperationType.NOT_EQUALS: Equality.ne,
    calculation_node_pb2.OperationType.GREATER_THAN: Equality.gt,
    calculation_node_pb2.OperationType.GREATER_THAN_EQUALS: Equality.gte,
    calculation_node_pb2.OperationType.LESS_THAN: Equality.lt,
    calculation_node_pb2.OperationType.LESS_THAN_EQUALS: Equality.lte,
}

DATE_PART_TO_INTERVAL_STRING: Dict[calculation_node_pb2.DatePart.ValueType, str] = {
    calculation_node_pb2.DatePart.DAY: "day",
    calculation_node_pb2.DatePart.MONTH: "month",
    calculation_node_pb2.DatePart.WEEK: "week",
    calculation_node_pb2.DatePart.YEAR: "year",
    calculation_node_pb2.DatePart.SECOND: "second",
    calculation_node_pb2.DatePart.HOUR: "hour",
    calculation_node_pb2.DatePart.MINUTE: "minute",
    calculation_node_pb2.DatePart.MILLENNIUM: "millennium",
    calculation_node_pb2.DatePart.CENTURY: "century",
    calculation_node_pb2.DatePart.DECADE: "decade",
    calculation_node_pb2.DatePart.QUARTER: "quarter",
    calculation_node_pb2.DatePart.MILLISECONDS: "milliseconds",
    calculation_node_pb2.DatePart.MICROSECONDS: "microseconds",
}

ARITHMETIC_OPERATION_TYPE_TO_PYPIKA_ARITHMETIC: Dict[calculation_node_pb2.OperationType.ValueType, Arithmetic] = {
    calculation_node_pb2.OperationType.ADDITION: Arithmetic.add,
    calculation_node_pb2.OperationType.SUBTRACTION: Arithmetic.sub,
    calculation_node_pb2.OperationType.MULTIPLICATION: Arithmetic.mul,
    calculation_node_pb2.OperationType.DIVISION: Arithmetic.div,
}

LOGICAL_OPERATOR_OPERATIONS: Set[calculation_node_pb2.OperationType.ValueType] = {
    calculation_node_pb2.OperationType.NOT,
    calculation_node_pb2.OperationType.AND,
    calculation_node_pb2.OperationType.OR,
}

DUCKDB_TRY_STRPTIME_DIRECTIVES_TO_SPARK = {
    "a": None,  # Weekday as abbreviated name (Sun, Mon, etc)
    "A": None,  # Weekday as full name (Sunday, Monday, etc)
    "b": None,  # Month as abbreviated name (Jan, Feb, etc)
    "B": None,  # Month as full name (January, February, etc)
    "c": None,  # ISO date and time representation (1992-03-02 10:30:20)
    # %d in duckdb does not restrict the day to zero padded; it accepts 1 to 2 digit valid day numbers with single digit days allowed to have 1 digit zero-padding.
    # We use d in spark, which behaves the same except it allows for unlimited zero-padding.
    "d": "d",  # Day of month as zero-padded decimal number (01-31)
    # %f in duckdb interprets the digits as count of microseconds. e.g 12.1 is not twelve and one tenth of a second, but twelve seconds and one microsecond.
    # To match this behavior as close as possible, we use SSSSSS in spark, where each S is a fractional second digit (while spark can parse upto nanosecond specified strings, it only supports microsecond precision).
    # Note: in contrast to duckdb's microsecond interpretation, spark interprets 12.1 as twelve and one tenth of a second.
    # Note: to achieve the most consistent cross-platform interpretation of fractional seconds, the timestamp strings should have a digit for every position in the franctional second portion (i.e. use trailing zeroes).
    "f": "SSSSSS",  # Microsecond as decimal number, zero-padded (000000-999999)
    "g": None,  # Millisecond as a decimal number, zero-padded (000-999), note: not supported in python
    "G": None,  # ISO 8601 year with century representing the year that contains the greater part of the ISO week (see %V) (0001, 0002, ..., 9999)
    # %H in duckdb does not restrict the hour to zero padded; it accepts 1 to 2 digit valid hour numbers with single digit hours allowed to have 1 digit zero-padding.
    # We use H in spark, which behaves the same except it allows for unlimited zero-padding.
    "H": "H",  # Hour (24-hour clock) as zero-padded decimal number (00-23)
    "I": None,  # Hour (12-hour clock) as zero-padded decimal number (01-12)
    "j": None,  # Day of year as zero-padded decimal number (001-366)
    # %m in duckdb does not restrict the month to zero padded; it accepts any valid month number 1-12 with single digit months allowed to have 1 digit zero-padding.
    # We use M in spark, which behaves the same except it allows for unlimited zero-padding.
    "m": "M",  # Month as zero-padded decimal number (01-12)
    # %M in duckdb does not restrict the minute to zero padded; it accepts any valid minute number 0-59 with single digit minutes allowed to have 1 digit zero-padding.
    # We use m in spark, which behaves the same except it allows for unlimited zero-padding.
    "M": "m",  # Minute as zero-padded decimal number (00-59)
    "n": None,  # nanosecond as a decimal number, zero-padded (000000000-999999999), note: not supported in python
    "p": None,  # Locale's AM/PM indicator (AM/PM)
    # %S in duckdb does not restrict the second to zero padded; it accepts any valid second number 0-59 with single digit seconds allowed to have 1 digit zero-padding.
    # We use s in spark, which behaves the same except it allows for unlimited zero-padding.
    "S": "s",  # Second as zero-padded decimal number (00-59)
    "u": None,  # ISO 8601 weekday as decimal number (1-7, 1=Monday)
    "U": None,  # Week number of year, week 01 starts on first Sunday of year (00-53, Sunday first day), not ISO 8601 compliant
    "V": None,  # ISO 8601 week number, monday is first day of week and week 01 is the week containing January 4 (01-53), not compatible with %Y (use %G instead)
    "w": None,  # Weekday as decimal number (0-6, 0=Sunday)
    "W": None,  # Week number of year, week 01 starts on the first Monday of the year (00-53), not ISO 8601 compliant
    "x": None,  # ISO date representation (1992-03-02)
    "X": None,  # ISO time representation (10:30:20)
    "y": None,  # Year without century, zero-padded (00-99)
    # %Y in duckdb does not restrict the year to zero padded; it accepts 1 to 4 digits.
    # We use y in spark, which is flexible to number of digits, though it does accept 1 to more than 4.
    "Y": "y",  # Year with century as a decimal number (2013, 2019, etc)
    # %z in duckdb allows for 2 or 4 digit offsets, with or without a colon, with a leading + or - e.g. +00, -00, +0000, -0000, +00:00, -00:00. The supported value range is from -9999 to 9999.
    # Spark has no such flexible equivalent, so we combine multiple formats specifiers using [] options: [XXX][X]
    # XXX accepts 4 or 6 digit offsets with colon separators, with a leading + or -. This does mean that spark will accept seconds offsets, which duckdb does not.
    # X accepts 2 or 4 digit offsets without colon separators, with a leading + or -. It also accepts 'Z' to indicate UTC, which duckdb does not.
    # [XXX][X] means we check for matches to the XXX pattern (colon separated), and if that fails, we check for matches to the X pattern (no colon). Combined, this is a superset of the supported duckdb behaviors.
    # Note: [XXX][X] means the timezone offset is optional in spark, which is different than duckdb where the timezone offset is required.
    # TODO: Explore using a regex check to first confirm the offset is present.
    # Note: Spark only supports certain value ranges for each offset component of hours, minutes, and seconds, with a max total offset of +-18 hours.
    #   Hours: [-18, +18]
    #   Minutes: [-59, +59]
    #   Seconds: [-59, +59]
    "z": "[XXX][X]",  # UTC offset in form +HHMM or -HHMM
    "Z": None,  # Time zone name
    "%": None,  # Literal % character
}

ISO_8601_FORMAT_DUCKDB = "%Y-%m-%dT%H:%M:%S.%f%z"
ISO_8601_FORMAT_SPARK = "y-M-d'T'H:m:s.SSSSSS[XXX][X]"


def _get_cast_string_for_numeric_dtype(dtype: data_types.DataType) -> str:
    if isinstance(dtype, data_types.Int32Type):
        return "INTEGER"
    elif isinstance(dtype, data_types.Int64Type):
        return "BIGINT"
    elif isinstance(dtype, data_types.Float32Type):
        return "FLOAT"
    elif isinstance(dtype, data_types.Float64Type):
        return "DOUBLE"
    else:
        msg = f"Data type {dtype} not supported for cast."
        raise TectonInternalError(msg)


@attrs.define
class CalculationSqlBuilder(ABC):
    fdw: FeatureDefinitionWrapper
    column_reference_resolver: ColumnReferenceResolver

    def _operation_node_to_query_term(self, operation_node: OperationNodeSpec) -> Term:
        if operation_node.operation == calculation_node_pb2.OperationType.COALESCE:
            return self._build_coalesce_query(operation_node)
        elif operation_node.operation in COMPARISON_OPERATION_TYPE_TO_PYPIKA_EQUALITY:
            return self._build_comparison_query(operation_node)
        elif operation_node.operation == calculation_node_pb2.OperationType.DATE_DIFF:
            return self._build_date_diff_query(operation_node)
        elif operation_node.operation in ARITHMETIC_OPERATION_TYPE_TO_PYPIKA_ARITHMETIC:
            return self._build_arithmetic_query(operation_node)
        elif operation_node.operation in LOGICAL_OPERATOR_OPERATIONS:
            return self._build_logical_operator_query(operation_node)
        elif operation_node.operation == calculation_node_pb2.OperationType.TRY_STRPTIME:
            return self._build_try_strptime_query(operation_node)
        else:
            msg = f"In Calculation sql generation, calculation operation {OperationType.Name(operation_node.operation)} not supported."
            raise TectonInternalError(msg)

    def _extract_try_strptime_operands(self, operation_node: OperationNodeSpec) -> Tuple[Term, Term]:
        if len(operation_node.operands) != 2:
            msg = "Calculation function try_strptime must have exactly 2 operands."
            raise TectonInternalError(msg)
        timestamp_string_sql = self.ast_node_to_query_term(operation_node.operands[0])
        format_string = self.ast_node_to_query_term(operation_node.operands[1])
        return timestamp_string_sql, format_string

    @abstractmethod
    def _build_try_strptime_query(self, operation_node: OperationNodeSpec) -> Term:
        raise NotImplementedError

    def _build_logical_operator_query(self, operation_node: OperationNodeSpec) -> Term:
        if operation_node.operation == calculation_node_pb2.OperationType.NOT:
            return self._build_logical_not_query(operation_node)
        elif operation_node.operation == calculation_node_pb2.OperationType.AND:
            return self._build_logical_and_query(operation_node)
        elif operation_node.operation == calculation_node_pb2.OperationType.OR:
            return self._build_logical_or_query(operation_node)
        else:
            msg = "Unhandled logical operator."
            raise TectonInternalError(msg)

    def _build_logical_not_query(self, operation_node: OperationNodeSpec) -> Term:
        if len(operation_node.operands) != 1:
            msg = "Calculation NOT operator must have exactly 1 operand."
            raise TectonInternalError(msg)

        operand_sql = fn.Cast(self.ast_node_to_query_term(operation_node.operands[0]), "BOOLEAN")
        return Not(operand_sql)

    def _build_logical_and_query(self, operation_node: OperationNodeSpec) -> Term:
        if len(operation_node.operands) != 2:
            msg = "Calculation AND operator must have exactly 2 operands."
            raise TectonInternalError(msg)

        operand_sqls = [fn.Cast(self.ast_node_to_query_term(operand), "BOOLEAN") for operand in operation_node.operands]
        return LiteralValue(f"{operand_sqls[0]} AND {operand_sqls[1]}")

    def _build_logical_or_query(self, operation_node: OperationNodeSpec) -> Term:
        if len(operation_node.operands) != 2:
            msg = "Calculation OR operator must have exactly 2 operands."
            raise TectonInternalError(msg)

        operand_sqls = [fn.Cast(self.ast_node_to_query_term(operand), "BOOLEAN") for operand in operation_node.operands]
        return LiteralValue(f"{operand_sqls[0]} OR {operand_sqls[1]}")

    def _build_coalesce_query(self, operation_node: OperationNodeSpec) -> Term:
        if len(operation_node.operands) < 1:
            msg = "Calculation function Coalesce must have at least 1 operand."
            raise TectonInternalError(msg)
        operand_sqls = [self.ast_node_to_query_term(operand) for operand in operation_node.operands]
        return fn.Coalesce(*operand_sqls)

    def _build_arithmetic_query(self, operation_node: OperationNodeSpec) -> Term:
        if len(operation_node.operands) != 2:
            msg = "Arithmetic function must have exactly 2 operands."
            raise TectonInternalError(msg)
        left = self.ast_node_to_query_term(operation_node.operands[0])
        right = self.ast_node_to_query_term(operation_node.operands[1])

        arithmetic_term = ARITHMETIC_OPERATION_TYPE_TO_PYPIKA_ARITHMETIC[operation_node.operation]
        base_expression = ArithmeticExpression(arithmetic_term, left, right)
        if operation_node.operation == calculation_node_pb2.OperationType.DIVISION:
            # this cast is necessary because:
            # in duckdb, x/0 returns inf, -x/0 returns -inf as of 1.1.0 (https://duckdb.org/2024/09/09/announcing-duckdb-110.html)
            # in spark, x/0 returns null.
            # we want to match duckdb behavior, so return inf if dividing by 0.
            positive_inf_literal = LiteralValue("CAST('inf' AS DOUBLE)")
            negative__inf_literal = LiteralValue("CAST('-inf' AS DOUBLE)")
            nan_literal = LiteralValue("CAST('nan' AS DOUBLE)")

            base_expression = (
                Case()
                .when((left == 0) & (right == 0), nan_literal)  # 0/0, return NaN
                .when((left < 0) & (right == 0), negative__inf_literal)  # -x/0, return -inf
                .when((left > 0) & (right == 0), positive_inf_literal)  # +x/0, return inf
                .else_(base_expression)  # Default case, use base_expression
            )

        cast_type = _get_cast_string_for_numeric_dtype(dtype=operation_node.dtype)
        return fn.Cast(base_expression, cast_type)

    def _build_comparison_query(self, operation_node: OperationNodeSpec) -> Term:
        if len(operation_node.operands) != 2:
            msg = "Calculation function must have exactly 2 operands."
            raise TectonInternalError(msg)
        left = self.ast_node_to_query_term(operation_node.operands[0])
        right = self.ast_node_to_query_term(operation_node.operands[1])

        comparator_term = COMPARISON_OPERATION_TYPE_TO_PYPIKA_EQUALITY[operation_node.operation]
        return BasicCriterion(comparator_term, left, right)

    @abstractmethod
    def _build_date_diff_query(self, operation_node: OperationNodeSpec) -> Term:
        raise NotImplementedError

    @staticmethod
    def _literal_value_node_to_query_term(literal_value_node: LiteralValueNodeSpec) -> Term:
        if literal_value_node.dtype is None or literal_value_node.value is None:
            return NULL
        sql = ValueWrapper(literal_value_node.value)
        if isinstance(literal_value_node.dtype, data_types.Int64Type):
            sql = fn.Cast(sql, _get_cast_string_for_numeric_dtype(dtype=literal_value_node.dtype))
        elif isinstance(literal_value_node.dtype, data_types.Float64Type):
            sql = fn.Cast(sql, _get_cast_string_for_numeric_dtype(dtype=literal_value_node.dtype))
        return sql

    def _column_reference_node_to_query_term(self, column_reference_node: ColumnReferenceNodeSpec) -> Term:
        internal_column_name = self.column_reference_resolver.get_internal_column_name(
            column_reference_node.value, self.fdw
        )
        # originally we used pypika.Field here since column references are fields in the table being queried
        # however, Field adds quotes to the column name when get_sql() is called under some conditions
        # we switched to LiteralValue because it will always reliably return the bare string, which works for our use case
        return LiteralValue(internal_column_name)

    def _case_statement_node_to_query_term(self, case_statement_node: CaseStatementNodeSpec) -> Term:
        base_expression = Case()
        for when_clause in case_statement_node.when_clauses:
            condition = fn.Cast(self.ast_node_to_query_term(when_clause.condition), "BOOLEAN")
            result = self.ast_node_to_query_term(when_clause.result)
            base_expression = base_expression.when(condition, result)
        if case_statement_node.else_clause is not None:
            result = self.ast_node_to_query_term(case_statement_node.else_clause.result)
            base_expression = base_expression.else_(result)
        return base_expression

    def ast_node_to_query_term(self, ast_node: AbstractSyntaxTreeNodeSpec) -> Term:
        if isinstance(ast_node, OperationNodeSpec):
            return self._operation_node_to_query_term(ast_node)
        elif isinstance(ast_node, LiteralValueNodeSpec):
            return self._literal_value_node_to_query_term(ast_node)
        elif isinstance(ast_node, ColumnReferenceNodeSpec):
            return self._column_reference_node_to_query_term(ast_node)
        elif isinstance(ast_node, CaseStatementNodeSpec):
            return self._case_statement_node_to_query_term(ast_node)
        else:
            msg = f"AST node type {ast_node.__class__.__name__} not recognized. Cannot extract calculation."
            raise TectonInternalError(msg)


@attrs.define
class DuckDBCalculationSqlBuilder(CalculationSqlBuilder):
    def _build_try_strptime_query(self, operation_node: OperationNodeSpec) -> Term:
        timestamp_string_sql, format_string = self._extract_try_strptime_operands(operation_node)
        return LiteralValue(f"TRY_STRPTIME({timestamp_string_sql}, {format_string})")

    def _build_date_diff_query(self, operation_node: OperationNodeSpec) -> Term:
        if len(operation_node.operands) != 3:
            msg = "Calculation function date diff must have exactly 3 operands."
            raise TectonInternalError(msg)
        [date_part_operand, start_date_operand, end_date_operand] = operation_node.operands
        date_part_str = DATE_PART_TO_INTERVAL_STRING[date_part_operand.value]
        start_date_operand = self.ast_node_to_query_term(start_date_operand)
        end_date_operand = self.ast_node_to_query_term(end_date_operand)

        return fn.DateDiff(date_part_str, start_date_operand, end_date_operand)


@attrs.define
class SparkCalculationSqlBuilder(CalculationSqlBuilder):
    @staticmethod
    def _translate_format_string_to_spark(format_string: str) -> str:
        # TODO: escape text in the format
        # TODO: replace duckdb directives e.g. %z with spark equivalents
        # for now, just return the appropriate spark format string
        if format_string == ISO_8601_FORMAT_DUCKDB:
            return ISO_8601_FORMAT_SPARK
        else:
            msg = f"Format string {format_string} not supported."
            raise TectonInternalError(msg)

    def _build_try_strptime_query(self, operation_node: OperationNodeSpec) -> Term:
        timestamp_string_sql, format_string = self._extract_try_strptime_operands(operation_node)
        translated_format_string = SparkCalculationSqlBuilder._translate_format_string_to_spark(format_string)
        return LiteralValue(f'to_timestamp({timestamp_string_sql}, "{translated_format_string}")')

    @staticmethod
    def _get_spark_date_diff_sql_str(
        date_part: calculation_node_pb2.DatePart.ValueType, start_date_sql: str, end_date_sql: str
    ) -> str:
        if date_part == calculation_node_pb2.DatePart.DAY:
            return f"FLOOR(DATEDIFF(DATE_TRUNC('day', {end_date_sql}), DATE_TRUNC('day', {start_date_sql})))"
        elif date_part == calculation_node_pb2.DatePart.MONTH:
            return f"FLOOR(MONTHS_BETWEEN(DATE_TRUNC('month', {end_date_sql}), DATE_TRUNC('month', {start_date_sql})))"
        elif date_part == calculation_node_pb2.DatePart.WEEK:
            return f"FLOOR(DATEDIFF({end_date_sql}, {start_date_sql})/7)"
        elif date_part == calculation_node_pb2.DatePart.YEAR:
            return f"YEAR({end_date_sql}) - YEAR({start_date_sql})"
        elif date_part == calculation_node_pb2.DatePart.SECOND:
            return f"UNIX_TIMESTAMP(DATE_TRUNC('second', {end_date_sql})) - UNIX_TIMESTAMP(DATE_TRUNC('second', {start_date_sql}))"
        elif date_part == calculation_node_pb2.DatePart.HOUR:
            return f"( UNIX_TIMESTAMP(DATE_TRUNC('hour', {end_date_sql})) - UNIX_TIMESTAMP(DATE_TRUNC('hour', {start_date_sql})) ) / 3600"
        elif date_part == calculation_node_pb2.DatePart.MINUTE:
            return f"( UNIX_TIMESTAMP(DATE_TRUNC('minute', {end_date_sql})) - UNIX_TIMESTAMP(DATE_TRUNC('minute', {start_date_sql})) ) / 60"
        elif date_part == calculation_node_pb2.DatePart.MILLENNIUM:
            return f"FLOOR(YEAR({end_date_sql}) / 1000) - FLOOR(YEAR({start_date_sql}) / 1000)"
        elif date_part == calculation_node_pb2.DatePart.CENTURY:
            return f"FLOOR(YEAR({end_date_sql}) / 100) - FLOOR(YEAR({start_date_sql}) / 100)"
        elif date_part == calculation_node_pb2.DatePart.DECADE:
            return f"FLOOR(YEAR({end_date_sql}) / 10) - FLOOR(YEAR({start_date_sql}) / 10)"
        elif date_part == calculation_node_pb2.DatePart.QUARTER:
            return f"4 * (YEAR({end_date_sql}) - YEAR({start_date_sql})) + FLOOR((MONTH({end_date_sql})-1 )/ 3) - FLOOR((MONTH({start_date_sql})-1 )/ 3)"
        elif date_part == calculation_node_pb2.DatePart.MILLISECONDS:
            return f"UNIX_MILLIS({end_date_sql}) - UNIX_MILLIS({start_date_sql})"
        elif date_part == calculation_node_pb2.DatePart.MICROSECONDS:
            return f"UNIX_MICROS({end_date_sql}) - UNIX_MICROS({start_date_sql})"
        else:
            msg = f"Date part {date_part} is not supported."
            raise TectonInternalError(msg)

    def _build_date_diff_query(self, operation_node: OperationNodeSpec) -> Term:
        if len(operation_node.operands) != 3:
            msg = "Calculation function date diff must have exactly 3 operands."
            raise TectonInternalError(msg)

        [date_part_operand, start_date_operand, end_date_operand] = operation_node.operands
        start_date_sql = self.ast_node_to_query_term(start_date_operand)
        end_date_sql = self.ast_node_to_query_term(end_date_operand)

        date_value = date_part_operand.value
        spark_sql = SparkCalculationSqlBuilder._get_spark_date_diff_sql_str(date_value, start_date_sql, end_date_sql)
        return LiteralValue(spark_sql)


class CalculationSqlBuilderFactory:
    @classmethod
    def create_builder(
        cls,
        fdw: FeatureDefinitionWrapper,
        column_reference_resolver: ColumnReferenceResolver,
        compute_mode: ComputeMode,
    ) -> CalculationSqlBuilder:
        sql_builders = {
            ComputeMode.SPARK: SparkCalculationSqlBuilder,
            ComputeMode.RIFT: DuckDBCalculationSqlBuilder,
        }
        return sql_builders[compute_mode](fdw, column_reference_resolver)
