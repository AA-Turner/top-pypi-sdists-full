#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
import contextlib
import dataclasses
import functools
import json
import re

from pyspark.errors.exceptions.connect import AnalysisException

from snowflake import snowpark
from snowflake.snowpark import Column, Session
from snowflake.snowpark._internal.analyzer.analyzer_utils import (
    create_file_format_statement,
    unquote_if_quoted,
)
from snowflake.snowpark.functions import col, equal_null, lit
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.utils.identifiers import FQN, spark_to_sf_single_id

_MINUS_AT_THE_BEGINNING_REGEX = re.compile(r"^-")


def cached_file_format(
    session: Session, file_format: str, format_type_options: dict[str, str]
) -> str:
    """
    Cache and return a file format name based on the given options.
    """

    function_name = _MINUS_AT_THE_BEGINNING_REGEX.sub(
        "1", str(hash(frozenset(format_type_options.items())))
    )
    file_format_name = f"__SNOWPARK_CONNECT_FILE_FORMAT__{file_format}_{function_name}"
    if file_format_name in session._file_formats:
        return file_format_name

    session.sql(
        create_file_format_statement(
            file_format_name,
            file_format,
            format_type_options,
            temp=True,
            if_not_exist=True,
            use_scoped_temp_objects=False,
            is_generated=True,
        )
    ).collect()

    session._file_formats.add(file_format_name)
    return file_format_name


@functools.cache
def file_format(
    session: Session, compression: str, record_delimiter: str = None
) -> str:
    """
    Create a temporary file format for reading text files in Snowpark Connect.
    """
    if record_delimiter is None:
        record_delimiter = "NONE"
        identifier_delimiter = "NONE"
    else:
        record_delimiter = record_delimiter
        # Encode delimiter to ensure that it is a valid identifier
        identifier_delimiter = record_delimiter.encode("utf-8").hex()

    file_format_name = f"IDENTIFIER('__SNOWPARK_CONNECT_TEXT_FILE_FORMAT__{compression}_{identifier_delimiter}')"
    session.sql(
        f"""
    CREATE TEMPORARY FILE FORMAT IF NOT EXISTS  {file_format_name}
    RECORD_DELIMITER = '{record_delimiter}'
    FIELD_DELIMITER = 'NONE'
    EMPTY_FIELD_AS_NULL = FALSE
    COMPRESSION = '{compression}'"""
    ).collect()

    return file_format_name


def get_table_type(
    snowpark_table_name: str,
    snowpark_session: Session,
) -> str:
    fqn = FQN.from_string(snowpark_table_name)
    with contextlib.suppress(Exception):
        if fqn.database is not None:
            return snowpark_session.catalog.getTable(
                table_name=fqn.name, schema=fqn.schema, database=fqn.database
            ).table_type
        elif fqn.schema is not None:
            return snowpark_session.catalog.getTable(
                table_name=fqn.name, schema=fqn.schema
            ).table_type
        else:
            return snowpark_session.catalog.getTable(table_name=fqn.name).table_type
    return "TABLE"


@dataclasses.dataclass
class PartitionField:
    name: str
    transform: str
    source_id: int

    @property
    def position(self) -> int:
        """
        0-indexed column position
        """
        return self.source_id - 1


@dataclasses.dataclass
class PartitionSpec:
    fields: list[PartitionField]

    def uses_transform(self) -> bool:
        """
        Returns True if any partition field uses a transform.
        """
        return any(f.transform != "identity" for f in self.fields)

    def columns(self) -> list[str]:
        return [f.name for f in self.fields]

    def partition_column_positions(self) -> list[int]:
        return [f.position for f in self.fields]


def get_partition_spec(table_name: str, session: Session) -> PartitionSpec | None:
    """
    Retrieves basic partition specs (list of fields with transforms) for the given table.
    """
    fqn = FQN.from_string(table_name)
    table_schema = ".".join(
        [part for part in [fqn.database, fqn.schema] if part is not None]
    )
    unquoted_table_name = unquote_if_quoted(fqn.name)

    # "show" is the only way to get partition specs
    if table_schema:
        show_query = (
            f"show iceberg tables like '{unquoted_table_name}' in schema {table_schema}"
        )
    else:
        show_query = f"show iceberg tables like '{unquoted_table_name}'"

    rows = session.sql(show_query).collect()

    # there should be only one table in the result, otherwise something's wrong
    if len(rows) != 1:
        exception = AnalysisException(
            f"[TABLE_NOT_FOUND] Could not find Iceberg table '{table_name}'"
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception

    spec_id = rows[0]["current_partition_spec_id"]
    if spec_id is None:
        return None

    partition_specs = [
        spec
        for spec in json.loads(rows[0]["partition_specs"])
        if spec["spec-id"] == spec_id
    ]
    if not partition_specs:
        return None

    if len(partition_specs) != 1:
        exception = AnalysisException(
            f"[TABLE_NOT_FOUND] Could not find partition spec for Iceberg table '{table_name}'"
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception

    fields = [
        PartitionField(f["name"], f["transform"], f["source-id"])
        for f in partition_specs[0]["fields"]
    ]
    return PartitionSpec(fields)


def get_overwrite_condition(
    distinct_partitions_df: snowpark.DataFrame,
    partition_column_names: list[str],
) -> Column | None:
    """
    Produces a (snowpark) column that can be used as an overwrite_condition when writing data to a table.
    """
    distinct_partitions = distinct_partitions_df.collect()
    if not distinct_partitions:
        return None

    or_conditions = []
    for row in distinct_partitions:
        and_conditions = []
        for partition_col, value in zip(partition_column_names, row):
            sf_col_name = spark_to_sf_single_id(
                unquote_if_quoted(partition_col), is_column=True
            )
            # partition values can be NULL, so we need to compare them with equal_null
            and_conditions.append(equal_null(col(sf_col_name), lit(value)))
        if and_conditions:
            combined_and = functools.reduce(lambda a, b: a & b, and_conditions)
            or_conditions.append(combined_and)

    if or_conditions:
        combined_or = functools.reduce(lambda a, b: a | b, or_conditions)
        return combined_or

    # no partitions in the input data
    return None
