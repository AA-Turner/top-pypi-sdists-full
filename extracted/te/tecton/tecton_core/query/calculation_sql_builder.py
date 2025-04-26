from abc import ABC
from abc import abstractmethod
from typing import Dict
from typing import Set

import attrs
import pypika.functions as fn
from pypika import NULL
from pypika.enums import Arithmetic
from pypika.enums import Equality
from pypika.terms import ArithmeticExpression
from pypika.terms import BasicCriterion
from pypika.terms import Case
from pypika.terms import Field
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
        else:
            msg = f"In Calculation sql generation, calculation operation {OperationType.Name(operation_node.operation)} not supported."
            raise TectonInternalError(msg)

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

        operand_sqls = [
            fn.Cast(self.ast_node_to_query_term(operand), "BOOLEAN").get_sql() for operand in operation_node.operands
        ]
        return LiteralValue(f"{operand_sqls[0]} AND {operand_sqls[1]}")

    def _build_logical_or_query(self, operation_node: OperationNodeSpec) -> Term:
        if len(operation_node.operands) != 2:
            msg = "Calculation OR operator must have exactly 2 operands."
            raise TectonInternalError(msg)

        operand_sqls = [
            fn.Cast(self.ast_node_to_query_term(operand), "BOOLEAN").get_sql() for operand in operation_node.operands
        ]
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
        return Field(internal_column_name)

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
        start_date_sql = self.ast_node_to_query_term(start_date_operand).get_sql()
        end_date_sql = self.ast_node_to_query_term(end_date_operand).get_sql()

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
