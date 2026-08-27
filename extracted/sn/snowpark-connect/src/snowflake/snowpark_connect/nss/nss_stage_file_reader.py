#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""Read path for the official ``STAGE_FILE_READER`` TVF (SNOW-3715057).

``STAGE_FILE_READER`` is a self-contained system table function that desugars to
``SELECT FROM @stage`` and produces the file's data columns directly — there is
**no per-schema decoder UDTF** and no ``udtf_fqn``. The Spark schema and reader
options travel in the ``OPTIONS`` JSON blob as ``DATA_SCHEMA`` / ``READER_OPTIONS``
(the backend derives ``READ_DATA_SCHEMA`` / ``SNOWFLAKE_TABLE_SCHEMA``).
"""

from snowflake import snowpark
from snowflake.snowpark import DataFrame
from snowflake.snowpark_connect.nss.nss_scan_options import (
    NssColumn,
    build_stage_file_reader_options,
    quote_options_literal,
    sql_quote_literal,
)
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger
from snowflake.snowpark_connect.utils.telemetry import telemetry


def nss_read_via_stage_file_reader(
    session: snowpark.Session,
    stage_path: str,
    file_format: str,
    columns: list[NssColumn],
    reader_options: dict | None = None,
    tvf_fqn: str = "STAGE_FILE_READER",
) -> DataFrame:
    """Read files via the official ``STAGE_FILE_READER`` TVF.

    Args:
        session: Active Snowpark session.
        stage_path: Stage path (unquoted, e.g. ``@DB.SCHEMA.STAGE/path``).
        file_format: FILE FORMAT name/FQN (passed as a string literal — the TVF
            resolves it through the same stage/format machinery as INFER_SCHEMA).
        columns: Target columns (given schema, or inferred via INFER_STAGE_FILE_SCHEMA)
            as :class:`NssColumn` — ``SPARK_DATA_TYPE`` is carried verbatim.
        reader_options: Spark ``DataFrameReader`` options, already filtered to the
            format's read-only allow-list by the caller.
        tvf_fqn: STAGE_FILE_READER function name (config-overridable).

    Returns:
        A Snowpark DataFrame over the TVF result (the file's data columns).
    """
    options_json = build_stage_file_reader_options(columns, reader_options)
    # Escape single quotes in the raw-interpolated literals so a path/format name
    # containing a ``'`` cannot break out of the SQL string. OPTIONS is wrapped by
    # quote_options_literal, which is safe even when the JSON payload contains ``$$``
    # (user column names / reader-option values can).
    sql = (
        f"SELECT * FROM TABLE({tvf_fqn}(\n"
        f"    LOCATION    => '{sql_quote_literal(stage_path)}',\n"
        f"    FILE_FORMAT => '{sql_quote_literal(file_format)}',\n"
        f"    OPTIONS     => {quote_options_literal(options_json)}\n"
        f"))"
    )
    # NSS read path (keyword kept out of the customer-visible log message)
    logger.info(f"STAGE_FILE_READER query: {sql}")
    telemetry.report_nss_tvf("STAGE_FILE_READER")
    return session.sql(sql)
