import pytest

from collate_sqllineage.core.models import DataFunction
from .helpers import assert_table_lineage_equal

"""
This test class will contain all the tests for testing 'Select Queries' where the dialect is not ANSI.
"""


@pytest.mark.parametrize(
    "dialect", ["athena", "bigquery", "databricks", "hive", "mysql", "sparksql"]
)
def test_select_with_table_name_in_backtick(dialect: str):
    assert_table_lineage_equal(
        "SELECT * FROM `tab1`",
        {"tab1"},
        dialect=dialect,
        # TODO: Remove once SqlGlot adds support for backtick identifiers in Athena dialect
        test_sqlglot=False,
    )


@pytest.mark.parametrize(
    "dialect", ["athena", "bigquery", "databricks", "hive", "mysql", "sparksql"]
)
def test_select_with_schema_in_backtick(dialect: str):
    assert_table_lineage_equal(
        "SELECT col1 FROM `schema1`.`tab1`",
        {"schema1.tab1"},
        dialect=dialect,
        # TODO: Remove once SqlGlot adds support for backtick identifiers in Athena dialect
        test_sqlglot=False,
    )


# Duplicate test with Athena excluded as it doesn't support backtick identifiers in SqlGlot
# TODO: Remove duplicate test once SqlGlot adds support for backtick identifiers in Athena dialect
@pytest.mark.parametrize(
    "dialect", ["bigquery", "databricks", "hive", "mysql", "sparksql"]
)
def test_select_with_table_name_in_backtick_sqlglot(dialect: str):
    assert_table_lineage_equal(
        "SELECT * FROM `tab1`",
        {"tab1"},
        dialect=dialect,
    )


# Duplicate test with Athena excluded as it doesn't support backtick identifiers in SqlGlot
# TODO: Remove duplicate test once SqlGlot adds support for backtick identifiers in Athena dialect
@pytest.mark.parametrize(
    "dialect", ["bigquery", "databricks", "hive", "mysql", "sparksql"]
)
def test_select_with_schema_in_backtick_sqlglot(dialect: str):
    assert_table_lineage_equal(
        "SELECT col1 FROM `schema1`.`tab1`",
        {"schema1.tab1"},
        dialect=dialect,
    )


@pytest.mark.parametrize("dialect", ["databricks", "hive", "sparksql"])
def test_select_left_semi_join(dialect: str):
    assert_table_lineage_equal(
        "SELECT * FROM tab1 LEFT SEMI JOIN tab2", {"tab1", "tab2"}, dialect=dialect
    )


@pytest.mark.parametrize("dialect", ["databricks", "hive", "sparksql"])
def test_select_left_semi_join_with_on(dialect: str):
    assert_table_lineage_equal(
        "SELECT * FROM tab1 LEFT SEMI JOIN tab2 ON (tab1.col1 = tab2.col2)",
        {"tab1", "tab2"},
        dialect=dialect,
    )


@pytest.mark.parametrize("dialect", ["snowflake"])
def test_select_from_generator(dialect: str):
    # generator is Snowflake specific
    sql = """SELECT seq4(), uniform(1, 10, random(12))
FROM table(generator()) v
ORDER BY 1;"""
    assert_table_lineage_equal(
        sql, {DataFunction("generator")}, dialect=dialect, test_sqlparse=False
    )


@pytest.mark.parametrize("dialect", ["postgres", "redshift", "tsql"])
def test_select_into(dialect: str):
    """
    postgres: https://www.postgresql.org/docs/current/sql-selectinto.html
    redshift: https://docs.aws.amazon.com/redshift/latest/dg/r_SELECT_INTO.html
    tsql: https://learn.microsoft.com/en-us/sql/t-sql/queries/select-into-clause-transact-sql?view=sql-server-ver16
    """
    sql = "SELECT * INTO films_recent FROM films WHERE date_prod >= '2002-01-01'"
    assert_table_lineage_equal(sql, {"films"}, {"films_recent"}, dialect=dialect)


@pytest.mark.parametrize("dialect", ["redshift"])
def test_redshift_system_types_cast(dialect: str):
    """
    Test Redshift support for PostgreSQL system types in cast expressions.
    Redshift inherits these from PostgreSQL for catalog table queries.
    """
    assert_table_lineage_equal(
        "SELECT relname FROM pg_class pc WHERE pc.oid = '1234'::oid",
        {"pg_class"},
        dialect=dialect,
        test_sqlparse=False,
    )
    assert_table_lineage_equal(
        "SELECT 'proname'::regproc, 'pg_class'::regclass, 'int4'::regtype FROM mytable",
        {"mytable"},
        dialect=dialect,
        test_sqlparse=False,
    )
    # Skip: SqlGlot doesn't support PostgreSQL internal types: cid, tid, xid, regprocedure
    # TODO: Work on adding support in SqlGlot parser for these types
    assert_table_lineage_equal(
        "SELECT p.oid::regprocedure AS proc_oid, '1'::cid, '1'::tid, '1'::xid FROM pg_proc p",
        {"pg_proc"},
        dialect=dialect,
        test_sqlparse=False,
        test_sqlglot=False,
    )
    assert_table_lineage_equal(
        "SELECT relname::name FROM pg_class",
        {"pg_class"},
        dialect=dialect,
        test_sqlparse=False,
    )


@pytest.mark.parametrize("dialect", ["redshift"])
def test_redshift_quoted_identifier_types(dialect: str):
    """
    Test Redshift support for quoted identifier types like "char".
    Used in PostgreSQL catalog queries where "char" is a single-byte internal type.
    """
    assert_table_lineage_equal(
        """SELECT relname FROM pg_class
WHERE relkind = 'r'::"char" OR relkind = 'v'::"char" """,
        {"pg_class"},
        dialect=dialect,
        test_sqlparse=False,
    )
    assert_table_lineage_equal(
        """SELECT CASE
    WHEN relkind = 'r'::"char" THEN 'table'::text
    ELSE 'view'::text
END AS objtype
FROM pg_class""",
        {"pg_class"},
        dialect=dialect,
        test_sqlparse=False,
    )


@pytest.mark.parametrize("dialect", ["redshift"])
def test_redshift_array_types_cast(dialect: str):
    """
    Test Redshift support for array types with [] notation in cast expressions.
    """
    # Skip: SqlGlot doesn't support aclitem[] array type
    # TODO: Work on adding support in SqlGlot parser for these types
    assert_table_lineage_equal(
        "SELECT defaclacl FROM pg_default_acl WHERE defaclacl = '{}'::aclitem[]",
        {"pg_default_acl"},
        dialect=dialect,
        test_sqlparse=False,
        test_sqlglot=False,
    )
    assert_table_lineage_equal(
        """SELECT '{1,2,3}'::integer[] AS numbers,
ARRAY['a','b','c']::text[] AS letters
FROM mytable""",
        {"mytable"},
        dialect=dialect,
        test_sqlparse=False,
    )
    assert_table_lineage_equal(
        """SELECT ARRAY['hello','world']::varchar(100)[] AS words,
ARRAY[ARRAY[1,2],ARRAY[3,4]]::integer[][] AS matrix
FROM mytable""",
        {"mytable"},
        dialect=dialect,
        test_sqlparse=False,
    )
