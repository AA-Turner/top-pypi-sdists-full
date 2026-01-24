#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import datetime
from collections import defaultdict

import pyspark.sql.connect.proto.expressions_pb2 as expressions_proto
from pyspark.errors.exceptions.connect import AnalysisException

import snowflake.snowpark.functions as snowpark_fn
from snowflake import snowpark
from snowflake.snowpark import Session
from snowflake.snowpark._internal.analyzer.expression import UnresolvedAttribute
from snowflake.snowpark.types import TimestampTimeZone, TimestampType
from snowflake.snowpark_connect.column_name_handler import ColumnNameMap
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.expression import (
    map_extension,
    map_udf,
    map_unresolved_attribute as map_att,
    map_unresolved_extract_value as map_unresolved_extract_value,
    map_unresolved_function as map_func,
    map_unresolved_star as map_unresolved_star,
    map_update_fields as map_update_fields,
    map_window_function as map_window_func,
)
from snowflake.snowpark_connect.expression.literal import get_literal_field_and_name
from snowflake.snowpark_connect.expression.map_cast import map_cast
from snowflake.snowpark_connect.expression.map_sql_expression import map_sql_expr
from snowflake.snowpark_connect.expression.typer import ExpressionTyper
from snowflake.snowpark_connect.type_mapping import (
    map_simple_types,
    proto_to_snowpark_type,
)
from snowflake.snowpark_connect.typed_column import TypedColumn
from snowflake.snowpark_connect.utils.context import (
    gen_sql_plan_id,
    get_current_lambda_params,
    is_function_argument_being_resolved,
    is_lambda_being_resolved,
    not_resolving_fun_args,
)
from snowflake.snowpark_connect.utils.telemetry import (
    SnowparkConnectNotImplementedError,
)


def map_alias(
    alias: expressions_proto.Expression.Alias,
    column_mapping: ColumnNameMap,
    typer: ExpressionTyper,
) -> tuple[list[str], TypedColumn]:
    """
    Map an alias expression to a Snowpark expression.
    - Single column: Returns ([alias_name], TypedColumn)
    - Multi-column: Returns ([alias1, alias2, ...], TypedColumn)

    Args:
        alias (expressions_proto.Expression.Alias): The alias expression to map.
    """
    if len(list(alias.name)) > 1:
        # Multi-column case: handle like explode("map").alias("key", "value")
        col_names, col = map_expression(alias.expr, column_mapping, typer)
        if len(col_names) != len(list(alias.name)):
            exception = ValueError(
                f"Found the unresolved operator: 'Project [{col_names} AS ({', '.join(list(alias.name))})]. Number of aliases ({len(list(alias.name))}) does not match number of columns ({len(col_names)})"
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
            raise exception
        return list(alias.name), col

    name, col = map_single_column_expression(alias.expr, column_mapping, typer)
    col_name = alias.name[0]
    if is_function_argument_being_resolved() or is_lambda_being_resolved():
        # Function arguments need to be quoted if they contain spaces and require syntax 'expr AS alias' instead of 'alias'
        col_name = (
            f"`{col_name.replace('`', '``')}`"
            if any(char.isspace() or char == "`" for char in col_name)
            else col_name
        )
        col_name = f"{name} AS {col_name}"
    # Spark passes a list for alias name, but it is unclear why since alias
    # can only take a single argument.
    # We need to make sure that the aliased snowpark column has a unique name, so
    # gen_sql_plan_id is used to suffix the alias.
    # TODO: do we need to push down the actual plan_id?
    if is_lambda_being_resolved():
        return [col_name], col
    return [col_name], col.alias(f"{alias.name[0]}-{gen_sql_plan_id()}")


def map_single_column_expression(
    exp: expressions_proto.Expression,
    column_mapping: ColumnNameMap,
    typer: ExpressionTyper,
) -> tuple[str, TypedColumn]:
    col_names, typed_col = map_expression(exp, column_mapping, typer)
    assert (
        len(col_names) == 1
    ), f"Expected exactly single column expression, got {len(col_names)}"
    return col_names[0], typed_col


def map_expression(
    exp: expressions_proto.Expression,
    column_mapping: ColumnNameMap,
    typer: ExpressionTyper,
) -> tuple[list[str], TypedColumn]:
    """
    Map an expression to a Snowpark expression.

    Args:
        exp (expressions_proto.Expression): The expression to map.
        column_mapping (ColumnNameMapper): The mapping from column names to Snowpark
            column objects.
    """

    expr_type = exp.WhichOneof("expr_type")
    match expr_type:
        case "alias":
            return map_alias(exp.alias, column_mapping, typer)
        case "call_function":
            new_expression = expressions_proto.Expression(
                unresolved_function=expressions_proto.Expression.UnresolvedFunction(
                    function_name=exp.call_function.function_name,
                    arguments=exp.call_function.arguments,
                )
            )
            return map_func.map_unresolved_function(
                new_expression, column_mapping, typer
            )
        case "cast":
            return map_cast(exp, column_mapping, typer)
        case "common_inline_user_defined_function":
            name, col = map_udf.map_common_inline_user_defined_udf(
                exp, column_mapping, typer
            )
            return [name], col
        case "expression_string":
            return map_sql_expr(exp, column_mapping, typer)
        case "extension":
            # Extensions can be passed as function args, and we need to reset the context here.
            # Matters only for resolving alias expressions in the extensions rel.
            with not_resolving_fun_args():
                return map_extension.map_extension(exp, column_mapping, typer)
        case "lambda_function":
            lambda_name, lambda_body = map_single_column_expression(
                exp.lambda_function.function, column_mapping, typer
            )
            args = [a.name_parts[0] for a in exp.lambda_function.arguments]
            args_str = ", ".join(args)
            analyzer = Session.get_active_session()._analyzer
            body_str = analyzer.analyze(lambda_body.col._expression, defaultdict())
            result_exp = snowpark_fn.sql_expr(f"({args_str}) -> {body_str}")
            args_name = ", ".join(["namedlambdavariable()"] * len(args))
            return (
                [f"lambdafunction({lambda_name}, {args_name})"],
                TypedColumn(
                    result_exp,
                    # It's not accurate - TypeColumn holds lambda expression, so "type of the lambda" should be returned here.
                    # Instead, we return type of lambda body expression. But it's ok - since no one ever should need "type of the lambda"
                    lambda: lambda_body.types,
                ),
            )
        case "literal":
            lit_value, lit_name = get_literal_field_and_name(exp.literal)
            lit_type_str = str(exp.literal.WhichOneof("literal_type"))
            # this is a hack until we would have an interval type supported in snowflake, for now
            # this will use the interval expression instead of literal expression to solve this usecase.
            if isinstance(lit_value, datetime.timedelta):
                return [lit_name], TypedColumn(
                    snowpark_fn.make_interval(
                        days=lit_value.days,
                        seconds=lit_value.seconds,
                        microseconds=lit_value.microseconds,
                    ),
                    lambda: [map_simple_types(lit_type_str)],
                )

            if lit_type_str == "array":
                result_exp = snowpark_fn.lit(lit_value)
                element_types = proto_to_snowpark_type(exp.literal.array.element_type)
                array_type = snowpark.types.ArrayType(element_types)
                return [lit_name], TypedColumn(result_exp, lambda: [array_type])

            # Decimal needs further processing to get the precision and scale properly.
            if lit_type_str == "decimal":
                # Precision and scale are optional in the proto.
                precision = 38
                scale = 0
                decimal_msg = exp.literal.decimal
                if decimal_msg.HasField("precision"):
                    precision = decimal_msg.precision
                if decimal_msg.HasField("scale"):
                    scale = decimal_msg.scale
                if "." in decimal_msg.value and precision == 10 and scale == 0:
                    # Spark Connect protobuf will sometimes give the default precision and scale for Decimals
                    # so we manually determine what the precision and scale actually are.
                    # decimal {
                    #    value: "123.45"
                    #    precision: 10
                    #    scale: 0
                    # }
                    precision = len(decimal_msg.value) - 1
                    scale = len(decimal_msg.value.split(".")[1])

                return_type = snowpark.types.DecimalType(precision, scale)
                return [lit_name], TypedColumn(
                    snowpark_fn.lit(lit_value, return_type), lambda: [return_type]
                )
            result_exp = snowpark_fn.lit(lit_value)

            if lit_type_str == "timestamp_ntz" and isinstance(
                lit_value, datetime.datetime
            ):
                result_exp = result_exp.cast(TimestampType(TimestampTimeZone.NTZ))

            return [lit_name], TypedColumn(
                result_exp, lambda: [map_simple_types(lit_type_str)]
            )
        case "sort_order":
            child_name, child_column = map_single_column_expression(
                exp.sort_order.child, column_mapping, typer
            )
            match exp.sort_order.direction:
                case (
                    exp.sort_order.SORT_DIRECTION_UNSPECIFIED
                    | exp.sort_order.SORT_DIRECTION_ASCENDING
                ):
                    if exp.sort_order.null_ordering == exp.sort_order.SORT_NULLS_LAST:
                        col = snowpark_fn.asc_nulls_last(child_column.col)
                    else:
                        # If nulls are not specified or null_ordering is FIRST in the sort order, Spark defaults to nulls
                        # first in the case of ascending sort order.
                        col = snowpark_fn.asc_nulls_first(child_column.col)
                case exp.sort_order.SORT_DIRECTION_DESCENDING:
                    if exp.sort_order.null_ordering == exp.sort_order.SORT_NULLS_FIRST:
                        col = snowpark_fn.desc_nulls_first(child_column.col)
                    else:
                        # If nulls are not specified or null_ordering is LAST in the sort order, Spark defaults to nulls
                        # last in the case of descending sort order.
                        col = snowpark_fn.desc_nulls_last(child_column.col)
                case _:
                    exception = ValueError(
                        f"Invalid sort direction {exp.sort_order.direction}"
                    )
                    attach_custom_error_code(
                        exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                    )
                    raise exception
            return [child_name], TypedColumn(col, lambda: typer.type(col))
        case "unresolved_attribute":
            col_name, col = map_att.map_unresolved_attribute(exp, column_mapping, typer)
            # Check if this is a multi-column regex expansion
            matched_cols = getattr(col, "_regex_matched_columns", list())
            if matched_cols:
                # Create expressions for all matched columns
                snowpark_cols = [c.snowpark_name for c in matched_cols]
                spark_cols = [c.spark_name for c in matched_cols]
                # Create a combined expression for all columns
                col_expr = snowpark_fn.sql_expr(", ".join(snowpark_cols))
                return (
                    spark_cols,
                    TypedColumn(
                        col_expr,
                        lambda: [
                            typer.type(snowpark_fn.col(sc))[0] for sc in snowpark_cols
                        ],
                    ),
                )
            return [col_name], col
        case "unresolved_extract_value":
            col_name, col = map_unresolved_extract_value.map_unresolved_extract_value(
                exp, column_mapping, typer
            )
            return [col_name], col
        case "unresolved_function":
            from snowflake.snowpark_connect.utils.context import (
                get_is_processing_order_by,
            )

            is_order_by = get_is_processing_order_by()
            if is_order_by:
                # For expressions in an order by clause check if we can reuse already-computed column.
                if exp.unresolved_function.function_name:
                    func_name = exp.unresolved_function.function_name
                    available_columns = column_mapping.get_spark_columns()

                    for col_name in available_columns:
                        if (
                            func_name.lower() in col_name.lower()
                            and "(" in col_name
                            and ")" in col_name
                        ):
                            # This looks like it might be an expression
                            snowpark_col_name = column_mapping.get_snowpark_column_name_from_spark_column_name(
                                col_name
                            )
                            if snowpark_col_name:
                                # Optimization applied - reusing already computed column
                                return [col_name], TypedColumn(
                                    snowpark_fn.col(snowpark_col_name),
                                    lambda col_name=snowpark_col_name: typer.type(
                                        col_name
                                    ),
                                )

            return map_func.map_unresolved_function(exp, column_mapping, typer)
        case "unresolved_named_lambda_variable":
            # Validate that this lambda variable is in scope
            var_name = exp.unresolved_named_lambda_variable.name_parts[0]
            current_params = get_current_lambda_params()

            if current_params and var_name not in current_params:
                outer_col_name = (
                    column_mapping.get_snowpark_column_name_from_spark_column_name(
                        var_name, allow_non_exists=True
                    )
                )
                if outer_col_name:
                    col = snowpark_fn.col(outer_col_name)
                    return ["namedlambdavariable()"], TypedColumn(
                        col, lambda: typer.type(col)
                    )
                else:
                    exception = AnalysisException(
                        f"Cannot resolve variable '{var_name}' within lambda function. "
                        f"Lambda functions can access their own parameters and parent dataframe columns. "
                        f"Current lambda parameters: {current_params}. "
                        f"If '{var_name}' is an outer scope lambda variable from a nested lambda, "
                        f"that is an unsupported feature in Snowflake SQL."
                    )
                    attach_custom_error_code(
                        exception, ErrorCodes.UNSUPPORTED_OPERATION
                    )
                    raise exception

            col = snowpark_fn.Column(
                UnresolvedAttribute(exp.unresolved_named_lambda_variable.name_parts[0])
            )
            for child_name in exp.unresolved_named_lambda_variable.name_parts[1:]:
                col = col.getItem(child_name)
            return ["namedlambdavariable()"], TypedColumn(col, lambda: typer.type(col))
        case "unresolved_regex":
            p = exp.unresolved_regex.col_name
            pattern_str = p[1:-1] if p.startswith("`") and p.endswith("`") else p

            columns = column_mapping.get_columns_matching_pattern(pattern_str)
            spark_cols, snowpark_cols = (
                [c.spark_name for c in columns],
                [c.snowpark_name for c in columns],
            )

            col_expr = snowpark_fn.sql_expr(", ".join(snowpark_cols))
            return (
                spark_cols,
                TypedColumn(col_expr, lambda: typer.type(col_expr))
                if snowpark_cols
                else TypedColumn.empty(),
            )
        case "unresolved_star":
            return map_unresolved_star.map_unresolved_star(exp, column_mapping, typer)
        case "window":
            col_name, col = map_window_func.map_window_function(
                exp, column_mapping, typer
            )
            return [col_name], col
        case "update_fields":
            return map_update_fields.map_update_fields(exp, column_mapping, typer)
        case _:
            exception = SnowparkConnectNotImplementedError(
                f"Unsupported expression type {expr_type}"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception
