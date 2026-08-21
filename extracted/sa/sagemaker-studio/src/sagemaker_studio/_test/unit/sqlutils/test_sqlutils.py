import unittest
from datetime import datetime
from unittest.mock import Mock, PropertyMock, patch

from dateutil.tz import tzlocal
from pandas import DataFrame

from sagemaker_studio import Connection, sqlutils
from sagemaker_studio.project import Project
from sagemaker_studio.sql_engine.sql_executor import SqlExecutor
from sagemaker_studio.utils._sql_cache import ManagedConnection


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

    @patch("sagemaker_studio.sqlutils._ensure_duckdb")
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

    @patch("sagemaker_studio.sqlutils.HelperFactory")
    @patch("sagemaker_studio.sqlutils._ensure_project")
    @patch("sagemaker_studio.sqlutils._ensure_sql_executor")
    def test_sql_with_athena_connection(
        self, mock_ensure_sql_executor, mock_ensure_project, mock_helper_factory
    ):
        """Test SQL execution with Athena connection"""
        # Setup mock project to return our Connection instance
        mock_project = Mock()
        # Allow connection to be called multiple times (for _is_spark_connection check and get_engine)
        mock_project.connection = Mock(return_value=self.mock_connection)
        mock_ensure_project.return_value = mock_project

        # Setup mock SQL helper
        mock_sql_helper = Mock()
        mock_sql_helper.to_sql_config.return_value = {
            "region_name": "us-east-1",
            "aws_access_key_id": "mock_access_key",
            "aws_secret_access_key": "mock_secret_key",
            "aws_session_token": "mock_session_token",
            "workgroup": "workgroup-projectid12345-environmentid1",
            "database": "default",
            "catalog": "AwsDataCatalog",
        }
        mock_helper_factory.get_sql_helper.return_value = mock_sql_helper

        mock_sql_executor = Mock()
        mock_ensure_sql_executor.return_value = mock_sql_executor
        mock_engine = Mock()
        mock_sql_executor.create_engine.return_value = mock_engine
        mock_sql_executor.get_supported_connection_types.return_value = ["ATHENA"]

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
        result = sqlutils.sql(query, connection_name="project.athena")

        # Verify the interaction with helper factory
        # Connection is called only once due to refactored _resolve_connection
        assert mock_project.connection.call_count == 1
        mock_project.connection.assert_called_with("project.athena")
        mock_helper_factory.get_sql_helper.assert_called_once_with("ATHENA")

        # Verify sql helper was called
        self.assertEqual(mock_sql_helper.to_sql_config.call_count, 1)
        call_args = mock_sql_helper.to_sql_config.call_args
        self.assertEqual(call_args[0][0], self.mock_connection)

        # Verify engine creation with correct config
        mock_sql_executor.create_engine.assert_called_once()

        # Verify query execution - with persist_session=True, conn is created
        mock_sql_executor.execute.assert_called_once()
        call_args = mock_sql_executor.execute.call_args
        self.assertEqual(call_args[0][0], mock_engine)  # engine (positional)
        self.assertEqual(call_args[0][1], query)  # query (positional)
        self.assertIsNotNone(call_args[1]["connection"])  # connection (keyword)
        self.assertEqual(call_args[1].get("parameters"), None)  # parameters (keyword)

        # Verify result
        self.assertIsInstance(result, DataFrame)
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

    @patch("sagemaker_studio.sqlutils._ensure_duckdb")
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

    @patch("sagemaker_studio.sqlutils.HelperFactory")
    @patch("sagemaker_studio.sqlutils._ensure_project")
    @patch("sagemaker_studio.sqlutils._sql_executor")
    def test_sql_stream_with_connection(
        self, mock_sql_executor, mock_ensure_project, mock_helper_factory
    ):
        """Test sql_stream execution with connection"""
        mock_project = Mock()
        mock_project.connection.return_value = self.mock_connection
        mock_ensure_project.return_value = mock_project

        mock_sql_helper = Mock()
        mock_sql_helper.to_sql_config.return_value = {"region_name": "us-east-1"}
        mock_helper_factory.get_sql_helper.return_value = mock_sql_helper

        mock_engine = Mock()
        mock_sql_executor.create_engine.return_value = mock_engine
        mock_sql_executor.get_supported_connection_types.return_value = ["ATHENA"]

        from sagemaker_studio.sql_engine.sql_executor import ExecutionResult

        results = [
            ExecutionResult(0, "SELECT 1", "SELECT", DataFrame({"col1": [1]}), status="success"),
            ExecutionResult(1, "SELECT 2", "SELECT", DataFrame({"col1": [2]}), status="success"),
        ]
        mock_sql_executor.execute.return_value = iter(results)

        query = "SELECT 1; SELECT 2"
        stream_results = list(sqlutils.sql_stream(query, connection_name="project.athena"))

        self.assertEqual(len(stream_results), 2)
        mock_sql_executor.execute.assert_called_once()

    @patch("sagemaker_studio.sqlutils._ensure_duckdb")
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

    @patch("sagemaker_studio.sqlutils.HelperFactory")
    @patch("sagemaker_studio.sqlutils._ensure_project")
    @patch("sagemaker_studio.sqlutils._sql_executor")
    def test_sql_with_connection_id(
        self, mock_sql_executor, mock_ensure_project, mock_helper_factory
    ):
        """Test SQL execution with connection_id instead of connection_name"""
        mock_project = Mock()
        # Allow connection to be called multiple times (for _is_spark_connection check and get_engine)
        mock_project.connection = Mock(return_value=self.mock_connection)
        mock_ensure_project.return_value = mock_project

        mock_sql_helper = Mock()
        mock_sql_helper.to_sql_config.return_value = {"region_name": "us-east-1"}
        mock_helper_factory.get_sql_helper.return_value = mock_sql_helper

        mock_engine = Mock()
        mock_sql_executor.create_engine.return_value = mock_engine
        mock_sql_executor.get_supported_connection_types.return_value = ["ATHENA"]

        from sagemaker_studio.sql_engine.sql_executor import ExecutionResult

        execution_result = ExecutionResult(
            statement_index=0,
            statement="SELECT 1",
            statement_type="SELECT",
            result=DataFrame({"col1": [1]}),
            status="success",
        )
        mock_sql_executor.execute.return_value = iter([execution_result])

        result = sqlutils.sql("SELECT 1", connection_id="conn123")

        # Connection is called only once due to refactored _resolve_connection
        assert mock_project.connection.call_count == 1
        mock_project.connection.assert_called_with(id="conn123")
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
    @patch("sagemaker_studio.sqlutils._ensure_sql_executor")
    @patch("sagemaker_studio.sqlutils._get_or_create_connection")
    @patch("sagemaker_studio.sqlutils._resolve_connection")
    def test_sql_athena_injects_catalog_and_schema(
        self, mock_resolve, mock_get_or_create, mock_executor, mock_ctx
    ):
        """When Athena query has catalog+database, they are passed as kwargs"""
        mock_conn = Mock()
        mock_conn.type = "ATHENA"
        mock_resolve.return_value = mock_conn
        mock_managed = Mock()
        mock_managed.engine = Mock()
        mock_managed.engine.get_execution_options.return_value = {"connection_type": "ATHENA"}
        mock_managed.connection = None
        mock_get_or_create.return_value = mock_managed
        mock_ctx.return_value = {"catalog": "my_cat", "database": "my_db"}
        mock_exec_result = Mock()
        mock_exec_result.result = "df"
        mock_executor.return_value.execute.return_value = iter([mock_exec_result])

        sqlutils.sql("SELECT 1", connection_id="c1")
        mock_ctx.assert_called_once()

    @patch("sagemaker_studio.utils.sql_handler.get_execution_context")
    @patch("sagemaker_studio.sqlutils._ensure_sql_executor")
    @patch("sagemaker_studio.sqlutils._get_or_create_connection")
    @patch("sagemaker_studio.sqlutils._resolve_connection")
    def test_sql_stream_athena_injects_catalog_and_schema(
        self, mock_resolve, mock_get_or_create, mock_executor, mock_ctx
    ):
        """sql_stream with Athena also calls _apply_athena_context"""
        mock_conn = Mock()
        mock_conn.type = "ATHENA"
        mock_resolve.return_value = mock_conn
        mock_managed = Mock()
        mock_managed.engine = Mock()
        mock_managed.engine.get_execution_options.return_value = {"connection_type": "ATHENA"}
        mock_managed.connection = None
        mock_get_or_create.return_value = mock_managed
        mock_ctx.return_value = {"catalog": "cat1", "database": "db1"}
        mock_executor.return_value.execute.return_value = iter([])

        list(sqlutils.sql_stream("SELECT 1", connection_id="c1"))
        mock_ctx.assert_called_once()

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
        mock_display.assert_called_once_with(df0)

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
        mock_display.assert_called_once_with(df0)

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
        mock_connection.type = "ATHENA"
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
        mock_sql_executor.get_supported_connection_types.return_value = ["ATHENA"]

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
        mock_connection.type = "ATHENA"
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
        mock_sql_executor.get_supported_connection_types.return_value = ["ATHENA"]

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

    @patch("sagemaker_studio.sqlutils._ensure_duckdb")
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
        mock_connection.type = "ATHENA"
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
        mock_sql_executor.get_supported_connection_types.return_value = ["ATHENA"]

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
        mock_connection.type = "ATHENA"
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
        mock_sql_executor.get_supported_connection_types.return_value = ["ATHENA"]

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
        mock_connection.type = "ATHENA"
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
        mock_sql_executor.get_supported_connection_types.return_value = ["ATHENA"]

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
        mock_connection.type = "ATHENA"
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
        mock_sql_executor.get_supported_connection_types.return_value = ["ATHENA"]

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
        mock_connection.type = "ATHENA"
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
        mock_sql_executor.get_supported_connection_types.return_value = ["ATHENA"]

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
        mock_connection.type = "ATHENA"
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
        mock_sql_executor.get_supported_connection_types.return_value = ["ATHENA"]

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

    @patch("sagemaker_studio.sqlutils._ensure_spark")
    @patch("sagemaker_studio.sqlutils._ensure_project")
    def test_sql_irc_glue_success(self, mock_ensure_project, mock_ensure_spark):
        mock_project = Mock()
        mock_conn = Mock()
        mock_conn.type = "WORKDAYICEBERGRESTCATALOG"
        mock_project.connection.return_value = mock_conn
        mock_ensure_project.return_value = mock_project

        mock_spark = Mock()
        mock_df = Mock()
        mock_df.limit.return_value.collect.return_value = [Mock()]
        mock_spark.sql.return_value = mock_df
        mock_ensure_spark.return_value = mock_spark

        result = sqlutils.sql("SELECT 1", connection_name="irc_conn")
        self.assertEqual(result, mock_df)

    @patch("sagemaker_studio.sqlutils._ensure_spark")
    @patch("sagemaker_studio.sqlutils._ensure_project")
    def test_sql_irc_glue_token_refresh_on_not_authorized(
        self, mock_ensure_project, mock_ensure_spark
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
        mock_ensure_spark.return_value = mock_spark

        result = sqlutils.sql("SELECT 1", connection_name="irc_conn")
        self.assertEqual(result, mock_df_success)
        # The stored token was rejected, so the retry must force a refresh rather
        # than re-reading the same token from the connection's secret.
        mock_conn._spark_catalog_configs.assert_called_once_with(force_token_refresh=True)
        mock_spark.conf.set.assert_any_call("spark.sql.catalog.catalog1.token", "new_token")
        mock_spark.conf.set.assert_any_call("spark.sql.catalog.catalog2.token", "new_token")

    @patch("sagemaker_studio.sqlutils._ensure_spark")
    @patch("sagemaker_studio.sqlutils._ensure_project")
    def test_sql_irc_glue_refresh_returning_none_reraises(
        self, mock_ensure_project, mock_ensure_spark
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
        mock_ensure_spark.return_value = mock_spark

        with self.assertRaises(Exception) as cm:
            sqlutils.sql("SELECT 1", connection_name="irc_conn")
        self.assertIn("NotAuthorizedException", str(cm.exception))
        mock_conn._spark_catalog_configs.assert_called_once_with(force_token_refresh=True)

    @patch("sagemaker_studio.sqlutils._ensure_spark")
    @patch("sagemaker_studio.sqlutils._ensure_project")
    def test_sql_irc_glue_non_auth_error_raises(self, mock_ensure_project, mock_ensure_spark):
        mock_project = Mock()
        mock_conn = Mock()
        mock_conn.type = "WORKDAYICEBERGRESTCATALOG"
        mock_project.connection.return_value = mock_conn
        mock_ensure_project.return_value = mock_project

        mock_spark = Mock()
        mock_df = Mock()
        type(mock_df).schema = PropertyMock(side_effect=Exception("some other error"))
        mock_spark.sql.return_value = mock_df
        mock_ensure_spark.return_value = mock_spark

        with self.assertRaises(Exception) as cm:
            sqlutils.sql("SELECT 1", connection_name="irc_conn")
        self.assertIn("some other error", str(cm.exception))

    @patch("sagemaker_studio.sqlutils._ensure_spark")
    @patch("sagemaker_studio.sqlutils._ensure_project")
    def test_sql_stream_irc_glue_success(self, mock_ensure_project, mock_ensure_spark):
        mock_project = Mock()
        mock_conn = Mock()
        mock_conn.type = "WORKDAYICEBERGRESTCATALOG"
        mock_project.connection.return_value = mock_conn
        mock_ensure_project.return_value = mock_project

        mock_spark = Mock()
        mock_df = Mock()
        mock_df.limit.return_value.collect.return_value = [Mock()]
        mock_spark.sql.return_value = mock_df
        mock_ensure_spark.return_value = mock_spark

        results = list(sqlutils.sql_stream("SELECT 1", connection_name="irc_conn"))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].status, "success")
        self.assertEqual(results[0].result, mock_df)

    @patch("sagemaker_studio.sqlutils._ensure_spark")
    @patch("sagemaker_studio.sqlutils._ensure_project")
    def test_sql_stream_irc_glue_token_refresh(self, mock_ensure_project, mock_ensure_spark):
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
        mock_ensure_spark.return_value = mock_spark

        results = list(sqlutils.sql_stream("SELECT 1", connection_name="irc_conn"))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].result, mock_df_success)
        mock_spark.conf.set.assert_called_with("spark.sql.catalog.cat1.token", "refreshed_token")


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
    @patch("sagemaker_studio.sqlutils._ensure_project")
    @patch("sagemaker_studio.sqlutils._ensure_sql_executor")
    def test_get_engine_delegates_to_get_engine_from_connection(
        self, mock_ensure_sql_executor, mock_ensure_project, mock_helper_factory
    ):
        """Test get_engine properly delegates to _get_engine_from_connection with identifiers"""
        mock_project = Mock()
        mock_conn = Mock()
        mock_conn.type = "ATHENA"
        mock_project.connection.return_value = mock_conn
        mock_ensure_project.return_value = mock_project

        mock_sql_helper = Mock()
        mock_sql_helper.to_sql_config.return_value = {"region_name": "us-east-1"}
        mock_helper_factory.get_sql_helper.return_value = mock_sql_helper

        mock_sql_executor = Mock()
        mock_ensure_sql_executor.return_value = mock_sql_executor
        mock_engine = Mock()
        mock_sql_executor.create_engine.return_value = mock_engine
        mock_sql_executor.get_supported_connection_types.return_value = ["ATHENA"]

        result = sqlutils.get_engine(connection_name="test_conn")

        # Verify connection was resolved
        mock_project.connection.assert_called_with("test_conn")

        # Verify engine was created
        self.assertEqual(result, mock_engine)

        # Verify credential_provider was passed
        call_args = mock_sql_helper.to_sql_config.call_args
        self.assertIn("credential_provider", call_args[1])


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
