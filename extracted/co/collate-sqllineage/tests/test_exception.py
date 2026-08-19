import warnings

import pytest

from collate_sqllineage.core.parser.sqlfluff.analyzer import SqlFluffLineageAnalyzer
from collate_sqllineage.core.parser.sqlglot.analyzer import SqlGlotLineageAnalyzer
from collate_sqllineage.exceptions import (
    InvalidSyntaxException,
    SQLLineageException,
    UnsupportedStatementException,
)
from collate_sqllineage.runner import LineageRunner


def test_select_without_table():
    with pytest.raises(SQLLineageException):
        LineageRunner("select * from where foo='bar'")._eval()


def test_full_unparsable_query_in_sqlfluff():
    with pytest.raises(InvalidSyntaxException):
        LineageRunner(
            "WRONG SELECT FROM tab1", dialect="ansi", analyzer=SqlFluffLineageAnalyzer
        )._eval()


def test_partial_unparsable_query_in_sqlfluff():
    with pytest.raises(InvalidSyntaxException):
        LineageRunner(
            "SELECT * FROM tab1 AS FULL FULL OUTER JOIN tab2",
            dialect="ansi",
            analyzer=SqlFluffLineageAnalyzer,
        )._eval()


def test_unsupported_query_type_in_sqlfluff():
    with pytest.raises(UnsupportedStatementException):
        LineageRunner(
            "CREATE UNIQUE INDEX title_idx ON films (title)",
            dialect="ansi",
            analyzer=SqlFluffLineageAnalyzer,
        )._eval()


def test_deprecated_warning_in_sqlparse():
    with warnings.catch_warnings(record=True) as w:
        LineageRunner("SELECT * FROM DUAL", dialect="non-validating")._eval()
        assert len(w) == 1
        assert issubclass(w[0].category, DeprecationWarning)


def test_unsupported_syntax_falling_back_to_command_raises_in_sqlglot():
    """sqlglot degrades a statement it cannot parse into a generic Command node.

    A lineage-bearing statement that sqlglot cannot parse must be reported as
    unsupported so callers can fall back to another parser, rather than silently
    yielding empty lineage. Here the Snowflake WITH ROW ACCESS POLICY clause is the
    unsupported syntax. SqlFluff resolves the same statement, see
    test_snowflake_view_with_row_access_policy in test_others_dialect_specific.py.
    """
    sql = """create or replace view VW_TEST(
    COL1,
    COL2
)
WITH ROW ACCESS POLICY POLICYDB.POLICYSCHEMA.POLICYNAME ON (COL2)
as (
    with
    -- Import CTEs
    TEST_TABLE as (
        select * from DB.SCHEMA.PARENT_TABLE
    )
    , final as (
        select
            COL1,
            COL2
        from TEST_TABLE
    )
    select * from final
);"""
    with pytest.raises(UnsupportedStatementException):
        LineageRunner(sql, dialect="snowflake", analyzer=SqlGlotLineageAnalyzer)._eval()


def test_noop_command_does_not_raise_in_sqlglot():
    """A command sqlglot fully parses carries no lineage and stays a silent no-op."""
    for sql, dialect in [
        ("show timezone", "postgres"),
        ("VACUUM ANALYZE tab1", "postgres"),
    ]:
        runner = LineageRunner(sql, dialect=dialect, analyzer=SqlGlotLineageAnalyzer)
        runner._eval()
        assert runner.source_tables == []
        assert runner.target_tables == []
