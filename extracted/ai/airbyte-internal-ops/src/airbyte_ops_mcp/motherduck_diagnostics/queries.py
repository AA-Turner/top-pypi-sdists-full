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
    ComputeUsageGrain,
    MotherDuckActiveConnectionsResult,
    MotherDuckComputeSummaryResult,
    MotherDuckComputeUsageBucket,
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

# Aggregation grains supported by the compute-usage summary. Each maps to the
# `date_trunc` unit applied to `START_TIME`; the mapping is closed so the grain
# is never interpolated from arbitrary caller input.
_GRAIN_TRUNC_UNIT: dict[str, str] = {"hour": "hour", "day": "day"}

# Label used for rows whose native `QUERY_TYPE` is null/empty, so the compute
# split always has a stable key rather than dropping unclassified rows.
_UNKNOWN_QUERY_TYPE = "UNKNOWN"

# Failed queries with a null/empty native `ERROR_TYPE` are folded under this key
# so the per-bucket error-type split always has a stable bucket for classified
# failures that MotherDuck left untyped, rather than dropping them.
_UNKNOWN_ERROR_TYPE = "UNKNOWN"


def _str_or_empty(value: Any) -> str:
    """Coerce a possibly-null DuckDB value to a string, mapping `None` to `""`.

    `str(row.get(key, ""))` returns the literal `"None"` when the column is
    present but null; this maps such nulls to an empty string instead.
    """
    return "" if value is None else str(value)


def _iso_or_empty(value: Any) -> str:
    """Render a timestamp value as ISO8601, mapping `None` to `""`.

    DuckDB returns `date_trunc` results as `datetime` objects, whose `str()`
    is space-separated (`YYYY-MM-DD HH:MM:SS+00:00`). Callers expect ISO8601
    (`T`-separated), so normalize `datetime` values via `isoformat()` and fall
    back to `_str_or_empty` for anything already stringified.
    """
    if isinstance(value, datetime):
        return value.isoformat()
    return _str_or_empty(value)


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


def _query_view(realtime: bool) -> str:
    """Return the MD_INFORMATION_SCHEMA view name for the requested mode."""
    return (
        "MD_INFORMATION_SCHEMA.RECENT_QUERIES"
        if realtime
        else "MD_INFORMATION_SCHEMA.QUERY_HISTORY"
    )


def _build_query_conditions(
    filters: MotherDuckQueryFilters,
    *,
    realtime: bool,
) -> tuple[list[str], list[Any]]:
    """Build the shared WHERE conditions (and params) for the query views."""
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
        conditions.append("(ERROR_MESSAGE IS NOT NULL OR ERROR_TYPE IS NOT NULL)")

    if filters.min_execution_seconds is not None:
        conditions.append("EXECUTION_TIME >= ? * INTERVAL '1 second'")
        params.append(filters.min_execution_seconds)

    if filters.min_total_elapsed_seconds is not None:
        conditions.append("TOTAL_ELAPSED_TIME >= ? * INTERVAL '1 second'")
        params.append(filters.min_total_elapsed_seconds)

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

    return conditions, params


def _where_clause(conditions: list[str]) -> str:
    """Render a `WHERE ...` clause from conditions, or `""` when there are none."""
    if not conditions:
        return ""
    return " WHERE " + " AND ".join(conditions)


def _build_query_sql(
    filters: MotherDuckQueryFilters,
    *,
    realtime: bool,
    limit: int,
) -> tuple[str, list[Any]]:
    """Build the SQL query for QUERY_HISTORY or RECENT_QUERIES with filters."""
    conditions, params = _build_query_conditions(filters, realtime=realtime)
    sql = (
        f"SELECT * "
        f"FROM {_query_view(realtime)}{_where_clause(conditions)} "
        f"ORDER BY START_TIME DESC "
        f"LIMIT {int(limit)}"
    )
    return sql, params


def _build_compute_summary_sql(
    filters: MotherDuckQueryFilters,
    *,
    realtime: bool,
    grain: ComputeUsageGrain,
) -> tuple[str, list[Any]]:
    """Build the compute-usage aggregate SQL for QUERY_HISTORY / RECENT_QUERIES.

    Rolls the window up server-side with
    `GROUP BY date_trunc(<grain>, START_TIME), QUERY_TYPE, ERROR_TYPE` so the
    totals cover every matching query, not just a `LIMIT`-capped page. Compute is
    split by MotherDuck's native `QUERY_TYPE` and failures are split by native
    `ERROR_TYPE` (via a `CASE` that is `NULL` for succeeded rows so only failures
    contribute), both in the database rather than by grouping detailed rows in
    memory or running a per-row regex over the whole window. `grain` (`hour` or
    `day`) is resolved through a closed mapping, so it is never interpolated from
    arbitrary input. `epoch(...)` converts each `EXECUTION_TIME` interval
    (falling back to `TOTAL_ELAPSED_TIME`) to seconds before summing, since
    DuckDB has no `SUM(INTERVAL)` aggregate.
    """
    trunc_unit = _GRAIN_TRUNC_UNIT.get(grain)
    if trunc_unit is None:
        raise ValueError(
            f"Unsupported compute-usage grain {grain!r}; "
            f"expected one of {sorted(_GRAIN_TRUNC_UNIT)}."
        )
    conditions, params = _build_query_conditions(filters, realtime=realtime)
    # The error-type split expression is repeated verbatim in GROUP BY / ORDER BY
    # rather than referenced by its `error_type` alias: DuckDB identifiers are
    # case-insensitive, so a bare `error_type` in GROUP BY binds to the base
    # `ERROR_TYPE` column instead of this `CASE`, leaving its `ERROR_MESSAGE`
    # reference ungrouped (a binder error). `query_type`/`bucket_start` don't hit
    # this because their expressions only reference their own grouped column.
    error_type_expr = (
        "CASE WHEN ERROR_MESSAGE IS NOT NULL OR ERROR_TYPE IS NOT NULL "
        f"THEN COALESCE(NULLIF(ERROR_TYPE, ''), '{_UNKNOWN_ERROR_TYPE}') "
        "ELSE NULL END"
    )
    sql = (
        "SELECT "
        f"date_trunc('{trunc_unit}', START_TIME) AS bucket_start, "
        f"COALESCE(NULLIF(QUERY_TYPE, ''), '{_UNKNOWN_QUERY_TYPE}') AS query_type, "
        f"{error_type_expr} AS error_type, "
        "COALESCE(SUM(epoch(COALESCE(EXECUTION_TIME, TOTAL_ELAPSED_TIME))), 0) "
        "AS compute_seconds, "
        "COUNT(*) AS query_count, "
        "COUNT(*) FILTER ("
        "WHERE ERROR_MESSAGE IS NOT NULL OR ERROR_TYPE IS NOT NULL"
        ") AS failed_count "
        f"FROM {_query_view(realtime)}{_where_clause(conditions)} "
        f"GROUP BY bucket_start, query_type, {error_type_expr} "
        f"ORDER BY bucket_start, query_type, {error_type_expr}"
    )
    return sql, params


class _BucketAccumulator:
    """Mutable fold state for one time bucket, built into a typed model at the end.

    Keeps the per-bucket totals and per-query-type compute split in plain Python
    containers while folding the SQL `GROUP BY (bucket, query_type)` rows, so the
    immutable `MotherDuckComputeUsageBucket` is constructed once, fully-formed.
    """

    def __init__(self, *, bucket_start: str) -> None:
        self.bucket_start = bucket_start
        self.compute_seconds = 0.0
        self.query_count = 0
        self.failed_count = 0
        self.query_type_compute_seconds: dict[str, float] = {}
        self.error_type_counts: dict[str, int] = {}

    def add(
        self,
        query_type: str,
        error_type: str,
        compute_seconds: float,
        query_count: int,
        failed_count: int,
    ) -> None:
        """Accumulate one `(bucket, query_type, error_type)` group row.

        `error_type` is empty for succeeded groups; only failure groups (where it
        holds the native classification, `UNKNOWN` for untyped failures)
        contribute to the per-bucket error-type split, keyed by that value.
        """
        self.compute_seconds += compute_seconds
        self.query_count += query_count
        self.failed_count += failed_count
        self.query_type_compute_seconds[query_type] = (
            self.query_type_compute_seconds.get(query_type, 0.0) + compute_seconds
        )
        if error_type:
            self.error_type_counts[error_type] = (
                self.error_type_counts.get(error_type, 0) + failed_count
            )

    def to_bucket(self, grain: ComputeUsageGrain) -> MotherDuckComputeUsageBucket:
        """Build the immutable typed bucket, rounding compute-seconds to 2 dp."""
        return MotherDuckComputeUsageBucket(
            bucket_start=self.bucket_start,
            grain=grain,
            compute_seconds=round(self.compute_seconds, 2),
            query_count=self.query_count,
            failed_count=self.failed_count,
            query_type_compute_seconds={
                query_type: round(seconds, 2)
                for query_type, seconds in self.query_type_compute_seconds.items()
            },
            error_type_counts=dict(self.error_type_counts),
        )


def query_compute_usage_summary(
    filters: MotherDuckQueryFilters,
    *,
    realtime: bool = False,
    grain: ComputeUsageGrain = "hour",
) -> MotherDuckComputeSummaryResult:
    """Aggregate compute usage server-side over a query window, split by query type.

    Unlike `query_motherduck_queries`, this issues a `GROUP BY` rollup and never
    fetches detailed rows, so the totals and per-grain buckets reflect the whole
    window regardless of any row limit. Each bucket also carries a compute
    breakdown keyed by MotherDuck's native `QUERY_TYPE`, computed by the same SQL
    `GROUP BY` — no per-row regex classification runs over the window. Raw query
    text is never returned to the caller (though `query_text_*` filters, if set,
    still apply their `QUERY_TEXT` predicates server-side).

    Args:
        filters: Structured filter criteria (same window/user filters as the
            row query).
        realtime: If `True`, aggregate RECENT_QUERIES; otherwise QUERY_HISTORY.
        grain: Aggregation grain — `hour` for intraday windows, `day` for
            multi-day windows.
    """
    sql, params = _build_compute_summary_sql(filters, realtime=realtime, grain=grain)
    logger.info("MotherDuck compute-usage aggregate SQL: %s", sql)

    try:
        rows = execute_admin_query(sql, params)
    except duckdb.Error as exc:
        logger.error("MotherDuck compute-usage aggregate failed: %s", exc)
        raise RuntimeError(f"MotherDuck compute-usage aggregate failed: {exc}") from exc

    # Fold the (bucket, query_type) grouped rows into one accumulator per time
    # slice, then build the typed buckets once at the end. This aggregates
    # already-aggregated group rows (at most buckets x query types), never
    # detailed query rows, so the "aggregate in SQL, not in memory" guarantee
    # still holds.
    accumulators: dict[str, _BucketAccumulator] = {}
    total_compute = 0.0
    total_queries = 0
    total_failed = 0
    for raw_row in rows:
        row = {str(key).lower(): value for key, value in raw_row.items()}
        bucket_start = _iso_or_empty(row.get("bucket_start"))
        query_type = str(row.get("query_type") or _UNKNOWN_QUERY_TYPE)
        raw_error_type = row.get("error_type")
        error_type = str(raw_error_type) if raw_error_type not in (None, "") else ""
        compute_seconds = float(row.get("compute_seconds") or 0.0)
        query_count = int(row.get("query_count") or 0)
        failed_count = int(row.get("failed_count") or 0)

        acc = accumulators.get(bucket_start)
        if acc is None:
            acc = _BucketAccumulator(bucket_start=bucket_start)
            accumulators[bucket_start] = acc
        acc.add(query_type, error_type, compute_seconds, query_count, failed_count)

        total_compute += compute_seconds
        total_queries += query_count
        total_failed += failed_count

    return MotherDuckComputeSummaryResult(
        mode="realtime" if realtime else "historical",
        grain=grain,
        total_compute_seconds=round(total_compute, 2),
        total_query_count=total_queries,
        total_failed_count=total_failed,
        # Sort by the ISO8601 bucket key so the chronological ordering promised by
        # `MotherDuckComputeSummaryResult.buckets` holds independently of dict
        # insertion order or the SQL `ORDER BY`.
        buckets=[
            acc.to_bucket(grain)
            for _, acc in sorted(accumulators.items(), key=lambda item: item[0])
        ],
    )


def _process_query_row(
    row: dict[str, Any],
    *,
    include_text: bool,
    treatment: QueryTextTreatment,
) -> MotherDuckQueryRecord:
    """Transform a raw DuckDB row dict into a MotherDuckQueryRecord.

    MotherDuck's `MD_INFORMATION_SCHEMA` views return their column names in
    lower case (DuckDB resolves identifiers in the query SQL case-insensitively,
    but the fetched result keys preserve the stored lower case). Normalize the
    row keys to upper case so the field reads below match regardless of the
    case MotherDuck returns.
    """
    row = {str(key).upper(): value for key, value in row.items()}

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
    limit: int = 1000,
    include_query_text: bool | QueryTextTreatment = True,
) -> MotherDuckQueryResult:
    """Query MotherDuck QUERY_HISTORY or RECENT_QUERIES with structured filters.

    Args:
        filters: Structured filter criteria.
        realtime: If `True`, query RECENT_QUERIES; otherwise QUERY_HISTORY.
        limit: Maximum number of rows to return (minimum 1).
        include_query_text: Controls query text inclusion. `False` omits entirely.
            `True` applies default treatment (1000 char limit, redact strings).
            A `QueryTextTreatment` instance provides fine-grained control.
    """
    limit = max(1, limit)

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
