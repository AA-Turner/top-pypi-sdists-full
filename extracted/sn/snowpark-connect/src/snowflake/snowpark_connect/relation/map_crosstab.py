#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import pyspark.sql.connect.proto.relations_pb2 as relation_proto

import snowflake.snowpark.functions as fn
from snowflake import snowpark
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.relation.map_relation import map_relation


def map_crosstab(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    Perform a crosstab on the input DataFrame.
    """
    input_container = map_relation(rel.crosstab.input)
    input_df = input_container.dataframe

    col1 = input_container.column_map.get_snowpark_column_name_from_spark_column_name(
        rel.crosstab.col1
    )
    col2 = input_container.column_map.get_snowpark_column_name_from_spark_column_name(
        rel.crosstab.col2
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
    new_columns = [f"{rel.crosstab.col1}_{rel.crosstab.col2}"] + [
        (
            # The Spark names are just the values, so we parse them from
            # the Snowpark string.
            "".join(c.split("CAST(")[1].split(" AS")[0].split("'"))
            if "CAST" in c
            else c.lower()
            if c == "NULL"
            else c[2:-2]
        )
        for c in result.columns[1:]
    ]
    # We can easily get to a point where the column names are too long and
    # the internal columns names don't really matter to the end user anyway.
    # Rename here keeps the mapping simpler.
    result = result.rename(
        dict(zip(result.columns, [f"c{i}" for i in range(len(result.columns))]))
    )
    return DataFrameContainer.create_with_column_mapping(
        dataframe=result,
        spark_column_names=new_columns,
        snowpark_column_names=result.columns,
    )
