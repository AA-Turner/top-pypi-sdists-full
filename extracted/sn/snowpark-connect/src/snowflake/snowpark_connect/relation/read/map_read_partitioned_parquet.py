#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import re
from copy import deepcopy
from typing import Any

from snowflake import snowpark
from snowflake.snowpark import Session
from snowflake.snowpark._internal.analyzer.analyzer_utils import (
    quote_name_without_upper_casing,
    unquote_if_quoted,
)
from snowflake.snowpark.functions import col, lit
from snowflake.snowpark.types import ArrayType, DataType, MapType, StructType
from snowflake.snowpark_connect.config import external_table_location
from snowflake.snowpark_connect.utils.context import (
    get_spark_session_id,
    register_request_external_table,
)
from snowflake.snowpark_connect.utils.io_utils import cached_file_format
from snowflake.snowpark_connect.utils.scala_udf_utils import map_type_to_snowflake_type

STRUCTURED_TYPE_PATTERN = re.compile(r"\([^)]*\)")


def use_external_table(session: Session, path: str) -> bool:
    external_table_path = external_table_location()
    stripped_path = path[1:-1]

    is_external_table_path_defined = external_table_path is not None
    is_stage = stripped_path.startswith("@")

    return (
        is_external_table_path_defined
        and is_stage
        and _is_external_stage(session, stripped_path)
    )


def _is_external_stage(session: Session, path: str) -> bool:
    try:
        stage_description = (
            session.sql(f"DESCRIBE STAGE {path.split('/')[0][1:]}")
            .filter(col('"property"') == lit("URL"))
            .collect()
        )
        return stage_description[0]["property_value"] != ""
    except Exception:
        return False


def _get_count_of_non_partition_path_parts(path: str) -> int:
    count = 0
    # First element of a path is a stage identifier we need to ignore it to count relative path parts
    for element in path.split("/")[1:]:
        if "=" in element:
            break
        count += 1
    return count


def read_partitioned_parquet_from_external_table(
    session: Session,
    schema: StructType,
    external_table_path: str,
    path: str,
    partition_columns: list[str],
    inferred_types: dict[str, DataType],
    snowpark_options: dict[str, Any],
) -> snowpark.DataFrame:
    skip_path_parts = _get_count_of_non_partition_path_parts(path)
    snowpark_partition_columns = ", ".join(
        [quote_name_without_upper_casing(col) for col in partition_columns]
    )
    snowpark_typed_partition_columns = ", ".join(
        [
            f"{quote_name_without_upper_casing(col)} {map_type_to_snowflake_type(inferred_types[col])} as (split_part(split_part(METADATA$FILENAME, '/', {i + skip_path_parts}), '=', 2)::{map_type_to_snowflake_type(inferred_types[col])})"
            for col, i in zip(partition_columns, range(len(partition_columns)))
        ]
    )
    snowpark_schema_columns = ",".join(
        [
            f"{field.name} {_map_snowpark_type_to_simplified_snowflake_type(field.datatype)} as (value:{field.name}::{_map_snowpark_type_to_simplified_snowflake_type(field.datatype)})"
            for field in schema.fields
            if unquote_if_quoted(field.name) not in snowpark_partition_columns
        ]
    )

    table_name = f"{external_table_path}.{quote_name_without_upper_casing(path + get_spark_session_id())}"
    snowpark_options_copy = deepcopy(snowpark_options)
    # These options are only used in the Snowpark Python reader, but not the actual emitted SQL.
    snowpark_options_copy.pop("PATTERN")
    snowpark_options_copy.pop("FORMAT_NAME")
    snowpark_options_copy.pop("ENFORCE_EXISTING_FILE_FORMAT")
    file_format_name = cached_file_format(session, "parquet", snowpark_options_copy)
    session.sql(
        f"""
        CREATE OR REPLACE EXTERNAL TABLE {table_name} (
            {snowpark_typed_partition_columns},
            {snowpark_schema_columns}
        )
        PARTITION BY ({snowpark_partition_columns})
        WITH LOCATION = {path}
        FILE_FORMAT = {file_format_name}
        PATTERN = '{snowpark_options.get('PATTERN', '.*')}'
        AUTO_REFRESH = false
        """
    ).collect()
    register_request_external_table(table_name)
    map_fields = ", ".join(
        [
            f"{field.name}::{_map_snowpark_type_to_snowflake(field.datatype)} as {field.name}"
            if isinstance(field.datatype, (StructType, MapType, ArrayType))
            else field.name
            for field in schema.fields
        ]
    )
    return session.sql(f"SELECT {map_fields} FROM {table_name}")


def _map_snowpark_type_to_simplified_snowflake_type(datatype: DataType) -> str:
    if isinstance(datatype, StructType):
        return "OBJECT"
    elif isinstance(datatype, MapType):
        return "VARIANT"
    else:
        return STRUCTURED_TYPE_PATTERN.sub("", map_type_to_snowflake_type(datatype))


def _map_snowpark_type_to_snowflake(datatype: DataType) -> str:
    if isinstance(datatype, StructType):
        object_fields = ", ".join(
            [
                f"{field.name} { _map_snowpark_type_to_snowflake(field.datatype)}"
                for field in datatype.fields
            ]
        )
        return f"OBJECT({object_fields})"
    else:
        return map_type_to_snowflake_type(datatype)
