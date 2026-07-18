# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Core query functions for MotherDuck diagnostics.

Builds and executes SQL against QUERY_HISTORY, RECENT_QUERIES,
and md_active_server_connections().
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

import duckdb

from airbyte_ops_mcp.motherduck_diagnostics.connection import (
    execute_admin_query,
)
from airbyte_ops_mcp.motherduck_diagnostics.models import (
    MotherDuckActiveConnectionsResult,
    MotherDuckConnectionFilters,
    MotherDuckConnectionInfo,
    MotherDuckQueryFilters,
    MotherDuckQueryRecord,
    MotherDuckQueryResult,
    QueryTextTreatment,
)
from airbyte_ops_mcp.motherduck_diagnostics.text_processing import (
    apply_query_text_treatment,
    compute_query_hash,
    detect_query_subtype,
    extract_metadata,
)

logger = logging.getLogger(__name__)

_DEFAULT_TREATMENT = QueryTextTreatment()


def _str_or_empty(value: Any) -> str:
    """Coerce a possibly-null DuckDB value to a string, mapping `None` to `""`.

    `str(row.get(key, ""))` returns the literal `"None"` when the column is
    present but null; this maps such nulls to an empty string instead.
    """
    return "" if value is None else str(value)


def _interval_to_seconds(interval_value: Any) -> float | None:
    """Convert a DuckDB INTERVAL value to seconds."""
    if interval_value is None:
        return None
    try:
        td = interval_value
        if hasattr(td, "total_seconds"):
            return td.total_seconds()
        return float(td)
    except (TypeError, ValueError):
        return None


def _elapsed_since(start_time: Any) -> float | None:
    """Compute seconds elapsed since `start_time` (for running queries)."""
    if start_time is None:
        return None
    try:
        if isinstance(start_time, datetime):
            dt = (
                start_time
                if start_time.tzinfo
                else start_time.replace(tzinfo=timezone.utc)
            )
        else:
            dt = datetime.fromisoformat(str(start_time).replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
        return (datetime.now(tz=timezone.utc) - dt).total_seconds()
    except (TypeError, ValueError):
        return None


def _build_query_sql(
    filters: MotherDuckQueryFilters,
    *,
    realtime: bool,
    limit: int,
) -> tuple[str, list[Any]]:
    """Build the SQL query for QUERY_HISTORY or RECENT_QUERIES with filters."""
    view = (
        "MD_INFORMATION_SCHEMA.RECENT_QUERIES"
        if realtime
        else "MD_INFORMATION_SCHEMA.QUERY_HISTORY"
    )

    conditions: list[str] = []
    params: list[Any] = []

    if filters.user_name is not None:
        conditions.append("USER_NAME = ?")
        params.append(filters.user_name)

    if filters.min_start_time is not None:
        conditions.append("START_TIME >= ?::TIMESTAMPTZ")
        params.append(filters.min_start_time)
    elif not realtime:
        conditions.append("START_TIME >= NOW() - INTERVAL '24 hours'")

    if filters.max_start_time is not None:
        conditions.append("START_TIME <= ?::TIMESTAMPTZ")
        params.append(filters.max_start_time)

    if filters.error_only:
        conditions.append("ERROR_MESSAGE IS NOT NULL")

    if filters.min_execution_seconds is not None:
        conditions.append("EXECUTION_TIME >= ? * INTERVAL '1 second'")
        params.append(filters.min_execution_seconds)

    if filters.query_text_contains is not None:
        conditions.append("QUERY_TEXT ILIKE '%' || ? || '%'")
        params.append(filters.query_text_contains)

    if filters.query_text_pattern is not None:
        conditions.append("regexp_matches(QUERY_TEXT, ?)")
        params.append(filters.query_text_pattern)

    if filters.instance_type is not None:
        conditions.append("INSTANCE_TYPE = ?")
        params.append(filters.instance_type)

    if filters.query_connection_id is not None:
        conditions.append("CONNECTION_ID = ?::UUID")
        params.append(filters.query_connection_id)

    if filters.session_name_contains is not None:
        conditions.append("SESSION_NAME ILIKE '%' || ? || '%'")
        params.append(filters.session_name_contains)

    if filters.session_name_pattern is not None:
        conditions.append("regexp_matches(SESSION_NAME, ?)")
        params.append(filters.session_name_pattern)

    where_clause = ""
    if conditions:
        where_clause = " WHERE " + " AND ".join(conditions)

    sql = (
        f"SELECT * "
        f"FROM {view}{where_clause} "
        f"ORDER BY START_TIME DESC "
        f"LIMIT {int(limit)}"
    )
    return sql, params


def _process_query_row(
    row: dict[str, Any],
    *,
    include_text: bool,
    treatment: QueryTextTreatment,
) -> MotherDuckQueryRecord:
    """Transform a raw DuckDB row dict into a MotherDuckQueryRecord."""
    raw_text: str = row.get("QUERY_TEXT") or ""

    query_metadata = extract_metadata(raw_text) if raw_text else None
    query_hash = compute_query_hash(raw_text) if raw_text else None
    query_subtype = detect_query_subtype(raw_text) if raw_text else "UNKNOWN"

    query_text: str | None = None
    if include_text and raw_text:
        query_text = apply_query_text_treatment(
            raw_text,
            char_limit=treatment.char_limit,
            redact_strings=treatment.redact_string_constants,
        )

    return MotherDuckQueryRecord(
        query_id=_str_or_empty(row.get("QUERY_ID")),
        query_text=query_text,
        query_hash=query_hash,
        query_metadata=query_metadata,
        query_type=row.get("QUERY_TYPE"),
        query_subtype=query_subtype,
        start_time=_str_or_empty(row.get("START_TIME")),
        end_time=str(row["END_TIME"]) if row.get("END_TIME") is not None else None,
        is_running=row.get("END_TIME") is None,
        execution_time_seconds=_interval_to_seconds(row.get("EXECUTION_TIME")),
        wait_time_seconds=_interval_to_seconds(row.get("WAIT_TIME")),
        total_elapsed_seconds=(
            elapsed
            if (elapsed := _interval_to_seconds(row.get("TOTAL_ELAPSED_TIME")))
            is not None
            else (
                _elapsed_since(row.get("START_TIME"))
                if row.get("END_TIME") is None
                else None
            )
        ),
        error_message=row.get("ERROR_MESSAGE"),
        error_type=row.get("ERROR_TYPE"),
        user_name=_str_or_empty(row.get("USER_NAME")),
        instance_type=row.get("INSTANCE_TYPE"),
        duckling_id=row.get("DUCKLING_ID"),
        bytes_spilled_to_disk=row.get("BYTES_SPILLED_TO_DISK"),
        session_name=row.get("SESSION_NAME"),
        connection_id=str(row["CONNECTION_ID"])
        if row.get("CONNECTION_ID") is not None
        else None,
    )


def query_motherduck_queries(
    filters: MotherDuckQueryFilters,
    *,
    realtime: bool = False,
    limit: int = 100,
    include_query_text: bool | QueryTextTreatment = True,
) -> MotherDuckQueryResult:
    """Query MotherDuck QUERY_HISTORY or RECENT_QUERIES with structured filters.

    Args:
        filters: Structured filter criteria.
        realtime: If `True`, query RECENT_QUERIES; otherwise QUERY_HISTORY.
        limit: Maximum number of rows to return (1-1000).
        include_query_text: Controls query text inclusion. `False` omits entirely.
            `True` applies default treatment (1000 char limit, redact strings).
            A `QueryTextTreatment` instance provides fine-grained control.
    """
    limit = max(1, min(limit, 1000))

    if isinstance(include_query_text, QueryTextTreatment):
        treatment = include_query_text
        include_text = True
    elif include_query_text:
        treatment = _DEFAULT_TREATMENT
        include_text = True
    else:
        treatment = _DEFAULT_TREATMENT
        include_text = False

    sql, params = _build_query_sql(filters, realtime=realtime, limit=limit)
    logger.info("MotherDuck diagnostics SQL: %s", sql)

    try:
        rows = execute_admin_query(sql, params)
    except duckdb.Error as exc:
        logger.error("MotherDuck diagnostics query failed: %s", exc)
        raise RuntimeError(f"MotherDuck diagnostics query failed: {exc}") from exc

    records = [
        _process_query_row(row, include_text=include_text, treatment=treatment)
        for row in rows
    ]

    return MotherDuckQueryResult(
        mode="realtime" if realtime else "historical",
        returned=len(records),
        queries=records,
    )


def _build_connections_sql(
    filters: MotherDuckConnectionFilters,
) -> tuple[str, list[Any]]:
    """Build SQL for md_active_server_connections() with filters.

    Note: md_active_server_connections() does not expose dedicated user_name or
    session_name columns. All filters proxy through `client_user_agent` which
    typically contains the service account name and session metadata.
    """
    conditions: list[str] = []
    params: list[Any] = []

    base_sql = "SELECT * FROM md_active_server_connections()"

    if filters.user_name is not None:
        conditions.append("client_user_agent ILIKE '%' || ? || '%'")
        params.append(filters.user_name)

    if filters.session_name_contains is not None:
        conditions.append("client_user_agent ILIKE '%' || ? || '%'")
        params.append(filters.session_name_contains)

    if filters.session_name_pattern is not None:
        conditions.append("regexp_matches(client_user_agent, ?)")
        params.append(filters.session_name_pattern)

    if filters.min_age_minutes is not None:
        conditions.append("server_transaction_elapsed_time >= ? * INTERVAL '1 minute'")
        params.append(filters.min_age_minutes)

    where_clause = ""
    if conditions:
        where_clause = " WHERE " + " AND ".join(conditions)

    return f"{base_sql}{where_clause}", params


def query_active_connections(
    filters: MotherDuckConnectionFilters,
    *,
    include_query_text: bool | QueryTextTreatment = True,
) -> MotherDuckActiveConnectionsResult:
    """Query active MotherDuck server connections.

    Args:
        filters: Structured filter criteria for connections.
        include_query_text: Controls client_query text inclusion. `False` omits entirely.
            `True` applies default treatment (1000 char limit, redact string constants).
            Pass a `QueryTextTreatment` object for fine-grained control.
    """
    sql, params = _build_connections_sql(filters)
    logger.info("MotherDuck active connections SQL: %s", sql)

    if isinstance(include_query_text, QueryTextTreatment):
        treatment = include_query_text
        include_text = True
    elif include_query_text:
        treatment = _DEFAULT_TREATMENT
        include_text = True
    else:
        treatment = _DEFAULT_TREATMENT
        include_text = False

    try:
        rows = execute_admin_query(sql, params)
    except duckdb.Error as exc:
        logger.error("MotherDuck active connections query failed: %s", exc)
        raise RuntimeError(
            f"MotherDuck active connections query failed: {exc}"
        ) from exc

    connections = [
        _process_connection_row(row, include_text=include_text, treatment=treatment)
        for row in rows
    ]

    return MotherDuckActiveConnectionsResult(
        total_connections=len(connections),
        connections=connections,
    )


def _process_connection_row(
    row: dict[str, Any],
    *,
    include_text: bool,
    treatment: QueryTextTreatment,
) -> MotherDuckConnectionInfo:
    """Transform a raw DuckDB row dict into a MotherDuckConnectionInfo."""
    raw_query: str = row.get("client_query") or ""

    client_query_hash = compute_query_hash(raw_query) if raw_query else None
    client_query_metadata = extract_metadata(raw_query) if raw_query else None
    client_query_subtype = detect_query_subtype(raw_query) if raw_query else None

    client_query: str | None = None
    if include_text and raw_query:
        client_query = apply_query_text_treatment(
            raw_query,
            char_limit=treatment.char_limit,
            redact_strings=treatment.redact_string_constants,
        )

    return MotherDuckConnectionInfo(
        client_connection_id=_str_or_empty(row.get("client_connection_id")),
        client_duckdb_id=_str_or_empty(row.get("client_duckdb_id")),
        client_user_agent=row.get("client_user_agent"),
        client_duckdb_version=str(row.get("client_duckdb_version"))
        if row.get("client_duckdb_version")
        else None,
        server_transaction_stage=row.get("server_transaction_stage"),
        server_transaction_elapsed_time=(
            str(row["server_transaction_elapsed_time"])
            if row.get("server_transaction_elapsed_time") is not None
            else None
        ),
        client_query=client_query,
        client_query_hash=client_query_hash,
        client_query_metadata=client_query_metadata,
        client_query_subtype=client_query_subtype,
        server_query_elapsed_time=(
            str(row["server_query_elapsed_time"])
            if row.get("server_query_elapsed_time") is not None
            else None
        ),
        server_query_progress_pct=(
            round(row["server_query_progress"] * 100, 1)
            if row.get("server_query_progress") is not None
            else None
        ),
    )
