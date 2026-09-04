#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""Spark ``SchemaUtils.checkColumnNameDuplication`` for file-read user schemas."""

from pyspark.errors.exceptions.base import AnalysisException

from snowflake.snowpark._internal.analyzer.analyzer_utils import unquote_if_quoted
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code


def check_read_schema_column_name_duplication(
    column_names: list[str],
    *,
    case_sensitive: bool,
) -> None:
    originals = [unquote_if_quoted(name) for name in column_names]
    folded = [name if case_sensitive else name.lower() for name in originals]
    counts: dict[str, int] = {}
    for name in folded:
        counts[name] = counts.get(name, 0) + 1
    duplicates = sorted(name for name, count in counts.items() if count > 1)
    if not duplicates:
        return
    offending = duplicates[0]
    exception = AnalysisException(
        f"[COLUMN_ALREADY_EXISTS] The column `{offending}` already exists. "
        "Consider to choose another name or rename the existing column."
    )
    attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
    raise exception
