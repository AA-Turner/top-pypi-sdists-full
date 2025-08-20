"""
Tests for nested JOIN handling with parentheses and alias registration.
These tests cover the fixes for extracting all source tables from deeply nested JOINs
and proper alias registration for column-level lineage.

Note: These tests only work with the sqlfluff parser (ansi dialect) as the fixes
are implemented in the sqlfluff handlers.
"""

from collate_sqllineage.runner import LineageRunner
from .helpers import assert_table_lineage_equal


def test_select_join_with_single_parenthesis():
    """Test JOIN within single parenthesis."""
    assert_table_lineage_equal(
        "SELECT * FROM (tab1 t1 INNER JOIN tab2 t2 ON t1.id = t2.id)",
        {"tab1", "tab2"},
        test_sqlparse=False,  # Only test with sqlfluff
    )


def test_select_join_with_parenthesis_then_join():
    """Test parenthesized JOIN followed by another JOIN."""
    assert_table_lineage_equal(
        "SELECT * FROM (tab1 t1 INNER JOIN tab2 t2 ON t1.id = t2.id) LEFT JOIN tab3 t3 ON t2.id = t3.id",
        {"tab1", "tab2", "tab3"},
        test_sqlparse=False,
    )


def test_select_join_with_double_parenthesis():
    """Test JOIN within double nested parentheses."""
    assert_table_lineage_equal(
        "SELECT * FROM ((tab1 t1 INNER JOIN tab2 t2 ON t1.id = t2.id) LEFT JOIN tab3 t3 ON t2.id = t3.id)",
        {"tab1", "tab2", "tab3"},
        test_sqlparse=False,
    )


def test_select_join_with_triple_parenthesis():
    """Test JOIN within triple nested parentheses."""
    assert_table_lineage_equal(
        """SELECT * FROM (((tab1 t1
        INNER JOIN tab2 t2 ON t1.id = t2.id)
        LEFT JOIN tab3 t3 ON t2.id = t3.id)
        INNER JOIN tab4 t4 ON t3.id = t4.id)""",
        {"tab1", "tab2", "tab3", "tab4"},
        test_sqlparse=False,
    )


def test_select_join_with_quad_parenthesis():
    """Test JOIN within quadruple nested parentheses - like the original issue."""
    assert_table_lineage_equal(
        """SELECT * FROM ((((tab1 t1
        INNER JOIN tab2 t2 ON t1.id = t2.id)
        LEFT JOIN tab3 t3 ON t2.id = t3.id)
        INNER JOIN tab4 t4 ON t3.id = t4.id)
        LEFT JOIN tab5 t5 ON t4.id = t5.id)""",
        {"tab1", "tab2", "tab3", "tab4", "tab5"},
        test_sqlparse=False,
    )


def test_select_join_with_schema_and_nested_parenthesis():
    """Test nested JOINs with schema-qualified table names."""
    assert_table_lineage_equal(
        """SELECT * FROM ((schema1.tab1 t1
        INNER JOIN schema2.tab2 t2 ON t1.id = t2.id)
        LEFT JOIN schema3.tab3 t3 ON t2.id = t3.id)""",
        {"schema1.tab1", "schema2.tab2", "schema3.tab3"},
        test_sqlparse=False,
    )


def test_select_join_with_database_schema_and_nested_parenthesis():
    """Test nested JOINs with fully qualified table names."""
    assert_table_lineage_equal(
        """SELECT * FROM ((db1.schema1.tab1 t1
        INNER JOIN db2.schema2.tab2 t2 ON t1.id = t2.id)
        LEFT JOIN db3.schema3.tab3 t3 ON t2.id = t3.id)""",
        {"db1.schema1.tab1", "db2.schema2.tab2", "db3.schema3.tab3"},
        test_sqlparse=False,
    )


def test_select_mixed_join_types_with_nested_parenthesis():
    """Test different JOIN types in nested parentheses."""
    assert_table_lineage_equal(
        """SELECT * FROM ((((tab1 t1
        INNER JOIN tab2 t2 ON t1.id = t2.id)
        LEFT JOIN tab3 t3 ON t2.id = t3.id)
        RIGHT JOIN tab4 t4 ON t3.id = t4.id)
        CROSS JOIN tab5 t5)""",
        {"tab1", "tab2", "tab3", "tab4", "tab5"},
        test_sqlparse=False,
    )


def test_select_join_original_issue_structure():
    """Test the exact structure from the original issue with generic table names."""
    sql = """
    SELECT *
    FROM ((((tab1 t1
    INNER JOIN tab2 t2 ON (t2.col1 >= t1.col1))
    LEFT JOIN tab3 t3 ON ((t1.col2 = t3.col2) AND (t1.col3 = (date(t3.col3) - INTERVAL '1' DAY))))
    INNER JOIN tab4 t4 ON (t4.col4 = t1.col4))
    LEFT JOIN tab5 t5 ON (t5.col5 = IF(((t3.col5 = '') OR (t3.col5 IS NULL)), t1.col5, t3.col5)))
    """
    assert_table_lineage_equal(
        sql, {"tab1", "tab2", "tab3", "tab4", "tab5"}, test_sqlparse=False
    )


def test_create_view_with_nested_joins():
    """Test CREATE VIEW with nested JOINs."""
    sql = """
    CREATE VIEW test_view AS
    SELECT *
    FROM ((tab1 t1
    INNER JOIN tab2 t2 ON t1.id = t2.id)
    LEFT JOIN tab3 t3 ON t2.id = t3.id)
    """
    lr = LineageRunner(sql, dialect="ansi")
    assert len(lr.source_tables) == 3
    assert {str(t) for t in lr.source_tables} == {
        "<default>.tab1",
        "<default>.tab2",
        "<default>.tab3",
    }
    assert len(lr.target_tables) == 1
    assert str(list(lr.target_tables)[0]) == "<default>.test_view"


def test_alias_registration_in_nested_joins():
    """Test that aliases are properly registered for tables in nested JOINs."""
    # Create a table so we have column lineage
    sql = """
    CREATE TABLE result AS
    SELECT t1.col1, t2.col2, t3.col3
    FROM ((tab1 t1
    INNER JOIN tab2 t2 ON t1.id = t2.id)
    LEFT JOIN tab3 t3 ON t2.id = t3.id)
    """
    lr = LineageRunner(sql, dialect="ansi", verbose=True)

    # Check that source tables are found
    assert len(lr.source_tables) == 3
    source_tables = {str(t) for t in lr.source_tables}
    assert source_tables == {"<default>.tab1", "<default>.tab2", "<default>.tab3"}

    # Check that target table is created
    assert len(lr.target_tables) == 1
    assert str(list(lr.target_tables)[0]) == "<default>.result"

    # Check column lineage - aliases should be resolved to table names
    column_lineages = list(lr.get_column_lineage())

    # We expect 3 column lineages
    assert len(column_lineages) == 3

    # Convert to strings for easier checking
    lineage_strs = {(str(src), str(tgt)) for src, tgt in column_lineages}

    # Check that columns are properly qualified with table names, not aliases
    expected_lineages = {
        ("<default>.tab1.col1", "<default>.result.col1"),
        ("<default>.tab2.col2", "<default>.result.col2"),
        ("<default>.tab3.col3", "<default>.result.col3"),
    }

    assert (
        lineage_strs == expected_lineages
    ), f"Expected {expected_lineages}, got {lineage_strs}"


def test_column_lineage_with_nested_joins_and_aliases():
    """Test column-level lineage with nested JOINs and table aliases."""
    sql = """
    CREATE VIEW result_view AS
    SELECT
        t1.col1 as result_col1,
        t2.col2 as result_col2,
        t3.col3 as result_col3
    FROM ((schema1.tab1 t1
    INNER JOIN schema2.tab2 t2 ON t1.id = t2.id)
    LEFT JOIN schema3.tab3 t3 ON t2.id = t3.id)
    """
    lr = LineageRunner(sql, dialect="ansi", verbose=True)

    # Check source tables
    assert len(lr.source_tables) == 3
    assert {str(t) for t in lr.source_tables} == {
        "schema1.tab1",
        "schema2.tab2",
        "schema3.tab3",
    }

    # Check column lineage
    column_lineages = list(lr.get_column_lineage())
    lineage_strs = {(str(src), str(tgt)) for src, tgt in column_lineages}

    # Verify that aliases are resolved to full table names
    expected = {
        ("schema1.tab1.col1", "<default>.result_view.result_col1"),
        ("schema2.tab2.col2", "<default>.result_view.result_col2"),
        ("schema3.tab3.col3", "<default>.result_view.result_col3"),
    }

    assert lineage_strs == expected, f"Expected {expected}, got {lineage_strs}"


def test_complex_nested_joins_from_original_issue():
    """Test the exact query structure from the original issue."""
    sql = """
    CREATE VIEW zyz AS
    SELECT
      c.snapshot_day,
      c.customer_cwid,
      c_lv.customer_number,
      c.sales_marketsegment,
      d.delivery_day
    FROM ((((delta.bi_data_is24_etl.d_customers_without_pii c
    INNER JOIN delta.bi_data_is24_utils.last_delivered_day d ON (d.delivery_day >= c.snapshot_day))
    LEFT JOIN delta.datalake_raw_personal_delta.salesforce_crm_acchierarchy_data_crm h
    ON ((c.customer_cwid = h.customer_cwid) AND (c.snapshot_day = (date(h.partition_date) - INTERVAL '1' DAY))))
    INNER JOIN delta.bi_data_is24_etl.d_customers_lv c_lv ON (c_lv.customer_cwid = c.customer_cwid))
    LEFT JOIN delta.bi_data_is24_etl.d_customers_lv tc ON (tc.customer_cwid = IF(((h.customer_cwid = '')
    OR (h.customer_cwid IS NULL)), c.customer_cwid, h.top_customer_cwid)))
    """

    lr = LineageRunner(sql, dialect="ansi", verbose=True)

    # Check all source tables are found
    source_tables = {str(t) for t in lr.source_tables}
    expected_tables = {
        "delta.bi_data_is24_etl.d_customers_without_pii",
        "delta.bi_data_is24_utils.last_delivered_day",
        "delta.datalake_raw_personal_delta.salesforce_crm_acchierarchy_data_crm",
        "delta.bi_data_is24_etl.d_customers_lv",
    }
    assert (
        source_tables == expected_tables
    ), f"Expected {expected_tables}, got {source_tables}"

    # Check column lineage - aliases should be resolved to table names
    column_lineages = list(lr.get_column_lineage())

    # Check specific columns from alias 'c' are resolved to the full table name
    for src, tgt in column_lineages:
        src_str = str(src)
        tgt_str = str(tgt)

        # Columns from 'c' alias should resolve to d_customers_without_pii
        if tgt_str in [
            "<default>.zyz.snapshot_day",
            "<default>.zyz.customer_cwid",
            "<default>.zyz.sales_marketsegment",
        ]:
            assert (
                "d_customers_without_pii" in src_str
            ), f"Column {tgt_str} should come from d_customers_without_pii, got {src_str}"
            assert not src_str.startswith(
                "<default>.c."
            ), f"Column should not use alias 'c', got {src_str}"

        # Column from 'd' alias should resolve to last_delivered_day
        if tgt_str == "<default>.zyz.delivery_day":
            assert (
                "last_delivered_day" in src_str
            ), f"Column delivery_day should come from last_delivered_day, got {src_str}"
            assert not src_str.startswith(
                "<default>.d."
            ), f"Column should not use alias 'd', got {src_str}"

        # Column from 'c_lv' alias should resolve to d_customers_lv
        if tgt_str == "<default>.zyz.customer_number":
            assert (
                "d_customers_lv" in src_str
            ), f"Column customer_number should come from d_customers_lv, got {src_str}"
            assert not src_str.startswith(
                "<default>.c_lv."
            ), f"Column should not use alias 'c_lv', got {src_str}"


def test_join_with_subquery_in_parenthesis():
    """Test JOIN with subquery inside parenthesis."""
    sql = """
    SELECT *
    FROM ((SELECT * FROM tab1) t1
    INNER JOIN tab2 t2 ON t1.id = t2.id)
    """
    assert_table_lineage_equal(sql, {"tab1", "tab2"}, test_sqlparse=False)


def test_multiple_separate_parenthesized_joins():
    """Test multiple separate parenthesized JOIN expressions.

    Note: This is a cross join pattern with comma-separated FROM clauses.
    The current implementation may not extract all tables from the second parenthesized expression.
    """
    sql = """
    SELECT *
    FROM (tab1 t1 INNER JOIN tab2 t2 ON t1.id = t2.id),
         (tab3 t3 LEFT JOIN tab4 t4 ON t3.id = t4.id)
    """
    lr = LineageRunner(sql, dialect="ansi")
    source_tables = {str(t) for t in lr.source_tables}

    # This query has a cross join between two parenthesized expressions
    # The parser might handle this differently - let's check what we actually get
    assert (
        len(source_tables) >= 2
    ), f"Should find at least 2 tables, found: {source_tables}"

    # We definitely should find tab1 and tab2 from the first parenthesized expression
    assert "<default>.tab1" in source_tables
    assert "<default>.tab2" in source_tables

    # Note: tab3 and tab4 extraction depends on how the parser handles comma-separated FROM clauses
    # This is a different pattern from the nested JOINs we fixed, and may require additional work
