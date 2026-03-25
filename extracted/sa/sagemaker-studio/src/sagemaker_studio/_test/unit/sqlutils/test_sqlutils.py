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
