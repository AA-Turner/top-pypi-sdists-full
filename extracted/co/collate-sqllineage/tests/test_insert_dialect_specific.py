import pytest

from .helpers import (
    TestColumnQualifierTuple,
    assert_column_lineage_equal,
    assert_table_lineage_equal,
)

"""
This test class will contain all the tests for testing 'Insert Queries' where the dialect is not ANSI.
"""


@pytest.mark.parametrize("dialect", ["databricks", "hive", "sparksql"])
def test_insert_overwrite(dialect: str):
    assert_table_lineage_equal(
        "INSERT OVERWRITE TABLE tab1 SELECT col1 FROM tab2",
        {"tab2"},
        {"tab1"},
        dialect=dialect,
    )


@pytest.mark.parametrize("dialect", ["databricks", "hive", "sparksql"])
def test_insert_overwrite_from_self(dialect: str):
    assert_table_lineage_equal(
        """INSERT OVERWRITE TABLE foo
SELECT col FROM foo
WHERE flag IS NOT NULL""",
        {"foo"},
        {"foo"},
        dialect=dialect,
    )


@pytest.mark.parametrize("dialect", ["databricks", "hive", "sparksql"])
def test_insert_overwrite_from_self_with_join(dialect: str):
    assert_table_lineage_equal(
        """INSERT OVERWRITE TABLE tab_1
SELECT tab_2.col_a from tab_2
JOIN tab_1
ON tab_1.col_a = tab_2.cola""",
        {"tab_1", "tab_2"},
        {"tab_1"},
        dialect=dialect,
    )


@pytest.mark.parametrize("dialect", ["databricks", "hive", "sparksql"])
def test_insert_overwrite_values(dialect: str):
    assert_table_lineage_equal(
        "INSERT OVERWRITE TABLE tab1 VALUES ('val1', 'val2'), ('val3', 'val4')",
        {},
        {"tab1"},
        dialect=dialect,
    )


@pytest.mark.parametrize("dialect", ["databricks", "hive", "sparksql"])
def test_insert_into_with_keyword_table(dialect: str):
    assert_table_lineage_equal(
        "INSERT INTO TABLE tab1 VALUES (1, 2)", set(), {"tab1"}, dialect=dialect
    )


@pytest.mark.parametrize("dialect", ["databricks", "hive", "sparksql"])
def test_insert_into_partitions(dialect: str):
    assert_table_lineage_equal(
        "INSERT INTO TABLE tab1 PARTITION (par1=1) SELECT * FROM tab2",
        {"tab2"},
        {"tab1"},
        dialect=dialect,
    )


@pytest.mark.parametrize("dialect", ["databricks", "sparksql"])
def test_insert_overwrite_without_table_keyword(dialect: str):
    assert_table_lineage_equal(
        "INSERT OVERWRITE tab1 SELECT * FROM tab2",
        {"tab2"},
        {"tab1"},
        dialect=dialect,
    )


@pytest.mark.parametrize("dialect", ["redshift"])
def test_insert_union_redshift(dialect: str):
    sql = """INSERT INTO test_schema.union_all_test
WITH initial_sub
     AS (SELECT eventid,
                listid,
                salesrow
         FROM   test_schema.sales),
     union_sub_test
     AS (SELECT eventid,
                listid,
                salesrow
         FROM   initial_sub
         WHERE  salesrow = 'Yes'
         UNION ALL
         SELECT eventid,
                listid,
                salesrow
         FROM   initial_sub
         WHERE  salesrow = 'No')
SELECT eventid,
       listid,
       salesrow
FROM   union_sub_test
WHERE  listid IN( 500, 501, 502 ); """
    assert_table_lineage_equal(
        sql,
        {"test_schema.sales"},
        {"test_schema.union_all_test"},
        dialect=dialect,
        test_sqlparse=False,
    )
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("eventid", "test_schema.sales"),
                TestColumnQualifierTuple("eventid", "test_schema.union_all_test"),
            ),
            (
                TestColumnQualifierTuple("listid", "test_schema.sales"),
                TestColumnQualifierTuple("listid", "test_schema.union_all_test"),
            ),
            (
                TestColumnQualifierTuple("salesrow", "test_schema.sales"),
                TestColumnQualifierTuple("salesrow", "test_schema.union_all_test"),
            ),
        ],
        dialect=dialect,
        test_sqlparse=False,
    )
