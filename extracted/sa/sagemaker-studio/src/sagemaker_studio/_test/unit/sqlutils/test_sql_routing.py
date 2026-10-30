"""``sqlutils._route``: the one place a statement's engine is chosen, for ``sql``, ``sql_stream``
and the async path."""

import unittest
from unittest.mock import MagicMock, patch

from sagemaker_studio.sql_engine.duckdb_engine import engine as duckdb_engine
from sagemaker_studio.utils import duckdbutils, sqlutils


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
