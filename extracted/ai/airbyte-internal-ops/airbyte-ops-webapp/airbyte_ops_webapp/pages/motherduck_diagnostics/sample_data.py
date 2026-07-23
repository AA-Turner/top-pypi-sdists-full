"""Sample MotherDuck diagnostics data used when the app runs in mock-only mode.

When `AIRBYTE_OPS_WEBAPP_MOCKONLY` is set the page renders these rows instead of
querying live MotherDuck (which needs an org-admin `MOTHERDUCK_ADMIN_TOKEN`),
mirroring the mock-mode behavior of the other Ops Webapp pages.

No raw SQL (`query_text` / `client_query`) appears here. Queries are identified
by a short `query_hash` prefix, their native `query_type`, and their
regex-derived `query_subtype`. The `query_text_treated` field holds only the
redacted/truncated form (string literals already replaced with `?`) that the
detail modal is allowed to surface — never verbatim SQL.
"""

from __future__ import annotations

from typing import TypedDict

from airbyte_ops_mcp.motherduck_diagnostics.models import (
    MotherDuckComputeUsageBucket,
)


class QueryRow(TypedDict):
    """A privacy-safe projection of a `MotherDuckQueryRecord`.

    `database_name` is the MotherDuck database (= Sonar source schema) the query
    ran against and `source_id` is the Airbyte source UUID parsed from it; both
    are safe identifiers. `database_name` is `""` only when the query has no
    `iceberg_scan` S3 path. `source_id` is `""` when `database_name` is absent
    *or* present but its trailing segment is not a canonical UUID, so a
    `database_name` can be populated while `source_id` is `""`.
    """

    query_hash: str
    query_type: str
    query_subtype: str
    user_name: str
    start_time: str
    total_elapsed_seconds: float
    execution_seconds: float
    wait_seconds: float
    succeeded: bool
    error_type: str
    error_message: str
    query_text_treated: str
    database_name: str
    source_id: str


class ConnectionRow(TypedDict):
    """A privacy-safe projection of a `MotherDuckConnectionInfo`."""

    client_connection_id: str
    client_user_agent: str
    server_transaction_stage: str
    server_query_elapsed_time: str
    database_name: str
    source_id: str


# Error types the mock distributes failures across, so the stacked "Failed
# queries" chart shows multiple series in mock mode.
_SAMPLE_ERROR_TYPES: tuple[str, ...] = (
    "OutOfMemory",
    "QueryTimeout",
    "PermissionDenied",
    "Connection",
)


def _split_failures(failed: int) -> dict[str, int]:
    """Spread a bucket's failed count across sample error types round-robin."""
    counts: dict[str, int] = {}
    for index in range(max(failed, 0)):
        error_type = _SAMPLE_ERROR_TYPES[index % len(_SAMPLE_ERROR_TYPES)]
        counts[error_type] = counts.get(error_type, 0) + 1
    return counts


def _bucket(
    bucket_start: str,
    grain: str,
    query: float,
    dml: float,
    ddl: float,
    failed: int,
    query_count: int,
) -> MotherDuckComputeUsageBucket:
    """Build a sample aggregate compute bucket split by native query type."""
    return MotherDuckComputeUsageBucket(
        bucket_start=bucket_start,
        grain=grain,
        compute_seconds=query + dml + ddl,
        query_count=query_count,
        failed_count=failed,
        query_type_compute_seconds={"QUERY": query, "DML": dml, "DDL": ddl},
        error_type_counts=_split_failures(failed),
    )


# Hourly aggregate compute usage (drives the 24h / 48h Summary options).
SAMPLE_COMPUTE_BUCKETS_HOURLY: list[MotherDuckComputeUsageBucket] = [
    _bucket("2026-07-15T09:00:00+00:00", "hour", 90, 30, 10, 1, 43),
    _bucket("2026-07-15T10:00:00+00:00", "hour", 120, 45, 15, 3, 61),
    _bucket("2026-07-15T11:00:00+00:00", "hour", 150, 50, 10, 0, 71),
    _bucket("2026-07-15T12:00:00+00:00", "hour", 100, 45, 15, 2, 51),
    _bucket("2026-07-15T13:00:00+00:00", "hour", 170, 55, 15, 5, 88),
    _bucket("2026-07-15T14:00:00+00:00", "hour", 150, 55, 15, 1, 78),
    _bucket("2026-07-15T15:00:00+00:00", "hour", 110, 50, 15, 4, 58),
]

# Daily aggregate compute usage (drives the 7d / 14d Summary options).
SAMPLE_COMPUTE_BUCKETS_DAILY: list[MotherDuckComputeUsageBucket] = [
    _bucket("2026-07-09T00:00:00+00:00", "day", 1900, 640, 210, 22, 940),
    _bucket("2026-07-10T00:00:00+00:00", "day", 2100, 700, 240, 31, 1020),
    _bucket("2026-07-11T00:00:00+00:00", "day", 1750, 610, 190, 18, 880),
    _bucket("2026-07-12T00:00:00+00:00", "day", 2300, 780, 260, 40, 1130),
    _bucket("2026-07-13T00:00:00+00:00", "day", 2050, 690, 230, 27, 1010),
    _bucket("2026-07-14T00:00:00+00:00", "day", 2400, 820, 280, 35, 1180),
    _bucket("2026-07-15T00:00:00+00:00", "day", 1650, 560, 180, 15, 820),
]


# Recent queries (QUERY_HISTORY, realtime=False). "Failed" == non-null error_type.
#
# `database_name` / `source_id` are populated only on the rows whose query reads
# a Sonar source's iceberg data (e.g. the full-reload COPY/DDL and the failed
# scan), mirroring live behavior: queries against internal/scratch tables carry
# no source database, so those rows leave both blank to exercise the graceful
# empty rendering. Each populated `source_id` is the exact UUID embedded in its
# `database_name` (`{slug}__{source_id}`, underscores -> hyphens).
SAMPLE_RECENT_QUERIES: list[QueryRow] = [
    {
        "query_hash": "a3f19c2b",
        "query_type": "QUERY",
        "query_subtype": "SELECT",
        "user_name": "sonar_org_a1b2c3d4",
        "start_time": "2026-07-15T15:41:02+00:00",
        "total_elapsed_seconds": 1.82,
        "execution_seconds": 1.50,
        "wait_seconds": 0.32,
        "succeeded": True,
        "error_type": "",
        "error_message": "",
        "query_text_treated": "SELECT id, name FROM connections WHERE org_id = ?",
        "database_name": "",
        "source_id": "",
    },
    {
        "query_hash": "7e0d84af",
        "query_type": "DML",
        "query_subtype": "INSERT",
        "user_name": "sonar_org_a1b2c3d4",
        "start_time": "2026-07-15T15:40:55+00:00",
        "total_elapsed_seconds": 12.47,
        "execution_seconds": 11.00,
        "wait_seconds": 1.47,
        "succeeded": True,
        "error_type": "",
        "error_message": "",
        "query_text_treated": "INSERT INTO sync_runs (id, status) VALUES (?, ?)",
        "database_name": "",
        "source_id": "",
    },
    {
        "query_hash": "c91b02de",
        "query_type": "DML",
        "query_subtype": "COPY",
        "user_name": "sonar_org_5f6a7b8c",
        "start_time": "2026-07-15T15:40:31+00:00",
        "total_elapsed_seconds": 48.93,
        "execution_seconds": 40.00,
        "wait_seconds": 8.93,
        "succeeded": False,
        "error_type": "OutOfMemory",
        "error_message": (
            "Out of Memory Error: failed to allocate data of size 2.3 GiB "
            "(12.8 GiB/12.8 GiB used) while executing COPY into 'events'"
        ),
        "query_text_treated": "COPY events FROM ? (FORMAT parquet)",
        "database_name": "postgres__2b1a9c40_5f3e_4c21_9d7a_8e6b0f1c2d3e",
        "source_id": "2b1a9c40-5f3e-4c21-9d7a-8e6b0f1c2d3e",
    },
    {
        "query_hash": "1d5e6f70",
        "query_type": "QUERY",
        "query_subtype": "SELECT",
        "user_name": "sonar_org_5f6a7b8c",
        "start_time": "2026-07-15T15:40:12+00:00",
        "total_elapsed_seconds": 0.41,
        "execution_seconds": 0.30,
        "wait_seconds": 0.11,
        "succeeded": True,
        "error_type": "",
        "error_message": "",
        "query_text_treated": "SELECT count(*) FROM streams WHERE state = ?",
        "database_name": "",
        "source_id": "",
    },
    {
        "query_hash": "b8a4c3d2",
        "query_type": "DDL",
        "query_subtype": "CREATE",
        "user_name": "sonar_org_9e8d7c6b",
        "start_time": "2026-07-15T15:39:58+00:00",
        "total_elapsed_seconds": 2.15,
        "execution_seconds": 1.90,
        "wait_seconds": 0.25,
        "succeeded": True,
        "error_type": "",
        "error_message": "",
        "query_text_treated": "CREATE TABLE staging_events AS SELECT * FROM raw",
        "database_name": "salesforce__f0e1d2c3_b4a5_4967_8879_6a5b4c3d2e1f",
        "source_id": "f0e1d2c3-b4a5-4967-8879-6a5b4c3d2e1f",
    },
    {
        "query_hash": "44f7e19a",
        "query_type": "QUERY",
        "query_subtype": "SELECT",
        "user_name": "sonar_org_9e8d7c6b",
        "start_time": "2026-07-15T15:39:40+00:00",
        "total_elapsed_seconds": 73.60,
        "execution_seconds": 60.00,
        "wait_seconds": 13.60,
        "succeeded": False,
        "error_type": "QueryTimeout",
        "error_message": (
            "Query exceeded the configured timeout of 60s and was cancelled "
            "(scanned 4.2B rows across 'huge_join')"
        ),
        "query_text_treated": "SELECT * FROM huge_join WHERE ts > ? ORDER BY ts",
        "database_name": "stripe__7c9d0e1f_2a3b_4c5d_6e7f_8a9b0c1d2e3f",
        "source_id": "7c9d0e1f-2a3b-4c5d-6e7f-8a9b0c1d2e3f",
    },
    {
        "query_hash": "2c0b91fe",
        "query_type": "DML",
        "query_subtype": "DELETE",
        "user_name": "sonar_org_a1b2c3d4",
        "start_time": "2026-07-15T15:39:22+00:00",
        "total_elapsed_seconds": 5.08,
        "execution_seconds": 4.50,
        "wait_seconds": 0.58,
        "succeeded": True,
        "error_type": "",
        "error_message": "",
        "query_text_treated": "DELETE FROM tmp_scratch WHERE created_at < ?",
        "database_name": "",
        "source_id": "",
    },
    {
        "query_hash": "9fa1207c",
        "query_type": "DML",
        "query_subtype": "INSERT",
        "user_name": "sonar_org_5f6a7b8c",
        "start_time": "2026-07-15T15:38:47+00:00",
        "total_elapsed_seconds": 21.36,
        "execution_seconds": 18.00,
        "wait_seconds": 3.36,
        "succeeded": False,
        "error_type": "PermissionDenied",
        "error_message": (
            "Permission denied: user does not have INSERT privilege on "
            "table 'audit_log' in schema 'main'"
        ),
        "query_text_treated": "INSERT INTO audit_log (actor, action) VALUES (?, ?)",
        "database_name": "",
        "source_id": "",
    },
]


# Active server connections (md_active_server_connections). No client_query text.
# `database_name` / `source_id` are populated only for connections whose running
# statement scans a Sonar source's iceberg data; idle / non-scan connections
# leave both blank.
SAMPLE_ACTIVE_CONNECTIONS: list[ConnectionRow] = [
    {
        "client_connection_id": "3b1f…8a2c",
        "client_user_agent": "sonar_org_a1b2c3d4 / duckdb 1.1.3",
        "server_transaction_stage": "RUNNING",
        "server_query_elapsed_time": "0:00:12",
        "database_name": "postgres__2b1a9c40_5f3e_4c21_9d7a_8e6b0f1c2d3e",
        "source_id": "2b1a9c40-5f3e-4c21-9d7a-8e6b0f1c2d3e",
    },
    {
        "client_connection_id": "c74e…19bd",
        "client_user_agent": "sonar_org_5f6a7b8c / duckdb 1.1.3",
        "server_transaction_stage": "COMMITTING",
        "server_query_elapsed_time": "0:00:03",
        "database_name": "",
        "source_id": "",
    },
    {
        "client_connection_id": "0a92…f5e1",
        "client_user_agent": "sonar_org_9e8d7c6b / duckdb 1.1.1",
        "server_transaction_stage": "IDLE_IN_TXN",
        "server_query_elapsed_time": "0:04:37",
        "database_name": "",
        "source_id": "",
    },
    {
        "client_connection_id": "e15d…6c40",
        "client_user_agent": "sonar_org_a1b2c3d4 / duckdb 1.1.3",
        "server_transaction_stage": "RUNNING",
        "server_query_elapsed_time": "0:00:48",
        "database_name": "stripe__7c9d0e1f_2a3b_4c5d_6e7f_8a9b0c1d2e3f",
        "source_id": "7c9d0e1f-2a3b-4c5d-6e7f-8a9b0c1d2e3f",
    },
]
