"""Example-based tests for DatabaseTransformer.apply_row_limit.

Generated-domain coverage lives in test_database_transformer_row_limit_properties.py.
"""

import logging
from typing import Any, Dict, List, Optional
from unittest.mock import patch

import pytest
import sqlglot

from sagemaker_studio.sql_engine.athena_transformer import AthenaTransformer
from sagemaker_studio.sql_engine.big_query_transformer import BigQueryTransformer
from sagemaker_studio.sql_engine.database_transformer import (
    DatabaseTransformer,
    _mask_placeholders,
)
from sagemaker_studio.sql_engine.duckdb_transformer import DuckDBTransformer
from sagemaker_studio.sql_engine.postgresql_transformer import PostgreSQLTransformer
from sagemaker_studio.sql_engine.redshift_transformer import RedshiftTransformer
from sagemaker_studio.sql_engine.resource_fetching_definition import ResourceFetchingDefinition
from sagemaker_studio.sql_engine.spark_transformer import SparkTransformer

LOGGER_NAME = "sagemaker_studio.sql_engine.database_transformer"


class _Generic(DatabaseTransformer):
    """Concrete transformer on the generic dialect; DatabaseTransformer is abstract."""

    # Declared, not inherited: the base default is False, so a stub has to opt in.
    supports_row_limit = True

    @classmethod
    def get_dialect(cls) -> Optional[str]:
        return None

    @staticmethod
    def get_required_fields() -> List[str]:
        return []

    @staticmethod
    def to_sqlalchemy_config(connection_data: Dict[str, Any]) -> Dict[str, Any]:
        return {}

    @staticmethod
    def get_resources_action(
        resource_type: Optional[str], parents: Optional[Dict[str, str]] = None
    ) -> ResourceFetchingDefinition:
        return DatabaseTransformer.get_resources_action(resource_type, parents)


class _Oracle(_Generic):
    @classmethod
    def get_dialect(cls) -> Optional[str]:
        return "oracle"


class _TSql(_Generic):
    @classmethod
    def get_dialect(cls) -> Optional[str]:
        return "tsql"


class _OptedOut(_Generic):
    """A connection type that never participates, the base-class default."""

    supports_row_limit = False


def _statement_type(statement: str, dialect: Optional[str] = None) -> str:
    """The statement_type split_query would assign: stmt.key.upper()."""
    return sqlglot.parse_one(statement, dialect=dialect).key.upper()


# An author-supplied limit is never clamped.


@pytest.mark.parametrize(
    "transformer,statement",
    [
        (_Generic, "SELECT a FROM t LIMIT 5"),
        (_Generic, "SELECT a FROM t LIMIT 1000"),
        (_Oracle, "SELECT a FROM t FETCH FIRST 3 ROWS ONLY"),
        (_TSql, "SELECT TOP 3 a FROM t"),
    ],
    ids=["limit_5_below_n", "limit_1000_above_n", "oracle_fetch_first", "tsql_top"],
)
def test_existing_limit_is_never_clamped(transformer, statement):
    # Identity here is what proves the existing-limit gate runs before anything is appended.
    assert transformer.apply_row_limit(statement, "SELECT", 100) == statement


# Non-read-only statements are never rewritten.


@pytest.mark.parametrize(
    "statement,statement_type",
    [
        ("INSERT INTO z SELECT a FROM t", "INSERT"),
        ("CREATE TABLE z AS SELECT a FROM t", "CREATE"),
        ("UPDATE t SET a = 1", "UPDATE"),
        ("DELETE FROM t", "DELETE"),
        ("SHOW TABLES", "COMMAND"),
        ("DESCRIBE t", "DESCRIBE"),
        ("VALUES (1), (2)", "VALUES"),
        # sqlglot classifies by the operation, not the leading keyword, so these root to
        # insert/update/delete -- a reader of the leading keyword would limit a write.
        ("WITH temp AS (SELECT * FROM t) INSERT INTO t2 SELECT * FROM temp", "INSERT"),
        ("WITH temp AS (SELECT * FROM t) UPDATE t2 SET a = 1", "UPDATE"),
        ("WITH temp AS (SELECT * FROM t) DELETE FROM t2", "DELETE"),
        ("INSERT INTO t2 WITH temp AS (SELECT * FROM t) SELECT * FROM temp", "INSERT"),
        ("CREATE TABLE t2 AS WITH temp AS (SELECT * FROM t) SELECT * FROM temp", "CREATE"),
    ],
    ids=[
        "insert_select",
        "ctas",
        "update",
        "delete",
        "command_show_tables",
        "describe",
        "values",
        "cte_then_insert",
        "cte_then_update",
        "cte_then_delete",
        "insert_with_cte",
        "ctas_with_cte",
    ],
)
def test_non_read_only_statement_is_unchanged(statement, statement_type):
    assert _statement_type(statement) == statement_type
    assert _Generic.apply_row_limit(statement, statement_type, 100) == statement


def test_unknown_statement_type_is_unchanged():
    statement = "with temp as select * from t, insert into t2 as select * from temp"
    assert _Generic.apply_row_limit(statement, "UNKNOWN", 100) == statement


def test_cte_led_select_is_limited():
    # Positive control: the exclusions above must be classification, not a refusal of WITH.
    statement = "WITH temp AS (SELECT * FROM t) SELECT * FROM temp"
    assert _statement_type(statement) == "SELECT"
    assert (
        _Generic.apply_row_limit(statement, "SELECT", 100)
        == "WITH temp AS (SELECT * FROM t) SELECT * FROM temp\nLIMIT 100"
    )


# Read-only statements with no trailing position for the clause. SELECT ... INTO would
# create a table holding n rows; Spark wants LIMIT before OFFSET.

_NO_TRAILING_POSITION = [
    pytest.param("SELECT a INTO new_table FROM t", "into", id="select-into"),
    pytest.param(
        "WITH c AS (SELECT a FROM t) SELECT a INTO new_table FROM c", "into", id="cte-select-into"
    ),
    pytest.param("SELECT a FROM t OFFSET 10", "offset", id="offset"),
    pytest.param("SELECT a FROM t ORDER BY a OFFSET 10", "offset", id="order-by-offset"),
    pytest.param("SELECT a FROM t UNION SELECT b FROM u OFFSET 5", "offset", id="union-offset"),
]

# PostgreSQL and Redshift are the two engines the reviewer named for SELECT ... INTO.
_GATED_TRANSFORMERS = [_Generic, PostgreSQLTransformer, RedshiftTransformer, SparkTransformer]
_GATED_IDS = ["generic", "postgres", "redshift", "spark"]


@pytest.mark.parametrize("statement,argument", _NO_TRAILING_POSITION)
@pytest.mark.parametrize("transformer", _GATED_TRANSFORMERS, ids=_GATED_IDS)
def test_a_statement_with_no_trailing_position_is_unchanged(transformer, statement, argument):
    dialect = transformer.get_dialect()
    # Non-vacuity: the family gate passes and the argument the new gate reads is set, so
    # identity below is this gate's doing rather than an earlier one's.
    node = sqlglot.parse_one(statement, dialect=dialect)
    assert node.key.upper() in {"SELECT", "UNION"}
    assert node.args.get("limit") is None
    assert node.args.get(argument) is not None

    assert transformer.apply_row_limit(statement, node.key.upper(), 100) == statement


# bool rejection and failure fall-through. Requirements: 1.6, 6.1, 6.2, 6.5

STMT = "SELECT a FROM t"


@pytest.mark.parametrize("value", [True, False], ids=["true", "false"])
def test_bool_limit_is_rejected(value):
    # isinstance(True, int) is True, so without the bool gate this would append "LIMIT True".
    assert _Generic.apply_row_limit(STMT, "SELECT", value) == STMT


def _warnings(caplog):
    return [r for r in caplog.records if r.name == LOGGER_NAME and r.levelno == logging.WARNING]


def test_parse_failure_returns_original_and_warns_once(caplog):
    # The statement still runs, unlimited, so the log record is the only signal.
    with patch.object(sqlglot, "parse_one", side_effect=RuntimeError("parse boom")):
        with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
            result = _Generic.apply_row_limit(STMT, "SELECT", 100)
    assert result == STMT

    records = _warnings(caplog)
    assert len(records) == 1
    assert "Row limit not applied" in records[0].getMessage()
    assert "100 rows" in records[0].getMessage()


# Unparseable as written, so split_query types it UNKNOWN; masking makes it a SELECT again.
_MASKS_TO_A_SELECT = "SELECT a FROM t WHERE ts > TIMESTAMP :ts"

# Unparseable masked too, so no family can be assigned by any means: the one real fail-open.
_UNPARSEABLE_EVEN_MASKED = "SELECT a FROM t WHERE b = :n AND (("


def test_a_statement_unparseable_even_when_masked_warns_once(caplog):
    statement = _UNPARSEABLE_EVEN_MASKED
    with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
        assert _Generic.apply_row_limit(statement, "UNKNOWN", 100) == statement

    records = _warnings(caplog)
    assert len(records) == 1
    assert "statement_type=UNKNOWN" in records[0].getMessage()


# The deliberate exclusions are silent; warning per write would bury the one case above.
# The value cases pair a bad limit with UNKNOWN on purpose: only their gate running before
# the statement-type gate keeps them silent, which a SELECT here would not prove.
@pytest.mark.parametrize(
    "transformer,statement,statement_type,limit",
    [
        (_Generic, "INSERT INTO z SELECT a FROM t", "INSERT", 100),
        (_Generic, "SHOW TABLES", "COMMAND", 100),
        (_Generic, "SELECT a FROM t LIMIT 5", "SELECT", 100),
        (_Generic, "SELECT a FROM t FOR UPDATE", "SELECT", 100),
        (_Generic, "SELECT a INTO new_table FROM t", "SELECT", 100),
        (_Generic, "SELECT a FROM t OFFSET 10", "SELECT", 100),
        # An opted-out connection type reaches no gate at all, UNKNOWN or otherwise.
        (_OptedOut, _UNPARSEABLE_EVEN_MASKED, "UNKNOWN", 100),
        (_Generic, _UNPARSEABLE_EVEN_MASKED, "UNKNOWN", None),
        (_Generic, _UNPARSEABLE_EVEN_MASKED, "UNKNOWN", 0),
        (_Generic, _UNPARSEABLE_EVEN_MASKED, "UNKNOWN", -5),
        (_Generic, _UNPARSEABLE_EVEN_MASKED, "UNKNOWN", True),
        (_Generic, _UNPARSEABLE_EVEN_MASKED, "UNKNOWN", "100"),
        # Masked to a write family: a deliberate exclusion, not a limit that went missing.
        (_Generic, "DELETE FROM t WHERE ts > TIMESTAMP :ts", "UNKNOWN", 100),
        (_Generic, "UPDATE t SET a = 1 WHERE ts > TIMESTAMP :ts", "UNKNOWN", 100),
        # Masked to a SELECT the author already limited, and to a locking read.
        (_Generic, "SELECT a FROM t WHERE ts > TIMESTAMP :ts LIMIT 5", "UNKNOWN", 100),
        (_Generic, "SELECT a FROM t WHERE ts > TIMESTAMP :ts FOR UPDATE", "UNKNOWN", 100),
    ],
    ids=[
        "write_statement",
        "command",
        "author_supplied_limit",
        "locking_read",
        "select_into",
        "offset_with_no_limit",
        "opted_out_connection_type",
        "no_limit_requested",
        "zero_limit",
        "negative_limit",
        "bool_limit",
        "non_int_limit",
        "masked_to_delete",
        "masked_to_update",
        "masked_to_an_author_supplied_limit",
        "masked_to_a_locking_read",
    ],
)
def test_deliberate_exclusions_do_not_warn(transformer, statement, statement_type, limit, caplog):
    with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
        assert transformer.apply_row_limit(statement, statement_type, limit) == statement

    assert _warnings(caplog) == []


# The masked parse: classifying a statement split_query could not.

_MASKED_CASES = [
    pytest.param(_MASKS_TO_A_SELECT, True, id="named-timestamp"),
    pytest.param("SELECT a FROM t WHERE d = DATE ?", True, id="positional-date"),
    pytest.param("SELECT a FROM t WHERE b IN (?, ?) AND d = DATE ?", True, id="several-markers"),
    # Every gate below applies to the masked node exactly as to an ordinary one.
    pytest.param(f"{_MASKS_TO_A_SELECT} LIMIT 5", False, id="author-supplied-limit"),
    pytest.param(f"{_MASKS_TO_A_SELECT} FOR UPDATE", False, id="locking-read"),
    pytest.param(f"{_MASKS_TO_A_SELECT} OFFSET 10", False, id="offset-with-no-limit"),
    pytest.param(
        "SELECT a INTO new_table FROM t WHERE ts > TIMESTAMP :ts", False, id="select-into"
    ),
    pytest.param("DELETE FROM t WHERE ts > TIMESTAMP :ts", False, id="delete"),
    pytest.param("UPDATE t SET a = 1 WHERE ts > TIMESTAMP :ts", False, id="update"),
    pytest.param(_UNPARSEABLE_EVEN_MASKED, False, id="unparseable-even-masked"),
]


@pytest.mark.parametrize("statement,expect_limited", _MASKED_CASES)
def test_the_masked_parse_decides_and_the_authors_text_is_returned(statement, expect_limited):
    # Precondition: unparseable as written, which is why split_query hands them over UNKNOWN.
    with pytest.raises(Exception):
        sqlglot.parse_one(statement)

    result = _Generic.apply_row_limit(statement, "UNKNOWN", 100)

    expected = f"{statement}\nLIMIT 100" if expect_limited else statement
    assert result == expected


# Constructs that only look like placeholders. Masking by text would replace them and the
# masked parse would then fail, so the clause landing here is the evidence they were skipped.
_NOT_A_PLACEHOLDER_CASES = [
    pytest.param("SELECT a::VARCHAR FROM t WHERE ts > TIMESTAMP :ts", id="cast-operator"),
    pytest.param("SELECT 'a:b' FROM t WHERE ts > TIMESTAMP :ts", id="colon-in-a-string"),
    pytest.param("SELECT 'what?' FROM t WHERE d = DATE ?", id="question-mark-in-a-string"),
    pytest.param("SELECT a::INT, 'x:y' FROM t WHERE d = DATE ?", id="both-at-once"),
]


@pytest.mark.parametrize("statement", _NOT_A_PLACEHOLDER_CASES)
def test_masking_leaves_casts_and_string_literals_alone(statement):
    assert _Generic.apply_row_limit(statement, "UNKNOWN", 100) == f"{statement}\nLIMIT 100"


def test_masking_runs_only_for_an_unclassified_statement():
    # By call count, not outcome: this statement is limited either way, so only the absent
    # call shows the branch did not run.
    statement = "SELECT a FROM t WHERE b = :name"
    module = "sagemaker_studio.sql_engine.database_transformer._mask_placeholders"

    with patch(module) as mask:
        assert _Generic.apply_row_limit(statement, "SELECT", 100) == f"{statement}\nLIMIT 100"
    assert mask.call_count == 0

    with patch(module, side_effect=_mask_placeholders) as mask:
        _Generic.apply_row_limit(statement, "UNKNOWN", 100)
    assert mask.call_count == 1


@pytest.mark.parametrize(
    "statement,masked",
    [
        ("SELECT a FROM t WHERE ts > TIMESTAMP :ts", "SELECT a FROM t WHERE ts > TIMESTAMP '0'"),
        ("SELECT a FROM t WHERE d = DATE ?", "SELECT a FROM t WHERE d = DATE '0'"),
        # Reverse order matters: masking left to right would invalidate the later offsets.
        (
            "SELECT a FROM t WHERE b IN (?, ?) AND d = DATE ?",
            "SELECT a FROM t WHERE b IN ('0', '0') AND d = DATE '0'",
        ),
        ("SELECT a::VARCHAR FROM t WHERE b = :n", "SELECT a::VARCHAR FROM t WHERE b = '0'"),
        ("SELECT 'a:b' FROM t WHERE b = :n", "SELECT 'a:b' FROM t WHERE b = '0'"),
        ("SELECT 'what?' FROM t WHERE b = ?", "SELECT 'what?' FROM t WHERE b = '0'"),
        # A lone colon with no name after it is not a placeholder and is not masked.
        ("SELECT a FROM t WHERE b = : ", "SELECT a FROM t WHERE b = : "),
        ("SELECT a FROM t", "SELECT a FROM t"),
    ],
    ids=[
        "named",
        "positional",
        "several-markers",
        "cast-operator",
        "colon-in-a-string",
        "question-mark-in-a-string",
        "bare-colon",
        "nothing-to-mask",
    ],
)
def test_mask_placeholders_replaces_exactly_the_placeholder_spans(statement, masked):
    # The helper alone, so a span one character off shows up here rather than as a lucky parse.
    assert _mask_placeholders(statement, "athena") == masked


# Driver-native markers ($1, $name, @name) and keyword-named :name, found by the next token.
@pytest.mark.parametrize(
    "dialect,statement,masked",
    [
        ("duckdb", "SELECT a FROM t WHERE b = $1", "SELECT a FROM t WHERE b = '0'"),
        ("duckdb", "SELECT a FROM t WHERE b = $ts", "SELECT a FROM t WHERE b = '0'"),
        (
            "postgres",
            "SELECT a FROM t WHERE b = $1 AND c = $2",
            "SELECT a FROM t WHERE b = '0' AND c = '0'",
        ),
        ("bigquery", "SELECT a FROM t WHERE b = @ts", "SELECT a FROM t WHERE b = '0'"),
        # Only the inner @name is a marker plus name; the outer @ is followed by another @.
        ("bigquery", "SELECT @@dataset_id", "SELECT @'0'"),
        # A keyword is still a name here: :date tokenizes as DATE, not VAR.
        ("athena", "SELECT a FROM t WHERE d = DATE :date", "SELECT a FROM t WHERE d = DATE '0'"),
        ("athena", "SELECT a FROM t WHERE e = :end", "SELECT a FROM t WHERE e = '0'"),
        # Not placeholders: a quoted name, a gap after the marker, a brace, pyformat.
        ("athena", 'SELECT a FROM t WHERE b = :"x"', 'SELECT a FROM t WHERE b = :"x"'),
        ("athena", "SELECT a FROM t WHERE b = : x", "SELECT a FROM t WHERE b = : x"),
        ("duckdb", "SELECT a FROM t WHERE b = $ 1", "SELECT a FROM t WHERE b = $ 1"),
        ("spark", "SELECT a FROM t WHERE b = ${ts}", "SELECT a FROM t WHERE b = ${ts}"),
        ("redshift", "SELECT a FROM t WHERE b = %(ts)s", "SELECT a FROM t WHERE b = %(ts)s"),
    ],
    ids=[
        "dollar-position",
        "dollar-name",
        "dollar-positions",
        "at-name",
        "double-at",
        "keyword-name-date",
        "keyword-name-end",
        "quoted-name",
        "space-after-colon",
        "space-after-dollar",
        "brace-after-dollar",
        "pyformat",
    ],
)
def test_mask_placeholders_takes_the_name_from_the_next_token(dialect, statement, masked):
    assert _mask_placeholders(statement, dialect) == masked


@pytest.mark.parametrize(
    "transformer,statement,expect_limited",
    [
        (DuckDBTransformer, "SELECT a FROM t WHERE ts > TIMESTAMP $1", True),
        (DuckDBTransformer, "SELECT a FROM t WHERE ts > TIMESTAMP $ts", True),
        (BigQueryTransformer, "SELECT a FROM t WHERE ts > TIMESTAMP @ts", True),
        (AthenaTransformer, "SELECT a FROM t WHERE d = DATE :date", True),
        # The gates still apply to a statement rescued this way.
        (DuckDBTransformer, "SELECT a FROM t WHERE ts > TIMESTAMP $1 LIMIT $2", False),
        (BigQueryTransformer, "SELECT a FROM t WHERE ts > TIMESTAMP @ts LIMIT @n", False),
        (PostgreSQLTransformer, "SELECT a FROM t WHERE ts > TIMESTAMP $1 FOR UPDATE", False),
        (DuckDBTransformer, "DELETE FROM t WHERE ts > TIMESTAMP $1", False),
    ],
    ids=[
        "duckdb-dollar-position",
        "duckdb-dollar-name",
        "bigquery-at-name",
        "athena-keyword-name",
        "author-supplied-limit-dollar",
        "author-supplied-limit-at",
        "locking-read",
        "delete",
    ],
)
def test_driver_native_markers_are_classified_from_a_masked_parse(
    transformer, statement, expect_limited
):
    with pytest.raises(Exception):
        sqlglot.parse_one(statement, dialect=transformer.get_dialect())

    result = transformer.apply_row_limit(statement, "UNKNOWN", 100)

    assert result == (f"{statement}\nLIMIT 100" if expect_limited else statement)


# Known gap: these are not recognised as markers, so the statement runs as written and warns.
@pytest.mark.parametrize(
    "transformer,statement",
    [
        (RedshiftTransformer, "SELECT a FROM t WHERE ts > TIMESTAMP %(ts)s"),
        (SparkTransformer, "SELECT a FROM t WHERE ts > TIMESTAMP ${ts}"),
    ],
    ids=["pyformat", "spark-variable"],
)
def test_unrecognised_markers_run_unlimited_with_a_warning(transformer, statement, caplog):
    with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
        assert transformer.apply_row_limit(statement, "UNKNOWN", 100) == statement

    assert len(_warnings(caplog)) == 1
