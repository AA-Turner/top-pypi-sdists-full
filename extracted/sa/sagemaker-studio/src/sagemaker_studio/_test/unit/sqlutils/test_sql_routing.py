"""``sqlutils._route``: the one place a statement's engine is chosen, for ``sql``, ``sql_stream``
and the async path."""

import inspect
import unittest
from contextlib import contextmanager
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from sagemaker_studio.sql_engine.duckdb_engine import engine as duckdb_engine
from sagemaker_studio.utils import athena_v4, duckdbutils, sqlutils


def _connection(conn_type):
    conn = MagicMock()
    conn.type = conn_type
    return conn


class TestRoute(unittest.TestCase):
    def test_spark_config_runs_on_spark_without_resolving_a_connection(self):
        with patch.object(sqlutils, "_resolve_connection") as resolve:
            route = sqlutils._route({"type": "spark"}, "ignored", None)
        self.assertEqual(route, sqlutils._Route(sqlutils._ENGINE_SPARK))
        resolve.assert_not_called()

    def test_other_connection_config_types_are_rejected(self):
        with self.assertRaises(ValueError):
            sqlutils._route({"type": "duckdb"}, None, None)

    def test_no_connection_runs_on_duckdb(self):
        route = sqlutils._route(None, None, None)
        self.assertEqual(route, sqlutils._Route(sqlutils._ENGINE_DUCKDB))

    def test_iceberg_rest_catalog_connection_runs_on_glue_spark(self):
        conn = _connection(sqlutils.SUPPORTED_IRC_GLUE_CONNECTION_TYPES[0])
        with patch.object(sqlutils, "_resolve_connection", return_value=conn):
            route = sqlutils._route(None, "irc-1", None)
        self.assertEqual(route, sqlutils._Route(sqlutils._ENGINE_GLUE_IRC, conn))

    def test_an_s3_connection_runs_on_its_own_engine_on_a_local_kernel_too(self):
        # No DuckDB route for an S3 connection in any mode: the native path refuses it as a type
        # with no SQL engine, the same way on SageMaker Unified Studio compute.
        conn = _connection("S3")
        with patch.object(sqlutils, "_resolve_connection", return_value=conn), patch.object(
            sqlutils.local_kernel, "is_local_kernel", return_value=True
        ):
            route = sqlutils._route(None, None, "my-bucket")
        self.assertEqual(route, sqlutils._Route(sqlutils._ENGINE_NATIVE, conn))

    def test_any_other_connection_runs_on_its_own_engine(self):
        conn = _connection("REDSHIFT")
        with patch.object(sqlutils, "_resolve_connection", return_value=conn):
            route = sqlutils._route(None, "redshift-1", None)
        self.assertEqual(route, sqlutils._Route(sqlutils._ENGINE_NATIVE, conn))


class TestEntryPointsShareTheRoute(unittest.TestCase):
    """``sql`` and ``sql_stream`` run a statement where ``_route`` says, never deciding themselves."""

    def test_sql_runs_a_duckdb_route_on_the_cells_engine(self):
        route = sqlutils._Route(sqlutils._ENGINE_DUCKDB)  # DuckDB runs cells with no connection
        duck = object()  # the cell's engine, got once and handed to the statement
        with patch.object(sqlutils, "_route", return_value=route), patch.object(
            duckdb_engine, "_ensure_duckdb", return_value=duck
        ), patch.object(
            duckdbutils, "_run_duckdb_statement", return_value="df"
        ) as run, patch.object(
            sqlutils, "_get_or_create_connection"
        ) as native:
            self.assertEqual(sqlutils.sql("SELECT 1"), "df")
        run.assert_called_once_with(duck, "SELECT 1")
        native.assert_not_called()

    def test_sql_stream_runs_each_duckdb_statement_on_the_cells_engine(self):
        route = sqlutils._Route(sqlutils._ENGINE_DUCKDB)
        duck = object()
        with patch.object(sqlutils, "_route", return_value=route), patch.object(
            duckdb_engine, "_ensure_duckdb", return_value=duck
        ) as ensure, patch.object(duckdbutils, "_run_duckdb_statement", return_value="df") as run:
            results = list(sqlutils.sql_stream("SELECT 1; SELECT 2"))
        self.assertEqual([r.result for r in results], ["df", "df"])
        self.assertEqual(
            [c.args for c in run.call_args_list], [(duck, "SELECT 1"), (duck, "SELECT 2")]
        )
        ensure.assert_called_once_with()  # once for the stream, not per statement

    def test_async_path_declines_every_route_but_native(self):
        for engine in (sqlutils._ENGINE_SPARK, sqlutils._ENGINE_GLUE_IRC, sqlutils._ENGINE_DUCKDB):
            with patch.object(
                sqlutils, "_route", return_value=sqlutils._Route(engine)
            ), patch.object(sqlutils, "_get_or_create_connection") as native:
                handled = sqlutils._stream_with_async_materialization("SELECT 1", "df")
            self.assertFalse(handled, engine)
            native.assert_not_called()


class TestNoEngineParameter(unittest.TestCase):
    """The SDK chooses the engine (see ``_route``): no entry point, and not ``_route``, takes one."""

    def test_no_function_takes_an_engine(self):
        import inspect

        for function in (
            sqlutils.sql,
            sqlutils.sql_stream,
            sqlutils.sql_stream_with_display,
            sqlutils._stream_with_async_materialization,
            sqlutils._route,
        ):
            self.assertNotIn("engine", inspect.signature(function).parameters, function.__name__)
        self.assertFalse(hasattr(sqlutils, "ENGINES"))

    def test_sql_stream_with_display_passes_no_engine_on(self):
        with patch.object(
            sqlutils, "_stream_with_async_materialization", return_value=False
        ) as async_path, patch.object(
            sqlutils, "sql_stream", return_value=iter([])
        ) as sync, patch.object(
            sqlutils, "_materialise_stream"
        ):
            sqlutils.sql_stream_with_display(
                "SELECT 1", "df", connection_id="athena-1", materialize="async"
            )
        self.assertNotIn("engine", async_path.call_args.kwargs)
        self.assertNotIn("engine", sync.call_args.kwargs)


class TestRouteAthena(unittest.TestCase):
    """Every Athena engine version runs through the SDK-owned native API executor."""

    def test_athena_connection_runs_on_native_api(self):
        conn = _connection("ATHENA")
        with patch.object(sqlutils, "_resolve_connection", return_value=conn):
            route = sqlutils._route(None, "athena-1", None)
        self.assertEqual(route, sqlutils._Route(sqlutils._ENGINE_ATHENA, conn))

    def test_lakehouse_catalog_naming_an_athena_workgroup_runs_on_native_api(self):
        conn = _connection("LAKEHOUSE")
        conn.sql_engine_type = "ATHENA"
        conn.athena_workgroup = "primary"
        with patch.object(sqlutils, "_resolve_connection", return_value=conn):
            route = sqlutils._route(None, "catalog-1", None)
        self.assertEqual(route, sqlutils._Route(sqlutils._ENGINE_ATHENA, conn))

    def test_parameters_do_not_change_the_athena_route(self):
        conn = _connection("ATHENA")
        with patch.object(sqlutils, "_resolve_connection", return_value=conn):
            route = sqlutils._route(None, "athena-1", None, {"value": 1})
        self.assertEqual(route, sqlutils._Route(sqlutils._ENGINE_ATHENA, conn))

    def test_no_athena_connection_reaches_duckdb(self):
        # Whatever engine the workgroup runs (Athena DuckDB included), a cell naming an Athena
        # connection runs on the native executor; only a cell with no connection runs on DuckDB,
        # against the workgroups attach_local_catalogs() attached.
        conn = _connection("ATHENA")
        conn.athena_workgroup = "duckdb-wg"
        with patch.object(sqlutils, "_resolve_connection", return_value=conn), patch.object(
            sqlutils.local_kernel, "is_local_kernel", return_value=True
        ):
            route = sqlutils._route(None, "athena-1", None)
        self.assertEqual(route, sqlutils._Route(sqlutils._ENGINE_ATHENA, conn))


class TestNoEngineForTheConnection(unittest.TestCase):
    def test_sql_and_sql_stream_say_so_instead_of_an_attribute_error(self):
        conn = _connection("REDSHIFT")
        conn.name = "warehouse"
        route = sqlutils._Route(sqlutils._ENGINE_NATIVE, conn)
        with patch.object(sqlutils, "_route", return_value=route), patch.object(
            sqlutils, "_get_or_create_connection", return_value=None
        ):
            with self.assertRaisesRegex(RuntimeError, "SQL engine for connection 'warehouse'"):
                sqlutils.sql("SELECT 1", connection_id="athena-1")
            with self.assertRaisesRegex(RuntimeError, "SQL engine for connection 'warehouse'"):
                sqlutils.sql_stream("SELECT 1", connection_id="athena-1")


# --- limit_query_results ------------------------------------------------------------------
#
# For the NATIVE and ATHENA routes sqlutils only carries the parameter; the limit is applied in
# SqlExecutor.execute and athena_v4.execute_query_statements. These tests patch those two
# execution layers and assert what each entry point handed them.

_QUERY = "SELECT a FROM t"
_SUCCESS = SimpleNamespace(
    status="success", result="df", error=None, statement=_QUERY, execution_metadata=None
)
_ENGINES = [sqlutils._ENGINE_NATIVE, sqlutils._ENGINE_ATHENA]


@contextmanager
def _execution_layer(engine):
    """Patch routing and the connection build so ``engine``'s execution layer is the only
    recorded boundary. Yields the mock standing in for it."""
    recorder = MagicMock(side_effect=lambda *a, **k: iter([_SUCCESS]))
    conn = _connection("ATHENA" if engine == sqlutils._ENGINE_ATHENA else "REDSHIFT")
    cached = SimpleNamespace(
        engine=SimpleNamespace(get_execution_options=lambda: {"connection_type": "REDSHIFT"}),
        connection=None,
    )
    with patch.object(sqlutils, "_route", return_value=sqlutils._Route(engine, conn)), patch.object(
        sqlutils, "_athena_api", return_value=MagicMock()
    ), patch.object(sqlutils, "_get_or_create_connection", return_value=cached), patch.object(
        sqlutils, "_ensure_sql_executor", return_value=SimpleNamespace(execute=recorder)
    ), patch.object(
        athena_v4, "execute_query_statements", recorder
    ):
        yield recorder


def _run_sql(**kwargs):
    sqlutils.sql(_QUERY, connection_id="c1", **kwargs)


def _run_sql_stream(**kwargs):
    list(sqlutils.sql_stream(_QUERY, connection_id="c1", **kwargs))


def _run_sql_stream_with_display(**kwargs):
    # materialize defaults to "sync", so this is the fall-through into sql_stream.
    with patch.object(sqlutils, "_materialise_stream"):
        sqlutils.sql_stream_with_display(_QUERY, "df", connection_id="c1", **kwargs)


_ENTRY_POINTS = {
    "sql": _run_sql,
    "sql_stream": _run_sql_stream,
    "sql_stream_with_display": _run_sql_stream_with_display,
}


@pytest.mark.parametrize("engine", _ENGINES)
@pytest.mark.parametrize("entry_point", sorted(_ENTRY_POINTS))
def test_the_limit_reaches_the_execution_layer(entry_point, engine):
    """The parameter reaches the execution layer unmodified."""
    with _execution_layer(engine) as execute:
        _ENTRY_POINTS[entry_point](limit_query_results=100)

    assert execute.call_count == 1
    assert execute.call_args.kwargs["limit_query_results"] == 100
    assert execute.call_args.args[1] == _QUERY


def test_the_limit_reaches_the_async_driver():
    """Fourth entry point: the hop into the async driver. The driver's own two
    engine routes are covered by AsyncRowLimitPropagationTest in test_sqlutils_async.py.
    """
    with patch.object(sqlutils, "_stream_with_async_materialization", return_value=True) as driver:
        sqlutils.sql_stream_with_display(
            _QUERY, "df", connection_id="c1", materialize="async", limit_query_results=100
        )

    assert driver.call_args.kwargs["limit_query_results"] == 100
    assert driver.call_args.args[0] == _QUERY


def test_the_limit_is_not_a_connection_kwarg():
    """The first_page_rows lesson: a non-connection knob must never reach connection
    construction, where an unexpected key is ignored at best and an error at worst."""
    recorder = MagicMock(side_effect=lambda *a, **k: iter([_SUCCESS]))
    conn = _connection("REDSHIFT")
    engine = SimpleNamespace(get_execution_options=lambda: {"connection_type": "REDSHIFT"})
    with patch.object(
        sqlutils, "_route", return_value=sqlutils._Route(sqlutils._ENGINE_NATIVE, conn)
    ), patch.object(
        sqlutils, "_get_or_create_connection", wraps=sqlutils._get_or_create_connection
    ) as get_connection, patch.object(
        sqlutils, "_get_engine_from_connection", return_value=engine
    ) as get_engine, patch.object(
        sqlutils.local_kernel, "is_local_kernel", return_value=False
    ), patch.object(
        sqlutils, "_ensure_sql_executor", return_value=SimpleNamespace(execute=recorder)
    ):
        sqlutils.sql(_QUERY, connection_id="c1", persist_session=False, limit_query_results=100)

    assert "limit_query_results" not in get_connection.call_args.kwargs
    assert "limit_query_results" not in get_engine.call_args.kwargs
    assert recorder.call_args.kwargs["limit_query_results"] == 100  # it went to the executor


def test_the_limit_never_changes_the_connection_cache_key():
    assert sqlutils._make_cache_key(
        "c1", None, catalog_name="awsdatacatalog"
    ) == sqlutils._make_cache_key(
        "c1", None, catalog_name="awsdatacatalog", limit_query_results=100
    )


def test_spark_runs_the_authors_sql_unchanged():
    spark = MagicMock()
    with patch.object(
        sqlutils, "_route", return_value=sqlutils._Route(sqlutils._ENGINE_SPARK)
    ), patch.object(sqlutils, "_ensure_spark", return_value=spark):
        sqlutils.sql(_QUERY, limit_query_results=100)
    spark.sql.assert_called_once_with(_QUERY)


def test_irc_glue_runs_the_authors_sql_unchanged():
    conn = _connection(sqlutils.SUPPORTED_IRC_GLUE_CONNECTION_TYPES[0])
    spark = MagicMock()
    with patch.object(
        sqlutils, "_route", return_value=sqlutils._Route(sqlutils._ENGINE_GLUE_IRC, conn)
    ), patch.object(sqlutils, "_ensure_glue_spark", return_value=spark):
        sqlutils.sql(_QUERY, connection_id="irc-1", limit_query_results=100)
    spark.sql.assert_called_once_with(_QUERY)


def test_duckdb_runs_the_authors_sql_unchanged():
    duck = object()
    with patch.object(
        sqlutils, "_route", return_value=sqlutils._Route(sqlutils._ENGINE_DUCKDB)
    ), patch.object(duckdb_engine, "_ensure_duckdb", return_value=duck), patch.object(
        duckdbutils, "_run_duckdb_statement", return_value="df"
    ) as run:
        assert sqlutils.sql(_QUERY, limit_query_results=100) == "df"
    run.assert_called_once_with(duck, _QUERY)


@pytest.mark.parametrize("engine", _ENGINES)
@pytest.mark.parametrize("entry_point", sorted(_ENTRY_POINTS))
def test_no_limit_kwarg_submits_the_pre_feature_text(entry_point, engine):
    """No effective row limit leaves the statement byte-identical."""
    with _execution_layer(engine) as execute:
        _ENTRY_POINTS[entry_point]()

    assert execute.call_count == 1
    assert execute.call_args.args[1] == _QUERY
    assert execute.call_args.kwargs["limit_query_results"] is None


def test_no_limit_kwarg_reaches_the_async_driver_as_none():
    """Fourth entry point: no default limit is injected on the way in."""
    with patch.object(sqlutils, "_stream_with_async_materialization", return_value=True) as driver:
        sqlutils.sql_stream_with_display(_QUERY, "df", connection_id="c1", materialize="async")

    assert driver.call_args.args[0] == _QUERY
    assert driver.call_args.kwargs["limit_query_results"] is None


# Recorded from the commit before limit_query_results was added, by parsing
# `git show HEAD:src/sagemaker_studio/utils/sqlutils.py` (c69a917) with `ast` rather than from
# the current signatures, so this guards against a reordering instead of restating one. None of
# the three had any keyword-only parameter then.
_PRE_FEATURE_POSITIONALS = {
    "sql": [
        "query",
        "parameters",
        "connection_id",
        "connection_name",
        "connection",
        "persist_session",
    ],
    "sql_stream": [
        "query",
        "parameters",
        "connection_id",
        "connection_name",
        "connection",
        "error_strategy",
        "persist_session",
    ],
    "sql_stream_with_display": [
        "query",
        "dataframe_name",
        "parameters",
        "connection_id",
        "connection_name",
        "connection",
        "error_strategy",
        "materialize",
    ],
}


@pytest.mark.parametrize("name", sorted(_PRE_FEATURE_POSITIONALS))
def test_existing_positional_parameters_keep_their_positions(name):
    """Existing positional parameters keep their positions."""
    parameters = inspect.signature(getattr(sqlutils, name)).parameters
    positional = [
        p.name
        for p in parameters.values()
        if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)
    ]

    assert positional == _PRE_FEATURE_POSITIONALS[name]
    assert parameters["limit_query_results"].kind is inspect.Parameter.KEYWORD_ONLY
    assert parameters["limit_query_results"].default is None


# --- DuckDB row limits -------------------------------------------------------------------
#
# DuckDB has no SqlExecutor.execute to apply the limit for it: sql_stream applies it itself,
# between split_query and the per-statement run. These tests assert the text DuckDB ran.


@contextmanager
def _duckdb_statements():
    """Route to DuckDB and record the statement text each run receives."""
    duck = object()
    with patch.object(
        sqlutils, "_route", return_value=sqlutils._Route(sqlutils._ENGINE_DUCKDB)
    ), patch.object(duckdb_engine, "_ensure_duckdb", return_value=duck), patch.object(
        duckdbutils, "_run_duckdb_statement", return_value="df"
    ) as run:
        yield run


def _duckdb_ran(run):
    return [call.args[1] for call in run.call_args_list]


def test_duckdb_stream_appends_the_limit():
    with _duckdb_statements() as run:
        list(sqlutils.sql_stream(_QUERY, limit_query_results=100))
    assert _duckdb_ran(run) == ["SELECT a FROM t\nLIMIT 100"]


def test_duckdb_stream_limits_each_statement():
    with _duckdb_statements() as run:
        list(sqlutils.sql_stream("SELECT a FROM t; SELECT b FROM u", limit_query_results=100))
    assert _duckdb_ran(run) == ["SELECT a FROM t\nLIMIT 100", "SELECT b FROM u\nLIMIT 100"]


def test_duckdb_stream_without_the_kwarg_submits_the_authors_sql():
    with _duckdb_statements() as run:
        list(sqlutils.sql_stream(_QUERY))
    assert _duckdb_ran(run) == [_QUERY]


def test_duckdb_stream_never_lowers_an_authors_limit():
    with _duckdb_statements() as run:
        list(sqlutils.sql_stream("SELECT a FROM t LIMIT 5", limit_query_results=100))
    assert _duckdb_ran(run) == ["SELECT a FROM t LIMIT 5"]


def test_duckdb_stream_leaves_a_write_statement_alone():
    with _duckdb_statements() as run:
        list(sqlutils.sql_stream("INSERT INTO t SELECT 1", limit_query_results=100))
    assert _duckdb_ran(run) == ["INSERT INTO t SELECT 1"]


# --- Spark row limits --------------------------------------------------------------------
#
# Both Spark routes split with SparkTransformer and then limit, like DuckDB. _ENGINE_SPARK is
# the kernel session; _ENGINE_GLUE_IRC is the Glue-backed session an Iceberg REST catalog
# connection runs on. These assert the statement text each one executed.


@contextmanager
def _spark_statements():
    """Route to the kernel Spark session and record what spark.sql ran."""
    spark = MagicMock()
    with patch.object(
        sqlutils, "_route", return_value=sqlutils._Route(sqlutils._ENGINE_SPARK)
    ), patch.object(sqlutils, "_ensure_spark", return_value=spark):
        yield spark.sql


@contextmanager
def _irc_statements():
    """Route to the Glue-backed Spark session and record what it ran."""
    conn = _connection(sqlutils.SUPPORTED_IRC_GLUE_CONNECTION_TYPES[0])
    with patch.object(
        sqlutils, "_route", return_value=sqlutils._Route(sqlutils._ENGINE_GLUE_IRC, conn)
    ), patch.object(sqlutils, "_execute_irc_connection_query", return_value="df") as run:
        yield run


def test_spark_stream_appends_the_limit():
    with _spark_statements() as ran:
        list(sqlutils.sql_stream(_QUERY, connection={"type": "spark"}, limit_query_results=100))
    assert [c.args[0] for c in ran.call_args_list] == ["SELECT a FROM t\nLIMIT 100"]


def test_spark_stream_without_the_kwarg_submits_the_authors_sql():
    with _spark_statements() as ran:
        list(sqlutils.sql_stream(_QUERY, connection={"type": "spark"}))
    assert [c.args[0] for c in ran.call_args_list] == [_QUERY]


def test_spark_stream_never_lowers_an_authors_limit():
    with _spark_statements() as ran:
        list(
            sqlutils.sql_stream(
                "SELECT a FROM t LIMIT 5", connection={"type": "spark"}, limit_query_results=100
            )
        )
    assert [c.args[0] for c in ran.call_args_list] == ["SELECT a FROM t LIMIT 5"]


def test_spark_stream_leaves_a_cache_statement_alone():
    # CACHE TABLE is Spark-only and not a read-only statement family.
    with _spark_statements() as ran:
        list(
            sqlutils.sql_stream(
                "CACHE TABLE t", connection={"type": "spark"}, limit_query_results=100
            )
        )
    assert [c.args[0] for c in ran.call_args_list] == ["CACHE TABLE t"]


def test_irc_glue_stream_appends_the_limit():
    with _irc_statements() as run:
        list(sqlutils.sql_stream(_QUERY, connection_id="irc-1", limit_query_results=100))
    assert [c.args[0] for c in run.call_args_list] == ["SELECT a FROM t\nLIMIT 100"]


def test_irc_glue_stream_without_the_kwarg_submits_the_authors_sql():
    with _irc_statements() as run:
        list(sqlutils.sql_stream(_QUERY, connection_id="irc-1"))
    assert [c.args[0] for c in run.call_args_list] == [_QUERY]


# --- Multi-statement cells ----------------------------------------------------------------
#
# A notebook cell commonly holds several statements. These assert, per route, that every
# eligible statement gains the clause and every ineligible one is submitted as written. The
# eligible statements sit at indices 1 and 2, not at index 0, so an implementation that
# limited only the first statement fails here.

_MIXED_CELL = (
    "CREATE TABLE z AS SELECT b FROM u; SELECT a FROM t; SELECT c FROM v; SELECT d FROM w LIMIT 5"
)
_MIXED_CELL_LIMITED = [
    "CREATE TABLE z AS SELECT b FROM u",
    "SELECT a FROM t\nLIMIT 100",
    "SELECT c FROM v\nLIMIT 100",
    "SELECT d FROM w LIMIT 5",
]


def test_spark_stream_limits_every_eligible_statement():
    with _spark_statements() as ran:
        list(
            sqlutils.sql_stream(_MIXED_CELL, connection={"type": "spark"}, limit_query_results=100)
        )
    assert [c.args[0] for c in ran.call_args_list] == _MIXED_CELL_LIMITED


def test_irc_glue_stream_limits_every_eligible_statement():
    with _irc_statements() as run:
        list(sqlutils.sql_stream(_MIXED_CELL, connection_id="irc-1", limit_query_results=100))
    assert [c.args[0] for c in run.call_args_list] == _MIXED_CELL_LIMITED


def test_duckdb_stream_limits_every_eligible_statement():
    with _duckdb_statements() as run:
        list(sqlutils.sql_stream(_MIXED_CELL, limit_query_results=100))
    assert _duckdb_ran(run) == _MIXED_CELL_LIMITED


def test_a_multi_statement_cell_is_limited_end_to_end():
    """The path a notebook cell actually takes: sql_stream_with_display -> sql_stream -> engine.

    Only the IPython display and assignment step is stubbed, and it is stubbed with something
    that still consumes the stream -- a MagicMock would leave the generator unread and no
    statement would run at all."""
    with _duckdb_statements() as run, patch.object(
        sqlutils, "_materialise_stream", lambda stream, dataframe_name: list(stream)
    ):
        sqlutils.sql_stream_with_display(_MIXED_CELL, "df", limit_query_results=100)

    assert _duckdb_ran(run) == _MIXED_CELL_LIMITED


def test_a_multi_statement_cell_without_the_kwarg_runs_the_authors_sql():
    with _duckdb_statements() as run, patch.object(
        sqlutils, "_materialise_stream", lambda stream, dataframe_name: list(stream)
    ):
        sqlutils.sql_stream_with_display(_MIXED_CELL, "df")

    assert _duckdb_ran(run) == [
        "CREATE TABLE z AS SELECT b FROM u",
        "SELECT a FROM t",
        "SELECT c FROM v",
        "SELECT d FROM w LIMIT 5",
    ]
