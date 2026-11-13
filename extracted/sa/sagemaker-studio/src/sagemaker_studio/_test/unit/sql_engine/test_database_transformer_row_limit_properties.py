"""Generated-domain tests for DatabaseTransformer.apply_row_limit / apply_row_limits.

Example-based cases live in test_database_transformer_row_limit.py. Hypothesis is not a
declared test dependency, so each domain is enumerated with pytest.mark.parametrize.
"""

from typing import Any, List, Optional

import pytest
import sqlglot
from sqlglot import exp

from sagemaker_studio._test.unit.sql_engine.test_database_transformer_row_limit import (
    _Generic,
    _Oracle,
    _statement_type,
)
from sagemaker_studio.sql_engine.database_transformer import SqlStatement


class _GenericOptedOut(_Generic):
    """No dialect and opted out: the flag alone must decide."""

    supports_row_limit = False


class _RedshiftOptedOut(_Generic):
    """A real dialect and opted out: the dialect must not override the flag."""

    supports_row_limit = False

    @classmethod
    def get_dialect(cls) -> Optional[str]:
        return "redshift"


def _type_of(statement: str) -> str:
    """The statement_type split_query assigns, including its UNKNOWN parse fallback."""
    try:
        return _statement_type(statement)
    except Exception:
        return "UNKNOWN"


def _limit_of(node: exp.Expression) -> int:
    """The row count in a node's limit argument, whichever clause spells it."""
    limit = node.args.get("limit")
    count = limit.args.get("count") if isinstance(limit, exp.Fetch) else limit.expression
    return int(count.this)


def _args_without_limit(node: exp.Expression) -> dict:
    return {key: value for key, value in node.args.items() if key != "limit"}


# Every value that is not a positive int, so every value that must disable the transform.
NO_LIMIT_VALUES = [None, 0, -1, -100, True, False, 100.0, 10.5, "100", ""]
NO_LIMIT_IDS = [
    "none",
    "zero",
    "minus_one",
    "minus_hundred",
    "true",
    "false",
    "float_whole",
    "float_fraction",
    "str_digits",
    "str_empty",
]

# Plain and modified SELECTs, CTEs, each set operation, an author-supplied limit, DML, DDL,
# read-only statements outside the limitable families, and unparseable text.
IDENTITY_STATEMENTS = [
    "SELECT a FROM t",
    "SELECT a FROM t ORDER BY a",
    "SELECT a FROM t OFFSET 10",
    "WITH c AS (SELECT a FROM t) SELECT a FROM c",
    "SELECT a FROM t UNION SELECT b FROM u",
    "SELECT a FROM t INTERSECT SELECT b FROM u",
    "SELECT a FROM t EXCEPT SELECT b FROM u",
    "(SELECT a FROM t) UNION (SELECT b FROM u)",
    "SELECT a FROM t LIMIT 5",
    'SELECT "x y" FROM db.sch."t t"',
    "SELECT /* keep me */ a FROM t",
    "INSERT INTO z SELECT a FROM t",
    "CREATE TABLE z AS SELECT a FROM t",
    "UPDATE t SET a = 1",
    "DELETE FROM t",
    "CREATE TABLE t (a INT)",
    "SHOW TABLES",
    "DESCRIBE t",
    "VALUES (1), (2)",
    "SELCT a FROM t",
    "",
]
IDENTITY_IDS = [
    "select",
    "select_order_by",
    "select_offset",
    "cte_select",
    "union",
    "intersect",
    "except",
    "parenthesized_union",
    "existing_limit",
    "quoted_qualified",
    "comment",
    "insert_select",
    "ctas",
    "update",
    "delete",
    "ddl",
    "show",
    "describe",
    "values",
    "malformed",
    "empty",
]

# Read-only statements carrying no limit argument of their own, and with a trailing
# position for the clause. "SELECT a FROM t OFFSET 10" was a member until the offset gate
# landed; it now belongs to NO_TRAILING_POSITION_STATEMENTS below.
UNLIMITED_STATEMENTS = [
    "SELECT a FROM t",
    "SELECT a, b FROM t WHERE a > 1 ORDER BY a",
    "WITH c AS (SELECT a FROM t) SELECT a FROM c",
    "SELECT a FROM t UNION SELECT b FROM u",
    "SELECT a FROM t INTERSECT SELECT b FROM u",
    "SELECT a FROM t EXCEPT SELECT b FROM u",
    "(SELECT a FROM t) UNION (SELECT b FROM u)",
    "SELECT a, COUNT(*) FROM t GROUP BY a HAVING COUNT(*) > 1",
]
UNLIMITED_IDS = [
    "select",
    "select_where_order_by",
    "cte_select",
    "union",
    "intersect",
    "except",
    "parenthesized_union",
    "group_by_having",
]

# Read-only statements with no trailing position (locking read, SELECT ... INTO, bare
# OFFSET). Identity must hold for every positive limit.
NO_TRAILING_POSITION_STATEMENTS = [
    "SELECT a FROM t FOR UPDATE",
    "SELECT a INTO new_table FROM t",
    "SELECT a FROM t OFFSET 10",
    "SELECT a FROM t ORDER BY a OFFSET 10",
    "SELECT a FROM t UNION SELECT b FROM u OFFSET 5",
]
NO_TRAILING_POSITION_IDS = [
    "locking_read",
    "select_into",
    "select_offset",
    "select_order_by_offset",
    "union_offset",
]

# There is no upper bound on the limit, so 10**18 belongs in the domain.
POSITIVE_LIMITS = [1, 100, 10**18]
POSITIVE_LIMIT_IDS = ["one", "hundred", "quintillion"]


# No effective row limit leaves the statement byte-identical.


@pytest.mark.parametrize("limit", NO_LIMIT_VALUES, ids=NO_LIMIT_IDS)
@pytest.mark.parametrize("statement", IDENTITY_STATEMENTS, ids=IDENTITY_IDS)
def test_no_effective_limit_is_identity(statement, limit):
    assert _Generic.apply_row_limit(statement, _type_of(statement), limit) == statement


@pytest.mark.parametrize("statement", IDENTITY_STATEMENTS, ids=IDENTITY_IDS)
def test_absent_limit_argument_is_identity(statement):
    # The parameter is not passed at all.
    assert _Generic.apply_row_limit(statement, _type_of(statement)) == statement


# A read-only statement with no limit gains exactly the requested limit.


@pytest.mark.parametrize("limit", POSITIVE_LIMITS, ids=POSITIVE_LIMIT_IDS)
@pytest.mark.parametrize("statement", UNLIMITED_STATEMENTS, ids=UNLIMITED_IDS)
@pytest.mark.parametrize("transformer", [_Generic, _Oracle], ids=["generic", "oracle"])
def test_unlimited_statement_gains_exactly_the_requested_limit(transformer, statement, limit):
    dialect = transformer.get_dialect()
    original = sqlglot.parse_one(statement, dialect=dialect)

    limited = transformer.apply_row_limit(statement, _statement_type(statement, dialect), limit)

    node = sqlglot.parse_one(limited, dialect=dialect)
    assert _limit_of(node) == limit
    assert _args_without_limit(node) == _args_without_limit(original)


# A read-only statement with no trailing position keeps its text for every positive limit.


@pytest.mark.parametrize("limit", POSITIVE_LIMITS, ids=POSITIVE_LIMIT_IDS)
@pytest.mark.parametrize("statement", NO_TRAILING_POSITION_STATEMENTS, ids=NO_TRAILING_POSITION_IDS)
@pytest.mark.parametrize("transformer", [_Generic, _Oracle], ids=["generic", "oracle"])
def test_a_statement_with_no_trailing_position_keeps_its_text(transformer, statement, limit):
    dialect = transformer.get_dialect()
    statement_type = _statement_type(statement, dialect)
    # Non-vacuity: the family gate admits these, so only a gate of their own excludes them.
    assert statement_type in {"SELECT", "UNION"}

    assert transformer.apply_row_limit(statement, statement_type, limit) == statement


# The opt-out flag decides eligibility independently of the dialect.


@pytest.mark.parametrize("statement", UNLIMITED_STATEMENTS, ids=UNLIMITED_IDS)
@pytest.mark.parametrize(
    "transformer,eligible",
    [
        (_Generic, True),
        (_Oracle, True),
        (_GenericOptedOut, False),
        (_RedshiftOptedOut, False),
    ],
    ids=["no_dialect_opted_in", "dialect_opted_in", "no_dialect_opted_out", "dialect_opted_out"],
)
def test_opt_out_flag_decides_independently_of_dialect(transformer, eligible, statement):
    dialect = transformer.get_dialect()
    statement_type = _statement_type(statement, dialect)

    limited = transformer.apply_row_limit(statement, statement_type, 100)

    if eligible:
        assert _limit_of(sqlglot.parse_one(limited, dialect=dialect)) == 100
    else:
        assert limited == statement


def test_opt_out_matrix_covers_both_axes():
    # Guards the matrix above: without this, a stub silently losing its dialect or its flag
    # would turn one of the four combinations into a duplicate of another.
    assert (_Generic.get_dialect(), _Generic.supports_row_limit) == (None, True)
    assert (_Oracle.get_dialect(), _Oracle.supports_row_limit) == ("oracle", True)
    assert (_GenericOptedOut.get_dialect(), _GenericOptedOut.supports_row_limit) == (None, False)
    assert (_RedshiftOptedOut.get_dialect(), _RedshiftOptedOut.supports_row_limit) == (
        "redshift",
        False,
    )


# The transformer is total.

# Realistic ways a notebook cell's text arrives broken, plus the two inputs that parse to
# something that is not a query (";;" yields a Block, "''" a Literal), which reach the
# exp.Query guard instead of the exception handler.
TOTALITY_STATEMENTS = [
    "",
    "   ",
    ";",
    "SELECT",
    "SELECT FROM",
    "SELECT a FROM",
    "SELCT a FROM t",
    "SELECT a FROM t WHERE",
    "SELECT * FROM (",
    "with temp as select * from t",
    "-- just a comment",
    "SELECT a FROM t;;",
    "''",
]
TOTALITY_IDS = [
    "empty",
    "whitespace",
    "semicolon",
    "select_only",
    "select_from",
    "select_a_from",
    "misspelled_select",
    "dangling_where",
    "unclosed_paren",
    "cte_missing_parens",
    "comment_only",
    "double_semicolon",
    "empty_string_literal",
]

# Any type, including the types a caller could plausibly pass by mistake.
ANY_LIMIT_VALUES: List[Any] = [None, 100, 0, -5, True, False, 10.5, "100", [100], object()]


@pytest.mark.parametrize("statement_type", ["SELECT", "UNION", "UNKNOWN", "COMMAND", "select", ""])
@pytest.mark.parametrize("statement", TOTALITY_STATEMENTS, ids=TOTALITY_IDS)
def test_transformer_is_total(statement, statement_type):
    for limit in ANY_LIMIT_VALUES:
        result = _Generic.apply_row_limit(statement, statement_type, limit)
        assert isinstance(result, str), (statement, statement_type, limit)


# Per-statement gating is independent of the surrounding statements.
# Statement order, count and type are invariant.

_MIXED = [
    SqlStatement("SELECT a FROM t", "SELECT"),
    SqlStatement("INSERT INTO z SELECT a FROM t", "INSERT"),
    SqlStatement("SELECT b FROM u LIMIT 5", "SELECT"),
    SqlStatement("SELECT c FROM v UNION SELECT d FROM w", "UNION"),
    SqlStatement("UPDATE t SET a = 1", "UPDATE"),
    SqlStatement("SELCT bad", "UNKNOWN"),
]

STATEMENT_LISTS = [
    [],
    [SqlStatement("SELECT a FROM t", "SELECT")],
    _MIXED,
    # Reversed, so an implementation carrying state from one statement to the next would
    # have to produce the same answers in both orders.
    list(reversed(_MIXED)),
    [SqlStatement("SELECT a FROM t", "SELECT")] * 3,
]
STATEMENT_LIST_IDS = ["empty", "single", "mixed", "mixed_reversed", "repeated"]

LIST_LIMITS = [None, 0, 100, True, 10.5]
LIST_LIMIT_IDS = ["none", "zero", "hundred", "true", "float"]


@pytest.mark.parametrize("limit", LIST_LIMITS, ids=LIST_LIMIT_IDS)
@pytest.mark.parametrize("statements", STATEMENT_LISTS, ids=STATEMENT_LIST_IDS)
def test_per_statement_gating_is_independent(statements, limit):
    results = _Generic.apply_row_limits(statements, limit)

    for index, item in enumerate(statements):
        assert results[index].statement == _Generic.apply_row_limit(
            item.statement, item.statement_type, limit
        )


@pytest.mark.parametrize("limit", LIST_LIMITS, ids=LIST_LIMIT_IDS)
@pytest.mark.parametrize("statements", STATEMENT_LISTS, ids=STATEMENT_LIST_IDS)
def test_order_count_and_type_are_invariant(statements, limit):
    results = _Generic.apply_row_limits(statements, limit)

    assert len(results) == len(statements)
    assert [item.statement_type for item in results] == [item.statement_type for item in statements]
