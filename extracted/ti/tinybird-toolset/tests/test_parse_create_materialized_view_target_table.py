import pytest

from chtoolset.query import parse_create_materialized_view_target_table


def test_parse_mv_with_database_and_table():
    sql = "CREATE MATERIALIZED VIEW mv TO warehouse.events_rollup AS SELECT * FROM events"
    result = parse_create_materialized_view_target_table(sql)
    assert result["database"] == "warehouse"
    assert result["table"] == "events_rollup"


def test_parse_mv_with_table_only():
    sql = "CREATE MATERIALIZED VIEW mv TO events_rollup AS SELECT * FROM events"
    result = parse_create_materialized_view_target_table(sql)
    assert result["database"] is None
    assert result["table"] == "events_rollup"


def test_parse_mv_with_backtick_quoted_identifiers():
    sql = "CREATE MATERIALIZED VIEW db.view TO `target_db`.`target_table` AS SELECT * FROM events"
    result = parse_create_materialized_view_target_table(sql)
    assert result["database"] == "target_db"
    assert result["table"] == "target_table"


def test_parse_mv_with_columns():
    sql = "CREATE MATERIALIZED VIEW db.view TO target_table (col1 UInt64, col2 String) AS SELECT * FROM events"
    result = parse_create_materialized_view_target_table(sql)
    assert result["database"] is None
    assert result["table"] == "target_table"


def test_parse_mv_with_database_table_and_columns():
    sql = "CREATE MATERIALIZED VIEW db.view TO target_db.target_table (col1 UInt64, col2 String) AS SELECT * FROM events"
    result = parse_create_materialized_view_target_table(sql)
    assert result["database"] == "target_db"
    assert result["table"] == "target_table"


def test_parse_mv_with_complex_column_types():
    sql = "CREATE MATERIALIZED VIEW db.view TO target_table (`id` Int32, `value` String, `timestamp` Nullable(DateTime64(3))) AS SELECT * FROM events"
    result = parse_create_materialized_view_target_table(sql)
    assert result["database"] is None
    assert result["table"] == "target_table"


def test_parse_mv_with_database_and_complex_column_types():
    sql = "CREATE MATERIALIZED VIEW db.view TO target_db.target_table (`id` Int32, `value` String, `timestamp` Nullable(DateTime64(3))) AS SELECT * FROM events"
    result = parse_create_materialized_view_target_table(sql)
    assert result["database"] == "target_db"
    assert result["table"] == "target_table"


def test_non_mv_query_raises():
    sql = "CREATE TABLE foo (id UInt64) ENGINE = MergeTree ORDER BY id"
    with pytest.raises(ValueError):
        parse_create_materialized_view_target_table(sql)


def test_mv_without_to_raises():
    sql = "CREATE MATERIALIZED VIEW mv ENGINE = MergeTree ORDER BY id AS SELECT * FROM events"
    with pytest.raises(ValueError):
        parse_create_materialized_view_target_table(sql)


def test_non_string_raises():
    with pytest.raises(TypeError):
        parse_create_materialized_view_target_table(123)
