"""Text-fidelity tests for the row-limit transform.

Re-rendering through sqlglot respells named parameters (``:id`` becomes ``%(id)s`` on
Redshift and Postgres) and rewrites line comments, so these tests check that:

* the author's text is a prefix of the submitted text, on every opted-in dialect;
* parameter binding is unchanged, on Redshift (Athena alone round-trips ``:name``);
* the clause is never absorbed by a trailing comment, by row count against real DuckDB.
"""

import duckdb
import pytest

from sagemaker_studio.sql_engine._sqlalchemy_redshift_data_api.dbapi.client import (
    RedshiftDataAPIClient,
)
from sagemaker_studio.sql_engine.athena_transformer import AthenaTransformer
from sagemaker_studio.sql_engine.big_query_transformer import BigQueryTransformer
from sagemaker_studio.sql_engine.duckdb_transformer import DuckDBTransformer
from sagemaker_studio.sql_engine.mysql_transformer import MySQLTransformer
from sagemaker_studio.sql_engine.postgresql_transformer import PostgreSQLTransformer
from sagemaker_studio.sql_engine.redshift_transformer import RedshiftTransformer
from sagemaker_studio.sql_engine.snowflake_transformer import SnowflakeTransformer
from sagemaker_studio.sql_engine.spark_transformer import SparkTransformer
from sagemaker_studio.sql_engine.sql_executor import SqlExecutor
from sagemaker_studio.sql_engine.workday_transformer import WorkdayTransformer

LIMIT = 100
# Written out, not imported: the clause and its leading newline are the contract here.
CLAUSE = f"\nLIMIT {LIMIT}"

# The allowlist itself is asserted in the dialects module.
OPTED_IN = {
    "Athena": AthenaTransformer,
    "Redshift": RedshiftTransformer,
    "PostgreSQL": PostgreSQLTransformer,
    "MySQL": MySQLTransformer,
    "Snowflake": SnowflakeTransformer,
    "BigQuery": BigQueryTransformer,
    "DuckDB": DuckDBTransformer,
    "Spark": SparkTransformer,
    "Workday LDQ": WorkdayTransformer,
}

# Statements a sqlglot re-render would rewrite. Third element: limited on every dialect
# (True), none (False), or dialect-dependent (None, prefix relation only). Entries are
# pre-stripped, as split_query hands them over.
CORPUS = [
    # :id survives a sqlglot round trip only on Athena.
    ("named-param", "SELECT a FROM t WHERE id = :id", True),
    ("named-param-repeated", "SELECT a FROM t WHERE id = :id OR alt = :id", True),
    # The Athena path binds ? markers positionally, so a reordering binds the wrong value.
    ("positional-param", "SELECT a FROM t WHERE id = ? AND b > ?", True),
    # A line comment was rewritten to a block comment on every dialect, Athena included.
    ("trailing-line-comment", "SELECT a FROM t -- trailing note", True),
    ("interior-line-comment", "SELECT a -- pick a\nFROM t", True),
    ("block-comment", "SELECT a FROM t /* why */ WHERE a > 0", True),
    ("both-comment-kinds", "SELECT a /* inline */ FROM t -- and trailing", True),
    ("quoted-identifiers", 'SELECT "Odd Column" FROM "Odd Table"', True),
    ("string-literal-with-double-dash", "SELECT a FROM t WHERE s = 'not -- a comment'", True),
    ("odd-whitespace", "SELECT    a,\n\t  b\n  FROM   t", True),
    ("cte", "WITH c AS (SELECT a FROM t) SELECT a FROM c", True),
    # A derived-table wrap would not guarantee this ORDER BY survives; appending does.
    ("order-by", "SELECT a FROM t ORDER BY a DESC", True),
    ("qualified-star", "SELECT t.* FROM t JOIN u ON t.a = u.a", True),
    # Classified from a masked copy, which must never be what is returned.
    ("masked-named-param", "SELECT a FROM t WHERE ts > TIMESTAMP :ts", True),
    ("masked-positional-param", "SELECT a FROM t WHERE d = DATE ?", True),
    ("masked-several-params", "SELECT a FROM t WHERE b IN (?, ?) AND d = DATE ?", True),
    # `::` and a `:` or `?` inside a string are not placeholders. Masking them would break
    # the masked parse, so expect_limited=True is the evidence the mask skipped them.
    ("masked-with-a-cast", "SELECT a::VARCHAR FROM t WHERE ts > TIMESTAMP :ts", True),
    ("masked-with-a-colon-string", "SELECT 'a:b' FROM t WHERE ts > TIMESTAMP :ts", True),
    ("masked-with-a-question-string", "SELECT 'what?' FROM t WHERE d = DATE ?", True),
    # Read-only families with no trailing position for the clause: appending would truncate
    # the table SELECT ... INTO creates, and Spark orders the clauses LIMIT then OFFSET.
    ("select-into", "SELECT a INTO new_table FROM t", False),
    ("offset-with-no-limit", "SELECT a FROM t ORDER BY a OFFSET 10", False),
    # Masked to a write, so the family gate declines and the author's text comes back.
    ("masked-to-a-delete", "DELETE FROM t WHERE ts > TIMESTAMP :ts", False),
    # Unparseable with the placeholder masked too: no family, no limit, author's text.
    ("unparseable-even-masked", "SELECT a FROM t WHERE b = :n AND ((", False),
    # The statement a re-render already broke once in split_query (CR-317418980). A CREATE,
    # so the family gate declines it.
    ("iceberg-ctas", "CREATE TABLE z USING ICEBERG AS SELECT a FROM t", False),
    # bigquery needs UNION ALL or UNION DISTINCT, so a bare UNION is UNKNOWN there and
    # UNION on the other eight. Both satisfy the prefix relation, which is the point of it.
    ("union", "SELECT a FROM t UNION SELECT b FROM u", None),
]

_CORPUS_IDS = [f"{name}-{entry[0]}" for name in OPTED_IN for entry in CORPUS]
_CORPUS_CASES = [(transformer, *entry) for transformer in OPTED_IN.values() for entry in CORPUS]


# The author's text is always a prefix of the submitted text.


@pytest.mark.parametrize(
    "transformer,case_id,statement,expect_limited", _CORPUS_CASES, ids=_CORPUS_IDS
)
def test_the_authors_text_is_a_prefix_and_the_remainder_is_only_the_clause(
    transformer, case_id, statement, expect_limited
):
    # Classified by split_query, as in production. The precondition pins that split_query
    # returns the author's text verbatim; without it the prefix relation could hold against
    # text already mangled upstream.
    split = transformer.split_query(statement)
    assert [item.statement for item in split] == [statement]
    statement_type = split[0].statement_type

    result = transformer.apply_row_limit(statement, statement_type, LIMIT)

    assert result.startswith(statement), (
        f"{transformer.__name__} did not preserve the author's text as a prefix.\n"
        f"  author:    {statement!r}\n"
        f"  submitted: {result!r}"
    )
    remainder = result[len(statement) :]
    assert remainder in ("", CLAUSE), (
        f"{transformer.__name__} added something other than the row-limit clause.\n"
        f"  remainder: {remainder!r}"
    )

    # Non-vacuity: a transform that never did anything would satisfy the prefix relation.
    if expect_limited is True:
        assert remainder == CLAUSE
    elif expect_limited is False:
        assert remainder == ""


def test_an_author_supplied_limit_is_still_the_end_of_the_text():
    # Never-clamp and the prefix relation together: byte for byte, not a second clause.
    statement = "SELECT a FROM t WHERE id = :id -- mine\nLIMIT 5"
    assert RedshiftTransformer.apply_row_limit(statement, "SELECT", LIMIT) == statement


# Parameter binding is unaffected by the row limit. Runs the real SqlExecutor.execute with
# only the boto3 client faked.

_REDSHIFT_CONNECTION_DATA = {
    "database_name": "dev",
    "workgroup_name": "wg",
    "region": "us-east-1",
}


class _FakeRedshiftDataClient:
    """The boto3 redshift-data client, and nothing above it, replaced by a recorder.

    Everything between SqlExecutor.execute and this object is real -- transformer,
    SQLAlchemy compilation, dialect, cursor -- so ``submissions`` holds exactly what would
    have reached the Data API.
    """

    def __init__(self):
        self.submissions = []

    def list_databases(self, **kwargs):
        # The driver's connection-validation probe.
        return {"Databases": ["dev"]}

    def execute_statement(self, **kwargs):
        self.submissions.append(kwargs)
        return {"Id": "stmt-1"}

    def describe_statement(self, **kwargs):
        return {
            "Status": "FINISHED",
            "HasResultSet": True,
            "ResultMetadata": {"ColumnMetadata": [{"name": "a", "typeName": "varchar"}]},
            "RecordsUpdated": 0,
        }

    def get_statement_result(self, **kwargs):
        return {
            "Records": [[{"stringValue": "read committed"}]],
            "ColumnMetadata": [{"name": "a", "typeName": "varchar"}],
            "NextToken": None,
        }


class _FakeBotoSession:
    """Hands the driver the fake client in place of a real redshift-data client.

    Deliberately not a Mock: the driver inspects the session and client for optional
    service-model wiring, and a Mock would answer with more Mocks. With no ``_session`` and
    no ``meta``, those inspections fail their guards and the driver falls back.
    """

    def __init__(self, client):
        self._client = client

    def client(self, service_name, **kwargs):
        return self._client


@pytest.fixture
def redshift_submissions(monkeypatch):
    """A real Redshift engine whose only fake is the boto3 client.

    Yields ``(submit, client)``; ``submit(query, parameters, limit)`` returns the
    ``execute_statement`` calls the query caused.
    """
    client = _FakeRedshiftDataClient()
    monkeypatch.setattr(
        RedshiftDataAPIClient,
        "_create_boto3_session",
        lambda self: _FakeBotoSession(client),
    )

    executor = SqlExecutor()
    engine = executor.create_engine("REDSHIFT", _REDSHIFT_CONNECTION_DATA)
    # Dialect initialization submits its own statements; get them out of the way first.
    engine.connect().close()

    def submit(query, parameters, limit_query_results):
        client.submissions.clear()
        results = list(
            executor.execute(
                engine,
                query,
                parameters,
                limit_query_results=limit_query_results,
            )
        )
        for result in results:
            assert result.error is None, result.error
        return list(client.submissions)

    yield submit, client
    engine.dispose()


@pytest.mark.parametrize(
    "query,parameters",
    [
        ("SELECT a FROM t WHERE id = :id", {"id": "1"}),
        # Two binds and a trailing line comment: the two things the round trip rewrote.
        (
            "SELECT a FROM t WHERE id = :id AND region = :region -- scoped\n",
            {"id": "1", "region": "us-east-1"},
        ),
    ],
    ids=["one-bind", "two-binds-and-a-comment"],
)
def test_redshift_binds_the_same_parameters_with_and_without_a_limit(
    redshift_submissions, query, parameters
):
    submit, _ = redshift_submissions

    unlimited = submit(query, parameters, None)
    limited = submit(query, parameters, LIMIT)

    assert len(unlimited) == 1 and len(limited) == 1
    unlimited_sql = unlimited[0]["Sql"]
    limited_sql = limited[0]["Sql"]

    assert limited_sql == unlimited_sql + CLAUSE

    # Spelled out as well as implied above, because the respelling is the defect.
    for name in parameters:
        assert f":{name}" in limited_sql
        assert f"%({name})s" not in limited_sql

    assert limited[0].get("Parameters") == unlimited[0].get("Parameters")
    assert limited[0].get("Parameters") == [
        {"name": name, "value": value} for name, value in parameters.items()
    ]


def test_redshift_submits_an_unparameterized_query_unchanged_but_for_the_clause(
    redshift_submissions,
):
    # The control: with no binds to lose, the only difference the limit may make is the clause.
    submit, _ = redshift_submissions
    query = "SELECT a FROM t -- trailing note"

    unlimited = submit(query, None, None)
    limited = submit(query, None, LIMIT)

    assert unlimited[0]["Sql"] == query
    assert limited[0]["Sql"] == query + CLAUSE


# An appended clause is never absorbed by a comment. Checked by row count against real
# DuckDB, since a same-line clause after "--" reads correctly but limits nothing.

_ROW_COUNT = 1000
_LIMITED_ROWS = 5


@pytest.fixture
def duckdb_connection():
    connection = duckdb.connect()
    connection.execute(f"CREATE TABLE t AS SELECT * FROM range({_ROW_COUNT}) AS r(i)")
    yield connection
    connection.close()


def _row_count(connection, sql):
    return len(connection.execute(sql).fetchall())


def test_a_statement_ending_in_a_line_comment_is_actually_limited(duckdb_connection):
    statement = "SELECT * FROM t -- my note"
    assert _row_count(duckdb_connection, statement) == _ROW_COUNT

    submitted = DuckDBTransformer.apply_row_limit(statement, "SELECT", _LIMITED_ROWS)

    assert _row_count(duckdb_connection, submitted) == _LIMITED_ROWS, (
        "DuckDB returned more rows than the limit, so the appended clause did not take "
        f"effect. Submitted: {submitted!r}"
    )


def test_the_same_clause_on_one_line_would_be_swallowed(duckdb_connection):
    # The negative control: one character of difference, 1000 rows instead of 5, no error.
    statement = "SELECT * FROM t -- my note"
    swallowed = f"{statement} LIMIT {_LIMITED_ROWS}"
    appended = f"{statement}\nLIMIT {_LIMITED_ROWS}"

    assert _row_count(duckdb_connection, swallowed) == _ROW_COUNT
    assert _row_count(duckdb_connection, appended) == _LIMITED_ROWS
    # Which of the two the transformer produces is the whole question.
    assert DuckDBTransformer.apply_row_limit(statement, "SELECT", _LIMITED_ROWS) == appended


def test_a_limited_statement_without_a_comment_is_unaffected_by_the_newline(duckdb_connection):
    # The clause's newline must not cost anything on ordinary statements.
    statement = "SELECT * FROM t"
    submitted = DuckDBTransformer.apply_row_limit(statement, "SELECT", _LIMITED_ROWS)
    assert _row_count(duckdb_connection, submitted) == _LIMITED_ROWS
