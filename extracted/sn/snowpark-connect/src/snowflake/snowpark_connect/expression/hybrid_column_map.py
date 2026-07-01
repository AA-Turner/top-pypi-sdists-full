#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""
Hybrid column mapping for HAVING clause resolution.

This module provides a special column mapping that can resolve expressions
in the context of both the input DataFrame (for base columns) and the
aggregated DataFrame (for aggregate expressions and aliases).
"""

from typing import Dict, List

import pyspark.sql.connect.proto.expressions_pb2 as expressions_proto

from snowflake import snowpark
from snowflake.snowpark_connect.column_name_handler import ColumnNameMap
from snowflake.snowpark_connect.expression.typer import ExpressionTyper
from snowflake.snowpark_connect.typed_column import TypedColumn
from snowflake.snowpark_connect.utils.identifiers import (
    split_fully_qualified_spark_name,
)


class HybridColumnMap:
    """
    A column mapping that can resolve expressions in both input and aggregated contexts.

    This is specifically designed for HAVING clause resolution where expressions may reference:
    1. Base columns from the input DataFrame (to build new aggregates)
    2. Existing aggregate expressions and their aliases
    3. Grouping columns
    """

    def __init__(
        self,
        input_column_map: ColumnNameMap,
        input_typer: ExpressionTyper,
        aggregated_column_map: ColumnNameMap,
        aggregated_typer: ExpressionTyper,
        aggregate_expressions: List[expressions_proto.Expression],
        grouping_expressions: List[expressions_proto.Expression],
        aggregate_aliases: Dict[str, expressions_proto.Expression],
    ) -> None:
        self.input_column_map = input_column_map
        self.input_typer = input_typer
        self.aggregated_column_map = aggregated_column_map
        self.aggregated_typer = aggregated_typer
        self.aggregate_expressions = aggregate_expressions
        self.grouping_expressions = grouping_expressions
        self.aggregate_aliases = aggregate_aliases

    def is_aggregate_function(self, exp: expressions_proto.Expression) -> bool:
        """Check if an expression is an aggregate function."""
        if exp.WhichOneof("expr_type") == "unresolved_function":
            func_name = exp.unresolved_function.function_name.lower()
            # Common aggregate functions - expand this list as needed
            aggregate_functions = {
                "avg",
                "average",
                "sum",
                "count",
                "min",
                "max",
                "stddev",
                "stddev_pop",
                "stddev_samp",
                "variance",
                "var_pop",
                "var_samp",
                "collect_list",
                "collect_set",
                "first",
                "last",
                "any_value",
                "bool_and",
                "bool_or",
                "corr",
                "covar_pop",
                "covar_samp",
                "kurtosis",
                "skewness",
                "percentile_cont",
                "percentile_disc",
                "approx_count_distinct",
            }
            return func_name in aggregate_functions
        return False

    def is_grouping_column(self, column_name: str) -> bool:
        """Check if a column name refers to a grouping column."""
        for group_exp in self.grouping_expressions:
            if (
                group_exp.WhichOneof("expr_type") == "unresolved_attribute"
                and group_exp.unresolved_attribute.unparsed_identifier == column_name
            ):
                return True
        return False

    def resolve_expression(
        self, exp: expressions_proto.Expression
    ) -> tuple[list[str], TypedColumn]:
        """
        Resolve an expression in the hybrid context.

        Strategy:
        1. If it's an aggregate function -> create new aggregate using input context
        2. If it's an alias to existing aggregate -> use aggregated context
        3. If it's a grouping column -> try aggregated context first, fall back to input context
           (handles exclude_grouping_columns=True case)
        4. Otherwise -> try input context first, then aggregated context
        """
        from snowflake.snowpark_connect.expression.map_expression import map_expression

        expr_type = exp.WhichOneof("expr_type")

        # Handle aggregate functions - need to evaluate against input DataFrame
        if self.is_aggregate_function(exp):
            return map_expression(exp, self.input_column_map, self.input_typer)

        # Handle column references
        if expr_type == "unresolved_attribute":
            column_name = exp.unresolved_attribute.unparsed_identifier
            name_parts = split_fully_qualified_spark_name(column_name)
            alias_column_name = name_parts[0]

            # Check if it's an alias to an existing aggregate expression
            if alias_column_name in self.aggregate_aliases:
                # Use the aggregated context to get the alias
                return map_expression(
                    exp, self.aggregated_column_map, self.aggregated_typer
                )

            # Check if it's a grouping column
            if self.is_grouping_column(column_name):
                # Try aggregated context first (for cases where grouping columns are included)
                try:
                    return map_expression(
                        exp, self.aggregated_column_map, self.aggregated_typer
                    )
                except Exception:
                    # Fall back to input context if grouping columns were excluded
                    # This handles the exclude_grouping_columns=True case
                    return map_expression(exp, self.input_column_map, self.input_typer)

            # Try input context first (for base columns used in new aggregates)
            try:
                return map_expression(exp, self.input_column_map, self.input_typer)
            except Exception:
                # Fall back to aggregated context
                return map_expression(
                    exp, self.aggregated_column_map, self.aggregated_typer
                )

        try:
            # 1. Evaluate the expression using the input grouping columns. i.e input_df.
            # If not found, use the aggregate alias.
            return map_expression(exp, self.input_column_map, self.input_typer)
        except Exception:
            # Fall back to input context
            return map_expression(
                exp, self.aggregated_column_map, self.aggregated_typer
            )


def create_hybrid_column_map_for_having(
    input_df: snowpark.DataFrame,
    input_column_map: ColumnNameMap,
    aggregated_df: snowpark.DataFrame,
    aggregated_column_map: ColumnNameMap,
    aggregate_expressions: List[expressions_proto.Expression],
    grouping_expressions: List[expressions_proto.Expression],
    spark_columns: List[str],
    raw_aggregations: List[tuple[str, TypedColumn]],
) -> HybridColumnMap:
    """
    Create a HybridColumnMap instance for HAVING clause resolution.
    """
    # Create typers for both contexts
    input_typer = ExpressionTyper(input_df)
    aggregated_typer = ExpressionTyper(aggregated_df)

    # Build alias mapping from spark column names to aggregate expressions
    aggregate_aliases = {}
    for i, (spark_name, _) in enumerate(raw_aggregations):
        if i < len(aggregate_expressions):
            aggregate_aliases[spark_name] = aggregate_expressions[i]

    return HybridColumnMap(
        input_column_map=input_column_map,
        input_typer=input_typer,
        aggregated_column_map=aggregated_column_map,
        aggregated_typer=aggregated_typer,
        aggregate_expressions=aggregate_expressions,
        grouping_expressions=grouping_expressions,
        aggregate_aliases=aggregate_aliases,
    )


def create_hybrid_column_map_for_order_by(
    aggregate_metadata,  # AggregateMetadata type
    aggregated_df: snowpark.DataFrame,
    aggregated_column_map: ColumnNameMap,
) -> HybridColumnMap:
    """
    Create a HybridColumnMap instance for ORDER BY clause resolution after aggregation.

    This is similar to HAVING clause resolution - ORDER BY can reference:
    1. Grouping columns (e.g., year, a)
    2. Aggregate aliases (e.g., cnt)
    3. Expressions on grouping columns (e.g., year(date) where date is pre-aggregation)

    Args:
        aggregate_metadata: Metadata from the aggregate operation
        aggregated_df: The DataFrame after aggregation
        aggregated_column_map: Column mapping for the aggregated DataFrame

    Returns:
        HybridColumnMap for resolving ORDER BY expressions
    """
    # Create typers for both contexts
    input_typer = ExpressionTyper(aggregate_metadata.input_dataframe)
    aggregated_typer = ExpressionTyper(aggregated_df)

    # Build alias mapping from spark column names to aggregate expressions
    aggregate_aliases = {}
    for i, (spark_name, _) in enumerate(aggregate_metadata.raw_aggregations):
        if i < len(aggregate_metadata.aggregate_expressions):
            aggregate_aliases[spark_name] = aggregate_metadata.aggregate_expressions[i]

    return HybridColumnMap(
        input_column_map=aggregate_metadata.input_column_map,
        input_typer=input_typer,
        aggregated_column_map=aggregated_column_map,
        aggregated_typer=aggregated_typer,
        aggregate_expressions=aggregate_metadata.aggregate_expressions,
        grouping_expressions=aggregate_metadata.grouping_expressions,
        aggregate_aliases=aggregate_aliases,
    )
