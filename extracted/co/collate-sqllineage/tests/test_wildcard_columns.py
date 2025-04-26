from .helpers import TestColumnQualifierTuple, assert_column_lineage_equal


def test_basic_cte():
    sql = """
    CREATE VIEW my_view as
    WITH tab1 AS (SELECT * FROM "db"."schema"."table2")
    SELECT
        id,
        name
    FROM tab1"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("id", "db.schema.table2"),
                TestColumnQualifierTuple("id", "my_view"),
            ),
            (
                TestColumnQualifierTuple("name", "db.schema.table2"),
                TestColumnQualifierTuple("name", "my_view"),
            ),
        ],
    )

    sql = """
    CREATE VIEW my_view as
    WITH tab1 AS (SELECT id, name FROM "db"."schema"."table2")
    SELECT
        *
    FROM tab1"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("id", "db.schema.table2"),
                TestColumnQualifierTuple("id", "my_view"),
            ),
            (
                TestColumnQualifierTuple("name", "db.schema.table2"),
                TestColumnQualifierTuple("name", "my_view"),
            ),
            (
                TestColumnQualifierTuple(
                    "*", "tab1", True, '(SELECT id, name FROM "db"."schema"."table2")'
                ),
                TestColumnQualifierTuple("*", "my_view"),
            ),
        ],
    )


def test_cte_with_join():
    sql = """
    CREATE VIEW my_view as
    WITH tab1 AS (SELECT a.id, b.name FROM table2 a left join table1 b on a.id = b.id)
    SELECT
        *
    FROM tab1"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("id", "table2"),
                TestColumnQualifierTuple("id", "my_view"),
            ),
            (
                TestColumnQualifierTuple("name", "table1"),
                TestColumnQualifierTuple("name", "my_view"),
            ),
            (
                TestColumnQualifierTuple(
                    "*",
                    "tab1",
                    True,
                    "(SELECT a.id, b.name FROM table2 a left join table1 b on a.id = b.id)",
                ),
                TestColumnQualifierTuple("*", "my_view"),
            ),
        ],
    )


def test_subquery():
    sql = """
    CREATE VIEW my_view as
    SELECT id, name from (
    select * from tab1
    ) sq1"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("id", "tab1"),
                TestColumnQualifierTuple("id", "my_view"),
            ),
            (
                TestColumnQualifierTuple("name", "tab1"),
                TestColumnQualifierTuple("name", "my_view"),
            ),
        ],
    )


def test_complex_subquery():
    sql = """
    CREATE VIEW my_view as
    select * from (SELECT id, name from (select * from tab1) sq1) sq2"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("id", "tab1"),
                TestColumnQualifierTuple("id", "my_view"),
            ),
            (
                TestColumnQualifierTuple("name", "tab1"),
                TestColumnQualifierTuple("name", "my_view"),
            ),
            (
                TestColumnQualifierTuple(
                    "*", "sq2", True, "(SELECT id, name from (select * from tab1) sq1)"
                ),
                TestColumnQualifierTuple("*", "my_view"),
            ),
        ],
    )


def test_partial_wildcard():
    sql = """
    CREATE OR REPLACE VIEW new_view
    AS
    WITH sq1 as (select id, name, age from std1),
    sq2 as (select id, name from std2)

    select a.*,
    b.id mid
    from sq1 a inner join sq2 b on a.id=b.id"""

    sq1 = "(select id, name, age from std1)"
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("age", "std1"),
                TestColumnQualifierTuple("age", "new_view"),
            ),
            (
                TestColumnQualifierTuple("id", "std1"),
                TestColumnQualifierTuple("id", "new_view"),
            ),
            (
                TestColumnQualifierTuple("id", "std2"),
                TestColumnQualifierTuple("mid", "new_view"),
            ),
            (
                TestColumnQualifierTuple("name", "std1"),
                TestColumnQualifierTuple("name", "new_view"),
            ),
            (
                TestColumnQualifierTuple("*", "sq1", True, sq1),
                TestColumnQualifierTuple("*", "new_view"),
            ),
        ],
    )
