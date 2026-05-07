import unittest
from datetime import datetime
from unittest.mock import Mock, patch

from dateutil.tz import tzlocal
from pandas import DataFrame

from sagemaker_studio import Connection, sqlutils
from sagemaker_studio.project import Project
from sagemaker_studio.sql_engine.sql_executor import SqlExecutor


class TestSqlutils(unittest.TestCase):

    def setUp(self):
        """Setup test fixtures"""
        self.mock_executor = Mock(spec=SqlExecutor)
        self.mock_project = Mock(spec=Project)

        # Reset global variables
        sqlutils._project = None
        sqlutils._sql_executor = SqlExecutor()

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
    @patch("sagemaker_studio.sqlutils._sql_executor")
    def test_sql_with_athena_connection(
        self, mock_sql_executor, mock_ensure_project, mock_helper_factory
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
        # Connection is called once for get_engine
        mock_project.connection.assert_called_once_with("project.athena")
        mock_helper_factory.get_sql_helper.assert_called_once_with("ATHENA")

        # Verify sql helper was called
        mock_sql_helper.to_sql_config.assert_called_once_with(self.mock_connection)

        # Verify engine creation with correct config
        mock_sql_executor.create_engine.assert_called_once()

        # Verify query execution
        mock_sql_executor.execute.assert_called_once_with(mock_engine, query, None)

        # Verify result
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(list(result["col1"]), [1, 2, 3])

    @patch("sagemaker_studio.sqlutils.HelperFactory")
    @patch("sagemaker_studio.sqlutils._ensure_project")
    @patch("sagemaker_studio.sqlutils._sql_executor")
    @patch(
        "sagemaker_studio.connections.connection.Connection._get_aws_client_with_connection_credentials"
    )
    def test_sql_with_redshift_connection(
        self, mock_get_aws_client, mock_sql_executor, mock_ensure_project, mock_helper_factory
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
        mock_sql_helper.to_sql_config.assert_called_once_with(redshift_connection)

        mock_sql_executor.create_engine.assert_called_once_with(
            "REDSHIFT", mock_sql_helper.to_sql_config.return_value
        )
        mock_sql_executor.execute.assert_called_once_with(mock_engine, query, None)

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

        # Connection is called once for get_engine
        mock_project.connection.assert_called_once_with(id="conn123")
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
    @patch("sagemaker_studio.sqlutils.get_engine")
    def test_sql_athena_injects_catalog_and_schema(self, mock_get_engine, mock_executor, mock_ctx):
        """When Athena query has catalog+database, they are passed as kwargs"""
        mock_engine = Mock()
        mock_engine.get_execution_options.return_value = {"connection_type": "ATHENA"}
        mock_get_engine.return_value = mock_engine
        mock_ctx.return_value = {"catalog": "my_cat", "database": "my_db"}
        mock_exec_result = Mock()
        mock_exec_result.result = "df"
        mock_executor.return_value.execute.return_value = iter([mock_exec_result])

        sqlutils.sql("SELECT 1", connection_id="c1")
        mock_ctx.assert_called_once()

    @patch("sagemaker_studio.utils.sql_handler.get_execution_context")
    @patch("sagemaker_studio.sqlutils._ensure_sql_executor")
    @patch("sagemaker_studio.sqlutils.get_engine")
    def test_sql_stream_athena_injects_catalog_and_schema(
        self, mock_get_engine, mock_executor, mock_ctx
    ):
        """sql_stream with Athena also calls _apply_athena_context"""
        mock_engine = Mock()
        mock_engine.get_execution_options.return_value = {"connection_type": "ATHENA"}
        mock_get_engine.return_value = mock_engine
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
        df0 = DataFrame({"a": [1]})
        df1 = DataFrame({"b": [2]})
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
        df0 = DataFrame({"a": [1]})
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
