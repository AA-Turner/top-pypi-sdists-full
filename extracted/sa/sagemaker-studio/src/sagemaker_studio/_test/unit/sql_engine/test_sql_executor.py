import unittest
from types import SimpleNamespace
from unittest.mock import Mock

import pandas as pd

from sagemaker_studio.sql_engine.database_transformer import DatabaseTransformer
from sagemaker_studio.sql_engine.resource_fetching_definition import (
    FetchMode,
    ResourceFetchingDefinition,
)
from sagemaker_studio.sql_engine.sql_executor import SqlExecutor


class TestGetResources(unittest.TestCase):
    def setUp(self):
        self.svc = SqlExecutor()
        if not hasattr(self.svc, "_transformer_classes"):
            self.svc._transformer_classes = {}
        self.engine = Mock(name="Engine")

    def _create_execution_result(
        self,
        statement="SELECT 1",
        statement_type="SELECT",
        result=None,
        error=None,
        status="success",
        statement_index=0,
    ):
        """Helper to create ExecutionResult objects"""
        from sagemaker_studio.sql_engine.sql_executor import ExecutionResult

        return ExecutionResult(
            statement_index=statement_index,
            statement=statement,
            statement_type=statement_type,
            result=result,
            error=error,
            status=status,
        )

    def _register_transformer(self, connection_type, transformer_obj):
        self.svc._transformer_classes[connection_type] = transformer_obj

    def test_unsupported_connection_type_raises(self):
        with self.assertRaises(ValueError) as cm:
            self.svc.get_resources(
                engine=self.engine,
                connection_type="unknown",
                resource_type="DATABASE",
                parents={},
            )
        self.assertIn("Unsupported connection type", str(cm.exception))

    def test_metadata_unsupported_action_raises(self):
        class Tx(DatabaseTransformer):
            @staticmethod
            def get_resources_action(resource_type, parents):
                return ResourceFetchingDefinition(
                    mode=FetchMode.SQLALCHEMY_METADATA,
                    default_type="SCHEMA",
                    children=(),
                    sqlalchemy_action=object(),
                )

        self._register_transformer("redshift", Tx)

        # Mock the inspect function to avoid SQLAlchemy inspection issues
        with unittest.mock.patch(
            "sagemaker_studio.sql_engine.sql_executor.inspect"
        ) as mock_inspect:
            mock_inspector = Mock()
            mock_inspect.return_value = mock_inspector

            with self.assertRaises(ValueError) as cm:
                self.svc.get_resources(
                    engine=self.engine,
                    connection_type="redshift",
                    resource_type="SCHEMA",
                    parents={"DATABASE": "dev"},
                )
            self.assertIn("Unsupported SQLAlchemy metadata action", str(cm.exception))

    def test_sql_execution_happy_path(self):
        class Tx(DatabaseTransformer):
            @staticmethod
            def get_resources_action(resource_type, parents):
                return ResourceFetchingDefinition.from_sql_execution(
                    "SELECT name FROM t",
                    default_type="TABLE",
                    children=("COLUMN",),
                    sql_parameters={"p": 1},
                )

        self._register_transformer("pg", Tx)
        df = pd.DataFrame({"name": ["a", "b"], "ignored": [1, 2]})
        mock_result = self._create_execution_result(statement="SELECT name FROM t", result=df)
        self.svc.execute = Mock(return_value=iter([mock_result]))

        out = self.svc.get_resources(
            engine=self.engine,
            connection_type="pg",
            resource_type=None,
            parents={},
        )
        self.svc.execute.assert_called_once_with(
            self.engine, "SELECT name FROM t", parameters={"p": 1}
        )
        self.assertEqual([r.name for r in out], ["a", "b"])
        self.assertEqual([r.type for r in out], ["TABLE", "TABLE"])
        self.assertEqual([r.children for r in out], [["COLUMN"], ["COLUMN"]])

    def test_sql_execution_empty_dataframe_yields_no_resources(self):
        class Tx(DatabaseTransformer):
            @staticmethod
            def get_resources_action(resource_type, parents):
                return ResourceFetchingDefinition.from_sql_execution(
                    "SELECT 1 WHERE 0=1",
                    default_type="DATABASE",
                    children=("SCHEMA",),
                )

        self._register_transformer("pg", Tx)
        empty_df = pd.DataFrame()
        mock_result = self._create_execution_result(statement="SELECT 1 WHERE 0=1", result=empty_df)
        self.svc.execute = Mock(return_value=iter([mock_result]))

        out = self.svc.get_resources(
            engine=self.engine,
            connection_type="pg",
            resource_type=None,
            parents={},
        )
        self.assertEqual(out, [])

    def test_unsupported_fetch_mode_raises(self):
        class Tx(DatabaseTransformer):
            @staticmethod
            def get_resources_action(resource_type, parents):
                return SimpleNamespace(
                    mode="WEIRD_MODE",
                    default_type="SCHEMA",
                    children=("TABLE",),
                    sqlalchemy_action=None,
                    sql=None,
                    sql_parameters=None,
                )

        self._register_transformer("pg", Tx)
        self.svc.execute = Mock()

        with self.assertRaises(ValueError) as cm:
            self.svc.get_resources(
                engine=self.engine,
                connection_type="pg",
                resource_type=None,
                parents={},
            )
        self.assertIn("Unsupported resource fetching mode", str(cm.exception))

    def test_sql_execution_error_result_raises(self):
        """Test that get_resources raises error when SQL execution fails"""

        class Tx(DatabaseTransformer):
            @staticmethod
            def get_resources_action(resource_type, parents):
                return ResourceFetchingDefinition.from_sql_execution(
                    "SELECT name FROM t",
                    default_type="TABLE",
                    children=("COLUMN",),
                )

        self._register_transformer("pg", Tx)
        error_result = self._create_execution_result(
            statement="SELECT name FROM t", error="Table 't' does not exist", status="error"
        )
        self.svc.execute = Mock(return_value=iter([error_result]))

        with self.assertRaises(ValueError) as cm:
            self.svc.get_resources(
                engine=self.engine,
                connection_type="pg",
                resource_type=None,
                parents={},
            )
        self.assertIn("SQL execution failed: Table 't' does not exist", str(cm.exception))


class TestGetResourcesSqlExecutionBranch(unittest.TestCase):
    """Tests specifically targeting the SQL_EXECUTION branch in get_resources."""

    def setUp(self):
        self.svc = SqlExecutor()
        if not hasattr(self.svc, "_transformer_classes"):
            self.svc._transformer_classes = {}
        self.engine = Mock(name="Engine")

    def _register_transformer(self, connection_type, transformer_obj):
        self.svc._transformer_classes[connection_type] = transformer_obj

    def test_sql_execution_stop_iteration_raises_value_error(self):
        """When execute returns an empty iterator, StopIteration should be caught
        and re-raised as ValueError."""

        class Tx(DatabaseTransformer):
            @staticmethod
            def get_resources_action(resource_type, parents):
                return ResourceFetchingDefinition.from_sql_execution(
                    "SELECT name FROM empty_table",
                    default_type="TABLE",
                    children=("COLUMN",),
                )

        self._register_transformer("pg", Tx)
        # Return an empty iterator so next() raises StopIteration
        with unittest.mock.patch.object(self.svc, "execute", return_value=iter([])):
            with self.assertRaises(ValueError) as cm:
                self.svc.get_resources(
                    engine=self.engine,
                    connection_type="pg",
                    resource_type="TABLE",
                    parents={},
                )
            self.assertIn("SQL execution returned no results", str(cm.exception))

    def test_sql_execution_failed_status_raises_value_error(self):
        """When the execution result has a non-success status, ValueError should
        be raised."""
        from sagemaker_studio.sql_engine.sql_executor import ExecutionResult

        class Tx(DatabaseTransformer):
            @staticmethod
            def get_resources_action(resource_type, parents):
                return ResourceFetchingDefinition.from_sql_execution(
                    "SELECT name FROM t",
                    default_type="TABLE",
                    children=("COLUMN",),
                )

        self._register_transformer("pg", Tx)
        error_result = ExecutionResult(
            statement_index=0,
            statement="SELECT name FROM t",
            statement_type="SELECT",
            result=None,
            error="relation 't' does not exist",
            status="error",
        )
        with unittest.mock.patch.object(self.svc, "execute", return_value=iter([error_result])):
            with self.assertRaises(ValueError) as cm:
                self.svc.get_resources(
                    engine=self.engine,
                    connection_type="pg",
                    resource_type="TABLE",
                    parents={},
                )
            self.assertIn("SQL execution failed", str(cm.exception))
            self.assertIn("relation 't' does not exist", str(cm.exception))

    def test_unsupported_fetch_mode_raises_value_error(self):
        """When the definition has an unrecognized mode, ValueError should be raised."""

        class Tx(DatabaseTransformer):
            @staticmethod
            def get_resources_action(resource_type, parents):
                return SimpleNamespace(
                    mode="UNSUPPORTED_MODE",
                    default_type="SCHEMA",
                    children=("TABLE",),
                    sqlalchemy_action=None,
                    sql=None,
                    sql_parameters=None,
                )

        self._register_transformer("pg", Tx)
        with unittest.mock.patch.object(self.svc, "execute"):
            with self.assertRaises(ValueError) as cm:
                self.svc.get_resources(
                    engine=self.engine,
                    connection_type="pg",
                    resource_type=None,
                    parents={},
                )
            self.assertIn("Unsupported resource fetching mode", str(cm.exception))

    def test_sql_execution_success_returns_resources(self):
        """Happy path for SQL_EXECUTION branch."""
        from sagemaker_studio.sql_engine.sql_executor import ExecutionResult

        class Tx(DatabaseTransformer):
            @staticmethod
            def get_resources_action(resource_type, parents):
                return ResourceFetchingDefinition.from_sql_execution(
                    "SELECT schema_name FROM information_schema.schemata",
                    default_type="SCHEMA",
                    children=("TABLE",),
                )

        self._register_transformer("pg", Tx)
        df = pd.DataFrame({"schema_name": ["public", "analytics", "staging"]})
        success_result = ExecutionResult(
            statement_index=0,
            statement="SELECT schema_name FROM information_schema.schemata",
            statement_type="SELECT",
            result=df,
            error=None,
            status="success",
        )
        with unittest.mock.patch.object(self.svc, "execute", return_value=iter([success_result])):
            out = self.svc.get_resources(
                engine=self.engine,
                connection_type="pg",
                resource_type=None,
                parents={},
            )
        self.assertEqual([r.name for r in out], ["public", "analytics", "staging"])
        self.assertEqual([r.type for r in out], ["SCHEMA", "SCHEMA", "SCHEMA"])


class TestGetResourcesMetadataBranch(unittest.TestCase):
    """Tests for the SQLALCHEMY_METADATA branch of get_resources covering
    GET_SCHEMA_NAMES, GET_TABLE_NAMES, and GET_COLUMN_NAMES actions.
    """

    def setUp(self):
        self.svc = SqlExecutor()
        if not hasattr(self.svc, "_transformer_classes"):
            self.svc._transformer_classes = {}
        self.engine = Mock(name="Engine")

    def _register_transformer(self, connection_type, transformer_obj):
        self.svc._transformer_classes[connection_type] = transformer_obj

    @unittest.mock.patch("sagemaker_studio.sql_engine.sql_executor.inspect")
    def test_get_schema_names_returns_resources(self, mock_inspect):
        """Test GET_SCHEMA_NAMES action returns schema resources."""
        from sagemaker_studio.sql_engine.resource_fetching_definition import (
            SQLAlchemyMetadataAction,
        )

        mock_inspector = Mock()
        mock_inspector.get_schema_names.return_value = ["public", "analytics"]
        mock_inspect.return_value = mock_inspector

        class Tx(DatabaseTransformer):
            @staticmethod
            def get_resources_action(resource_type, parents):
                return ResourceFetchingDefinition.from_sqlalchemy_metadata(
                    SQLAlchemyMetadataAction.GET_SCHEMA_NAMES,
                    default_type="SCHEMA",
                    children=("TABLE",),
                )

        self._register_transformer("pg", Tx)

        out = self.svc.get_resources(
            engine=self.engine,
            connection_type="pg",
            resource_type="SCHEMA",
            parents={},
        )
        self.assertEqual([r.name for r in out], ["public", "analytics"])
        self.assertEqual([r.type for r in out], ["SCHEMA", "SCHEMA"])
        mock_inspector.get_schema_names.assert_called_once()

    @unittest.mock.patch("sagemaker_studio.sql_engine.sql_executor.inspect")
    def test_get_table_names_returns_resources(self, mock_inspect):
        """Test GET_TABLE_NAMES action returns table resources."""
        from sagemaker_studio.sql_engine.resource_fetching_definition import (
            SQLAlchemyMetadataAction,
        )

        mock_inspector = Mock()
        mock_inspector.get_table_names.return_value = ["users", "orders", "products"]
        mock_inspect.return_value = mock_inspector

        class Tx(DatabaseTransformer):
            @staticmethod
            def get_resources_action(resource_type, parents):
                return ResourceFetchingDefinition.from_sqlalchemy_metadata(
                    SQLAlchemyMetadataAction.GET_TABLE_NAMES,
                    default_type="TABLE",
                    children=("COLUMN",),
                )

        self._register_transformer("pg", Tx)

        out = self.svc.get_resources(
            engine=self.engine,
            connection_type="pg",
            resource_type="TABLE",
            parents={"DATABASE": "mydb"},
        )
        self.assertEqual([r.name for r in out], ["users", "orders", "products"])
        self.assertEqual([r.type for r in out], ["TABLE", "TABLE", "TABLE"])
        mock_inspector.get_table_names.assert_called_once_with(schema="mydb")

    @unittest.mock.patch("sagemaker_studio.sql_engine.sql_executor.inspect")
    def test_get_column_names_returns_resources(self, mock_inspect):
        """Test GET_COLUMN_NAMES action returns column resources."""
        from sagemaker_studio.sql_engine.resource_fetching_definition import (
            SQLAlchemyMetadataAction,
        )

        mock_inspector = Mock()
        mock_inspector.get_columns.return_value = [
            {"name": "id", "type": "INTEGER"},
            {"name": "email", "type": "VARCHAR"},
            {"name": "created_at", "type": "TIMESTAMP"},
        ]
        mock_inspect.return_value = mock_inspector

        class Tx(DatabaseTransformer):
            @staticmethod
            def get_resources_action(resource_type, parents):
                return ResourceFetchingDefinition.from_sqlalchemy_metadata(
                    SQLAlchemyMetadataAction.GET_COLUMN_NAMES,
                    default_type="COLUMN",
                    children=(),
                )

        self._register_transformer("pg", Tx)

        out = self.svc.get_resources(
            engine=self.engine,
            connection_type="pg",
            resource_type="COLUMN",
            parents={"DATABASE": "mydb", "TABLE": "users"},
        )
        self.assertEqual([r.name for r in out], ["id", "email", "created_at"])
        self.assertEqual([r.type for r in out], ["COLUMN", "COLUMN", "COLUMN"])
        mock_inspector.get_columns.assert_called_once_with(table_name="users", schema="mydb")


class TestMultiStatementExecution(unittest.TestCase):
    def setUp(self):
        self.executor = SqlExecutor()
        self.mock_engine = Mock()
        self.mock_connection = Mock()
        # Create a proper context manager mock
        self.mock_engine.connect.return_value = Mock()
        self.mock_engine.connect.return_value.__enter__ = Mock(return_value=self.mock_connection)
        self.mock_engine.connect.return_value.__exit__ = Mock(return_value=None)
        self.mock_engine.get_execution_options.return_value = {"connection_type": "REDSHIFT"}

    def test_execute_statements_single_statement_success(self):
        """Test successful execution of single statement"""
        from sagemaker_studio.sql_engine.database_transformer import SqlStatement

        statements = [SqlStatement("SELECT 1", "SELECT")]
        executor_func = Mock(return_value=pd.DataFrame({"col": [1]}))

        results = list(SqlExecutor.execute_statements(statements, executor_func))

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].statement_index, 0)
        self.assertEqual(results[0].statement, "SELECT 1")
        self.assertEqual(results[0].statement_type, "SELECT")
        self.assertEqual(results[0].status, "success")
        self.assertIsNotNone(results[0].result)
        self.assertIsNone(results[0].error)

    def test_execute_statements_multiple_statements_success(self):
        """Test successful execution of multiple statements"""
        from sagemaker_studio.sql_engine.database_transformer import SqlStatement

        statements = [
            SqlStatement("SELECT 1", "SELECT"),
            SqlStatement("SELECT 2", "SELECT"),
            SqlStatement("INSERT INTO t VALUES (1)", "INSERT"),
        ]
        executor_func = Mock(
            side_effect=[
                pd.DataFrame({"col": [1]}),
                pd.DataFrame({"col": [2]}),
                5,  # row count for INSERT
            ]
        )

        results = list(SqlExecutor.execute_statements(statements, executor_func))

        self.assertEqual(len(results), 3)
        for i, result in enumerate(results):
            self.assertEqual(result.statement_index, i)
            self.assertEqual(result.status, "success")
            self.assertIsNone(result.error)

    def test_execute_statements_stop_on_error(self):
        """Test stop_on_error strategy stops execution on first error"""
        from sagemaker_studio.sql_engine.database_transformer import SqlStatement
        from sagemaker_studio.sql_engine.sql_executor import ErrorStrategy

        statements = [
            SqlStatement("SELECT 1", "SELECT"),
            SqlStatement("INVALID SQL", "UNKNOWN"),
            SqlStatement("SELECT 3", "SELECT"),
        ]
        executor_func = Mock(
            side_effect=[
                pd.DataFrame({"col": [1]}),
                Exception("Syntax error"),
                pd.DataFrame({"col": [3]}),
            ]
        )

        results = list(
            SqlExecutor.execute_statements(statements, executor_func, ErrorStrategy.STOP_ON_ERROR)
        )

        self.assertEqual(len(results), 2)  # Should stop after error
        self.assertEqual(results[0].status, "success")
        self.assertEqual(results[1].status, "error")
        self.assertEqual(results[1].error, "Syntax error")

    def test_execute_statements_continue_on_error(self):
        """Test continue_on_error strategy continues execution after errors"""
        from sagemaker_studio.sql_engine.database_transformer import SqlStatement
        from sagemaker_studio.sql_engine.sql_executor import ErrorStrategy

        statements = [
            SqlStatement("SELECT 1", "SELECT"),
            SqlStatement("INVALID SQL", "UNKNOWN"),
            SqlStatement("SELECT 3", "SELECT"),
        ]
        executor_func = Mock(
            side_effect=[
                pd.DataFrame({"col": [1]}),
                Exception("Syntax error"),
                pd.DataFrame({"col": [3]}),
            ]
        )

        results = list(
            SqlExecutor.execute_statements(
                statements, executor_func, ErrorStrategy.CONTINUE_ON_ERROR
            )
        )

        self.assertEqual(len(results), 3)  # Should execute all statements
        self.assertEqual(results[0].status, "success")
        self.assertEqual(results[1].status, "error")
        self.assertEqual(results[2].status, "success")

    def test_execute_statements_max_statements_limit(self):
        """Test that MAX_STATEMENTS limit is enforced"""
        from sagemaker_studio.sql_engine.database_transformer import SqlStatement

        statements = [SqlStatement(f"SELECT {i}", "SELECT") for i in range(11)]
        executor_func = Mock()

        with self.assertRaises(ValueError) as cm:
            list(SqlExecutor.execute_statements(statements, executor_func))

        self.assertIn("Too many statements: 11", str(cm.exception))
        self.assertIn("Maximum allowed: 10", str(cm.exception))

    def test_execute_method_single_statement(self):
        """Test execute method with single statement"""
        mock_transformer = Mock()
        mock_transformer.split_query.return_value = [
            Mock(statement="SELECT 1", statement_type="SELECT")
        ]
        mock_transformer.get_loggers.return_value = []  # Return empty list for loggers
        self.executor._transformer_classes = {"REDSHIFT": mock_transformer}

        # Mock connection.execute to return a result with rows
        mock_result = Mock()
        mock_result.returns_rows = True
        mock_result.fetchall.return_value = [(1,)]
        mock_result.keys.return_value = ["col"]
        self.mock_connection.execute.return_value = mock_result

        results = list(self.executor.execute(self.mock_engine, "SELECT 1"))

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].status, "success")
        self.assertIsInstance(results[0].result, pd.DataFrame)

    def test_execute_method_multiple_statements(self):
        """Test execute method with multiple statements"""
        mock_transformer = Mock()
        mock_transformer.split_query.return_value = [
            Mock(statement="SELECT 1", statement_type="SELECT"),
            Mock(statement="SELECT 2", statement_type="SELECT"),
        ]
        mock_transformer.get_loggers.return_value = []  # Return empty list for loggers
        self.executor._transformer_classes = {"REDSHIFT": mock_transformer}

        # Mock connection.execute to return results with rows
        mock_result1 = Mock()
        mock_result1.returns_rows = True
        mock_result1.fetchall.return_value = [(1,)]
        mock_result1.keys.return_value = ["col"]

        mock_result2 = Mock()
        mock_result2.returns_rows = True
        mock_result2.fetchall.return_value = [(2,)]
        mock_result2.keys.return_value = ["col"]

        self.mock_connection.execute.side_effect = [mock_result1, mock_result2]

        results = list(self.executor.execute(self.mock_engine, "SELECT 1; SELECT 2"))

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].status, "success")
        self.assertEqual(results[1].status, "success")

    def test_execute_method_with_parameters(self):
        """Test execute method with parameters"""
        mock_transformer = Mock()
        mock_transformer.split_query.return_value = [
            Mock(statement="SELECT :param", statement_type="SELECT")
        ]
        mock_transformer.get_loggers.return_value = []  # Return empty list for loggers
        self.executor._transformer_classes = {"REDSHIFT": mock_transformer}

        mock_result = Mock()
        mock_result.returns_rows = True
        mock_result.fetchall.return_value = [(42,)]
        mock_result.keys.return_value = ["col"]
        self.mock_connection.execute.return_value = mock_result

        parameters = {"param": 42}
        results = list(
            self.executor.execute(self.mock_engine, "SELECT :param", parameters=parameters)
        )

        self.assertEqual(len(results), 1)
        self.mock_connection.execute.assert_called_with(unittest.mock.ANY, parameters)

    def test_execute_method_dml_statement(self):
        """Test execute method with DML statement (returns row count)"""
        mock_transformer = Mock()
        mock_transformer.split_query.return_value = [
            Mock(statement="INSERT INTO t VALUES (1)", statement_type="INSERT")
        ]
        mock_transformer.get_loggers.return_value = []  # Return empty list for loggers
        self.executor._transformer_classes = {"REDSHIFT": mock_transformer}

        # Mock connection.execute to return a result without rows
        mock_result = Mock()
        mock_result.returns_rows = False
        mock_result.rowcount = 5
        self.mock_connection.execute.return_value = mock_result

        results = list(self.executor.execute(self.mock_engine, "INSERT INTO t VALUES (1)"))

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].status, "success")
        self.assertEqual(results[0].result, 5)  # Should return row count

    def test_execute_method_with_error_strategy(self):
        """Test execute method with different error strategies"""
        from sagemaker_studio.sql_engine.sql_executor import ErrorStrategy

        mock_transformer = Mock()
        mock_transformer.split_query.return_value = [
            Mock(statement="SELECT 1", statement_type="SELECT"),
            Mock(statement="INVALID", statement_type="UNKNOWN"),
        ]
        mock_transformer.get_loggers.return_value = []  # Return empty list for loggers
        self.executor._transformer_classes = {"REDSHIFT": mock_transformer}

        # First call succeeds, second fails
        mock_result = Mock()
        mock_result.returns_rows = True
        mock_result.fetchall.return_value = [(1,)]
        mock_result.keys.return_value = ["col"]

        self.mock_connection.execute.side_effect = [mock_result, Exception("Syntax error")]

        results = list(
            self.executor.execute(
                self.mock_engine,
                "SELECT 1; INVALID",
                error_strategy=ErrorStrategy.CONTINUE_ON_ERROR,
            )
        )

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].status, "success")
        self.assertEqual(results[1].status, "error")

    def test_execution_result_dataclass(self):
        """Test ExecutionResult dataclass structure"""
        from sagemaker_studio.sql_engine.sql_executor import ExecutionResult

        result = ExecutionResult(
            statement_index=0,
            statement="SELECT 1",
            statement_type="SELECT",
            result=pd.DataFrame({"col": [1]}),
            status="success",
        )

        self.assertEqual(result.statement_index, 0)
        self.assertEqual(result.statement, "SELECT 1")
        self.assertEqual(result.statement_type, "SELECT")
        self.assertEqual(result.status, "success")
        self.assertIsNone(result.error)
        self.assertIsNone(result.rows_affected)
        self.assertIsNone(result.execution_time)

    def test_execute_with_sqlalchemy_error_propagation(self):
        """Test that SQLAlchemy errors are properly propagated"""
        from sqlalchemy.exc import SQLAlchemyError

        mock_transformer = Mock()
        mock_transformer.split_query.return_value = [
            Mock(statement="SELECT 1", statement_type="SELECT")
        ]
        mock_transformer.get_loggers.return_value = []  # Return empty list for loggers
        self.executor._transformer_classes = {"REDSHIFT": mock_transformer}

        # Mock engine.connect to raise SQLAlchemyError
        self.mock_engine.connect.side_effect = SQLAlchemyError("Connection failed")

        with self.assertRaises(SQLAlchemyError):
            list(self.executor.execute(self.mock_engine, "SELECT 1"))

    def test_execute_empty_query(self):
        """Test execute with empty query"""
        mock_transformer = Mock()
        mock_transformer.split_query.return_value = []
        mock_transformer.get_loggers.return_value = []  # Return empty list for loggers
        self.executor._transformer_classes = {"REDSHIFT": mock_transformer}

        results = list(self.executor.execute(self.mock_engine, ""))

        self.assertEqual(len(results), 0)

    def test_execute_with_unknown_connection_type(self):
        """Test execute with unknown connection type"""
        self.mock_engine.get_execution_options.return_value = {"connection_type": "UNKNOWN_DB"}

        with self.assertRaises(ValueError) as cm:
            list(self.executor.execute(self.mock_engine, "SELECT 1"))

        self.assertIn("Unsupported connection type: UNKNOWN_DB", str(cm.exception))


class TestExecuteWithOptionalConnection(unittest.TestCase):
    """Test suite for execute method with optional connection parameter"""

    def setUp(self):
        self.executor = SqlExecutor()
        self.mock_engine = Mock()
        self.mock_auto_connection = Mock()
        self.mock_provided_connection = Mock()

        # Setup auto-managed connection (context manager)
        self.mock_engine.connect.return_value = Mock()
        self.mock_engine.connect.return_value.__enter__ = Mock(
            return_value=self.mock_auto_connection
        )
        self.mock_engine.connect.return_value.__exit__ = Mock(return_value=None)
        self.mock_engine.get_execution_options.return_value = {"connection_type": "REDSHIFT"}

        # Setup transformer
        self.mock_transformer = Mock()
        self.mock_transformer.split_query.return_value = [
            Mock(statement="SELECT 1", statement_type="SELECT")
        ]
        self.mock_transformer.get_loggers.return_value = []
        self.executor._transformer_classes = {"REDSHIFT": self.mock_transformer}

    def test_execute_without_connection_creates_and_closes_connection(self):
        """Test that execute without connection parameter creates and auto-closes connection"""
        mock_result = Mock()
        mock_result.returns_rows = True
        mock_result.fetchall.return_value = [(1,)]
        mock_result.keys.return_value = ["col"]
        self.mock_auto_connection.execute.return_value = mock_result

        results = list(self.executor.execute(self.mock_engine, "SELECT 1"))

        # Verify connection was created via context manager
        self.mock_engine.connect.assert_called_once()
        # Verify __enter__ and __exit__ were called (context manager protocol)
        self.mock_engine.connect.return_value.__enter__.assert_called_once()
        self.mock_engine.connect.return_value.__exit__.assert_called_once()
        # Verify query was executed on auto-managed connection
        self.mock_auto_connection.execute.assert_called_once()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].status, "success")

    def test_execute_with_connection_uses_provided_connection(self):
        """Test that execute with connection parameter uses provided connection"""
        mock_result = Mock()
        mock_result.returns_rows = True
        mock_result.fetchall.return_value = [(1,)]
        mock_result.keys.return_value = ["col"]
        self.mock_provided_connection.execute.return_value = mock_result

        results = list(
            self.executor.execute(
                self.mock_engine, "SELECT 1", connection=self.mock_provided_connection
            )
        )

        # Verify engine.connect was NOT called (no auto-managed connection)
        self.mock_engine.connect.assert_not_called()
        # Verify query was executed on provided connection
        self.mock_provided_connection.execute.assert_called_once()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].status, "success")

    def test_execute_with_connection_does_not_close_connection(self):
        """Test that provided connection is not closed by execute method"""
        mock_result = Mock()
        mock_result.returns_rows = True
        mock_result.fetchall.return_value = [(1,)]
        mock_result.keys.return_value = ["col"]
        self.mock_provided_connection.execute.return_value = mock_result
        self.mock_provided_connection.close = Mock()

        list(
            self.executor.execute(
                self.mock_engine, "SELECT 1", connection=self.mock_provided_connection
            )
        )

        # Verify connection.close was NOT called
        self.mock_provided_connection.close.assert_not_called()

    def test_execute_with_connection_multiple_statements(self):
        """Test persistent connection with multiple statements"""
        self.mock_transformer.split_query.return_value = [
            Mock(statement="CREATE TEMP TABLE t (id INT)", statement_type="CREATE"),
            Mock(statement="INSERT INTO t VALUES (1)", statement_type="INSERT"),
            Mock(statement="SELECT * FROM t", statement_type="SELECT"),
        ]

        # Mock results for each statement
        create_result = Mock(returns_rows=False, rowcount=0)
        insert_result = Mock(returns_rows=False, rowcount=1)
        select_result = Mock(returns_rows=True)
        select_result.fetchall.return_value = [(1,)]
        select_result.keys.return_value = ["id"]

        self.mock_provided_connection.execute.side_effect = [
            create_result,
            insert_result,
            select_result,
        ]

        results = list(
            self.executor.execute(
                self.mock_engine,
                "CREATE TEMP TABLE t (id INT); INSERT INTO t VALUES (1); SELECT * FROM t",
                connection=self.mock_provided_connection,
            )
        )

        # Verify all statements executed on same connection
        self.assertEqual(self.mock_provided_connection.execute.call_count, 3)
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0].statement_type, "CREATE")
        self.assertEqual(results[1].statement_type, "INSERT")
        self.assertEqual(results[2].statement_type, "SELECT")
        # Verify connection not closed
        self.mock_engine.connect.assert_not_called()

    def test_execute_with_connection_and_parameters(self):
        """Test provided connection with parameterized query"""
        mock_result = Mock()
        mock_result.returns_rows = True
        mock_result.fetchall.return_value = [(42,)]
        mock_result.keys.return_value = ["value"]
        self.mock_provided_connection.execute.return_value = mock_result

        parameters = {"param": 42}
        results = list(
            self.executor.execute(
                self.mock_engine,
                "SELECT :param",
                connection=self.mock_provided_connection,
                parameters=parameters,
            )
        )

        # Verify parameters were passed to execute
        self.mock_provided_connection.execute.assert_called_once()
        call_args = self.mock_provided_connection.execute.call_args
        self.assertEqual(call_args[0][1], parameters)
        self.assertEqual(len(results), 1)

    def test_execute_with_connection_and_error_strategy(self):
        """Test provided connection with error strategy"""
        from sagemaker_studio.sql_engine.sql_executor import ErrorStrategy

        self.mock_transformer.split_query.return_value = [
            Mock(statement="SELECT 1", statement_type="SELECT"),
            Mock(statement="INVALID", statement_type="UNKNOWN"),
            Mock(statement="SELECT 3", statement_type="SELECT"),
        ]

        mock_result1 = Mock(returns_rows=True)
        mock_result1.fetchall.return_value = [(1,)]
        mock_result1.keys.return_value = ["col"]

        mock_result3 = Mock(returns_rows=True)
        mock_result3.fetchall.return_value = [(3,)]
        mock_result3.keys.return_value = ["col"]

        self.mock_provided_connection.execute.side_effect = [
            mock_result1,
            Exception("Syntax error"),
            mock_result3,
        ]

        results = list(
            self.executor.execute(
                self.mock_engine,
                "SELECT 1; INVALID; SELECT 3",
                connection=self.mock_provided_connection,
                error_strategy=ErrorStrategy.CONTINUE_ON_ERROR,
            )
        )

        # Verify all statements attempted on same connection
        self.assertEqual(self.mock_provided_connection.execute.call_count, 3)
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0].status, "success")
        self.assertEqual(results[1].status, "error")
        self.assertEqual(results[2].status, "success")

    def test_execute_connection_parameter_none_vs_not_provided(self):
        """Test that connection=None behaves same as not providing connection"""
        mock_result = Mock()
        mock_result.returns_rows = True
        mock_result.fetchall.return_value = [(1,)]
        mock_result.keys.return_value = ["col"]
        self.mock_auto_connection.execute.return_value = mock_result

        # Test with connection=None explicitly
        results1 = list(self.executor.execute(self.mock_engine, "SELECT 1", connection=None))

        # Reset mocks
        self.mock_engine.connect.reset_mock()
        self.mock_auto_connection.execute.reset_mock()

        # Test without connection parameter
        results2 = list(self.executor.execute(self.mock_engine, "SELECT 1"))

        # Both should create auto-managed connection
        self.assertEqual(len(results1), 1)
        self.assertEqual(len(results2), 1)
        # Verify engine.connect was called both times
        self.assertEqual(
            self.mock_engine.connect.call_count, 1
        )  # Only second call counted after reset

    def test_execute_with_connection_error_wrapped_in_execution_result(self):
        """Test that errors with provided connection are wrapped in ExecutionResult"""
        self.mock_provided_connection.execute.side_effect = Exception("Database error")

        results = list(
            self.executor.execute(
                self.mock_engine,
                "SELECT 1",
                connection=self.mock_provided_connection,
            )
        )

        # Error should be wrapped in ExecutionResult, not raised
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].status, "error")
        self.assertIn("Database error", results[0].error)
        # Verify connection was not closed by executor
        self.mock_engine.connect.assert_not_called()


class TestCreateEngine(unittest.TestCase):
    """Test suite for SqlExecutor.create_engine method."""

    def setUp(self):
        self.executor = SqlExecutor()

    @unittest.mock.patch("sagemaker_studio.sql_engine.sql_executor.create_engine")
    def test_create_engine_with_creator_uses_engine_kwargs(self, mock_create_engine):
        """Test that all config keys (except connection_string) are passed to create_engine."""
        from sqlalchemy.pool import NullPool

        mock_engine = Mock()
        mock_engine.execution_options.return_value = mock_engine
        mock_create_engine.return_value = mock_engine

        mock_transformer = Mock()
        mock_transformer.to_sqlalchemy_config.return_value = {
            "connection_string": "oracle+oracledb://@",
            "creator": lambda: Mock(),
            "poolclass": NullPool,
            "isolation_level": "AUTOCOMMIT",
            "thick_mode": False,
        }
        mock_transformer.get_loggers.return_value = []
        self.executor._transformer_classes = {"ORACLE": mock_transformer}

        result = self.executor.create_engine("ORACLE", {})

        mock_create_engine.assert_called_once()
        call_args = mock_create_engine.call_args
        assert call_args[0][0] == "oracle+oracledb://@"
        call_kwargs = call_args[1]
        assert call_kwargs["poolclass"] is NullPool
        assert call_kwargs["isolation_level"] == "AUTOCOMMIT"
        assert call_kwargs["thick_mode"] is False
        assert "creator" in call_kwargs
        assert "connection_string" not in call_kwargs
        assert result is mock_engine

    @unittest.mock.patch("sagemaker_studio.sql_engine.sql_executor.create_engine")
    def test_create_engine_without_creator_uses_connect_args(self, mock_create_engine):
        """Test that non-creator config passes connect_args to create_engine."""
        mock_engine = Mock()
        mock_engine.execution_options.return_value = mock_engine
        mock_create_engine.return_value = mock_engine

        mock_transformer = Mock()
        mock_transformer.to_sqlalchemy_config.return_value = {
            "connection_string": "mysql+pymysql://user@host/db",
            "connect_args": {"timeout": 30},
        }
        mock_transformer.get_loggers.return_value = []
        self.executor._transformer_classes = {"MYSQL": mock_transformer}

        result = self.executor.create_engine("MYSQL", {})

        mock_create_engine.assert_called_once_with(
            "mysql+pymysql://user@host/db", connect_args={"timeout": 30}
        )
        assert result is mock_engine

    def test_create_engine_missing_connection_string_raises(self):
        """Test that missing connection_string raises ValueError."""
        mock_transformer = Mock()
        mock_transformer.to_sqlalchemy_config.return_value = {"creator": lambda: Mock()}
        mock_transformer.get_loggers.return_value = []
        self.executor._transformer_classes = {"ORACLE": mock_transformer}

        with self.assertRaises(ValueError) as cm:
            self.executor.create_engine("ORACLE", {})

        self.assertIn("must return 'connection_string'", str(cm.exception))

    @unittest.mock.patch(
        "sagemaker_studio.sql_engine.teradata_transformer._TERADATA_DEPS_AVAILABLE", True
    )
    @unittest.mock.patch("sagemaker_studio.sql_engine.sql_executor._TERADATA_AVAILABLE", True)
    @unittest.mock.patch("sagemaker_studio.sql_engine.sql_executor.create_engine")
    def test_create_engine_for_teradata_uses_connect_args(self, mock_create_engine):
        """Test that TERADATA create_engine passes connect_args with dbs_port and sslmode."""
        mock_engine = Mock()
        mock_engine.execution_options.return_value = mock_engine
        mock_create_engine.return_value = mock_engine

        connection_data = {
            "host": "teradata.example.com",
            "port": 1025,
            "database": "analytics",
            "user": "dbadmin",
            "password": "secret123",
        }

        # Re-create executor so it picks up the patched _TERADATA_AVAILABLE
        executor = SqlExecutor()
        result = executor.create_engine("TERADATA", connection_data)

        # Verify URL.create() was used (connection_string is a URL object)
        call_args = mock_create_engine.call_args
        url_arg = call_args[0][0]
        from sqlalchemy.engine import URL

        assert isinstance(url_arg, URL)
        assert url_arg.drivername == "teradatasql"
        assert url_arg.username == "dbadmin"
        assert url_arg.password == "secret123"
        assert url_arg.host == "teradata.example.com"
        assert url_arg.query == {"database": "analytics"}
        # Verify connect_args includes dbs_port and TLS enforcement
        assert call_args[1]["connect_args"] == {"dbs_port": 1025, "sslmode": "REQUIRE"}
        assert result is mock_engine

    def test_create_engine_unsupported_type_raises(self):
        """Test that unsupported connection type raises ValueError."""
        with self.assertRaises(ValueError) as cm:
            self.executor.create_engine("UNSUPPORTED_DB", {})

        self.assertIn("Unsupported connection type", str(cm.exception))


class TestExecuteSingleMetadataExtraction(unittest.TestCase):
    """Tests for _execute_single extracting metadata before fetchall."""

    def setUp(self):
        self.executor = SqlExecutor()

    def test_extracts_metadata_from_cursor(self):
        """_execute_single returns SingleStatementResult with metadata."""
        from sagemaker_studio.sql_engine.sql_executor import SingleStatementResult

        mock_cursor = Mock()
        mock_cursor.get_execution_metadata.return_value = {"statement_id": "test-123"}

        mock_result = Mock()
        mock_result.cursor = mock_cursor
        mock_result.returns_rows = True
        mock_result.fetchall.return_value = [(1, "a")]
        mock_result.keys.return_value = ["id", "name"]

        mock_connection = Mock()
        mock_connection.execute.return_value = mock_result
        mock_connection.engine.get_execution_options.return_value = {"connection_type": "REDSHIFT"}

        result = self.executor._execute_single(mock_connection, "SELECT 1")

        self.assertIsInstance(result, SingleStatementResult)
        self.assertEqual(result.execution_metadata, {"statement_id": "test-123"})
        self.assertEqual(list(result.result.columns), ["id", "name"])

    def test_metadata_none_when_transformer_has_no_support(self):
        """For engines without get_execution_metadata, returns None metadata."""
        from sagemaker_studio.sql_engine.sql_executor import SingleStatementResult

        mock_result = Mock()
        mock_result.cursor = Mock(spec=[])  # no get_execution_metadata
        mock_result.returns_rows = False
        mock_result.rowcount = 5

        mock_connection = Mock()
        mock_connection.execute.return_value = mock_result
        mock_connection.engine.get_execution_options.return_value = {"connection_type": "MYSQL"}

        result = self.executor._execute_single(mock_connection, "INSERT INTO t VALUES (1)")

        self.assertIsInstance(result, SingleStatementResult)
        self.assertIsNone(result.execution_metadata)
        self.assertEqual(result.result, 5)


class TestExecuteStatementsMetadata(unittest.TestCase):
    """Tests for execute_statements passing through metadata from executor_func."""

    def test_passes_metadata_from_single_statement_result(self):
        from sagemaker_studio.sql_engine.database_transformer import SqlStatement
        from sagemaker_studio.sql_engine.sql_executor import SingleStatementResult

        statements = [SqlStatement(statement="SELECT 1", statement_type="SELECT")]
        metadata = {"statement_id": "xyz", "result_rows": 10}

        def executor_func(stmt):
            return SingleStatementResult(
                result=pd.DataFrame({"a": [1]}), execution_metadata=metadata
            )

        results = list(SqlExecutor.execute_statements(statements, executor_func))

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].execution_metadata, metadata)
        self.assertEqual(results[0].status, "success")

    def test_plain_result_has_none_metadata(self):
        from sagemaker_studio.sql_engine.database_transformer import SqlStatement

        statements = [SqlStatement(statement="SELECT 1", statement_type="SELECT")]

        def executor_func(stmt):
            return pd.DataFrame({"a": [1]})  # plain result, no metadata

        results = list(SqlExecutor.execute_statements(statements, executor_func))

        self.assertEqual(len(results), 1)
        self.assertIsNone(results[0].execution_metadata)

    def test_error_result_has_no_metadata(self):
        from sagemaker_studio.sql_engine.database_transformer import SqlStatement

        statements = [SqlStatement(statement="BAD SQL", statement_type="SELECT")]

        def executor_func(stmt):
            raise RuntimeError("syntax error")

        results = list(SqlExecutor.execute_statements(statements, executor_func))

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].status, "error")
        self.assertEqual(results[0].error, "syntax error")
        self.assertIsNone(results[0].execution_metadata)


class TestTeradataAvailability(unittest.TestCase):
    """Tests for SqlExecutor behavior when Teradata packages are not available."""

    @unittest.mock.patch("sagemaker_studio.sql_engine.sql_executor._TERADATA_AVAILABLE", False)
    def test_teradata_not_in_supported_types_when_unavailable(self):
        """Test that TERADATA is not listed in supported types when packages are missing."""
        executor = SqlExecutor()
        supported = executor.get_supported_connection_types()
        self.assertNotIn("TERADATA", supported)

    @unittest.mock.patch("sagemaker_studio.sql_engine.sql_executor._TERADATA_AVAILABLE", False)
    def test_get_transformer_raises_import_error_for_teradata_when_unavailable(self):
        """Test that _get_transformer raises ImportError for TERADATA when packages are missing."""
        executor = SqlExecutor()
        with self.assertRaises(ImportError) as cm:
            executor._get_transformer("TERADATA")
        self.assertIn("teradatasql", str(cm.exception))


class TestSqlExecutorTeradataModuleImport(unittest.TestCase):
    """Tests that cover module-level import behavior of sql_executor.py."""

    def test_module_sets_teradata_unavailable_when_import_fails(self):
        """Test that _TERADATA_AVAILABLE is False when teradata_transformer import fails.

        This covers the except ImportError branch in sql_executor.py.
        """
        import importlib
        import sys

        import sagemaker_studio.sql_engine.sql_executor as se_module

        transformer_module_name = "sagemaker_studio.sql_engine.teradata_transformer"
        original_transformer = sys.modules.get(transformer_module_name)
        original_teradatasql = sys.modules.get("teradatasql")
        original_teradatasqlalchemy = sys.modules.get("teradatasqlalchemy")

        try:
            # Remove the teradata_transformer module from cache AND make it
            # fail on reimport by poisoning the teradatasql dependency.
            # Setting a module to None in sys.modules causes ImportError on import.
            sys.modules[transformer_module_name] = None
            sys.modules["teradatasql"] = None

            # Reload sql_executor so module-level try/except re-executes
            importlib.reload(se_module)

            self.assertFalse(se_module._TERADATA_AVAILABLE)
        finally:
            # Restore original state
            if original_teradatasql is not None:
                sys.modules["teradatasql"] = original_teradatasql
            else:
                sys.modules.pop("teradatasql", None)
            if original_teradatasqlalchemy is not None:
                sys.modules["teradatasqlalchemy"] = original_teradatasqlalchemy
            else:
                sys.modules.pop("teradatasqlalchemy", None)
            if original_transformer is not None:
                sys.modules[transformer_module_name] = original_transformer
            else:
                sys.modules.pop(transformer_module_name, None)
            # Reload to restore normal state
            importlib.reload(se_module)
