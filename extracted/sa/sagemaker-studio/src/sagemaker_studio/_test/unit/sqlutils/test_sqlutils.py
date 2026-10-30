import os
import sys
import tempfile
import threading
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, PropertyMock, call, patch

from dateutil.tz import tzlocal
from pandas import DataFrame

from sagemaker_studio import Connection, sqlutils
from sagemaker_studio.project import Project
from sagemaker_studio.sql_engine.duckdb_engine import engine as duckdb_engine
from sagemaker_studio.sql_engine.duckdb_engine import extensions as duckdb_extensions
from sagemaker_studio.sql_engine.sql_executor import SqlExecutor
from sagemaker_studio.utils._sql_cache import ConnectionCache, ManagedConnection


class TestSqlutils(unittest.TestCase):

    def setUp(self):
        """Setup test fixtures"""
        self.mock_executor = Mock(spec=SqlExecutor)
        self.mock_project = Mock(spec=Project)

        # Reset global variables
        sqlutils._project = None
        sqlutils._sql_executor = SqlExecutor()
        sqlutils._connection_cache.clear()  # Clear cache between tests

        # Create mock connection data that will be used across tests
        self.connection_dict = {
            "connectionId": "connectionid12",
            "description": "This is a default ATHENA connection.",
            "domainId": "dzd_domainid124567",
            "domainUnitId": "domainunitid12",
            "environmentId": "environmentid1",
            "environmentUserRole": "arn:aws:iam::123456789012:role/datazone_usr_role_projectid12345_environmentid1",
            "name": "project.athena",
            "physicalEndpoints": [
                {"awsLocation": {"awsAccountId": "123456789012", "awsRegion": "us-east-1"}}
            ],
            "projectId": "projectid12345",
            "workgroupName": "workgroup-projectid12345-environmentid1",
            "type": "ATHENA",
            "connectionCredentials": {
                "accessKeyId": "mock_access_key",
                "secretAccessKey": "mock_secret_key",
                "sessionToken": "mock_session_token",
                "expiration": datetime(2025, 1, 1, 12, 00, 00, tzinfo=tzlocal()).isoformat(),
            },
        }

        # Create a temporary Connection instance just to use _create_connection_data
        self.mock_connection = Connection(
            connection_data=self.connection_dict,
            glue_api=Mock(),
            datazone_api=Mock(),
            secrets_manager_api=Mock(),
            kms_api=Mock(),
            project_config=Mock(),
        )

    @patch("sagemaker_studio.sql_engine.duckdb_engine.engine._ensure_duckdb")
    def test_sql_without_connection(self, mock_ensure_duckdb):
        """Test SQL execution without any connection specified"""
        mock_result = Mock()
        mock_result.df.return_value = DataFrame({"col1": [1, 2, 3]})

        mock_duckdb = Mock()
        mock_duckdb.sql.return_value = mock_result

        mock_ensure_duckdb.return_value = mock_duckdb

        query = "SELECT * FROM test_table"
        result = sqlutils.sql(query)

        mock_duckdb.sql.assert_called_once_with(query)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(list(result["col1"]), [1, 2, 3])

    @patch("sagemaker_studio.sqlutils._ensure_project")
    def test_sql_with_athena_connection(self, mock_ensure_project):
        """Athena SQL executes through the SDK-owned API executor."""
        from sagemaker_studio.sql_engine.sql_executor import SingleStatementResult

        mock_project = Mock()
        mock_project.connection = Mock(return_value=self.mock_connection)
        mock_ensure_project.return_value = mock_project
        native = Mock()
        native.execute.return_value = SingleStatementResult(
            result=DataFrame({"col1": [1, 2, 3]}),
            execution_metadata={"query_execution_id": "q"},
        )

        query = "SELECT * FROM test_table"
        with patch.object(sqlutils, "_athena_api", return_value=native):
            result = sqlutils.sql(query, connection_name="project.athena")

        mock_project.connection.assert_called_once_with("project.athena")
        native.execute.assert_called_once_with(query)
        self.assertEqual(list(result["col1"]), [1, 2, 3])

    @patch("sagemaker_studio.sqlutils.HelperFactory")
    @patch("sagemaker_studio.sqlutils._ensure_project")
    @patch("sagemaker_studio.sqlutils._ensure_sql_executor")
    @patch(
        "sagemaker_studio.connections.connection.Connection._get_aws_client_with_connection_credentials"
    )
    def test_sql_with_redshift_connection(
        self,
        mock_get_aws_client,
        mock_ensure_sql_executor,
        mock_ensure_project,
        mock_helper_factory,
    ):
        """Test SQL execution with Redshift connection"""
        # Mock the glue API client since REDSHIFT is now in SUPPORTED_GLUE_CONNECTION_TYPES
        mock_glue_api = Mock()
        mock_get_aws_client.return_value = mock_glue_api

        # Create Redshift connection
        redshift_connection_dict = self.connection_dict.copy()
        redshift_connection_dict.update(
            {
                "type": "REDSHIFT",
                "name": "project.redshift",
                "physicalEndpoints": [
                    {
                        "awsLocation": {"awsAccountId": "123456789012", "awsRegion": "us-east-1"},
                        "host": "redshift-cluster.123456789012.us-east-1.redshift.amazonaws.com",
                        "port": "5439",
                    }
                ],
            }
        )

        redshift_connection = Connection(
            connection_data=redshift_connection_dict,
            glue_api=Mock(),
            datazone_api=Mock(),
            secrets_manager_api=Mock(),
            kms_api=Mock(),
            project_config=Mock(),
        )

        mock_project = Mock()
        mock_project.connection.return_value = redshift_connection
        mock_ensure_project.return_value = mock_project

        # Setup mock SQL helper
        mock_sql_helper = Mock()
        mock_sql_helper.to_sql_config.return_value = {
            "region_name": "us-east-1",
            "aws_access_key_id": "mock_access_key",
            "aws_secret_access_key": "mock_secret_key",
            "aws_session_token": "mock_session_token",
            "host": "redshift-cluster.123456789012.us-east-1.redshift.amazonaws.com",
            "port": "5439",
            "database": "dev",
            "schema": "public",
        }
        mock_helper_factory.get_sql_helper.return_value = mock_sql_helper

        mock_sql_executor = Mock()
        mock_ensure_sql_executor.return_value = mock_sql_executor
        mock_engine = Mock()
        mock_sql_executor.create_engine.return_value = mock_engine
        mock_sql_executor.get_supported_connection_types.return_value = ["REDSHIFT"]

        # Mock execute to return ExecutionResult generator
        from sagemaker_studio.sql_engine.sql_executor import ExecutionResult

        execution_result = ExecutionResult(
            statement_index=0,
            statement="SELECT * FROM test_table",
            statement_type="SELECT",
            result=DataFrame({"col1": [1, 2, 3]}),
            status="success",
        )
        mock_sql_executor.execute.return_value = iter([execution_result])

        query = "SELECT * FROM test_table"
        sqlutils.sql(query, connection_name="project.redshift")

        # Verify interactions
        mock_helper_factory.get_sql_helper.assert_called_once_with("REDSHIFT")

        # Verify sql helper was called
        self.assertEqual(mock_sql_helper.to_sql_config.call_count, 1)
        call_args = mock_sql_helper.to_sql_config.call_args
        self.assertEqual(call_args[0][0], redshift_connection)

        mock_sql_executor.create_engine.assert_called_once_with(
            "REDSHIFT", mock_sql_helper.to_sql_config.return_value
        )
        # Verify execute was called with connection (persist_session=True by default)
        mock_sql_executor.execute.assert_called_once()
        call_args = mock_sql_executor.execute.call_args
        self.assertEqual(call_args[0][0], mock_engine)  # engine (positional)
        self.assertEqual(call_args[0][1], query)  # query (positional)
        self.assertIsNotNone(call_args[1]["connection"])  # connection (keyword)
        self.assertEqual(call_args[1].get("parameters"), None)  # parameters (keyword)

    @patch("sagemaker_studio.sql_engine.duckdb_engine.engine._ensure_duckdb")
    def test_sql_stream_without_connection(self, mock_ensure_duckdb):
        """Test sql_stream execution without any connection specified"""
        mock_result1 = Mock()
        mock_result1.df.return_value = DataFrame({"col1": [1]})
        mock_result2 = Mock()
        mock_result2.df.return_value = DataFrame({"col1": [2]})

        mock_duckdb = Mock()
        mock_duckdb.sql.side_effect = [mock_result1, mock_result2]
        mock_ensure_duckdb.return_value = mock_duckdb

        query = "SELECT 1; SELECT 2"
        results = list(sqlutils.sql_stream(query))

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].status, "success")
        self.assertEqual(results[1].status, "success")

    @patch("sagemaker_studio.sqlutils._ensure_project")
    def test_sql_stream_with_connection(self, mock_ensure_project):
        """Athena streaming executes through the SDK-owned API executor."""
        from sagemaker_studio.sql_engine.sql_executor import SingleStatementResult

        mock_project = Mock()
        mock_project.connection.return_value = self.mock_connection
        mock_ensure_project.return_value = mock_project
        native = Mock()
        native.execute.side_effect = lambda statement: SingleStatementResult(
            result=DataFrame({"statement": [statement]}),
            execution_metadata={"query_execution_id": statement},
        )

        with patch.object(sqlutils, "_athena_api", return_value=native):
            results = list(
                sqlutils.sql_stream("SELECT 1; SELECT 2", connection_name="project.athena")
            )

        self.assertEqual(len(results), 2)
        self.assertEqual(native.execute.call_count, 2)

    @patch("sagemaker_studio.sql_engine.duckdb_engine.engine._ensure_duckdb")
    def test_sql_with_parameters_no_connection(self, mock_ensure_duckdb):
        """Test sql with parameters and no connection"""
        mock_result = Mock()
        mock_result.df.return_value = DataFrame({"col1": [42]})

        mock_duckdb = Mock()
        mock_duckdb.sql.return_value = mock_result
        mock_ensure_duckdb.return_value = mock_duckdb

        query = "SELECT :param"
        parameters = {"param": 42}
        result = sqlutils.sql(query, parameters)

        mock_duckdb.sql.assert_called_once_with(query)
        self.assertIsInstance(result, DataFrame)

    @patch("sagemaker_studio.sqlutils._ensure_project")
    def test_sql_with_connection_id(self, mock_ensure_project):
        """Native Athena execution resolves a connection by ID once."""
        from sagemaker_studio.sql_engine.sql_executor import SingleStatementResult

        mock_project = Mock()
        mock_project.connection = Mock(return_value=self.mock_connection)
        mock_ensure_project.return_value = mock_project
        native = Mock()
        native.execute.return_value = SingleStatementResult(
            result=DataFrame({"col1": [1]}),
            execution_metadata={"query_execution_id": "q"},
        )

        with patch.object(sqlutils, "_athena_api", return_value=native):
            result = sqlutils.sql("SELECT 1", connection_id="conn123")

        mock_project.connection.assert_called_once_with(id="conn123")
        native.execute.assert_called_once_with("SELECT 1")
        self.assertIsInstance(result, DataFrame)

    @patch("sagemaker_studio.sqlutils._ensure_project")
    def test_get_engine_multiple_params_error(self, mock_ensure_project):
        """Test get_engine raises error when multiple connection params provided"""
        with self.assertRaises(ValueError) as cm:
            sqlutils.get_engine(connection_id="conn1", connection_name="conn2")
        self.assertIn(
            "Only one of connection_id or connection_name should be provided", str(cm.exception)
        )

    @patch("sagemaker_studio.sqlutils._ensure_project")
    def test_get_engine_project_not_initialized(self, mock_ensure_project):
        """Test get_engine raises error when project not initialized"""
        mock_ensure_project.return_value = False

        with self.assertRaises(RuntimeError) as cm:
            sqlutils.get_engine(connection_name="test")
        self.assertIn("Project is not initialized", str(cm.exception))

    @patch("sagemaker_studio.sqlutils.HelperFactory")
    @patch("sagemaker_studio.sqlutils._ensure_project")
    @patch("sagemaker_studio.sqlutils._sql_executor")
    def test_get_engine_unsupported_connection_type(
        self, mock_sql_executor, mock_ensure_project, mock_helper_factory
    ):
        """Test get_engine raises error for unsupported connection type"""
        mock_project = Mock()
        mock_connection = Mock()
        mock_connection.type = "UNSUPPORTED"
        mock_project.connection.return_value = mock_connection
        mock_ensure_project.return_value = mock_project

        mock_sql_executor.get_supported_connection_types.return_value = ["ATHENA", "REDSHIFT"]

        with self.assertRaises(RuntimeError) as cm:
            sqlutils.get_engine(connection_name="test")
        self.assertIn("SQL is not supported for connection type UNSUPPORTED", str(cm.exception))

    @patch("sagemaker_studio.sqlutils._ensure_spark")
    def test_sql_with_spark_connection(self, mock_ensure_spark):
        """Test SQL execution with Spark connection using connection object"""
        # Mock Spark session
        mock_spark = Mock()
        mock_spark_df = Mock()
        mock_spark.sql.return_value = mock_spark_df
        mock_ensure_spark.return_value = mock_spark

        query = "SELECT * FROM test_table"
        result = sqlutils.sql(query, connection={"type": "spark"})

        # Verify Spark session was retrieved
        mock_ensure_spark.assert_called_once()

        # Verify Spark SQL was called
        mock_spark.sql.assert_called_once_with(query)

        # Verify result is Spark DataFrame (not pandas)
        self.assertEqual(result, mock_spark_df)

    @patch("sagemaker_studio.sqlutils._ensure_spark")
    def test_sql_stream_with_spark_connection(self, mock_ensure_spark):
        """Test sql_stream execution with Spark connection for multi-statement support"""
        # Mock Spark session
        mock_spark = Mock()
        mock_spark_df1 = Mock()
        mock_spark_df2 = Mock()
        mock_spark.sql.side_effect = [mock_spark_df1, mock_spark_df2]
        mock_ensure_spark.return_value = mock_spark

        query = "SELECT 1; SELECT 2"
        results = list(sqlutils.sql_stream(query, connection={"type": "spark"}))

        # Verify we got 2 results
        self.assertEqual(len(results), 2)

        # Verify both statements were executed
        self.assertEqual(mock_spark.sql.call_count, 2)

        # Verify results contain Spark DataFrames
        self.assertEqual(results[0].result, mock_spark_df1)
        self.assertEqual(results[1].result, mock_spark_df2)
        self.assertEqual(results[0].status, "success")
        self.assertEqual(results[1].status, "success")

    # --- Athena context injection ---

    @patch("sagemaker_studio.utils.sql_handler.get_execution_context")
    @patch("sagemaker_studio.sqlutils._athena_api")
    @patch("sagemaker_studio.sqlutils._resolve_connection")
    def test_sql_athena_injects_catalog_and_schema(self, mock_resolve, mock_athena, mock_ctx):
        """When Athena query has catalog+database, they are passed as kwargs."""
        from sagemaker_studio.sql_engine.sql_executor import SingleStatementResult

        mock_resolve.return_value = Mock(type="ATHENA")
        native = Mock()
        native.execute.return_value = SingleStatementResult(result="df")
        mock_athena.return_value = native
        mock_ctx.return_value = {"catalog": "my_cat", "database": "my_db"}

        sqlutils.sql("SELECT 1", connection_id="c1")
        mock_ctx.assert_called_once()
        mock_athena.assert_called_once_with(
            mock_resolve.return_value,
            {"catalog_name": "my_cat", "schema_name": "my_db"},
            None,
            required=True,
        )

    @patch("sagemaker_studio.utils.sql_handler.get_execution_context")
    @patch("sagemaker_studio.sqlutils._athena_api")
    @patch("sagemaker_studio.sqlutils._resolve_connection")
    def test_sql_stream_athena_injects_catalog_and_schema(
        self, mock_resolve, mock_athena, mock_ctx
    ):
        """sql_stream with Athena also calls _apply_athena_context."""
        from sagemaker_studio.sql_engine.sql_executor import SingleStatementResult

        mock_resolve.return_value = Mock(type="ATHENA")
        native = Mock()
        native.execute.return_value = SingleStatementResult(result="df")
        mock_athena.return_value = native
        mock_ctx.return_value = {"catalog": "cat1", "database": "db1"}

        list(sqlutils.sql_stream("SELECT 1", connection_id="c1"))
        mock_ctx.assert_called_once()
        mock_athena.assert_called_once_with(
            mock_resolve.return_value,
            {"catalog_name": "cat1", "schema_name": "db1"},
            None,
            required=True,
        )

    # --- _ensure_spark ---

    def test_ensure_spark_import_error(self):
        """_ensure_spark raises RuntimeError when IPython is not installed"""
        with patch.dict("sys.modules", {"IPython": None}):
            with self.assertRaises(RuntimeError) as cm:
                sqlutils._ensure_spark()
            self.assertIn("IPython not available", str(cm.exception))

    def test_ensure_spark_ipython_none(self):
        """_ensure_spark raises when get_ipython returns None"""
        mock_module = Mock()
        mock_module.get_ipython = Mock(return_value=None)
        with patch.dict("sys.modules", {"IPython": mock_module}):
            with self.assertRaises(RuntimeError) as cm:
                sqlutils._ensure_spark()
            self.assertIn("IPython kernel not available", str(cm.exception))

    def test_ensure_spark_no_spark_in_ns(self):
        """_ensure_spark raises when spark not in user_ns"""
        mock_ipython = Mock()
        mock_ipython.user_ns = {}
        mock_module = Mock()
        mock_module.get_ipython = Mock(return_value=mock_ipython)
        with patch.dict("sys.modules", {"IPython": mock_module}):
            with self.assertRaises(RuntimeError) as cm:
                sqlutils._ensure_spark()
            self.assertIn("Spark session not initialized", str(cm.exception))

    def test_ensure_spark_success(self):
        """_ensure_spark returns spark when available"""
        mock_spark = Mock()
        mock_ipython = Mock()
        mock_ipython.user_ns = {"spark": mock_spark}
        mock_module = Mock()
        mock_module.get_ipython = Mock(return_value=mock_ipython)
        with patch.dict("sys.modules", {"IPython": mock_module}):
            result = sqlutils._ensure_spark()
        self.assertEqual(result, mock_spark)

    # --- _is_spark_connection ---

    def test_is_spark_connection_none(self):
        self.assertFalse(sqlutils._is_spark_connection(None))

    def test_is_spark_connection_empty(self):
        self.assertFalse(sqlutils._is_spark_connection({}))

    def test_is_spark_connection_spark(self):
        self.assertTrue(sqlutils._is_spark_connection({"type": "spark"}))

    def test_is_spark_connection_unknown_type_raises(self):
        with self.assertRaises(ValueError):
            sqlutils._is_spark_connection({"type": "mysql"})

    # --- _apply_athena_context ---

    @patch("sagemaker_studio.utils.sql_handler.get_execution_context")
    def test_apply_athena_context_injects_kwargs(self, mock_ctx):
        mock_ctx.return_value = {"catalog": "cat", "database": "db"}
        kwargs = {}
        sqlutils._apply_athena_context("SELECT 1", kwargs)
        self.assertEqual(kwargs["catalog_name"], "cat")
        self.assertEqual(kwargs["schema_name"], "db")

    @patch("sagemaker_studio.utils.sql_handler.get_execution_context")
    def test_apply_athena_context_skips_if_already_set(self, mock_ctx):
        kwargs = {"catalog_name": "existing", "schema_name": "existing"}
        sqlutils._apply_athena_context("SELECT 1", kwargs)
        mock_ctx.assert_not_called()
        self.assertEqual(kwargs["catalog_name"], "existing")

    @patch("sagemaker_studio.utils.sql_handler.get_execution_context")
    def test_apply_athena_context_no_context_found(self, mock_ctx):
        mock_ctx.return_value = {"catalog": None, "database": None}
        kwargs = {}
        sqlutils._apply_athena_context("SELECT 1", kwargs)
        self.assertNotIn("catalog_name", kwargs)

    # --- get_engine returns None ---

    def test_get_engine_no_params_returns_none(self):
        self.assertIsNone(sqlutils.get_engine())

    # --- sql_stream returns generator (no dataframe_name) ---

    @patch("sagemaker_studio.sqlutils._ensure_spark")
    def test_sql_stream_returns_generator(self, mock_ensure_spark):
        """sql_stream returns the raw generator"""
        mock_spark = Mock()
        mock_spark.sql.return_value = Mock()
        mock_ensure_spark.return_value = mock_spark

        result = sqlutils.sql_stream("SELECT 1", connection={"type": "spark"})

        import types

        self.assertIsInstance(result, types.GeneratorType)

    # --- sql_stream_with_display tests ---

    @patch("sagemaker_studio.sqlutils._ensure_spark")
    @patch("sagemaker_studio.sqlutils._materialise_stream")
    def test_sql_stream_with_display_calls_materialise(self, mock_materialise, mock_ensure_spark):
        """sql_stream_with_display delegates to sql_stream then _materialise_stream"""
        mock_spark = Mock()
        mock_spark.sql.return_value = Mock()
        mock_ensure_spark.return_value = mock_spark

        sqlutils.sql_stream_with_display(
            "SELECT 1", dataframe_name="df", connection={"type": "spark"}
        )

        mock_materialise.assert_called_once()
        args = mock_materialise.call_args
        self.assertEqual(args[0][1], "df")

    @patch("sagemaker_studio.sqlutils._stream_with_async_materialization", return_value=True)
    def test_sql_stream_with_display_forwards_first_page_rows_to_async(self, mock_async):
        """materialize='async' with first_page_rows forwards it into the async path (and the
        async path fully handling the query short-circuits the sync fallback)."""
        sqlutils.sql_stream_with_display(
            "SELECT 1",
            dataframe_name="df",
            connection_id="c1",
            materialize="async",
            first_page_rows=5000,
        )
        mock_async.assert_called_once()
        self.assertEqual(mock_async.call_args.kwargs.get("first_page_rows"), 5000)

    @patch("sagemaker_studio.sqlutils._ensure_spark")
    def test_sql_stream_with_display_assigns_namespace(self, mock_ensure_spark):
        """sql_stream_with_display materialises results into IPython namespace"""

        mock_spark = Mock()
        df0 = Mock(wraps=DataFrame({"a": [1]}))
        df0.schema = Mock()
        df1 = Mock(wraps=DataFrame({"b": [2]}))
        df1.schema = Mock()
        mock_spark.sql.side_effect = [df0, df1]
        mock_ensure_spark.return_value = mock_spark

        mock_ip, mock_display, modules = self._mock_ipython_modules()

        with patch.dict("sys.modules", modules):
            sqlutils.sql_stream_with_display(
                "SELECT 1; SELECT 2", dataframe_name="df", connection={"type": "spark"}
            )

        self.assertIs(mock_ip.user_ns["df_0"], df0)
        self.assertIs(mock_ip.user_ns["df_1"], df1)
        self.assertIsInstance(mock_ip.user_ns["df"], list)
        self.assertEqual(len(mock_ip.user_ns["df"]), 2)
        self.assertEqual(mock_display.call_count, 2)

    @patch("sagemaker_studio.sqlutils._ensure_spark")
    def test_sql_stream_with_display_single_result(self, mock_ensure_spark):
        """sql_stream_with_display with single result assigns directly (no indexed vars)"""
        mock_spark = Mock()
        df0 = Mock(wraps=DataFrame({"a": [1]}))
        df0.schema = Mock()
        mock_spark.sql.return_value = df0
        mock_ensure_spark.return_value = mock_spark

        mock_ip, mock_display, modules = self._mock_ipython_modules()

        with patch.dict("sys.modules", modules):
            sqlutils.sql_stream_with_display(
                "SELECT 1", dataframe_name="df", connection={"type": "spark"}
            )

        self.assertNotIn("df_0", mock_ip.user_ns)
        self.assertIs(mock_ip.user_ns["df"], df0)
        mock_display.assert_called_once_with(df0, metadata={})

    @patch("sagemaker_studio.sqlutils._ensure_spark")
    def test_sql_stream_with_display_raises_on_error(self, mock_ensure_spark):
        """sql_stream_with_display raises exception on error result"""
        mock_spark = Mock()
        mock_spark.sql.side_effect = Exception("syntax error")
        mock_ensure_spark.return_value = mock_spark

        mock_ip, mock_display, modules = self._mock_ipython_modules()

        with patch.dict("sys.modules", modules):
            with self.assertRaises(Exception) as cm:
                sqlutils.sql_stream_with_display(
                    "BAD SQL", dataframe_name="df", connection={"type": "spark"}
                )

        self.assertIn("syntax error", str(cm.exception))

    def _mock_ipython_modules(self):
        """Create mock IPython modules for _materialise_stream tests.

        Returns (mock_ip, mock_display, modules_dict) where modules_dict
        should be passed to patch.dict("sys.modules", ...).
        """
        mock_ip = Mock()
        mock_ip.user_ns = {}

        mock_ipython_mod = Mock()
        mock_ipython_mod.get_ipython = Mock(return_value=mock_ip)

        mock_display_func = Mock()
        mock_display_mod = Mock()
        mock_display_mod.display = mock_display_func

        modules = {
            "IPython": mock_ipython_mod,
            "IPython.display": mock_display_mod,
        }
        return mock_ip, mock_display_func, modules

    def test_materialise_stream_all_success_multiple(self):
        """Multiple successful results: indexed vars + list variable assigned"""
        from sagemaker_studio.sql_engine.sql_executor import ExecutionResult

        mock_ip, mock_display, modules = self._mock_ipython_modules()

        df0 = DataFrame({"a": [1]})
        df1 = DataFrame({"b": [2]})
        stream = [
            ExecutionResult(0, "SELECT 1", "SELECT", result=df0, status="success"),
            ExecutionResult(1, "SELECT 2", "SELECT", result=df1, status="success"),
        ]

        with patch.dict("sys.modules", modules):
            sqlutils._materialise_stream(iter(stream), "df")

        # Indexed vars assigned
        self.assertIs(mock_ip.user_ns["df_0"], df0)
        self.assertIs(mock_ip.user_ns["df_1"], df1)
        # Main var is a list
        self.assertIsInstance(mock_ip.user_ns["df"], list)
        self.assertEqual(len(mock_ip.user_ns["df"]), 2)
        self.assertIs(mock_ip.user_ns["df"][0], df0)
        self.assertIs(mock_ip.user_ns["df"][1], df1)
        # display called for each result
        self.assertEqual(mock_display.call_count, 2)

    def test_materialise_stream_single_success(self):
        """Single successful result: no indexed vars, main var = single result"""
        from sagemaker_studio.sql_engine.sql_executor import ExecutionResult

        mock_ip, mock_display, modules = self._mock_ipython_modules()

        df0 = DataFrame({"a": [1]})
        stream = [
            ExecutionResult(0, "SELECT 1", "SELECT", result=df0, status="success"),
        ]

        with patch.dict("sys.modules", modules):
            sqlutils._materialise_stream(iter(stream), "df")

        # No indexed vars for single result
        self.assertNotIn("df_0", mock_ip.user_ns)
        # Main var is the single result directly
        self.assertIs(mock_ip.user_ns["df"], df0)
        mock_display.assert_called_once_with(df0, metadata={})

    def test_materialise_stream_attaches_redshift_query_id_as_display_metadata(self):
        from sagemaker_studio.sql_engine.sql_executor import ExecutionResult

        mock_ip, mock_display, modules = self._mock_ipython_modules()

        df0 = DataFrame({"a": [1]})
        df1 = DataFrame({"b": [2]})
        df2 = DataFrame({"c": [3]})
        stream = [
            ExecutionResult(
                0,
                "SELECT 1",
                "SELECT",
                result=df0,
                status="success",
                execution_metadata={"statement_id": "rs-1", "redshift_query_id": 123456},
            ),
            ExecutionResult(
                1,
                "SELECT 'x'",
                "SELECT",
                result=df1,
                status="success",
                execution_metadata={"statement_id": "rs-2"},
            ),
            ExecutionResult(
                2,
                "SELECT 2",
                "SELECT",
                result=df2,
                status="success",
                execution_metadata={"query_execution_id": "athena-1"},
            ),
        ]

        with patch.dict("sys.modules", modules):
            sqlutils._materialise_stream(iter(stream), "df")

        self.assertEqual(
            mock_display.call_args_list,
            [
                call(df0, metadata={"redshift_query_id": 123456}),
                call(df1, metadata={}),
                call(df2, metadata={}),
            ],
        )

    def test_materialise_stream_error_with_partial_results(self):
        """Error after some successes: partial indexed vars saved, then raises"""
        from sagemaker_studio.sql_engine.sql_executor import ExecutionResult

        mock_ip, mock_display, modules = self._mock_ipython_modules()

        df0 = DataFrame({"a": [1]})
        stream = [
            ExecutionResult(0, "SELECT 1", "SELECT", result=df0, status="success"),
            ExecutionResult(1, "BAD SQL", "UNKNOWN", error="syntax error", status="error"),
        ]

        with patch.dict("sys.modules", modules):
            with self.assertRaises(Exception) as cm:
                sqlutils._materialise_stream(iter(stream), "df")

        self.assertIn("syntax error", str(cm.exception))
        # Partial result saved for debugging
        self.assertIs(mock_ip.user_ns["df_0"], df0)
        # Main var NOT assigned on error
        self.assertNotIn("df", mock_ip.user_ns)

    def test_materialise_stream_single_error_no_results(self):
        """Single error with no prior successes: nothing saved, raises"""
        from sagemaker_studio.sql_engine.sql_executor import ExecutionResult

        mock_ip, mock_display, modules = self._mock_ipython_modules()

        stream = [
            ExecutionResult(0, "BAD SQL", "UNKNOWN", error="table not found", status="error"),
        ]

        with patch.dict("sys.modules", modules):
            with self.assertRaises(Exception) as cm:
                sqlutils._materialise_stream(iter(stream), "df")

        self.assertIn("table not found", str(cm.exception))
        # Nothing saved
        self.assertNotIn("df_0", mock_ip.user_ns)
        self.assertNotIn("df", mock_ip.user_ns)
        mock_display.assert_not_called()

    def test_materialise_stream_error_wraps_string(self):
        """When result.error is a string, it is wrapped in Exception"""
        from sagemaker_studio.sql_engine.sql_executor import ExecutionResult

        mock_ip, mock_display, modules = self._mock_ipython_modules()

        stream = [
            ExecutionResult(0, "BAD SQL", "UNKNOWN", error="some error string", status="error"),
        ]

        with patch.dict("sys.modules", modules):
            with self.assertRaises(Exception) as cm:
                sqlutils._materialise_stream(iter(stream), "df")

        self.assertNotIsInstance(cm.exception, RuntimeError)
        self.assertIn("some error string", str(cm.exception))

    def test_materialise_stream_empty_results(self):
        """Empty stream: nothing assigned to namespace"""
        mock_ip, mock_display, modules = self._mock_ipython_modules()

        with patch.dict("sys.modules", modules):
            sqlutils._materialise_stream(iter([]), "df")

        self.assertNotIn("df", mock_ip.user_ns)
        mock_display.assert_not_called()


class TestConnectionCache(unittest.TestCase):
    """Test ConnectionCache functionality"""

    def setUp(self):
        sqlutils._connection_cache.clear()

    def tearDown(self):
        sqlutils._connection_cache.clear()

    def test_cache_stores_and_retrieves_connection(self):
        """Test cache can store and retrieve connections"""

        mock_engine = Mock()
        mock_connection = Mock()
        mock_connection.closed = False

        managed_conn = ManagedConnection(
            engine=mock_engine, connection=mock_connection, id="test-id-1", cache_key="key1"
        )
        sqlutils._connection_cache.put("key1", managed_conn)
        cached = sqlutils._connection_cache.get("key1")

        self.assertIsNotNone(cached)
        self.assertEqual(cached.engine, mock_engine)
        self.assertEqual(cached.connection, mock_connection)
        self.assertEqual(cached.cache_key, "key1")

    def test_cache_returns_none_for_missing_key(self):
        """Test cache returns None for non-existent key"""
        self.assertIsNone(sqlutils._connection_cache.get("nonexistent"))

    def test_cache_remove(self):
        """Test cache can remove entries"""

        mock_engine = Mock()
        mock_connection = Mock()
        mock_connection.closed = False

        managed_conn = ManagedConnection(
            engine=mock_engine, connection=mock_connection, id="test-id-1", cache_key="key1"
        )
        sqlutils._connection_cache.put("key1", managed_conn)
        self.assertIsNotNone(sqlutils._connection_cache.get("key1"))

        sqlutils._connection_cache.remove("key1")
        self.assertIsNone(sqlutils._connection_cache.get("key1"))

    def test_cache_clear(self):
        """Test cache can clear all entries"""

        mock_conn1 = Mock()
        mock_conn1.closed = False
        mock_conn2 = Mock()
        mock_conn2.closed = False

        sqlutils._connection_cache.put(
            "key1", ManagedConnection(Mock(), mock_conn1, "id-1", "key1")
        )
        sqlutils._connection_cache.put(
            "key2", ManagedConnection(Mock(), mock_conn2, "id-2", "key2")
        )

        self.assertEqual(len(sqlutils._connection_cache), 2)

        sqlutils._connection_cache.clear()
        self.assertEqual(len(sqlutils._connection_cache), 0)

    def test_cache_list_keys(self):
        """Test cache can list all keys"""

        mock_conn1 = Mock()
        mock_conn1.closed = False
        mock_conn2 = Mock()
        mock_conn2.closed = False

        sqlutils._connection_cache.put(
            "key1", ManagedConnection(Mock(), mock_conn1, "id-1", "key1")
        )
        sqlutils._connection_cache.put(
            "key2", ManagedConnection(Mock(), mock_conn2, "id-2", "key2")
        )

        keys = sqlutils._connection_cache.list_keys()
        self.assertEqual(set(keys), {"key1", "key2"})

    def test_cache_contains(self):
        """Test cache __contains__ method"""

        mock_conn = Mock()
        mock_conn.closed = False

        sqlutils._connection_cache.put("key1", ManagedConnection(Mock(), mock_conn, "id-1", "key1"))

        self.assertTrue("key1" in sqlutils._connection_cache)
        self.assertFalse("key2" in sqlutils._connection_cache)


class TestConnectionCacheConcurrencyAndTeardown(unittest.TestCase):
    """Cover the health-check eviction, teardown, and concurrency-safe removal paths."""

    def setUp(self):
        self.cache = ConnectionCache()

    def _managed(self, conn_id="id-1", key="key1", closed=False, connection=None):
        if connection is None:
            connection = Mock()
            connection.closed = closed
        return ManagedConnection(engine=Mock(), connection=connection, id=conn_id, cache_key=key)

    def test_get_evicts_and_tears_down_closed_connection(self):
        """get() on a closed connection evicts it (teardown outside lock) and returns None."""
        conn = Mock()
        conn.closed = True
        mc = self._managed(connection=conn)
        self.cache.put("key1", mc)

        self.assertIsNone(self.cache.get("key1"))
        self.assertNotIn("key1", self.cache)
        conn.close.assert_called_once()
        mc.engine.dispose.assert_called_once()

    def test_get_evicts_when_closed_check_raises(self):
        """If reading .closed raises, get() treats it as unhealthy and evicts."""
        conn = Mock()
        type(conn).closed = PropertyMock(side_effect=RuntimeError("boom"))
        mc = self._managed(connection=conn)
        self.cache.put("key1", mc)

        self.assertIsNone(self.cache.get("key1"))
        self.assertNotIn("key1", self.cache)

    def test_put_replacing_key_drops_previous_id_mapping(self):
        """Re-caching a key with a new connection drops the old id->key mapping so a later
        remove_by_id(old_id) cannot tear down the current healthy connection."""
        first = self._managed(conn_id="id-old", key="key1")
        self.cache.put("key1", first)
        second = self._managed(conn_id="id-new", key="key1")
        self.cache.put("key1", second)

        # Old id no longer resolves; the current entry is untouched.
        self.assertFalse(self.cache.remove_by_id("id-old"))
        self.assertIsNotNone(self.cache.get("key1"))
        # New id still resolves.
        self.assertTrue(self.cache.remove_by_id("id-new"))
        self.assertNotIn("key1", self.cache)

    def test_teardown_skips_close_when_connection_is_none(self):
        """_teardown disposes the engine but skips close() when connection is None."""
        mc = self._managed(connection=Mock())
        mc.connection = None
        self.cache.put("key1", mc)

        self.assertTrue(self.cache.remove("key1"))
        mc.engine.dispose.assert_called_once()

    def test_teardown_swallows_dispose_error(self):
        """A failing engine.dispose() is logged and swallowed, not raised."""
        conn = Mock()
        conn.closed = False
        mc = self._managed(connection=conn)
        mc.engine.dispose.side_effect = RuntimeError("dispose failed")
        self.cache.put("key1", mc)

        self.assertTrue(self.cache.remove("key1"))  # does not raise
        conn.close.assert_called_once()

    def test_remove_if_same_leaves_replaced_entry_untouched(self):
        """The compare-and-swap guard does not tear down a fresh connection that replaced the
        stale one (the get()-eviction TOCTOU window)."""
        stale = self._managed(conn_id="id-stale", key="key1")
        fresh = self._managed(conn_id="id-fresh", key="key1")
        self.cache.put("key1", fresh)  # current entry is the fresh one

        # Asking to remove the stale object must be a no-op and leave fresh in place.
        self.assertFalse(self.cache._remove_if_same("key1", stale))
        self.assertIsNotNone(self.cache.get("key1"))
        fresh.connection.close.assert_not_called()

    def test_remove_by_id_unknown_returns_false(self):
        """remove_by_id for an id not present returns False."""
        self.assertFalse(self.cache.remove_by_id("no-such-id"))

    def test_remove_by_id_leaves_replaced_entry_untouched(self):
        """If the entry at the resolved key was replaced (concurrent put) by the time
        remove_by_id tears down, the current (different-id) connection is not removed."""
        stale = self._managed(conn_id="id-stale", key="key1")
        self.cache.put("key1", stale)
        # Simulate a concurrent replacement: same key, fresh connection with a new id.
        fresh = self._managed(conn_id="id-fresh", key="key1")
        self.cache.put("key1", fresh)

        # id-stale no longer maps anywhere (put dropped it); remove_by_id is a no-op.
        self.assertFalse(self.cache.remove_by_id("id-stale"))
        self.assertIsNotNone(self.cache.get("key1"))
        fresh.connection.close.assert_not_called()
        # The current id still removes cleanly.
        self.assertTrue(self.cache.remove_by_id("id-fresh"))
        self.assertNotIn("key1", self.cache)

    def test_remove_missing_key_returns_false(self):
        """remove() for a key not present returns False (no teardown attempted)."""
        self.assertFalse(self.cache.remove("no-such-key"))

    def test_clear_skips_key_removed_concurrently(self):
        """clear() snapshots keys then removes outside the lock; a key already gone by the time
        remove() runs is skipped and not counted."""
        self.cache.put("key1", self._managed(conn_id="id-1", key="key1"))
        self.cache.put("key2", self._managed(conn_id="id-2", key="key2"))

        real_remove = self.cache.remove

        def flaky_remove(key):
            # Simulate a concurrent disappearance of key2 before clear() reaches it.
            if key == "key2":
                return False
            return real_remove(key)

        self.cache.remove = flaky_remove
        self.assertEqual(self.cache.clear(), 1)

    def test_clear_removes_all_and_counts(self):
        """clear() tears down every entry (outside the lock) and returns the count."""
        self.cache.put("key1", self._managed(conn_id="id-1", key="key1"))
        self.cache.put("key2", self._managed(conn_id="id-2", key="key2"))

        self.assertEqual(self.cache.clear(), 2)
        self.assertEqual(len(self.cache), 0)


class TestSessionPersistence(unittest.TestCase):
    """Test session persistence functionality"""

    def setUp(self):
        sqlutils._connection_cache.clear()

    def tearDown(self):
        sqlutils._connection_cache.clear()

    @patch("sagemaker_studio.sqlutils.HelperFactory")
    @patch("sagemaker_studio.sqlutils._ensure_project")
    @patch("sagemaker_studio.sqlutils._ensure_sql_executor")
    def test_persist_session_caches_connection(
        self, mock_ensure_sql_executor, mock_ensure_project, mock_helper_factory
    ):
        """Test persist_session=True caches connection"""
        mock_project = Mock()
        mock_connection = Mock()
        mock_connection.type = "REDSHIFT"
        mock_connection.id = "conn_123"
        mock_project.connection.return_value = mock_connection
        mock_ensure_project.return_value = mock_project

        mock_sql_helper = Mock()
        mock_sql_helper.to_sql_config.return_value = {"region_name": "us-east-1"}
        mock_helper_factory.get_sql_helper.return_value = mock_sql_helper

        mock_sql_executor = Mock()
        mock_ensure_sql_executor.return_value = mock_sql_executor
        mock_engine = Mock()
        mock_db_connection = Mock()
        mock_engine.connect.return_value.__enter__ = Mock(return_value=mock_db_connection)
        mock_engine.connect.return_value.__exit__ = Mock(return_value=None)
        mock_sql_executor.create_engine.return_value = mock_engine
        mock_sql_executor.get_supported_connection_types.return_value = ["REDSHIFT"]

        from sagemaker_studio.sql_engine.sql_executor import ExecutionResult

        execution_result = ExecutionResult(
            statement_index=0,
            statement="SELECT 1",
            statement_type="SELECT",
            result=DataFrame({"col1": [1]}),
            status="success",
        )
        mock_sql_executor.execute.return_value = iter([execution_result])

        # First call with persist_session=True
        sqlutils.sql_stream("SELECT 1", connection_name="test_conn", persist_session=True)
        # Consume generator
        list(sqlutils.sql_stream("SELECT 1", connection_name="test_conn", persist_session=True))

        # Verify connection was cached
        self.assertEqual(len(sqlutils._connection_cache), 1)
        self.assertTrue("test_conn" in sqlutils._connection_cache)

    @patch("sagemaker_studio.sqlutils.HelperFactory")
    @patch("sagemaker_studio.sqlutils._ensure_project")
    @patch("sagemaker_studio.sqlutils._ensure_sql_executor")
    def test_persist_session_reuses_cached_connection(
        self, mock_ensure_sql_executor, mock_ensure_project, mock_helper_factory
    ):
        """Test persist_session=True reuses cached connection"""

        mock_project = Mock()
        mock_connection = Mock()
        mock_connection.type = "REDSHIFT"
        mock_connection.id = "conn_123"
        mock_project.connection.return_value = mock_connection
        mock_ensure_project.return_value = mock_project

        mock_sql_helper = Mock()
        mock_sql_helper.to_sql_config.return_value = {"region_name": "us-east-1"}
        mock_helper_factory.get_sql_helper.return_value = mock_sql_helper

        mock_sql_executor = Mock()
        mock_ensure_sql_executor.return_value = mock_sql_executor
        mock_engine = Mock()
        mock_db_connection = Mock()
        mock_db_connection.closed = False
        mock_sql_executor.create_engine.return_value = mock_engine
        mock_sql_executor.get_supported_connection_types.return_value = ["REDSHIFT"]

        from sagemaker_studio.sql_engine.sql_executor import ExecutionResult

        execution_result = ExecutionResult(
            statement_index=0,
            statement="SELECT 1",
            statement_type="SELECT",
            result=DataFrame({"col1": [1]}),
            status="success",
        )
        mock_sql_executor.execute.return_value = iter([execution_result])

        # Pre-populate cache
        managed_conn = ManagedConnection(
            engine=mock_engine,
            connection=mock_db_connection,
            id="test-conn-id",
            cache_key="test_conn",
        )
        sqlutils._connection_cache.put("test_conn", managed_conn)

        # Call with persist_session=True
        list(sqlutils.sql_stream("SELECT 1", connection_name="test_conn", persist_session=True))

        # Verify engine was not created again
        mock_sql_executor.create_engine.assert_not_called()
        # Verify execute was called with cached connection
        mock_sql_executor.execute.assert_called_once()
        call_args = mock_sql_executor.execute.call_args
        self.assertEqual(
            call_args[1]["connection"], mock_db_connection
        )  # connection is keyword arg

    @patch("sagemaker_studio.sql_engine.duckdb_engine.engine._ensure_duckdb")
    def test_sql_stream_with_duckdb(self, mock_ensure_duckdb):
        """Test sql_stream without connection uses DuckDB"""
        mock_result1 = Mock()
        mock_result1.df.return_value = DataFrame({"col1": [1]})
        mock_result2 = Mock()
        mock_result2.df.return_value = DataFrame({"col1": [2]})

        mock_duckdb = Mock()
        mock_duckdb.sql.side_effect = [mock_result1, mock_result2]
        mock_ensure_duckdb.return_value = mock_duckdb

        results = list(sqlutils.sql_stream("SELECT 1; SELECT 2"))

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].status, "success")
        self.assertEqual(results[1].status, "success")

    @patch("sagemaker_studio.sqlutils.HelperFactory")
    @patch("sagemaker_studio.sqlutils._ensure_project")
    @patch("sagemaker_studio.sqlutils._ensure_sql_executor")
    def test_sql_stream_with_connection_id(
        self, mock_ensure_sql_executor, mock_ensure_project, mock_helper_factory
    ):
        """Test sql_stream with connection_id instead of connection_name"""
        mock_project = Mock()
        mock_connection = Mock()
        mock_connection.type = "REDSHIFT"
        mock_connection.id = "conn_123"
        mock_project.connection.return_value = mock_connection
        mock_ensure_project.return_value = mock_project

        mock_sql_helper = Mock()
        mock_sql_helper.to_sql_config.return_value = {"region_name": "us-east-1"}
        mock_helper_factory.get_sql_helper.return_value = mock_sql_helper

        mock_sql_executor = Mock()
        mock_ensure_sql_executor.return_value = mock_sql_executor
        mock_engine = Mock()
        mock_sql_executor.create_engine.return_value = mock_engine
        mock_sql_executor.get_supported_connection_types.return_value = ["REDSHIFT"]

        from sagemaker_studio.sql_engine.sql_executor import ExecutionResult

        execution_result = ExecutionResult(
            statement_index=0,
            statement="SELECT 1",
            statement_type="SELECT",
            result=DataFrame({"col1": [1]}),
            status="success",
        )
        mock_sql_executor.execute.return_value = iter([execution_result])

        list(sqlutils.sql_stream("SELECT 1", connection_id="conn_123", persist_session=True))

        # Verify connection was fetched by ID
        mock_project.connection.assert_called_with(id="conn_123")
        # Verify connection was cached
        self.assertTrue("conn_123" in sqlutils._connection_cache)

    @patch("sagemaker_studio.sqlutils.HelperFactory")
    @patch("sagemaker_studio.sqlutils._ensure_project")
    @patch("sagemaker_studio.sqlutils._ensure_sql_executor")
    def test_mixed_persist_session_scenarios(
        self, mock_ensure_sql_executor, mock_ensure_project, mock_helper_factory
    ):
        """Test persist=True caches, persist=False on second call uses cache if exists"""

        mock_project = Mock()
        mock_connection = Mock()
        mock_connection.type = "REDSHIFT"
        mock_connection.id = "conn_123"
        mock_project.connection.return_value = mock_connection
        mock_ensure_project.return_value = mock_project

        mock_sql_helper = Mock()
        mock_sql_helper.to_sql_config.return_value = {"region_name": "us-east-1"}
        mock_helper_factory.get_sql_helper.return_value = mock_sql_helper

        mock_sql_executor = Mock()
        mock_ensure_sql_executor.return_value = mock_sql_executor
        mock_engine = Mock()
        mock_cached_connection = Mock()
        mock_cached_connection.closed = False
        mock_sql_executor.create_engine.return_value = mock_engine
        mock_sql_executor.get_supported_connection_types.return_value = ["REDSHIFT"]

        from sagemaker_studio.sql_engine.sql_executor import ExecutionResult

        execution_result = ExecutionResult(
            statement_index=0,
            statement="SELECT 1",
            statement_type="SELECT",
            result=DataFrame({"col1": [1]}),
            status="success",
        )
        mock_sql_executor.execute.return_value = iter([execution_result])

        # First call with persist=True caches connection
        managed_conn = ManagedConnection(
            engine=mock_engine,
            connection=mock_cached_connection,
            id="test-conn-id",
            cache_key="test_conn",
        )
        sqlutils._connection_cache.put("test_conn", managed_conn)
        list(sqlutils.sql_stream("SELECT 1", connection_name="test_conn", persist_session=True))

        # Verify cached connection was used
        call_args = mock_sql_executor.execute.call_args
        self.assertEqual(call_args[1]["connection"], mock_cached_connection)

        # Reset mock
        mock_sql_executor.execute.reset_mock()
        mock_sql_executor.execute.return_value = iter([execution_result])

        # Second call with persist=False creates new connection (conn=None)
        list(sqlutils.sql_stream("SELECT 2", connection_name="test_conn", persist_session=False))

        # Verify new connection was created (conn=None for non-persistent)
        call_args = mock_sql_executor.execute.call_args
        self.assertIsNone(call_args[1]["connection"])  # conn should be None for persist=False

    @patch("sagemaker_studio.sqlutils.HelperFactory")
    @patch("sagemaker_studio.sqlutils._ensure_project")
    @patch("sagemaker_studio.sqlutils._ensure_sql_executor")
    def test_persist_session_false_does_not_cache(
        self, mock_ensure_sql_executor, mock_ensure_project, mock_helper_factory
    ):
        """Test persist_session=False does not cache connection"""
        mock_project = Mock()
        mock_connection = Mock()
        mock_connection.type = "REDSHIFT"
        mock_connection.id = "conn_123"
        mock_project.connection.return_value = mock_connection
        mock_ensure_project.return_value = mock_project

        mock_sql_helper = Mock()
        mock_sql_helper.to_sql_config.return_value = {"region_name": "us-east-1"}
        mock_helper_factory.get_sql_helper.return_value = mock_sql_helper

        mock_sql_executor = Mock()
        mock_ensure_sql_executor.return_value = mock_sql_executor
        mock_engine = Mock()
        mock_db_connection = Mock()
        mock_engine.connect.return_value.__enter__ = Mock(return_value=mock_db_connection)
        mock_engine.connect.return_value.__exit__ = Mock(return_value=None)
        mock_sql_executor.create_engine.return_value = mock_engine
        mock_sql_executor.get_supported_connection_types.return_value = ["REDSHIFT"]

        from sagemaker_studio.sql_engine.sql_executor import ExecutionResult

        execution_result = ExecutionResult(
            statement_index=0,
            statement="SELECT 1",
            statement_type="SELECT",
            result=DataFrame({"col1": [1]}),
            status="success",
        )
        mock_sql_executor.execute.return_value = iter([execution_result])

        # Call with persist_session=False
        list(sqlutils.sql_stream("SELECT 1", connection_name="test_conn", persist_session=False))

        # Verify connection was not cached
        self.assertEqual(len(sqlutils._connection_cache), 0)

    def test_list_connections(self):
        """Test list_connections returns cached connection details"""

        mock_conn1 = Mock()
        mock_conn1.closed = False
        mock_conn2 = Mock()
        mock_conn2.closed = False

        mc1 = ManagedConnection(Mock(), mock_conn1, "id-1", "conn_1")
        mc2 = ManagedConnection(Mock(), mock_conn2, "id-2", "conn_2")

        sqlutils._connection_cache.put("conn_1", mc1)
        sqlutils._connection_cache.put("conn_2", mc2)

        connections = sqlutils.list_connections()
        self.assertEqual(len(connections), 2)
        self.assertIn("id", connections[0])
        self.assertIn("cache_key", connections[0])
        self.assertIn("created_at", connections[0])
        self.assertIn("last_used", connections[0])

    def test_close_connection(self):
        """Test close_connection closes and removes from cache by ID"""

        mock_connection = Mock()
        mock_connection.closed = False

        managed_conn = ManagedConnection(
            engine=Mock(), connection=mock_connection, id="uuid-123", cache_key="conn_1"
        )
        sqlutils._connection_cache.put("conn_1", managed_conn)

        sqlutils.close_connection(id="uuid-123")

        mock_connection.close.assert_called_once()
        self.assertIsNone(sqlutils._connection_cache.get("conn_1"))

    def test_close_connection_nonexistent(self):
        """Test close_connection with non-existent ID does nothing"""
        # Should not raise error
        result = sqlutils.close_connection(id="nonexistent-uuid")
        self.assertFalse(result)

    def test_close_all_connections(self):
        """Test close_all_connections closes all cached connections"""

        mock_conn1 = Mock()
        mock_conn1.closed = False
        mock_conn2 = Mock()
        mock_conn2.closed = False

        sqlutils._connection_cache.put(
            "conn_1", ManagedConnection(Mock(), mock_conn1, "id-1", "conn_1")
        )
        sqlutils._connection_cache.put(
            "conn_2", ManagedConnection(Mock(), mock_conn2, "id-2", "conn_2")
        )

        sqlutils.close_all_connections()

        mock_conn1.close.assert_called_once()
        mock_conn2.close.assert_called_once()
        self.assertEqual(len(sqlutils._connection_cache), 0)

    def test_close_connection_with_error(self):
        """Test close_connection handles connection.close() errors gracefully"""

        mock_connection = Mock()
        mock_connection.close.side_effect = Exception("Connection already closed")
        mock_connection.closed = False

        managed_conn = ManagedConnection(
            engine=Mock(), connection=mock_connection, id="uuid-123", cache_key="conn_1"
        )
        sqlutils._connection_cache.put("conn_1", managed_conn)

        # Should not raise, but should still remove from cache
        result = sqlutils.close_connection(id="uuid-123")

        self.assertTrue(result)
        self.assertIsNone(sqlutils._connection_cache.get("conn_1"))


class TestCacheKeyGeneration(unittest.TestCase):
    """Test cache key generation with kwargs"""

    def test_make_cache_key_no_kwargs(self):
        """Test cache key generation without kwargs"""
        key = sqlutils._make_cache_key("conn_123", None)
        self.assertEqual(key, "conn_123")

    def test_make_cache_key_with_connection_name(self):
        """Test cache key generation with connection_name"""
        key = sqlutils._make_cache_key(None, "my_connection")
        self.assertEqual(key, "my_connection")

    def test_make_cache_key_connection_id_takes_precedence(self):
        """Test connection_id takes precedence over connection_name"""
        key = sqlutils._make_cache_key("conn_123", "my_connection")
        self.assertEqual(key, "conn_123")

    def test_make_cache_key_default_when_no_identifiers(self):
        """Test default key when no identifiers provided"""
        key = sqlutils._make_cache_key(None, None)
        self.assertEqual(key, "default")

    def test_make_cache_key_with_catalog_name(self):
        """Test cache key includes catalog_name"""
        key = sqlutils._make_cache_key("conn_123", None, catalog_name="prod")
        self.assertEqual(key, "conn_123::catalog_name=prod")

    def test_make_cache_key_with_schema_name(self):
        """Test cache key includes schema_name"""
        key = sqlutils._make_cache_key("conn_123", None, schema_name="public")
        self.assertEqual(key, "conn_123::schema_name=public")

    def test_make_cache_key_with_database_name(self):
        """Test cache key includes database_name"""
        key = sqlutils._make_cache_key("conn_123", None, database_name="mydb")
        self.assertEqual(key, "conn_123::database_name=mydb")

    def test_make_cache_key_with_multiple_kwargs(self):
        """Test cache key with multiple kwargs are sorted"""
        key = sqlutils._make_cache_key(
            "conn_123", None, schema_name="public", catalog_name="prod", database_name="mydb"
        )
        # Should be sorted a|phabetically
        self.assertEqual(key, "conn_123::catalog_name=prod:database_name=mydb:schema_name=public")

    def test_make_cache_key_ignores_irrelevant_kwargs(self):
        """Test cache key ignores kwargs not in relevant_keys list"""
        key = sqlutils._make_cache_key(
            "conn_123", None, catalog_name="prod", some_other_param="value", another_param=123
        )
        self.assertEqual(key, "conn_123::catalog_name=prod")

    def test_make_cache_key_with_connection_name_and_kwargs(self):
        """Test cache key with connection_name and kwargs"""
        key = sqlutils._make_cache_key(
            None, "my_athena_conn", catalog_name="prod", schema_name="public"
        )
        self.assertEqual(key, "my_athena_conn::catalog_name=prod:schema_name=public")


class TestCacheKeyIntegration(unittest.TestCase):
    """Test cache key integration with sql execution"""

    def setUp(self):
        sqlutils._connection_cache.clear()

    def tearDown(self):
        sqlutils._connection_cache.clear()

    @patch("sagemaker_studio.sqlutils.HelperFactory")
    @patch("sagemaker_studio.sqlutils._ensure_project")
    @patch("sagemaker_studio.sqlutils._ensure_sql_executor")
    def test_different_kwargs_create_separate_cache_entries(
        self, mock_ensure_sql_executor, mock_ensure_project, mock_helper_factory
    ):
        """Test that different kwargs create separate cache entries"""
        mock_project = Mock()
        mock_connection = Mock()
        mock_connection.type = "REDSHIFT"
        mock_connection.id = "conn_123"
        mock_project.connection.return_value = mock_connection
        mock_ensure_project.return_value = mock_project

        mock_sql_helper = Mock()
        mock_sql_helper.to_sql_config.return_value = {"region_name": "us-east-1"}
        mock_helper_factory.get_sql_helper.return_value = mock_sql_helper

        mock_sql_executor = Mock()
        mock_ensure_sql_executor.return_value = mock_sql_executor
        mock_engine1 = Mock()
        mock_engine2 = Mock()
        mock_sql_executor.create_engine.side_effect = [mock_engine1, mock_engine2]
        mock_sql_executor.get_supported_connection_types.return_value = ["REDSHIFT"]

        from sagemaker_studio.sql_engine.sql_executor import ExecutionResult

        execution_result = ExecutionResult(
            statement_index=0,
            statement="SELECT 1",
            statement_type="SELECT",
            result=DataFrame({"col1": [1]}),
            status="success",
        )
        mock_sql_executor.execute.return_value = iter([execution_result])

        # First call with catalog_name="prod"
        list(
            sqlutils.sql_stream(
                "SELECT 1", connection_name="test_conn", persist_session=True, catalog_name="prod"
            )
        )

        # Second call with catalog_name="dev"
        mock_sql_executor.execute.return_value = iter([execution_result])
        list(
            sqlutils.sql_stream(
                "SELECT 1", connection_name="test_conn", persist_session=True, catalog_name="dev"
            )
        )

        # Verify two separate cache entries exist
        self.assertEqual(len(sqlutils._connection_cache), 2)
        self.assertTrue("test_conn::catalog_name=prod" in sqlutils._connection_cache)
        self.assertTrue("test_conn::catalog_name=dev" in sqlutils._connection_cache)

        # Verify two engines were created
        self.assertEqual(mock_sql_executor.create_engine.call_count, 2)

    @patch("sagemaker_studio.sqlutils.HelperFactory")
    @patch("sagemaker_studio.sqlutils._ensure_project")
    @patch("sagemaker_studio.sqlutils._ensure_sql_executor")
    def test_same_kwargs_reuse_cache(
        self, mock_ensure_sql_executor, mock_ensure_project, mock_helper_factory
    ):
        """Test that same connection with same kwargs reuses cached engine"""

        mock_project = Mock()
        mock_connection = Mock()
        mock_connection.type = "REDSHIFT"
        mock_connection.id = "conn_123"
        mock_project.connection.return_value = mock_connection
        mock_ensure_project.return_value = mock_project

        mock_sql_helper = Mock()
        mock_sql_helper.to_sql_config.return_value = {"region_name": "us-east-1"}
        mock_helper_factory.get_sql_helper.return_value = mock_sql_helper

        mock_sql_executor = Mock()
        mock_ensure_sql_executor.return_value = mock_sql_executor
        mock_engine = Mock()
        mock_db_connection = Mock()
        mock_db_connection.closed = False
        mock_sql_executor.create_engine.return_value = mock_engine
        mock_sql_executor.get_supported_connection_types.return_value = ["REDSHIFT"]

        from sagemaker_studio.sql_engine.sql_executor import ExecutionResult

        execution_result = ExecutionResult(
            statement_index=0,
            statement="SELECT 1",
            statement_type="SELECT",
            result=DataFrame({"col1": [1]}),
            status="success",
        )
        mock_sql_executor.execute.return_value = iter([execution_result])

        # Pre-populate cache with specific kwargs
        managed_conn = ManagedConnection(
            engine=mock_engine,
            connection=mock_db_connection,
            id="test-conn-id",
            cache_key="test_conn::catalog_name=prod:schema_name=public",
        )
        sqlutils._connection_cache.put(
            "test_conn::catalog_name=prod:schema_name=public", managed_conn
        )

        # Call with same kwargs
        list(
            sqlutils.sql_stream(
                "SELECT 1",
                connection_name="test_conn",
                persist_session=True,
                catalog_name="prod",
                schema_name="public",
            )
        )

        # Verify engine was not created again
        mock_sql_executor.create_engine.assert_not_called()
        # Verify cached connection was used
        call_args = mock_sql_executor.execute.call_args
        self.assertEqual(call_args[1]["connection"], mock_db_connection)

    @patch("sagemaker_studio.sqlutils.HelperFactory")
    @patch("sagemaker_studio.sqlutils._ensure_project")
    @patch("sagemaker_studio.sqlutils._ensure_sql_executor")
    def test_no_kwargs_and_with_kwargs_separate_cache(
        self, mock_ensure_sql_executor, mock_ensure_project, mock_helper_factory
    ):
        """Test that connection without kwargs and with kwargs have separate cache entries"""
        mock_project = Mock()
        mock_connection = Mock()
        mock_connection.type = "REDSHIFT"
        mock_connection.id = "conn_123"
        mock_project.connection.return_value = mock_connection
        mock_ensure_project.return_value = mock_project

        mock_sql_helper = Mock()
        mock_sql_helper.to_sql_config.return_value = {"region_name": "us-east-1"}
        mock_helper_factory.get_sql_helper.return_value = mock_sql_helper

        mock_sql_executor = Mock()
        mock_ensure_sql_executor.return_value = mock_sql_executor
        mock_engine1 = Mock()
        mock_engine2 = Mock()
        mock_sql_executor.create_engine.side_effect = [mock_engine1, mock_engine2]
        mock_sql_executor.get_supported_connection_types.return_value = ["REDSHIFT"]

        from sagemaker_studio.sql_engine.sql_executor import ExecutionResult

        execution_result = ExecutionResult(
            statement_index=0,
            statement="SELECT 1",
            statement_type="SELECT",
            result=DataFrame({"col1": [1]}),
            status="success",
        )
        mock_sql_executor.execute.return_value = iter([execution_result])

        # First call without kwargs
        list(sqlutils.sql_stream("SELECT 1", connection_name="test_conn", persist_session=True))

        # Second call with kwargs
        mock_sql_executor.execute.return_value = iter([execution_result])
        list(
            sqlutils.sql_stream(
                "SELECT 1", connection_name="test_conn", persist_session=True, catalog_name="prod"
            )
        )

        # Verify two separate cache entries
        self.assertEqual(len(sqlutils._connection_cache), 2)
        self.assertTrue("test_conn" in sqlutils._connection_cache)
        self.assertTrue("test_conn::catalog_name=prod" in sqlutils._connection_cache)

        # Verify two engines were created
        self.assertEqual(mock_sql_executor.create_engine.call_count, 2)


class TestIRCGlueConnectionPaths(unittest.TestCase):
    """Tests for IRC/Glue connection (WORKDAYICEBERGRESTCATALOG) paths."""

    def setUp(self):
        sqlutils._project = None
        sqlutils._connection_cache.clear()

    def tearDown(self):
        sqlutils._connection_cache.clear()

    @patch("sagemaker_studio.sqlutils._ensure_glue_spark")
    @patch("sagemaker_studio.sqlutils._ensure_project")
    def test_sql_irc_glue_success(self, mock_ensure_project, mock_ensure_glue_spark):
        mock_project = Mock()
        mock_conn = Mock()
        mock_conn.type = "WORKDAYICEBERGRESTCATALOG"
        mock_project.connection.return_value = mock_conn
        mock_ensure_project.return_value = mock_project

        mock_spark = Mock()
        mock_df = Mock()
        mock_df.limit.return_value.collect.return_value = [Mock()]
        mock_spark.sql.return_value = mock_df
        mock_ensure_glue_spark.return_value = mock_spark

        result = sqlutils.sql("SELECT 1", connection_name="irc_conn")
        self.assertEqual(result, mock_df)

    @patch("sagemaker_studio.sqlutils._ensure_glue_spark")
    @patch("sagemaker_studio.sqlutils._ensure_project")
    def test_sql_irc_glue_token_refresh_on_not_authorized(
        self, mock_ensure_project, mock_ensure_glue_spark
    ):
        mock_project = Mock()
        mock_conn = Mock()
        mock_conn.type = "WORKDAYICEBERGRESTCATALOG"
        mock_conn._spark_catalog_configs.return_value = {
            "SOURCE_CATALOG_LIST": '["catalog1", "catalog2"]',
            "ACCESS_TOKEN": "new_token",
        }
        mock_project.connection.return_value = mock_conn
        mock_ensure_project.return_value = mock_project

        mock_spark = Mock()
        mock_df_fail = Mock()
        type(mock_df_fail).schema = PropertyMock(
            side_effect=Exception(
                "org.apache.iceberg.exceptions.NotAuthorizedException: token expired"
            )
        )
        mock_df_success = Mock()
        mock_spark.sql.side_effect = [mock_df_fail, mock_df_success]
        mock_ensure_glue_spark.return_value = mock_spark

        result = sqlutils.sql("SELECT 1", connection_name="irc_conn")
        self.assertEqual(result, mock_df_success)
        # The stored token was rejected, so the retry must force a refresh rather
        # than re-reading the same token from the connection's secret.
        mock_conn._spark_catalog_configs.assert_called_once_with(force_token_refresh=True)
        mock_spark.conf.set.assert_any_call("spark.sql.catalog.catalog1.token", "new_token")
        mock_spark.conf.set.assert_any_call("spark.sql.catalog.catalog2.token", "new_token")

    @patch("sagemaker_studio.sqlutils._ensure_glue_spark")
    @patch("sagemaker_studio.sqlutils._ensure_project")
    def test_sql_irc_glue_refresh_returning_none_reraises(
        self, mock_ensure_project, mock_ensure_glue_spark
    ):
        """If the forced refresh yields no configs, the original auth error surfaces."""
        mock_project = Mock()
        mock_conn = Mock()
        mock_conn.type = "DATABRICKSICEBERGRESTCATALOG"
        mock_conn._spark_catalog_configs.return_value = None
        mock_project.connection.return_value = mock_conn
        mock_ensure_project.return_value = mock_project

        mock_spark = Mock()
        mock_df_fail = Mock()
        type(mock_df_fail).schema = PropertyMock(
            side_effect=Exception(
                "org.apache.iceberg.exceptions.NotAuthorizedException: token expired"
            )
        )
        mock_spark.sql.return_value = mock_df_fail
        mock_ensure_glue_spark.return_value = mock_spark

        with self.assertRaises(Exception) as cm:
            sqlutils.sql("SELECT 1", connection_name="irc_conn")
        self.assertIn("NotAuthorizedException", str(cm.exception))
        mock_conn._spark_catalog_configs.assert_called_once_with(force_token_refresh=True)

    @patch("sagemaker_studio.sqlutils._ensure_glue_spark")
    @patch("sagemaker_studio.sqlutils._ensure_project")
    def test_sql_irc_glue_non_auth_error_raises(self, mock_ensure_project, mock_ensure_glue_spark):
        mock_project = Mock()
        mock_conn = Mock()
        mock_conn.type = "WORKDAYICEBERGRESTCATALOG"
        mock_project.connection.return_value = mock_conn
        mock_ensure_project.return_value = mock_project

        mock_spark = Mock()
        mock_df = Mock()
        type(mock_df).schema = PropertyMock(side_effect=Exception("some other error"))
        mock_spark.sql.return_value = mock_df
        mock_ensure_glue_spark.return_value = mock_spark

        with self.assertRaises(Exception) as cm:
            sqlutils.sql("SELECT 1", connection_name="irc_conn")
        self.assertIn("some other error", str(cm.exception))

    @patch("sagemaker_studio.sqlutils._ensure_glue_spark")
    @patch("sagemaker_studio.sqlutils._ensure_project")
    def test_sql_stream_irc_glue_success(self, mock_ensure_project, mock_ensure_glue_spark):
        mock_project = Mock()
        mock_conn = Mock()
        mock_conn.type = "WORKDAYICEBERGRESTCATALOG"
        mock_project.connection.return_value = mock_conn
        mock_ensure_project.return_value = mock_project

        mock_spark = Mock()
        mock_df = Mock()
        mock_df.limit.return_value.collect.return_value = [Mock()]
        mock_spark.sql.return_value = mock_df
        mock_ensure_glue_spark.return_value = mock_spark

        results = list(sqlutils.sql_stream("SELECT 1", connection_name="irc_conn"))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].status, "success")
        self.assertEqual(results[0].result, mock_df)

    @patch("sagemaker_studio.sqlutils._ensure_glue_spark")
    @patch("sagemaker_studio.sqlutils._ensure_project")
    def test_sql_stream_irc_glue_token_refresh(self, mock_ensure_project, mock_ensure_glue_spark):
        mock_project = Mock()
        mock_conn = Mock()
        mock_conn.type = "WORKDAYICEBERGRESTCATALOG"
        mock_conn._spark_catalog_configs.return_value = {
            "SOURCE_CATALOG_LIST": '["cat1"]',
            "ACCESS_TOKEN": "refreshed_token",
        }
        mock_project.connection.return_value = mock_conn
        mock_ensure_project.return_value = mock_project

        mock_spark = Mock()
        mock_df_fail = Mock()
        type(mock_df_fail).schema = PropertyMock(
            side_effect=Exception("org.apache.iceberg.exceptions.NotAuthorizedException: expired")
        )
        mock_df_success = Mock()
        mock_spark.sql.side_effect = [mock_df_fail, mock_df_success]
        mock_ensure_glue_spark.return_value = mock_spark

        results = list(sqlutils.sql_stream("SELECT 1", connection_name="irc_conn"))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].result, mock_df_success)
        mock_spark.conf.set.assert_called_with("spark.sql.catalog.cat1.token", "refreshed_token")


class _FakeLazySparkSession:
    """Stand-in for LazySparkSession: session manager lives in the instance __dict__."""

    def __init__(self, session_manager=None, connection_name=None, config=None, spark_conf=None):
        self._spark = None
        self._session_manager = session_manager
        self._connection_name = connection_name
        self._config = config
        self._spark_conf = spark_conf


class TestEnsureGlueSpark(unittest.TestCase):
    """Tests for _ensure_glue_spark and its Glue-backend resolution helpers."""

    def setUp(self):
        sqlutils._project = None
        sqlutils._glue_spark = None

    def tearDown(self):
        sqlutils._glue_spark = None

    @staticmethod
    def _named_mock(class_name):
        """Mock whose type name matches class_name (checked via type(x).__name__)."""
        return type(class_name, (), {})()

    @patch("sagemaker_studio.sqlutils._get_kernel_spark")
    def test_kernel_spark_reused_when_glue_backed(self, mock_kernel_spark):
        """A kernel spark already backed by a Glue session manager is reused as-is."""
        manager = self._named_mock("GlueSparkSessionManager")
        kernel_spark = _FakeLazySparkSession(session_manager=manager)
        mock_kernel_spark.return_value = kernel_spark

        result = sqlutils._ensure_glue_spark()

        self.assertIs(result, kernel_spark)
        self.assertIsNone(sqlutils._glue_spark)

    @patch("sagemaker_studio.sqlutils._create_glue_spark")
    @patch("sagemaker_studio.sqlutils._get_kernel_spark")
    def test_non_glue_kernel_spark_triggers_dedicated_session(self, mock_kernel_spark, mock_create):
        """A kernel spark backed by a non-Glue manager is not used; a Glue session is created."""
        manager = self._named_mock("AthenaSparkSessionManager")
        mock_kernel_spark.return_value = _FakeLazySparkSession(session_manager=manager)
        glue_spark = Mock()
        mock_create.return_value = glue_spark

        result = sqlutils._ensure_glue_spark()

        self.assertIs(result, glue_spark)
        mock_create.assert_called_once()

    @patch("sagemaker_studio.sqlutils._create_glue_spark")
    @patch("sagemaker_studio.sqlutils._get_kernel_spark")
    def test_missing_kernel_spark_triggers_dedicated_session(self, mock_kernel_spark, mock_create):
        """No spark in the kernel namespace: a dedicated Glue session is created."""
        mock_kernel_spark.return_value = None
        glue_spark = Mock()
        mock_create.return_value = glue_spark

        result = sqlutils._ensure_glue_spark()

        self.assertIs(result, glue_spark)

    @patch("sagemaker_studio.sqlutils._create_glue_spark")
    @patch("sagemaker_studio.sqlutils._get_kernel_spark")
    def test_dedicated_glue_session_is_cached(self, mock_kernel_spark, mock_create):
        """The dedicated Glue session is created once and reused across calls."""
        mock_kernel_spark.return_value = None
        mock_create.return_value = Mock()

        first = sqlutils._ensure_glue_spark()
        second = sqlutils._ensure_glue_spark()

        self.assertIs(first, second)
        mock_create.assert_called_once()

    def test_unresolved_lazy_session_resolves_manager_without_starting_session(self):
        """A lazy kernel spark with no manager yet gets its manager resolved (not a session)."""
        kernel_spark = _FakeLazySparkSession(connection_name="my_glue_conn")
        manager = self._named_mock("GlueSparkSessionManager")

        with patch(
            "sagemaker_studio.utils.spark.connection_resolver._resolve_connection_and_create_session_manager",
            return_value=manager,
        ) as mock_resolve:
            self.assertTrue(sqlutils._spark_session_is_glue(kernel_spark))

        mock_resolve.assert_called_once_with(
            connection_name="my_glue_conn", config=None, spark_conf=None
        )
        # Manager is assigned back so the lazy session does not resolve twice.
        self.assertIs(kernel_spark._session_manager, manager)

    def test_resolution_failure_treated_as_non_glue(self):
        """If backend resolution fails, the kernel spark is treated as non-Glue."""
        kernel_spark = _FakeLazySparkSession()

        with patch(
            "sagemaker_studio.utils.spark.connection_resolver._resolve_connection_and_create_session_manager",
            side_effect=RuntimeError("no notebook metadata"),
        ):
            self.assertFalse(sqlutils._spark_session_is_glue(kernel_spark))

    def test_plain_spark_session_treated_as_non_glue(self):
        """An object without a session manager (plain SparkSession) cannot be identified."""
        self.assertFalse(sqlutils._spark_session_is_glue(object()))

    @patch("sagemaker_studio.sqlutils._ensure_project")
    def test_create_glue_spark_uses_project_glue_connection(self, mock_ensure_project):
        """_create_glue_spark finds the project's Glue compute connection and wraps it."""
        athena_conn = Mock()
        athena_conn.type = "SPARK_CONNECT"
        glue_conn = Mock()
        glue_conn.type = "SPARK"
        glue_conn.name = "project.spark.compatibility"
        redshift_conn = Mock()
        redshift_conn.type = "REDSHIFT"

        mock_project = Mock()
        mock_project.connections = [redshift_conn, athena_conn, glue_conn]
        mock_ensure_project.return_value = mock_project

        def identify(conn):
            return "GLUE" if conn is glue_conn else "ATHENA"

        mock_manager = Mock()
        with patch(
            "sagemaker_studio.utils.spark.connection_resolver._identify_service_from_props",
            side_effect=identify,
        ), patch(
            "sagemaker_studio.utils.spark.session.glue.glue_spark_session_manager.GlueSparkSessionManager",
            return_value=mock_manager,
        ) as mock_manager_cls, patch(
            "sagemaker_studio.utils.spark.session.lazy_spark_session.LazySparkSession"
        ) as mock_lazy_cls:
            sqlutils._create_glue_spark()

        mock_manager_cls.assert_called_once_with(
            connection=glue_conn, connection_name="project.spark.compatibility", spark_conf=None
        )
        mock_lazy_cls.assert_called_once_with(session_manager=mock_manager)

    @patch("sagemaker_studio.sqlutils._create_glue_spark")
    @patch("sagemaker_studio.sqlutils._get_kernel_spark")
    def test_kernel_config_and_spark_conf_carried_to_dedicated_session(
        self, mock_kernel_spark, mock_create
    ):
        """The kernel lazy session's ClientConfig/spark_conf are passed to the Glue session."""
        config = Mock()
        spark_conf = {"spark.some.key": "value"}
        manager = self._named_mock("AthenaSparkSessionManager")
        mock_kernel_spark.return_value = _FakeLazySparkSession(
            session_manager=manager, config=config, spark_conf=spark_conf
        )
        mock_create.return_value = Mock()

        sqlutils._ensure_glue_spark()

        mock_create.assert_called_once_with(config=config, spark_conf=spark_conf)

    @patch("sagemaker_studio.sqlutils._spark_session_is_glue")
    @patch("sagemaker_studio.sqlutils._get_kernel_spark")
    def test_cached_dedicated_session_skips_kernel_backend_probe(
        self, mock_kernel_spark, mock_is_glue
    ):
        """Once the dedicated session exists, the kernel backend is not re-probed.

        The backend probe can perform connection-resolution network calls, so it must
        not run on every query after the dedicated session has been created.
        """
        cached = Mock()
        sqlutils._glue_spark = cached

        result = sqlutils._ensure_glue_spark()

        self.assertIs(result, cached)
        mock_kernel_spark.assert_not_called()
        mock_is_glue.assert_not_called()

    @patch("atexit.register")
    @patch("sagemaker_studio.sqlutils._create_glue_spark")
    @patch("sagemaker_studio.sqlutils._get_kernel_spark")
    def test_dedicated_session_registers_atexit_stop(
        self, mock_kernel_spark, mock_create, mock_atexit_register
    ):
        """Creating the dedicated session registers the shutdown stop hook."""
        mock_kernel_spark.return_value = None
        mock_create.return_value = Mock()

        sqlutils._ensure_glue_spark()

        mock_atexit_register.assert_called_once_with(sqlutils._stop_glue_spark)

    def test_stop_glue_spark_stops_and_clears(self):
        """_stop_glue_spark stops the session and clears the cache."""
        glue_spark = Mock()
        sqlutils._glue_spark = glue_spark

        sqlutils._stop_glue_spark()

        glue_spark.stop.assert_called_once()
        self.assertIsNone(sqlutils._glue_spark)

    def test_stop_glue_spark_noop_without_session(self):
        """_stop_glue_spark is a no-op when no dedicated session exists."""
        sqlutils._stop_glue_spark()
        self.assertIsNone(sqlutils._glue_spark)

    def test_stop_glue_spark_swallows_stop_errors(self):
        """A failing stop() still clears the cache and does not raise."""
        glue_spark = Mock()
        glue_spark.stop.side_effect = RuntimeError("session already gone")
        sqlutils._glue_spark = glue_spark

        sqlutils._stop_glue_spark()

        self.assertIsNone(sqlutils._glue_spark)

    def test_close_all_connections_stops_glue_spark(self):
        """close_all_connections also stops the dedicated Glue session."""
        glue_spark = Mock()
        sqlutils._glue_spark = glue_spark

        sqlutils.close_all_connections()

        glue_spark.stop.assert_called_once()
        self.assertIsNone(sqlutils._glue_spark)

    @patch("sagemaker_studio.sqlutils._ensure_project")
    def test_create_glue_spark_no_glue_connection_raises(self, mock_ensure_project):
        """A project without a Glue compute connection gets an actionable error."""
        athena_conn = Mock()
        athena_conn.type = "SPARK_CONNECT"
        mock_project = Mock()
        mock_project.connections = [athena_conn]
        mock_ensure_project.return_value = mock_project

        with patch(
            "sagemaker_studio.utils.spark.connection_resolver._identify_service_from_props",
            return_value="ATHENA",
        ):
            with self.assertRaises(RuntimeError) as ctx:
                sqlutils._create_glue_spark()

        self.assertIn("Glue compute connection", str(ctx.exception))

    @patch("sagemaker_studio.sqlutils._ensure_project")
    def test_create_glue_spark_project_not_initialized_raises(self, mock_ensure_project):
        """A missing project is reported clearly."""
        mock_ensure_project.return_value = False

        with self.assertRaises(RuntimeError) as ctx:
            sqlutils._create_glue_spark()

        self.assertIn("Project is not initialized", str(ctx.exception))

    def test_get_kernel_spark_returns_spark_from_namespace(self):
        """_get_kernel_spark reads the spark object from the IPython user namespace."""
        kernel_spark = Mock()
        mock_ipython = Mock()
        mock_ipython.user_ns = {"spark": kernel_spark}
        mock_module = Mock()
        mock_module.get_ipython = Mock(return_value=mock_ipython)

        with patch.dict("sys.modules", {"IPython": mock_module}):
            self.assertIs(sqlutils._get_kernel_spark(), kernel_spark)

    def test_get_kernel_spark_no_ipython_kernel_returns_none(self):
        """No running IPython kernel (get_ipython() is None) yields None."""
        mock_module = Mock()
        mock_module.get_ipython = Mock(return_value=None)

        with patch.dict("sys.modules", {"IPython": mock_module}):
            self.assertIsNone(sqlutils._get_kernel_spark())

    def test_get_kernel_spark_ipython_not_installed_returns_none(self):
        """IPython not importable yields None instead of raising."""
        with patch.dict("sys.modules", {"IPython": None}):
            self.assertIsNone(sqlutils._get_kernel_spark())

    def test_create_glue_spark_pyspark_unavailable_raises(self):
        """Missing Spark session modules surface as an actionable RuntimeError."""
        with patch.dict("sys.modules", {"sagemaker_studio.utils.spark.connection_resolver": None}):
            with self.assertRaises(RuntimeError) as ctx:
                sqlutils._create_glue_spark()

        self.assertIn("PySpark is not available", str(ctx.exception))

    @patch("sagemaker_studio.sqlutils._ensure_project")
    def test_create_glue_spark_passes_client_config_to_manager(self, mock_ensure_project):
        """A carried-over ClientConfig is forwarded to GlueSparkSessionManager."""
        glue_conn = Mock()
        glue_conn.type = "SPARK"
        glue_conn.name = "project.spark.compatibility"
        mock_project = Mock()
        mock_project.connections = [glue_conn]
        mock_ensure_project.return_value = mock_project
        config = Mock()

        with patch(
            "sagemaker_studio.utils.spark.connection_resolver._identify_service_from_props",
            return_value="GLUE",
        ), patch(
            "sagemaker_studio.utils.spark.session.glue.glue_spark_session_manager.GlueSparkSessionManager",
        ) as mock_manager_cls, patch(
            "sagemaker_studio.utils.spark.session.lazy_spark_session.LazySparkSession"
        ):
            sqlutils._create_glue_spark(config=config)

        mock_manager_cls.assert_called_once_with(
            connection=glue_conn,
            connection_name="project.spark.compatibility",
            spark_conf=None,
            config=config,
        )


class TestGetEngineFromConnection(unittest.TestCase):
    """Tests for _get_engine_from_connection."""

    def test_none_conn_returns_none(self):
        self.assertIsNone(sqlutils._get_engine_from_connection(None))

    @patch("sagemaker_studio.sqlutils._ensure_sql_executor")
    def test_unsupported_type_raises(self, mock_ensure_sql_executor):
        mock_executor = Mock()
        mock_executor.get_supported_connection_types.return_value = ["ATHENA", "REDSHIFT"]
        mock_ensure_sql_executor.return_value = mock_executor

        mock_conn = Mock()
        mock_conn.type = "UNSUPPORTED_TYPE"

        with self.assertRaises(RuntimeError) as cm:
            sqlutils._get_engine_from_connection(mock_conn)
        self.assertIn(
            "SQL is not supported for connection type UNSUPPORTED_TYPE", str(cm.exception)
        )
        self.assertIn("ATHENA", str(cm.exception))


class TestCredentialRefresh(unittest.TestCase):
    """Tests for credential refresh functionality."""

    def test_create_credential_provider_formats_credentials(self):
        """Test _create_credential_provider formats credentials correctly"""
        mock_creds = Mock()
        mock_creds.access_key_id = "test_key"
        mock_creds.secret_access_key = "test_secret"
        mock_creds.session_token = "test_token"
        mock_creds.expiration = datetime(2025, 12, 31, 23, 59, 59, tzinfo=tzlocal())

        def credential_getter():
            return mock_creds

        provider = sqlutils._create_credential_provider(credential_getter)

        result = provider()

        self.assertEqual(result["access_key_id"], "test_key")
        self.assertEqual(result["secret_access_key"], "test_secret")
        self.assertEqual(result["session_token"], "test_token")
        self.assertIn("expiration", result)

    def test_create_credential_provider_defaults_expiration(self):
        """Test _create_credential_provider sets default expiration when None"""
        mock_creds = Mock()
        mock_creds.access_key_id = "test_key"
        mock_creds.secret_access_key = "test_secret"
        mock_creds.session_token = "test_token"
        mock_creds.expiration = None

        def credential_getter():
            return mock_creds

        provider = sqlutils._create_credential_provider(credential_getter)

        result = provider()

        self.assertIn("expiration", result)
        # Verify expiration is set to ~15 minutes from now
        from datetime import datetime, timezone

        expiry = datetime.fromisoformat(result["expiration"])
        now = datetime.now(timezone.utc)
        delta = (expiry - now).total_seconds()
        self.assertGreater(delta, 14 * 60)  # At least 14 minutes
        self.assertLess(delta, 16 * 60)  # At most 16 minutes

    @patch("sagemaker_studio.sqlutils.HelperFactory")
    @patch("sagemaker_studio.sqlutils._ensure_project")
    @patch("sagemaker_studio.sqlutils._ensure_sql_executor")
    def test_get_engine_from_connection_with_identifiers_refreshes_credentials(
        self, mock_ensure_sql_executor, mock_ensure_project, mock_helper_factory
    ):
        """Test _get_engine_from_connection with identifiers creates refreshing credential provider"""
        mock_project = Mock()

        # Create two different credential objects to simulate refresh
        mock_creds_1 = Mock()
        mock_creds_1.access_key_id = "old_key"
        mock_creds_1.secret_access_key = "old_secret"
        mock_creds_1.session_token = "old_token"
        mock_creds_1.expiration = None

        mock_creds_2 = Mock()
        mock_creds_2.access_key_id = "new_key"
        mock_creds_2.secret_access_key = "new_secret"
        mock_creds_2.session_token = "new_token"
        mock_creds_2.expiration = None

        mock_conn_1 = Mock()
        mock_conn_1.type = "REDSHIFT"
        mock_conn_1.connection_creds = mock_creds_1

        mock_conn_2 = Mock()
        mock_conn_2.type = "REDSHIFT"
        mock_conn_2.connection_creds = mock_creds_2

        # First call returns old creds, second call returns new creds
        mock_project.connection.side_effect = [mock_conn_1, mock_conn_2]
        mock_ensure_project.return_value = mock_project

        mock_sql_helper = Mock()
        mock_sql_helper.to_sql_config.return_value = {"host": "localhost"}
        mock_helper_factory.get_sql_helper.return_value = mock_sql_helper

        mock_sql_executor = Mock()
        mock_ensure_sql_executor.return_value = mock_sql_executor
        mock_engine = Mock()
        mock_sql_executor.create_engine.return_value = mock_engine
        mock_sql_executor.get_supported_connection_types.return_value = ["REDSHIFT"]

        # Call _get_engine_from_connection with connection_name
        sqlutils._get_engine_from_connection(mock_conn_1, connection_name="test_conn")

        # Get the credential_provider that was passed
        call_args = mock_sql_helper.to_sql_config.call_args
        credential_provider = call_args[1]["credential_provider"]

        # First call should return old credentials
        creds_1 = credential_provider()
        self.assertEqual(creds_1["access_key_id"], "old_key")

        # Second call should fetch fresh connection and return new credentials
        creds_2 = credential_provider()
        self.assertEqual(creds_2["access_key_id"], "new_key")

        # Verify connection was fetched twice (once for each credential_provider call)
        self.assertEqual(mock_project.connection.call_count, 2)

    @patch("sagemaker_studio.sqlutils.HelperFactory")
    @patch("sagemaker_studio.sqlutils._ensure_sql_executor")
    def test_get_engine_from_connection_without_identifiers_uses_cached_credentials(
        self, mock_ensure_sql_executor, mock_helper_factory
    ):
        """Test _get_engine_from_connection without identifiers uses cached credentials"""
        mock_creds = Mock()
        mock_creds.access_key_id = "cached_key"
        mock_creds.secret_access_key = "cached_secret"
        mock_creds.session_token = "cached_token"
        mock_creds.expiration = None

        mock_conn = Mock()
        mock_conn.type = "REDSHIFT"
        mock_conn.connection_creds = mock_creds

        mock_sql_helper = Mock()
        mock_sql_helper.to_sql_config.return_value = {"host": "localhost"}
        mock_helper_factory.get_sql_helper.return_value = mock_sql_helper

        mock_sql_executor = Mock()
        mock_ensure_sql_executor.return_value = mock_sql_executor
        mock_engine = Mock()
        mock_sql_executor.create_engine.return_value = mock_engine
        mock_sql_executor.get_supported_connection_types.return_value = ["REDSHIFT"]

        # Call without connection identifiers
        sqlutils._get_engine_from_connection(mock_conn)

        # Get the credential_provider that was passed
        call_args = mock_sql_helper.to_sql_config.call_args
        credential_provider = call_args[1]["credential_provider"]

        # Multiple calls should return same cached credentials
        creds_1 = credential_provider()
        creds_2 = credential_provider()

        self.assertEqual(creds_1["access_key_id"], "cached_key")
        self.assertEqual(creds_2["access_key_id"], "cached_key")

    @patch("sagemaker_studio.sqlutils.HelperFactory")
    @patch("sagemaker_studio.sqlutils._ensure_sql_executor")
    @patch("sagemaker_studio.sqlutils._ensure_project")
    def test_get_engine_returns_sqlalchemy_engine(
        self, mock_ensure_project, mock_ensure_sql_executor, mock_helper_factory
    ):
        mock_project = Mock()
        mock_conn = Mock(type="ATHENA")
        mock_conn.connection_creds.expiration = None
        mock_project.connection.return_value = mock_conn
        mock_ensure_project.return_value = mock_project
        mock_ensure_sql_executor.return_value.get_supported_connection_types.return_value = [
            "ATHENA"
        ]
        mock_ensure_sql_executor.return_value.create_engine.return_value = "sqlalchemy-engine"
        mock_helper_factory.get_sql_helper.return_value.to_sql_config.return_value = {
            "work_group": "wg",
            "region": "us-west-2",
        }

        result = sqlutils.get_engine(connection_name="test_conn")

        self.assertEqual(result, "sqlalchemy-engine")
        mock_project.connection.assert_called_with("test_conn")
        mock_ensure_sql_executor.return_value.create_engine.assert_called_once_with(
            "ATHENA", {"work_group": "wg", "region": "us-west-2"}
        )


class TestStreamAndCaptureMetadata(unittest.TestCase):
    """Tests for _stream_and_capture_metadata generator wrapper."""

    def setUp(self):
        sqlutils._last_sql_execution_metadata = None

    def test_captures_metadata_incrementally(self):
        """Metadata is available even before generator is fully consumed."""
        from sagemaker_studio.sql_engine.sql_executor import ExecutionResult

        results = [
            ExecutionResult(
                statement_index=0,
                statement="SELECT 1",
                statement_type="SELECT",
                result=DataFrame({"a": [1]}),
                status="success",
                execution_metadata={"statement_id": "s1"},
            ),
            ExecutionResult(
                statement_index=1,
                statement="SELECT 2",
                statement_type="SELECT",
                result=DataFrame({"b": [2]}),
                status="success",
                execution_metadata={"statement_id": "s2"},
            ),
        ]

        gen = sqlutils._stream_and_capture_metadata(iter(results))

        # After first yield, metadata has one entry
        first = next(gen)
        self.assertEqual(first.statement, "SELECT 1")
        self.assertEqual(len(sqlutils._last_sql_execution_metadata), 1)

        # After second yield, metadata has two entries
        second = next(gen)
        self.assertEqual(second.statement, "SELECT 2")
        self.assertEqual(len(sqlutils._last_sql_execution_metadata), 2)

        # Verify content
        self.assertEqual(sqlutils._last_sql_execution_metadata[0]["statement_index"], 0)
        self.assertEqual(
            sqlutils._last_sql_execution_metadata[0]["execution_metadata"]["statement_id"], "s1"
        )
        self.assertEqual(sqlutils._last_sql_execution_metadata[1]["statement_index"], 1)

    def test_captures_error_status(self):
        from sagemaker_studio.sql_engine.sql_executor import ExecutionResult

        results = [
            ExecutionResult(
                statement_index=0,
                statement="BAD SQL",
                statement_type="SELECT",
                error="syntax error",
                status="error",
            ),
        ]

        gen = sqlutils._stream_and_capture_metadata(iter(results))
        next(gen)

        self.assertEqual(len(sqlutils._last_sql_execution_metadata), 1)
        self.assertEqual(sqlutils._last_sql_execution_metadata[0]["status"], "error")
        self.assertEqual(sqlutils._last_sql_execution_metadata[0]["error"], "syntax error")

    def test_empty_stream_produces_empty_list(self):
        gen = sqlutils._stream_and_capture_metadata(iter([]))
        collected = list(gen)

        self.assertEqual(collected, [])
        self.assertEqual(sqlutils._last_sql_execution_metadata, [])

    def test_metadata_available_after_partial_consumption(self):
        """If consumer stops mid-stream (e.g., error raised), metadata is still populated."""
        from sagemaker_studio.sql_engine.sql_executor import ExecutionResult

        results = [
            ExecutionResult(
                statement_index=0,
                statement="SELECT 1",
                statement_type="SELECT",
                result=DataFrame(),
                status="success",
                execution_metadata=None,
            ),
            ExecutionResult(
                statement_index=1,
                statement="SELECT 2",
                statement_type="SELECT",
                result=DataFrame(),
                status="success",
                execution_metadata=None,
            ),
        ]

        gen = sqlutils._stream_and_capture_metadata(iter(results))
        next(gen)  # consume only first

        # Metadata has one entry even though generator isn't exhausted
        self.assertEqual(len(sqlutils._last_sql_execution_metadata), 1)

    def test_yields_results_unchanged(self):
        from sagemaker_studio.sql_engine.sql_executor import ExecutionResult

        original = ExecutionResult(
            statement_index=0,
            statement="SELECT 1",
            statement_type="SELECT",
            result="my_result",
            status="success",
        )

        gen = sqlutils._stream_and_capture_metadata(iter([original]))
        yielded = next(gen)

        self.assertIs(yielded, original)

    def test_includes_connection_id_and_type(self):
        """connection_id and connection_type are added to each entry when provided."""
        from sagemaker_studio.sql_engine.sql_executor import ExecutionResult

        results = [
            ExecutionResult(
                statement_index=0,
                statement="SELECT 1",
                statement_type="SELECT",
                result=DataFrame({"a": [1]}),
                status="success",
            ),
            ExecutionResult(
                statement_index=1,
                statement="SELECT 2",
                statement_type="SELECT",
                result=DataFrame({"b": [2]}),
                status="success",
            ),
        ]

        gen = sqlutils._stream_and_capture_metadata(
            iter(results), connection_id="conn-abc", connection_type="REDSHIFT"
        )
        list(gen)  # exhaust

        self.assertEqual(len(sqlutils._last_sql_execution_metadata), 2)
        self.assertEqual(sqlutils._last_sql_execution_metadata[0]["connection_id"], "conn-abc")
        self.assertEqual(sqlutils._last_sql_execution_metadata[0]["connection_type"], "REDSHIFT")
        self.assertEqual(sqlutils._last_sql_execution_metadata[1]["connection_id"], "conn-abc")
        self.assertEqual(sqlutils._last_sql_execution_metadata[1]["connection_type"], "REDSHIFT")

    def test_omits_connection_fields_when_none(self):
        """When connection_id/connection_type are None, they are not in the entry."""
        from sagemaker_studio.sql_engine.sql_executor import ExecutionResult

        results = [
            ExecutionResult(
                statement_index=0,
                statement="SELECT 1",
                statement_type="SELECT",
                result=DataFrame(),
                status="success",
            ),
        ]

        gen = sqlutils._stream_and_capture_metadata(iter(results))
        list(gen)

        entry = sqlutils._last_sql_execution_metadata[0]
        self.assertNotIn("connection_id", entry)
        self.assertNotIn("connection_type", entry)


class TestDuckDbPendingResolve(unittest.TestCase):
    """Tests for ``_resolve_pending_for_duckdb`` -- the DuckDB pre-resolve of
    ``PendingDataFrame`` proxies -- plus a version-drift guard asserting DuckDB's
    ``get_table_names`` returns a bound namespace name (the API the pre-resolve relies on).
    """

    def setUp(self):
        duckdb_engine._duckdb = None  # force a fresh duckdb connection per test

    def _ipython_modules(self, ns):
        """Return a sys.modules dict whose IPython.get_ipython() yields an ip with ns."""
        mock_ip = Mock()
        mock_ip.user_ns = ns
        mock_mod = Mock()
        mock_mod.get_ipython = Mock(return_value=mock_ip)
        return {"IPython": mock_mod}

    def _bare_duckdb(self):
        """A duckdb connection with only ``python_scan_all_frames`` set -- NOT the S3
        secret ``_ensure_duckdb`` also creates. get_table_names / replacement scans do not
        need the aws extension, and loading it requires a newer glibc than some build hosts
        have, so tests that exercise the real binder use this minimal connection."""
        import duckdb

        con = duckdb.connect()
        con.execute("SET python_scan_all_frames = true;")
        return con

    def test_ensure_duckdb_return_object_exposes_get_table_names(self):
        # Test-seam guard: production _resolve_pending_for_duckdb calls get_table_names on
        # the object _ensure_duckdb() RETURNS and the cell hands down -- the duckdb MODULE, not a
        # connection. Other tests hand it a connection, so they would not catch the module-level
        # get_table_names export going away (production would then fall into the except and
        # silently no-op behind logger.debug).
        #
        # Assert the EXPORT on the bare `import duckdb` module: no S3 extension / secret
        # needed, so this ALWAYS runs in CI (it is NOT skippable). This is the regression
        # that would actually break production. The functional parse check lives in a
        # separate, environment-gated test so a missing extension never masks THIS guard.
        import duckdb

        self.assertTrue(
            hasattr(duckdb, "get_table_names"),
            "the duckdb module must expose get_table_names -- the pre-resolve relies on it; "
            "if this fails, DuckDB pending pre-resolve silently no-ops in production",
        )

    def test_a_cell_asks_for_the_engine_once_and_pre_resolves_and_runs_on_it(self):
        # sql() with a pending frame referenced: one _ensure_duckdb() for the cell; the
        # pre-resolve's get_table_names and the statement both run on what it returned, and a
        # stream of three statements asks once as well.
        from sagemaker_studio.utils.pending_dataframe import PendingDataFrame
        from sagemaker_studio.utils.sqlutils_async import _MaterializationRegistry

        reg = _MaterializationRegistry()
        gen, _ = reg.start("df")
        reg.settle("df", gen, result=DataFrame({"a": [1]}))
        proxy = PendingDataFrame("df", gen, reg, timeout=2)
        engine_ = Mock()
        engine_.get_table_names.return_value = {"df"}
        engine_.sql.return_value.df.return_value = DataFrame({"a": [1]})

        with patch.dict("sys.modules", self._ipython_modules({"df": proxy})):
            with patch.object(duckdb_engine, "_ensure_duckdb", return_value=engine_) as ensure:
                sqlutils.sql("SELECT * FROM df")
        ensure.assert_called_once_with()
        engine_.get_table_names.assert_called_once_with("SELECT * FROM df")
        engine_.sql.assert_called_once_with("SELECT * FROM df")
        self.assertTrue(proxy.is_resolved)

        engine_.reset_mock()
        with patch.dict("sys.modules", self._ipython_modules({"df": proxy})):
            with patch.object(duckdb_engine, "_ensure_duckdb", return_value=engine_) as ensure:
                results = list(sqlutils.sql_stream("SELECT 1; SELECT 2; SELECT 3"))
        self.assertEqual([r.status for r in results], ["success"] * 3)
        ensure.assert_called_once_with()
        self.assertEqual(engine_.sql.call_count, 3)

    def test_ensure_duckdb_get_table_names_parses_referenced_name(self):
        # Functional companion to the module-level guard above: prove get_table_names on the
        # object _ensure_duckdb() actually returns parses a referenced name out of the SQL.
        # Needs the live duckdb the setup builds (S3 extension), so it is environment-gated;
        # the always-running guard above covers the export-removal regression regardless.
        try:
            duck = duckdb_engine._ensure_duckdb()
        except Exception as e:  # pragma: no cover - environment without the s3 extension
            self.skipTest(f"_ensure_duckdb unavailable for the functional check: {e}")

        class FakeProxy:
            pass

        df = FakeProxy()  # noqa: F841 -- bound so the name resolves for get_table_names
        self.assertIn("df", duck.get_table_names("SELECT * FROM df"))

    def test_get_table_names_returns_bound_name_version_guard(self):
        # Version-drift guard: assert against the LIVE duckdb API, not a hardcoded value,
        # so a duckdb bump that changes get_table_names behavior fails here on every build.
        con = self._bare_duckdb()

        class FakeProxy:
            pass

        df = FakeProxy()  # noqa: F841 -- bound so python_scan_all_frames can find `df`
        names = con.get_table_names("SELECT * FROM df")
        self.assertIn("df", names)
        # get_table_names does NOT execute / trigger the replacement scan on the proxy:
        # no InvalidInputException is raised even though `df` is an unsuitable type.
        multi = con.get_table_names("SELECT * FROM df JOIN df2 ON df.a = df2.a")
        self.assertEqual(set(multi), {"df", "df2"})

    def test_resolve_pending_resolves_referenced_proxy(self):
        from sagemaker_studio.utils.pending_dataframe import PendingDataFrame
        from sagemaker_studio.utils.sqlutils_async import _MaterializationRegistry

        reg = _MaterializationRegistry()
        gen, _ = reg.start("df")
        reg.settle("df", gen, result=DataFrame({"a": [1, 2]}))
        proxy = PendingDataFrame("df", gen, reg, timeout=2)
        ns = {"df": proxy}

        with patch.dict("sys.modules", self._ipython_modules(ns)):
            duckdb_engine._resolve_pending_for_duckdb(self._bare_duckdb(), "SELECT * FROM df")

        self.assertTrue(proxy.is_resolved)

    def test_resolve_pending_skips_unreferenced_proxy(self):
        from sagemaker_studio.utils.pending_dataframe import PendingDataFrame
        from sagemaker_studio.utils.sqlutils_async import _MaterializationRegistry

        reg = _MaterializationRegistry()
        gen_a, _ = reg.start("df_a")
        gen_b, _ = reg.start("df_b")
        reg.settle("df_a", gen_a, result=DataFrame({"a": [1]}))
        # df_b never settles -- if the pre-resolve wrongly touched it, it would block/time out.
        proxy_a = PendingDataFrame("df_a", gen_a, reg, timeout=2)
        proxy_b = PendingDataFrame("df_b", gen_b, reg, timeout=2)
        ns = {"df_a": proxy_a, "df_b": proxy_b}

        with patch.dict("sys.modules", self._ipython_modules(ns)):
            # Query references only df_a; df_b must be left untouched (referenced-only).
            duckdb_engine._resolve_pending_for_duckdb(self._bare_duckdb(), "SELECT * FROM df_a")

        self.assertTrue(proxy_a.is_resolved)
        self.assertFalse(proxy_b.is_resolved)

    def test_resolve_pending_noop_when_nothing_pending(self):
        # No PendingDataFrame in the namespace -> fast path returns without calling duckdb.
        ns = {"df": DataFrame({"a": [1]})}
        with patch.dict("sys.modules", self._ipython_modules(ns)):
            engine_ = Mock()
            duckdb_engine._resolve_pending_for_duckdb(engine_, "SELECT * FROM df")
            engine_.get_table_names.assert_not_called()

    def test_resolve_pending_swallows_get_table_names_error(self):
        from sagemaker_studio.utils.pending_dataframe import PendingDataFrame
        from sagemaker_studio.utils.sqlutils_async import _MaterializationRegistry

        reg = _MaterializationRegistry()
        gen, _ = reg.start("df")
        proxy = PendingDataFrame("df", gen, reg, timeout=2)
        ns = {"df": proxy}
        bad_con = Mock()
        bad_con.get_table_names.side_effect = RuntimeError("parse boom")

        with patch.dict("sys.modules", self._ipython_modules(ns)):
            # Must not raise -- falls through to today's behavior.
            duckdb_engine._resolve_pending_for_duckdb(bad_con, "SELECT * FROM df")
        # Proxy left unresolved (DuckDB then errors/handles as today), but no exception here.
        self.assertFalse(proxy.is_resolved)


class TestDuckDbPreResolveEdgePaths(unittest.TestCase):
    """The remaining defensive branches of _resolve_pending_for_duckdb: IPython import
    failure, no IPython shell, and the namespace-snapshot RuntimeError retry exhausting."""

    def setUp(self):
        duckdb_engine._duckdb = None

    def _ipython_modules(self, ns):
        mock_ip = Mock()
        mock_ip.user_ns = ns
        mock_mod = Mock()
        mock_mod.get_ipython = Mock(return_value=mock_ip)
        return {"IPython": mock_mod}

    def _bare_duckdb(self):
        import duckdb

        con = duckdb.connect()
        con.execute("SET python_scan_all_frames = true;")
        return con

    def test_no_op_when_ipython_import_fails(self):
        # `from IPython import get_ipython` raising -> the except returns without touching
        # duckdb. Simulate by making the IPython module raise on attribute access.
        import builtins

        real_import = builtins.__import__

        def fake_import(name, *args, **kwargs):
            if name == "IPython":
                raise ImportError("no IPython in this env")
            return real_import(name, *args, **kwargs)

        with patch.object(builtins, "__import__", side_effect=fake_import):
            engine_ = Mock()
            duckdb_engine._resolve_pending_for_duckdb(engine_, "SELECT * FROM df")  # must not raise
            engine_.get_table_names.assert_not_called()

    def test_no_op_when_no_ipython_shell(self):
        # get_ipython() returns None (no interactive shell) -> return before duckdb.
        mock_mod = Mock()
        mock_mod.get_ipython = Mock(return_value=None)
        with patch.dict("sys.modules", {"IPython": mock_mod}):
            engine_ = Mock()
            duckdb_engine._resolve_pending_for_duckdb(engine_, "SELECT * FROM df")
            engine_.get_table_names.assert_not_called()

    def test_snapshot_retry_exhausts_returns_without_duckdb(self):
        # Every namespace-snapshot attempt raises RuntimeError -> after the retry budget the
        # function returns without calling duckdb (best-effort pre-resolve, never fatal).
        class AngryNS(dict):
            def items(self):
                raise RuntimeError("dictionary changed size during iteration")

        mock_ip = Mock()
        mock_ip.user_ns = AngryNS({"df": object()})
        mock_mod = Mock()
        mock_mod.get_ipython = Mock(return_value=mock_ip)
        with patch.dict("sys.modules", {"IPython": mock_mod}):
            engine_ = Mock()
            duckdb_engine._resolve_pending_for_duckdb(engine_, "SELECT * FROM df")  # must not raise
            engine_.get_table_names.assert_not_called()

    def test_referenced_non_proxy_name_is_skipped(self):
        # A referenced name bound to a non-proxy (plain DataFrame) is skipped by the resolve
        # loop's isinstance check, while a sibling proxy still resolves.
        from sagemaker_studio.utils.pending_dataframe import PendingDataFrame
        from sagemaker_studio.utils.sqlutils_async import _MaterializationRegistry

        reg = _MaterializationRegistry()
        gen, _ = reg.start("df")
        reg.settle("df", gen, result=DataFrame({"a": [1]}))
        proxy = PendingDataFrame("df", gen, reg, timeout=2)
        plain = DataFrame({"b": [9]})  # a real frame, NOT a proxy
        ns = {"df": proxy, "plain": plain}

        con = self._bare_duckdb()
        with patch.dict("sys.modules", self._ipython_modules(ns)):
            # References both: `plain` (skipped) and `df` (resolved).
            duckdb_engine._resolve_pending_for_duckdb(
                con, "SELECT * FROM df JOIN plain ON df.a = plain.b"
            )

        self.assertTrue(proxy.is_resolved)
        self.assertIs(ns["plain"], plain)  # non-proxy left untouched


class TestEnsureDuckdb(unittest.TestCase):
    """Managed DuckDB extension baseline: _duckdb_bundle_directory and _ensure_duckdb (doc section 3.1)."""

    def setUp(self):
        duckdb_engine._duckdb = None

    def tearDown(self):
        duckdb_engine._duckdb = None
        duckdb_engine._ambient_s3_secret = False
        duckdb_engine._ambient_s3_secret_unavailable = False
        duckdb_engine._default_aws_credentials_disabled = False

    # --- _duckdb_bundle_directory ---

    @staticmethod
    def _duckdb_module_in(venv_dir):
        """A fake duckdb module whose __file__ sits inside venv_dir."""
        module = Mock()
        module.__file__ = os.path.join(
            venv_dir, "lib", "python3.11", "site-packages", "duckdb", "__init__.py"
        )
        return module

    def test_bundle_directory_returns_sibling_of_pyvenv(self):
        with tempfile.TemporaryDirectory() as root:
            venv = os.path.join(root, ".venv")
            os.makedirs(os.path.join(venv, "lib", "python3.11", "site-packages", "duckdb"))
            Path(venv, "pyvenv.cfg").write_text("")
            bundle = os.path.join(
                root, duckdb_extensions._DUCKDB_BUNDLE_DIRECTORY_NAME
            )  # sibling of the venv
            os.makedirs(bundle)
            result = duckdb_extensions._duckdb_bundle_directory(self._duckdb_module_in(venv))
            # Production code resolves symlinks (e.g. macOS /var -> /private/var), so resolve here too.
            self.assertEqual(result, str(Path(bundle).resolve()))

    def test_bundle_directory_none_when_sibling_missing(self):
        with tempfile.TemporaryDirectory() as root:
            venv = os.path.join(root, ".venv")
            os.makedirs(os.path.join(venv, "lib", "python3.11", "site-packages", "duckdb"))
            Path(venv, "pyvenv.cfg").write_text("")
            # No duckdb_extensions sibling created.
            self.assertIsNone(
                duckdb_extensions._duckdb_bundle_directory(self._duckdb_module_in(venv))
            )

    def test_bundle_directory_none_when_not_in_venv(self):
        with tempfile.TemporaryDirectory() as root:
            # No pyvenv.cfg anywhere above duckdb.__file__, and not under the base interpreter.
            pkg = os.path.join(root, "site-packages", "duckdb")
            os.makedirs(pkg)
            module = Mock()
            module.__file__ = os.path.join(pkg, "__init__.py")
            self.assertIsNone(duckdb_extensions._duckdb_bundle_directory(module))

    def test_bundle_directory_is_beside_the_base_runtime_without_a_venv(self):
        # An AWS Notebook local kernel: duckdb in the bundled runtime (no pyvenv.cfg), the
        # pre-installed extensions beside it: <app>/dist/python -> <app>/dist/duckdb_extensions.
        with tempfile.TemporaryDirectory() as root:
            runtime = os.path.join(root, "dist", "python")
            os.makedirs(os.path.join(runtime, "lib", "python3.11", "site-packages", "duckdb"))
            bundle = os.path.join(root, "dist", duckdb_extensions._DUCKDB_BUNDLE_DIRECTORY_NAME)
            os.makedirs(bundle)
            with patch.object(sys, "base_prefix", runtime):
                result = duckdb_extensions._duckdb_bundle_directory(self._duckdb_module_in(runtime))
            self.assertEqual(result, str(Path(bundle).resolve()))

    def test_bundle_directory_none_for_a_duckdb_in_the_users_own_packages(self):
        # The user's venv sits beside their own duckdb_extensions folder: never a bundle.
        with tempfile.TemporaryDirectory() as root:
            venv = os.path.join(root, ".awsnotebook", ".venv")
            os.makedirs(os.path.join(venv, "lib", "python3.11", "site-packages", "duckdb"))
            Path(venv, "pyvenv.cfg").write_text("")
            os.makedirs(
                os.path.join(root, ".awsnotebook", duckdb_extensions._DUCKDB_BUNDLE_DIRECTORY_NAME)
            )
            with patch.dict(os.environ, {"UV_PROJECT_ENVIRONMENT": venv}):
                self.assertIsNone(
                    duckdb_extensions._duckdb_bundle_directory(self._duckdb_module_in(venv))
                )

    # --- _ensure_duckdb ---

    @staticmethod
    def _make_duckdb_mock(fail_on=None, installed=("httpfs", "aws")):
        """Mock duckdb module; .sql raises when a statement contains the fail_on substring, and
        duckdb_extensions() reports ``installed`` as installed."""
        calls = []
        duckdb = Mock()

        def _sql(stmt):
            calls.append(stmt)
            if fail_on and fail_on in stmt:
                raise RuntimeError(f"boom: {stmt}")
            if "duckdb_extensions()" in stmt:
                return Mock(fetchall=Mock(return_value=[(name, []) for name in installed]))
            return Mock()

        def _execute(stmt, params=None):
            calls.append(stmt)
            return Mock()

        duckdb.sql.side_effect = _sql
        duckdb.execute.side_effect = _execute
        duckdb._calls = calls
        return duckdb

    @staticmethod
    def _run_ensure(duckdb_mock, bundle_dir):
        with patch.dict(sys.modules, {"duckdb": duckdb_mock}), patch(
            "sagemaker_studio.sql_engine.duckdb_engine.extensions._duckdb_bundle_directory",
            return_value=bundle_dir,
        ):
            return duckdb_engine._ensure_duckdb()

    def test_bundle_loads_all_required_extensions(self):
        duckdb = self._make_duckdb_mock()
        result = self._run_ensure(duckdb, "/bundle")
        self.assertIs(result, duckdb)
        self.assertIn("LOAD httpfs;", duckdb._calls)
        self.assertIn("LOAD aws;", duckdb._calls)
        self.assertIn("SET lock_configuration = true;", duckdb._calls)

    def test_neither_mode_replaces_duckdbs_default_connection(self):
        # No connection of the SDK's own: a cell's own duckdb.sql() and the SDK's statements share
        # DuckDB's default session in both modes.
        for local in (True, False):
            duckdb = self._make_duckdb_mock()
            duckdb_engine._duckdb = None
            with patch("sagemaker_studio.sql_engine.duckdb_engine.engine.local_kernel") as lk:
                lk.is_local_kernel.return_value = local
                self._run_ensure(duckdb, "/bundle" if local else None)
            duckdb.connect.assert_not_called()
            duckdb.set_default_connection.assert_not_called()

    def test_both_modes_keep_state_made_with_duckdb_sql_before_the_first_sql_cell(self):
        import duckdb as real_duckdb

        for local in (False, True):
            duckdb_engine._duckdb = None
            saved = real_duckdb.default_connection()
            real_duckdb.set_default_connection(real_duckdb.connect(":memory:"))
            try:
                real_duckdb.sql("CREATE TEMP TABLE made_by_the_user AS SELECT 42 AS answer")
                with patch(
                    "sagemaker_studio.sql_engine.duckdb_engine.engine.local_kernel"
                ) as lk, patch(
                    "sagemaker_studio.sql_engine.duckdb_engine.extensions._duckdb_bundle_directory",
                    return_value=None,
                ), patch.object(
                    duckdb_engine, "_sync_ambient_s3_secret"
                ):  # its S3 secret would download the aws extension, and builds have no network
                    lk.is_local_kernel.return_value = local
                    duck = duckdb_engine._ensure_duckdb()
                    self.assertEqual(
                        duck.sql("SELECT answer FROM made_by_the_user").fetchall(), [(42,)], local
                    )
            finally:
                real_duckdb.set_default_connection(saved)

    def test_no_bundle_runs_todays_behavior(self):
        duckdb = self._make_duckdb_mock()
        result = self._run_ensure(duckdb, None)
        self.assertIs(result, duckdb)
        joined = " ".join(duckdb._calls)
        self.assertNotIn("extension_directories", joined)
        self.assertNotIn("lock_configuration", joined)
        self.assertNotIn("autoinstall_known_extensions", joined)
        self.assertIn("SET python_scan_all_frames = true;", duckdb._calls)

    def test_local_kernel_takes_the_bundle_path_like_smus(self):
        duckdb = self._make_duckdb_mock()
        with patch(
            "sagemaker_studio.sql_engine.duckdb_engine.engine.local_kernel"
        ) as mock_local_kernel, patch.dict(os.environ, {"UV_PROJECT": "/ws/.awsnotebook"}):
            mock_local_kernel.is_local_kernel.return_value = True
            result = self._run_ensure(duckdb, "/app/dist/duckdb_extensions")
        self.assertIs(result, duckdb)
        ext_call = next(
            c for c in duckdb.execute.call_args_list if "extension_directories" in c.args[0]
        )
        self.assertEqual(
            ext_call.args[1][0],
            ["/ws/.awsnotebook/duckdb_extensions", "/app/dist/duckdb_extensions"],
        )
        self.assertIn("SET autoinstall_known_extensions = false;", duckdb._calls)
        self.assertIn("LOAD httpfs;", duckdb._calls)
        self.assertIn("LOAD aws;", duckdb._calls)
        self.assertIn("SET lock_configuration = true;", duckdb._calls)
        self.assertLess(
            duckdb._calls.index("SET allowed_configs = ?"),
            duckdb._calls.index("SET lock_configuration = true;"),
        )
        # A local kernel gets the credential-chain secret too: the chain resolves the container
        # credentials the kernel server serves from the app's signed-in session.
        self.assertIn(duckdb_engine._AMBIENT_S3_SECRET_STATEMENT, duckdb._calls)

    def test_bundle_present_issues_statements_in_order(self):
        duckdb = self._make_duckdb_mock()
        with patch.dict(os.environ, {"UV_PROJECT": "/user/proj"}):
            result = self._run_ensure(duckdb, "/bundle")
        self.assertIs(result, duckdb)
        calls = duckdb._calls
        self.assertEqual(
            calls,
            [
                "SET extension_directories = ?",
                "SET autoinstall_known_extensions = false;",
                "LOAD httpfs;",
                "LOAD aws;",
                "SET python_scan_all_frames = true;",
                "CREATE SECRET (TYPE s3, PROVIDER credential_chain, REFRESH auto);",
                "SET GLOBAL aws_default_credentials = false;",
                "SET allowed_configs = ?",
                "SET lock_configuration = true;",
            ],
        )
        self.assertEqual(
            duckdb.execute.call_args_list,
            [
                call(
                    "SET extension_directories = ?", [["/user/proj/duckdb_extensions", "/bundle"]]
                ),
                call("SET allowed_configs = ?", [list(duckdb_extensions._DUCKDB_USER_CONFIGS)]),
            ],
        )

    def test_two_threads_asking_for_the_engine_at_once_set_it_up_once(self):
        # The engine is set up under its lock: a second caller arriving while the first is still
        # loading extensions waits for that engine instead of starting another on the same
        # default connection.
        duckdb = self._make_duckdb_mock()
        original, paused = duckdb.sql.side_effect, []
        inside, release = threading.Event(), threading.Event()

        def pausing(stmt):
            if stmt == "LOAD httpfs;" and not paused:
                paused.append(stmt)
                inside.set()
                release.wait(5)
            return original(stmt)

        duckdb.sql.side_effect = pausing
        results = []
        with patch.dict(sys.modules, {"duckdb": duckdb}), patch(
            "sagemaker_studio.sql_engine.duckdb_engine.extensions._duckdb_bundle_directory",
            return_value="/bundle",
        ):
            first = threading.Thread(target=lambda: results.append(duckdb_engine._ensure_duckdb()))
            first.start()
            self.assertTrue(inside.wait(5))
            second = threading.Thread(target=lambda: results.append(duckdb_engine._ensure_duckdb()))
            second.start()
            second.join(0.3)
            self.assertTrue(second.is_alive())  # waiting for the set-up under way
            release.set()
            first.join(5)
            second.join(5)
        self.assertEqual(results, [duckdb, duckdb])
        for statement in (
            "LOAD httpfs;",
            "CREATE SECRET (TYPE s3, PROVIDER credential_chain, REFRESH auto);",
            "SET lock_configuration = true;",
        ):
            self.assertEqual(duckdb._calls.count(statement), 1, statement)

    def test_the_aws_extensions_default_chain_fallback_is_switched_off_after_the_load_and_before_the_lock(
        self,
    ):
        # DuckDB 2.0's aws extension signs an unmatched s3:// read with the identity the default
        # chain found at the first such read, for the database's lifetime: off, so the SDK's
        # secrets are the only credentials DuckDB ever signs with. The setting exists only once the
        # extension is loaded, and the lock afterwards keeps user code from switching it back on.
        duckdb = self._make_duckdb_mock()
        self._run_ensure(duckdb, "/bundle")
        calls = duckdb._calls
        off = calls.index("SET GLOBAL aws_default_credentials = false;")
        self.assertLess(calls.index("LOAD aws;"), off)
        self.assertLess(off, calls.index("SET lock_configuration = true;"))
        self.assertNotIn("aws_default_credentials", duckdb_extensions._DUCKDB_USER_CONFIGS)
        # Without a bundle too: the secret's CREATE autoloads the extension, and there is no lock.
        duckdb_engine._duckdb = None  # a new engine, as the test's setUp gives
        duckdb = self._make_duckdb_mock()
        self._run_ensure(duckdb, None)
        self.assertIn("SET GLOBAL aws_default_credentials = false;", duckdb._calls)

    def test_a_duckdb_without_the_aws_default_credentials_setting_still_comes_up(self):
        # An older aws extension (DuckDB 1.x) has neither the fallback nor the setting: the refusal
        # is noted at DEBUG and the setup goes on to the lock.
        duckdb = self._make_duckdb_mock(fail_on="aws_default_credentials")
        with self.assertLogs(
            "sagemaker_studio.sql_engine.duckdb_engine.engine", level="DEBUG"
        ) as logs:
            result = self._run_ensure(duckdb, "/bundle")
        self.assertIs(result, duckdb)
        self.assertIs(duckdb_engine._duckdb, duckdb)
        self.assertIn("SET lock_configuration = true;", duckdb._calls)
        self.assertTrue(any("no aws_default_credentials setting" in line for line in logs.output))
        self.assertFalse(any("WARNING" in line or "ERROR" in line for line in logs.output))
        self.assertFalse(duckdb_engine._default_aws_credentials_disabled)

    def test_the_fallback_is_switched_off_once_the_extension_loads_even_when_setup_could_not(self):
        # No bundle and offline at setup: the chain secret's CREATE cannot download the aws
        # extension, so the setting does not exist yet and the fallback stays on. The first attempt
        # that loads the extension (a sign-in's attach_local_catalogs() resetting the ambient secret)
        # switches it off, and once off it is not set again.
        calls = []
        offline = {"on": True}
        duckdb = Mock()

        def _sql(stmt):
            calls.append(stmt)
            if offline["on"] and ("CREATE SECRET" in stmt or "aws_default_credentials" in stmt):
                raise RuntimeError(f"offline: {stmt}")
            return Mock()

        duckdb.sql.side_effect = _sql
        duckdb.execute.side_effect = lambda stmt, params=None: calls.append(stmt)
        switch = "SET GLOBAL aws_default_credentials = false;"
        with patch("sagemaker_studio.sql_engine.duckdb_engine.engine.local_kernel") as lk:
            lk.is_local_kernel.return_value = True
            self.assertIs(self._run_ensure(duckdb, None), duckdb)
        self.assertEqual(calls.count(switch), 1)  # tried right after the failed CREATE, refused
        self.assertFalse(duckdb_engine._default_aws_credentials_disabled)
        offline["on"] = (
            False  # the user signs in: attach_local_catalogs() resets the ambient secret
        )
        duckdb_engine._reset_ambient_s3_secret(duckdb)
        self.assertTrue(duckdb_engine._ambient_s3_secret)
        self.assertTrue(duckdb_engine._default_aws_credentials_disabled)
        self.assertEqual(calls.count(switch), 2)
        self.assertEqual(
            calls[-2:],
            ["CREATE SECRET (TYPE s3, PROVIDER credential_chain, REFRESH auto);", switch],
        )
        duckdb_engine._reset_ambient_s3_secret(duckdb)  # off already: not set again
        self.assertEqual(calls.count(switch), 2)

    def test_bundle_present_uv_project_unset_falls_back(self):
        duckdb = self._make_duckdb_mock()
        with patch.dict(os.environ, {}, clear=True):
            self._run_ensure(duckdb, "/bundle")
            expected_user = os.path.join(os.path.expanduser("~"), ".duckdb", "extensions")
        ext_call = next(
            c for c in duckdb.execute.call_args_list if "extension_directories" in c.args[0]
        )
        self.assertEqual(ext_call.args[1][0], [expected_user, "/bundle"])

    def test_setup_failure_leaves_duckdb_uncached(self):
        duckdb = self._make_duckdb_mock(fail_on="SET python_scan_all_frames")
        with self.assertRaises(RuntimeError):
            self._run_ensure(duckdb, None)
        self.assertIsNone(duckdb_engine._duckdb)  # next call retries the full setup

    def test_no_bundle_create_secret_failure_is_nonfatal(self):
        duckdb = self._make_duckdb_mock(fail_on="CREATE SECRET")
        with self.assertLogs("sagemaker_studio.sql_engine.duckdb_engine.engine", level="WARNING"):
            result = self._run_ensure(duckdb, None)
        self.assertIs(result, duckdb)
        self.assertIs(duckdb_engine._duckdb, duckdb)  # still cached

    def test_bundle_present_create_secret_failure_raises(self):
        duckdb = self._make_duckdb_mock(fail_on="CREATE SECRET")
        with patch.dict(os.environ, {"UV_PROJECT": "/user/proj"}):
            with self.assertRaises(RuntimeError):
                self._run_ensure(duckdb, "/bundle")
        self.assertIsNone(duckdb_engine._duckdb)
        self.assertNotIn("SET lock_configuration = true;", duckdb._calls)  # nothing locked

    def test_a_local_kernel_signed_out_still_gets_its_engine_without_the_secret(self):
        # The chain has nothing to resolve while the app is signed out: a normal state on a local
        # kernel, so the engine comes up (local files need no credentials) and only S3 reads are
        # refused, when they run.
        duckdb = self._make_duckdb_mock(fail_on="CREATE SECRET")
        with patch(
            "sagemaker_studio.sql_engine.duckdb_engine.engine.local_kernel"
        ) as lk, patch.dict(os.environ, {"UV_PROJECT": "/user/proj"}):
            lk.is_local_kernel.return_value = True
            with self.assertLogs(
                "sagemaker_studio.sql_engine.duckdb_engine.engine", level="INFO"
            ) as logs:
                result = self._run_ensure(duckdb, "/bundle")
        self.assertIs(result, duckdb)
        self.assertIs(duckdb_engine._duckdb, duckdb)
        self.assertIn("SET lock_configuration = true;", duckdb._calls)
        self.assertTrue(duckdb_engine._ambient_s3_secret_unavailable)
        self.assertFalse(duckdb_engine._ambient_s3_secret)
        self.assertTrue(any("signed out" in line for line in logs.output))
        self.assertFalse(any("WARNING" in line for line in logs.output))

    def test_bundle_present_incomplete_load_raises(self):
        duckdb = self._make_duckdb_mock(fail_on="LOAD httpfs")
        with patch.dict(os.environ, {"UV_PROJECT": "/user/proj"}):
            with self.assertRaises(RuntimeError):
                self._run_ensure(duckdb, "/bundle")
        self.assertIsNone(duckdb_engine._duckdb)


class TestAthenaV4SyncPath(unittest.TestCase):
    """Athena engine version 4 on the sync path: the Athena API executor, no PyAthena engine."""

    def _patches(self, athena_v4):
        conn = Mock(type="ATHENA")
        return [
            patch("sagemaker_studio.utils.sqlutils._resolve_connection", return_value=conn),
            patch("sagemaker_studio.utils.sqlutils._athena_api", return_value=athena_v4),
            patch(
                "sagemaker_studio.utils.sqlutils._get_or_create_connection",
                side_effect=AssertionError("no PyAthena engine"),
            ),
        ]

    def _executor(self):
        from sagemaker_studio.sql_engine.sql_executor import SingleStatementResult

        athena_v4 = Mock()
        athena_v4.execute.side_effect = lambda stmt: SingleStatementResult(
            result=DataFrame({"stmt": [stmt]}), execution_metadata={"query_execution_id": "q"}
        )
        return athena_v4

    def test_sql_runs_through_the_athena_api_executor(self):
        athena_v4 = self._executor()
        patches = self._patches(athena_v4)
        for p in patches:
            p.start()
        self.addCleanup(lambda: [p.stop() for p in patches])
        result = sqlutils.sql("SELECT 1", connection_name="athena_conn")
        self.assertEqual(result["stmt"].tolist(), ["SELECT 1"])
        athena_v4.execute.assert_called_once_with("SELECT 1")

    def test_sql_raises_native_athena_failure(self):
        athena_v4 = Mock()
        athena_v4.execute.side_effect = RuntimeError("Athena query q FAILED: bad data")
        patches = self._patches(athena_v4)
        for patcher in patches:
            patcher.start()
        self.addCleanup(lambda: [patcher.stop() for patcher in patches])

        with self.assertRaisesRegex(RuntimeError, "Athena query q FAILED: bad data"):
            sqlutils.sql("SELECT 1", connection_name="athena_conn")

    def test_comment_only_query_returns_none(self):
        athena_v4 = self._executor()
        patches = self._patches(athena_v4)
        for patcher in patches:
            patcher.start()
        self.addCleanup(lambda: [patcher.stop() for patcher in patches])

        self.assertIsNone(sqlutils.sql("-- comment only", connection_name="athena_conn"))
        athena_v4.execute.assert_not_called()

    def test_sql_stream_runs_each_statement_and_records_metadata(self):
        athena_v4 = self._executor()
        patches = self._patches(athena_v4)
        for p in patches:
            p.start()
        self.addCleanup(lambda: [p.stop() for p in patches])
        results = list(sqlutils.sql_stream("SELECT 1; SELECT 2", connection_name="athena_conn"))
        self.assertEqual([r.result["stmt"].tolist() for r in results], [["SELECT 1"], ["SELECT 2"]])
        self.assertEqual(
            [m["connection_type"] for m in sqlutils._last_sql_execution_metadata],
            ["ATHENA", "ATHENA"],
        )

    def test_named_parameters_reach_native_athena_executor(self):
        from sagemaker_studio.utils import athena_v4 as athena_module

        conn = Mock(type="ATHENA")
        with patch.object(athena_module, "athena_executor", return_value="native") as native:
            result = sqlutils._athena_api(conn, {}, parameters={"a": 1})
        self.assertEqual(result, "native")
        native.assert_called_once_with(
            conn,
            catalog=None,
            schema=None,
            selected_engine_version=None,
            parameters={"a": 1},
        )

    def test_non_athena_connection_has_no_native_executor(self):
        from sagemaker_studio.utils import athena_v4 as athena_module

        with patch.object(athena_module, "athena_executor", return_value=None):
            self.assertIsNone(sqlutils._athena_api(Mock(type="REDSHIFT"), {}))

    def test_malformed_athena_connection_never_falls_back_to_duckdb(self):
        conn = Mock(type="ATHENA", id="conn-1", name="athena")
        conn.data.workgroup_name = None
        with patch.object(sqlutils, "_resolve_connection", return_value=conn), patch.object(
            duckdb_engine, "_run_local_duckdb", side_effect=AssertionError("must not use DuckDB")
        ):
            with self.assertRaisesRegex(ValueError, "non-empty workgroup_name"):
                sqlutils.sql("SELECT 1", connection_name="athena")

    def test_catalog_schema_engine_and_parameters_reach_the_executor(self):
        from sagemaker_studio.utils import athena_v4 as athena_module

        conn = Mock(type="ATHENA")
        with patch.object(athena_module, "athena_executor") as select:
            sqlutils._athena_api(
                conn,
                {
                    "catalog_name": "cat",
                    "schema_name": "db",
                    "selected_engine_version": "Athena engine version 4",
                },
                parameters=["value"],
            )
        select.assert_called_once_with(
            conn,
            catalog="cat",
            schema="db",
            selected_engine_version="Athena engine version 4",
            parameters=["value"],
        )

    def test_close_all_connections_clears_the_engine_version_cache(self):
        from sagemaker_studio.utils import athena_v4 as athena_v4_module

        with patch("sagemaker_studio.utils.sqlutils._stop_glue_spark"), patch(
            "sagemaker_studio.utils.sqlutils._connection_cache"
        ), patch.object(athena_v4_module, "clear_cache") as clear:
            sqlutils.close_all_connections()
        clear.assert_called_once()


class TestNativeAthenaCredentialProvider(unittest.TestCase):
    class FakeConnection(Connection):
        def __init__(self, connection_id=None, name=None):
            self.type = "ATHENA"
            self.id = connection_id
            self.name = name
            self._test_creds = Mock(
                access_key_id="cached",
                secret_access_key="secret",
                session_token="token",
                expiration=None,
            )

        @property
        def sql_engine_type(self):
            return "ATHENA"

        @property
        def connection_creds(self):
            return self._test_creds

    def _provider(self, conn):
        from sagemaker_studio.utils import athena_v4 as athena_module

        with patch.object(athena_module, "athena_executor", return_value="native") as native:
            self.assertEqual(sqlutils._athena_api(conn, {}), "native")
        return native.call_args.kwargs["credential_provider"]

    def test_refresh_re_resolves_connection_by_id(self):
        conn = self.FakeConnection(connection_id="id-1", name="name-1")
        fresh = Mock(
            connection_creds=Mock(
                access_key_id="fresh-id",
                secret_access_key="secret",
                session_token="token",
                expiration=None,
            )
        )
        with patch.object(sqlutils, "_resolve_connection", return_value=fresh) as resolve:
            credentials = self._provider(conn)()
        self.assertEqual(credentials["access_key_id"], "fresh-id")
        resolve.assert_called_once_with("id-1", None)

    def test_refresh_re_resolves_connection_by_name(self):
        conn = self.FakeConnection(name="name-1")
        fresh = Mock(
            connection_creds=Mock(
                access_key_id="fresh-name",
                secret_access_key="secret",
                session_token="token",
                expiration=None,
            )
        )
        with patch.object(sqlutils, "_resolve_connection", return_value=fresh) as resolve:
            credentials = self._provider(conn)()
        self.assertEqual(credentials["access_key_id"], "fresh-name")
        resolve.assert_called_once_with(None, "name-1")

    def test_refresh_falls_back_to_the_connection_credentials(self):
        conn = self.FakeConnection()
        credentials = self._provider(conn)()
        self.assertEqual(credentials["access_key_id"], "cached")


if __name__ == "__main__":
    unittest.main()
