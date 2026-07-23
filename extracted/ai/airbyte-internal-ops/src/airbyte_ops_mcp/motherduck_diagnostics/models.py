# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Pydantic models for MotherDuck diagnostics tools."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

ComputeUsageGrain = Literal["hour", "day"]
"""Aggregation grain for compute-usage rollups: `hour` or `day`."""


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
    min_total_elapsed_seconds: float | None = Field(
        default=None,
        ge=0,
        description="Minimum total_elapsed_time threshold (seconds).",
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
    database_name: str | None = Field(
        default=None,
        description=(
            "MotherDuck database (= Sonar source schema) the query ran against, "
            "derived from the `iceberg_scan('s3://.../data/<database_name>.db/...')` "
            "path in the raw query text. `QUERY_HISTORY` exposes no native "
            "database column, so this is parsed from the query text; `None` when "
            "no such path is present."
        ),
    )
    source_id: str | None = Field(
        default=None,
        description=(
            "Airbyte source UUID parsed deterministically from `database_name` "
            "(Sonar format `{env_prefix}{slug}__{source_id}`, underscores mapped "
            "back to hyphens). `None` when `database_name` is absent or its "
            "trailing segment is not a canonical UUID (fails closed)."
        ),
    )


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


class MotherDuckComputeUsageBucket(BaseModel):
    """Aggregated compute usage for a single time bucket, split by query type."""

    bucket_start: str = Field(
        description="ISO8601 start of the time bucket (UTC), e.g. `2026-07-15T18:00:00+00:00`."
    )
    grain: ComputeUsageGrain = Field(
        description="Aggregation grain of this bucket: `hour` or `day`.",
    )
    compute_seconds: float = Field(
        description="Sum of `EXECUTION_TIME` (falling back to `TOTAL_ELAPSED_TIME`) in seconds."
    )
    query_count: int = Field(description="Number of queries started in this bucket.")
    failed_count: int = Field(
        description="Number of queries in this bucket with a non-null error."
    )
    query_type_compute_seconds: dict[str, float] = Field(
        default_factory=dict,
        description=(
            "Compute-seconds within this bucket keyed by MotherDuck's native "
            "`QUERY_TYPE` (e.g. `DDL`, `DML`, `QUERY`, .../`UNKNOWN`). This is a "
            "coarse server-side category, distinct from the regex-derived "
            "statement `subtype` shown on the detailed query view."
        ),
    )
    error_type_counts: dict[str, int] = Field(
        default_factory=dict,
        description=(
            "Failed-query counts within this bucket keyed by MotherDuck's native "
            "`ERROR_TYPE` classification, computed by the same server-side "
            "`GROUP BY`. Failures with a null/empty `ERROR_TYPE` fold under "
            "`UNKNOWN`. Succeeded queries contribute nothing here, so the values "
            "sum to `failed_count`."
        ),
    )


class MotherDuckComputeSummaryResult(BaseModel):
    """Server-side aggregate rollup of query compute usage over a window.

    Computed with a SQL `GROUP BY date_trunc(<grain>, START_TIME), QUERY_TYPE`
    (grain is `hour` or `day`) so the totals reflect every matching query in the
    window, independent of any row limit, and the compute is split by MotherDuck's
    native `QUERY_TYPE` server-side rather than by grouping detailed rows in memory
    or evaluating a per-row regex classification over the whole window.
    """

    mode: str = Field(
        description="'historical' or 'realtime' — which view was aggregated."
    )
    grain: ComputeUsageGrain = Field(
        description="Aggregation grain applied to every bucket: `hour` or `day`.",
    )
    total_compute_seconds: float = Field(
        description="Total compute-seconds across the whole window."
    )
    total_query_count: int = Field(
        description="Total number of queries in the whole window."
    )
    total_failed_count: int = Field(
        description="Total number of failed queries in the whole window."
    )
    buckets: list[MotherDuckComputeUsageBucket] = Field(
        description="Compute-usage buckets at the requested grain, ordered chronologically."
    )


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
    database_name: str | None = Field(
        default=None,
        description=(
            "MotherDuck database (= Sonar source schema) the running query "
            "targets, derived from the `iceberg_scan('s3://...')` path in the "
            "raw client_query text. `None` when no such path is present."
        ),
    )
    source_id: str | None = Field(
        default=None,
        description=(
            "Airbyte source UUID parsed deterministically from `database_name` "
            "(underscores mapped back to hyphens). `None` when absent or the "
            "trailing segment is not a canonical UUID (fails closed)."
        ),
    )


class MotherDuckActiveConnectionsResult(BaseModel):
    """Result of querying active MotherDuck server connections."""

    total_connections: int = Field(
        description="Total number of active connections matching filters."
    )
    connections: list[MotherDuckConnectionInfo] = Field(
        description="Active connection records."
    )
