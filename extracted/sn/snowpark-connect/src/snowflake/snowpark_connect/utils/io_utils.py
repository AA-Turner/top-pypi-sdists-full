#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
import contextlib
import functools
import re

from snowflake.snowpark import Session
from snowflake.snowpark._internal.analyzer.analyzer_utils import (
    create_file_format_statement,
)
from snowflake.snowpark_connect.utils.identifiers import FQN

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
