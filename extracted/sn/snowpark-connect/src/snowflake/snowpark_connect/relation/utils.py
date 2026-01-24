#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import random
import re
import string
import time
import uuid
from typing import Any, Sequence

import pyspark.sql.connect.proto.relations_pb2 as relation_proto

import snowflake.snowpark.functions as snowpark_fn
from snowflake import snowpark
from snowflake.snowpark import Column
from snowflake.snowpark.types import (
    BinaryType,
    BooleanType,
    ByteType,
    DataType,
    DateType,
    DecimalType,
    DoubleType,
    FloatType,
    IntegerType,
    LongType,
    ShortType,
    StringType,
    StructType,
    TimestampType,
    _NumericType,
)
from snowflake.snowpark_connect.column_name_handler import (
    ColumnNameMap,
    make_column_names_snowpark_compatible,
)
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.relation.map_relation import map_relation

TYPE_MAP_FOR_TO_SCHEMA = {
    StringType: {
        StringType,
    },
    _NumericType: {
        t
        for t in (
            _NumericType,
            DecimalType,
            StringType,
            IntegerType,
            FloatType,
            DoubleType,
            LongType,
            ShortType,
            ByteType,
        )
    },
    DecimalType: {
        t
        for t in (
            _NumericType,
            DecimalType,
            StringType,
            IntegerType,
            FloatType,
            DoubleType,
            LongType,
            ShortType,
            ByteType,
        )
    },
    BooleanType: {
        StringType,
        BooleanType,
    },
    DateType: {
        StringType,
        DateType,
        TimestampType,
    },
    TimestampType: {
        StringType,
        DateType,
        TimestampType,
    },
    BinaryType: {
        StringType,
        BinaryType,
    },
    StructType: {
        StructType,
    },
}


# This mapping is used to map the compression type to the extension of the file.
FILE_COMPRESSION_TO_EXTENSION = {
    "GZIP": "gz",
    "BZ2": "bz2",
    "BROTLI": "br",
    "ZSTD": "zst",
    "DEFLATE": "deflate",
    "RAW_DEFLATE": "raw_deflate",
    "SNAPPY": "snappy",
    "LZO": "lzo",
    "LZ4": "lz4",
    "BZIP2": "bz2",
}


def get_df_with_partition_row_number(
    container: DataFrameContainer,
    plan_id: int | None,
    row_number_column_name: str,
) -> snowpark.DataFrame:
    """
    Add a row number for each row in each partition for the given df, where
    the df is partition based on all columns.
    For example:
    +---+---+         will become           +---+---+------------+
    | C1| C2|                               | C1| C2| ROW_NUMBER |
    +---+---+                               +---+---+------------+
    |  a|  1|                               |  a|  1|  0         |
    |  a|  1|                               |  a|  1|  1         |
    |  a|  2|                               |  a|  2|  0         |
    |  c|  4|                               |  c|  4|  0         |
    +---+---+                               +---+---+------------+
    """
    df = container.dataframe
    column_map = container.column_map

    row_number_snowpark_column_name = make_column_names_snowpark_compatible(
        [row_number_column_name], plan_id, len(column_map.get_spark_columns())
    )[0]
    row_number_snowpark_column = (
        snowpark_fn.row_number()
        .over(
            snowpark.window.Window.partition_by(
                *column_map.get_snowpark_columns()
            ).order_by(snowpark_fn.lit(1))
        )
        .alias(row_number_snowpark_column_name)
    )

    df_with_partition_number = df.select(
        *column_map.get_snowpark_columns(), row_number_snowpark_column
    )
    return df_with_partition_number


def random_string(
    length: int,
    prefix: str = "",
    suffix: str = "",
    choices: Sequence[str] = string.ascii_lowercase,
) -> str:
    """Our convenience function to generate random string for object names.

    Args:
        length: How many random characters to choose from choices.
            length would be at least 6 for avoiding collision
        prefix: Prefix to add to random string generated.
        suffix: Suffix to add to random string generated.
        choices: A generator of things to choose from.
    """
    random_part = "".join([random.choice(choices) for _ in range(length)]) + str(
        time.time_ns()
    )

    return "".join([prefix, random_part, suffix])


def generate_spark_compatible_filename(
    task_id: int = 0,
    attempt_number: int = 0,
    compression: str = None,
    format_ext: str = "parquet",
    shared_uuid: str = None,
) -> str:
    """Generate a Spark-compatible filename following the convention:
    part-<task-id>-<uuid>-c<attempt-number>.<compression>.<format>

    Args:
        task_id: Task ID (usually 0 for single partition)
        attempt_number: Attempt number (usually 0)
        compression: Compression type (e.g., 'snappy', 'gzip', 'none')
        format_ext: File format extension (e.g., 'parquet', 'csv', 'json')
        shared_uuid: Shared UUID for the file

    Returns:
        A filename string following Spark's naming convention
    """
    # Use the shared UUID if provided, otherwise generate a new one for uniqueness
    file_uuid = shared_uuid or str(uuid.uuid4())

    # Format task ID with leading zeros (5 digits)
    formatted_task_id = f"{task_id:05d}"

    # Format attempt number with leading zeros (3 digits)
    formatted_attempt = f"{attempt_number:03d}"

    # Build the base filename
    base_name = f"part-{formatted_task_id}-{file_uuid}-c{formatted_attempt}"

    # Add compression if specified and not 'none'
    if compression and compression.lower() not in ("none", "uncompressed"):
        compression_part = f".{FILE_COMPRESSION_TO_EXTENSION.get(compression.upper(), compression.lower())}"
    else:
        compression_part = ""

    # Add format extension if specified
    if format_ext == "parquet":
        return f"{base_name}{compression_part}.{format_ext}"
    elif format_ext is not None and format_ext != "":
        return f"{base_name}.{format_ext}{compression_part}"
    else:
        return f"{base_name}{compression_part}"


def _normalize_query_for_semantic_hash(query_str: str) -> str:
    """
    Normalize a query string for semantic comparison by extracting original names from
    snowpark identifiers generated by make_column_names_snowpark_compatible.

    The make_column_names_snowpark_compatible function generates column names in the format:
    "original_name-plan_id_hex-column_index" where plan_id_hex is an 8-digit hexadecimal number.

    Examples:
    - "id-00000005-0" -> "id" (extract original name for source columns)
    - "col1-00000002-1" -> "COL_TARGET" (normalize target column names)
    - "a-0-0" -> "a-0-0" (not generated, leave as is)

    This makes semantically equivalent expressions with different plan IDs compare as equal
    by using the original column names for sources and normalizing target column names.
    """

    def extract_original_name(match):
        quoted_content = match.group(1)
        parts = quoted_content.split("-")
        if len(parts) >= 3:
            # Check if the second-to-last part is an 8-digit hex number
            plan_id_part = parts[-2]
            if len(plan_id_part) == 8 and all(
                c in "0123456789abcdefABCDEF" for c in plan_id_part
            ):
                # This is a generated column name, extract the original name
                original_name = "-".join(parts[:-2])
                return f'"{original_name}"'
        # Not a generated column name, return as is
        return match.group(0)

    # Apply the normalization to generated column names
    normalized_query = re.sub(
        r'"([^"]*-[0-9a-fA-F]{8}-\d+)"', extract_original_name, query_str
    )

    return normalized_query


def get_semantic_string(rel: relation_proto.Relation) -> str:
    """Calculate semantic hash of the input relation proto.
    This function parse the proto into Snowpark execution queries and calculate the hash of the parsed query strings.
    The queries are normalized to remove random identifiers for better semantic comparison.

    Args:
        rel: An input relation
    """
    queries = [
        query
        for query_list in map_relation(rel).dataframe._plan.execution_queries.values()
        for query in query_list
    ]

    normalized_queries = []
    for query in queries:
        # Set query id placeholder to empty for consistency
        query.query_id_place_holder = ""
        normalized_query_str = _normalize_query_for_semantic_hash(str(query))
        normalized_queries.append(normalized_query_str)

    return "".join(normalized_queries)


def snowpark_functions_col(name: str, column_map: ColumnNameMap) -> snowpark.Column:
    """
    Return snowpark column, by default have parameter "_is_qualified_name" on to support nested StructuredType
    """
    is_qualified_name = name not in column_map.get_snowpark_columns()
    return snowpark_fn.col(name, _is_qualified_name=is_qualified_name)


def is_aggregate_function(func_name: str) -> bool:
    """
    Check if a function name is an aggregate function.

    Uses a hybrid approach:
    1. First checks PySpark's docstring convention (docstrings starting with "Aggregate function:")
    2. Falls back to a hardcoded list for functions with missing/incorrect docstrings

    This ensures comprehensive coverage while automatically supporting new PySpark aggregate functions.

    Args:
        func_name: The function name to check (case-insensitive)

    Returns:
        True if the function is an aggregate function, False otherwise
    """
    try:
        import pyspark.sql.functions as pyspark_functions

        # TODO:
        """
        Check we can leverage scala classes to determine agg functions:
        https://github.com/apache/spark/blob/master/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/aggregate/interfaces.scala#L207
        """

        # Try PySpark docstring approach first (covers most aggregate functions)
        pyspark_func = getattr(pyspark_functions, func_name.lower(), None)
        if pyspark_func and pyspark_func.__doc__:
            if pyspark_func.__doc__.lstrip().startswith("Aggregate function:"):
                return True

        # Fallback list for aggregate functions with missing/incorrect docstrings
        # These are known aggregate functions that don't have proper docstring markers
        fallback_aggregates = {
            "percentile_cont",
            "percentile_disc",
            "any_value",
            "grouping",
            "grouping_id",
        }
        return func_name.lower() in fallback_aggregates

    except Exception:
        return False


def get_all_dependent_column_names(columns: list[Column]) -> set[str]:
    all_dependent_column_names = set()

    for col in columns:
        if hasattr(col, "_expr1"):
            all_dependent_column_names = all_dependent_column_names.union(
                col._expr1.dependent_column_names()
            )

    return all_dependent_column_names


def map_pivot_value_to_spark_column_name(pivot_value: Any) -> tuple[str, bool]:
    """
    Maps pivot_value to the spark column name, without appending the aggregation suffix.

    Returns:
        A tuple containing the spark column name and a boolean indicating whether the original_value was null or not.
    """

    is_null = False

    if pivot_value in (None, "NULL", "None"):
        spark_name = "null"
        is_null = True
    else:
        if isinstance(pivot_value, tuple):
            spark_name = str(list(pivot_value))
        elif isinstance(pivot_value, dict):
            spark_name = "{" + ", ".join(str(v) for v in pivot_value.values()) + "}"
        else:
            spark_name = str(pivot_value)

    return spark_name, is_null


def create_pivot_column_condition(
    col: Column,
    pivot_value: Any,
    pivot_value_is_null: bool,
    cast_literal_to: DataType | None = None,
) -> snowpark.Column:
    if isinstance(pivot_value, dict):
        elements = [
            snowpark_fn.lit(item) for pair in pivot_value.items() for item in pair
        ]
        lit = snowpark_fn.object_construct_keep_null(*elements)
    else:
        lit = snowpark_fn.lit(pivot_value)

    if cast_literal_to:
        lit = snowpark_fn.cast(lit, cast_literal_to)

    return snowpark_fn.is_null(col) if pivot_value_is_null else (col == lit)
