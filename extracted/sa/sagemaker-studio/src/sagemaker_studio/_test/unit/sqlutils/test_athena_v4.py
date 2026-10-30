"""Tests for sagemaker_studio.utils.athena_v4 (Athena engine version 4 without PyAthena)."""

import gc
import io
import os
import unittest
import weakref
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from unittest import mock

import pyarrow as pa
from botocore.credentials import RefreshableCredentials
from botocore.exceptions import IncompleteReadError, ResponseStreamingError
from botocore.response import StreamingBody

from sagemaker_studio.utils import athena_v4
from sagemaker_studio.utils.athena_v4 import (
    AthenaQueryError,
    AthenaV4Executor,
    athena_executor,
    dataframe_from_arrow,
    execution_metadata,
    returns_rows,
    split_query,
    workgroup_engine_version,
    workgroup_info,
)
from sagemaker_studio.utils.sqlutils_async import AsyncResultMarker

QID = "11111111-2222-3333-4444-555555555555"


def _ipc_bytes(table):
    sink = io.BytesIO()
    with pa.ipc.new_stream(sink, table.schema) as writer:
        writer.write_table(table)
    return sink.getvalue()


def _stream_response(payload, status=200, content_length=None):
    """A GetQueryResultStream response the way botocore returns it."""
    length = len(payload) if content_length is None else content_length
    return {
        "Body": StreamingBody(io.BytesIO(payload), len(payload)),
        "ResponseMetadata": {
            "HTTPStatusCode": status,
            "HTTPHeaders": {"content-length": str(length)},
        },
    }


class _CutOffBody:
    """A response body that yields ``data`` and then fails with ``error`` (a dropped read)."""

    def __init__(self, data, error):
        self._data, self._error = data, error

    def iter_chunks(self, chunk_size=1024):
        if self._data:
            yield self._data
        raise self._error


def _cut_off_response(data, error, total):
    return {
        "Body": _CutOffBody(data, error),
        "ResponseMetadata": {"HTTPStatusCode": 200, "HTTPHeaders": {"content-length": str(total)}},
    }


def _work_group(version, managed=True, output_location=None):
    """A GetWorkGroup response. By default the workgroup uses Athena managed result storage;
    pass ``managed=False`` with an ``output_location`` to model a customer output location."""
    configuration = {
        "EngineVersion": {"EffectiveEngineVersion": f"Athena engine version {version}"}
    }
    if managed:
        configuration["ManagedQueryResultsConfiguration"] = {"Enabled": True}
    if output_location is not None:
        configuration["ResultConfiguration"] = {"OutputLocation": output_location}
    return {"WorkGroup": {"Configuration": configuration}}


def _connection(version=4, conn_type="ATHENA", managed=True, output_location=None):
    conn = mock.Mock(type=conn_type, id="conn-1")
    conn.name = "athena_conn"
    conn.data.workgroup_name = "wg"
    client = conn.create_client.return_value
    client.get_work_group.return_value = _work_group(
        version, managed=managed, output_location=output_location
    )
    return conn, client


def _execution(state="SUCCEEDED", statement_type="DML", substatement_type="SELECT", **status):
    return {
        "QueryExecution": {
            "QueryExecutionId": QID,
            "StatementType": statement_type,
            "SubstatementType": substatement_type,
            "Status": {"State": state, **status},
            "Statistics": {"DataScannedInBytes": 10, "TotalExecutionTimeInMillis": 20},
        }
    }


class SplitQueryTest(unittest.TestCase):
    def test_preserves_comments_and_semicolons_inside_literals(self):
        query = "-- first :ignored\nSELECT ';' AS value; /* second */ DELETE FROM t WHERE id = :id;"

        statements = split_query(query)

        self.assertEqual(
            [statement.statement for statement in statements],
            ["-- first :ignored\nSELECT ';' AS value", "/* second */ DELETE FROM t WHERE id = :id"],
        )
        self.assertEqual(
            [statement.statement_type for statement in statements], ["SELECT", "DELETE"]
        )

    def test_unparseable_statement_keeps_exact_text_with_unknown_type(self):
        statements = split_query("BROKEN ( ; -- comment only")

        self.assertEqual(len(statements), 1)
        self.assertEqual(statements[0].statement, "BROKEN (")
        self.assertEqual(statements[0].statement_type, "UNKNOWN")


class StatementParameterScopingTest(unittest.TestCase):
    def test_positional_values_are_distributed_by_statement(self):
        statements = split_query("SELECT ?; SELECT 2; SELECT ?")
        self.assertEqual(
            athena_v4._statement_parameter_sets(statements, ["first", "third"]),
            [["first"], [], ["third"]],
        )

    def test_named_values_are_reused_for_each_statement(self):
        statements = split_query("SELECT :value; SELECT :value")
        parameters = {"value": 1}
        scoped = athena_v4._statement_parameter_sets(statements, parameters)
        self.assertEqual(scoped, [parameters, parameters])

    def test_missing_named_value_fails_before_execution(self):
        executor = mock.Mock()
        executor.execution_parameters = {"present": 1}
        with self.assertRaisesRegex(ValueError, "Missing Athena query parameter: missing"):
            athena_v4.execute_query_statements(
                executor,
                "INSERT INTO audit VALUES (:present); SELECT :missing",
                "stop_on_error",
            )
        executor.execute.assert_not_called()

    def test_named_validation_ignores_literals_comments_and_casts(self):
        statements = split_query("SELECT ':literal', value::varchar, :present -- :comment")
        parameters = {"present": 1}
        self.assertEqual(athena_v4._statement_parameter_sets(statements, parameters), [parameters])

    def test_positional_mismatch_fails_before_execution(self):
        executor = mock.Mock()
        executor.execution_parameters = [1]
        with self.assertRaisesRegex(ValueError, "2 positional placeholders but 1 values"):
            athena_v4.execute_query_statements(
                executor,
                "SELECT ?; SELECT ?",
                "stop_on_error",
            )
        executor.execute.assert_not_called()

    def test_execution_uses_each_scope_and_restores_parameters(self):
        from sagemaker_studio.sql_engine.sql_executor import SingleStatementResult

        executor = mock.Mock()
        executor.execution_parameters = ["first", "third"]
        seen = []

        def execute(statement):
            seen.append((statement, list(executor.execution_parameters)))
            return SingleStatementResult(result=statement)

        executor.execute.side_effect = execute
        results = list(
            athena_v4.execute_query_statements(
                executor,
                "SELECT ?; SELECT 2; SELECT ?",
                "stop_on_error",
            )
        )
        self.assertEqual(
            seen,
            [("SELECT ?", ["first"]), ("SELECT 2", []), ("SELECT ?", ["third"])],
        )
        self.assertEqual(executor.execution_parameters, ["first", "third"])
        self.assertEqual(
            [result.result for result in results], ["SELECT ?", "SELECT 2", "SELECT ?"]
        )

    def test_custom_execute_method_uses_the_same_scoping(self):
        executor = mock.Mock()
        executor.execution_parameters = [1]
        execute = mock.Mock(side_effect=RuntimeError("boom"))
        results = athena_v4.execute_query_statements(
            executor,
            "SELECT ?",
            "stop_on_error",
            execute,
        )
        result = next(results)
        self.assertEqual(result.status, "error")
        self.assertEqual(executor.execution_parameters, [1])
        execute.assert_called_once_with("SELECT ?")


class WorkgroupEngineVersionTest(unittest.TestCase):
    def test_reads_the_effective_engine_version(self):
        client = mock.Mock()
        client.get_work_group.return_value = _work_group(4)
        self.assertEqual(workgroup_engine_version(client, "wg"), 4)
        client.get_work_group.assert_called_once_with(WorkGroup="wg")

    def test_v4_transition_names_are_recognized(self):
        client = mock.Mock()
        for name in (
            "Athena engine version 4",
            "Athena DuckDB",
            "KeplerSparkSQL-2.x",
            "DuckDB-2.x",
        ):
            with self.subTest(name=name):
                client.get_work_group.return_value = {
                    "WorkGroup": {
                        "Configuration": {"EngineVersion": {"EffectiveEngineVersion": name}}
                    }
                }
                self.assertEqual(workgroup_engine_version(client, "wg"), 4)

    def test_unknown_version_is_none(self):
        client = mock.Mock()
        client.get_work_group.return_value = {"WorkGroup": {"Configuration": {}}}
        self.assertIsNone(workgroup_engine_version(client, "wg"))


class WorkgroupInfoTest(unittest.TestCase):
    def test_managed_storage_workgroup(self):
        client = mock.Mock()
        client.get_work_group.return_value = _work_group(4, managed=True)
        info = workgroup_info(client, "wg")
        self.assertEqual((info.engine_version, info.managed_storage), (4, True))

    def test_customer_output_location_workgroup(self):
        client = mock.Mock()
        client.get_work_group.return_value = _work_group(
            4, managed=False, output_location="s3://customer-bucket/results/"
        )
        info = workgroup_info(client, "wg")
        self.assertEqual((info.engine_version, info.managed_storage), (4, False))

    def test_absent_configuration_is_not_managed(self):
        client = mock.Mock()
        client.get_work_group.return_value = {"WorkGroup": {"Configuration": {}}}
        info = workgroup_info(client, "wg")
        self.assertEqual((info.engine_version, info.managed_storage), (None, False))


class AthenaExecutorRoutingTest(unittest.TestCase):
    def tearDown(self):
        athena_v4.clear_cache()

    def test_v3_uses_native_row_reader_without_pyathena(self):
        conn, client = _connection(version=3, managed=False, output_location="s3://results/")
        executor = athena_executor(conn)
        self.assertIsNotNone(executor)
        client.start_query_execution.return_value = {"QueryExecutionId": QID}
        response = _execution()
        response["QueryExecution"]["EngineVersion"] = {
            "EffectiveEngineVersion": "Athena engine version 3"
        }
        client.get_query_execution.return_value = response
        client.get_query_results.return_value = {
            "ResultSet": {
                "ResultSetMetadata": {"ColumnInfo": [{"Name": "n", "Type": "integer"}]},
                "Rows": [
                    {"Data": [{"VarCharValue": "n"}]},
                    {"Data": [{"VarCharValue": "42"}]},
                ],
            }
        }

        result = executor.execute("SELECT 42 AS n")

        self.assertEqual(result.result.iloc[0, 0], 42)
        self.assertEqual(result.execution_metadata["result_reader"], "get_query_results")
        client.get_query_result_stream.assert_not_called()

    def test_v3_workgroup_query_override_to_v4_uses_arrow_when_managed(self):
        conn, client = _connection(version=3, managed=True)
        executor = athena_executor(conn, selected_engine_version="Athena engine version 4")
        client.start_query_execution.return_value = {"QueryExecutionId": QID}
        response = _execution()
        response["QueryExecution"]["EngineVersion"] = {
            "EffectiveEngineVersion": "Athena engine version 4"
        }
        client.get_query_execution.return_value = response
        client.get_query_result_stream.return_value = _stream_response(
            _ipc_bytes(pa.table({"n": pa.array([42], pa.int32())}))
        )

        result = executor.execute("SELECT 42 AS n")

        self.assertEqual(result.result.iloc[0, 0], 42)
        self.assertEqual(result.execution_metadata["result_reader"], "get_query_result_stream")
        request = client.start_query_execution.call_args.kwargs
        self.assertEqual(request["EngineVersion"], "Athena engine version 4")

    def test_actual_v3_execution_overrides_v4_workgroup_and_uses_rows(self):
        conn, client = _connection(version=4, managed=True)
        executor = athena_executor(conn, selected_engine_version="Athena engine version 3")
        client.start_query_execution.return_value = {"QueryExecutionId": QID}
        response = _execution()
        response["QueryExecution"]["EngineVersion"] = {
            "EffectiveEngineVersion": "Athena engine version 3"
        }
        client.get_query_execution.return_value = response
        client.get_query_results.return_value = {
            "ResultSet": {
                "ResultSetMetadata": {"ColumnInfo": [{"Name": "n", "Type": "integer"}]},
                "Rows": [
                    {"Data": [{"VarCharValue": "n"}]},
                    {"Data": [{"VarCharValue": "7"}]},
                ],
            }
        }

        result = executor.execute("SELECT 7 AS n")

        self.assertEqual(result.result.iloc[0, 0], 7)
        client.get_query_result_stream.assert_not_called()

    def test_v4_customer_output_uses_native_rows(self):
        conn, client = _connection(version=4, managed=False, output_location="s3://results/")
        executor = athena_executor(conn)
        client.start_query_execution.return_value = {"QueryExecutionId": QID}
        response = _execution()
        response["QueryExecution"]["StatementType"] = None
        response["QueryExecution"]["SubstatementType"] = None
        response["QueryExecution"]["EngineVersion"] = {
            "EffectiveEngineVersion": "Athena engine version 4"
        }
        client.get_query_execution.return_value = response
        client.get_query_results.return_value = {
            "ResultSet": {
                "ResultSetMetadata": {"ColumnInfo": [{"Name": "n", "Type": "integer"}]},
                "Rows": [
                    {"Data": [{"VarCharValue": "n"}]},
                    {"Data": [{"VarCharValue": "9"}]},
                ],
            }
        }

        result = executor.execute("SELECT 9 AS n")

        self.assertEqual(result.result.iloc[0, 0], 9)
        self.assertEqual(result.execution_metadata["result_reader"], "get_query_results")


class AthenaV4ExecutorTest(unittest.TestCase):
    def setUp(self):
        self.client = mock.Mock()
        self.executor = AthenaV4Executor(self.client, "wg", catalog="cat", schema="db")
        for target in ("sagemaker_studio.utils.athena_v4.time.sleep",):
            patcher = mock.patch(target)
            patcher.start()
            self.addCleanup(patcher.stop)

    def test_start_sends_no_result_configuration(self):
        self.client.start_query_execution.return_value = {"QueryExecutionId": QID}
        self.assertEqual(self.executor.start("SELECT 1"), QID)
        self.client.start_query_execution.assert_called_once_with(
            QueryString="SELECT 1",
            WorkGroup="wg",
            QueryExecutionContext={"Catalog": "cat", "Database": "db"},
        )

    def test_start_binds_named_parameters_as_literals_without_rewriting_sql(self):
        self.client.start_query_execution.return_value = {"QueryExecutionId": QID}
        executor = AthenaV4Executor(
            self.client,
            "wg",
            execution_parameters={
                "start": "2024-01-01",
                "name": "O'Brien",
                "missing": None,
                "day": date(2024, 1, 2),
                "amount": Decimal("12.30"),
            },
        )
        statement = (
            "-- keep :ignored\nSELECT ':literal', order_date >= :start, name = :name, "
            ":missing, :day, :amount /* keep :also_ignored */"
        )

        executor.start(statement)

        request = self.client.start_query_execution.call_args.kwargs
        self.assertEqual(
            request["QueryString"],
            "-- keep :ignored\nSELECT ':literal', order_date >= '2024-01-01', "
            "name = 'O''Brien', NULL, DATE '2024-01-02', DECIMAL '12.30' "
            "/* keep :also_ignored */",
        )
        self.assertNotIn("ExecutionParameters", request)

    def test_start_binds_positional_parameters_client_side_for_any_statement(self):
        self.client.start_query_execution.return_value = {"QueryExecutionId": QID}
        executor = AthenaV4Executor(
            self.client,
            "wg",
            execution_parameters=[7, "O'Brien"],
        )

        executor.start("DELETE FROM t WHERE id = ? AND name = ? -- keep ?")

        request = self.client.start_query_execution.call_args.kwargs
        self.assertEqual(
            request["QueryString"],
            "DELETE FROM t WHERE id = 7 AND name = 'O''Brien' -- keep ?",
        )
        self.assertNotIn("ExecutionParameters", request)

    def test_start_rejects_missing_named_parameter(self):
        executor = AthenaV4Executor(self.client, "wg", execution_parameters={"x": 1})
        with self.assertRaisesRegex(ValueError, "Missing Athena query parameter: y"):
            executor.start("SELECT :y")
        self.client.start_query_execution.assert_not_called()

    def test_start_without_context(self):
        self.client.start_query_execution.return_value = {"QueryExecutionId": QID}
        AthenaV4Executor(self.client, "wg").start("SELECT 1")
        self.assertEqual(
            self.client.start_query_execution.call_args.kwargs,
            {"QueryString": "SELECT 1", "WorkGroup": "wg"},
        )

    def test_wait_polls_until_the_query_finishes(self):
        self.client.get_query_execution.side_effect = [
            _execution("QUEUED"),
            _execution("RUNNING"),
            _execution("SUCCEEDED"),
        ]
        execution = self.executor.wait(QID)
        self.assertEqual(execution["Status"]["State"], "SUCCEEDED")
        self.assertEqual(self.client.get_query_execution.call_count, 3)

    def test_failed_query_raises_with_the_reason(self):
        self.client.get_query_execution.return_value = _execution(
            "FAILED", StateChangeReason="TABLE_NOT_FOUND: t"
        )
        with self.assertRaises(AthenaQueryError) as raised:
            self.executor.wait(QID)
        self.assertEqual(raised.exception.state, "FAILED")
        self.assertIn("TABLE_NOT_FOUND: t", str(raised.exception))

    def test_failed_query_falls_back_to_the_athena_error_message(self):
        self.client.get_query_execution.return_value = _execution(
            "FAILED", AthenaError={"ErrorMessage": "boom"}
        )
        with self.assertRaisesRegex(AthenaQueryError, "boom"):
            self.executor.wait(QID)

    def test_interrupt_stops_the_query(self):
        self.client.get_query_execution.side_effect = KeyboardInterrupt
        with self.assertRaises(KeyboardInterrupt):
            self.executor.wait(QID)
        self.client.stop_query_execution.assert_called_once_with(QueryExecutionId=QID)

    def _stream(self, table):
        self.client.get_query_result_stream.return_value = _stream_response(_ipc_bytes(table))

    def test_execute_select_returns_the_stream_as_a_dataframe(self):
        self.client.start_query_execution.return_value = {"QueryExecutionId": QID}
        self.client.get_query_execution.return_value = _execution()
        self._stream(pa.table({"id": pa.array([1, 2], pa.int64()), "s": pa.array(["a", None])}))
        single = self.executor.execute("SELECT id, s FROM t")
        self.assertEqual(list(single.result.columns), ["id", "s"])
        self.assertEqual(single.result["id"].tolist(), [1, 2])
        self.assertEqual(single.execution_metadata["query_execution_id"], QID)
        self.client.get_query_result_stream.assert_called_once_with(QueryExecutionId=QID)
        self.client.get_query_results.assert_not_called()

    def test_execute_insert_returns_the_update_count(self):
        self.client.start_query_execution.return_value = {"QueryExecutionId": QID}
        self.client.get_query_execution.return_value = _execution(substatement_type="INSERT")
        self.client.get_query_results.return_value = {"UpdateCount": 7}
        self.assertEqual(self.executor.execute("INSERT INTO t VALUES (1)").result, 7)
        self.client.get_query_result_stream.assert_not_called()

    def test_execute_ddl_returns_minus_one(self):
        self.client.start_query_execution.return_value = {"QueryExecutionId": QID}
        self.client.get_query_execution.return_value = _execution(
            statement_type="DDL", substatement_type="CREATE_TABLE"
        )
        self.assertEqual(self.executor.execute("CREATE TABLE t (id int)").result, -1)
        self.client.get_query_results.assert_not_called()
        self.client.get_query_result_stream.assert_not_called()

    def test_execute_ctas_returns_the_update_count(self):
        self.client.start_query_execution.return_value = {"QueryExecutionId": QID}
        self.client.get_query_execution.return_value = _execution(
            statement_type="DDL", substatement_type="CREATE_TABLE_AS_SELECT"
        )
        self.client.get_query_results.return_value = {"UpdateCount": 1}
        self.assertEqual(self.executor.execute("CREATE TABLE t AS SELECT 1").result, 1)
        self.client.get_query_result_stream.assert_not_called()

    def test_execute_without_fetch_returns_a_marker(self):
        self.client.start_query_execution.return_value = {"QueryExecutionId": QID}
        self.client.get_query_execution.return_value = _execution()
        single = self.executor.execute_without_fetch("SELECT 1")
        self.assertEqual(single.result, AsyncResultMarker(execution_id=QID))
        self.client.get_query_result_stream.assert_not_called()

    def test_read_chunks_is_positional_with_the_exact_total(self):
        table = pa.Table.from_arrays([pa.array([1, 2]), pa.array(["x", "y"])], names=["a", "a"])
        self._stream(table)
        columns, chunks, total = self.executor.read_chunks(QID)
        self.assertEqual(columns, ["a", "a"])
        self.assertEqual([row for chunk in chunks for row in chunk], [[1, "x"], [2, "y"]])
        self.assertEqual(total, 2)


def _ipc_bytes_batches(batches, schema):
    """An Arrow IPC stream written as multiple record batches (so batch boundaries survive)."""
    sink = io.BytesIO()
    with pa.ipc.new_stream(sink, schema) as writer:
        for batch in batches:
            writer.write_batch(batch)
    return sink.getvalue()


class ReadChunksIncrementalTest(unittest.TestCase):
    """read_chunks' Arrow path decodes the IPC stream batch-by-batch instead of materializing the
    whole pyarrow.Table, while preserving column names, types, the exact total, resume and the
    GetQueryResults fallback."""

    def setUp(self):
        self.client = mock.Mock()
        self.executor = AthenaV4Executor(self.client, "wg")
        # Mark QID as a V4 managed-storage execution so read_chunks takes the Arrow branch.
        self.executor.managed_storage = True
        self.executor._executions[QID] = _execution()["QueryExecution"]
        self.schema = pa.schema([("id", pa.int64()), ("s", pa.string())])
        self.batches = [
            pa.record_batch(
                [pa.array([1, 2], pa.int64()), pa.array(["a", "b"])], schema=self.schema
            ),
            pa.record_batch([pa.array([3], pa.int64()), pa.array(["c"])], schema=self.schema),
        ]
        self.payload = _ipc_bytes_batches(self.batches, self.schema)

    def _stream(self, payload=None, status=200, content_length=None):
        self.client.get_query_result_stream.return_value = _stream_response(
            self.payload if payload is None else payload,
            status=status,
            content_length=content_length,
        )

    def test_columns_and_total_available_without_building_the_full_table(self):
        # The old path built the whole pyarrow.Table via read_table()/read_all(); the incremental
        # path must not call read_table at all. Columns and the exact total are returned up front.
        self._stream()
        with mock.patch.object(
            self.executor, "read_table", side_effect=AssertionError("read_table must not be called")
        ):
            columns, chunks, total = self.executor.read_chunks(QID)
            self.assertEqual(columns, ["id", "s"])
            self.assertEqual(total, 3)
        # The iterator still yields every row with the right values after the fact.
        self.assertEqual([row for chunk in chunks for row in chunk], [[1, "a"], [2, "b"], [3, "c"]])

    def test_first_chunk_yielded_before_the_iterator_is_exhausted(self):
        # Pulling one chunk must not force the whole result through; later chunks remain pending.
        self._stream()
        _columns, chunks, _total = self.executor.read_chunks(QID)
        first = next(chunks)
        self.assertEqual(first, [[1, "a"], [2, "b"]])
        self.assertEqual(next(chunks), [[3, "c"]])

    def test_batches_are_released_incrementally(self):
        # After a batch is yielded its reference is dropped by the generator, so it becomes
        # collectable while later batches are still pending -- the whole set is never held
        # resident during iteration (the old path kept the full table alive in the closure).
        self._stream()
        _columns, chunks, _total = self.executor.read_chunks(QID)
        # The generator holds its pending batches in a closure list that shrinks as it yields.
        pending = chunks.gi_frame.f_locals["batches"]
        self.assertEqual(len(pending), 2)
        first_batch = pending[0]
        ref = weakref.ref(first_batch)
        next(chunks)
        # The first batch is popped out of the pending list after it is yielded.
        self.assertEqual(len(chunks.gi_frame.f_locals["batches"]), 1)
        del first_batch
        gc.collect()
        self.assertIsNone(ref(), "the yielded batch should be released, not held for the whole run")
        next(chunks)
        self.assertEqual(len(chunks.gi_frame.f_locals["batches"]), 0)

    def test_resume_with_range_header_feeds_the_incremental_path(self):
        half = len(self.payload) // 2
        self.client.get_query_result_stream.side_effect = [
            _cut_off_response(
                self.payload[:half],
                IncompleteReadError(actual_bytes=half, expected_bytes=len(self.payload)),
                len(self.payload),
            ),
            _stream_response(self.payload[half:], status=206),
        ]
        columns, chunks, total = self.executor.read_chunks(QID)
        self.assertEqual(columns, ["id", "s"])
        self.assertEqual(total, 3)
        self.assertEqual([row for chunk in chunks for row in chunk], [[1, "a"], [2, "b"], [3, "c"]])
        ranges = [c.kwargs.get("Range") for c in self.client.get_query_result_stream.call_args_list]
        self.assertEqual(ranges, [None, f"bytes={half}-"])

    def test_error_during_streaming_propagates(self):
        # A cut-off read with no Content-Length to resume against re-raises the original error,
        # exactly as the eager path does -- the incremental decode never masks it.
        cut = ResponseStreamingError(error="reset")
        self.client.get_query_result_stream.return_value = {
            "Body": _CutOffBody(self.payload[: len(self.payload) // 2], cut),
            "ResponseMetadata": {"HTTPStatusCode": 200, "HTTPHeaders": {}},
        }
        with self.assertRaises(ResponseStreamingError):
            self.executor.read_chunks(QID)

    def test_types_preserved_through_the_incremental_path(self):
        schema = pa.schema(
            [("i", pa.int64()), ("f", pa.float64()), ("b", pa.bool_()), ("n", pa.int64())]
        )
        batch = pa.record_batch(
            [
                pa.array([7], pa.int64()),
                pa.array([1.5], pa.float64()),
                pa.array([True]),
                pa.array([None], pa.int64()),
            ],
            schema=schema,
        )
        self._stream(_ipc_bytes_batches([batch], schema))
        columns, chunks, total = self.executor.read_chunks(QID)
        self.assertEqual(columns, ["i", "f", "b", "n"])
        self.assertEqual(total, 1)
        row = next(chunks)[0]
        self.assertEqual(row[0], 7)
        self.assertIsInstance(row[0], int)
        self.assertEqual(row[1], 1.5)
        self.assertIsInstance(row[1], float)
        self.assertIs(row[2], True)
        self.assertIsNone(row[3])

    def test_empty_batches_are_skipped(self):
        schema = pa.schema([("id", pa.int64())])
        batches = [
            pa.record_batch([pa.array([], pa.int64())], schema=schema),
            pa.record_batch([pa.array([1, 2], pa.int64())], schema=schema),
        ]
        self._stream(_ipc_bytes_batches(batches, schema))
        columns, chunks, total = self.executor.read_chunks(QID)
        self.assertEqual(columns, ["id"])
        self.assertEqual(total, 2)
        self.assertEqual([row for chunk in chunks for row in chunk], [[1], [2]])

    def test_non_arrow_execution_falls_back_to_get_query_results(self):
        # A non-managed-storage execution must still route to the native GetQueryResults reader,
        # never GetQueryResultStream.
        self.executor.managed_storage = False
        with mock.patch(
            "sagemaker_studio.utils.sqlutils_async_reader.read_athena_result",
            return_value=(["c"], iter([[[1]]]), 1),
        ) as read_athena_result:
            columns, chunks, total = self.executor.read_chunks(QID)
        self.assertEqual(columns, ["c"])
        self.assertEqual(total, 1)
        self.assertEqual([row for chunk in chunks for row in chunk], [[1]])
        read_athena_result.assert_called_once()
        self.client.get_query_result_stream.assert_not_called()


class ResultStreamReadTest(unittest.TestCase):
    """GetQueryResultStream reads, including resuming a cut-off read with a Range request."""

    def setUp(self):
        self.client = mock.Mock()
        self.executor = AthenaV4Executor(self.client, "wg")
        self.table = pa.table({"id": pa.array(range(100), pa.int64())})
        self.payload = _ipc_bytes(self.table)
        self.half = len(self.payload) // 2

    def _ranges(self):
        return [c.kwargs.get("Range") for c in self.client.get_query_result_stream.call_args_list]

    def test_full_read_needs_no_resume(self):
        self.client.get_query_result_stream.return_value = _stream_response(self.payload)
        with self.assertLogs(athena_v4.logger, level="INFO") as logs:
            table = self.executor.read_table(QID)
        self.assertTrue(table.equals(self.table))
        self.assertEqual(self._ranges(), [None])
        self.assertRegex(
            logs.output[-1],
            rf"Athena query {QID}: read 100 rows \({len(self.payload)} bytes\) with "
            r"GetQueryResultStream in \d+\.\d\ds",
        )

    def test_incomplete_read_resumes_from_the_received_bytes(self):
        self.client.get_query_result_stream.side_effect = [
            _cut_off_response(
                self.payload[: self.half],
                IncompleteReadError(actual_bytes=self.half, expected_bytes=len(self.payload)),
                len(self.payload),
            ),
            _stream_response(self.payload[self.half :], status=206),
        ]
        self.assertTrue(self.executor.read_table(QID).equals(self.table))
        self.assertEqual(self._ranges(), [None, f"bytes={self.half}-"])

    def test_dropped_connection_resumes(self):
        self.client.get_query_result_stream.side_effect = [
            _cut_off_response(
                self.payload[: self.half], ResponseStreamingError(error="reset"), len(self.payload)
            ),
            _stream_response(self.payload[self.half :], status=206),
        ]
        self.assertTrue(self.executor.read_table(QID).equals(self.table))

    def test_resume_answered_with_the_whole_body_replaces_it(self):
        self.client.get_query_result_stream.side_effect = [
            _cut_off_response(
                self.payload[: self.half], ResponseStreamingError(error="reset"), len(self.payload)
            ),
            _stream_response(self.payload, status=200),
        ]
        self.assertTrue(self.executor.read_table(QID).equals(self.table))

    def test_resume_without_new_bytes_raises(self):
        self.client.get_query_result_stream.side_effect = [
            _cut_off_response(
                self.payload[: self.half], ResponseStreamingError(error="reset"), len(self.payload)
            ),
            _stream_response(b"", status=206),
        ]
        with self.assertRaisesRegex(RuntimeError, "returned no data"):
            self.executor.read_table(QID)

    def test_gives_up_after_the_last_resume(self):
        cut = ResponseStreamingError(error="reset")
        self.client.get_query_result_stream.side_effect = [
            _cut_off_response(self.payload[:10], cut, len(self.payload))
        ] + [
            {
                "Body": _CutOffBody(self.payload[10 + i : 11 + i], cut),
                "ResponseMetadata": {"HTTPStatusCode": 206, "HTTPHeaders": {}},
            }
            for i in range(athena_v4._MAX_STREAM_RESUMES)
        ]
        with self.assertRaisesRegex(RuntimeError, "after 3 resumes"):
            self.executor.read_table(QID)
        self.assertEqual(len(self._ranges()), 1 + athena_v4._MAX_STREAM_RESUMES)

    def test_more_bytes_than_advertised_raises(self):
        self.client.get_query_result_stream.return_value = _stream_response(
            self.payload, content_length=len(self.payload) - 1
        )
        with mock.patch.object(
            athena_v4, "_read_available", return_value=(bytearray(self.payload), None)
        ):
            with self.assertRaisesRegex(RuntimeError, "more than the advertised"):
                self.executor.read_table(QID)

    def test_cut_off_read_without_a_length_reraises(self):
        cut = ResponseStreamingError(error="reset")
        self.client.get_query_result_stream.return_value = {
            "Body": _CutOffBody(self.payload[: self.half], cut),
            "ResponseMetadata": {"HTTPStatusCode": 200, "HTTPHeaders": {}},
        }
        with self.assertRaises(ResponseStreamingError):
            self.executor.read_table(QID)


class HelpersTest(unittest.TestCase):
    def test_returns_rows(self):
        self.assertTrue(returns_rows({"StatementType": "DML", "SubstatementType": "SELECT"}))
        self.assertTrue(
            returns_rows({"StatementType": "UTILITY", "SubstatementType": "SHOW_TABLES"})
        )
        self.assertFalse(returns_rows({"StatementType": "DML", "SubstatementType": "INSERT"}))
        self.assertFalse(returns_rows({"StatementType": "DDL"}))

    def test_execution_metadata_uses_the_pyathena_keys(self):
        submitted = datetime(2026, 10, 8, tzinfo=timezone.utc)
        metadata = execution_metadata(
            {
                "QueryExecutionId": QID,
                "Statistics": {"DataScannedInBytes": 10, "EngineExecutionTimeInMillis": 5},
                "Status": {"SubmissionDateTime": submitted},
            }
        )
        self.assertEqual(
            metadata,
            {
                "query_execution_id": QID,
                "data_scanned_bytes": 10,
                "engine_execution_time_ms": 5,
                "submission_time": submitted.isoformat(),
            },
        )

    def test_dataframe_keeps_duplicate_columns_and_empty_results(self):
        df = dataframe_from_arrow(
            pa.Table.from_arrays([pa.array([1]), pa.array(["x"])], names=["a", "a"])
        )
        self.assertEqual(list(df.columns), ["a", "a"])
        empty = dataframe_from_arrow(pa.table({"a": pa.array([], pa.int64())}))
        self.assertEqual((list(empty.columns), len(empty)), (["a"], 0))


class BundledModelRequestTest(unittest.TestCase):
    """The real requests, built from the bundled rest-json Athena model."""

    class _Sent(Exception):
        pass

    def setUp(self):
        import boto3
        import botocore.session

        import sagemaker_studio

        session = botocore.session.get_session()
        session.get_component("data_loader").search_paths.insert(
            0, os.path.join(os.path.dirname(sagemaker_studio.__file__), "boto3_models")
        )
        session.set_credentials("AKIDTEST", "secret")
        self.client = boto3.Session(botocore_session=session).client(
            "athena", region_name="us-west-2"
        )
        self.sent = []

        def _capture(request, **_kwargs):
            self.sent.append(request)
            raise self._Sent()

        self.client.meta.events.register("before-send.athena", _capture)

    def test_start_query_execution_request_has_no_result_configuration(self):
        import json

        with self.assertRaises(self._Sent):
            AthenaV4Executor(self.client, "wg", schema="db").start("SELECT 1")
        request = self.sent[-1]
        self.assertEqual(request.url, "https://athena.us-west-2.amazonaws.com/query-executions")
        body = json.loads(request.body)
        self.assertEqual(body["WorkGroup"], "wg")
        self.assertEqual(body["QueryExecutionContext"], {"Database": "db"})
        self.assertNotIn("ResultConfiguration", body)

    def test_query_level_engine_override_request(self):
        import json

        with self.assertRaises(self._Sent):
            AthenaV4Executor(
                self.client,
                "wg",
                selected_engine_version="Athena engine version 4",
            ).start("SELECT 1")
        body = json.loads(self.sent[-1].body)
        self.assertEqual(body["EngineVersion"], "Athena engine version 4")

    def test_result_stream_request(self):
        with self.assertRaises(self._Sent):
            self.client.get_query_result_stream(QueryExecutionId=QID)
        request = self.sent[-1]
        self.assertEqual(request.method, "GET")
        self.assertEqual(
            request.url,
            f"https://athena.us-west-2.amazonaws.com/query-executions/{QID}/result-stream",
        )

    def test_resume_range_is_sent_as_a_header(self):
        with self.assertRaises(self._Sent):
            self.client.get_query_result_stream(QueryExecutionId=QID, Range="bytes=1024-")
        self.assertEqual(self.sent[-1].headers["Range"], b"bytes=1024-")


class RegressionTrapParityTest(unittest.TestCase):
    """The four behaviours the Arrow (V4) path must preserve relative to the PyAthena path.

    1. dtype parity -- Arrow -> DataFrame yields the SAME Python types the PyAthena sync
       path produces via ``DefaultTypeConverter`` (decimal/date/timestamp incl. named tz/
       varbinary/json/nulls).
    2. no header echo -- Athena's row-0 column-label echo is a GetQueryResults (row-paging)
       artifact; GetQueryResultStream returns typed columns with no echo, so the Arrow path
       must NOT drop a first data row, even one whose values equal the column names.
    3. INLINE_FIRST_PAGE_ROWS -- the async V4 path reuses ``split_first_page`` with the same
       default inline page size as the PyAthena async path.
    4. total_rows -- the Arrow path returns the EXACT row count where the PyAthena async
       reader returns None (a strictly-better divergence the UI pagination must tolerate).
    """

    def setUp(self):
        self.client = mock.Mock()
        self.executor = AthenaV4Executor(self.client, "wg")

    # --- 1. dtype parity ------------------------------------------------------------------

    def test_dtypes_match_the_pyathena_default_type_converter(self):
        """Every value coming off the Arrow table is the SAME Python type the PyAthena sync
        cursor would produce from the equivalent VarCharValue string."""
        import datetime as dt
        import decimal

        from sagemaker_studio.utils.athena_type_converter import convert_athena_value

        table = pa.table(
            {
                "amt": pa.array([decimal.Decimal("123.45"), None], pa.decimal128(5, 2)),
                "d": pa.array([dt.date(2026, 10, 15), None], pa.date32()),
                "ts": pa.array([dt.datetime(2026, 10, 15, 12, 34, 56), None], pa.timestamp("us")),
                "b": pa.array([b"\xde\xad\xbe\xef", None], pa.binary()),
                "n": pa.array([42, None], pa.int64()),
                "flag": pa.array([True, None], pa.bool_()),
            }
        )
        df = dataframe_from_arrow(table)

        # Row 0: types match PyAthena's converter output exactly.
        self.assertEqual(df["amt"][0], convert_athena_value("123.45", "decimal"))
        self.assertIsInstance(df["amt"][0], decimal.Decimal)
        self.assertEqual(df["d"][0], convert_athena_value("2026-10-15", "date"))
        self.assertIsInstance(df["d"][0], dt.date)
        self.assertEqual(df["ts"][0], convert_athena_value("2026-10-15 12:34:56.000", "timestamp"))
        self.assertIsInstance(df["ts"][0], dt.datetime)
        self.assertEqual(df["b"][0], convert_athena_value("de ad be ef", "varbinary"))
        self.assertIsInstance(df["b"][0], (bytes, bytearray))
        self.assertEqual(df["n"][0], convert_athena_value("42", "integer"))
        self.assertEqual(df["flag"][0], convert_athena_value("true", "boolean"))

        # Nulls: both paths represent a null cell as NA. A datetime column coerces to
        # datetime64[ns] (null -> NaT) and object columns keep None -- IDENTICAL to the
        # PyAthena async path's DataFrame(rows, columns) over coerced values, so assert
        # NA-ness (pd.isna) rather than literal None, which only holds for object columns.
        import pandas as pd

        for column in ("amt", "d", "ts", "b", "n", "flag"):
            self.assertTrue(pd.isna(df[column][1]), f"{column} null should be NA")
        # The timestamp column lands in datetime64[ns] in both paths (null -> NaT), not object.
        self.assertEqual(str(df["ts"].dtype), "datetime64[ns]")
        # Decimal/date stay object-typed with real None, like PyAthena.
        self.assertIsNone(df["amt"][1])
        self.assertIsNone(df["d"][1])

    def test_timestamp_with_time_zone_is_tz_aware_with_the_named_zone(self):
        """A zoned Arrow timestamp yields a tz-aware ``datetime`` carrying the named zone --
        the same kind of value PyAthena's ``timestamp with time zone`` conversion produces
        (both represent the same instant; this asserts type + awareness + zone key, not a
        wall-clock equality, which depends only on how the instant is encoded)."""
        import datetime as dt

        from sagemaker_studio.utils.athena_type_converter import convert_athena_value

        row_value = convert_athena_value(
            "2026-10-15 12:34:56.000 America/Los_Angeles", "timestamp with time zone"
        )
        table = pa.table(
            {
                "ts": pa.array(
                    [dt.datetime(2026, 10, 15, 12, 34, 56)],
                    pa.timestamp("us", "America/Los_Angeles"),
                )
            }
        )
        arrow_value = dataframe_from_arrow(table)["ts"][0]

        self.assertIsInstance(arrow_value, dt.datetime)
        self.assertIsNotNone(arrow_value.tzinfo, "Arrow zoned timestamp must be tz-aware")
        self.assertIsNotNone(row_value.tzinfo)
        self.assertEqual(arrow_value.utcoffset(), row_value.utcoffset())
        self.assertEqual(arrow_value.tzname(), row_value.tzname())

    def test_execute_select_preserves_dtypes_end_to_end(self):
        """The whole execute() path (StartQueryExecution -> stream -> DataFrame) keeps the
        decimal/date dtypes, not just the pure ``dataframe_from_arrow`` helper."""
        import datetime as dt
        import decimal

        self.client.start_query_execution.return_value = {"QueryExecutionId": QID}
        self.client.get_query_execution.return_value = _execution()
        self.client.get_query_result_stream.return_value = _stream_response(
            _ipc_bytes(
                pa.table(
                    {
                        "amt": pa.array([decimal.Decimal("1.50")], pa.decimal128(3, 2)),
                        "d": pa.array([dt.date(2026, 1, 1)], pa.date32()),
                    }
                )
            )
        )
        df = self.executor.execute("SELECT amt, d FROM t").result
        self.assertIsInstance(df["amt"][0], decimal.Decimal)
        self.assertEqual(df["amt"][0], decimal.Decimal("1.50"))
        self.assertIsInstance(df["d"][0], dt.date)

    # --- 2. no header echo ----------------------------------------------------------------

    def test_arrow_path_does_not_strip_a_header_echo_row(self):
        """GetQueryResultStream has no column-label echo, so a first data row whose values
        equal the column names must survive -- unlike the GetQueryResults row API, where
        read_athena_result drops row 0. This guards against anyone copying the skip-header
        logic onto the Arrow path."""
        table = pa.table({"id": pa.array(["id", "1"]), "name": pa.array(["name", "alice"])})
        self.client.get_query_result_stream.return_value = _stream_response(_ipc_bytes(table))
        columns, chunks, total = self.executor.read_chunks(QID)
        rows = [row for chunk in chunks for row in chunk]
        self.assertEqual(columns, ["id", "name"])
        # The literal ("id", "name") first row is kept, NOT dropped as an echo.
        self.assertEqual(rows, [["id", "name"], ["1", "alice"]])
        self.assertEqual(total, 2)

    # --- 3. INLINE_FIRST_PAGE_ROWS default --------------------------------------------------

    def test_async_v4_first_page_uses_the_same_default_inline_size(self):
        """The async V4 path feeds ``read_chunks`` into ``split_first_page`` with the same
        default inline page size (``INLINE_FIRST_PAGE_ROWS``) as the PyAthena async path, so
        the first-page/remainder split behaves identically. With more rows than the default,
        the inline page is exactly the default size and the remainder carries the rest."""
        from sagemaker_studio.utils.sqlutils_async_reader import (
            INLINE_FIRST_PAGE_ROWS,
            split_first_page,
        )

        self.assertEqual(INLINE_FIRST_PAGE_ROWS, 999)
        row_count = INLINE_FIRST_PAGE_ROWS + 5
        table = pa.table({"id": pa.array(list(range(row_count)), pa.int64())})
        self.client.get_query_result_stream.return_value = _stream_response(_ipc_bytes(table))

        _columns, chunks, total = self.executor.read_chunks(QID)
        first_page, remaining = split_first_page(chunks, INLINE_FIRST_PAGE_ROWS)

        self.assertEqual(len(first_page), INLINE_FIRST_PAGE_ROWS)
        self.assertEqual(total, row_count)
        remaining_rows = [row for chunk in remaining for row in chunk]
        self.assertEqual(len(remaining_rows), row_count - INLINE_FIRST_PAGE_ROWS)
        # No rows lost or duplicated across the split.
        self.assertEqual(
            [r[0] for r in first_page] + [r[0] for r in remaining_rows], list(range(row_count))
        )

    def test_async_v4_first_page_smaller_than_default_pulls_everything_inline(self):
        """A result below the default inline size is returned whole as the first page, with an
        empty remainder -- the single-round-trip property the 999 default protects."""
        from sagemaker_studio.utils.sqlutils_async_reader import (
            INLINE_FIRST_PAGE_ROWS,
            split_first_page,
        )

        table = pa.table({"id": pa.array([1, 2, 3], pa.int64())})
        self.client.get_query_result_stream.return_value = _stream_response(_ipc_bytes(table))
        _columns, chunks, _total = self.executor.read_chunks(QID)
        first_page, remaining = split_first_page(chunks, INLINE_FIRST_PAGE_ROWS)
        self.assertEqual([r[0] for r in first_page], [1, 2, 3])
        self.assertEqual([row for chunk in remaining for row in chunk], [])

    # --- 4. total_rows divergence (exact vs None) ------------------------------------------

    def test_total_rows_is_exact_not_none(self):
        """Where the PyAthena async reader returns ``total_rows=None`` (no cheap upfront count),
        the Arrow path returns the EXACT count -- Arrow knows num_rows for free. The UI
        pagination contract must accept a real integer where it previously got None."""
        from sagemaker_studio.utils.sqlutils_async_reader import read_athena_result

        # PyAthena async reader: total is None.
        pyathena_client = mock.Mock()
        pyathena_client.get_query_results.return_value = {
            "ResultSet": {
                "ResultSetMetadata": {"ColumnInfo": [{"Name": "id", "Type": "integer"}]},
                "Rows": [
                    {"Data": [{"VarCharValue": "id"}]},  # header echo
                    {"Data": [{"VarCharValue": "1"}]},
                    {"Data": [{"VarCharValue": "2"}]},
                ],
            }
        }
        _c, _chunks, pyathena_total = read_athena_result(pyathena_client, QID)
        self.assertIsNone(pyathena_total)

        # Arrow V4 reader: total is the exact row count.
        table = pa.table({"id": pa.array([1, 2], pa.int64())})
        self.client.get_query_result_stream.return_value = _stream_response(_ipc_bytes(table))
        _columns, _chunks2, v4_total = self.executor.read_chunks(QID)
        self.assertEqual(v4_total, 2)
        self.assertIsInstance(v4_total, int)


class AthenaNativeMetadataTest(unittest.TestCase):
    def setUp(self):
        self.client = mock.Mock()
        self.executor = AthenaV4Executor(
            self.client, "wg", catalog="catalog", managed_storage=False
        )

    def test_lists_paginated_databases(self):
        self.client.list_databases.side_effect = [
            {"DatabaseList": [{"Name": "db1"}], "NextToken": "next"},
            {"DatabaseList": [{"Name": "db2"}]},
        ]

        resources = self.executor.get_resources("DATABASE")

        self.assertEqual(
            [(item.name, item.type, item.children) for item in resources],
            [("db1", "DATABASE", ["TABLE"]), ("db2", "DATABASE", ["TABLE"])],
        )
        self.assertEqual(
            self.client.list_databases.call_args_list,
            [
                mock.call(CatalogName="catalog", WorkGroup="wg"),
                mock.call(CatalogName="catalog", WorkGroup="wg", NextToken="next"),
            ],
        )

    def test_lists_tables_in_database(self):
        self.client.list_table_metadata.return_value = {"TableMetadataList": [{"Name": "orders"}]}

        resources = self.executor.get_resources("TABLE", {"DATABASE": "analytics"})

        self.assertEqual(resources[0].name, "orders")
        self.assertEqual(resources[0].children, ["COLUMN"])
        self.client.list_table_metadata.assert_called_once_with(
            CatalogName="catalog", WorkGroup="wg", DatabaseName="analytics"
        )

    def test_lists_columns_in_table(self):
        self.client.get_table_metadata.return_value = {
            "TableMetadata": {"Columns": [{"Name": "id"}, {"Name": "amount"}]}
        }

        resources = self.executor.get_resources(
            "COLUMN", {"DATABASE": "analytics", "TABLE": "orders"}
        )

        self.assertEqual([item.name for item in resources], ["id", "amount"])
        self.client.get_table_metadata.assert_called_once_with(
            CatalogName="catalog",
            WorkGroup="wg",
            DatabaseName="analytics",
            TableName="orders",
        )

    def test_rejects_unsupported_resource_type(self):
        with self.assertRaisesRegex(ValueError, "Unsupported resource type"):
            self.executor.get_resources("VIEW")


class AthenaExecutorRoutingBranchTest(unittest.TestCase):
    """Edge paths of ``athena_executor`` not exercised by the happy-path routing tests."""

    def tearDown(self):
        athena_v4.clear_cache()

    def test_none_connection_returns_none(self):
        self.assertIsNone(athena_executor(None))

    def test_non_athena_connection_returns_none(self):
        self.assertIsNone(athena_executor(mock.Mock(type="REDSHIFT")))

    def test_lakehouse_athena_connection_uses_its_workgroup(self):
        conn, client = _connection(4, conn_type="LAKEHOUSE")
        conn.sql_engine_type = "ATHENA"
        conn.data.workgroup_name = None
        conn.athena_workgroup = "catalog-wg"

        executor = athena_executor(conn)

        self.assertIsInstance(executor, AthenaV4Executor)
        self.assertEqual(executor.work_group, "catalog-wg")
        client.get_work_group.assert_called_once_with(WorkGroup="catalog-wg")

    def test_connection_catalog_is_used_without_a_query_override(self):
        conn, _client = _connection(4)
        conn.data.catalog = "AwsDataCatalog"

        executor = athena_executor(conn)

        self.assertEqual(executor.catalog, "AwsDataCatalog")

    def test_missing_workgroup_name_returns_none(self):
        conn = mock.Mock(type="ATHENA", id="conn-1")
        conn.name = "c"
        conn.data.workgroup_name = None
        self.assertIsNone(athena_executor(conn))

    def test_missing_connection_identity_returns_none(self):
        conn, _client = _connection(4)
        conn.id = None
        conn.name = None
        self.assertIsNone(athena_executor(conn))

    def test_unreadable_workgroup_falls_back_to_native_reader_and_warns(self):
        conn, client = _connection(4)
        client.get_work_group.side_effect = RuntimeError("AccessDenied")
        with self.assertLogs(athena_v4.logger, level="WARNING"):
            executor = athena_executor(conn)
        self.assertIsNotNone(executor)
        self.assertFalse(executor.managed_storage)
        self.assertIsNone(executor.workgroup_engine_version)

    def test_override_read_from_connection_selected_engine_version(self):
        conn, _client = _connection(4)
        conn.data.selected_engine_version = "Athena engine version 4"
        executor = athena_executor(conn)
        self.assertEqual(executor.selected_engine_version, "Athena engine version 4")

    def test_override_falls_back_to_connection_engine_version(self):
        conn, _client = _connection(4)
        conn.data.selected_engine_version = None
        conn.data.engine_version = "Athena engine version 3"
        executor = athena_executor(conn)
        self.assertEqual(executor.selected_engine_version, "Athena engine version 3")

    def test_integer_override_is_coerced_to_string(self):
        conn, _client = _connection(4)
        executor = athena_executor(conn, selected_engine_version=4)
        self.assertEqual(executor.selected_engine_version, "4")

    def test_non_string_non_int_override_is_discarded(self):
        conn, _client = _connection(4)
        executor = athena_executor(conn, selected_engine_version=["v4"])
        self.assertIsNone(executor.selected_engine_version)

    def test_rejects_non_mapping_non_list_parameters(self):
        conn, _client = _connection(4)
        with self.assertRaisesRegex(ValueError, "mapping or positional list"):
            athena_executor(conn, parameters="x")

    def test_native_client_uses_refreshable_credentials(self):
        conn, client = _connection(4)
        provider = mock.Mock(
            return_value={
                "access_key_id": "AKIA_REFRESHED",
                "secret_access_key": "secret",
                "session_token": "token",
                "expiration": datetime(2099, 1, 1, tzinfo=timezone.utc).isoformat(),
            }
        )
        session = mock.Mock()
        session.get_component.return_value.search_paths = []
        conn._create_client_with_session.return_value = client

        with mock.patch.object(athena_v4, "get_session", return_value=session):
            executor = athena_executor(conn, credential_provider=provider)

        credentials = session._credentials
        self.assertIsInstance(credentials, RefreshableCredentials)
        self.assertEqual(credentials.access_key, "AKIA_REFRESHED")
        self.assertIs(executor.client, client)
        conn._create_client_with_session.assert_called_once_with("athena", session)
        session.create_client.assert_not_called()

    def test_refreshable_credentials_require_complete_metadata(self):
        provider = mock.Mock(return_value={"access_key_id": "key"})
        with self.assertRaisesRegex(ValueError, "missing required keys"):
            athena_v4._refreshable_credentials(provider)


class ArrowValuesFallbackTest(unittest.TestCase):
    """``_arrow_values`` fallback when the installed PyArrow lacks ``maps_as_pydicts``."""

    def _column(self, pylist, is_map):
        column = mock.Mock()
        column.to_pylist.side_effect = [TypeError("maps_as_pydicts unsupported"), pylist]
        column.type = mock.Mock()
        return column

    def test_map_column_is_converted_to_dicts_on_type_error(self):
        column = self._column([[("k", 1)], None], is_map=True)
        with mock.patch.object(pa.types, "is_map", return_value=True):
            self.assertEqual(athena_v4._arrow_values(column), [{"k": 1}, None])

    def test_non_map_column_returns_plain_values_on_type_error(self):
        column = self._column([1, 2], is_map=False)
        with mock.patch.object(pa.types, "is_map", return_value=False):
            self.assertEqual(athena_v4._arrow_values(column), [1, 2])


class WaitInterruptBranchTest(unittest.TestCase):
    """``wait`` interrupt handling when StopQueryExecution itself fails."""

    def setUp(self):
        self.client = mock.Mock()
        self.executor = AthenaV4Executor(self.client, "wg")

    def test_interrupt_with_failing_stop_still_reraises(self):
        self.client.get_query_execution.side_effect = KeyboardInterrupt
        self.client.stop_query_execution.side_effect = RuntimeError("stop failed")
        with self.assertRaises(KeyboardInterrupt):
            self.executor.wait(QID)
        self.client.stop_query_execution.assert_called_once_with(QueryExecutionId=QID)


class ExecutionVersionTest(unittest.TestCase):
    """``_execution_version`` resolution from the selected engine version string."""

    def test_falls_back_to_selected_engine_version_number(self):
        executor = AthenaV4Executor(
            mock.Mock(), "wg", selected_engine_version="Athena engine version 4"
        )
        # No execution-level EngineVersion -> parse the selected engine version string.
        self.assertEqual(executor._execution_version({}), 4)

    def test_renamed_effective_engine_version_selects_v4(self):
        executor = AthenaV4Executor(mock.Mock(), "wg", workgroup_engine_version=3)
        execution = {"EngineVersion": {"EffectiveEngineVersion": "Athena DuckDB"}}
        self.assertEqual(executor._execution_version(execution), 4)

    def test_selected_engine_version_without_a_number_falls_back_to_workgroup(self):
        executor = AthenaV4Executor(
            mock.Mock(),
            "wg",
            selected_engine_version="AUTO",
            workgroup_engine_version=3,
        )
        self.assertEqual(executor._execution_version({}), 3)

    def test_auto_override_is_not_sent_to_start_query_execution(self):
        client = mock.Mock()
        client.start_query_execution.return_value = {"QueryExecutionId": QID}
        executor = AthenaV4Executor(client, "wg", selected_engine_version="AUTO")

        self.assertEqual(executor.start("SELECT 1"), QID)
        request = client.start_query_execution.call_args.kwargs
        self.assertNotIn("EngineVersion", request)

    def test_concrete_override_is_sent_to_start_query_execution(self):
        client = mock.Mock()
        client.start_query_execution.return_value = {"QueryExecutionId": QID}
        executor = AthenaV4Executor(client, "wg", selected_engine_version="Athena engine version 4")

        self.assertEqual(executor.start("SELECT 1"), QID)
        self.assertEqual(
            client.start_query_execution.call_args.kwargs["EngineVersion"],
            "Athena engine version 4",
        )

    def test_renamed_override_is_sent_to_start_query_execution(self):
        client = mock.Mock()
        client.start_query_execution.return_value = {"QueryExecutionId": QID}
        executor = AthenaV4Executor(client, "wg", selected_engine_version="Athena DuckDB")

        self.assertEqual(executor.start("SELECT 1"), QID)
        self.assertEqual(
            client.start_query_execution.call_args.kwargs["EngineVersion"],
            "Athena DuckDB",
        )


class ReadChunksEmptyBatchTest(unittest.TestCase):
    """The Arrow ``read_chunks`` generator skips empty record batches (line 540)."""

    def setUp(self):
        self.client = mock.Mock()
        self.executor = AthenaV4Executor(self.client, "wg")

    def test_empty_batch_is_skipped(self):
        empty = pa.RecordBatch.from_arrays([pa.array([], pa.int64())], names=["id"])
        full = pa.RecordBatch.from_arrays([pa.array([1, 2], pa.int64())], names=["id"])
        # read_chunks now streams the IPC body incrementally (no read_table); feed both batches
        # through the GetQueryResultStream body so the empty-batch skip is exercised on the
        # streaming path.
        payload = _ipc_bytes_batches([empty, full], empty.schema)
        self.client.get_query_result_stream.return_value = _stream_response(payload)
        _columns, chunks, total = self.executor.read_chunks(QID)
        rows = [row for chunk in chunks for row in chunk]
        # The empty batch contributes no chunk; only the full batch's rows appear.
        self.assertEqual(rows, [[1], [2]])
        self.assertEqual(total, 2)


class ReadStreamResumeBranchTest(unittest.TestCase):
    """Remaining ``_read_stream`` raises: a resume that neither errors nor yields bytes, and a
    body longer than the advertised length."""

    def setUp(self):
        self.client = mock.Mock()
        self.executor = AthenaV4Executor(self.client, "wg")
        self.table = pa.table({"id": pa.array(range(50), pa.int64())})
        self.payload = _ipc_bytes(self.table)
        self.half = len(self.payload) // 2

    def test_empty_erroring_resume_loops_until_a_later_resume_completes(self):
        # Resume 1 (206) yields no bytes but DOES error -> not 200, not chunk, not
        # error-is-None, so the loop continues (branch 509->485) instead of raising. Resume 2
        # (206) delivers the rest and completes the read.
        cut = ResponseStreamingError(error="reset")
        empty_206 = {
            "Body": _CutOffBody(b"", cut),
            "ResponseMetadata": {"HTTPStatusCode": 206, "HTTPHeaders": {}},
        }
        self.client.get_query_result_stream.side_effect = [
            _cut_off_response(self.payload[: self.half], cut, len(self.payload)),
            empty_206,
            _stream_response(self.payload[self.half :], status=206),
        ]
        self.assertTrue(self.executor.read_table(QID).equals(self.table))

    def test_resume_with_no_error_and_no_new_bytes_raises(self):
        # First read is cut off; the resume returns a 206 with no body and no error.
        self.client.get_query_result_stream.side_effect = [
            _cut_off_response(
                self.payload[: self.half],
                ResponseStreamingError(error="reset"),
                len(self.payload),
            ),
            {
                "Body": StreamingBody(io.BytesIO(b""), 0),
                "ResponseMetadata": {
                    "HTTPStatusCode": 206,
                    "HTTPHeaders": {},
                },
            },
        ]
        with self.assertRaisesRegex(RuntimeError, "returned no data"):
            self.executor.read_table(QID)

    def test_body_longer_than_advertised_raises(self):
        self.client.get_query_result_stream.return_value = _stream_response(
            self.payload, content_length=len(self.payload) - 1
        )
        with mock.patch.object(
            athena_v4, "_read_available", return_value=(bytearray(self.payload), None)
        ):
            with self.assertRaisesRegex(RuntimeError, "more than the advertised"):
                self.executor.read_table(QID)


class GetResourcesFallthroughTest(unittest.TestCase):
    """The defensive final ``raise`` in ``get_resources`` (line 579 / branch 571->579).

    Normal resource types all return before it, so it is reached only with a value that
    passes the initial membership guard yet matches none of the handled branches.
    """

    def setUp(self):
        self.client = mock.Mock()
        self.executor = AthenaV4Executor(self.client, "wg", catalog="cat", managed_storage=False)

    def test_value_passing_membership_but_matching_no_branch_raises(self):
        class _MembershipOnlyColumn:
            # Equals "COLUMN" exactly once -- consumed by the membership guard at line 557
            # (``resource_type not in (..., "COLUMN", ...)``) so it is accepted, then compares
            # unequal everywhere after, so the DATABASE/None, TABLE and COLUMN branches are all
            # skipped and the final defensive raise (line 579) is reached.
            def __init__(self):
                self._matched = False

            def __eq__(self, other):
                if other == "COLUMN" and not self._matched:
                    self._matched = True
                    return True
                return False

            def __hash__(self):
                return hash("COLUMN")

            def __repr__(self):
                return "<membership-only>"

        with self.assertRaisesRegex(ValueError, "Unsupported resource type"):
            self.executor.get_resources(_MembershipOnlyColumn(), {"DATABASE": "db"})


class RowcountBranchTest(unittest.TestCase):
    """``rowcount`` DDL short-circuit and the GetQueryResults failure fallback."""

    def setUp(self):
        self.client = mock.Mock()
        self.executor = AthenaV4Executor(self.client, "wg")

    def test_ddl_without_a_rowcount_substatement_returns_minus_one(self):
        result = self.executor.rowcount(
            {"QueryExecutionId": QID, "StatementType": "DDL", "SubstatementType": "CREATE_TABLE"}
        )
        self.assertEqual(result, -1)
        self.client.get_query_results.assert_not_called()

    def test_failed_update_count_read_returns_minus_one(self):
        self.client.get_query_results.side_effect = RuntimeError("boom")
        with self.assertLogs(athena_v4.logger, level="DEBUG"):
            result = self.executor.rowcount(
                {
                    "QueryExecutionId": QID,
                    "StatementType": "DML",
                    "SubstatementType": "INSERT",
                }
            )
        self.assertEqual(result, -1)

    def test_non_integer_update_count_returns_minus_one(self):
        self.client.get_query_results.return_value = {"UpdateCount": None}
        result = self.executor.rowcount(
            {"QueryExecutionId": QID, "StatementType": "DML", "SubstatementType": "INSERT"}
        )
        self.assertEqual(result, -1)


class ExecuteNativeRowsPathTest(unittest.TestCase):
    """``execute`` and ``execute_without_fetch`` on the non-Arrow (GetQueryResults) path."""

    def setUp(self):
        self.client = mock.Mock()
        # managed_storage=False forces the native Row/Datum reader regardless of version.
        self.executor = AthenaV4Executor(self.client, "wg", managed_storage=False)
        patcher = mock.patch("sagemaker_studio.utils.athena_v4.time.sleep")
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_execute_select_uses_native_rows_and_builds_a_dataframe(self):
        self.client.start_query_execution.return_value = {"QueryExecutionId": QID}
        self.client.get_query_execution.return_value = _execution()
        self.client.get_query_results.return_value = {
            "ResultSet": {
                "ResultSetMetadata": {"ColumnInfo": [{"Name": "n", "Type": "integer"}]},
                "Rows": [
                    {"Data": [{"VarCharValue": "n"}]},
                    {"Data": [{"VarCharValue": "5"}]},
                ],
            }
        }
        single = self.executor.execute("SELECT 5 AS n")
        self.assertEqual(list(single.result.columns), ["n"])
        self.assertEqual(int(single.result.iloc[0, 0]), 5)
        self.assertEqual(single.execution_metadata["result_reader"], "get_query_results")
        self.client.get_query_result_stream.assert_not_called()

    def test_execute_without_fetch_insert_returns_the_rowcount(self):
        self.client.start_query_execution.return_value = {"QueryExecutionId": QID}
        self.client.get_query_execution.return_value = _execution(substatement_type="INSERT")
        self.client.get_query_results.return_value = {"UpdateCount": 3}
        single = self.executor.execute_without_fetch("INSERT INTO t VALUES (1)")
        self.assertEqual(single.result, 3)
        self.assertEqual(single.execution_metadata["result_reader"], "get_query_results")


class ExecutionMetadataOutputLocationTest(unittest.TestCase):
    """``execution_metadata`` records an output location when present (branch 716->717)."""

    def test_output_location_is_included(self):
        metadata = execution_metadata(
            {
                "QueryExecutionId": QID,
                "ResultConfiguration": {"OutputLocation": "s3://bucket/results/"},
            }
        )
        self.assertEqual(metadata["output_location"], "s3://bucket/results/")

    def test_content_length_non_numeric_header_is_none(self):
        # Covers _content_length's (TypeError, ValueError) guard (lines 673-674).
        self.assertIsNone(
            athena_v4._content_length(
                {"ResponseMetadata": {"HTTPHeaders": {"content-length": "not-a-number"}}}
            )
        )


class AthenaTypeConverterCoverageTest(unittest.TestCase):
    """Exercise every native Row/Datum converter and malformed-value fallback."""

    def setUp(self):
        from sagemaker_studio.utils import athena_type_converter

        self.converter = athena_type_converter

    def test_scalar_and_temporal_values(self):
        convert = self.converter.convert_athena_value
        self.assertIsNone(convert(None, "varchar"))
        self.assertEqual(convert("raw", "unknown"), "raw")
        self.assertIsNone(convert("", "boolean"))
        self.assertTrue(convert("YES", "boolean"))
        self.assertFalse(convert("off", "boolean"))
        self.assertEqual(convert("invalid", "boolean"), "invalid")
        self.assertIsNone(convert("", "decimal(10,2)"))
        self.assertEqual(convert("12:34:56.123", "time").hour, 12)
        zoned = convert("2026-10-20 12:34:56.123 America/Los_Angeles", "timestamp with time zone")
        self.assertIsNotNone(zoned.tzinfo)
        self.assertEqual(convert("0a ff", "varbinary"), b"\x0a\xff")
        self.assertEqual(convert("not-hex", "varbinary"), "not-hex")

    def test_native_scalar_and_top_level_split(self):
        scalar = self.converter._native_scalar
        self.assertEqual(
            [scalar(value) for value in ("null", "true", "false", "12", "-3", "1.5", "text")],
            [None, True, False, 12, -3, 1.5, "text"],
        )
        self.assertEqual(
            self.converter._split_top_level("a,{b=1,c=2},[3,4],z"),
            ["a", "{b=1,c=2}", "[3,4]", "z"],
        )

    def test_array_values_and_fallbacks(self):
        array = self.converter._array
        self.assertIsNone(array("not-an-array"))
        self.assertEqual(array("[1, true, null]"), [1, True, None])
        self.assertEqual(array("[]"), [])
        with mock.patch.object(
            self.converter.json,
            "loads",
            side_effect=self.converter.json.JSONDecodeError("invalid", "[]", 0),
        ):
            self.assertEqual(array("[]"), [])
        self.assertEqual(array("[[1]]"), [[1]])
        self.assertIsNone(array("[[1,]]"))
        self.assertEqual(array('[{a=1},,two,three=four,"quoted"]'), [{"a": 1}, "two"])
        self.assertIsNone(array("[three=four]"))

    def test_map_values_and_fallbacks(self):
        mapping = self.converter._map
        self.assertIsNone(mapping("not-a-map"))
        self.assertEqual(mapping('{"a":1}'), {"a": 1})
        self.assertEqual(mapping("{}"), {})
        self.assertIsNone(mapping("{a=(1)}"))
        self.assertEqual(mapping("{a=1,skip,b=true}"), {"a": 1, "b": True})
        self.assertIsNone(mapping('{bad="quoted"}'))
        self.assertIsNone(mapping("{missing}"))

    def test_struct_values_and_fallbacks(self):
        struct = self.converter._struct
        self.assertIsNone(struct("not-a-struct"))
        self.assertEqual(struct('{"a":1}'), {"a": 1})
        self.assertEqual(struct("{}"), {})
        self.assertEqual(struct("{1,true,text}"), {"0": 1, "1": True, "2": "text"})
        self.assertEqual(struct("{a=1,skip,b=false}"), {"a": 1, "b": False})
        self.assertIsNone(struct('{bad="quoted"}'))


class AthenaParameterLiteralCoverageTest(unittest.TestCase):
    def test_supported_literals(self):
        cases = (
            (None, "NULL"),
            (True, "TRUE"),
            (False, "FALSE"),
            ("O'Brien", "'O''Brien'"),
            (
                datetime(2024, 1, 2, 3, 4, 5, 123000, tzinfo=timezone.utc),
                "TIMESTAMP '2024-01-02 03:04:05.123'",
            ),
            (
                datetime(2024, 1, 2, 3, 4, 5, tzinfo=timezone(timedelta(hours=2))),
                "TIMESTAMP '2024-01-02 01:04:05.000'",
            ),
            (datetime(2024, 1, 2, 3, 4, 5, 123456), "TIMESTAMP '2024-01-02 03:04:05.123456'"),
            (date(2024, 1, 2), "DATE '2024-01-02'"),
            (Decimal("12.30"), "DECIMAL '12.30'"),
            (7, "7"),
            (1.5, "1.5"),
            (b"\x01\xff", "X'01ff'"),
            (bytearray(b"a"), "X'61'"),
            (memoryview(b"b"), "X'62'"),
            ([1, "two"], "(1, 'two')"),
            ((3,), "(3)"),
            ({4}, "(4)"),
        )
        for value, expected in cases:
            with self.subTest(value=value):
                self.assertEqual(athena_v4._sql_literal(value), expected)

    def test_rejects_non_finite_and_unsupported_literals(self):
        for value, message in (
            (Decimal("NaN"), "decimal parameters must be finite"),
            (float("inf"), "float parameters must be finite"),
            (object(), "Unsupported Athena query parameter type"),
        ):
            with self.subTest(value=value), self.assertRaisesRegex(
                (ValueError, TypeError), message
            ):
                athena_v4._sql_literal(value)

    def test_no_parameters_returns_the_statement_unchanged(self):
        statement = "-- keep\nSELECT 1"
        self.assertEqual(athena_v4._bind_parameters(statement, None), statement)

    def test_colon_without_a_parameter_name_is_ignored(self):
        self.assertEqual(athena_v4._bind_parameters("SELECT :1", {}), "SELECT :1")

    def test_positional_parameter_count_must_match(self):
        with self.assertRaisesRegex(ValueError, "1 positional placeholders but 0 values"):
            athena_v4._bind_parameters("SELECT ?", [])

    def test_parameter_container_must_be_mapping_or_list(self):
        with self.assertRaisesRegex(ValueError, "mapping or positional list"):
            athena_v4._bind_parameters("SELECT 1", "invalid")


if __name__ == "__main__":
    unittest.main()
