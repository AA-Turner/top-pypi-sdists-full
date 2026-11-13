"""Allowlist tests: which transformers opt in to the row limit.

The nine opted-in transformers append ``"\\nLIMIT n"``; every other one returns the statement
unchanged. Results are compared as text, not re-parsed: sqlglot's parser accepts a trailing
LIMIT even for tsql, teradata and oracle, so a successful parse proves nothing.
"""

import importlib
import pkgutil

import pytest

import sagemaker_studio.sql_engine as sql_engine_package
from sagemaker_studio.sql_engine.athena_transformer import AthenaTransformer
from sagemaker_studio.sql_engine.big_query_transformer import BigQueryTransformer
from sagemaker_studio.sql_engine.database_transformer import DatabaseTransformer
from sagemaker_studio.sql_engine.documentdb_transformer import DocumentDBTransformer
from sagemaker_studio.sql_engine.duckdb_transformer import DuckDBTransformer
from sagemaker_studio.sql_engine.dynamodb_transformer import DynamoDBTransformer
from sagemaker_studio.sql_engine.mssql_transformer import MSSQLTransformer
from sagemaker_studio.sql_engine.mysql_transformer import MySQLTransformer
from sagemaker_studio.sql_engine.opensearch_transformer import OpenSearchTransformer
from sagemaker_studio.sql_engine.oracle_transformer import OracleTransformer
from sagemaker_studio.sql_engine.postgresql_transformer import PostgreSQLTransformer
from sagemaker_studio.sql_engine.redshift_transformer import RedshiftTransformer
from sagemaker_studio.sql_engine.snowflake_transformer import SnowflakeTransformer
from sagemaker_studio.sql_engine.spark_transformer import SparkTransformer
from sagemaker_studio.sql_engine.sql_executor import SqlExecutor
from sagemaker_studio.sql_engine.teradata_transformer import TeraDataTransformer
from sagemaker_studio.sql_engine.vertica_transformer import VerticaTransformer
from sagemaker_studio.sql_engine.workday_transformer import WorkdayTransformer

STMT = "SELECT a FROM t"
LIMITED = f"{STMT}\nLIMIT 100"

# All 16 transformers, including those the registry omits (Teradata without its driver).
ALL_TRANSFORMERS = {
    "Athena": AthenaTransformer,
    "Redshift": RedshiftTransformer,
    "PostgreSQL": PostgreSQLTransformer,
    "MySQL": MySQLTransformer,
    "Snowflake": SnowflakeTransformer,
    "BigQuery": BigQueryTransformer,
    "DuckDB": DuckDBTransformer,
    "Spark": SparkTransformer,
    "Workday LDQ": WorkdayTransformer,
    "MSSQL": MSSQLTransformer,
    "Teradata": TeraDataTransformer,
    "Oracle": OracleTransformer,
    "Vertica": VerticaTransformer,
    "OpenSearch": OpenSearchTransformer,
    "DocumentDB": DocumentDBTransformer,
    "DynamoDB": DynamoDBTransformer,
}

# Dialects whose native row limit is a trailing LIMIT n.
OPTED_IN_NAMES = frozenset(
    {
        "Athena",
        "Redshift",
        "PostgreSQL",
        "MySQL",
        "Snowflake",
        "BigQuery",
        "DuckDB",
        "Spark",
        "Workday LDQ",
    }
)

_ALL_IDS = list(ALL_TRANSFORMERS)
_ALL_CLASSES = list(ALL_TRANSFORMERS.values())
_OPTED_IN_IDS = [name for name in _ALL_IDS if name in OPTED_IN_NAMES]
_OPTED_OUT_IDS = [name for name in _ALL_IDS if name not in OPTED_IN_NAMES]


def _discovered_transformers():
    """Every concrete DatabaseTransformer subclass; ImportError propagates on purpose."""
    found = {}
    for module_info in pkgutil.iter_modules(sql_engine_package.__path__):
        if not module_info.name.endswith("_transformer"):
            continue
        module = importlib.import_module(f"{sql_engine_package.__name__}.{module_info.name}")
        for attribute in vars(module).values():
            if (
                isinstance(attribute, type)
                and issubclass(attribute, DatabaseTransformer)
                and attribute is not DatabaseTransformer
            ):
                found[attribute.__name__] = attribute
    return found


@pytest.mark.parametrize("name,transformer", list(ALL_TRANSFORMERS.items()), ids=_ALL_IDS)
def test_every_transformer_declares_its_row_limit_decision(name, transformer):
    expected = name in OPTED_IN_NAMES
    assert transformer.supports_row_limit is expected, f"{transformer.__name__} disagrees"


@pytest.mark.parametrize(
    "transformer", [ALL_TRANSFORMERS[name] for name in _OPTED_IN_IDS], ids=_OPTED_IN_IDS
)
def test_opted_in_transformer_appends_the_clause(transformer):
    # Byte for byte, so the leading newline (which keeps a trailing comment from
    # swallowing the clause) is pinned too.
    assert transformer.apply_row_limit(STMT, "SELECT", 100) == LIMITED


@pytest.mark.parametrize(
    "transformer", [ALL_TRANSFORMERS[name] for name in _OPTED_OUT_IDS], ids=_OPTED_OUT_IDS
)
def test_opted_out_transformer_returns_the_statement_unchanged(transformer):
    # TOP n (MSSQL, Teradata), unverified FETCH FIRST (Oracle), no dialect (Vertica), not SQL.
    assert transformer.apply_row_limit(STMT, "SELECT", 100) == STMT


def test_opted_in_set_is_exactly_nine():
    declared = {name for name, cls in ALL_TRANSFORMERS.items() if cls.supports_row_limit}
    assert declared == OPTED_IN_NAMES
    assert len(OPTED_IN_NAMES) == 9


def test_every_transformer_in_the_package_has_a_decision_here():
    # A new transformer must be added to ALL_TRANSFORMERS rather than inherit False unnoticed.
    discovered = set(_discovered_transformers())
    tabulated = {cls.__name__ for cls in _ALL_CLASSES}
    assert discovered == tabulated, (
        "A DatabaseTransformer subclass in sagemaker_studio.sql_engine is missing from "
        "ALL_TRANSFORMERS. Decide whether its dialect takes a trailing LIMIT n and add it."
    )


@pytest.mark.parametrize("transformer", _ALL_CLASSES, ids=_ALL_IDS)
def test_apply_row_limit_is_inherited_from_base(transformer):
    # One gating point; an override would fork it silently.
    assert transformer.apply_row_limit.__func__ is DatabaseTransformer.apply_row_limit.__func__


def test_registry_is_covered_by_the_table():
    # The registry is a subset: Teradata drops out without its optional driver, and DuckDB
    # and Spark are never in it because sqlutils imports them directly for local execution.
    registry = SqlExecutor()._transformer_classes
    assert set(registry.values()) <= set(_ALL_CLASSES)
    assert {DuckDBTransformer, SparkTransformer}.isdisjoint(registry.values())
