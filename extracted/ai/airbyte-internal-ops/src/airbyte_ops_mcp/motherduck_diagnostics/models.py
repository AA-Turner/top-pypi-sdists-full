# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Pydantic models for MotherDuck diagnostics tools."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class QueryTextTreatment(BaseModel):
    """Controls how QUERY_TEXT is processed before returning to the caller."""

    char_limit: int = Field(
        default=1000,
        gt=0,
        description="Truncate QUERY_TEXT to this many characters.",
    )
    redact_string_constants: bool = Field(
        default=True,
        description="Replace string literals in QUERY_TEXT with `?` placeholders.",
    )


class MotherDuckQueryFilters(BaseModel):
    """Structured filters for MotherDuck query searches."""

    user_name: str | None = Field(
        default=None,
        description="Service account filter (e.g. 'sonar_org_a1b2c3d4').",
    )
    min_start_time: str | None = Field(
        default=None,
        description=(
            "ISO8601 lower bound on START_TIME. In historical mode "
            "(QUERY_HISTORY) this defaults to the last 24h when omitted; in "
            "realtime mode (RECENT_QUERIES) no default lower bound is applied."
        ),
    )
    max_start_time: str | None = Field(
        default=None,
        description=(
            "ISO8601 upper bound on START_TIME. When omitted, no upper bound "
            "is applied (results extend through the most recent queries)."
        ),
    )
    error_only: bool = Field(
        default=False,
        description="If true, return only queries with a non-null ERROR_MESSAGE.",
    )
    min_execution_seconds: float | None = Field(
        default=None,
        ge=0,
        description="Minimum execution_time threshold (seconds).",
    )
    query_text_contains: str | None = Field(
        default=None,
        description="Case-insensitive substring match on QUERY_TEXT.",
    )
    query_text_pattern: str | None = Field(
        default=None,
        description="Regex pattern on QUERY_TEXT. DuckDB RE2 syntax.",
    )
    instance_type: str | None = Field(
        default=None,
        description="Filter by duckling size (Pulse/Standard/Jumbo/Mega/Giga).",
    )
    query_connection_id: str | None = Field(
        default=None,
        description="Filter by CONNECTION_ID UUID (bridge from active_connections tool).",
    )
    session_name_contains: str | None = Field(
        default=None,
        description="Substring match on SESSION_NAME (typically a workspace UUID).",
    )
    session_name_pattern: str | None = Field(
        default=None,
        description="Regex on SESSION_NAME. DuckDB RE2 syntax.",
    )


class MotherDuckQueryRecord(BaseModel):
    """A single query record from QUERY_HISTORY or RECENT_QUERIES."""

    query_id: str = Field(description="Unique query UUID.")
    query_text: str | None = Field(
        description="Processed SQL text (may be truncated/redacted), or None if omitted."
    )
    query_hash: str | None = Field(
        description="SHA-256 hex of normalized query (whitespace-trimmed, metadata stripped)."
    )
    query_metadata: dict[str, Any] | None = Field(
        description="Parsed JSON from leading /* {...} */ comment, if present."
    )
    query_type: str | None = Field(
        description="MotherDuck native QUERY_TYPE (DDL/DML/QUERY/...)."
    )
    query_subtype: str = Field(
        description="Regex-derived statement classification (SELECT/INSERT/COPY/.../UNKNOWN)."
    )
    start_time: str = Field(description="Query start timestamp.")
    end_time: str | None = Field(
        description="Query end timestamp (null if still running)."
    )
    is_running: bool = Field(
        description="Whether the query is still executing (derived from end_time being null)."
    )
    execution_time_seconds: float | None = Field(
        description="Active execution duration in seconds."
    )
    wait_time_seconds: float | None = Field(
        description="Time spent waiting on resources in seconds."
    )
    total_elapsed_seconds: float | None = Field(
        description="Total wall-clock duration in seconds."
    )
    error_message: str | None = Field(description="Error message if query failed.")
    error_type: str | None = Field(description="Error classification.")
    user_name: str = Field(description="MotherDuck user/service account identifier.")
    instance_type: str | None = Field(description="Duckling size that ran the query.")
    duckling_id: str | None = Field(
        description="Specific duckling identifier (user_rw, user_rs.0, etc)."
    )
    bytes_spilled_to_disk: int | None = Field(
        description="Bytes spilled for larger-than-memory workloads."
    )
    session_name: str | None = Field(
        description="Client session name if supplied at connect time."
    )
    connection_id: str | None = Field(description="Client connection UUID.")


class MotherDuckQueryResult(BaseModel):
    """Result of a MotherDuck query history/recent queries search."""

    mode: str = Field(
        description="'historical' or 'realtime' — which view was queried."
    )
    returned: int = Field(
        description=(
            "Number of rows returned (capped by `limit`). Narrow the filters or "
            "raise `limit` if you suspect there are more matching rows."
        )
    )
    queries: list[MotherDuckQueryRecord] = Field(description="Query records.")


class MotherDuckConnectionFilters(BaseModel):
    """Structured filters for active connection searches."""

    user_name: str | None = Field(
        default=None,
        description=(
            "Substring match on client_user_agent. "
            "md_active_server_connections() does not expose a dedicated user column; "
            "service account names are typically embedded in the user agent string."
        ),
    )
    session_name_contains: str | None = Field(
        default=None,
        description=(
            "Substring match on client_user_agent. "
            "md_active_server_connections() does not expose a session_name column; "
            "this filter proxies through client_user_agent."
        ),
    )
    session_name_pattern: str | None = Field(
        default=None,
        description=(
            "Regex on client_user_agent. DuckDB RE2 syntax. "
            "md_active_server_connections() does not expose a session_name column; "
            "this filter proxies through client_user_agent."
        ),
    )
    min_age_minutes: float | None = Field(
        default=None,
        ge=0,
        description=(
            "Minimum connection age in minutes. Filters on server_transaction_elapsed_time "
            "to find long-running connections (e.g. 60 for connections open 1+ hour)."
        ),
    )


class MotherDuckConnectionInfo(BaseModel):
    """A single active MotherDuck server connection."""

    client_connection_id: str = Field(description="Unique client connection UUID.")
    client_duckdb_id: str = Field(description="Unique client DuckDB instance UUID.")
    client_user_agent: str | None = Field(
        description="User agent string of the client."
    )
    client_duckdb_version: str | None = Field(description="Client DuckDB version.")
    server_transaction_stage: str | None = Field(
        description="Current server transaction stage."
    )
    server_transaction_elapsed_time: str | None = Field(
        description="How long in the current stage."
    )
    client_query: str | None = Field(
        description="Currently running SQL text (processed per QueryTextTreatment), or None if omitted."
    )
    client_query_hash: str | None = Field(
        description="SHA-256 hex of normalized client_query (whitespace-trimmed, metadata stripped)."
    )
    client_query_metadata: dict[str, Any] | None = Field(
        description="Parsed JSON from leading /* {...} */ comment in client_query, if present."
    )
    client_query_subtype: str | None = Field(
        description="Regex-derived statement classification of client_query (SELECT/INSERT/COPY/.../UNKNOWN)."
    )
    server_query_elapsed_time: str | None = Field(
        description="How long the query has been running."
    )
    server_query_progress_pct: float | None = Field(
        description="Query progress percent (from 0.0 to 100.0)."
    )


class MotherDuckActiveConnectionsResult(BaseModel):
    """Result of querying active MotherDuck server connections."""

    total_connections: int = Field(
        description="Total number of active connections matching filters."
    )
    connections: list[MotherDuckConnectionInfo] = Field(
        description="Active connection records."
    )
