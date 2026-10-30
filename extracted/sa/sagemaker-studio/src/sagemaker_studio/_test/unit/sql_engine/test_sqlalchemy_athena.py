import unittest
from types import SimpleNamespace
from unittest import mock

from pandas import DataFrame
from sqlalchemy import inspect, text
from sqlalchemy.engine import make_url

from sagemaker_studio.sql_engine._sqlalchemy_athena import dbapi
from sagemaker_studio.sql_engine._sqlalchemy_athena.dialect import AthenaDialect
from sagemaker_studio.sql_engine.sql_executor import SingleStatementResult, SqlExecutor
from sagemaker_studio.utils.athena_v4 import AthenaQueryError, AthenaV4Executor


class TestSqlAlchemyEngine(unittest.TestCase):
    def _executor(self):
        executor = mock.Mock()
        executor.execution_parameters = None
        executor.catalog = "AwsDataCatalog"
        executor.schema = "analytics"
        executor.work_group = "wg"
        executor.execute.return_value = SingleStatementResult(
            result=DataFrame({"id": [1, 2], "name": ["a", "b"]}),
            execution_metadata={"query_execution_id": "q-1", "data_scanned_bytes": 42},
        )
        return executor

    def test_get_engine_contract_executes_and_returns_rows(self):
        native = self._executor()
        with mock.patch.object(dbapi, "_executor_from_config", return_value=native):
            engine = SqlExecutor().create_engine(
                "ATHENA",
                {"region": "us-west-2", "work_group": "wg", "schema_name": "analytics"},
            )
            with engine.connect() as connection:
                rows = connection.execute(text("SELECT :id"), {"id": 1}).fetchall()

        self.assertEqual(rows, [(1, "a"), (2, "b")])
        native.execute.assert_called_once_with("SELECT :id")
        self.assertIsNone(native.execution_parameters)

    def test_pandas_read_sql_compatible_result_shape(self):
        import pandas as pd

        native = self._executor()
        with mock.patch.object(dbapi, "_executor_from_config", return_value=native):
            engine = SqlExecutor().create_engine(
                "ATHENA", {"region": "us-west-2", "work_group": "wg"}
            )
            frame = pd.read_sql("SELECT id, name FROM t", engine)

        self.assertEqual(frame.to_dict("records"), [{"id": 1, "name": "a"}, {"id": 2, "name": "b"}])

    def test_inspector_uses_native_metadata_apis(self):
        native = self._executor()
        native.get_resources.return_value = [SimpleNamespace(name="analytics")]
        page_one = {
            "TableMetadataList": [
                {"Name": "orders", "TableType": "EXTERNAL_TABLE"},
                {"Name": "report", "TableType": "VIRTUAL_VIEW"},
            ],
            "NextToken": "next",
        }
        page_two = {"TableMetadataList": [{"Name": "managed", "TableType": "MANAGED_TABLE"}]}
        native.client.list_table_metadata.side_effect = [
            page_one,
            page_two,
            page_one,
            page_two,
        ]
        native.client.get_table_metadata.return_value = {
            "TableMetadata": {
                "Columns": [
                    {"Name": "id", "Type": "bigint", "Comment": "identifier"},
                    {"Name": "amount", "Type": "decimal(10,2)"},
                ],
                "PartitionKeys": [{"Name": "day", "Type": "date"}],
            }
        }
        with mock.patch.object(dbapi, "_executor_from_config", return_value=native):
            engine = SqlExecutor().create_engine(
                "ATHENA",
                {"region": "us-west-2", "work_group": "wg", "schema_name": "analytics"},
            )
            inspector = inspect(engine)
            self.assertEqual(inspector.get_schema_names(), ["analytics"])
            self.assertEqual(inspector.get_table_names(schema="analytics"), ["orders", "managed"])
            self.assertEqual(inspector.get_view_names(schema="analytics"), ["report"])
            columns = inspector.get_columns("orders", schema="analytics")

        self.assertEqual([column["name"] for column in columns], ["id", "amount", "day"])
        self.assertEqual(columns[0]["comment"], "identifier")
        self.assertTrue(columns[2]["dialect_options"]["awsathena_partition"])


class TestDBAPI(unittest.TestCase):
    def setUp(self):
        self.executor = mock.Mock(spec=AthenaV4Executor)
        self.executor.execution_parameters = None
        self.executor.catalog = None
        self.executor.schema = None
        self.executor.work_group = "wg"
        patcher = mock.patch.object(dbapi, "_executor_from_config", return_value=self.executor)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.connection = dbapi.Connection(work_group="wg", region="us-west-2")

    def test_connection_lifecycle(self):
        cursor = self.connection.cursor()
        self.connection.commit()
        self.connection.rollback()
        self.connection.close()
        with self.assertRaisesRegex(dbapi.InterfaceError, "Connection is closed"):
            self.connection.cursor()
        with self.assertRaisesRegex(dbapi.InterfaceError, "Connection is closed"):
            self.connection.commit()
        with self.assertRaisesRegex(dbapi.InterfaceError, "Connection is closed"):
            self.connection.rollback()
        self.assertIsInstance(cursor, dbapi.Cursor)

    def test_cursor_fetch_lifecycle_and_metadata(self):
        self.executor.execute.return_value = SingleStatementResult(
            result=DataFrame({"id": [1, 2, 3]}),
            execution_metadata={"query_execution_id": "q-1"},
        )
        cursor = self.connection.cursor()
        self.assertIs(cursor.execute("SELECT :id", {"id": 1}), cursor)
        self.assertEqual(cursor.query_id, "q-1")
        self.assertEqual(cursor.rowcount, 3)
        self.assertEqual(cursor.fetchone(), (1,))
        self.assertEqual(cursor.fetchmany(), [(2,), (3,)])
        self.assertEqual(cursor.fetchall(), [])
        self.assertEqual(cursor.get_execution_metadata(), {"query_execution_id": "q-1"})
        cursor.execute("SELECT 1")
        self.assertEqual(list(cursor), [(1,), (2,), (3,)])
        with cursor:
            pass
        with self.assertRaisesRegex(dbapi.InterfaceError, "Cursor is closed"):
            cursor.fetchone()
        self.executor.execute.assert_called_with("SELECT 1")

    def test_dml_rowcount_and_no_result_fetch(self):
        self.executor.execute.return_value = SingleStatementResult(result=7)
        cursor = self.connection.cursor().execute("DELETE FROM t")
        self.assertEqual(cursor.rowcount, 7)
        self.assertIsNone(cursor.description)
        with self.assertRaisesRegex(dbapi.ProgrammingError, "did not return rows"):
            cursor.fetchall()

    def test_errors_are_mapped_to_dbapi_classes(self):
        cursor = self.connection.cursor()
        for error, expected in (
            (ValueError("bad parameter"), dbapi.ProgrammingError),
            (AthenaQueryError("q", "FAILED", "bad data"), dbapi.OperationalError),
            (RuntimeError("service"), dbapi.DatabaseError),
        ):
            cursor.description = [("stale", None, None, None, None, None, True)]
            cursor.query_id = "stale"
            cursor._rows = [(1,)]
            with self.subTest(error=error), mock.patch.object(
                self.executor, "execute", side_effect=error
            ), self.assertRaises(expected):
                cursor.execute("SELECT 1")
            self.assertIsNone(cursor.description)
            self.assertIsNone(cursor.query_id)
            self.assertEqual(cursor._rows, [])
        cursor.close()
        with self.assertRaisesRegex(dbapi.InterfaceError, "Cursor is closed"):
            cursor.execute("SELECT 1")

    def test_executemany_and_size_methods(self):
        self.executor.execute.return_value = SingleStatementResult(result=1)
        cursor = self.connection.cursor()
        self.assertIsNone(cursor.executemany("INSERT INTO t VALUES (?)", [[1], [2]]))
        self.assertEqual(self.executor.execute.call_count, 2)
        self.assertIsNone(cursor.setinputsizes(10))
        self.assertIsNone(cursor.setoutputsize(10))

        self.executor.execute.return_value = SingleStatementResult(result=DataFrame({"id": [1]}))
        with self.assertRaisesRegex(dbapi.NotSupportedError, "result-returning"):
            cursor.executemany("SELECT ?", [[1]])


class TestExecutorConstruction(unittest.TestCase):
    def setUp(self):
        self.session = mock.Mock()
        self.session.get_component.return_value.search_paths = []
        self.client = self.session.create_client.return_value
        self.client.get_work_group.return_value = {
            "WorkGroup": {
                "Configuration": {
                    "EngineVersion": {"EffectiveEngineVersion": "Athena DuckDB"},
                    "ManagedQueryResultsConfiguration": {"Enabled": True},
                }
            }
        }
        patcher = mock.patch.object(dbapi, "get_session", return_value=self.session)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_refreshable_provider_builds_native_executor(self):
        provider = mock.Mock(
            return_value={
                "access_key_id": "key",
                "secret_access_key": "secret",
                "session_token": "token",
                "expiration": "2099-01-01T00:00:00+00:00",
            }
        )
        executor = dbapi._executor_from_config(
            {"work_group": "wg", "region": "us-west-2", "credential_provider": provider}
        )
        self.assertIs(executor.client, self.client)
        self.assertIsNotNone(self.session._credentials)
        self.assertTrue(provider.called)

    def test_static_credentials_and_endpoint(self):
        executor = dbapi._executor_from_config(
            {
                "work_group": "wg",
                "region": "us-west-2",
                "endpoint_url": "https://athena.example",
                "aws_access_key_id": "key",
                "aws_secret_access_key": "secret",
                "aws_session_token": "token",
            }
        )
        self.assertIs(executor.client, self.client)
        self.session.set_credentials.assert_called_once_with("key", "secret", "token")
        self.session.create_client.assert_called_once_with(
            "athena", region_name="us-west-2", endpoint_url="https://athena.example"
        )

    def test_requires_workgroup_and_region(self):
        with self.assertRaisesRegex(dbapi.InterfaceError, "work_group and region"):
            dbapi._executor_from_config({"work_group": "wg"})

    def test_unreadable_workgroup_falls_back_to_rows(self):
        self.client.get_work_group.side_effect = RuntimeError("denied")
        executor = dbapi._executor_from_config({"work_group": "wg", "region": "us-west-2"})
        self.assertEqual(
            (executor.managed_storage, executor.workgroup_engine_version), (False, None)
        )

    def test_existing_model_path_is_not_added_twice(self):
        model_path = str(
            __import__("pathlib").Path(dbapi.__file__).resolve().parents[2] / "boto3_models"
        )
        self.session.get_component.return_value.search_paths = [model_path]
        dbapi._executor_from_config({"work_group": "wg", "region": "us-west-2"})
        self.assertEqual(self.session.get_component.return_value.search_paths, [model_path])


class TestDialect(unittest.TestCase):
    def test_connect_args_preserve_public_url(self):
        dialect = AthenaDialect()
        args, options = dialect.create_connect_args(
            make_url("awsathena+rest://@athena.us-west-2.amazonaws.com/analytics?work_group=wg")
        )
        self.assertEqual(args, [])
        self.assertEqual(
            options,
            {"region": "us-west-2", "schema_name": "analytics", "work_group": "wg"},
        )

    def test_column_types_and_constraints(self):
        dialect = AthenaDialect()
        self.assertEqual(str(dialect._column_type("decimal(10,2)")), "DECIMAL(10, 2)")
        self.assertEqual(str(dialect._column_type("varchar(20)")), "VARCHAR(20)")
        self.assertEqual(str(dialect._column_type("bigint")), "BIGINT")
        self.assertEqual(str(dialect._column_type("future")), "NULL")
        self.assertEqual(str(dialect._column_type("???")), "NULL")
        self.assertEqual(dialect.get_foreign_keys(None, "t"), [])
        self.assertEqual(
            dialect.get_pk_constraint(None, "t"), {"name": None, "constrained_columns": []}
        )
        self.assertEqual(dialect.get_indexes(None, "t"), [])

    def test_connect_args_without_standard_host_or_database(self):
        dialect = AthenaDialect()
        self.assertEqual(
            dialect.create_connect_args(make_url("awsathena+rest://custom-host?work_group=wg")),
            ([], {"work_group": "wg"}),
        )
        self.assertEqual(
            dialect.create_connect_args(make_url("awsathena+rest://?region=us-west-2")),
            ([], {"region": "us-west-2"}),
        )

    def test_execution_and_connection_hooks_delegate_to_dbapi(self):
        dialect = AthenaDialect()
        cursor = mock.Mock()
        connection = mock.Mock()
        dialect.do_executemany(cursor, "INSERT INTO t VALUES (?)", [[1], [2]])
        dialect.do_commit(connection)
        dialect.do_close(connection)
        cursor.executemany.assert_called_once()
        connection.commit.assert_called_once()
        connection.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
