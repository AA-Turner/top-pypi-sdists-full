#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

#
# Copyright (c) 2012-2026 Snowflake Computing Inc. All rights reserved.
#

"""
GAP-021: Iceberg ``create_changelog_view`` procedure translation.

Translates a parsed ``create_changelog_view`` CallStatement into
``CALL SYSTEM$CREATE_ICEBERG_CHANGELOG_VIEW(...)`` on Snowflake.
All carry-over removal, update detection, and view creation logic
is platform-side — SCOS is purely a syntax translator.

The CALL is parsed by the Iceberg Spark SQL extension parser into a
``CallStatement`` plan node, which ``map_sql.py`` dispatches here via
the ``case "CallStatement"`` handler.
"""

from __future__ import annotations

from dataclasses import dataclass

import snowflake.snowpark as snowpark
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger


@dataclass
class CreateChangelogViewMatch:
    """Parsed parameters from a ``create_changelog_view`` CallStatement."""

    table: str
    changelog_view: str | None = None
    start_snapshot_id: str | None = None
    end_snapshot_id: str | None = None
    start_timestamp: str | None = None
    end_timestamp: str | None = None
    compute_updates: bool | None = None  # None = not explicitly set
    identifier_columns: list[str] | None = None
    net_changes: bool = False


def translate_create_changelog_view(
    match: CreateChangelogViewMatch, session: snowpark.Session
) -> None:
    """Translate to CALL SYSTEM$CREATE_ICEBERG_CHANGELOG_VIEW on Snowflake.

    SCOS is purely a syntax translator.  The platform procedure handles
    parameter validation, carry-over removal, view creation, and all other
    logic.

    All args are passed as string literals (quoted).  SYSTEM$ functions use
    SqlFunctionArgumentAccessorImpl.getArg() which throws "inputs may not be
    null" on SQL NULL for ANY parameter type (SNOW-3484889).  The established
    workaround (cf. AiCreateListingFromShare.java:87) is to pass '' for
    absent optional params; the GS side normalizes blanks to Optional.empty().
    Booleans are passed as 'true'/'false' strings — the GS side parses them
    with equalsIgnoreCase("true").

    Procedure signature (all args are VARCHAR string literals):
      1. TABLE_NAME          VARCHAR  (required)
      2. VIEW_NAME           VARCHAR  ('' = default <table>_changes)
      3. START_SNAPSHOT_ID   VARCHAR  ('' = full history)
      4. END_SNAPSHOT_ID     VARCHAR  ('' = current)
      5. START_TIMESTAMP_MS  VARCHAR  ('' = unused)
      6. END_TIMESTAMP_MS    VARCHAR  ('' = unused)
      7. COMPUTE_UPDATES     VARCHAR  ('true'/'false')
      8. IDENTIFIER_COLUMNS  VARCHAR  ('' = read from table PK)
      9. NET_CHANGES         VARCHAR  ('true'/'false')
    """

    def _esc(s: str) -> str:
        return s.replace("'", "''")

    table_fqn = _esc(match.table)
    view_name = match.changelog_view
    if not view_name:
        table_parts = match.table.rsplit(".", 1)
        view_name = f"{table_parts[-1]}_changes"
    # Uppercase the view name so the double-quoted DDL from the GS procedure
    # matches Snowflake's default case-insensitive resolution.  Without this,
    # the GS creates "cv_name" (lowercase, case-sensitive) but unquoted queries
    # resolve to CV_NAME → not found.
    view_name = _esc(view_name).upper()

    start_snap = _esc(match.start_snapshot_id or "")
    end_snap = _esc(match.end_snapshot_id or "")
    start_ts = _esc(match.start_timestamp or "")
    end_ts = _esc(match.end_timestamp or "")

    # compute_updates defaults to true when identifier_columns is explicitly
    # provided (matches Spark behaviour).
    compute_updates = match.compute_updates
    if compute_updates is None:
        compute_updates = match.identifier_columns is not None
    compute_updates_str = "true" if compute_updates else "false"
    net_changes_str = "true" if match.net_changes else "false"

    if match.identifier_columns:
        id_cols_str = ",".join(c.replace("'", "''") for c in match.identifier_columns)
    else:
        id_cols_str = ""

    # Use SELECT (not CALL) — CALL through Snowpark returns empty, but
    # SELECT SYSTEM$...() returns the JSON response as a scalar result.
    select_sql = (
        f"SELECT SYSTEM$CREATE_ICEBERG_CHANGELOG_VIEW("
        f"'{table_fqn}', '{view_name}', "
        f"'{start_snap}', '{end_snap}', '{start_ts}', '{end_ts}', "
        f"'{compute_updates_str}', '{id_cols_str}', '{net_changes_str}')"
    )

    logger.debug(
        "create_changelog_view: table=%s view=%s sql=%s",
        match.table,
        match.changelog_view or view_name,
        select_sql,
    )

    # SYSTEM$ functions cannot execute DDL directly — the procedure returns
    # a JSON response containing the DDL to execute.  Parse the response
    # and execute the CREATE TEMPORARY VIEW statement.
    import json

    rows = session.sql(select_sql).collect()
    response_str = str(rows[0][0]) if rows and rows[0] else ""
    if not response_str:
        raise RuntimeError(
            "SYSTEM$CREATE_ICEBERG_CHANGELOG_VIEW returned empty response"
        )

    response = json.loads(response_str)
    ddl = response.get("ddl", "")
    ddl_executed = response.get("ddlExecuted", False)

    if not ddl_executed and ddl:
        logger.debug("create_changelog_view: executing DDL: %s", ddl)
        session.sql(ddl).collect()
    elif not ddl:
        raise RuntimeError(
            f"SYSTEM$CREATE_ICEBERG_CHANGELOG_VIEW returned no DDL: {response_str}"
        )
