"""Shared test utilities for integration tests.

This module contains helper functions and test data used by both
REST API and Worker integration tests.
"""

from sqlalchemy.dialects.sqlite import insert as sqlite_insert


# MARK: - Pandas to_sql Helper Methods


def make_sqlite_method(conflict_prefix: str = "OR IGNORE"):
    """Return a pandas.to_sql(method=...) that inserts with a given prefix.

    Args:
        conflict_prefix: SQL conflict handling prefix.
            - "OR IGNORE": Skip rows that violate constraints
            - "OR REPLACE": Replace existing rows on conflict
            - "": No conflict handling (will error on duplicates)

    Returns:
        A callable suitable for pandas DataFrame.to_sql(method=...)
    """

    def _method(table, conn, keys, data_iter):
        # Pandas hands us a pandas.io.sql.SQLTable wrapper; unwrap to SA Table
        sa_table = getattr(table, "table", table)

        rows = [dict(zip(keys, row)) for row in data_iter]
        if not rows:
            return

        stmt = sqlite_insert(sa_table).values(rows)
        if conflict_prefix:
            stmt = stmt.prefix_with(conflict_prefix)

        conn.execute(stmt)

    return _method


def make_sqlite_upsert_method(conflict_target=("id",)):
    """Return a pandas.to_sql(method=...) that does ON CONFLICT DO NOTHING.

    Args:
        conflict_target: Tuple of column names that form the unique constraint.

    Returns:
        A callable suitable for pandas DataFrame.to_sql(method=...)
    """

    def _method(table, conn, keys, data_iter):
        sa_table = getattr(table, "table", table)
        rows = [dict(zip(keys, row)) for row in data_iter]
        if not rows:
            return

        stmt = sqlite_insert(sa_table).values(rows)
        stmt = stmt.on_conflict_do_nothing(index_elements=list(conflict_target))
        conn.execute(stmt)

    return _method


# MARK: - Test Data Constants

# JSON test data for filtering tests
JSON_FILTER_TEST_DATA = [
    {"name": "Alice", "tags": ["python", "sqlalchemy", "d1"]},
    {"name": "Bob", "tags": ["javascript", "react"]},
    {"name": "Charlie", "tags": ["python", "fastapi"]},
]

# JSON aggregate test data
JSON_AGGREGATE_TEST_DATA = [
    {"post_id": "p1", "tags": ["tech", "python"], "score": 10},
    {"post_id": "p2", "tags": ["tech", "javascript"], "score": 20},
    {"post_id": "p3", "tags": ["python", "data"], "score": 15},
]

# Expected aggregate results by tag
JSON_AGGREGATE_EXPECTED = {
    "data": 15,
    "javascript": 20,
    "python": 25,
    "tech": 30,
}

# Product categories test data
PRODUCT_CATEGORIES_TEST_DATA = [
    {"product": "Widget A", "categories": ["electronics", "gadgets"]},
    {"product": "Widget B", "categories": ["home", "kitchen"]},
    {"product": "Widget C", "categories": ["electronics", "office"]},
    {"product": "Widget D", "categories": ["sports", "outdoor"]},
]

# SQL injection test payloads
SQLI_PAYLOADS = {
    "string_bypass": "' OR '1'='1",
    "union_attack": "' UNION SELECT name FROM sqlite_master--",
    "like_bypass": "%' OR '1'='1' --",
    "numeric_bypass": "1 OR 1=1",
}

# Pandas test DataFrames data
PANDAS_BASIC_DATA = {
    "name": ["Alice", "Bob", "Charlie"],
    "score": [85, 92, 78],
}

PANDAS_JSON_DATA = {
    "name": ["service_a", "service_b"],
    "config": [
        {"enabled": True, "retries": 3},
        {"enabled": False, "retries": 1},
    ],
}
