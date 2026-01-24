#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import re
from contextvars import ContextVar
from functools import cache

import jpype
import pyspark.sql.connect.proto.expressions_pb2 as expressions_proto
import pyspark.sql.connect.proto.types_pb2 as types_proto
from google.protobuf.any_pb2 import Any
from pyspark.errors.exceptions.base import AnalysisException
from pyspark.sql.connect import functions as pyspark_functions

import snowflake.snowpark_connect.proto.snowflake_expression_ext_pb2 as snowflake_proto
from snowflake.snowpark._internal.analyzer.analyzer_utils import unquote_if_quoted
from snowflake.snowpark.types import DayTimeIntervalType, YearMonthIntervalType
from snowflake.snowpark_connect.column_name_handler import ColumnNameMap
from snowflake.snowpark_connect.config import global_config
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.typed_column import TypedColumn
from snowflake.snowpark_connect.utils.context import (
    get_jpype_jclass_lock,
    get_sql_named_arg,
    get_sql_plan,
    get_sql_pos_arg,
    push_evaluating_sql_scope,
    push_sql_scope,
)
from snowflake.snowpark_connect.utils.telemetry import (
    SnowparkConnectNotImplementedError,
)

from .typer import ExpressionTyper

DECIMAL_RE = re.compile(r"decimal\((\d+), *(\d+)\)")

_INTERVAL_YEARMONTH_PATTERN_RE = re.compile(r"interval (year|month)( to (year|month))?")
_INTERVAL_DAYTIME_PATTERN_RE = re.compile(
    r"interval (day|hour|minute|second)( to (day|hour|minute|second))?"
)

# Interval field mappings using proper constants
_YEAR_MONTH_FIELD_MAP = {
    "year": YearMonthIntervalType.YEAR,
    "month": YearMonthIntervalType.MONTH,
}

_DAY_TIME_FIELD_MAP = {
    "day": DayTimeIntervalType.DAY,
    "hour": DayTimeIntervalType.HOUR,
    "minute": DayTimeIntervalType.MINUTE,
    "second": DayTimeIntervalType.SECOND,
}

_window_specs = ContextVar[dict[str, any]]("_window_specs", default={})

# Functions that can be called without parentheses in Spark SQL. Build up the list as we see more functions.
NILARY_FUNCTIONS = frozenset(
    [
        "current_date",
        "current_timestamp",
        "current_user",
        "user",
    ]
)


def sql_parser():
    """
    SparkSqlParser needs spark.config. Here we are setting required config keys for SAS.
    We can't do it in set.config request handler, because SparkSqlParser initialized without active SparkSession (our case, todo: fix it)
    uses ThreadLocal to access conf, and conf.set can be handled by other thread.
    https://github.com/apache/spark/blob/ea53ea71461508801586b1e5677aa6011df7cd95/sql/catalyst/src/main/scala/org/apache/spark/sql/internal/SQLConf.scala#L143
    """

    ts_type = global_config.spark_sql_timestampType
    session_tz = global_config.spark_sql_session_timeZone

    if ts_type is not None:
        _get_sql_conf().get().setConfString("spark.sql.timestampType", str(ts_type))

    if session_tz is not None:
        _get_sql_conf().get().setConfString(
            "spark.sql.session.timeZone", str(session_tz)
        )

    return _get_sql_parser()


@cache
def _get_sql_parser():
    with get_jpype_jclass_lock():
        return jpype.JClass("org.apache.spark.sql.execution.SparkSqlParser")()


@cache
def _get_sql_conf():
    with get_jpype_jclass_lock():
        return jpype.JClass("org.apache.spark.sql.internal.SQLConf")


@cache
def _as_java_list():
    with get_jpype_jclass_lock():
        return jpype.JClass("scala.collection.JavaConverters").seqAsJavaList


def as_java_list(obj):
    return _as_java_list()(obj)


@cache
def _as_java_map():
    with get_jpype_jclass_lock():
        return jpype.JClass("scala.collection.JavaConverters").mapAsJavaMap


def as_java_map(obj):
    return _as_java_map()(obj)


def as_scala_seq(input):
    inputList = as_java_list(input)
    return (
        jpype.JClass("scala.collection.JavaConverters")
        .asScalaIteratorConverter(inputList.iterator())
        .asScala()
        .toSeq()
    )


@cache
def _scala_some():
    return jpype.JClass("scala.Some")


def map_sql_expr(
    exp: expressions_proto.Expression,
    column_mapping: ColumnNameMap,
    typer: ExpressionTyper,
) -> tuple[list[str], TypedColumn]:
    """
    Map Spark SQL to a Snowpark expression.
    """
    from snowflake.snowpark_connect.expression.map_expression import map_expression

    sql = exp.expression_string.expression
    logical_plan = sql_parser().parseExpression(sql)

    with push_sql_scope():
        proto = map_logical_plan_expression(logical_plan)

    with push_evaluating_sql_scope():
        return map_expression(proto, column_mapping, typer)


SPARK_OP_TO_PROTO = {
    "Add": "+",
    "Subtract": "-",
    "Multiply": "*",
    "Divide": "/",
    "IntegralDivide": "div",
    "Remainder": "%",
    "Subtract": "-",
    "UnaryMinus": "unary_minus",
    "UnaryPositive": "positive",
    "LessThan": "<",
    "GreaterThan": ">",
    "LessThanOrEqual": "<=",
    "GreaterThanOrEqual": ">=",
    "EqualTo": "==",
    "EqualNullSafe": "<=>",
    "BitwiseAnd": "&",
    "BitwiseOr": "|",
    "BitwiseXor": "^",
    "BitwiseNot": "~",
    "Not": "not",
    "And": "and",
    "Or": "or",
    "Concat": "concat",
    "In": "in",
    "IsNull": "isnull",
    "IsNotNull": "isnotnull",
    "PercentileCont": "percentile_cont",
    "PercentileDisc": "percentiledisc",
    "Lower": "lower",
    "Overlay": "overlay",
}

SPARK_SORT_DIRECTION_TO_PROTO = {
    "Ascending": expressions_proto.Expression.SortOrder.SORT_DIRECTION_ASCENDING,
    "Descending": expressions_proto.Expression.SortOrder.SORT_DIRECTION_DESCENDING,
}

SPARK_SORT_NULL_ORDERING_TO_PROTO = {
    "NullsFirst": expressions_proto.Expression.SortOrder.SORT_NULLS_FIRST,
    "NullsLast": expressions_proto.Expression.SortOrder.SORT_NULLS_LAST,
}

SPARK_FRAME_TYPE_TO_PROTO = {
    "RowFrame": expressions_proto.Expression.Window.WindowFrame.FRAME_TYPE_ROW,
    "RangeFrame": expressions_proto.Expression.Window.WindowFrame.FRAME_TYPE_RANGE,
}

SPARK_STRING_TRIM_FUNCS = {
    "StringTrim": "trim",
    "StringTrimLeft": "ltrim",
    "StringTrimRight": "rtrim",
}


def escape_spark_quoted(name: str) -> str:
    double_ticks = name.replace("`", "``")
    return f"`{double_ticks}`"


def map_frame_boundary(
    exp: jpype.JObject,
) -> expressions_proto.Expression.Window.WindowFrame.FrameBoundary:
    match str(exp.nodeName()):
        case "UnboundedPreceding$" | "UnboundedFollowing$":
            return expressions_proto.Expression.Window.WindowFrame.FrameBoundary(
                unbounded=True,
            )
        case "CurrentRow$":
            return expressions_proto.Expression.Window.WindowFrame.FrameBoundary(
                current_row=True,
            )
        case _:
            return expressions_proto.Expression.Window.WindowFrame.FrameBoundary(
                value=map_logical_plan_expression(exp)
            )


def apply_filter_clause(
    func_name: str,
    args: list[expressions_proto.Expression],
    exp: jpype.JObject,
    is_distinct: bool = False,
) -> expressions_proto.Expression:
    """Apply FILTER clause transformation if present, otherwise return normal function call."""
    if hasattr(exp, "filter"):
        filter_opt = exp.filter()
        if filter_opt.isDefined():
            # FILTER clause found - translate to CASE WHEN
            # This is the standard SQL transformation:
            # sum(value) FILTER (WHERE condition) → sum(CASE WHEN condition THEN value ELSE NULL END)
            filter_condition = map_logical_plan_expression(filter_opt.get())

            # Wrap each argument with CASE WHEN filter_condition THEN arg ELSE NULL END
            args = [
                expressions_proto.Expression(
                    unresolved_function=expressions_proto.Expression.UnresolvedFunction(
                        function_name="when",
                        arguments=[filter_condition, arg],
                    )
                )
                for arg in args
            ]

    return expressions_proto.Expression(
        unresolved_function=expressions_proto.Expression.UnresolvedFunction(
            function_name=func_name,
            arguments=args,
            is_distinct=is_distinct,
        )
    )


def map_logical_plan_expression(exp: jpype.JObject) -> expressions_proto.Expression:
    from snowflake.snowpark_connect.relation.map_sql import map_logical_plan_relation

    class_name = str(exp.getClass().getSimpleName())
    match class_name:
        case "AggregateExpression":
            aggregate_func = as_java_list(exp.children())[0]
            func_name = aggregate_func.nodeName()
            args = [
                map_logical_plan_expression(e)
                for e in list(as_java_list(aggregate_func.children()))
            ]

            # Special handling for percentile_cont and percentile_disc
            # These functions have a 'reverse' property that indicates sort order
            # Pass it as a 3rd argument (sort_order expression) without modifying children
            if func_name.lower() in ("percentile_cont", "percentiledisc"):
                # percentile_cont/disc should always have exactly 2 children: unresolved attribute and percentile value
                if len(args) != 2:
                    exception = AssertionError(
                        f"{func_name} expected 2 args but got {len(args)}"
                    )
                    attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
                    raise exception

                reverse = bool(aggregate_func.reverse())

                direction = (
                    expressions_proto.Expression.SortOrder.SORT_DIRECTION_DESCENDING
                    if reverse
                    else expressions_proto.Expression.SortOrder.SORT_DIRECTION_ASCENDING
                )

                sort_order_expr = expressions_proto.Expression(
                    sort_order=expressions_proto.Expression.SortOrder(
                        child=args[0],
                        direction=direction,
                    )
                )
                args.append(sort_order_expr)
                proto = apply_filter_clause(func_name, [args[0]], exp)
                # second arg is a literal value and it doesn't make sense to apply filter on it.
                # also skips filtering on sort_order.
                proto.unresolved_function.arguments.append(args[1])
                proto.unresolved_function.arguments.append(sort_order_expr)
            else:
                proto = apply_filter_clause(func_name, args, exp)
        case "Alias":
            proto = expressions_proto.Expression(
                alias=expressions_proto.Expression.Alias(
                    expr=map_logical_plan_expression(exp.child()),
                    name=[str(exp.name())],
                )
            )
        case "CaseWhen":
            # exp has a .branches() method that gives us conditions and results
            # in a more structured format - however, we would need to flatten them, anyway,
            # so just use .children()
            proto = expressions_proto.Expression(
                unresolved_function=expressions_proto.Expression.UnresolvedFunction(
                    function_name="when",
                    arguments=[
                        map_logical_plan_expression(e)
                        for e in list(as_java_list(exp.children()))
                    ],
                )
            )
        case "Cast":
            proto = expressions_proto.Expression(
                cast=expressions_proto.Expression.Cast(
                    expr=map_logical_plan_expression(exp.child()),
                    type=None,
                    type_str=str(exp.dataType().simpleString()),
                )
            )
        case "Coalesce":
            arguments = [
                map_logical_plan_expression(e)
                for e in list(as_java_list(exp.children()))
            ]

            proto = expressions_proto.Expression(
                unresolved_function=expressions_proto.Expression.UnresolvedFunction(
                    function_name="coalesce",
                    arguments=arguments,
                )
            )
        case "CreateNamedStruct":
            # Both struct() and named_struct() Spark SQL functions produce a CreateNamedStruct
            # logical plan. We distinguish them by checking exp.prettyName():
            # - "named_struct" -> explicit named_struct() call, requires name-value pairs
            # - "struct" -> struct() call, field names are inferred from column expressions

            # Additionally, struct(*) with star expansion is handled as named_struct.
            # TODO - consider refactoring the impl and handle it in "struct" impl

            arg_exprs = [
                arg
                for k_v in zip(
                    as_java_list(exp.nameExprs()), as_java_list(exp.valExprs())
                )
                for arg in k_v
            ]

            if (
                "unresolvedstar" in [e.prettyName() for e in arg_exprs]
                or exp.prettyName() == "named_struct"
            ):
                struct_args = [
                    map_logical_plan_expression(e)
                    for e in arg_exprs
                    if e.prettyName() != "NamePlaceholder"
                ]
                proto = expressions_proto.Expression(
                    unresolved_function=expressions_proto.Expression.UnresolvedFunction(
                        function_name="named_struct",
                        arguments=struct_args,
                    )
                )
            else:
                arg_exprs = [arg for arg in as_java_list(exp.valExprs())]
                struct_args = [map_logical_plan_expression(e) for e in arg_exprs]
                proto = expressions_proto.Expression(
                    unresolved_function=expressions_proto.Expression.UnresolvedFunction(
                        function_name="struct",
                        arguments=struct_args,
                    )
                )
        case "Exists":
            rel_proto = map_logical_plan_relation(exp.plan())
            any_proto = Any()
            any_proto.Pack(
                snowflake_proto.ExpExtension(
                    subquery_expression=snowflake_proto.SubqueryExpression(
                        input=rel_proto,
                        subquery_type=snowflake_proto.SubqueryExpression.SUBQUERY_TYPE_EXISTS,
                    )
                )
            )
            proto = expressions_proto.Expression(extension=any_proto)
        case "ExpressionWithUnresolvedIdentifier":
            from snowflake.snowpark_connect.relation.map_sql import (
                get_relation_identifier_name,
            )

            value = unquote_if_quoted(get_relation_identifier_name(exp))
            if getattr(pyspark_functions, value.lower(), None) is not None:
                unresolved_function = exp.exprBuilder().apply(
                    _scala_some()(value).toList()
                )
                proto = map_logical_plan_expression(unresolved_function)
            else:
                proto = expressions_proto.Expression(
                    unresolved_attribute=expressions_proto.Expression.UnresolvedAttribute(
                        unparsed_identifier=str(value),
                        plan_id=None,
                    ),
                )
        case "InSubquery":
            rel_proto = map_logical_plan_relation(exp.query().plan())
            any_proto = Any()
            any_proto.Pack(
                snowflake_proto.ExpExtension(
                    subquery_expression=snowflake_proto.SubqueryExpression(
                        input=rel_proto,
                        subquery_type=snowflake_proto.SubqueryExpression.SUBQUERY_TYPE_IN,
                        in_subquery_values=[
                            map_logical_plan_expression(value)
                            for value in list(as_java_list(exp.values()))
                        ],
                    )
                )
            )
            proto = expressions_proto.Expression(extension=any_proto)
        case "LambdaFunction":
            arguments = [
                map_logical_plan_expression(arg).unresolved_named_lambda_variable
                for arg in list(as_java_list(exp.arguments()))
            ]
            proto = expressions_proto.Expression(
                lambda_function=expressions_proto.Expression.LambdaFunction(
                    function=map_logical_plan_expression(exp.function()),
                    arguments=arguments,
                )
            )
        case "Like" | "ILike" | "RLike":
            arguments = [
                map_logical_plan_expression(e)
                for e in list(as_java_list(exp.children()))
            ]
            # exp.escapeChar() returns a JPype JChar - convert to string and create a literal
            if getattr(exp, "escapeChar", None) is not None:
                escape_char_str = str(exp.escapeChar())
                escape_literal = expressions_proto.Expression(
                    literal=expressions_proto.Expression.Literal(string=escape_char_str)
                )
                arguments.append(escape_literal)
            proto = expressions_proto.Expression(
                unresolved_function=expressions_proto.Expression.UnresolvedFunction(
                    function_name=class_name.lower(),
                    arguments=arguments,
                )
            )
        case "LikeAny" | "NotLikeAny" | "LikeAll" | "NotLikeAll":
            patterns = list(as_java_list(exp.patterns()))
            arguments = [
                map_logical_plan_expression(e)
                for e in list(as_java_list(exp.children()))
            ]
            arguments += [map_logical_plan_expression(e) for e in patterns]
            proto = expressions_proto.Expression(
                unresolved_function=expressions_proto.Expression.UnresolvedFunction(
                    function_name=class_name.lower(),
                    arguments=arguments,
                )
            )
        case "Literal":
            type_name = str(exp.dataType().typeName())
            type_value = exp.value()

            if type_name == "string":
                type_value = str(type_value)
            elif type_name == "void":
                type_name = "null"
                type_value = types_proto.DataType()
            elif type_name == "binary":
                type_value = bytes(type_value)
            elif year_month_match := _INTERVAL_YEARMONTH_PATTERN_RE.match(type_name):
                # Extract start and end fields for year-month intervals
                start_field_name = year_month_match.group(1)  # 'year' or 'month'
                end_field_name = (
                    year_month_match.group(3)
                    if year_month_match.group(3)
                    else start_field_name
                )

                # Validate field names exist in mapping
                start_field = _YEAR_MONTH_FIELD_MAP.get(start_field_name)
                end_field = _YEAR_MONTH_FIELD_MAP.get(end_field_name)

                if start_field is None:
                    exception = AnalysisException(
                        f"Invalid year-month interval start field: '{start_field_name}'. Expected 'year' or 'month'."
                    )
                    attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                    raise exception
                if end_field is None:
                    exception = AnalysisException(
                        f"Invalid year-month interval end field: '{end_field_name}'. Expected 'year' or 'month'."
                    )
                    attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                    raise exception

                # Validate field ordering (start_field should be <= end_field)
                if start_field > end_field:
                    exception = AnalysisException(
                        f"Invalid year-month interval: start field '{start_field_name}' must come before or equal to end field '{end_field_name}'."
                    )
                    attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                    raise exception

                # Use extension for year-month intervals to preserve start/end field info
                literal = expressions_proto.Expression.Literal(
                    year_month_interval=type_value
                )
                any_proto = Any()
                any_proto.Pack(
                    snowflake_proto.ExpExtension(
                        interval_literal=snowflake_proto.IntervalLiteralExpression(
                            literal=literal,
                            start_field=start_field,
                            end_field=end_field,
                        )
                    )
                )
                return expressions_proto.Expression(extension=any_proto)
            elif day_time_match := _INTERVAL_DAYTIME_PATTERN_RE.match(type_name):
                # Extract start and end fields for day-time intervals
                start_field_name = day_time_match.group(
                    1
                )  # 'day', 'hour', 'minute', 'second'
                end_field_name = (
                    day_time_match.group(3)
                    if day_time_match.group(3)
                    else start_field_name
                )

                # Validate field names exist in mapping
                start_field = _DAY_TIME_FIELD_MAP.get(start_field_name)
                end_field = _DAY_TIME_FIELD_MAP.get(end_field_name)

                if start_field is None:
                    exception = AnalysisException(
                        f"Invalid day-time interval start field: '{start_field_name}'. Expected 'day', 'hour', 'minute', or 'second'."
                    )
                    attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                    raise exception
                if end_field is None:
                    exception = AnalysisException(
                        f"Invalid day-time interval end field: '{end_field_name}'. Expected 'day', 'hour', 'minute', or 'second'."
                    )
                    attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                    raise exception

                # Validate field ordering (start_field should be <= end_field)
                if start_field > end_field:
                    exception = AnalysisException(
                        f"Invalid day-time interval: start field '{start_field_name}' must come before or equal to end field '{end_field_name}'."
                    )
                    attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                    raise exception

                # Use extension for day-time intervals to preserve start/end field info
                literal = expressions_proto.Expression.Literal(
                    day_time_interval=type_value
                )
                any_proto = Any()
                any_proto.Pack(
                    snowflake_proto.ExpExtension(
                        interval_literal=snowflake_proto.IntervalLiteralExpression(
                            literal=literal,
                            start_field=start_field,
                            end_field=end_field,
                        )
                    )
                )
                return expressions_proto.Expression(extension=any_proto)
            elif m := DECIMAL_RE.fullmatch(type_name):
                type_name = "decimal"
                type_value = expressions_proto.Expression.Literal.Decimal(
                    value=str(type_value),
                    precision=int(m.group(1)),
                    scale=int(m.group(2)),
                )

            proto = expressions_proto.Expression(
                literal=expressions_proto.Expression.Literal(
                    **{
                        type_name: type_value,
                    }
                )
            )
        case "MultiAlias":
            proto = expressions_proto.Expression(
                alias=expressions_proto.Expression.Alias(
                    expr=map_logical_plan_expression(exp.child()),
                    name=as_java_list(exp.names()),
                )
            )
        case "NamedArgumentExpression":
            name = str(exp.key())
            value = map_logical_plan_expression(exp.child())
            any_proto = Any()
            any_proto.Pack(
                snowflake_proto.ExpExtension(
                    named_argument=snowflake_proto.NamedArgumentExpression(
                        key=name,
                        value=value,
                    )
                )
            )
            proto = expressions_proto.Expression(extension=any_proto)
        case "NamedParameter":
            name = str(exp.name())
            value = get_sql_named_arg(name)
            if not value.HasField("literal_type"):
                exception = AnalysisException(f"Found an unbound parameter {name!r}")
                attach_custom_error_code(exception, ErrorCodes.INVALID_SQL_SYNTAX)
                raise exception
            proto = expressions_proto.Expression(literal=value)
        case "NamePlaceholder$":
            # This is a placeholder for an expression name to be resolved later.
            exception = SnowparkConnectNotImplementedError(
                "NamePlaceholder is not supported in SQL expressions."
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception
        case "PosParameter":
            pos = exp.pos()
            try:
                value = get_sql_pos_arg(pos)
            except KeyError:
                exception = AnalysisException(
                    f"Found an unbound parameter at position {pos}"
                )
                attach_custom_error_code(exception, ErrorCodes.INVALID_SQL_SYNTAX)
                raise exception
            proto = expressions_proto.Expression(literal=value)
        case "ScalarSubquery":
            rel_proto = map_logical_plan_relation(exp.plan())
            any_proto = Any()
            any_proto.Pack(
                snowflake_proto.ExpExtension(
                    subquery_expression=snowflake_proto.SubqueryExpression(
                        input=rel_proto,
                        subquery_type=snowflake_proto.SubqueryExpression.SUBQUERY_TYPE_SCALAR,
                    )
                )
            )
            proto = expressions_proto.Expression(extension=any_proto)
        case "SortOrder":
            direction = SPARK_SORT_DIRECTION_TO_PROTO[str(exp.direction())]
            null_ordering = SPARK_SORT_NULL_ORDERING_TO_PROTO[str(exp.nullOrdering())]
            proto = expressions_proto.Expression(
                sort_order=expressions_proto.Expression.SortOrder(
                    child=map_logical_plan_expression(exp.child()),
                    direction=direction,
                    null_ordering=null_ordering,
                )
            )
        case op if (func_name := SPARK_STRING_TRIM_FUNCS.get(op)):
            args = [exp.srcStr()]
            if not exp.trimStr().isEmpty():
                args.append(exp.trimStr().get())
            proto = expressions_proto.Expression(
                unresolved_function=expressions_proto.Expression.UnresolvedFunction(
                    function_name=func_name,
                    arguments=[map_logical_plan_expression(arg) for arg in args],
                )
            )
        case "StringLocate":
            proto = expressions_proto.Expression(
                unresolved_function=expressions_proto.Expression.UnresolvedFunction(
                    function_name="position",
                    arguments=[
                        map_logical_plan_expression(exp.substr()),
                        map_logical_plan_expression(exp.str()),
                        map_logical_plan_expression(exp.start()),
                    ],
                )
            )
        case "Substring":
            proto = expressions_proto.Expression(
                unresolved_function=expressions_proto.Expression.UnresolvedFunction(
                    function_name="substring",
                    arguments=[
                        map_logical_plan_expression(exp.str()),
                        map_logical_plan_expression(exp.pos()),
                        map_logical_plan_expression(exp.len()),
                    ],
                )
            )
        case "TimestampAdd" | "TimestampDiff":
            func = "timestamp_add" if class_name == "TimestampAdd" else "timestamp_diff"
            proto = expressions_proto.Expression(
                unresolved_function=expressions_proto.Expression.UnresolvedFunction(
                    function_name=func,
                    arguments=[
                        expressions_proto.Expression(
                            literal=expressions_proto.Expression.Literal(
                                string=str(exp.unit())
                            )
                        )
                    ]
                    + [
                        map_logical_plan_expression(e)
                        for e in list(as_java_list(exp.children()))
                    ],
                )
            )
        case "UnresolvedAlias":
            proto = map_logical_plan_expression(exp.child())
        case "UnresolvedAttribute":
            *parents, name = as_java_list(exp.nameParts())
            if not parents and name.lower() in NILARY_FUNCTIONS:
                # this is very likely a function call without parentheses disguised as an attribute, e.g. `CURRENT_TIMESTAMP` instead of `CURRENT_TIMESTAMP()`.
                # Note limitation: this only works when these names are not real table column names, which should be very rare and is bad practice. E.g., mytable(CURRENT_TIMESTAMP, col2, col3).
                proto = expressions_proto.Expression(
                    unresolved_function=expressions_proto.Expression.UnresolvedFunction(
                        function_name=name.lower(),
                        is_distinct=False,
                    )
                )
            else:
                plan_id = None
                is_fully_qualified_name = False
                if parents:
                    parent_name = ".".join(str(p) for p in parents)
                    plan_id = get_sql_plan(parent_name)
                    # If no plan_id exists, treat the column name as fully qualified by its parent.
                    if plan_id is None:
                        # There's a difference in how Spark sql and dataframe operation passes backticks in column names.
                        # Spark sql un-escapes the backticks instead of passing the raw string. This
                        # logic is to escape backticks again to make it consistent with regular spark functions.
                        parent_chain = ".".join(escape_spark_quoted(p) for p in parents)
                        name = f"{parent_chain}.{escape_spark_quoted(name)}"
                        is_fully_qualified_name = True

                if not is_fully_qualified_name:
                    # There's a difference in how Spark sql and dataframe operation passes backticks in column names.
                    # Spark sql un-escapes the backticks instead of passing the raw string. This
                    # logic is to escape backticks again to make it consistent with regular spark functions.
                    name = escape_spark_quoted(name)

                proto = expressions_proto.Expression(
                    unresolved_attribute=expressions_proto.Expression.UnresolvedAttribute(
                        unparsed_identifier=str(name),
                        plan_id=plan_id,
                    ),
                )
        case "UnresolvedExtractValue":
            proto = expressions_proto.Expression(
                unresolved_extract_value=expressions_proto.Expression.UnresolvedExtractValue(
                    child=map_logical_plan_expression(exp.child()),
                    extraction=map_logical_plan_expression(exp.extraction()),
                )
            )
        case "UnresolvedFunction":
            func_name = ".".join(
                str(part) for part in list(as_java_list(exp.nameParts()))
            ).lower()
            args = [
                map_logical_plan_expression(arg)
                for arg in list(as_java_list(exp.arguments()))
            ]

            proto = apply_filter_clause(func_name, args, exp, exp.isDistinct())
        case "UnresolvedNamedLambdaVariable":
            proto = expressions_proto.Expression(
                unresolved_named_lambda_variable=expressions_proto.Expression.UnresolvedNamedLambdaVariable(
                    name_parts=[
                        str(part) for part in list(as_java_list(exp.nameParts()))
                    ],
                )
            )
        case "UnresolvedStar":
            if exp.target().isEmpty():
                proto = expressions_proto.Expression(
                    unresolved_star=expressions_proto.Expression.UnresolvedStar()
                )
            else:
                proto = expressions_proto.Expression(
                    unresolved_star=expressions_proto.Expression.UnresolvedStar(
                        unparsed_target=f"{'.'.join(as_java_list(exp.target().get()))}.*",
                    )
                )
        case "UnresolvedWindowExpression":
            window_spec_reference = exp.windowSpec().name()
            window_spec = _window_specs.get().get(window_spec_reference)
            if window_spec is not None:
                # Build Window expression
                proto = get_window_expression_proto(window_spec, exp.child())
            else:
                exception = AnalysisException(
                    f"Window specification not found {window_spec_reference!r}"
                )
                attach_custom_error_code(exception, ErrorCodes.INSUFFICIENT_INPUT)
                raise exception
        case "UTF8String":
            proto = expressions_proto.Expression(
                literal=expressions_proto.Expression.Literal(
                    **{
                        "string": exp.toString(),
                    }
                )
            )
        case "WindowExpression":
            window_spec = exp.windowSpec()
            proto = get_window_expression_proto(window_spec, exp.windowFunction())
        case "FunctionTableSubqueryArgumentExpression":
            rel_proto = map_logical_plan_relation(exp.plan())
            any_proto = Any()
            any_proto.Pack(
                snowflake_proto.ExpExtension(
                    subquery_expression=snowflake_proto.SubqueryExpression(
                        input=rel_proto,
                        subquery_type=snowflake_proto.SubqueryExpression.SUBQUERY_TYPE_TABLE_ARG,
                    )
                )
            )
            proto = expressions_proto.Expression(extension=any_proto)
        case op if (proto_func := SPARK_OP_TO_PROTO.get(op)) is not None:
            proto = expressions_proto.Expression(
                unresolved_function=expressions_proto.Expression.UnresolvedFunction(
                    function_name=proto_func,
                    arguments=[
                        map_logical_plan_expression(arg)
                        for arg in list(as_java_list(exp.children()))
                    ],
                )
            )

        case other:
            exception = SnowparkConnectNotImplementedError(f"Not implemented: {other}")
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception

    return proto


def get_window_expression_proto(
    window_spec, window_function
) -> expressions_proto.Expression:
    frame_spec = window_spec.frameSpecification()
    if frame_spec.nodeName() == "UnspecifiedFrame$":
        frame_spec_proto = None
    else:
        frame_spec_proto = expressions_proto.Expression.Window.WindowFrame(
            frame_type=SPARK_FRAME_TYPE_TO_PROTO[str(frame_spec.frameType())],
            lower=map_frame_boundary(frame_spec.lower()),
            upper=map_frame_boundary(frame_spec.upper()),
        )

    proto = expressions_proto.Expression(
        window=expressions_proto.Expression.Window(
            window_function=map_logical_plan_expression(window_function),
            partition_spec=[
                map_logical_plan_expression(e)
                for e in list(as_java_list(window_spec.partitionSpec()))
            ],
            order_spec=[
                map_logical_plan_expression(e).sort_order
                for e in list(as_java_list(window_spec.orderSpec()))
            ],
            frame_spec=frame_spec_proto,
        )
    )
    return proto
