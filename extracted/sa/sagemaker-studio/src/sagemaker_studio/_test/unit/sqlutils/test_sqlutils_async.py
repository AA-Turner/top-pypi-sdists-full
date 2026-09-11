"""Unit tests for sagemaker_studio.utils.sqlutils_async."""

import contextlib
import json
import sys
import threading
import unittest
from types import SimpleNamespace
from unittest import mock

from sagemaker_studio.utils import sqlutils_async as async_mod
from sagemaker_studio.utils import sqlutils_async_reader as reader_mod
from sagemaker_studio.utils.sqlutils_async import (
    ROWS_PER_PAGE,
    AsyncResultMarker,
    AsyncSqlResult,
    Manifest,
    StatementSpec,
    _MaterializationRegistry,
    _rebuffer_to_pages,
    build_result_prefix,
    extract_execution_id,
    manifest_key,
    materialize_async,
    materialize_async_multi,
    page_key,
    spec_from_result,
)


class ExtractExecutionIdTest(unittest.TestCase):
    def test_athena(self):
        self.assertEqual(extract_execution_id({"query_execution_id": "athena-1"}), "athena-1")

    def test_redshift(self):
        self.assertEqual(extract_execution_id({"statement_id": "rs-1"}), "rs-1")

    def test_athena_wins_when_both_present(self):
        self.assertEqual(
            extract_execution_id({"query_execution_id": "a", "statement_id": "b"}), "a"
        )

    def test_none_and_empty(self):
        self.assertIsNone(extract_execution_id(None))
        self.assertIsNone(extract_execution_id({}))


class PrefixAndKeyTest(unittest.TestCase):
    def test_prefix_strips_trailing_slash(self):
        self.assertEqual(
            build_result_prefix("s3://bkt/dom/proj/dev/", "exec-9"),
            "s3://bkt/dom/proj/dev/results/exec-9/",
        )

    def test_page_key_zero_padded(self):
        prefix = "s3://b/results/e/"
        self.assertEqual(page_key(prefix, 0), "s3://b/results/e/page_000.parquet")
        self.assertEqual(page_key(prefix, 12), "s3://b/results/e/page_012.parquet")

    def test_manifest_key(self):
        self.assertEqual(manifest_key("s3://b/results/e/"), "s3://b/results/e/_manifest.json")

    def test_missing_inputs_raise(self):
        with self.assertRaises(ValueError):
            build_result_prefix("", "e")
        with self.assertRaises(ValueError):
            build_result_prefix("s3://b", "")


class ManifestTest(unittest.TestCase):
    def test_defaults(self):
        self.assertEqual(
            json.loads(Manifest().to_json()),
            {
                "totalfiles": 0,
                "rowPerPages": ROWS_PER_PAGE,
                "status": "in_progress",
                "row_count": 0,
            },
        )

    def test_complete(self):
        self.assertEqual(
            json.loads(Manifest(totalfiles=9, status="complete", row_count=85235).to_json()),
            {
                "totalfiles": 9,
                "rowPerPages": ROWS_PER_PAGE,
                "status": "complete",
                "row_count": 85235,
            },
        )


class RebufferTest(unittest.TestCase):
    def test_fixed_pages_and_first_page_order(self):
        cancel = threading.Event()
        pages = list(_rebuffer_to_pages([[1], [2], [3]], iter([[[4], [5]]]), 2, cancel))
        self.assertEqual(pages, [[[1], [2]], [[3], [4]], [[5]]])
        # page_000 leads with the inline first-page rows, in order.
        self.assertEqual(pages[0], [[1], [2]])

    def test_cancel_stops_before_remaining(self):
        cancel = threading.Event()
        cancel.set()
        self.assertEqual(list(_rebuffer_to_pages([[1]], iter([[[2], [3]]]), 2, cancel)), [])


class MaterializationRegistryTest(unittest.TestCase):
    def test_second_start_supersedes_and_cancels_first(self):
        reg = _MaterializationRegistry()
        g1, e1 = reg.start("df")
        self.assertTrue(reg.is_current("df", g1))
        g2, e2 = reg.start("df")
        self.assertTrue(e1.is_set())
        self.assertFalse(e2.is_set())
        self.assertFalse(reg.is_current("df", g1))
        self.assertTrue(reg.is_current("df", g2))

    def test_finish_clears_only_current(self):
        reg = _MaterializationRegistry()
        g1, _ = reg.start("df")
        g2, _ = reg.start("df")
        reg.finish("df", g1)  # stale finish is a no-op
        self.assertTrue(reg.is_current("df", g2))
        # finishing the current run clears its cancel tracking, but the generation
        # stays current until a newer run supersedes it.
        reg.finish("df", g2)
        self.assertTrue(reg.is_current("df", g2))
        g3, _ = reg.start("df")
        self.assertFalse(reg.is_current("df", g2))
        self.assertTrue(reg.is_current("df", g3))


class _Seams:
    """Recording fakes for the injectable IO seams."""

    def __init__(self):
        self.first_page = None
        self.pages = []
        self.manifests = []
        self.namespace = {}
        self.ready = []
        self.done = threading.Event()

    def display(self, df):
        self.first_page = df

    def assign(self, name, df):
        self.namespace[name] = df

    def write_page(self, uri, df):
        self.pages.append((uri, df))

    def write_manifest(self, uri, body):
        self.manifests.append(json.loads(body))

    def emit_ready(self, execution_id, status):
        self.ready.append((execution_id, status))
        self.done.set()


class MaterializeAsyncTest(unittest.TestCase):
    def test_full_run(self):
        seams = _Seams()
        registry = _MaterializationRegistry()
        payload = materialize_async(
            dataframe_name="df",
            columns=["a"],
            first_page_rows=[[1], [2], [3]],
            remaining_rows=iter([[[4], [5]]]),
            execution_id="exec-1",
            project_s3_root="s3://bkt/proj/dev",
            display_fn=seams.display,
            assign_namespace_fn=seams.assign,
            write_page_fn=seams.write_page,
            write_manifest_fn=seams.write_manifest,
            emit_ready_fn=seams.emit_ready,
            registry=registry,
            rows_per_page=2,
        )
        self.assertEqual(
            payload,
            {
                "execution_id": "exec-1",
                "s3_path": "s3://bkt/proj/dev/results/exec-1/",
                "total_rows": None,
            },
        )
        self.assertTrue(seams.done.wait(5), "background thread did not finish")

        # first page displayed inline as an AsyncSqlResult wrapper (3 fetched rows)
        self.assertIsInstance(seams.first_page, AsyncSqlResult)
        self.assertEqual(len(seams.first_page.first_page_rows), 3)
        # 5 rows / 2 per page -> 3 pages (2, 2, 1)
        self.assertEqual(
            [uri for uri, _ in seams.pages],
            [
                "s3://bkt/proj/dev/results/exec-1/page_000.parquet",
                "s3://bkt/proj/dev/results/exec-1/page_001.parquet",
                "s3://bkt/proj/dev/results/exec-1/page_002.parquet",
            ],
        )
        self.assertEqual([len(df) for _, df in seams.pages], [2, 2, 1])
        # final manifest is authoritative + complete
        self.assertEqual(
            seams.manifests[-1],
            {"totalfiles": 3, "rowPerPages": 2, "status": "complete", "row_count": 5},
        )
        # full DataFrame written to the namespace, in order
        self.assertEqual(seams.namespace["df"]["a"].tolist(), [1, 2, 3, 4, 5])
        self.assertEqual(seams.ready, [("exec-1", "success")])

    def test_superseded_run_emits_no_ready(self):
        seams = _Seams()
        registry = _MaterializationRegistry()
        gen, cancel = registry.start("df")
        registry.start("df")  # a newer run supersedes `gen`
        async_mod._background_materialize(
            dataframe_name="df",
            columns=["a"],
            first_page_rows=[[1], [2]],
            remaining_rows=iter([]),
            prefix="s3://b/results/e/",
            execution_id="e",
            gen=gen,
            cancel=cancel,  # note: superseding start() set this event
            registry=registry,
            rows_per_page=2,
            assign_namespace_fn=seams.assign,
            write_page_fn=seams.write_page,
            write_manifest_fn=seams.write_manifest,
            emit_ready_fn=seams.emit_ready,
        )
        # Superseded run does not write the namespace and emits NO dataframe_ready
        # (no live card to resolve). It writes a terminal manifest for S3 hygiene.
        self.assertNotIn("df", seams.namespace)
        self.assertEqual(seams.ready, [])
        self.assertEqual(seams.manifests[-1]["status"], async_mod.STATUS_FAILED)

    def test_cancelled_run_writes_terminal_manifest_no_ready(self):
        seams = _Seams()
        registry = _MaterializationRegistry()
        gen, cancel = registry.start("df2")
        cancel.set()
        async_mod._background_materialize(
            dataframe_name="df2",
            columns=["a"],
            first_page_rows=[[1], [2]],
            remaining_rows=iter([[[3], [4]]]),
            prefix="s3://b/results/e2/",
            execution_id="e2",
            gen=gen,
            cancel=cancel,
            registry=registry,
            rows_per_page=2,
            assign_namespace_fn=seams.assign,
            write_page_fn=seams.write_page,
            write_manifest_fn=seams.write_manifest,
            emit_ready_fn=seams.emit_ready,
        )
        self.assertTrue(seams.manifests)
        self.assertEqual(seams.manifests[-1]["status"], async_mod.STATUS_FAILED)
        self.assertNotIn("df2", seams.namespace)
        self.assertEqual(seams.ready, [])


class SpecFromResultTest(unittest.TestCase):
    class _R:
        def __init__(self, index, result):
            self.statement_index = index
            self.result = result

    def test_result_statement(self):
        s = spec_from_result(self._R(2, AsyncResultMarker(execution_id="e9")))
        self.assertEqual((s.index, s.kind, s.execution_id), (2, "result", "e9"))

    def test_dml_statement(self):
        s = spec_from_result(self._R(0, 7))
        self.assertEqual((s.index, s.kind, s.rowcount), (0, "dml", 7))


class MaterializeAsyncMultiTest(unittest.TestCase):
    def _run(self, specs, readers):
        # Synchronize on the consolidated `df` (base_name) bind itself. It is written in
        # on_settle (the finally), AFTER emit_ready, so waiting on emit_ready would race.
        seams = _Seams()
        bound = threading.Event()
        base_assign = seams.assign

        def assign(name, df):
            base_assign(name, df)
            if name == "df":
                bound.set()

        materialize_async_multi(
            base_name="df",
            specs=specs,
            project_s3_root="s3://bkt/p",
            reader_factory=lambda eid: readers[eid],
            display_fn=seams.display,
            assign_namespace_fn=assign,
            write_page_fn=seams.write_page,
            write_manifest_fn=seams.write_manifest,
            emit_ready_fn=seams.emit_ready,
            registry=_MaterializationRegistry(),
            rows_per_page=10000,
        )
        self.assertTrue(bound.wait(5), "consolidated df was not bound")
        return seams

    def test_multi_preserves_df_list(self):
        specs = [
            StatementSpec(index=0, kind="dml", rowcount=5),
            StatementSpec(index=1, kind="result", execution_id="e1"),
            StatementSpec(index=2, kind="result", execution_id="e2"),
        ]
        readers = {"e1": (["a"], [[1], [2]], iter([]), None), "e2": (["b"], [[9]], iter([]), None)}
        seams = self._run(specs, readers)

        self.assertEqual(seams.namespace["df_0"], 5)  # DML rowcount
        self.assertEqual(seams.namespace["df_1"]["a"].tolist(), [1, 2])
        self.assertEqual(seams.namespace["df_2"]["b"].tolist(), [9])
        df = seams.namespace["df"]
        self.assertIsInstance(df, list)
        self.assertEqual(df[0], 5)
        self.assertEqual(df[1]["a"].tolist(), [1, 2])
        self.assertEqual(df[2]["b"].tolist(), [9])

    def test_single_result_binds_base(self):
        specs = [StatementSpec(index=0, kind="result", execution_id="s1")]
        readers = {"s1": (["c"], [[7], [8]], iter([]), None)}
        seams = self._run(specs, readers)
        self.assertNotIn("df_0", seams.namespace)
        self.assertEqual(seams.namespace["df"]["c"].tolist(), [7, 8])

    def test_dml_only_single_binds_rowcount(self):
        # DML-only cell handled in-place (display + bind), returns [] (no async payloads).
        seams = _Seams()
        payloads = materialize_async_multi(
            base_name="df",
            specs=[StatementSpec(index=0, kind="dml", rowcount=1)],
            project_s3_root="s3://bkt/p",
            reader_factory=lambda eid: (["a"], [], iter([]), None),
            display_fn=seams.display,
            assign_namespace_fn=seams.assign,
            write_page_fn=seams.write_page,
            write_manifest_fn=seams.write_manifest,
            emit_ready_fn=seams.emit_ready,
        )
        self.assertEqual(payloads, [])
        self.assertEqual(seams.namespace["df"], 1)  # single DML -> df = rowcount

    def test_dml_only_multi_binds_list(self):
        seams = _Seams()
        payloads = materialize_async_multi(
            base_name="df",
            specs=[
                StatementSpec(index=0, kind="dml", rowcount=3),
                StatementSpec(index=1, kind="dml", rowcount=4),
            ],
            project_s3_root="s3://bkt/p",
            reader_factory=lambda eid: (["a"], [], iter([]), None),
            display_fn=seams.display,
            assign_namespace_fn=seams.assign,
            write_page_fn=seams.write_page,
            write_manifest_fn=seams.write_manifest,
            emit_ready_fn=seams.emit_ready,
        )
        self.assertEqual(payloads, [])
        self.assertEqual(seams.namespace["df_0"], 3)
        self.assertEqual(seams.namespace["df_1"], 4)
        self.assertEqual(seams.namespace["df"], [3, 4])

    def test_multi_barrier_settles_when_one_result_fails(self):
        # One result statement's background write fails; the barrier must still settle
        # (no hang) and bind the consolidated df from the successful subset.
        specs = [
            StatementSpec(index=0, kind="result", execution_id="ok"),
            StatementSpec(index=1, kind="result", execution_id="bad"),
        ]
        readers = {"ok": (["a"], [[1]], iter([]), None), "bad": (["b"], [[2]], iter([]), None)}
        seams = _Seams()
        bound = threading.Event()
        base_assign = seams.assign

        def assign(name, df):
            base_assign(name, df)
            if name == "df":
                bound.set()

        def failing_write_page(uri, df):
            if "bad" in uri:
                raise RuntimeError("boom")
            seams.write_page(uri, df)

        materialize_async_multi(
            base_name="df",
            specs=specs,
            project_s3_root="s3://bkt/p",
            reader_factory=lambda eid: readers[eid],
            display_fn=seams.display,
            assign_namespace_fn=assign,
            write_page_fn=failing_write_page,
            write_manifest_fn=seams.write_manifest,
            emit_ready_fn=seams.emit_ready,
            registry=_MaterializationRegistry(),
            rows_per_page=10000,
        )
        self.assertTrue(bound.wait(5), "barrier hung when one result failed")
        # Successful result is bound; failed one is not.
        self.assertIn("df_0", seams.namespace)
        self.assertNotIn("df_1", seams.namespace)
        # Consolidated df keeps positions aligned: failed statement 1 -> None hole.
        df = seams.namespace["df"]
        self.assertIsInstance(df, list)
        self.assertEqual(len(df), 2)
        self.assertEqual(df[0]["a"].tolist(), [1])
        self.assertIsNone(df[1])

    def test_multi_reader_open_failure_aborts_cleanly(self):
        # If a reader open raises during setup, no thread is spawned and nothing is
        # partially materialized -- the error propagates and the barrier is never armed.
        specs = [
            StatementSpec(index=0, kind="result", execution_id="ok"),
            StatementSpec(index=1, kind="result", execution_id="bad"),
        ]
        seams = _Seams()

        def reader_factory(eid):
            if eid == "bad":
                raise RuntimeError("reader open failed")
            return (["a"], [[1]], iter([]), None)

        with self.assertRaises(RuntimeError):
            materialize_async_multi(
                base_name="df",
                specs=specs,
                project_s3_root="s3://bkt/p",
                reader_factory=reader_factory,
                display_fn=seams.display,
                assign_namespace_fn=seams.assign,
                write_page_fn=seams.write_page,
                write_manifest_fn=seams.write_manifest,
                emit_ready_fn=seams.emit_ready,
                registry=_MaterializationRegistry(),
                rows_per_page=10000,
            )
        # nothing partially bound / written / signalled
        self.assertNotIn("df_0", seams.namespace)
        self.assertNotIn("df_1", seams.namespace)
        self.assertNotIn("df", seams.namespace)
        self.assertEqual(seams.pages, [])
        self.assertEqual(seams.ready, [])


class StreamMetadataCaptureTest(unittest.TestCase):
    """The async driver wraps executor.execute with _stream_and_capture_metadata so
    query-history metadata is populated like the sync path. Verify the capture works
    over async-shaped ExecutionResults (marker/rowcount payloads, execution_metadata
    accessed generically)."""

    class _FakeResult:
        def __init__(self, index, status="success"):
            self.statement_index = index
            self.statement = f"stmt{index}"
            self.status = status
            self.execution_metadata = None
            self.error = None

    def test_populates_last_sql_execution_metadata(self):
        from sagemaker_studio.utils import sqlutils

        stream = iter([self._FakeResult(0), self._FakeResult(1)])
        consumed = list(
            sqlutils._stream_and_capture_metadata(
                stream, connection_id="c1", connection_type="ATHENA"
            )
        )
        self.assertEqual(len(consumed), 2)  # stream yielded unchanged
        md = sqlutils._last_sql_execution_metadata
        self.assertEqual([e["statement_index"] for e in md], [0, 1])
        self.assertTrue(all(e.get("connection_type") == "ATHENA" for e in md))
        self.assertTrue(all(e.get("connection_id") == "c1" for e in md))


class AsyncDriverMetadataPropagationTest(unittest.TestCase):
    """Regression guard: the injected async per-statement executor must return a
    SingleStatementResult so the REAL SqlExecutor.execute_statements propagates
    execution_metadata into each ExecutionResult. Otherwise the driver's
    _stream_and_capture_metadata wrap records None and query-history metadata is
    silently lost on the async path (returning a bare marker regresses this)."""

    def test_execution_metadata_reaches_last_sql_execution_metadata(self):
        from types import SimpleNamespace
        from unittest.mock import patch

        from sagemaker_studio.sql_engine.sql_executor import SqlExecutor
        from sagemaker_studio.utils import sqlutils
        from sagemaker_studio.utils import sqlutils_async as _async

        metadata = {"query_execution_id": "athena-query-123", "data_scanned_bytes": 42}

        # Minimal SQLAlchemy stand-ins: the real execute_statements loop drives our
        # injected executor against these; connection.execute returns a result whose
        # cursor the (faked) transformer reads metadata from.
        class _FakeResult:
            returns_rows = True
            rowcount = -1
            cursor = object()

        class _FakeConn:
            def execute(self, *a, **k):
                return _FakeResult()

            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

        class _FakeEngine:
            def get_execution_options(self):
                return {"connection_type": "ATHENA"}

            def connect(self):
                return _FakeConn()

        fake_transformer = SimpleNamespace(
            split_query=lambda q: [SimpleNamespace(statement=q, statement_type="SELECT")],
            get_execution_metadata=lambda cursor: dict(metadata),
        )
        executor = SqlExecutor()
        executor._get_transformer = lambda ct: fake_transformer  # type: ignore[assignment]

        cached = SimpleNamespace(engine=_FakeEngine())
        project = SimpleNamespace(s3=SimpleNamespace(root="s3://bucket/proj"))
        resolved = SimpleNamespace(type="ATHENA")

        with patch.object(sqlutils, "_is_spark_connection", return_value=False), patch.object(
            sqlutils, "_resolve_connection", return_value=resolved
        ), patch.object(sqlutils, "_apply_athena_context"), patch.object(
            sqlutils, "_get_or_create_connection", return_value=cached
        ), patch.object(
            sqlutils, "_ensure_project", return_value=project
        ), patch.object(
            sqlutils, "_ensure_sql_executor", return_value=executor
        ), patch.object(
            _async, "materialize_async_multi"
        ) as mock_mat:
            handled = sqlutils._stream_with_async_materialization(
                "SELECT 1", "df", connection_id="c1"
            )

        self.assertTrue(handled)
        mock_mat.assert_called_once()  # reached materialization -> metadata already captured
        md = sqlutils._last_sql_execution_metadata
        self.assertEqual(len(md), 1)
        self.assertEqual(md[0]["execution_metadata"], metadata)
        self.assertEqual(md[0]["connection_type"], "ATHENA")
        self.assertEqual(md[0]["connection_id"], "c1")


class AsyncSqlResultTest(unittest.TestCase):
    """The first-page display object emits the async mimetype carrying the sync-reply
    payload + the inline first page, and (being non-DataFrame) bypasses the kernel's
    _LargeDataframeFormatter."""

    def test_repr_mimebundle_carries_payload_and_first_page(self):
        from unittest.mock import patch

        from sagemaker_studio.utils.sqlutils_async import ASYNC_SQL_MIMETYPE

        result = AsyncSqlResult(
            execution_id="exec-9",
            s3_path="s3://bkt/proj/results/exec-9/",
            columns=["a"],
            first_page_rows=[[1], [2]],
            total_rows=42,
        )
        # Patch the parquet serialization (pyarrow) so the test does not depend on it;
        # the real base64-parquet encoding runs in the kernel where pyarrow is present.
        with patch.object(AsyncSqlResult, "_first_page_parquet_b64", return_value="<b64>"):
            bundle = result._repr_mimebundle_()
        self.assertIn(ASYNC_SQL_MIMETYPE, bundle)
        payload = bundle[ASYNC_SQL_MIMETYPE]
        self.assertEqual(payload["execution_id"], "exec-9")
        self.assertEqual(payload["s3_path"], "s3://bkt/proj/results/exec-9/")
        self.assertEqual(payload["total_rows"], 42)
        self.assertEqual(payload["data"], "<b64>")  # base64 snappy-parquet of the first page
        self.assertIn("text/plain", bundle)


class TotalRowsThreadingTest(unittest.TestCase):
    """total_rows from the reader (Redshift TotalNumRows) flows through
    materialize_async_multi into the first-page payload; None (Athena) passes through."""

    def test_reader_total_rows_flows_into_payload(self):
        seams = _Seams()
        payloads = materialize_async_multi(
            base_name="df",
            specs=[StatementSpec(index=0, kind="result", execution_id="s1")],
            project_s3_root="s3://bkt/p",
            reader_factory=lambda eid: (["a"], [[1]], iter([]), 123),
            display_fn=seams.display,
            assign_namespace_fn=seams.assign,
            write_page_fn=seams.write_page,
            write_manifest_fn=seams.write_manifest,
            emit_ready_fn=seams.emit_ready,
            registry=_MaterializationRegistry(),
            rows_per_page=10000,
        )
        self.assertEqual(len(payloads), 1)
        self.assertEqual(payloads[0]["total_rows"], 123)
        self.assertEqual(payloads[0]["execution_id"], "s1")


class AtexitFlushTest(unittest.TestCase):
    """flush_inflight_on_exit finalizes runs whose background thread never reached its
    finally (graceful shutdown), and is a no-op for runs that completed normally."""

    def test_flush_finalizes_inflight_run(self):
        registry = _MaterializationRegistry()
        seams = _Seams()
        manifest = async_mod.Manifest(rowPerPages=async_mod.ROWS_PER_PAGE)
        registry.mark_inflight(
            ("df", 1),
            async_mod._InFlightRun(
                execution_id="e1",
                prefix="s3://b/results/e1/",
                manifest=manifest,
                write_manifest_fn=seams.write_manifest,
                emit_ready_fn=seams.emit_ready,
            ),
        )
        registry.flush_inflight_on_exit()
        self.assertEqual(seams.manifests[-1]["status"], async_mod.STATUS_FAILED)
        self.assertEqual(seams.ready, [("e1", async_mod.READY_FAILED)])
        # idempotent: the run was cleared, so a second flush emits nothing more
        registry.flush_inflight_on_exit()
        self.assertEqual(seams.ready, [("e1", async_mod.READY_FAILED)])

    def test_completed_run_leaves_nothing_to_flush(self):
        registry = _MaterializationRegistry()
        seams = _Seams()
        gen, cancel = registry.start("df")
        async_mod._background_materialize(
            dataframe_name="df",
            columns=["a"],
            first_page_rows=[[1]],
            remaining_rows=iter([]),
            prefix="s3://b/results/e/",
            execution_id="e",
            gen=gen,
            cancel=cancel,
            registry=registry,
            rows_per_page=2,
            assign_namespace_fn=seams.assign,
            write_page_fn=seams.write_page,
            write_manifest_fn=seams.write_manifest,
            emit_ready_fn=seams.emit_ready,
        )
        # run completed -> finally cleared inflight -> flush is a no-op (no extra emit)
        ready_after_run = list(seams.ready)
        registry.flush_inflight_on_exit()
        self.assertEqual(seams.ready, ready_after_run)


class ParquetColumnTransformTest(unittest.TestCase):
    """Parity with the kernel formatter: nested (dict/list) columns are JSON-stringified
    and dotted names are escaped with a mapping, before Parquet serialization."""

    def test_flatten_nested_columns(self):
        import pandas as pd

        df = pd.DataFrame({"id": [1, 2], "meta": [{"a": 1}, {"b": 2}], "tags": [["x", "y"], ["z"]]})
        out = async_mod._flatten_nested_columns(df)
        self.assertEqual(out["id"].tolist(), [1, 2])  # scalar column untouched
        self.assertEqual(out["meta"].tolist(), ['{"a": 1}', '{"b": 2}'])
        self.assertEqual(out["tags"].tolist(), ['["x", "y"]', '["z"]'])

    def test_flatten_no_nested_is_noop(self):
        import pandas as pd

        df = pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})
        self.assertIs(async_mod._flatten_nested_columns(df), df)  # no copy when nothing nested

    def test_escape_dotted_columns(self):
        import pandas as pd

        df = pd.DataFrame({"a.b": [1], "c": [2]})
        out, mapping = async_mod._escape_dotted_columns(df)
        self.assertEqual(list(out.columns), ["a__DOT__b", "c"])
        self.assertEqual(mapping, {"a__DOT__b": "a.b"})

    def test_escape_no_dot_is_noop(self):
        import pandas as pd

        df = pd.DataFrame({"a": [1], "b": [2]})
        out, mapping = async_mod._escape_dotted_columns(df)
        self.assertIs(out, df)
        self.assertEqual(mapping, {})


class ParseS3UriTest(unittest.TestCase):
    def test_valid_uri_splits_bucket_and_key(self):
        self.assertEqual(
            async_mod._parse_s3_uri("s3://my-bucket/results/exec-1/page_000.parquet"),
            ("my-bucket", "results/exec-1/page_000.parquet"),
        )

    def test_bucket_only_uri_has_empty_key(self):
        self.assertEqual(async_mod._parse_s3_uri("s3://my-bucket/"), ("my-bucket", ""))

    def test_non_s3_uri_raises(self):
        with self.assertRaises(ValueError):
            async_mod._parse_s3_uri("https://example.com/x")


class DfToParquetBytesTest(unittest.TestCase):
    """The serialized page/first-page must decode in the UI with the same transforms the
    kernel formatter applies: nested columns JSON-stringified, dotted names escaped, and
    the escaped->original mapping recorded in the Parquet key-value metadata."""

    def test_round_trip_flattens_nested_and_escapes_dotted(self):
        import io

        import pandas as pd
        import pyarrow.parquet as pq

        df = pd.DataFrame({"plain": [1, 2], "a.b": ["x", "y"], "nested": [{"k": 1}, [1, 2]]})
        data = async_mod._df_to_parquet_bytes(df)

        back = pd.read_parquet(io.BytesIO(data))
        # dotted column escaped; nested values JSON-stringified; scalars preserved
        self.assertIn("a__DOT__b", back.columns)
        self.assertNotIn("a.b", back.columns)
        self.assertEqual(back["nested"].tolist(), ['{"k": 1}', "[1, 2]"])
        self.assertEqual(back["plain"].tolist(), [1, 2])
        # escaped->original mapping recorded for the UI to un-escape
        meta = pq.read_table(io.BytesIO(data)).schema.metadata or {}
        self.assertIn(b"column_name_mapping", meta)
        self.assertEqual(json.loads(meta[b"column_name_mapping"]), {"a__DOT__b": "a.b"})

    def test_round_trip_no_transforms_is_noop(self):
        import io

        import pandas as pd
        import pyarrow.parquet as pq

        df = pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})
        data = async_mod._df_to_parquet_bytes(df)
        back = pd.read_parquet(io.BytesIO(data))
        self.assertEqual(list(back.columns), ["a", "b"])
        self.assertEqual(back["a"].tolist(), [1, 2])
        meta = pq.read_table(io.BytesIO(data)).schema.metadata or {}
        self.assertNotIn(b"column_name_mapping", meta)


class DefaultS3SeamTest(unittest.TestCase):
    def setUp(self):
        async_mod._s3_client = None

    def tearDown(self):
        async_mod._s3_client = None

    def test_get_s3_client_is_created_once_and_cached(self):
        fake = object()
        with mock.patch("boto3.client", return_value=fake) as mk:
            first = async_mod._get_s3_client()
            second = async_mod._get_s3_client()
        self.assertIs(first, fake)
        self.assertIs(second, fake)
        mk.assert_called_once_with("s3")

    def test_write_page_puts_parquet_bytes_at_parsed_key(self):
        import pandas as pd

        client = mock.MagicMock()
        async_mod._s3_client = client
        async_mod._default_write_page(
            "s3://bkt/results/e/page_000.parquet", pd.DataFrame({"a": [1, 2]})
        )
        client.put_object.assert_called_once()
        kwargs = client.put_object.call_args.kwargs
        self.assertEqual(kwargs["Bucket"], "bkt")
        self.assertEqual(kwargs["Key"], "results/e/page_000.parquet")
        self.assertIsInstance(kwargs["Body"], (bytes, bytearray))

    def test_write_manifest_puts_utf8_json_body(self):
        client = mock.MagicMock()
        async_mod._s3_client = client
        async_mod._default_write_manifest(
            "s3://bkt/results/e/_manifest.json", '{"status": "complete"}'
        )
        kwargs = client.put_object.call_args.kwargs
        self.assertEqual(kwargs["Bucket"], "bkt")
        self.assertEqual(kwargs["Key"], "results/e/_manifest.json")
        self.assertEqual(kwargs["Body"], b'{"status": "complete"}')


class DefaultIPythonSeamTest(unittest.TestCase):
    # IPython is a lazy runtime import (kernel-provided), not a build dependency, so it is
    # absent from the test env. Inject fake IPython modules into sys.modules so the seams'
    # `from IPython import ...` resolves without the real package installed.
    def setUp(self):
        self.fake_ip = mock.MagicMock()
        self.ipython_mod = mock.MagicMock()
        self.ipython_mod.get_ipython.return_value = self.fake_ip
        self.display_mod = mock.MagicMock()
        patcher = mock.patch.dict(
            sys.modules,
            {"IPython": self.ipython_mod, "IPython.display": self.display_mod},
        )
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_assign_namespace_sets_user_ns(self):
        self.fake_ip.user_ns = {}
        async_mod._default_assign_namespace("df", 123)
        self.assertEqual(self.fake_ip.user_ns["df"], 123)

    def test_assign_namespace_no_ipython_is_noop(self):
        self.ipython_mod.get_ipython.return_value = None
        async_mod._default_assign_namespace("df", 123)  # must not raise

    def test_display_invokes_ipython_display(self):
        async_mod._default_display("obj")
        self.display_mod.display.assert_called_once_with("obj")


class DefaultEmitDataframeReadyTest(unittest.TestCase):
    def setUp(self):
        self.ipython_mod = mock.MagicMock()
        patcher = mock.patch.dict(sys.modules, {"IPython": self.ipython_mod})
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_emits_on_iopub_when_kernel_present(self):
        kernel = mock.MagicMock()
        kernel.iopub_socket = "sock"
        kernel._parent_header = {"h": 1}
        fake_ip = mock.MagicMock()
        fake_ip.kernel = kernel
        self.ipython_mod.get_ipython.return_value = fake_ip
        async_mod._default_emit_dataframe_ready("exec-1", async_mod.READY_SUCCESS)
        kernel.session.send.assert_called_once()
        args, kwargs = kernel.session.send.call_args
        self.assertEqual(args[0], "sock")
        self.assertEqual(args[1], "dataframe_ready")
        self.assertEqual(kwargs["content"], {"execution_id": "exec-1", "status": "success"})
        self.assertEqual(kwargs["parent"], {"h": 1})

    def test_no_kernel_does_not_send(self):
        fake_ip = mock.MagicMock()
        fake_ip.kernel = None
        self.ipython_mod.get_ipython.return_value = fake_ip
        async_mod._default_emit_dataframe_ready("exec-1", async_mod.READY_SUCCESS)  # no raise

    def test_send_exception_is_swallowed(self):
        fake_ip = mock.MagicMock()
        fake_ip.kernel.session.send.side_effect = RuntimeError("boom")
        self.ipython_mod.get_ipython.return_value = fake_ip
        async_mod._default_emit_dataframe_ready("exec-1", async_mod.READY_FAILED)  # no raise


class BackgroundMaterializeFailureTest(unittest.TestCase):
    """A mid-materialize exception must write a terminal failed manifest, leave the
    namespace unbound, and emit dataframe_ready(failed) so the UI can recover."""

    def test_write_page_exception_writes_failed_manifest_and_emits_failed(self):
        seams = _Seams()
        registry = _MaterializationRegistry()
        gen, cancel = registry.start("df")

        def boom(_uri, _df):
            raise RuntimeError("s3 down")

        async_mod._background_materialize(
            dataframe_name="df",
            columns=["a"],
            first_page_rows=[[1], [2]],
            remaining_rows=iter([]),
            prefix="s3://b/results/e/",
            execution_id="e",
            gen=gen,
            cancel=cancel,
            registry=registry,
            rows_per_page=2,
            assign_namespace_fn=seams.assign,
            write_page_fn=boom,
            write_manifest_fn=seams.write_manifest,
            emit_ready_fn=seams.emit_ready,
        )
        self.assertEqual(seams.manifests[-1]["status"], async_mod.STATUS_FAILED)
        self.assertNotIn("df", seams.namespace)
        self.assertEqual(seams.ready, [("e", async_mod.READY_FAILED)])

    def test_flush_claimed_run_makes_later_failed_emit_stand_down(self):
        # r3p24: the failure path must be single-owner like the success path. If flush
        # already claimed + emitted failed at shutdown, a daemon except reaching
        # claim_terminal for the same run gets False -> no duplicate dataframe_ready(failed).
        registry = _MaterializationRegistry()
        seams = _Seams()
        gen, _cancel = registry.start("df")
        key = ("df", gen)
        registry.mark_inflight(
            key,
            async_mod._InFlightRun(
                execution_id="e1",
                prefix="s3://b/results/e1/",
                manifest=async_mod.Manifest(rowPerPages=async_mod.ROWS_PER_PAGE),
                write_manifest_fn=seams.write_manifest,
                emit_ready_fn=seams.emit_ready,
            ),
        )
        registry.flush_inflight_on_exit()  # flush claims + emits failed
        self.assertEqual(seams.ready, [("e1", async_mod.READY_FAILED)])
        # daemon except reaches claim_terminal for the SAME run -> already popped -> False
        self.assertFalse(registry.claim_terminal(key))
        self.assertEqual(seams.ready, [("e1", async_mod.READY_FAILED)])  # no duplicate

    def test_claim_terminal_true_when_owned_and_none_key(self):
        registry = _MaterializationRegistry()
        gen, _cancel = registry.start("df")
        key = ("df", gen)
        registry.mark_inflight(
            key,
            async_mod._InFlightRun(
                execution_id="e",
                prefix="s3://b/",
                manifest=async_mod.Manifest(),
                write_manifest_fn=lambda *_: None,
                emit_ready_fn=lambda *_: None,
            ),
        )
        self.assertTrue(registry.claim_terminal(key))  # owned -> wins the claim
        self.assertFalse(registry.claim_terminal(key))  # second caller loses
        self.assertTrue(registry.claim_terminal(None))  # untracked run always emits once


class MultiResultAlignmentTest(unittest.TestCase):
    """A middle result statement failing must leave a None hole at its position, not
    left-shift later results (which would desync df[i] from the df_i bindings)."""

    def test_middle_result_failure_keeps_positions_aligned(self):
        specs = [
            StatementSpec(index=0, kind="result", execution_id="e0"),
            StatementSpec(index=1, kind="result", execution_id="e1"),
            StatementSpec(index=2, kind="result", execution_id="e2"),
        ]
        readers = {
            "e0": (["a"], [[10]], iter([]), None),
            "e1": (["a"], [[20]], iter([]), None),
            "e2": (["a"], [[30]], iter([]), None),
        }
        seams = _Seams()
        bound = threading.Event()
        base_assign = seams.assign

        def assign(name, df):
            base_assign(name, df)
            if name == "df":
                bound.set()

        def failing_write_page(uri, df):
            if "e1" in uri:  # the MIDDLE statement fails
                raise RuntimeError("boom")
            seams.write_page(uri, df)

        materialize_async_multi(
            base_name="df",
            specs=specs,
            project_s3_root="s3://bkt/p",
            reader_factory=lambda eid: readers[eid],
            display_fn=seams.display,
            assign_namespace_fn=assign,
            write_page_fn=failing_write_page,
            write_manifest_fn=seams.write_manifest,
            emit_ready_fn=seams.emit_ready,
            registry=_MaterializationRegistry(),
            rows_per_page=10000,
        )
        self.assertTrue(bound.wait(5), "barrier hung on middle-result failure")
        df = seams.namespace["df"]
        self.assertEqual(len(df), 3)
        # position 1 (failed) is a None hole; 0 and 2 keep their statement positions
        self.assertIsNone(df[1])
        self.assertEqual(df[0]["a"].tolist(), [10])
        self.assertEqual(df[2]["a"].tolist(), [30])
        # df[i] matches df_i (no left-shift); failed df_1 is unbound
        self.assertNotIn("df_1", seams.namespace)
        self.assertEqual(df[0]["a"].tolist(), seams.namespace["df_0"]["a"].tolist())
        self.assertEqual(df[2]["a"].tolist(), seams.namespace["df_2"]["a"].tolist())


class CommitClearsInflightTest(unittest.TestCase):
    """A run that commits successfully is removed from _inflight under the registry lock,
    so a racing atexit flush at shutdown cannot re-finalize it as failed."""

    def test_commit_clears_inflight_so_flush_cannot_refinalize(self):
        registry = _MaterializationRegistry()
        seams = _Seams()
        gen, _cancel = registry.start("df")
        key = ("df", gen)
        registry.mark_inflight(
            key,
            async_mod._InFlightRun(
                execution_id="e1",
                prefix="s3://b/results/e1/",
                manifest=async_mod.Manifest(rowPerPages=async_mod.ROWS_PER_PAGE),
                write_manifest_fn=seams.write_manifest,
                emit_ready_fn=seams.emit_ready,
            ),
        )
        ran = registry.commit("df", gen, lambda: None, inflight_key=key)
        self.assertTrue(ran)
        # shutdown flush now finds nothing -> no contradictory dataframe_ready(failed)
        registry.flush_inflight_on_exit()
        self.assertEqual(seams.ready, [])

    def test_flush_skips_already_terminal_run(self):
        # B2 hardening: a failed/superseded run that set a terminal manifest status but
        # whose clear_inflight raced the flush must NOT be re-finalized (no duplicate
        # failed manifest write, no duplicate dataframe_ready(failed)).
        registry = _MaterializationRegistry()
        seams = _Seams()
        manifest = async_mod.Manifest(rowPerPages=async_mod.ROWS_PER_PAGE)
        manifest.status = async_mod.STATUS_FAILED  # terminal already reached by the run
        registry.mark_inflight(
            ("df", 1),
            async_mod._InFlightRun(
                execution_id="e1",
                prefix="s3://b/results/e1/",
                manifest=manifest,
                write_manifest_fn=seams.write_manifest,
                emit_ready_fn=seams.emit_ready,
            ),
        )
        registry.flush_inflight_on_exit()
        self.assertEqual(seams.manifests, [])  # no re-write
        self.assertEqual(seams.ready, [])  # no duplicate failed emit

    def test_flush_does_not_clobber_completed_run(self):
        # r3p8: a run that reached COMPLETE must never be re-finalized to FAILED by the
        # flush (the transition decision is made under the lock against terminal status).
        registry = _MaterializationRegistry()
        seams = _Seams()
        manifest = async_mod.Manifest(rowPerPages=async_mod.ROWS_PER_PAGE)
        manifest.status = async_mod.STATUS_COMPLETE
        registry.mark_inflight(
            ("df", 1),
            async_mod._InFlightRun(
                execution_id="e1",
                prefix="s3://b/results/e1/",
                manifest=manifest,
                write_manifest_fn=seams.write_manifest,
                emit_ready_fn=seams.emit_ready,
            ),
        )
        registry.flush_inflight_on_exit()
        self.assertEqual(manifest.status, async_mod.STATUS_COMPLETE)  # not clobbered
        self.assertEqual(seams.ready, [])


class AthenaCoerceParityTest(unittest.TestCase):
    """The async Athena reader must coerce to the same Python types the sync PyAthena
    driver yields, so a query's column dtypes match between materialize modes."""

    def test_numeric_and_boolean(self):
        self.assertEqual(reader_mod._athena_coerce("42", "bigint"), 42)
        self.assertEqual(reader_mod._athena_coerce("3.5", "double"), 3.5)
        self.assertIs(reader_mod._athena_coerce("true", "boolean"), True)
        self.assertIs(reader_mod._athena_coerce("false", "boolean"), False)

    def test_decimal_is_exact_decimal(self):
        import decimal

        v = reader_mod._athena_coerce("10.50", "decimal")
        self.assertIsInstance(v, decimal.Decimal)
        self.assertEqual(v, decimal.Decimal("10.50"))
        # parameterized type name (decimal(p,s)) also handled
        self.assertIsInstance(reader_mod._athena_coerce("1.0", "decimal(10,2)"), decimal.Decimal)

    def test_date_is_date(self):
        import datetime as dt

        self.assertEqual(reader_mod._athena_coerce("2024-01-15", "date"), dt.date(2024, 1, 15))

    def test_timestamp_is_datetime(self):
        import datetime as dt

        # PyAthena's _to_datetime requires the fractional-seconds form.
        self.assertEqual(
            reader_mod._athena_coerce("2024-01-15 10:30:00.000", "timestamp"),
            dt.datetime(2024, 1, 15, 10, 30, 0),
        )

    def test_none_and_unparseable_fall_back(self):
        self.assertIsNone(reader_mod._athena_coerce(None, "date"))
        # unparseable stays a string (graceful, no crash)
        self.assertEqual(reader_mod._athena_coerce("not-a-date", "date"), "not-a-date")

    def test_varchar_kept_as_string(self):
        self.assertEqual(reader_mod._athena_coerce("hello", "varchar"), "hello")
        self.assertEqual(reader_mod._athena_coerce("hello", "char"), "hello")

    def test_time_is_time(self):
        import datetime as dt

        # PyAthena's _to_time requires the fractional-seconds form.
        self.assertEqual(reader_mod._athena_coerce("10:30:00.000", "time"), dt.time(10, 30, 0))

    def test_timestamp_with_tz_matches_pyathena(self):
        import datetime as dt

        # Delegates to PyAthena's _to_datetime_with_tz (dateutil gettz): a NAMED zone
        # resolves to a tz-aware datetime; a bare numeric offset is not a gettz zone name,
        # so it yields a naive datetime. We assert parity with sync, not our own scheme.
        named = reader_mod._athena_coerce("2024-01-15 10:30:00.000 UTC", "timestamp with time zone")
        self.assertIsInstance(named, dt.datetime)
        self.assertIsNotNone(named.tzinfo)

    def test_time_with_tz_matches_sync_string_fallback(self):
        # PyAthena has NO converter for "time with time zone" -> its default converter
        # leaves it a string. True parity = string (our old hand-roll wrongly typed it).
        v = reader_mod._athena_coerce("10:30:00.000 +00:00", "time with time zone")
        self.assertEqual(v, "10:30:00.000 +00:00")

    def test_varbinary_is_bytes(self):
        self.assertEqual(reader_mod._athena_coerce("de ad be ef", "varbinary"), b"\xde\xad\xbe\xef")

    def test_unparseable_new_types_fall_back(self):
        self.assertEqual(reader_mod._athena_coerce("nope", "time"), "nope")
        self.assertEqual(reader_mod._athena_coerce("xyz", "varbinary"), "xyz")

    def test_read_athena_result_rows_are_typed(self):
        import datetime as dt
        import decimal

        client = mock.MagicMock()
        client.get_query_results.return_value = {
            "ResultSet": {
                "ResultSetMetadata": {
                    "ColumnInfo": [
                        {"Name": "d", "Type": "date"},
                        {"Name": "amt", "Type": "decimal"},
                    ]
                },
                "Rows": [
                    {"Data": [{"VarCharValue": "d"}, {"VarCharValue": "amt"}]},  # header echo
                    {"Data": [{"VarCharValue": "2024-01-15"}, {"VarCharValue": "10.50"}]},
                ],
            }
        }
        columns, chunks, total = reader_mod.read_athena_result(client, "qid")
        self.assertEqual(columns, ["d", "amt"])
        self.assertIsNone(total)
        rows = list(chunks)[0]
        self.assertEqual(rows[0][0], dt.date(2024, 1, 15))
        self.assertIsInstance(rows[0][1], decimal.Decimal)


class MultiSpawnFailureTest(unittest.TestCase):
    """r3p10: if materialize_async raises mid spawn-loop after earlier specs armed the
    barrier, the barrier must still settle (bind the consolidated df) rather than hang."""

    def test_empty_execution_id_is_rejected_before_arming(self):
        specs = [StatementSpec(index=0, kind="result", execution_id="")]
        with self.assertRaises(RuntimeError):
            materialize_async_multi(
                base_name="df",
                specs=specs,
                project_s3_root="s3://bkt/p",
                reader_factory=lambda eid: (["a"], [[1]], iter([]), None),
                display_fn=lambda *_: None,
                assign_namespace_fn=lambda *_: None,
                write_page_fn=lambda *_: None,
                write_manifest_fn=lambda *_: None,
                emit_ready_fn=lambda *_: None,
                registry=_MaterializationRegistry(),
            )

    def test_spawn_failure_settles_barrier_no_hang(self):
        specs = [
            StatementSpec(index=0, kind="result", execution_id="e0"),
            StatementSpec(index=1, kind="result", execution_id="e1"),
        ]
        readers = {
            "e0": (["a"], [[10]], iter([]), None),
            "e1": (["a"], [[20]], iter([]), None),
        }
        seams = _Seams()
        bound = threading.Event()
        base_assign = seams.assign

        def assign(name, df):
            base_assign(name, df)
            if name == "df":
                bound.set()

        real_materialize = async_mod.materialize_async
        calls = [0]

        def flaky_materialize(*args, **kwargs):
            calls[0] += 1
            if calls[0] == 2:  # second spec's spawn blows up AFTER the first armed/settled
                raise RuntimeError("spawn boom")
            return real_materialize(*args, **kwargs)

        with mock.patch.object(async_mod, "materialize_async", side_effect=flaky_materialize):
            materialize_async_multi(
                base_name="df",
                specs=specs,
                project_s3_root="s3://bkt/p",
                reader_factory=lambda eid: readers[eid],
                display_fn=seams.display,
                assign_namespace_fn=assign,
                write_page_fn=seams.write_page,
                write_manifest_fn=seams.write_manifest,
                emit_ready_fn=seams.emit_ready,
                registry=_MaterializationRegistry(),
                rows_per_page=10000,
            )
        self.assertTrue(bound.wait(5), "barrier hung after a mid-loop spawn failure")
        df = seams.namespace["df"]
        self.assertEqual(len(df), 2)
        self.assertEqual(df[0]["a"].tolist(), [10])  # spec 0 succeeded
        self.assertIsNone(df[1])  # spec 1 spawn failed -> None hole
        # r3p23: the failed spec's already-displayed card must be resolved via a failed
        # dataframe_ready (spec 1's execution_id e1), not left waiting forever.
        self.assertIn(("e1", async_mod.READY_FAILED), seams.ready)


class AthenaHeaderDetectionTest(unittest.TestCase):
    """r3p22: header-skip is driven by the caller's statement-type decision (skip_header),
    NOT by comparing row-0 values to column names -- so a legitimate first row whose values
    equal the column labels is never dropped."""

    def _client(self, rows):
        client = mock.MagicMock()
        client.get_query_results.return_value = {
            "ResultSet": {
                "ResultSetMetadata": {"ColumnInfo": [{"Name": "c", "Type": "varchar"}]},
                "Rows": rows,
            }
        }
        return client

    def test_skip_header_true_drops_first_row(self):
        # SELECT/CTAS: caller passes skip_header=True (the default) -> row 0 echo dropped.
        client = self._client(
            [{"Data": [{"VarCharValue": "c"}]}, {"Data": [{"VarCharValue": "real"}]}]
        )
        _cols, chunks, _ = reader_mod.read_athena_result(client, "qid", skip_header=True)
        self.assertEqual(list(chunks)[0], [["real"]])

    def test_skip_header_false_keeps_all_rows(self):
        # Non-SELECT (SHOW/DESCRIBE): caller passes skip_header=False -> nothing dropped.
        client = self._client(
            [{"Data": [{"VarCharValue": "t1"}]}, {"Data": [{"VarCharValue": "t2"}]}]
        )
        _cols, chunks, _ = reader_mod.read_athena_result(client, "qid", skip_header=False)
        self.assertEqual(list(chunks)[0], [["t1"], ["t2"]])

    def test_value_matching_first_row_not_dropped(self):
        # The r3p22 bug: a real first row whose value equals the column name ("c") must NOT
        # be dropped. Value-based detection would have wrongly dropped it; skip_header only
        # drops exactly one row (the true header echo), keeping the rest verbatim.
        client = self._client(
            [
                {"Data": [{"VarCharValue": "c"}]},  # header echo (dropped)
                {"Data": [{"VarCharValue": "c"}]},  # REAL data row that equals the column name
                {"Data": [{"VarCharValue": "x"}]},
            ]
        )
        _cols, chunks, _ = reader_mod.read_athena_result(client, "qid", skip_header=True)
        self.assertEqual(list(chunks)[0], [["c"], ["x"]])  # only the first (header) dropped


class PartialBindTest(unittest.TestCase):
    """r3p9 option A: on a mid-cell async failure, the statements that already succeeded
    are sync-bound as df_<index> (matching the sync path's partial-save for debugging)."""

    def test_binds_result_and_dml_partials_into_namespace(self):
        from sagemaker_studio.utils import sqlutils

        specs = [
            async_mod.StatementSpec(index=0, kind="result", execution_id="e0"),
            async_mod.StatementSpec(index=1, kind="dml", rowcount=7),
        ]
        fake_ip = mock.MagicMock()
        fake_ip.user_ns = {}
        reader = (["a"], iter([[[1], [2]]]), None)  # (columns, chunk_iterator, total_rows)

        with mock.patch.dict(sys.modules, {"IPython": mock.MagicMock()}), mock.patch(
            "IPython.get_ipython", return_value=fake_ip
        ), mock.patch.object(reader_mod, "open_result_reader", return_value=reader):
            sqlutils._bind_succeeded_partials(specs, "df", object(), "ATHENA")

        # result statement -> DataFrame bound at df_0; dml -> rowcount at df_1
        self.assertIn("df_0", fake_ip.user_ns)
        self.assertEqual(fake_ip.user_ns["df_0"]["a"].tolist(), [1, 2])
        self.assertEqual(fake_ip.user_ns["df_1"], 7)

    def test_no_ipython_is_noop(self):
        from sagemaker_studio.utils import sqlutils

        with mock.patch.dict(sys.modules, {"IPython": mock.MagicMock()}), mock.patch(
            "IPython.get_ipython", return_value=None
        ):
            # must not raise even though a result spec is present
            sqlutils._bind_succeeded_partials(
                [async_mod.StatementSpec(index=0, kind="result", execution_id="e0")],
                "df",
                object(),
                "ATHENA",
            )

    def test_reader_failure_is_swallowed_not_masking_error(self):
        from sagemaker_studio.utils import sqlutils

        fake_ip = mock.MagicMock()
        fake_ip.user_ns = {}
        with mock.patch.dict(sys.modules, {"IPython": mock.MagicMock()}), mock.patch(
            "IPython.get_ipython", return_value=fake_ip
        ), mock.patch.object(reader_mod, "open_result_reader", side_effect=RuntimeError("boom")):
            # a failed partial bind must not raise (it would mask the real statement error)
            sqlutils._bind_succeeded_partials(
                [async_mod.StatementSpec(index=0, kind="result", execution_id="e0")],
                "df",
                object(),
                "ATHENA",
            )
        self.assertNotIn("df_0", fake_ip.user_ns)


class PostCommitManifestFailureTest(unittest.TestCase):
    """r3p15: if the COMPLETE manifest write (or success emit) raises AFTER the namespace
    commit, the run must stay a success -- df bound, NO dataframe_ready(failed)."""

    def test_complete_manifest_write_failure_after_commit_stays_success(self):
        seams = _Seams()
        registry = _MaterializationRegistry()
        gen, cancel = registry.start("df")

        # Fail only the terminal COMPLETE manifest write (status == complete), which runs
        # after commit; the in-progress page manifests must still succeed.
        def flaky_write_manifest(uri, body):
            if '"status": "complete"' in body or '"status":"complete"' in body:
                raise RuntimeError("s3 put failed")
            seams.write_manifest(uri, body)

        async_mod._background_materialize(
            dataframe_name="df",
            columns=["a"],
            first_page_rows=[[1], [2]],
            remaining_rows=iter([]),
            prefix="s3://b/results/e/",
            execution_id="e",
            gen=gen,
            cancel=cancel,
            registry=registry,
            rows_per_page=2,
            assign_namespace_fn=seams.assign,
            write_page_fn=seams.write_page,
            write_manifest_fn=flaky_write_manifest,
            emit_ready_fn=seams.emit_ready,
        )
        # df committed and correct even though the COMPLETE manifest write raised.
        # The manifest write precedes the success emit, so on its failure no emit fires at
        # all (card stays blue, reconciled by the UI stall timeout) -- crucially, NO failed
        # emit and the run is not downgraded.
        self.assertEqual(seams.namespace["df"]["a"].tolist(), [1, 2])
        self.assertNotIn(("e", async_mod.READY_FAILED), seams.ready)

    def test_success_emit_failure_after_commit_does_not_emit_failed(self):
        seams = _Seams()
        registry = _MaterializationRegistry()
        gen, cancel = registry.start("df")

        emits = []

        def flaky_emit(execution_id, status):
            emits.append((execution_id, status))
            if status == async_mod.READY_SUCCESS:
                raise RuntimeError("ws push failed")

        async_mod._background_materialize(
            dataframe_name="df",
            columns=["a"],
            first_page_rows=[[1]],
            remaining_rows=iter([]),
            prefix="s3://b/results/e/",
            execution_id="e",
            gen=gen,
            cancel=cancel,
            registry=registry,
            rows_per_page=2,
            assign_namespace_fn=seams.assign,
            write_page_fn=seams.write_page,
            write_manifest_fn=seams.write_manifest,
            emit_ready_fn=flaky_emit,
        )
        # df committed; the failed success-emit is NOT followed by a failed emit.
        self.assertEqual(seams.namespace["df"]["a"].tolist(), [1])
        self.assertEqual(
            emits, [("e", async_mod.READY_SUCCESS)]
        )  # only the (failed) success attempt

    def test_flush_claimed_run_makes_later_commit_stand_down(self):
        # r3p16: flush and the daemon must not both finalize the same run. Flush removes
        # the inflight entry under the lock (emitting failed); a subsequent daemon commit
        # for that run must see the entry gone and return False -> stand down (no success).
        registry = _MaterializationRegistry()
        seams = _Seams()
        gen, _cancel = registry.start("df")
        key = ("df", gen)
        registry.mark_inflight(
            key,
            async_mod._InFlightRun(
                execution_id="e1",
                prefix="s3://b/results/e1/",
                manifest=async_mod.Manifest(rowPerPages=async_mod.ROWS_PER_PAGE),
                write_manifest_fn=seams.write_manifest,
                emit_ready_fn=seams.emit_ready,
            ),
        )
        # Flush claims the run first (shutdown), emitting failed and removing the entry.
        registry.flush_inflight_on_exit()
        self.assertEqual(seams.ready, [("e1", async_mod.READY_FAILED)])

        # Daemon then reaches commit for the SAME run: generation is still current (flush
        # does not bump it), but the inflight entry is gone -> commit must return False.
        bound = []
        ran = registry.commit("df", gen, lambda: bound.append(True), inflight_key=key)
        self.assertFalse(ran, "commit ran despite flush already claiming the run")
        self.assertEqual(bound, [])  # namespace NOT bound
        self.assertEqual(seams.ready, [("e1", async_mod.READY_FAILED)])  # no success emit added

    def test_commit_still_succeeds_when_flush_has_not_run(self):
        # Guard against over-tightening: a normal run (inflight entry present, generation
        # current) must still commit successfully.
        registry = _MaterializationRegistry()
        gen, _cancel = registry.start("df")
        key = ("df", gen)
        registry.mark_inflight(
            key,
            async_mod._InFlightRun(
                execution_id="e1",
                prefix="s3://b/results/e1/",
                manifest=async_mod.Manifest(rowPerPages=async_mod.ROWS_PER_PAGE),
                write_manifest_fn=lambda *_: None,
                emit_ready_fn=lambda *_: None,
            ),
        )
        bound = []
        ran = registry.commit("df", gen, lambda: bound.append(True), inflight_key=key)
        self.assertTrue(ran)
        self.assertEqual(bound, [True])


class RedshiftReaderTest(unittest.TestCase):
    """read_redshift_result: columns via ResultConverter, TotalNumRows -> total_rows,
    NextToken pagination, and typed record conversion."""

    def _client(self, pages):
        # pages: list of get_statement_result responses returned in sequence
        client = mock.MagicMock()
        client.get_statement_result.side_effect = pages
        return client

    def test_single_page_columns_total_and_typed_rows(self):
        client = self._client(
            [
                {
                    "ColumnMetadata": [
                        {"name": "id", "typeName": "int4"},
                        {"name": "name", "typeName": "varchar"},
                    ],
                    "TotalNumRows": 2,
                    "Records": [
                        [{"longValue": 1}, {"stringValue": "a"}],
                        [{"longValue": 2}, {"stringValue": "b"}],
                    ],
                }
            ]
        )
        columns, chunks, total = reader_mod.read_redshift_result(client, "sid")
        self.assertEqual(columns, ["id", "name"])
        self.assertEqual(total, 2)
        rows = [r for chunk in chunks for r in chunk]
        self.assertEqual(rows, [[1, "a"], [2, "b"]])  # ints typed, strings preserved

    def test_pagination_follows_next_token(self):
        client = self._client(
            [
                {
                    "ColumnMetadata": [{"name": "id", "typeName": "int4"}],
                    "TotalNumRows": 3,
                    "Records": [[{"longValue": 1}]],
                    "NextToken": "t1",
                },
                {"Records": [[{"longValue": 2}], [{"longValue": 3}]]},  # no NextToken -> stop
            ]
        )
        _cols, chunks, total = reader_mod.read_redshift_result(client, "sid")
        rows = [r for chunk in chunks for r in chunk]
        self.assertEqual(rows, [[1], [2], [3]])
        self.assertEqual(total, 3)
        self.assertEqual(client.get_statement_result.call_count, 2)

    def test_missing_or_negative_total_is_none(self):
        for bad_total in ({}, {"TotalNumRows": -1}):
            resp = {"ColumnMetadata": [{"name": "id", "typeName": "int4"}], "Records": []}
            resp.update(bad_total)
            _cols, _chunks, total = reader_mod.read_redshift_result(self._client([resp]), "sid")
            self.assertIsNone(total)


class OpenResultReaderDispatchTest(unittest.TestCase):
    def test_athena_dispatch_uses_athena_client(self):
        conn = mock.MagicMock()
        with mock.patch.object(
            reader_mod, "read_athena_result", return_value=(["c"], iter([]), None)
        ) as rd:
            reader_mod.open_result_reader(conn, "ATHENA", "qid")
        conn.create_client.assert_called_once_with("athena")
        rd.assert_called_once()

    def test_redshift_dispatch_uses_redshift_data_client(self):
        conn = mock.MagicMock()
        with mock.patch.object(
            reader_mod, "read_redshift_result", return_value=(["c"], iter([]), 0)
        ) as rd:
            reader_mod.open_result_reader(conn, "redshift", "sid")  # case-insensitive
        conn.create_client.assert_called_once_with("redshift-data")
        rd.assert_called_once()

    def test_unsupported_engine_raises(self):
        with self.assertRaises(ValueError):
            reader_mod.open_result_reader(mock.MagicMock(), "MYSQL", "x")


class SplitFirstPageTest(unittest.TestCase):
    def test_exact_fill_no_overflow(self):
        first, remaining = reader_mod.split_first_page(iter([[[1], [2]], [[3], [4]]]), 2)
        self.assertEqual(first, [[1], [2]])
        self.assertEqual([r for chunk in remaining for r in chunk], [[3], [4]])

    def test_overflow_from_last_chunk_is_prepended_to_remainder(self):
        # first chunk of 3 rows, page size 2 -> first page [1,2], overflow [3] leads remainder
        first, remaining = reader_mod.split_first_page(iter([[[1], [2], [3]], [[4]]]), 2)
        self.assertEqual(first, [[1], [2]])
        self.assertEqual([r for chunk in remaining for r in chunk], [[3], [4]])

    def test_fewer_rows_than_page_size(self):
        first, remaining = reader_mod.split_first_page(iter([[[1]]]), 10)
        self.assertEqual(first, [[1]])
        self.assertEqual([r for chunk in remaining for r in chunk], [])


class PersistSessionKwargTest(unittest.TestCase):
    """r3p7 + r3p21: the async driver must pass persist_session to the connection without
    a kwarg collision, AND without mutating the caller's kwargs (so a return-False fallback
    still forwards persist_session to the sync path)."""

    def _drive_until_connection(self, cached_return, kwargs):
        from sagemaker_studio.utils import sqlutils

        dz_conn = mock.MagicMock()
        dz_conn.type = "ATHENA"  # in ASYNC_SUPPORTED_CONNECTION_TYPES, not IRC-Glue
        with mock.patch.object(
            sqlutils, "_is_spark_connection", return_value=False
        ), mock.patch.object(
            sqlutils, "_resolve_connection", return_value=dz_conn
        ), mock.patch.object(
            sqlutils, "_apply_athena_context"
        ), mock.patch.object(
            sqlutils, "_get_or_create_connection", return_value=cached_return
        ) as goc:
            result = sqlutils._stream_with_async_materialization("SELECT 1", "df", **kwargs)
        return result, goc

    def test_persist_session_passed_explicitly_without_collision(self):
        kwargs = {"persist_session": False, "other": 1}
        # cached falsy -> hits `if not cached: return False` (async bails to sync).
        result, goc = self._drive_until_connection(None, kwargs)
        self.assertFalse(result)  # fell back to sync
        # connection call got persist_session explicitly, and NOT duplicated in **kwargs
        # (a duplicate would have raised TypeError -> no clean call recorded).
        _args, call_kwargs = goc.call_args
        self.assertEqual(call_kwargs["persist_session"], False)
        # persist_session is forwarded EXACTLY ONCE and as the explicit value (not shadowed
        # by a duplicate from **conn_kwargs): a real collision would raise TypeError at the
        # call site, so a clean recorded call_args already proves single-delivery. Assert the
        # OTHER caller kwarg is forwarded too, proving **conn_kwargs passes through intact
        # alongside the explicit persist_session rather than being dropped.
        self.assertEqual(call_kwargs.get("other"), 1)

    def test_caller_kwargs_not_mutated_on_fallback(self):
        kwargs = {"persist_session": True, "other": 1}
        self._drive_until_connection(None, kwargs)  # async bails to sync
        # r3p21: persist_session must still be present for the sync fallback's **kwargs.
        self.assertIn("persist_session", kwargs)
        self.assertEqual(kwargs["persist_session"], True)


class DefensiveSwallowBranchTest(unittest.TestCase):
    """Cover the best-effort exception-swallow branches so a failing IO seam degrades
    gracefully instead of propagating: the atexit finalizer's manifest-write and
    ready-emit swallows, _write_failed's manifest-write swallow, and materialize's
    on_settle swallow."""

    def test_atexit_flush_swallows_manifest_and_emit_failures(self):
        registry = _MaterializationRegistry()
        manifest = async_mod.Manifest(rowPerPages=async_mod.ROWS_PER_PAGE)

        def boom_manifest(_uri, _body):
            raise RuntimeError("manifest s3 down")

        def boom_emit(_eid, _status):
            raise RuntimeError("emit ws down")

        registry.mark_inflight(
            ("df", 1),
            async_mod._InFlightRun(
                execution_id="e1",
                prefix="s3://b/results/e1/",
                manifest=manifest,
                write_manifest_fn=boom_manifest,
                emit_ready_fn=boom_emit,
            ),
        )
        # Both seams raise; flush must NOT propagate (best-effort finalization at shutdown).
        registry.flush_inflight_on_exit()
        self.assertEqual(manifest.status, async_mod.STATUS_FAILED)  # still transitioned

    def test_write_failed_swallows_manifest_write_error(self):
        manifest = async_mod.Manifest(rowPerPages=async_mod.ROWS_PER_PAGE)

        def boom(_uri, _body):
            raise RuntimeError("s3 down")

        # Must not raise even though the manifest write fails.
        async_mod._write_failed(manifest, "s3://b/results/e/", boom)
        self.assertEqual(manifest.status, async_mod.STATUS_FAILED)

    def test_materialize_swallows_on_settle_failure(self):
        seams = _Seams()
        registry = _MaterializationRegistry()
        gen, cancel = registry.start("df")

        def boom_settle(_df):
            raise RuntimeError("barrier settle boom")

        # A raising on_settle must be swallowed in the finally (never breaks the run).
        async_mod._background_materialize(
            dataframe_name="df",
            columns=["a"],
            first_page_rows=[[1]],
            remaining_rows=iter([]),
            prefix="s3://b/results/e/",
            execution_id="e",
            gen=gen,
            cancel=cancel,
            registry=registry,
            rows_per_page=2,
            assign_namespace_fn=seams.assign,
            write_page_fn=seams.write_page,
            write_manifest_fn=seams.write_manifest,
            emit_ready_fn=seams.emit_ready,
            on_settle=boom_settle,
        )
        # Run still succeeded despite the settle callback raising.
        self.assertEqual(seams.namespace["df"]["a"].tolist(), [1])
        self.assertEqual(seams.ready, [("e", async_mod.READY_SUCCESS)])


class SqlStreamWithDisplayAsyncBranchTest(unittest.TestCase):
    """Cover the materialize="async" dispatch in the PUBLIC sql_stream_with_display entry
    point (both edges: async handled -> return; async declined -> fall through to sync)."""

    def test_async_handled_returns_without_sync_fallback(self):
        from sagemaker_studio.utils import sqlutils

        with mock.patch.object(
            sqlutils, "_stream_with_async_materialization", return_value=True
        ) as amat, mock.patch.object(sqlutils, "sql_stream") as sync_stream, mock.patch.object(
            sqlutils, "_materialise_stream"
        ) as materialise:
            sqlutils.sql_stream_with_display("SELECT 1", "df", materialize="async")
        amat.assert_called_once()
        sync_stream.assert_not_called()  # async handled -> no sync fallback
        materialise.assert_not_called()

    def test_async_declined_falls_through_to_sync(self):
        from sagemaker_studio.utils import sqlutils

        with mock.patch.object(
            sqlutils, "_stream_with_async_materialization", return_value=False
        ) as amat, mock.patch.object(
            sqlutils, "sql_stream", return_value=iter([])
        ) as sync_stream, mock.patch.object(
            sqlutils, "_materialise_stream"
        ) as materialise:
            sqlutils.sql_stream_with_display("SELECT 1", "df", materialize="async")
        amat.assert_called_once()
        sync_stream.assert_called_once()  # declined pre-execution -> sync path runs
        materialise.assert_called_once()

    def test_sync_materialize_skips_async_entirely(self):
        from sagemaker_studio.utils import sqlutils

        with mock.patch.object(
            sqlutils, "_stream_with_async_materialization"
        ) as amat, mock.patch.object(
            sqlutils, "sql_stream", return_value=iter([])
        ), mock.patch.object(
            sqlutils, "_materialise_stream"
        ):
            sqlutils.sql_stream_with_display("SELECT 1", "df")  # default materialize="sync"
        amat.assert_not_called()  # async dispatch not entered when materialize != "async"


class BindSucceededPartialsEdgeTest(unittest.TestCase):
    """Cover the remaining _bind_succeeded_partials branch edges: the IPython-import
    except path, and a result spec whose execution_id is falsy (elif short-circuits)."""

    def test_ipython_import_failure_returns_quietly(self):
        from sagemaker_studio.utils import sqlutils

        # Make `from IPython import get_ipython` raise -> the except returns without binding.
        real_import = __import__

        def blocking_import(name, *a, **k):
            if name == "IPython":
                raise ImportError("no IPython")
            return real_import(name, *a, **k)

        with mock.patch("builtins.__import__", side_effect=blocking_import):
            # must not raise despite a result spec being present
            sqlutils._bind_succeeded_partials(
                [async_mod.StatementSpec(index=0, kind="result", execution_id="e0")],
                "df",
                object(),
                "ATHENA",
            )

    def test_result_spec_without_execution_id_is_skipped(self):
        from sagemaker_studio.utils import sqlutils

        fake_ip = mock.MagicMock()
        fake_ip.user_ns = {}
        opened = mock.Mock()
        with mock.patch.dict(sys.modules, {"IPython": mock.MagicMock()}), mock.patch(
            "IPython.get_ipython", return_value=fake_ip
        ), mock.patch.object(reader_mod, "open_result_reader", opened):
            # result spec with empty execution_id -> elif condition False -> reader NOT opened
            sqlutils._bind_succeeded_partials(
                [async_mod.StatementSpec(index=0, kind="result", execution_id="")],
                "df",
                object(),
                "ATHENA",
            )
        opened.assert_not_called()
        self.assertNotIn("df_0", fake_ip.user_ns)


class CommitDirectBranchTest(unittest.TestCase):
    """Direct branch coverage for _MaterializationRegistry.commit: the inflight_key-gone
    edge, the normal-success edge, and the inflight_key=None (untracked) edge."""

    def test_commit_returns_false_when_inflight_key_missing(self):
        reg = _MaterializationRegistry()
        gen, _ = reg.start("df")
        # inflight_key given but never marked inflight -> `not in self._inflight` True -> False
        ran = reg.commit("df", gen, lambda: None, inflight_key=("df", gen))
        self.assertFalse(ran)

    def test_commit_runs_with_none_inflight_key(self):
        reg = _MaterializationRegistry()
        gen, _ = reg.start("df")
        calls = []
        # inflight_key=None -> skip the inflight ownership check, action runs, returns True
        ran = reg.commit("df", gen, lambda: calls.append(1), inflight_key=None)
        self.assertTrue(ran)
        self.assertEqual(calls, [1])

    def test_commit_returns_false_on_stale_generation(self):
        reg = _MaterializationRegistry()
        gen, _ = reg.start("df")
        reg.start("df")  # supersede -> gen is now stale
        ran = reg.commit("df", gen, lambda: None, inflight_key=None)
        self.assertFalse(ran)


class DefaultGetS3ClientReturnCachedTest(unittest.TestCase):
    """Cover the `return _s3_client` line when the client is already cached (second call
    returns without reconstructing)."""

    def setUp(self):
        async_mod._s3_client = None

    def tearDown(self):
        async_mod._s3_client = None

    def test_returns_existing_cached_client(self):
        sentinel = object()
        async_mod._s3_client = sentinel  # pre-populate cache
        # already set -> the `if _s3_client is None` guard is False -> straight return
        self.assertIs(async_mod._get_s3_client(), sentinel)


class AsyncSqlResultTextPlainTest(unittest.TestCase):
    """Cover the text/plain branch of _repr_mimebundle_ (message string construction)."""

    def test_text_plain_message_included(self):
        result = AsyncSqlResult(
            execution_id="e",
            s3_path="s3://b/results/e/",
            columns=["a"],
            first_page_rows=[[1], [2], [3]],
        )
        with mock.patch.object(AsyncSqlResult, "_first_page_parquet_b64", return_value="x"):
            bundle = result._repr_mimebundle_()
        self.assertIn("text/plain", bundle)
        self.assertIn("3 rows shown", bundle["text/plain"])
        self.assertIn("s3://b/results/e/", bundle["text/plain"])


class AsyncDriverEligibilityTest(unittest.TestCase):
    """Full eligibility/fallback matrix for sqlutils._stream_with_async_materialization.
    Each pre-execution guard must return False (so the caller runs the sync path) without
    executing anything; the committed-phase branches raise instead of returning False."""

    def _drive(self, kwargs=None, **patches):
        """Call the driver with the given patches on the sqlutils module. Returns the
        (result, mocks) so a test can assert both the return and what was reached."""
        from sagemaker_studio.utils import sqlutils

        kwargs = kwargs or {}
        with contextlib.ExitStack() as stack:
            for name, m in patches.items():
                stack.enter_context(mock.patch.object(sqlutils, name, m))
            result = sqlutils._stream_with_async_materialization("SELECT 1", "df", **kwargs)
        return result

    def test_continue_on_error_falls_back_to_sync(self):
        from sagemaker_studio.utils import sqlutils

        # CONTINUE_ON_ERROR is not supported by the async path -> pre-execution False.
        result = sqlutils._stream_with_async_materialization(
            "SELECT 1", "df", error_strategy="CONTINUE_ON_ERROR"
        )
        self.assertFalse(result)

    def test_spark_connection_falls_back_to_sync(self):
        # Spark connections stream results through their own path (no engine execution_id
        # / S3 page layout), so the async materialization path must not claim them.
        result = self._drive(_is_spark_connection=mock.Mock(return_value=True))
        self.assertFalse(result)

    def test_none_connection_falls_back_to_sync(self):
        # No resolvable connection (e.g. local DuckDB / no id or name) -> the async path
        # has nothing to materialize against and defers to sync.
        result = self._drive(
            _is_spark_connection=mock.Mock(return_value=False),
            _resolve_connection=mock.Mock(return_value=None),
        )
        self.assertFalse(result)

    def test_irc_glue_connection_falls_back_to_sync(self):
        from sagemaker_studio.utils import sqlutils

        irc_type = next(iter(sqlutils.SUPPORTED_IRC_GLUE_CONNECTION_TYPES))
        conn = mock.Mock()
        conn.type = irc_type
        result = self._drive(
            _is_spark_connection=mock.Mock(return_value=False),
            _resolve_connection=mock.Mock(return_value=conn),
        )
        self.assertFalse(result)

    def test_unsupported_connection_type_falls_back_to_sync(self):
        conn = mock.Mock()
        conn.type = "MYSQL"  # not in ASYNC_SUPPORTED_CONNECTION_TYPES
        result = self._drive(
            _is_spark_connection=mock.Mock(return_value=False),
            _resolve_connection=mock.Mock(return_value=conn),
        )
        self.assertFalse(result)

    def test_no_cached_connection_falls_back_to_sync(self):
        conn = mock.Mock()
        conn.type = "ATHENA"
        result = self._drive(
            _is_spark_connection=mock.Mock(return_value=False),
            _resolve_connection=mock.Mock(return_value=conn),
            _apply_athena_context=mock.Mock(),
            _get_or_create_connection=mock.Mock(return_value=None),  # falsy -> bail
        )
        self.assertFalse(result)

    def test_missing_project_s3_root_falls_back_to_sync(self):
        conn = mock.Mock()
        conn.type = "ATHENA"
        project = SimpleNamespace(s3=SimpleNamespace(root=None))  # no s3 root
        result = self._drive(
            _is_spark_connection=mock.Mock(return_value=False),
            _resolve_connection=mock.Mock(return_value=conn),
            _apply_athena_context=mock.Mock(),
            _get_or_create_connection=mock.Mock(return_value=mock.Mock()),
            _ensure_project=mock.Mock(return_value=project),
        )
        self.assertFalse(result)

    def test_setup_exception_falls_back_to_sync(self):
        # An unexpected error anywhere in Phase 1 setup is caught -> False (safe fallback,
        # nothing executed yet).
        result = self._drive(
            _is_spark_connection=mock.Mock(side_effect=RuntimeError("boom")),
        )
        self.assertFalse(result)


class AsyncDriverCommittedPhaseTest(unittest.TestCase):
    """Committed-phase branches: after statements execute, the driver must NOT fall back
    to sync (which would re-run side effects). It raises on error / missing id, binds
    partials, and handles the DML executor branch."""

    def _phase1_patches(self, sqlutils, executor, project_root="s3://bucket/proj"):
        conn = mock.Mock()
        conn.type = "ATHENA"
        cached = SimpleNamespace(
            engine=SimpleNamespace(get_execution_options=lambda: {"connection_type": "ATHENA"})
        )
        project = SimpleNamespace(s3=SimpleNamespace(root=project_root))
        return dict(
            _is_spark_connection=mock.Mock(return_value=False),
            _resolve_connection=mock.Mock(return_value=conn),
            _apply_athena_context=mock.Mock(),
            _get_or_create_connection=mock.Mock(return_value=cached),
            _ensure_project=mock.Mock(return_value=project),
            _ensure_sql_executor=mock.Mock(return_value=executor),
        )

    def test_statement_error_binds_partials_then_raises(self):
        from sagemaker_studio.sql_engine.sql_executor import ExecutionStatus
        from sagemaker_studio.utils import sqlutils

        executor = mock.Mock()
        executor._get_transformer.return_value = mock.Mock()
        # First result SUCCESS, second FAILED -> driver binds partials for the first, raises.
        good = SimpleNamespace(
            status=ExecutionStatus.SUCCESS.value,
            statement_index=0,
            result=async_mod.AsyncResultMarker(execution_id="e0"),
        )
        bad = SimpleNamespace(status="FAILED", statement_index=1, error="statement blew up")
        executor.execute.return_value = iter([good, bad])

        patches = self._phase1_patches(sqlutils, executor)
        bind = mock.Mock()
        with contextlib.ExitStack() as stack:
            for name, m in patches.items():
                stack.enter_context(mock.patch.object(sqlutils, name, m))
            stack.enter_context(mock.patch.object(sqlutils, "_bind_succeeded_partials", bind))
            stack.enter_context(
                mock.patch.object(sqlutils, "_stream_and_capture_metadata", lambda s, **k: s)
            )
            with self.assertRaises(Exception) as ctx:
                sqlutils._stream_with_async_materialization("SELECT 1; SELECT 2", "df")
        self.assertIn("statement blew up", str(ctx.exception))
        bind.assert_called_once()  # partial-bind reached before raising

    def test_partial_bind_failure_is_swallowed_and_original_error_still_raised(self):
        # Covers the defensive except/log branch around _bind_succeeded_partials: if the
        # best-effort partial-bind itself raises, it must be swallowed (logged) so the
        # ORIGINAL statement error still propagates -- the bind failure must never mask it.
        from sagemaker_studio.sql_engine.sql_executor import ExecutionStatus
        from sagemaker_studio.utils import sqlutils

        executor = mock.Mock()
        executor._get_transformer.return_value = mock.Mock()
        good = SimpleNamespace(
            status=ExecutionStatus.SUCCESS.value,
            statement_index=0,
            result=async_mod.AsyncResultMarker(execution_id="e0"),
        )
        bad = SimpleNamespace(status="FAILED", statement_index=1, error="statement blew up")
        executor.execute.return_value = iter([good, bad])

        patches = self._phase1_patches(sqlutils, executor)
        bind = mock.Mock(side_effect=RuntimeError("bind boom"))  # partial-bind itself fails
        with contextlib.ExitStack() as stack:
            for name, m in patches.items():
                stack.enter_context(mock.patch.object(sqlutils, name, m))
            stack.enter_context(mock.patch.object(sqlutils, "_bind_succeeded_partials", bind))
            stack.enter_context(
                mock.patch.object(sqlutils, "_stream_and_capture_metadata", lambda s, **k: s)
            )
            with self.assertRaises(Exception) as ctx:
                sqlutils._stream_with_async_materialization("SELECT 1; SELECT 2", "df")
        # The ORIGINAL statement error surfaces, NOT the bind failure (swallow branch worked).
        self.assertIn("statement blew up", str(ctx.exception))
        self.assertNotIn("bind boom", str(ctx.exception))
        bind.assert_called_once()

    def test_missing_execution_id_raises_runtime_error(self):
        from sagemaker_studio.sql_engine.sql_executor import ExecutionStatus
        from sagemaker_studio.utils import sqlutils

        executor = mock.Mock()
        executor._get_transformer.return_value = mock.Mock()
        # A result-bearing statement whose execution_id came back None -> RuntimeError
        # (re-running would be unsafe, so surface rather than silently double-execute).
        res = SimpleNamespace(
            status=ExecutionStatus.SUCCESS.value,
            statement_index=0,
            result=async_mod.AsyncResultMarker(execution_id=None),
        )
        executor.execute.return_value = iter([res])

        patches = self._phase1_patches(sqlutils, executor)
        with contextlib.ExitStack() as stack:
            for name, m in patches.items():
                stack.enter_context(mock.patch.object(sqlutils, name, m))
            stack.enter_context(
                mock.patch.object(sqlutils, "_stream_and_capture_metadata", lambda s, **k: s)
            )
            with self.assertRaises(RuntimeError):
                sqlutils._stream_with_async_materialization("SELECT 1", "df")

    def test_success_result_is_appended_to_specs(self):
        # Directly cover the success-path append (specs.append(spec_from_result(...))):
        # one SUCCESS result flows through the loop and must reach materialize_async_multi
        # as a single result-bearing StatementSpec (execution_id preserved).
        from sagemaker_studio.sql_engine.sql_executor import ExecutionStatus
        from sagemaker_studio.utils import sqlutils

        executor = mock.Mock()
        executor._get_transformer.return_value = mock.Mock()
        res = SimpleNamespace(
            status=ExecutionStatus.SUCCESS.value,
            statement_index=0,
            result=async_mod.AsyncResultMarker(execution_id="e0"),
        )
        executor.execute.return_value = iter([res])

        patches = self._phase1_patches(sqlutils, executor)
        with contextlib.ExitStack() as stack:
            for name, m in patches.items():
                stack.enter_context(mock.patch.object(sqlutils, name, m))
            stack.enter_context(
                mock.patch.object(sqlutils, "_stream_and_capture_metadata", lambda s, **k: s)
            )
            mat = stack.enter_context(mock.patch.object(async_mod, "materialize_async_multi"))
            handled = sqlutils._stream_with_async_materialization("SELECT 1", "df")

        self.assertTrue(handled)
        mat.assert_called_once()
        specs = mat.call_args.kwargs["specs"]
        self.assertEqual(len(specs), 1)
        self.assertEqual(specs[0].kind, "result")
        self.assertEqual(specs[0].execution_id, "e0")

    def test_success_path_reaches_materialize_and_reader_factory(self):
        from sagemaker_studio.sql_engine.sql_executor import ExecutionStatus
        from sagemaker_studio.utils import sqlutils

        executor = mock.Mock()
        executor._get_transformer.return_value = mock.Mock()
        res = SimpleNamespace(
            status=ExecutionStatus.SUCCESS.value,
            statement_index=0,
            result=async_mod.AsyncResultMarker(execution_id="e0"),
        )
        executor.execute.return_value = iter([res])

        patches = self._phase1_patches(sqlutils, executor)
        with contextlib.ExitStack() as stack:
            for name, m in patches.items():
                stack.enter_context(mock.patch.object(sqlutils, name, m))
            stack.enter_context(
                mock.patch.object(sqlutils, "_stream_and_capture_metadata", lambda s, **k: s)
            )
            mat = stack.enter_context(mock.patch.object(async_mod, "materialize_async_multi"))
            # Prove the _reader_factory closure wiring is exercised by invoking the
            # reader_factory the driver hands to materialize_async_multi.
            opened = stack.enter_context(
                mock.patch.object(
                    reader_mod, "open_result_reader", return_value=(["a"], iter([[[1]]]), None)
                )
            )
            handled = sqlutils._stream_with_async_materialization("SELECT 1", "df")
            self.assertTrue(handled)
            mat.assert_called_once()
            reader_factory = mat.call_args.kwargs["reader_factory"]
            columns, first_page, remaining, total = reader_factory("e0")
        self.assertEqual(columns, ["a"])
        self.assertEqual(first_page, [[1]])
        self.assertIsNone(total)
        opened.assert_called_once()

    def test_async_statement_executor_dml_branch(self):
        # Directly drive the injected per-statement executor's DML branch (returns_rows
        # False -> SingleStatementResult(rowcount)) and its result branch (returns_rows
        # True -> AsyncResultMarker). The executor closure is built inside the driver, so
        # we capture it via the real SqlExecutor.execute call.
        from sagemaker_studio.sql_engine.sql_executor import SingleStatementResult
        from sagemaker_studio.utils import sqlutils

        executor = mock.Mock()
        transformer = mock.Mock()
        transformer.get_execution_metadata.return_value = {"query_execution_id": "e0"}
        executor._get_transformer.return_value = transformer

        captured = {}

        def fake_execute(engine, query, **kwargs):
            captured["statement_executor"] = kwargs["statement_executor"]
            return iter([])  # no specs -> DML-only-ish; we test the executor closure directly

        executor.execute.side_effect = fake_execute

        patches = self._phase1_patches(sqlutils, executor)
        with contextlib.ExitStack() as stack:
            for name, m in patches.items():
                stack.enter_context(mock.patch.object(sqlutils, name, m))
            stack.enter_context(
                mock.patch.object(sqlutils, "_stream_and_capture_metadata", lambda s, **k: s)
            )
            stack.enter_context(
                mock.patch.object(async_mod, "materialize_async_multi", return_value=[])
            )
            sqlutils._stream_with_async_materialization("INSERT INTO t VALUES (1)", "df")

        stmt_exec = captured["statement_executor"]
        # DML: returns_rows False -> SingleStatementResult carrying the rowcount
        conn = mock.Mock()
        dml_res = mock.Mock()
        dml_res.returns_rows = False
        dml_res.rowcount = 7
        conn.execute.return_value = dml_res
        out = stmt_exec(conn, "INSERT INTO t VALUES (1)", None)
        self.assertIsInstance(out, SingleStatementResult)
        self.assertEqual(out.result, 7)

        # Result-bearing: returns_rows True -> AsyncResultMarker(execution_id)
        sel_res = mock.Mock()
        sel_res.returns_rows = True
        conn.execute.return_value = sel_res
        out2 = stmt_exec(conn, "SELECT 1", {})
        self.assertIsInstance(out2.result, async_mod.AsyncResultMarker)
        self.assertEqual(out2.result.execution_id, "e0")

    def test_async_statement_executor_swallows_metadata_error(self):
        from sagemaker_studio.sql_engine.sql_executor import SingleStatementResult
        from sagemaker_studio.utils import sqlutils

        executor = mock.Mock()
        transformer = mock.Mock()
        transformer.get_execution_metadata.side_effect = RuntimeError("no cursor")
        executor._get_transformer.return_value = transformer

        captured = {}

        def fake_execute(engine, query, **kwargs):
            captured["se"] = kwargs["statement_executor"]
            return iter([])

        executor.execute.side_effect = fake_execute
        patches = self._phase1_patches(sqlutils, executor)
        with contextlib.ExitStack() as stack:
            for name, m in patches.items():
                stack.enter_context(mock.patch.object(sqlutils, name, m))
            stack.enter_context(
                mock.patch.object(sqlutils, "_stream_and_capture_metadata", lambda s, **k: s)
            )
            stack.enter_context(
                mock.patch.object(async_mod, "materialize_async_multi", return_value=[])
            )
            sqlutils._stream_with_async_materialization("SELECT 1", "df")

        # metadata extraction raised -> swallowed to None; DML result still returned.
        conn = mock.Mock()
        r = mock.Mock()
        r.returns_rows = False
        r.rowcount = 3
        conn.execute.return_value = r
        out = captured["se"](conn, "DELETE FROM t", None)
        self.assertIsInstance(out, SingleStatementResult)
        self.assertEqual(out.result, 3)
        self.assertIsNone(out.execution_metadata)


class FirstPageParquetBodyTest(unittest.TestCase):
    """Exercise the REAL _first_page_parquet_b64 body (pyarrow present in the test env),
    not the patched-out stub other tests use, so the base64/parquet path is covered."""

    def test_returns_decodable_base64_parquet(self):
        import base64
        import io

        import pandas as pd
        import pyarrow.parquet as pq

        result = AsyncSqlResult(
            execution_id="exec-1",
            s3_path="s3://bkt/proj/results/exec-1/",
            columns=["a", "b"],
            first_page_rows=[[1, "x"], [2, "y"]],
        )
        b64 = result._first_page_parquet_b64()
        raw = base64.b64decode(b64)
        back = pd.read_parquet(io.BytesIO(raw))
        self.assertEqual(list(back.columns), ["a", "b"])
        self.assertEqual(back["a"].tolist(), [1, 2])
        self.assertEqual(back["b"].tolist(), ["x", "y"])
        # sanity: it really is a parquet buffer
        self.assertEqual(pq.read_table(io.BytesIO(raw)).num_rows, 2)


class RemainingBranchGapTest(unittest.TestCase):
    """Close the last branch-partial edges flagged by coverage:
    - _background_materialize: commit() returns False AFTER a full stream (the superseded/
      flush-claimed else-branch, lines 349-False + 364-369), and the except path where
      claim_terminal() returns False (384-False, no duplicate failed emit).
    - materialize_async_multi: DML-only cell with an empty specs list (672-False), and a
      spawn failure whose spec has no execution_id (742-False).
    """

    def test_commit_false_after_stream_takes_superseded_branch(self):
        # The real commit() must return False AFTER a full stream so line 349's False edge
        # runs (else-branch: NO namespace bind, NO dataframe_ready, terminal FAILED
        # manifest). We use the REAL registry and bump the generation AFTER start() without
        # setting this run's cancel event -- so streaming completes (cancel not set), then
        # the genuine commit() sees a stale generation and returns False.
        seams = _Seams()
        registry = _MaterializationRegistry()
        gen, cancel = registry.start("df")
        # Make gen stale without signalling cancel (so the stream is NOT short-circuited at
        # the cancel check): overwrite the generation map directly to a newer value.
        with registry._lock:
            registry._generation["df"] = gen + 1
        async_mod._background_materialize(
            dataframe_name="df",
            columns=["a"],
            first_page_rows=[[1], [2]],
            remaining_rows=iter([]),
            prefix="s3://b/results/e/",
            execution_id="e",
            gen=gen,
            cancel=cancel,  # NOT set -> stream runs to completion, then commit() fails on gen
            registry=registry,
            rows_per_page=2,
            assign_namespace_fn=seams.assign,
            write_page_fn=seams.write_page,
            write_manifest_fn=seams.write_manifest,
            emit_ready_fn=seams.emit_ready,
        )
        self.assertNotIn("df", seams.namespace)  # else-branch: no namespace bind
        self.assertEqual(seams.ready, [])  # no dataframe_ready emitted
        self.assertEqual(
            seams.manifests[-1]["status"], async_mod.STATUS_FAILED
        )  # terminal manifest

    def test_except_path_claim_terminal_false_no_emit(self):
        # write_page raises (uncommitted failure). A registry whose claim_terminal() returns
        # False (flush already claimed) drives the 384-False edge: failed manifest written,
        # but NO dataframe_ready(failed) emitted (single-owner finalization).
        seams = _Seams()

        class _ClaimFalseRegistry(_MaterializationRegistry):
            def claim_terminal(self, key):
                return False

        registry = _ClaimFalseRegistry()
        gen, cancel = registry.start("df")

        def boom(_uri, _df):
            raise RuntimeError("s3 down")

        async_mod._background_materialize(
            dataframe_name="df",
            columns=["a"],
            first_page_rows=[[1]],
            remaining_rows=iter([]),
            prefix="s3://b/results/e/",
            execution_id="e",
            gen=gen,
            cancel=cancel,
            registry=registry,
            rows_per_page=2,
            assign_namespace_fn=seams.assign,
            write_page_fn=boom,
            write_manifest_fn=seams.write_manifest,
            emit_ready_fn=seams.emit_ready,
        )
        self.assertEqual(seams.manifests[-1]["status"], async_mod.STATUS_FAILED)
        self.assertEqual(seams.ready, [])  # claim_terminal False -> no failed emit

    def test_dml_only_empty_specs_binds_nothing(self):
        # materialize_async_multi with an EMPTY specs list: no result specs AND `if specs:`
        # is False (672-False) -> returns [] without binding base_name.
        seams = _Seams()
        payloads = materialize_async_multi(
            base_name="df",
            specs=[],
            project_s3_root="s3://bkt/p",
            reader_factory=lambda eid: (["a"], [], iter([]), None),
            display_fn=seams.display,
            assign_namespace_fn=seams.assign,
            write_page_fn=seams.write_page,
            write_manifest_fn=seams.write_manifest,
            emit_ready_fn=seams.emit_ready,
        )
        self.assertEqual(payloads, [])
        self.assertNotIn("df", seams.namespace)  # nothing bound for an empty cell

    def test_spawn_failure_without_execution_id_skips_emit(self):
        # A result spec passes the pre-arm validation (execution_id present) but
        # materialize_async is patched to raise, taking the except path. With execution_id
        # falsy at that point we exercise the 742-False edge (no emit). Being a SINGLE
        # (non-multi) result cell, the except now RE-RAISES so df is never left silently
        # unbound (r5p6) -- assert both the no-emit and the raise.
        seams = _Seams()

        class _Spec:
            # execution_id truthy for the pre-arm check, then flipped to "" so the except's
            # `if spec.execution_id:` is False.
            def __init__(self):
                self.index = 0
                self.kind = "result"
                self._eid = "e0"

            @property
            def execution_id(self):
                return self._eid

        spec = _Spec()

        def flaky_materialize(*a, **k):
            spec._eid = ""  # flip to falsy so the except-branch skips the emit
            raise RuntimeError("spawn boom")

        with mock.patch.object(async_mod, "materialize_async", side_effect=flaky_materialize):
            with self.assertRaises(RuntimeError):  # single-result failure surfaces (r5p6)
                materialize_async_multi(
                    base_name="df",
                    specs=[spec],
                    project_s3_root="s3://bkt/p",
                    reader_factory=lambda eid: (["a"], [[1]], iter([]), None),
                    display_fn=seams.display,
                    assign_namespace_fn=seams.assign,
                    write_page_fn=seams.write_page,
                    write_manifest_fn=seams.write_manifest,
                    emit_ready_fn=seams.emit_ready,
                    registry=_MaterializationRegistry(),
                    rows_per_page=10000,
                )
        self.assertEqual(seams.ready, [])  # execution_id falsy -> no failed emit
        self.assertNotIn("df", seams.namespace)  # df never silently bound

    def test_single_result_spawn_failure_reraises_and_emits_failed(self):
        # r5p6: a single-result (non-multi) cell whose materialize_async spawn raises must
        # emit dataframe_ready(failed) for the orphaned card AND re-raise (so the caller /
        # sql_stream_with_display surfaces the error), rather than returning with df unbound.
        seams = _Seams()
        with mock.patch.object(
            async_mod, "materialize_async", side_effect=RuntimeError("spawn boom")
        ):
            with self.assertRaises(RuntimeError):
                materialize_async_multi(
                    base_name="df",
                    specs=[StatementSpec(index=0, kind="result", execution_id="e0")],
                    project_s3_root="s3://bkt/p",
                    reader_factory=lambda eid: (["a"], [[1]], iter([]), None),
                    display_fn=seams.display,
                    assign_namespace_fn=seams.assign,
                    write_page_fn=seams.write_page,
                    write_manifest_fn=seams.write_manifest,
                    emit_ready_fn=seams.emit_ready,
                    registry=_MaterializationRegistry(),
                    rows_per_page=10000,
                )
        # failed event emitted for the orphaned card; df never bound
        self.assertIn(("e0", async_mod.READY_FAILED), seams.ready)
        self.assertNotIn("df", seams.namespace)


if __name__ == "__main__":
    unittest.main()
