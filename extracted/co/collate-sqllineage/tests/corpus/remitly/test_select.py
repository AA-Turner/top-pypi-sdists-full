"""Tests for Remitly Trino SELECT queries."""

import pytest

from tests.helpers import assert_table_lineage_equal


@pytest.mark.parametrize("dialect", ["trino"])
def test_token_matching_simple_where(dialect: str):
    """Test SELECT with simple WHERE clause on string literal."""
    sql = """
    SELECT col1
    FROM source_table
    WHERE status = 'pendingfunds'
    """
    assert_table_lineage_equal(
        sql,
        {"source_table"},
        {},
        dialect=dialect,
    )


@pytest.mark.parametrize("dialect", ["trino"])
def test_token_matching_string_comparison(dialect: str):
    """Test SELECT with CASE WHEN string comparison."""
    sql = """
    SELECT
        CASE WHEN status = 'pendingfunds' THEN 'Pending' ELSE 'Complete' END as status_desc
    FROM source_table
    """
    assert_table_lineage_equal(
        sql,
        {"source_table"},
        {},
        dialect=dialect,
    )
