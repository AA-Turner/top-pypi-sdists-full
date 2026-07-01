#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

from snowflake.snowpark import Column, functions as snowpark_fn
from snowflake.snowpark._internal.analyzer.expression import (
    CaseWhen,
    Expression,
    FunctionExpression,
    SnowflakeUDF,
)

_SF_AGGREGATE_FUNCTIONS = [
    "any_value",
    "avg",
    "corr",
    "count",
    "count_if",
    "covar_pop",
    "covar_samp",
    "listagg",
    "max",
    "max_by",
    "median",
    "min",
    "min_by",
    "mode",
    "percentile_cont",
    "percentile_disc",
    "stddev",
    "stddev_samp",
    "stddev_pop",
    "sum",
    "var_pop",
    "var_samp",
    "variance_pop",
    "variance",
    "variance_samp",
    "bitand_agg",
    "bitor_agg",
    "bitxor_agg",
    "booland_agg",
    "boolor_agg",
    "boolxor_agg",
    "hash_agg",
    "array_agg",
    "object_agg",
    "regr_avgx",
    "regr_avgy",
    "regr_count",
    "regr_intercept",
    "regr_r2",
    "regr_slope",
    "regr_sxx",
    "regr_sxy",
    "regr_syy",
    "kurtosis",
    "skew",
    "array_union_agg",
    "array_unique_agg",
    "bitmap_bit_position",
    "bitmap_bucket_number",
    "bitmap_count",
    "bitmap_construct_agg",
    "bitmap_or_agg",
    "approx_count_distinct",
    "datasketches_hll",
    "datasketches_hll_accumulate",
    "datasketches_hll_combine",
    "datasketches_hll_estimate",
    "hll",
    "hll_accumulate",
    "hll_combine",
    "hll_estimate",
    "hll_export",
    "hll_import",
    "approximate_jaccard_index",
    "approximate_similarity",
    "minhash",
    "minhash_combine",
    "approx_top_k",
    "approx_top_k_accumulate",
    "approx_top_k_combine",
    "approx_top_k_estimate",
    "approx_percentile",
    "approx_percentile_accumulate",
    "approx_percentile_combine",
    "approx_percentile_estimate",
    "grouping",
    "grouping_id",
    "ai_agg",
    "ai_summarize_agg",
]


def _is_agg_function_expression(expression: Expression) -> bool:
    if (
        isinstance(expression, FunctionExpression)
        and expression.pretty_name.lower() in _SF_AGGREGATE_FUNCTIONS
    ):
        return True

    # For PySpark aggregate functions that were mapped using a UDAF, e.g. try_sum
    if isinstance(expression, SnowflakeUDF) and expression.is_aggregate_function:
        return True

    return False


def _get_child_expressions(expression: Expression) -> list[Expression]:
    if isinstance(expression, CaseWhen):
        return expression._child_expressions

    return expression.children or []


def inject_condition_to_all_agg_functions(
    expression: Expression, condition: Column
) -> None:
    """
    Recursively traverses an expression tree and wraps all aggregate function arguments with a CASE WHEN condition.

    Args:
        expression: The Snowpark expression tree to traverse and modify.
        condition: The Column condition to inject into aggregate function arguments.
    """

    any_agg_function_found = _inject_condition_to_all_agg_functions(
        expression, condition
    )

    if not any_agg_function_found:
        raise ValueError(f"No aggregate functions found in: {expression.sql}")


def _inject_condition_to_all_agg_functions(
    expression: Expression, condition: Column
) -> bool:
    any_agg_function_found = False

    if _is_agg_function_expression(expression):
        new_children = []
        for child in _get_child_expressions(expression):
            case_when = snowpark_fn.when(condition, Column(child))

            new_children.append(case_when._expr1)

        # Swap children
        expression.children = new_children
        if len(new_children) > 0:
            expression.child = new_children[0]

        return True

    for child in _get_child_expressions(expression):
        is_agg_function_in_child = _inject_condition_to_all_agg_functions(
            child, condition
        )

        if is_agg_function_in_child:
            any_agg_function_found = True

    return any_agg_function_found


def is_child_agg_function_expression(exp: Expression) -> bool:
    if _is_agg_function_expression(exp):
        return True

    return any(
        is_child_agg_function_expression(child) for child in _get_child_expressions(exp)
    )
