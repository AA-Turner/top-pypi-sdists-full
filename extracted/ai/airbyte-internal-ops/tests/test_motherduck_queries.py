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
    _build_connections_sql,
    _build_query_sql,
    _process_connection_row,
    _process_query_row,
    query_active_connections,
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
    assert "ERROR_MESSAGE IS NOT NULL" in sql
    assert "EXECUTION_TIME >= ? * INTERVAL '1 second'" in sql
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
