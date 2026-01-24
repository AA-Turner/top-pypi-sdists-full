#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import pyspark.sql.connect.proto.expressions_pb2 as expressions_proto
import pyspark.sql.connect.proto.relations_pb2 as relation_proto

from snowflake import snowpark
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.expression.literal import get_literal_field_and_name
from snowflake.snowpark_connect.expression.map_expression import (
    map_single_column_expression,
)
from snowflake.snowpark_connect.expression.typer import ExpressionTyper
from snowflake.snowpark_connect.relation.map_relation import map_relation


def map_sample_by(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    Sample by an expression on the input DataFrame.
    """
    input_container = map_relation(rel.sample_by.input)
    input_df = input_container.dataframe

    exp: expressions_proto.Expression = rel.sample_by.col
    _, col_expr = map_single_column_expression(
        exp, input_container.column_map, ExpressionTyper(input_df)
    )
    fractions = {
        get_literal_field_and_name(frac.stratum)[0]: frac.fraction
        for frac in rel.sample_by.fractions
    }
    result: snowpark.DataFrame = input_df.sampleBy(col_expr.col, fractions)
    return DataFrameContainer(
        result,
        column_map=input_container.column_map,
        table_name=input_container.table_name,
        alias=input_container.alias,
        cached_schema_getter=lambda: input_df.schema,
    )
