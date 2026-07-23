# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Parameterized unit tests for MotherDuck text processing utilities."""

import hashlib
from typing import Any

import pytest

from airbyte_ops_mcp.motherduck_diagnostics.text_processing import (
    apply_query_text_treatment,
    compute_query_hash,
    detect_query_subtype,
    extract_database_name,
    extract_metadata,
    normalize_query,
    parse_source_id_from_database_name,
    redact_string_constants,
)

# A real source UUID and the Sonar database name that embeds it (hyphens ->
# underscores). Tests derive their expectations from these two known values, not
# from strings restated inline at each assertion.
_SOURCE_ID = "2b1a9c40-5f3e-4c21-9d7a-8e6b0f1c2d3e"
_SOURCE_ID_UNDERSCORED = _SOURCE_ID.replace("-", "_")
_DATABASE_NAME = f"postgres__{_SOURCE_ID_UNDERSCORED}"


def _full_reload_ddl(database_name: str, *, table: str = "users") -> str:
    """Build a full-reload DDL that scans `database_name`'s iceberg S3 path."""
    return (
        f'CREATE OR REPLACE TABLE "{table}" AS '
        f"SELECT * FROM iceberg_scan("
        f"'s3://ab-cloud-bucket/data/{database_name}.db/{table}/metadata/v1.json')"
    )


@pytest.mark.unit
@pytest.mark.parametrize("char_limit", [1, 2, 3, 4, 10])
def test_apply_query_text_treatment_respects_small_char_limit(
    char_limit: int,
) -> None:
    result = apply_query_text_treatment(
        "SELECT * FROM some_long_table_name",
        char_limit=char_limit,
        redact_strings=False,
    )
    assert len(result) <= char_limit


@pytest.mark.unit
@pytest.mark.parametrize(
    "raw_query,expected_metadata,expected_normalized,expected_subtype",
    [
        pytest.param(
            '/* {"source": "sonar", "workspace_id": "abc123"} */ SELECT 1',
            {"source": "sonar", "workspace_id": "abc123"},
            "SELECT 1",
            "SELECT",
            id="select_with_metadata",
        ),
        pytest.param(
            '/* {"key": 42, "nested": {"a": true}} */ INSERT INTO t VALUES (1)',
            {"key": 42, "nested": {"a": True}},
            "INSERT INTO t VALUES (1)",
            "INSERT",
            id="insert_with_nested_metadata",
        ),
        pytest.param(
            "SELECT * FROM users",
            None,
            "SELECT * FROM users",
            "SELECT",
            id="select_no_metadata",
        ),
        pytest.param(
            "/* not json */ SELECT 1",
            None,
            "/* not json */ SELECT 1",
            "UNKNOWN",
            id="non_json_comment_not_stripped",
        ),
        pytest.param(
            "/* {invalid json} */ SELECT 1",
            None,
            "SELECT 1",
            "SELECT",
            id="malformed_json_still_stripped",
        ),
        pytest.param(
            '  /* {"key": "val"} */ SELECT 1',
            {"key": "val"},
            "SELECT 1",
            "SELECT",
            id="leading_whitespace_with_metadata",
        ),
        pytest.param(
            "COPY t TO 's3://bucket/path'",
            None,
            "COPY t TO 's3://bucket/path'",
            "COPY",
            id="copy_statement",
        ),
        pytest.param(
            "CREATE TABLE t (id INT)",
            None,
            "CREATE TABLE t (id INT)",
            "CREATE",
            id="create_statement",
        ),
        pytest.param(
            "DROP TABLE t",
            None,
            "DROP TABLE t",
            "DROP",
            id="drop_statement",
        ),
        pytest.param(
            "ALTER TABLE t ADD COLUMN c INT",
            None,
            "ALTER TABLE t ADD COLUMN c INT",
            "ALTER",
            id="alter_statement",
        ),
        pytest.param(
            "UPDATE users SET name = 'x'",
            None,
            "UPDATE users SET name = 'x'",
            "UPDATE",
            id="update_statement",
        ),
        pytest.param(
            "DELETE FROM users WHERE id = 1",
            None,
            "DELETE FROM users WHERE id = 1",
            "DELETE",
            id="delete_statement",
        ),
        pytest.param(
            "ATTACH 'md:db'",
            None,
            "ATTACH 'md:db'",
            "ATTACH",
            id="attach_statement",
        ),
        pytest.param(
            "DETACH db",
            None,
            "DETACH db",
            "DETACH",
            id="detach_statement",
        ),
        pytest.param(
            "EXPLAIN SELECT 1",
            None,
            "EXPLAIN SELECT 1",
            "EXPLAIN",
            id="explain_statement",
        ),
        pytest.param(
            "WITH cte AS (SELECT 1) SELECT * FROM cte",
            None,
            "WITH cte AS (SELECT 1) SELECT * FROM cte",
            "WITH",
            id="with_cte",
        ),
        pytest.param(
            "FROM users SELECT *",
            None,
            "FROM users SELECT *",
            "FROM",
            id="from_first_syntax",
        ),
        pytest.param(
            "CALL md_active_server_connections()",
            None,
            "CALL md_active_server_connections()",
            "CALL",
            id="call_statement",
        ),
        pytest.param(
            "PRAGMA version",
            None,
            "PRAGMA version",
            "PRAGMA",
            id="pragma_statement",
        ),
        pytest.param(
            "SHOW TABLES",
            None,
            "SHOW TABLES",
            "SHOW",
            id="show_statement",
        ),
        pytest.param(
            "INSTALL httpfs",
            None,
            "INSTALL httpfs",
            "INSTALL",
            id="install_statement",
        ),
        pytest.param(
            "select * from users",
            None,
            "select * from users",
            "SELECT",
            id="lowercase_select",
        ),
        pytest.param(
            "",
            None,
            "",
            "UNKNOWN",
            id="empty_string",
        ),
        pytest.param(
            "   ",
            None,
            "",
            "UNKNOWN",
            id="whitespace_only",
        ),
        pytest.param(
            "/* {\"a\": 1} */ SELECT * WHERE x = '}' /* comment */",
            {"a": 1},
            "SELECT * WHERE x = '}' /* comment */",
            "SELECT",
            id="no_over_strip_with_braces_after_metadata",
        ),
        pytest.param(
            "MERGE INTO t USING s",
            None,
            "MERGE INTO t USING s",
            "UNKNOWN",
            id="unknown_keyword",
        ),
        pytest.param(
            "123 SELECT",
            None,
            "123 SELECT",
            "UNKNOWN",
            id="starts_with_number",
        ),
    ],
)
def test_query_text_structured_output(
    raw_query: str,
    expected_metadata: dict[str, Any] | None,
    expected_normalized: str,
    expected_subtype: str,
) -> None:
    """Validate metadata extraction, normalization, subtype, and hash from one input."""
    assert extract_metadata(raw_query) == expected_metadata
    assert normalize_query(raw_query) == expected_normalized
    assert detect_query_subtype(raw_query) == expected_subtype

    if expected_normalized:
        expected_hash = hashlib.sha256(expected_normalized.encode("utf-8")).hexdigest()
        assert compute_query_hash(raw_query) == expected_hash


@pytest.mark.unit
def test_query_hash_ignores_metadata_differences() -> None:
    """Queries with different metadata but same SQL produce the same hash."""
    q1 = '/* {"source": "a"} */ SELECT * FROM t'
    q2 = '/* {"source": "b"} */ SELECT * FROM t'
    assert compute_query_hash(q1) == compute_query_hash(q2)


@pytest.mark.unit
def test_query_hash_differs_for_different_sql() -> None:
    """Different SQL text produces different hashes."""
    assert compute_query_hash("SELECT 1") != compute_query_hash("SELECT 2")


# --- redact_string_constants ---


@pytest.mark.unit
@pytest.mark.parametrize(
    "query_text,expected",
    [
        pytest.param(
            "SELECT * FROM users WHERE name = 'AJ'",
            "SELECT * FROM users WHERE name = ?",
            id="single_string_literal",
        ),
        pytest.param(
            "WHERE a = 'foo' AND b = 'bar'",
            "WHERE a = ? AND b = ?",
            id="multiple_string_literals",
        ),
        pytest.param(
            "SELECT * FROM users WHERE id = 42",
            "SELECT * FROM users WHERE id = 42",
            id="no_string_literals",
        ),
        pytest.param(
            "WHERE name = 'O''Brien'",
            "WHERE name = ?",
            id="escaped_quote_doubled",
        ),
        pytest.param(
            "SELECT ''",
            "SELECT ?",
            id="empty_string_literal",
        ),
    ],
)
def test_redact_string_constants(query_text: str, expected: str) -> None:
    assert redact_string_constants(query_text) == expected


# --- apply_query_text_treatment ---


@pytest.mark.unit
@pytest.mark.parametrize(
    "query_text,char_limit,redact_strings,expected",
    [
        pytest.param(
            "SELECT * FROM users WHERE name = 'AJ'",
            1000,
            True,
            "SELECT * FROM users WHERE name = ?",
            id="redact_within_limit",
        ),
        pytest.param(
            "SELECT * FROM users WHERE name = 'AJ'",
            1000,
            False,
            "SELECT * FROM users WHERE name = 'AJ'",
            id="no_redact_within_limit",
        ),
        pytest.param(
            "SELECT " + "x" * 100,
            20,
            False,
            "SELECT " + "x" * 10 + "...",
            id="truncation_applied",
        ),
        pytest.param(
            '/* {"key": "val"} */ SELECT 1',
            1000,
            False,
            "SELECT 1",
            id="metadata_stripped",
        ),
        pytest.param(
            "SELECT 'secret_value' FROM t",
            12,
            True,
            "SELECT ? ...",
            id="redact_then_truncate",
        ),
    ],
)
def test_apply_query_text_treatment(
    query_text: str,
    char_limit: int,
    redact_strings: bool,
    expected: str,
) -> None:
    result = apply_query_text_treatment(
        query_text,
        char_limit=char_limit,
        redact_strings=redact_strings,
    )
    assert result == expected


# --- extract_database_name ---


@pytest.mark.unit
@pytest.mark.parametrize(
    "query_text, expected",
    [
        pytest.param(
            _full_reload_ddl(_DATABASE_NAME),
            _DATABASE_NAME,
            id="full_reload_ddl",
        ),
        pytest.param(
            _full_reload_ddl(_DATABASE_NAME, table="daily_active_users"),
            _DATABASE_NAME,
            id="ignores_unqualified_create_target",
        ),
        pytest.param("SELECT * FROM users WHERE id = 1", None, id="plain_select"),
        pytest.param("", None, id="empty"),
        pytest.param(
            "COPY events FROM 's3://bucket/data/events.parquet'",
            None,
            id="s3_path_without_iceberg_scan",
        ),
        pytest.param(
            "SELECT * FROM iceberg_scan('s3://bucket/warehouse/users/meta.json')",
            None,
            id="iceberg_scan_without_data_db_segment",
        ),
    ],
)
def test_extract_database_name(query_text: str, expected: str | None) -> None:
    """Extraction reads the `data/<db>.db/` segment of the iceberg_scan path.

    It uses only that S3 path (never the unqualified `CREATE ... TABLE
    "<table>"` write target) and returns `None` when there is no clean match.
    """
    assert extract_database_name(query_text) == expected


# --- parse_source_id_from_database_name ---


@pytest.mark.unit
@pytest.mark.parametrize(
    "database_name, expected",
    [
        pytest.param(_DATABASE_NAME, _SOURCE_ID, id="plain"),
        pytest.param(f"stg_{_DATABASE_NAME}", _SOURCE_ID, id="env_prefixed"),
        pytest.param(
            f"google_ads__{_SOURCE_ID_UNDERSCORED}",
            _SOURCE_ID,
            id="slug_with_single_underscore",
        ),
        pytest.param("postgres_no_delimiter", None, id="no_double_underscore"),
        pytest.param("postgres__not_a_uuid", None, id="trailing_not_uuid"),
        pytest.param("postgres__", None, id="empty_trailing"),
        pytest.param(
            f"postgres__{_SOURCE_ID_UNDERSCORED}_extra",
            None,
            id="trailing_has_extra_chars",
        ),
        pytest.param(
            f"postgres__{_SOURCE_ID.replace('-', '')}",
            None,
            id="hyphenless_hex_not_canonical",
        ),
        pytest.param("", None, id="empty"),
    ],
)
def test_parse_source_id_from_database_name(
    database_name: str,
    expected: str | None,
) -> None:
    """The trailing `__`-delimited segment maps back to the canonical UUID.

    The split is on the final double-underscore boundary, so an env prefix and
    single underscores in the slug don't disturb the parse. Anything without a
    canonical UUID trailing segment fails closed to `None`.
    """
    assert parse_source_id_from_database_name(database_name) == expected
