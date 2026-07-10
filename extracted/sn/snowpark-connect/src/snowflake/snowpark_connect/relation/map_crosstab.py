#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import pyspark.sql.connect.proto.relations_pb2 as relation_proto

import snowflake.snowpark.functions as fn
from snowflake import snowpark
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.relation.map_relation import map_relation
from snowflake.snowpark_connect.utils.identifiers import strip_backtick_quotes_if_quoted


def map_crosstab(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    Perform a crosstab on the input DataFrame.
    """
    input_container = map_relation(rel.crosstab.input)
    input_df = input_container.dataframe

    col1 = input_container.column_map.get_snowpark_column_name_from_spark_column_name(
        strip_backtick_quotes_if_quoted(rel.crosstab.col1)
    )
    col2 = input_container.column_map.get_snowpark_column_name_from_spark_column_name(
        strip_backtick_quotes_if_quoted(rel.crosstab.col2)
    )
    input_df = input_df.select(
        fn.col(col1).cast("string").alias(col1), fn.col(col2).cast("string").alias(col2)
    )

    # Handle empty DataFrame case
    if input_df.count() == 0:
        # For empty DataFrame, return a DataFrame with just the first column name
        result = input_df.select(
            fn.lit(f"{rel.crosstab.col1}_{rel.crosstab.col2}").alias("c0")
        )
        return DataFrameContainer.create_with_column_mapping(
            dataframe=result,
            spark_column_names=[f"{rel.crosstab.col1}_{rel.crosstab.col2}"],
            snowpark_column_names=["c0"],
        )

    result: snowpark.DataFrame = input_df.crosstab(col1, col2)

    # Parse Snowpark column names back to plain value strings.
    def _parse_value_col_name(c: str) -> str:
        if "CAST" in c:
            return "".join(c.split("CAST(")[1].split(" AS")[0].split("'"))
        if c == "NULL":
            return c.lower()
        return c[2:-2]

    raw_value_cols = result.columns[1:]
    spark_value_names = [_parse_value_col_name(c) for c in raw_value_cols]

    # Spark orders value columns alphabetically; Snowflake does not guarantee this.
    sorted_pairs = sorted(zip(spark_value_names, raw_value_cols), key=lambda p: p[0])
    sorted_spark_names = [p[0] for p in sorted_pairs]
    sorted_snowpark_cols = [p[1] for p in sorted_pairs]

    # Reorder and cast count columns to LongType (Snowflake COUNT returns Decimal)
    result = result.select(
        fn.col(result.columns[0]),
        *[fn.col(c).cast("long").alias(c) for c in sorted_snowpark_cols],
    )

    new_columns = [f"{rel.crosstab.col1}_{rel.crosstab.col2}"] + sorted_spark_names

    result = result.rename(
        dict(zip(result.columns, [f"c{i}" for i in range(len(result.columns))]))
    )
    return DataFrameContainer.create_with_column_mapping(
        dataframe=result,
        spark_column_names=new_columns,
        snowpark_column_names=result.columns,
    )
