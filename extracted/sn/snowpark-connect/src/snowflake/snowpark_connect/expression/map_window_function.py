#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import pyspark.sql.connect.proto.expressions_pb2 as expressions_proto

from snowflake import snowpark
from snowflake.snowpark_connect.column_name_handler import ColumnNameMap
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import (
    SparkException,
    attach_custom_error_code,
)
from snowflake.snowpark_connect.expression.literal import get_literal_field_and_name
from snowflake.snowpark_connect.expression.typer import ExpressionTyper
from snowflake.snowpark_connect.typed_column import TypedColumn
from snowflake.snowpark_connect.utils.context import temporary_window_expression

# SQL functions that support ROWS BETWEEN but not RANGE BETWEEN.
ROWS_ONLY_FUNCTIONS = frozenset(
    ["first", "first_value", "last", "last_value", "nth_value", "rank", "dense_rank"]
)

SPARK_RANKING_FUNCTIONS = frozenset(
    [
        "row_number",
        "rank",
        "dense_rank",
        "percent_rank",
        "ntile",
        "lag",
        "lead",
    ]
)

RANGE_BASED_WINDOW_FRAME_ONLY_SNOWFLAKE_FUNCTIONS = frozenset(["percent_rank"])

CAPITAL_FUNCTION_NAMES = frozenset(["rank()", "dense_rank()", "percent_rank()"])


def map_window_function(
    exp: expressions_proto.Expression,
    column_mapping: ColumnNameMap,
    typer: ExpressionTyper,
) -> tuple[str, TypedColumn]:
    from snowflake.snowpark_connect.expression.map_expression import (
        map_single_column_expression,
    )

    with temporary_window_expression():

        def parse_frame_boundary(
            boundary: expressions_proto.Expression.Window.WindowFrame.FrameBoundary,
            is_upper: bool,
        ) -> tuple[str, int]:
            if boundary.HasField("current_row"):
                return "CURRENT ROW", snowpark.Window.CURRENT_ROW
            elif boundary.HasField("unbounded"):
                if is_upper:
                    return "UNBOUNDED FOLLOWING", snowpark.Window.UNBOUNDED_FOLLOWING
                else:
                    return "UNBOUNDED PRECEDING", snowpark.Window.UNBOUNDED_PRECEDING
            elif boundary.HasField("value"):
                # the expression has to be literal of int in the case of rows_between or range_betwen
                if boundary.value.HasField("literal"):
                    literal, _ = get_literal_field_and_name(boundary.value.literal)
                else:
                    expr_proto = boundary.value
                    session = snowpark.Session.get_active_session()
                    m = ColumnNameMap([], [], None)
                    expr = map_single_column_expression(
                        expr_proto, m, ExpressionTyper.dummy_typer(session)
                    )
                    literal = session.range(1).select(expr[1].col).collect()[0][0]

                return f"{literal} FOLLOWING", literal

        function_name, window_func = map_single_column_expression(
            exp.window.window_function, column_mapping, typer
        )
        partitions = []
        partition_col_names = []
        for p in exp.window.partition_spec:
            partition_col_name, typed_col = map_single_column_expression(
                p, column_mapping, typer
            )
            map_single_column_expression(p, column_mapping, typer)[1].col
            partition_col_names.append(partition_col_name)
            partitions.append(typed_col.col)

        orders = []
        order_col_names = []
        for order in exp.window.order_spec:
            order_col_name, (order_exp, _) = map_single_column_expression(
                order.child, column_mapping, typer
            )

            order_col_name_parts = [order_col_name]
            match order.direction:
                case expressions_proto.Expression.SortOrder.SortDirection.SORT_DIRECTION_ASCENDING:
                    order_col_name_parts.append("ASC")
                    match order.null_ordering:
                        case expressions_proto.Expression.SortOrder.NullOrdering.SORT_NULLS_FIRST:
                            order_col_name_parts.append("NULLS FIRST")
                            orders.append(order_exp.asc_nulls_first())
                        case expressions_proto.Expression.SortOrder.NullOrdering.SORT_NULLS_LAST:
                            order_col_name_parts.append("NULLS LAST")
                            orders.append(order_exp.asc_nulls_last())
                        case _:
                            orders.append(order_exp.asc())
                case expressions_proto.Expression.SortOrder.SortDirection.SORT_DIRECTION_DESCENDING:
                    order_col_name_parts.append("DESC")
                    match order.null_ordering:
                        case expressions_proto.Expression.SortOrder.NullOrdering.SORT_NULLS_FIRST:
                            order_col_name_parts.append("NULLS FIRST")
                            orders.append(order_exp.desc_nulls_first())
                        case expressions_proto.Expression.SortOrder.NullOrdering.SORT_NULLS_LAST:
                            order_col_name_parts.append("NULLS LAST")
                            orders.append(order_exp.desc_nulls_last())
                        case _:
                            orders.append(order_exp.desc())
                case _:
                    # When order direction is not specified, nulls first/last is ignored, because
                    # there is no order_exp.nulls_first() / order_exp.nulls_last()
                    orders.append(order_exp)

            order_col_names.append(" ".join(order_col_name_parts))

        frame_name = []
        proto_func_name = (
            exp.window.window_function.unresolved_function.function_name.lower()
        )
        match exp.window.frame_spec.frame_type:
            case expressions_proto.Expression.Window.WindowFrame.FrameType.FRAME_TYPE_ROW:
                frame_name.append("ROWS BETWEEN")
                frame_type_func_string = "rows_between"
                if proto_func_name in RANGE_BASED_WINDOW_FRAME_ONLY_SNOWFLAKE_FUNCTIONS:
                    # Seems like Snowflake and Spark have different understanding of some functions. For those,
                    # Spark only allows rows_between while Snowflake only allows range_between. To be compatible
                    # with Spark, we have to use range_between here.
                    frame_type_func_string = "range_between"
                lower_name, lower = parse_frame_boundary(
                    exp.window.frame_spec.lower, is_upper=False
                )
                upper_name, upper = parse_frame_boundary(
                    exp.window.frame_spec.upper, is_upper=True
                )
                if proto_func_name in SPARK_RANKING_FUNCTIONS and (
                    lower != snowpark.Window.UNBOUNDED_PRECEDING
                    or upper != snowpark.Window.CURRENT_ROW
                ):
                    exception = SparkException.invalid_ranking_function_window_frame(
                        window_frame=f"specifiedwindowframe(RowFrame, {lower_name}, {upper_name})"
                    )
                    attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                    raise exception

                is_unbounded = (
                    lower == snowpark.Window.UNBOUNDED_PRECEDING
                    and upper == snowpark.Window.UNBOUNDED_FOLLOWING
                )
                if not orders and is_unbounded:
                    orders = [column_mapping.get_snowpark_columns()[0]]
                frame_name.append(f"{lower_name} AND {upper_name}")
            case expressions_proto.Expression.Window.WindowFrame.FrameType.FRAME_TYPE_RANGE:
                frame_name.append("RANGE BETWEEN")
                frame_type_func_string = "range_between"

                lower_name, lower = parse_frame_boundary(
                    exp.window.frame_spec.lower, is_upper=False
                )
                upper_name, upper = parse_frame_boundary(
                    exp.window.frame_spec.upper, is_upper=True
                )
                if lower == upper == snowpark.Window.CURRENT_ROW and orders:
                    # only one order is allowed when the frame is between current row and current row. and spark seems
                    # to ignore the non-first order.
                    orders = orders[:1]

                if proto_func_name in SPARK_RANKING_FUNCTIONS:
                    exception = SparkException.invalid_ranking_function_window_frame(
                        window_frame=f"specifiedwindowframe(RangeFrame, {lower_name}, {upper_name})"
                    )
                    attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                    raise exception

                is_unbounded = (
                    lower == snowpark.Window.UNBOUNDED_PRECEDING
                    and upper == snowpark.Window.UNBOUNDED_FOLLOWING
                )
                if not orders and is_unbounded:
                    orders = [column_mapping.get_snowpark_columns()[0]]
                frame_name.append(f"{lower_name} AND {upper_name}")
            case _:
                """
                Spark behavior:

                Default frame specification depends on other aspects of a given window defintion:

                if the ORDER BY clause is specified and the function accepts the frame specification, then the frame specification is defined by RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW,
                otherwise the frame specification is defined by ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING.

                RANKING window functions do not accept FRAMING.
                """
                frame_type_func_string = "rows_between"
                frame_type_string = "ROWS"
                if orders:
                    # Work around functions that support ROWS BETWEEN but not RANGE BETWEEN:
                    # for current row or unbounded limits there should be no difference.
                    lower_name, lower = (
                        "UNBOUNDED PRECEDING",
                        snowpark.Window.UNBOUNDED_PRECEDING,
                    )
                    upper_name, upper = "CURRENT ROW", snowpark.Window.CURRENT_ROW
                    match proto_func_name:
                        case "nth_value":
                            frame_type_string = "RANGE"
                        case "lag" | "lead":
                            frame_type_func_string = "range_between"
                            func_args = (
                                exp.window.window_function.unresolved_function.arguments
                            )
                            sign = -1 if proto_func_name == "lag" else 1
                            offset = (
                                func_args[1].literal.integer
                                if len(func_args) > 1
                                else 1
                            )
                            lower_name = upper_name = f"{sign * offset} FOLLOWING"
                        case _ if proto_func_name not in ROWS_ONLY_FUNCTIONS:
                            frame_type_func_string = "range_between"
                            frame_type_string = (
                                "RANGE"
                                if proto_func_name not in SPARK_RANKING_FUNCTIONS
                                else frame_type_string
                            )
                else:
                    orders = [column_mapping.get_snowpark_columns()[0]]
                    lower_name, lower = (
                        "UNBOUNDED PRECEDING",
                        snowpark.Window.UNBOUNDED_PRECEDING,
                    )
                    upper_name, upper = (
                        "UNBOUNDED FOLLOWING",
                        snowpark.Window.UNBOUNDED_FOLLOWING,
                    )
                frame_name.append(
                    f"{frame_type_string} BETWEEN {lower_name} AND {upper_name}"
                )

        # build window
        window = snowpark.Window
        if len(partitions) > 0:
            window = window.partitionBy(partitions)
        if len(orders) > 0:
            window = window.orderBy(orders)
        window = getattr(window, frame_type_func_string)(lower, upper)

        if function_name in CAPITAL_FUNCTION_NAMES:
            # weird spark behavior
            function_name = function_name.upper()

        window_parts = []
        if partition_col_names:
            window_parts.append(f"PARTITION BY {', '.join(partition_col_names)}")
        if order_col_names:
            window_parts.append(f"ORDER BY {', '.join(order_col_names)}")
        window_parts.extend(frame_name)
        spark_col_name = f"{function_name} OVER ({' '.join(window_parts)})"

        result_exp = window_func.over(window)

        return spark_col_name, TypedColumn(result_exp, lambda: window_func.types)
