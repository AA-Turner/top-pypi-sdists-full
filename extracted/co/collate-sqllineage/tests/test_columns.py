import pytest

from collate_sqllineage import SQLPARSE_DIALECT
from collate_sqllineage.runner import LineageRunner

from .helpers import TestColumnQualifierTuple, assert_column_lineage_equal


def test_select_column():
    sql = """INSERT INTO tab1
SELECT col1
FROM tab2"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("col1", "tab1"),
            )
        ],
    )
    sql = """INSERT INTO tab1
SELECT col1 AS col2
FROM tab2"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("col2", "tab1"),
            )
        ],
    )
    sql = """INSERT INTO tab1
SELECT tab2.col1 AS col2
FROM tab2"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("col2", "tab1"),
            )
        ],
    )


def test_select_column_wildcard():
    sql = """INSERT INTO tab1
SELECT *
FROM tab2"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("*", "tab2"),
                TestColumnQualifierTuple("*", "tab1"),
            )
        ],
    )
    sql = """INSERT INTO tab1
SELECT *
FROM tab2 a
         INNER JOIN tab3 b
                    ON a.id = b.id"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("*", "tab2"),
                TestColumnQualifierTuple("*", "tab1"),
            ),
            (
                TestColumnQualifierTuple("*", "tab3"),
                TestColumnQualifierTuple("*", "tab1"),
            ),
        ],
    )


def test_select_distinct_column():
    sql = """INSERT INTO tab1
SELECT DISTINCT col1
FROM tab2"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("col1", "tab1"),
            )
        ],
    )


def test_select_column_using_function():
    sql = """INSERT INTO tab1
SELECT max(col1),
       count(*)
FROM tab2"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("max(col1)", "tab1"),
            ),
            (
                TestColumnQualifierTuple("*", "tab2"),
                TestColumnQualifierTuple("count(*)", "tab1"),
            ),
        ],
    )
    sql = """INSERT INTO tab1
SELECT max(col1) AS col2,
       count(*)  AS cnt
FROM tab2"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("col2", "tab1"),
            ),
            (
                TestColumnQualifierTuple("*", "tab2"),
                TestColumnQualifierTuple("cnt", "tab1"),
            ),
        ],
    )
    sql = """INSERT INTO tab1
SELECT cast(col1 AS timestamp)
FROM tab2"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("cast(col1 as timestamp)", "tab1"),
            )
        ],
    )
    sql = """INSERT INTO tab1
SELECT cast(col1 AS timestamp) AS col2
FROM tab2"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("col2", "tab1"),
            )
        ],
    )


def test_select_column_using_function_with_complex_parameter():
    sql = """INSERT INTO tab1
SELECT if(col1 = 'foo' AND col2 = 'bar', 1, 0) AS flag
FROM tab2"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("flag", "tab1"),
            ),
            (
                TestColumnQualifierTuple("col2", "tab2"),
                TestColumnQualifierTuple("flag", "tab1"),
            ),
        ],
    )


def test_select_column_using_window_function():
    sql = """INSERT INTO tab1
SELECT row_number() over (partition BY col1 ORDER BY col2 DESC) AS rnum
FROM tab2"""
    assert_column_lineage_equal(
        sql,
        [],
        test_sqlparse=False,
    )


def test_select_column_using_window_function_with_parameters():
    sql = """INSERT INTO tab1
SELECT col0,
       max(col3) over (partition BY col1 ORDER BY col2 DESC) AS rnum,
       col4
FROM tab2"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col0", "tab2"),
                TestColumnQualifierTuple("col0", "tab1"),
            ),
            (
                TestColumnQualifierTuple("col3", "tab2"),
                TestColumnQualifierTuple("rnum", "tab1"),
            ),
            (
                TestColumnQualifierTuple("col4", "tab2"),
                TestColumnQualifierTuple("col4", "tab1"),
            ),
        ],
        test_sqlparse=False,
    )


def test_select_column_using_expression():
    sql = """INSERT INTO tab1
SELECT col1 + col2
FROM tab2"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("col1 + col2", "tab1"),
            ),
            (
                TestColumnQualifierTuple("col2", "tab2"),
                TestColumnQualifierTuple("col1 + col2", "tab1"),
            ),
        ],
    )
    sql = """INSERT INTO tab1
SELECT col1 + col2 AS col3
FROM tab2"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("col3", "tab1"),
            ),
            (
                TestColumnQualifierTuple("col2", "tab2"),
                TestColumnQualifierTuple("col3", "tab1"),
            ),
        ],
    )


def test_select_column_using_expression_in_parenthesis():
    sql = """INSERT INTO tab1
SELECT (col1 + col2)
FROM tab2"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("(col1 + col2)", "tab1"),
            ),
            (
                TestColumnQualifierTuple("col2", "tab2"),
                TestColumnQualifierTuple("(col1 + col2)", "tab1"),
            ),
        ],
    )
    sql = """INSERT INTO tab1
SELECT (col1 + col2) AS col3
FROM tab2"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("col3", "tab1"),
            ),
            (
                TestColumnQualifierTuple("col2", "tab2"),
                TestColumnQualifierTuple("col3", "tab1"),
            ),
        ],
    )


def test_select_column_using_boolean_expression_in_parenthesis():
    sql = """INSERT INTO tab1
SELECT (col1 > 0 AND col2 > 0) AS col3
FROM tab2"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("col3", "tab1"),
            ),
            (
                TestColumnQualifierTuple("col2", "tab2"),
                TestColumnQualifierTuple("col3", "tab1"),
            ),
        ],
    )


def test_select_column_using_expression_with_table_qualifier_without_column_alias():
    sql = """INSERT INTO tab1
SELECT a.col1 + a.col2 + a.col3 + a.col4
FROM tab2 a"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("a.col1 + a.col2 + a.col3 + a.col4", "tab1"),
            ),
            (
                TestColumnQualifierTuple("col2", "tab2"),
                TestColumnQualifierTuple("a.col1 + a.col2 + a.col3 + a.col4", "tab1"),
            ),
            (
                TestColumnQualifierTuple("col3", "tab2"),
                TestColumnQualifierTuple("a.col1 + a.col2 + a.col3 + a.col4", "tab1"),
            ),
            (
                TestColumnQualifierTuple("col4", "tab2"),
                TestColumnQualifierTuple("a.col1 + a.col2 + a.col3 + a.col4", "tab1"),
            ),
        ],
    )


def test_select_column_using_case_when():
    sql = """INSERT INTO tab1
SELECT CASE WHEN col1 = 1 THEN 'V1' WHEN col1 = 2 THEN 'V2' END
FROM tab2"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple(
                    "CASE WHEN col1 = 1 THEN 'V1' WHEN col1 = 2 THEN 'V2' END", "tab1"
                ),
            ),
        ],
    )
    sql = """INSERT INTO tab1
SELECT CASE WHEN col1 = 1 THEN 'V1' WHEN col1 = 2 THEN 'V2' END AS col2
FROM tab2"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("col2", "tab1"),
            )
        ],
    )


def test_select_column_using_case_when_with_subquery():
    sql = """INSERT INTO tab1
SELECT CASE WHEN (SELECT avg(col1) FROM tab3) > 0 AND col2 = 1 THEN (SELECT avg(col1) FROM tab3) ELSE 0 END AS col1
FROM tab4"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col2", "tab4"),
                TestColumnQualifierTuple("col1", "tab1"),
            ),
            (
                TestColumnQualifierTuple("col1", "tab3"),
                TestColumnQualifierTuple("col1", "tab1"),
            ),
        ],
    )


def test_select_column_using_multiple_case_when_with_subquery():
    sql = """INSERT INTO tab1
SELECT CASE
WHEN (SELECT avg(col1) FROM tab3) > 0 AND col2 = 1 THEN (SELECT avg(col1) FROM tab3)
WHEN (SELECT avg(col1) FROM tab3) > 0 AND col2 = 1 THEN (SELECT avg(col1) FROM tab5) ELSE 0 END AS col1
FROM tab4"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col2", "tab4"),
                TestColumnQualifierTuple("col1", "tab1"),
            ),
            (
                TestColumnQualifierTuple("col1", "tab3"),
                TestColumnQualifierTuple("col1", "tab1"),
            ),
            (
                TestColumnQualifierTuple("col1", "tab5"),
                TestColumnQualifierTuple("col1", "tab1"),
            ),
        ],
    )


def test_select_column_with_table_qualifier():
    sql = """INSERT INTO tab1
SELECT tab2.col1
FROM tab2"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("col1", "tab1"),
            )
        ],
    )
    sql = """INSERT INTO tab1
SELECT t.col1
FROM tab2 AS t"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("col1", "tab1"),
            )
        ],
    )


def test_select_columns():
    sql = """INSERT INTO tab1
SELECT col1,
col2
FROM tab2"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("col1", "tab1"),
            ),
            (
                TestColumnQualifierTuple("col2", "tab2"),
                TestColumnQualifierTuple("col2", "tab1"),
            ),
        ],
    )
    sql = """INSERT INTO tab1
SELECT max(col1),
max(col2)
FROM tab2"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("max(col1)", "tab1"),
            ),
            (
                TestColumnQualifierTuple("col2", "tab2"),
                TestColumnQualifierTuple("max(col2)", "tab1"),
            ),
        ],
    )


def test_select_column_in_subquery():
    sql = """INSERT INTO tab1
SELECT col1
FROM (SELECT col1 FROM tab2) dt"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("col1", "tab1"),
            )
        ],
    )
    sql = """INSERT INTO tab1
SELECT col1
FROM (SELECT col1, col2 FROM tab2) dt"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("col1", "tab1"),
            )
        ],
    )
    sql = """INSERT INTO tab1
SELECT col1
FROM (SELECT col1 FROM tab2)"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("col1", "tab1"),
            )
        ],
    )


def test_select_column_in_subquery_with_two_parenthesis():
    sql = """INSERT INTO tab1
SELECT col1
FROM ((SELECT col1 FROM tab2)) dt"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("col1", "tab1"),
            )
        ],
    )


def test_select_column_in_subquery_with_two_parenthesis_and_blank_in_between():
    sql = """INSERT INTO tab1
SELECT col1
FROM (
(SELECT col1 FROM tab2)
) dt"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("col1", "tab1"),
            )
        ],
    )


def test_select_column_in_subquery_with_two_parenthesis_and_union():
    sql = """INSERT INTO tab1
SELECT col1
FROM (
    (SELECT col1 FROM tab2)
    UNION ALL
    (SELECT col1 FROM tab3)
) dt"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("col1", "tab1"),
            ),
            (
                TestColumnQualifierTuple("col1", "tab3"),
                TestColumnQualifierTuple("col1", "tab1"),
            ),
        ],
    )


def test_select_column_in_subquery_with_two_parenthesis_and_union_v2():
    sql = """INSERT INTO tab1
SELECT col1
FROM (
    SELECT col1 FROM tab2
    UNION ALL
    SELECT col1 FROM tab3
) dt"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("col1", "tab1"),
            ),
            (
                TestColumnQualifierTuple("col1", "tab3"),
                TestColumnQualifierTuple("col1", "tab1"),
            ),
        ],
    )


def test_select_column_from_table_join():
    sql = """INSERT INTO tab1
SELECT tab2.col1,
       tab3.col2
FROM tab2
         INNER JOIN tab3
                    ON tab2.id = tab3.id"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("col1", "tab1"),
            ),
            (
                TestColumnQualifierTuple("col2", "tab3"),
                TestColumnQualifierTuple("col2", "tab1"),
            ),
        ],
    )
    sql = """INSERT INTO tab1
SELECT tab2.col1 AS col3,
       tab3.col2 AS col4
FROM tab2
         INNER JOIN tab3
                    ON tab2.id = tab3.id"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("col3", "tab1"),
            ),
            (
                TestColumnQualifierTuple("col2", "tab3"),
                TestColumnQualifierTuple("col4", "tab1"),
            ),
        ],
    )
    sql = """INSERT INTO tab1
SELECT a.col1 AS col3,
       b.col2 AS col4
FROM tab2 a
         INNER JOIN tab3 b
                    ON a.id = b.id"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("col3", "tab1"),
            ),
            (
                TestColumnQualifierTuple("col2", "tab3"),
                TestColumnQualifierTuple("col4", "tab1"),
            ),
        ],
    )


def test_select_column_without_table_qualifier_from_table_join():
    sql = """INSERT INTO tab1
SELECT col1
FROM tab2 a
         INNER JOIN tab3 b
                    ON a.id = b.id"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", None),
                TestColumnQualifierTuple("col1", "tab1"),
            )
        ],
    )


def test_select_column_from_same_table_multiple_time_using_different_alias():
    sql = """INSERT INTO tab1
SELECT a.col1 AS col2,
       b.col1 AS col3
FROM tab2 a
         JOIN tab2 b
              ON a.parent_id = b.id"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("col2", "tab1"),
            ),
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("col3", "tab1"),
            ),
        ],
    )


def test_comment_after_column_comma_first():
    sql = """INSERT INTO tab1
SELECT a.col1
       --, a.col2
       , a.col3
FROM tab2 a"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("col1", "tab1"),
            ),
            (
                TestColumnQualifierTuple("col3", "tab2"),
                TestColumnQualifierTuple("col3", "tab1"),
            ),
        ],
    )


def test_comment_after_column_comma_last():
    sql = """INSERT INTO tab1
SELECT a.col1,
       -- a.col2,
       a.col3
FROM tab2 a"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("col1", "tab1"),
            ),
            (
                TestColumnQualifierTuple("col3", "tab2"),
                TestColumnQualifierTuple("col3", "tab1"),
            ),
        ],
    )


def test_cast_with_comparison():
    sql = """INSERT INTO tab1
SELECT cast(col1 = 1 AS int) col1, col2 = col3 col2
FROM tab2"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("col1", "tab1"),
            ),
            (
                TestColumnQualifierTuple("col2", "tab2"),
                TestColumnQualifierTuple("col2", "tab1"),
            ),
            (
                TestColumnQualifierTuple("col3", "tab2"),
                TestColumnQualifierTuple("col2", "tab1"),
            ),
        ],
    )


@pytest.mark.parametrize("dtype", ["string", "timestamp", "date", "decimal(18, 0)"])
def test_cast_to_data_type(dtype: str):
    sql = f"""INSERT INTO tab1
SELECT cast(col1 as {dtype}) AS col1
FROM tab2"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("col1", "tab1"),
            )
        ],
    )


@pytest.mark.parametrize("dtype", ["string", "timestamp", "date", "decimal(18, 0)"])
def test_nested_cast_to_data_type(dtype: str):
    sql = f"""INSERT INTO tab1
SELECT cast(cast(col1 AS {dtype}) AS {dtype}) AS col1
FROM tab2"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("col1", "tab1"),
            )
        ],
    )
    sql = f"""INSERT INTO tab1
SELECT cast(cast(cast(cast(cast(col1 AS {dtype}) AS {dtype}) AS {dtype}) AS {dtype}) AS {dtype}) AS col1
FROM tab2"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("col1", "tab1"),
            )
        ],
    )


@pytest.mark.parametrize("dtype", ["string", "timestamp", "date", "decimal(18, 0)"])
def test_cast_to_data_type_with_case_when(dtype: str):
    sql = f"""INSERT INTO tab1
SELECT cast(case when col1 > 0 then col2 else col3 end as {dtype}) AS col1
FROM tab2"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("col1", "tab1"),
            ),
            (
                TestColumnQualifierTuple("col2", "tab2"),
                TestColumnQualifierTuple("col1", "tab1"),
            ),
            (
                TestColumnQualifierTuple("col3", "tab2"),
                TestColumnQualifierTuple("col1", "tab1"),
            ),
        ],
    )


def test_cast_using_constant():
    sql = """INSERT INTO tab1
SELECT cast('2012-12-21' AS date) AS col2"""
    assert_column_lineage_equal(sql)


def test_postgres_style_type_cast():
    sql = """INSERT INTO tab1
SELECT col1::timestamp
FROM tab2"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("col1", "tab1"),
            )
        ],
    )


def test_window_function_in_subquery():
    sql = """INSERT INTO tab1
SELECT rn FROM (
    SELECT
        row_number() over (partition BY col1, col2) rn
    FROM tab2
) sub
WHERE rn = 1"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("rn", "sub", is_subquery=True),
                TestColumnQualifierTuple("rn", "tab1"),
            ),
        ],
        test_sqlparse=False,
    )


def test_invalid_syntax_as_without_alias():
    sql = """INSERT INTO tab1
SELECT col1,
       col2 AS,
       col3
FROM tab2"""
    # just assure no exception, don't guarantee the result
    LineageRunner(sql, dialect=SQLPARSE_DIALECT).print_column_lineage()


def test_column_with_ctas_and_func():
    sql = """CREATE TABLE tab2 AS
SELECT
  coalesce(col1, 0) AS col1,
  if(
    col1 IS NOT NULL,
    1,
    NULL
  ) AS col2
FROM
  tab1"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab1"),
                TestColumnQualifierTuple("col1", "tab2"),
            ),
            (
                TestColumnQualifierTuple("col1", "tab1"),
                TestColumnQualifierTuple("col2", "tab2"),
            ),
        ],
    )


def test_column_reference_from_cte_using_qualifier():
    sql = """WITH wtab1 AS (SELECT col1 FROM tab2)
INSERT INTO tab1
SELECT wtab1.col1 FROM wtab1"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("col1", "tab1"),
            )
        ],
    )


def test_column_reference_from_cte_using_alias():
    sql = """WITH wtab1 AS (SELECT col1 FROM tab2)
INSERT INTO tab1
SELECT wt.col1 FROM wtab1 wt"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("col1", "tab1"),
            )
        ],
    )


def test_column_reference_from_previous_defined_cte():
    sql = """WITH
cte1 AS (SELECT a FROM tab1),
cte2 AS (SELECT a FROM cte1)
INSERT INTO tab2
SELECT a FROM cte2"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("a", "tab1"),
                TestColumnQualifierTuple("a", "tab2"),
            )
        ],
    )


def test_multiple_column_references_from_previous_defined_cte():
    sql = """WITH
cte1 AS (SELECT a, b FROM tab1),
cte2 AS (SELECT a, max(b) AS b_max, count(b) AS b_cnt FROM cte1 GROUP BY a)
INSERT INTO tab2
SELECT cte1.a, cte2.b_max, cte2.b_cnt FROM cte1 JOIN cte2
WHERE cte1.a = cte2.a"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("a", "tab1"),
                TestColumnQualifierTuple("a", "tab2"),
            ),
            (
                TestColumnQualifierTuple("b", "tab1"),
                TestColumnQualifierTuple("b_max", "tab2"),
            ),
            (
                TestColumnQualifierTuple("b", "tab1"),
                TestColumnQualifierTuple("b_cnt", "tab2"),
            ),
        ],
    )


def test_column_reference_with_ansi89_join():
    sql = """INSERT INTO tab3
SELECT a.id,
       a.name AS name1,
       b.name AS name2
FROM (SELECT id, name
      FROM tab1) a,
     (SELECT id, name
      FROM tab2) b
WHERE a.id = b.id"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("id", "tab1"),
                TestColumnQualifierTuple("id", "tab3"),
            ),
            (
                TestColumnQualifierTuple("name", "tab1"),
                TestColumnQualifierTuple("name1", "tab3"),
            ),
            (
                TestColumnQualifierTuple("name", "tab2"),
                TestColumnQualifierTuple("name2", "tab3"),
            ),
        ],
    )


def test_smarter_column_resolution_using_query_context():
    sql = """WITH
cte1 AS (SELECT a, b FROM tab1),
cte2 AS (SELECT c, d FROM tab2)
INSERT INTO tab3
SELECT b, d FROM cte1 JOIN cte2
WHERE cte1.a = cte2.c"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("b", "tab1"),
                TestColumnQualifierTuple("b", "tab3"),
            ),
            (
                TestColumnQualifierTuple("d", "tab2"),
                TestColumnQualifierTuple("d", "tab3"),
            ),
        ],
    )


def test_column_reference_using_union():
    sql = """INSERT INTO tab3
SELECT col1
FROM tab1
UNION ALL
SELECT col1
FROM tab2"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab1"),
                TestColumnQualifierTuple("col1", "tab3"),
            ),
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("col1", "tab3"),
            ),
        ],
    )
    sql = """INSERT INTO tab3
SELECT col1
FROM tab1
UNION
SELECT col1
FROM tab2"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab1"),
                TestColumnQualifierTuple("col1", "tab3"),
            ),
            (
                TestColumnQualifierTuple("col1", "tab2"),
                TestColumnQualifierTuple("col1", "tab3"),
            ),
        ],
    )


def test_column_lineage_multiple_paths_for_same_column():
    sql = """INSERT INTO tab2
SELECT tab1.id,
       coalesce(join_table_1.col1, join_table_2.col1, join_table_3.col1) AS col1
FROM tab1
         LEFT JOIN (SELECT id, col1 FROM tab1 WHERE flag = 1) AS join_table_1
                   ON tab1.id = join_table_1.id
         LEFT JOIN (SELECT id, col1 FROM tab1 WHERE flag = 2) AS join_table_2
                   ON tab1.id = join_table_2.id
         LEFT JOIN (SELECT id, col1 FROM tab1 WHERE flag = 3) AS join_table_3
                   ON tab1.id = join_table_3.id"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("id", "tab1"),
                TestColumnQualifierTuple("id", "tab2"),
            ),
            (
                TestColumnQualifierTuple("col1", "tab1"),
                TestColumnQualifierTuple("col1", "tab2"),
            ),
        ],
    )


@pytest.mark.parametrize(
    "func",
    [
        "coalesce(col1, 0) as varchar",
        "if(col1 > 100, 100, col1) as varchar",
        "ln(col1) as varchar",
        "conv(col1, 10, 2) as varchar",
        "ln(cast(coalesce(col1, '0') as int)) as varchar",
        "coalesce(col1, 0) as decimal(10, 6)",
    ],
)
def test_column_try_cast_with_func(func: str):
    sql = f"""INSERT INTO tab2
SELECT try_cast({func}) AS col2
FROM tab1"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "tab1"),
                TestColumnQualifierTuple("col2", "tab2"),
            ),
        ],
    )


def test_merge_into_update():
    sql = """MERGE INTO target
USING src ON target.k = src.k
WHEN MATCHED THEN UPDATE SET target.v = src.v"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("v", "src"),
                TestColumnQualifierTuple("v", "target"),
            )
        ],
    )


def test_merge_into_update_multiple_columns():
    sql = """MERGE INTO target
USING src ON target.k = src.k
WHEN MATCHED THEN UPDATE SET target.v = src.v, target.v1 = src.v1"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("v", "src"),
                TestColumnQualifierTuple("v", "target"),
            ),
            (
                TestColumnQualifierTuple("v1", "src"),
                TestColumnQualifierTuple("v1", "target"),
            ),
        ],
    )


def test_merge_into_update_multiple_columns_with_constant():
    sql = """MERGE INTO target
USING src ON target.k = src.k
WHEN MATCHED THEN UPDATE SET target.v = src.v, target.v1 = 1"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("v", "src"),
                TestColumnQualifierTuple("v", "target"),
            )
        ],
    )
    sql = """MERGE INTO target
USING src ON target.k = src.k
WHEN MATCHED THEN UPDATE SET target.v1 = 1, target.v = src.v"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("v", "src"),
                TestColumnQualifierTuple("v", "target"),
            )
        ],
    )


def test_merge_into_update_multiple_match():
    sql = """MERGE INTO target
USING src ON target.k = src.k
WHEN MATCHED AND src.v0=1 THEN UPDATE SET target.v = src.v
WHEN MATCHED AND src.v0=2 THEN UPDATE SET target.v1 = src.v1"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("v", "src"),
                TestColumnQualifierTuple("v", "target"),
            ),
            (
                TestColumnQualifierTuple("v1", "src"),
                TestColumnQualifierTuple("v1", "target"),
            ),
        ],
    )


def test_merge_into_insert():
    sql = """MERGE INTO target
USING src ON target.k = src.k
WHEN NOT MATCHED THEN INSERT (k, v) VALUES (src.k, src.v)"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("k", "src"),
                TestColumnQualifierTuple("k", "target"),
            ),
            (
                TestColumnQualifierTuple("v", "src"),
                TestColumnQualifierTuple("v", "target"),
            ),
        ],
    )


def test_merge_into_insert_with_constant():
    sql = """MERGE INTO target
USING src ON target.k = src.k
WHEN NOT MATCHED THEN INSERT (k, v) VALUES (src.k, 1)"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("k", "src"),
                TestColumnQualifierTuple("k", "target"),
            )
        ],
    )
    sql = """MERGE INTO target
USING src ON target.k = src.k
WHEN NOT MATCHED THEN INSERT (v, k) VALUES (1, src.k)"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("k", "src"),
                TestColumnQualifierTuple("k", "target"),
            )
        ],
    )


def test_merge_into_insert_one_column():
    sql = """MERGE INTO target
USING src ON target.k = src.k
WHEN NOT MATCHED THEN INSERT (k) VALUES (src.k)"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("k", "src"),
                TestColumnQualifierTuple("k", "target"),
            )
        ],
    )


def test_merge_into_using_subquery():
    sql = """MERGE INTO target USING (select k, max(v) as v_max from src group by k) AS b ON target.k = b.k
WHEN MATCHED THEN UPDATE SET target.v = b.v_max
WHEN NOT MATCHED THEN INSERT (k, v) VALUES (b.k, b.v_max)"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("v", "src"),
                TestColumnQualifierTuple("v", "target"),
            ),
            (
                TestColumnQualifierTuple("k", "src"),
                TestColumnQualifierTuple("k", "target"),
            ),
        ],
    )


def test_union_inside_cte():
    sql = """INSERT INTO dataset.target WITH temp_cte AS (SELECT col1 FROM dataset.tab1 UNION ALL
SELECT col1 FROM dataset.tab2) SELECT col1 FROM temp_cte"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("col1", "dataset.tab1"),
                TestColumnQualifierTuple("col1", "dataset.target"),
            ),
            (
                TestColumnQualifierTuple("col1", "dataset.tab2"),
                TestColumnQualifierTuple("col1", "dataset.target"),
            ),
        ],
    )


def test_create_view_with_complex_sub_queries():
    sql = """create view new_table as select col1 from (
    select col1 from (
        select c1 col1 from tab1
        UNION
        select c11 col1 from tab2
    ) as my_tab_inner
) as my_tab"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("c1", "tab1"),
                TestColumnQualifierTuple("col1", "new_table"),
            ),
            (
                TestColumnQualifierTuple("c11", "tab2"),
                TestColumnQualifierTuple("col1", "new_table"),
            ),
        ],
    )


def test_sqlfluff_create_view_with_complex_sub_queries():
    # sqlparse does not recognize the column definitions made for views
    # for example cc1 column in this test
    sql = """create view new_table (cc1) as select col1 from (
    select col1 from (
        select c1 col1 from tab1
        UNION
        select c11 col1 from tab2
    ) as my_tab_inner
) as my_tab"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("c1", "tab1"),
                TestColumnQualifierTuple("cc1", "new_table"),
            ),
            (
                TestColumnQualifierTuple("c11", "tab2"),
                TestColumnQualifierTuple("cc1", "new_table"),
            ),
        ],
        test_sqlparse=False,
    )


def test_insert_with_cte():
    sql = """insert into xyz (a,b,c)
        with cte as (select p as x, q as y, r as z from abc)
        select x,y,z from cte
    """
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("p", "abc"),
                TestColumnQualifierTuple("a", "xyz"),
            ),
            (
                TestColumnQualifierTuple("q", "abc"),
                TestColumnQualifierTuple("b", "xyz"),
            ),
            (
                TestColumnQualifierTuple("r", "abc"),
                TestColumnQualifierTuple("c", "xyz"),
            ),
        ],
        test_sqlparse=False,
    )


def test_alias_with_casing():
    sql = """create or replace view trg_tbl as
        SELECT
            ldlg.ld_leg_id
            ,stpp.PICK_ARVL_RPTD_DTT Actual_Pickup_Arrival
            ,stpp.PICK_DPTR_RPTD_DTT Actual_Pickup_Departure
        FROM src_tbl_1 ldlg
        LEFT JOIN src_tbl_2 STPP
            ON ldlg.PICK_STOP_ID = stpp.STOP_ID
        WHERE ldlg.LGST_GRP_CD = 'GEC'
        AND ldlg.LD_LEG_ID IS NOT NULL
    """
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("ld_leg_id", "src_tbl_1"),
                TestColumnQualifierTuple("ld_leg_id", "trg_tbl"),
            ),
            (
                TestColumnQualifierTuple("PICK_ARVL_RPTD_DTT", "src_tbl_2"),
                TestColumnQualifierTuple("Actual_Pickup_Arrival", "trg_tbl"),
            ),
            (
                TestColumnQualifierTuple("PICK_DPTR_RPTD_DTT", "src_tbl_2"),
                TestColumnQualifierTuple("Actual_Pickup_Departure", "trg_tbl"),
            ),
        ],
        test_sqlparse=False,
    )
