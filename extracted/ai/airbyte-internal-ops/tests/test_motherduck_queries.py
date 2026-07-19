# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for MotherDuck diagnostics SQL building and row processing.

These tests exercise the pure SQL-construction and row-shaping helpers, plus
the `query_motherduck_queries` / `query_active_connections` entry points with
`execute_admin_query` mocked so no live MotherDuck connection is required.
"""

from datetime import datetime, timedelta, timezone
from typing import Any

import pytest

from airbyte_ops_mcp.motherduck_diagnostics import queries as queries_mod
from airbyte_ops_mcp.motherduck_diagnostics.models import (
    MotherDuckConnectionFilters,
    MotherDuckQueryFilters,
    QueryTextTreatment,
)
from airbyte_ops_mcp.motherduck_diagnostics.queries import (
    _build_compute_summary_sql,
    _build_connections_sql,
    _build_query_sql,
    _process_connection_row,
    _process_query_row,
    query_active_connections,
    query_compute_usage_summary,
    query_motherduck_queries,
)


@pytest.mark.unit
def test_build_query_sql_historical_default_adds_24h_lower_bound() -> None:
    sql, params = _build_query_sql(MotherDuckQueryFilters(), realtime=False, limit=100)
    assert "MD_INFORMATION_SCHEMA.QUERY_HISTORY" in sql
    assert "START_TIME >= NOW() - INTERVAL '24 hours'" in sql
    assert "LIMIT 100" in sql
    assert params == []


@pytest.mark.unit
@pytest.mark.parametrize(
    ("requested", "expected"),
    [
        pytest.param(0, 1, id="floored_up_to_1"),
        pytest.param(-5, 1, id="negative_floored_to_1"),
        pytest.param(500, 500, id="passthrough"),
        pytest.param(50_000, 50_000, id="no_upper_cap"),
    ],
)
def test_query_motherduck_queries_floors_limit_at_1(
    monkeypatch: pytest.MonkeyPatch, requested: int, expected: int
) -> None:
    captured: dict[str, Any] = {}

    def fake_execute(sql: str, params: list[Any]) -> list[dict[str, Any]]:
        captured["sql"] = sql
        return []

    monkeypatch.setattr(queries_mod, "execute_admin_query", fake_execute)
    query_motherduck_queries(MotherDuckQueryFilters(), limit=requested)
    assert f"LIMIT {expected}" in captured["sql"]


@pytest.mark.unit
def test_build_query_sql_realtime_has_no_default_lower_bound() -> None:
    sql, params = _build_query_sql(MotherDuckQueryFilters(), realtime=True, limit=50)
    assert "MD_INFORMATION_SCHEMA.RECENT_QUERIES" in sql
    assert "24 hours" not in sql
    assert "WHERE" not in sql
    assert params == []


@pytest.mark.unit
def test_build_query_sql_all_filters_produce_conditions_and_params() -> None:
    filters = MotherDuckQueryFilters(
        user_name="sonar_org_a1b2c3d4",
        min_start_time="2026-01-01T00:00:00Z",
        max_start_time="2026-01-02T00:00:00Z",
        error_only=True,
        min_execution_seconds=1.5,
        min_total_elapsed_seconds=10.0,
        query_text_contains="select",
        query_text_pattern="^SELECT",
        instance_type="Standard",
        query_connection_id="11111111-1111-1111-1111-111111111111",
        session_name_contains="workspace",
        session_name_pattern="^ws-",
    )
    sql, params = _build_query_sql(filters, realtime=False, limit=10)

    assert "USER_NAME = ?" in sql
    assert "START_TIME >= ?::TIMESTAMPTZ" in sql
    assert "START_TIME <= ?::TIMESTAMPTZ" in sql
    # `error_only` treats a row as failed when either error field is set, so it
    # catches errored queries whose message is null but whose type is populated.
    assert "(ERROR_MESSAGE IS NOT NULL OR ERROR_TYPE IS NOT NULL)" in sql
    assert "EXECUTION_TIME >= ? * INTERVAL '1 second'" in sql
    # Slow / very-slow modality filters on wall-clock elapsed, not execution.
    assert "TOTAL_ELAPSED_TIME >= ? * INTERVAL '1 second'" in sql
    assert "QUERY_TEXT ILIKE '%' || ? || '%'" in sql
    assert "regexp_matches(QUERY_TEXT, ?)" in sql
    assert "INSTANCE_TYPE = ?" in sql
    assert "CONNECTION_ID = ?::UUID" in sql
    assert "SESSION_NAME ILIKE '%' || ? || '%'" in sql
    assert "regexp_matches(SESSION_NAME, ?)" in sql
    # An explicit min_start_time suppresses the 24h default.
    assert "24 hours" not in sql
    assert params == [
        "sonar_org_a1b2c3d4",
        "2026-01-01T00:00:00Z",
        "2026-01-02T00:00:00Z",
        1.5,
        10.0,
        "select",
        "^SELECT",
        "Standard",
        "11111111-1111-1111-1111-111111111111",
        "workspace",
        "^ws-",
    ]


@pytest.mark.unit
def test_build_connections_sql_no_filters() -> None:
    sql, params = _build_connections_sql(MotherDuckConnectionFilters())
    assert sql == "SELECT * FROM md_active_server_connections()"
    assert params == []


@pytest.mark.unit
def test_build_connections_sql_all_filters_proxy_through_user_agent() -> None:
    filters = MotherDuckConnectionFilters(
        user_name="sonar",
        session_name_contains="ws",
        session_name_pattern="^ws-",
        min_age_minutes=60,
    )
    sql, params = _build_connections_sql(filters)
    assert sql.count("client_user_agent ILIKE '%' || ? || '%'") == 2
    assert "regexp_matches(client_user_agent, ?)" in sql
    assert "server_transaction_elapsed_time >= ? * INTERVAL '1 minute'" in sql
    assert params == ["sonar", "ws", "^ws-", 60]


@pytest.mark.unit
def test_process_query_row_completed_query() -> None:
    row: dict[str, Any] = {
        "QUERY_ID": "q-1",
        "QUERY_TEXT": '/* {"app": "sonar"} */ SELECT * FROM t WHERE name = \'AJ\'',
        "QUERY_TYPE": "QUERY",
        "START_TIME": "2026-01-01T00:00:00Z",
        "END_TIME": "2026-01-01T00:00:01Z",
        "EXECUTION_TIME": timedelta(seconds=2),
        "WAIT_TIME": timedelta(0),
        "TOTAL_ELAPSED_TIME": timedelta(seconds=3),
        "USER_NAME": "sonar_org_a1b2c3d4",
        "CONNECTION_ID": "c-1",
    }
    record = _process_query_row(row, include_text=True, treatment=QueryTextTreatment())
    assert record.query_id == "q-1"
    assert record.query_metadata == {"app": "sonar"}
    assert record.query_subtype == "SELECT"
    assert record.is_running is False
    assert record.execution_time_seconds == 2.0
    assert record.wait_time_seconds == 0.0  # zero preserved, not dropped
    assert record.total_elapsed_seconds == 3.0
    # String constant redacted; metadata comment stripped.
    assert record.query_text is not None
    assert "AJ" not in record.query_text
    assert record.connection_id == "c-1"


@pytest.mark.unit
def test_process_query_row_reads_lowercase_columns() -> None:
    """MotherDuck's `MD_INFORMATION_SCHEMA` views return lower-case column keys.

    The row reads must be case-insensitive, otherwise every field comes back
    empty (blank hash/user/start, `UNKNOWN` subtype, zero elapsed).
    """
    row: dict[str, Any] = {
        "query_id": "q-lower",
        "query_text": "SELECT * FROM t",
        "query_type": "QUERY",
        "start_time": "2026-01-01T00:00:00Z",
        "end_time": "2026-01-01T00:00:02Z",
        "execution_time": timedelta(seconds=2),
        "total_elapsed_time": timedelta(seconds=3),
        "user_name": "sonar_org_a1b2c3d4",
        "connection_id": "c-lower",
    }
    record = _process_query_row(row, include_text=False, treatment=QueryTextTreatment())
    assert record.query_id == "q-lower"
    assert record.query_subtype == "SELECT"
    assert record.query_hash is not None
    assert record.start_time == "2026-01-01T00:00:00Z"
    assert record.execution_time_seconds == 2.0
    assert record.total_elapsed_seconds == 3.0
    assert record.user_name == "sonar_org_a1b2c3d4"
    assert record.connection_id == "c-lower"


@pytest.mark.unit
def test_process_query_row_running_query_uses_elapsed_since() -> None:
    start = datetime.now(tz=timezone.utc) - timedelta(seconds=5)
    row: dict[str, Any] = {
        "QUERY_ID": "q-2",
        "QUERY_TEXT": "COPY t TO 's3://bucket/f'",
        "START_TIME": start,
        "END_TIME": None,
        "TOTAL_ELAPSED_TIME": None,
        "USER_NAME": "svc",
    }
    record = _process_query_row(row, include_text=False, treatment=QueryTextTreatment())
    assert record.is_running is True
    assert record.query_text is None  # include_text=False omits text
    assert record.query_subtype == "COPY"
    assert record.total_elapsed_seconds is not None
    assert record.total_elapsed_seconds >= 5.0


@pytest.mark.unit
def test_process_query_row_running_query_parses_z_suffixed_start_time() -> None:
    start = datetime.now(tz=timezone.utc) - timedelta(seconds=7)
    row: dict[str, Any] = {
        "QUERY_ID": "q-3",
        "QUERY_TEXT": "SELECT 1",
        "START_TIME": start.isoformat().replace("+00:00", "Z"),
        "END_TIME": None,
        "TOTAL_ELAPSED_TIME": None,
        "USER_NAME": "svc",
    }
    record = _process_query_row(row, include_text=False, treatment=QueryTextTreatment())
    assert record.is_running is True
    # Z-suffixed timestamp must parse rather than falling back to None.
    assert record.total_elapsed_seconds is not None
    assert record.total_elapsed_seconds >= 7.0


@pytest.mark.unit
def test_process_query_row_null_columns_become_empty_not_literal_none() -> None:
    row: dict[str, Any] = {
        "QUERY_ID": None,
        "QUERY_TEXT": "SELECT 1",
        "START_TIME": None,
        "END_TIME": None,
        "USER_NAME": None,
    }
    record = _process_query_row(row, include_text=False, treatment=QueryTextTreatment())
    assert record.query_id == ""
    assert record.start_time == ""
    assert record.user_name == ""


@pytest.mark.unit
def test_process_connection_row_null_ids_become_empty_not_literal_none() -> None:
    row: dict[str, Any] = {
        "client_connection_id": None,
        "client_duckdb_id": None,
        "client_query": None,
    }
    info = _process_connection_row(
        row, include_text=False, treatment=QueryTextTreatment()
    )
    assert info.client_connection_id == ""
    assert info.client_duckdb_id == ""


@pytest.mark.unit
def test_process_connection_row_zero_progress_preserved() -> None:
    row: dict[str, Any] = {
        "client_connection_id": "cc-1",
        "client_duckdb_id": "cd-1",
        "client_user_agent": "sonar/1.0",
        "client_query": "SELECT 1",
        "server_transaction_elapsed_time": timedelta(0),
        "server_query_elapsed_time": timedelta(0),
        "server_query_progress": 0.0,
    }
    info = _process_connection_row(
        row, include_text=True, treatment=QueryTextTreatment()
    )
    assert info.client_connection_id == "cc-1"
    assert info.client_query_subtype == "SELECT"
    # Zero durations/progress are preserved (not coerced to None).
    assert info.server_transaction_elapsed_time is not None
    assert info.server_query_elapsed_time is not None
    assert info.server_query_progress_pct == 0.0


@pytest.mark.unit
def test_query_motherduck_queries_mocked(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, Any] = {}

    def fake_execute(sql: str, params: list[Any]) -> list[dict[str, Any]]:
        captured["sql"] = sql
        captured["params"] = params
        return [
            {
                "QUERY_ID": "q-1",
                "QUERY_TEXT": "SELECT 1",
                "START_TIME": "2026-01-01T00:00:00Z",
                "END_TIME": "2026-01-01T00:00:01Z",
                "USER_NAME": "svc",
            }
        ]

    monkeypatch.setattr(queries_mod, "execute_admin_query", fake_execute)

    result = query_motherduck_queries(MotherDuckQueryFilters(), limit=5)
    assert result.mode == "historical"
    assert result.returned == 1
    assert result.queries[0].query_id == "q-1"
    assert "LIMIT 5" in captured["sql"]


@pytest.mark.unit
@pytest.mark.parametrize(
    "grain,trunc_unit",
    [
        pytest.param("hour", "hour", id="hourly_grain"),
        pytest.param("day", "day", id="daily_grain"),
    ],
)
def test_build_compute_summary_sql_aggregates_by_grain_no_limit(
    grain: str, trunc_unit: str
) -> None:
    sql, params = _build_compute_summary_sql(
        MotherDuckQueryFilters(), realtime=False, grain=grain
    )
    assert f"date_trunc('{trunc_unit}', START_TIME) AS bucket_start" in sql
    assert "SUM(epoch(COALESCE(EXECUTION_TIME, TOTAL_ELAPSED_TIME)))" in sql
    assert "COUNT(*) AS query_count" in sql
    assert "FILTER (WHERE ERROR_MESSAGE IS NOT NULL OR ERROR_TYPE IS NOT NULL)" in sql
    # The compute split groups by MotherDuck's native QUERY_TYPE in SQL — no
    # per-row regex classification over the window, no detailed-row fetch.
    assert "QUERY_TYPE" in sql
    assert "AS query_type" in sql
    # Failures are additionally split by native ERROR_TYPE in SQL (NULL for
    # succeeded rows via the CASE guard), so the trend never over-fetches rows.
    assert "AS error_type" in sql
    assert "ERROR_TYPE" in sql
    # The error-type CASE is repeated verbatim in GROUP BY (not referenced by its
    # alias): a bare `error_type` binds to the base column, leaving ERROR_MESSAGE
    # ungrouped and raising a DuckDB binder error.
    error_type_expr = (
        "CASE WHEN ERROR_MESSAGE IS NOT NULL OR ERROR_TYPE IS NOT NULL "
        "THEN COALESCE(NULLIF(ERROR_TYPE, ''), 'UNKNOWN') "
        "ELSE NULL END"
    )
    assert f"GROUP BY bucket_start, query_type, {error_type_expr}" in sql
    assert "GROUP BY bucket_start, query_type, error_type " not in sql
    # The aggregate must never fetch a capped page of detailed rows.
    assert "LIMIT" not in sql
    # Historical mode still applies the default 24h lower bound.
    assert "START_TIME >= NOW() - INTERVAL '24 hours'" in sql
    assert params == []


@pytest.mark.unit
def test_query_compute_usage_summary_mocked(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_execute(sql: str, params: list[Any]) -> list[dict[str, Any]]:
        # MotherDuck returns lower-case result keys; one row per (bucket, query_type).
        return [
            {
                "bucket_start": "2026-01-01T00:00:00+00:00",
                "query_type": "QUERY",
                "compute_seconds": 10.0,
                "query_count": 3,
                "failed_count": 1,
            },
            {
                "bucket_start": "2026-01-01T00:00:00+00:00",
                "query_type": "DML",
                "compute_seconds": 2.5,
                "query_count": 1,
                "failed_count": 0,
            },
            {
                "bucket_start": "2026-01-01T01:00:00+00:00",
                "query_type": "QUERY",
                "compute_seconds": 7.5,
                "query_count": 2,
                "failed_count": 0,
            },
        ]

    monkeypatch.setattr(queries_mod, "execute_admin_query", fake_execute)

    result = query_compute_usage_summary(MotherDuckQueryFilters())
    assert result.mode == "historical"
    assert result.grain == "hour"
    assert result.total_compute_seconds == 20.0
    assert result.total_query_count == 6
    assert result.total_failed_count == 1
    # Two (bucket, query_type) rows collapse into a single 00:00 bucket.
    assert len(result.buckets) == 2
    first = result.buckets[0]
    assert first.bucket_start == "2026-01-01T00:00:00+00:00"
    assert first.grain == "hour"
    assert first.compute_seconds == 12.5
    assert first.query_count == 4
    assert first.failed_count == 1
    assert first.query_type_compute_seconds == {"QUERY": 10.0, "DML": 2.5}


@pytest.mark.unit
def test_query_compute_usage_summary_daily_grain(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, str] = {}

    def fake_execute(sql: str, params: list[Any]) -> list[dict[str, Any]]:
        captured["sql"] = sql
        return [
            {
                "bucket_start": "2026-01-01T00:00:00+00:00",
                "query_type": "QUERY",
                "compute_seconds": 5.0,
                "query_count": 2,
                "failed_count": 0,
            }
        ]

    monkeypatch.setattr(queries_mod, "execute_admin_query", fake_execute)

    result = query_compute_usage_summary(MotherDuckQueryFilters(), grain="day")
    assert "date_trunc('day', START_TIME)" in captured["sql"]
    assert result.grain == "day"
    assert result.buckets[0].grain == "day"


@pytest.mark.unit
def test_query_compute_usage_summary_folds_error_type_counts(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_execute(sql: str, params: list[Any]) -> list[dict[str, Any]]:
        # One (bucket, query_type, error_type) group per row. Succeeded groups
        # carry a NULL error_type; failure groups carry the native classification
        # (UNKNOWN when MotherDuck left an errored query untyped).
        return [
            {
                "bucket_start": "2026-01-01T00:00:00+00:00",
                "query_type": "QUERY",
                "error_type": None,
                "compute_seconds": 8.0,
                "query_count": 5,
                "failed_count": 0,
            },
            {
                "bucket_start": "2026-01-01T00:00:00+00:00",
                "query_type": "QUERY",
                "error_type": "OutOfMemory",
                "compute_seconds": 2.0,
                "query_count": 2,
                "failed_count": 2,
            },
            {
                "bucket_start": "2026-01-01T00:00:00+00:00",
                "query_type": "DML",
                "error_type": "UNKNOWN",
                "compute_seconds": 1.0,
                "query_count": 1,
                "failed_count": 1,
            },
        ]

    monkeypatch.setattr(queries_mod, "execute_admin_query", fake_execute)

    result = query_compute_usage_summary(MotherDuckQueryFilters())
    (bucket,) = result.buckets
    assert bucket.failed_count == 3
    # Only failure groups contribute; the NULL-error succeeded group does not.
    assert bucket.error_type_counts == {"OutOfMemory": 2, "UNKNOWN": 1}
    # The split sums back to the bucket's total failures.
    assert sum(bucket.error_type_counts.values()) == bucket.failed_count


@pytest.mark.unit
@pytest.mark.parametrize("grain", ["hour", "day"], ids=["hourly", "daily"])
def test_build_compute_summary_sql_executes_against_duckdb(grain: str) -> None:
    """Execute the summary SQL against real DuckDB to catch binder errors.

    The mocked tests bypass the database, so they cannot catch SQL that fails to
    bind. DuckDB is the MotherDuck engine and its identifiers are
    case-insensitive, so grouping by a bare `error_type` alias silently binds to
    the base `ERROR_TYPE` column and leaves the `CASE`'s `ERROR_MESSAGE`
    reference ungrouped — a binder error that only surfaces at execution time.
    """
    duckdb = pytest.importorskip("duckdb")
    con = duckdb.connect()
    con.execute("CREATE SCHEMA MD_INFORMATION_SCHEMA")
    con.execute(
        "CREATE TABLE MD_INFORMATION_SCHEMA.QUERY_HISTORY ("
        "START_TIME TIMESTAMP, QUERY_TYPE VARCHAR, ERROR_TYPE VARCHAR, "
        "ERROR_MESSAGE VARCHAR, EXECUTION_TIME INTERVAL, TOTAL_ELAPSED_TIME INTERVAL)"
    )
    con.execute(
        "INSERT INTO MD_INFORMATION_SCHEMA.QUERY_HISTORY VALUES "
        "(NOW() - INTERVAL 30 MINUTE, 'QUERY', NULL, NULL, "
        "INTERVAL 1500 MILLISECOND, INTERVAL 2 SECOND), "
        "(NOW() - INTERVAL 25 MINUTE, 'QUERY', 'OutOfMemory', 'OOM', "
        "INTERVAL 500 MILLISECOND, INTERVAL 600 MILLISECOND), "
        "(NOW() - INTERVAL 20 MINUTE, 'DML', NULL, 'boom', "
        "INTERVAL 200 MILLISECOND, INTERVAL 300 MILLISECOND)"
    )

    sql, params = _build_compute_summary_sql(
        MotherDuckQueryFilters(), realtime=False, grain=grain
    )
    rows = con.execute(sql, params).fetchall()
    columns = [descriptor[0] for descriptor in con.description]
    records = [dict(zip(columns, row, strict=True)) for row in rows]

    # Succeeded rows carry a NULL error_type and never count as failures.
    succeeded = [r for r in records if r["error_type"] is None]
    assert succeeded and all(r["failed_count"] == 0 for r in succeeded)
    # Failures are split by native ERROR_TYPE; a null classification folds to
    # UNKNOWN. Each failure group contributes exactly its failed rows.
    failures = {
        r["error_type"]: r["failed_count"]
        for r in records
        if r["error_type"] is not None
    }
    assert failures == {"OutOfMemory": 1, "UNKNOWN": 1}
    assert sum(r["failed_count"] for r in records) == 2


@pytest.mark.unit
def test_query_compute_usage_summary_normalizes_datetime_bucket_to_iso(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # DuckDB returns `date_trunc` as a datetime; the model advertises ISO8601,
    # so a space-separated `str(datetime)` would violate the contract.
    def fake_execute(sql: str, params: list[Any]) -> list[dict[str, Any]]:
        return [
            {
                "bucket_start": datetime(2026, 1, 1, 0, 0, tzinfo=timezone.utc),
                "query_type": "QUERY",
                "compute_seconds": 1.0,
                "query_count": 1,
                "failed_count": 0,
            }
        ]

    monkeypatch.setattr(queries_mod, "execute_admin_query", fake_execute)

    result = query_compute_usage_summary(MotherDuckQueryFilters())
    assert result.buckets[0].bucket_start == "2026-01-01T00:00:00+00:00"


@pytest.mark.unit
def test_query_active_connections_mocked(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_execute(sql: str, params: list[Any]) -> list[dict[str, Any]]:
        return [
            {
                "client_connection_id": "cc-1",
                "client_duckdb_id": "cd-1",
                "client_query": "SELECT 1",
            }
        ]

    monkeypatch.setattr(queries_mod, "execute_admin_query", fake_execute)

    result = query_active_connections(MotherDuckConnectionFilters())
    assert result.total_connections == 1
    assert result.connections[0].client_connection_id == "cc-1"
