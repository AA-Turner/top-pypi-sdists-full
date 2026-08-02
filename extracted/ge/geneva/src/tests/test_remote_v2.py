# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Unit tests for V2 remote routing (namespace_client-based)."""

from collections.abc import Iterator
from typing import NoReturn
from unittest.mock import MagicMock

import pytest

from geneva.jobs.jobs import JobMetric, JobRecord, JobStatus
from geneva.jobs.remote import RemoteJob
from geneva.remote_v2 import RemoteJobFuture


class TestRemoteJob:
    def test_remote_job_fields(self) -> None:
        conn = MagicMock()
        job = RemoteJob(
            job_id="abc",
            table_name="my_table",
            conn=conn,
            column_name="col",
            job_type="backfill",
        )
        assert job.job_id == "abc"
        assert job.table_name == "my_table"
        assert job.column_name == "col"
        assert job.job_type == "backfill"

    def test_done_returns_false_for_running(self) -> None:
        conn = MagicMock()
        conn.get_job.return_value = JobRecord(
            table_name="t", column_name="c", job_id="j1", status=JobStatus.RUNNING
        )
        job = RemoteJob(job_id="j1", table_name="t", conn=conn)
        assert job.done() is False

    def test_done_returns_true_for_completed(self) -> None:
        conn = MagicMock()
        conn.get_job.return_value = JobRecord(
            table_name="t", column_name="c", job_id="j1", status=JobStatus.DONE
        )
        job = RemoteJob(job_id="j1", table_name="t", conn=conn)
        assert job.done() is True


class TestRemoteJobPollingLogs:
    """Logging behavior of the remote polling loop.

    Per-tick status transitions are intentionally NOT logged from the render
    loop: raw log writes interleaved with the live tqdm bars desynced tqdm's
    cursor and made the status/events lines overlap the metric bars. The loop
    logs only the terminal completion; live status shows on the tqdm status
    line and durable transitions live in the job record's ``events``."""

    JOB_ID = "abc12345-6789-0123-4567-89abcdef0123"

    def _job(self, conn: MagicMock) -> RemoteJob:
        return RemoteJob(
            job_id=self.JOB_ID,
            table_name="my_table",
            conn=conn,
            column_name="my_col",
        )

    @staticmethod
    def _record(status: JobStatus) -> JobRecord:
        return JobRecord(
            table_name="my_table",
            column_name="my_col",
            job_id="abc12345-6789-0123-4567-89abcdef0123",
            status=status,
        )

    def test_polling_logs_only_terminal_completion(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        # PENDING -> RUNNING -> DONE. Per-tick status transitions are no longer
        # logged from the render loop (raw log lines corrupt the live tqdm
        # bars); only the terminal completion line is emitted.
        conn = MagicMock()
        conn.get_job.side_effect = [
            ValueError("job record not yet created"),
            ValueError("job record not yet created"),
            self._record(JobStatus.RUNNING),
            self._record(JobStatus.RUNNING),
            self._record(JobStatus.DONE),
        ]

        with caplog.at_level("INFO", logger="geneva.jobs.remote"):
            self._job(conn)._poll_until_done(refresh_secs=0)

        msgs = [
            r.getMessage() for r in caplog.records if r.name == "geneva.jobs.remote"
        ]
        assert msgs == [f"Job {self.JOB_ID} completed"], msgs

    def test_repeated_running_does_not_spam(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        # 5x RUNNING (long-running job, many polls at the same status) then
        # DONE. The loop must never spam the log per tick — only the single
        # terminal completion line is emitted, regardless of poll count.
        conn = MagicMock()
        conn.get_job.side_effect = [
            *([self._record(JobStatus.RUNNING)] * 5),
            self._record(JobStatus.DONE),
        ]

        with caplog.at_level("INFO", logger="geneva.jobs.remote"):
            self._job(conn)._poll_until_done(refresh_secs=0)

        msgs = [
            r.getMessage() for r in caplog.records if r.name == "geneva.jobs.remote"
        ]
        assert msgs == [f"Job {self.JOB_ID} completed"], msgs

    def test_per_tick_status_is_not_logged(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        # Regression guard for the tqdm-overlap fix: the render loop must not
        # log per-tick PENDING/RUNNING status lines (those raw writes desync
        # the live bars). Only the terminal completion is logged.
        conn = MagicMock()
        conn.get_job.side_effect = [
            ValueError("not yet"),
            self._record(JobStatus.RUNNING),
            self._record(JobStatus.DONE),
        ]

        with caplog.at_level("INFO", logger="geneva.jobs.remote"):
            self._job(conn)._poll_until_done(refresh_secs=0)

        msgs = [
            r.getMessage() for r in caplog.records if r.name == "geneva.jobs.remote"
        ]
        assert not any("PENDING" in m or "RUNNING" in m for m in msgs), msgs
        assert msgs == [f"Job {self.JOB_ID} completed"], msgs


class TestRemoteJobFuture:
    def test_status_done_for_completed_job(self) -> None:
        from geneva.jobs.types import DONE, Job

        completed = JobRecord(
            table_name="t", column_name="c", job_id="j1", status=JobStatus.DONE
        )
        rj = MagicMock(spec=RemoteJob)
        rj.job_id = "j1"
        rj.done.return_value = True
        rj._read_job_record.return_value = completed

        future = RemoteJobFuture(rj)
        job = Job(future, table_name="t", column_names=["c"])
        assert job.status == DONE

    def test_result_zero_timeout_in_flight_raises_timeout(self) -> None:
        running = JobRecord(
            table_name="t", column_name="c", job_id="j2", status=JobStatus.RUNNING
        )
        rj = MagicMock(spec=RemoteJob)
        rj.job_id = "j2"
        rj.done.return_value = False
        rj._read_job_record.return_value = running

        future = RemoteJobFuture(rj)
        with pytest.raises(TimeoutError):
            future.result(timeout=0)

    def test_result_zero_timeout_failed_raises_runtime(self) -> None:
        failed = JobRecord(
            table_name="t",
            column_name="c",
            job_id="j3",
            status=JobStatus.FAILED,
            events=["worker pod OOM-killed"],
        )
        rj = MagicMock(spec=RemoteJob)
        rj.job_id = "j3"
        rj.done.return_value = True
        rj._read_job_record.return_value = failed

        future = RemoteJobFuture(rj)
        with pytest.raises(RuntimeError, match="OOM-killed"):
            future.result(timeout=0)

    def test_marshals_metrics_into_payload(self) -> None:
        record = JobRecord(
            table_name="t1",
            column_name="upper",
            input_columns=["MetaData.UserId"],
            output_columns=["upper"],
            job_id="j1",
            status=JobStatus.DONE,
            metrics=[
                JobMetric(
                    name="rows_checkpointed", n=100, total=100, done=True, desc=""
                ),
                JobMetric(name="rows_skipped", n=5, total=5, done=True, desc=""),
            ],
        )
        rj = MagicMock(spec=RemoteJob)
        rj.job_id = "j1"
        rj.result.return_value = record

        future = RemoteJobFuture(rj)
        payload = future.result()

        assert payload["job_id"] == "j1"
        assert payload["status"] == "DONE"
        assert payload["table_name"] == "t1"
        assert payload["column_name"] == "upper"
        assert payload["input_columns"] == ["MetaData.UserId"]
        assert payload["output_columns"] == ["upper"]
        assert payload["rows_processed"] == 100
        assert payload["rows_skipped"] == 5


class TestV2Routing:
    """V2 routing: requests are built correctly and sent to namespace_client.

    V2 dispatch is now the default behavior for remote (``db://``)
    connections — no env-var opt-in. The ``is_remote`` monkeypatch in
    each test below is sufficient to drive the connection through
    ``routes_through_v2()``.
    """

    @pytest.fixture
    def table(self, tmp_path, monkeypatch) -> "geneva.table.Table":  # noqa: ANN201, F821
        import pyarrow as pa

        from geneva import connect

        db = connect(str(tmp_path))
        tbl = db.create_table("t", pa.table({"a": [1, 2, 3]}))
        table_uri = tbl.uri
        monkeypatch.setattr(type(tbl._conn), "is_remote_uri", lambda self: True)
        # Mock namespace_client and _history
        tbl._conn._ns_client_mock = MagicMock()
        tbl._conn._ns_client_mock.describe_table.return_value.location = table_uri
        monkeypatch.setattr(
            type(tbl._conn), "namespace_client", lambda self: self._ns_client_mock
        )
        tbl._conn._history = MagicMock()
        return tbl

    def test_backfill_async_builds_correct_request(self, table) -> None:
        """backfill_async builds AlterTableBackfillColumnsRequest with all params."""
        ns = table._conn.namespace_client()
        ns.alter_table_backfill_columns.return_value = MagicMock(job_id="job-123")

        from geneva.jobs.types import Job

        job = table.backfill_async("a", where="a IS NULL", concurrency=16)

        ns.alter_table_backfill_columns.assert_called_once()
        req = ns.alter_table_backfill_columns.call_args[0][0]
        assert req.column == "a"
        assert req.where == "a IS NULL"
        assert req.concurrency == 16
        assert req.id == table._table_id
        assert isinstance(job, Job)
        assert job.job_id == "job-123"

    def test_backfill_async_passes_all_params(self, table) -> None:
        ns = table._conn.namespace_client()
        ns.alter_table_backfill_columns.return_value = MagicMock(job_id="j")

        table.backfill_async(
            "a",
            where="a > 0",
            concurrency=4,
            intra_applier_concurrency=2,
            min_checkpoint_size=10,
            max_checkpoint_size=100,
            batch_checkpoint_flush_interval_seconds=5.0,
            cluster="my_cluster",
            manifest="my_manifest",
            read_version=42,
            task_size=1000,
            num_frags=5,
            checkpoint_size=50,
            commit_granularity=10,
        )

        req = ns.alter_table_backfill_columns.call_args[0][0]
        assert req.where == "a > 0"
        assert req.concurrency == 4
        assert req.intra_applier_concurrency == 2
        assert req.min_checkpoint_size == 10
        assert req.max_checkpoint_size == 100
        assert req.batch_checkpoint_flush_interval_seconds == 5.0
        assert req.cluster == "my_cluster"
        assert req.manifest == "my_manifest"
        assert req.read_version == 42
        assert req.task_size == 1000
        assert req.num_frags == 5
        assert req.checkpoint_size == 50
        assert req.commit_granularity == 10

    def test_backfill_async_full_reprocess_passes_checkpoint_index_skip_when_supported(
        self, table, monkeypatch
    ) -> None:
        import lance_namespace

        ns = table._conn.namespace_client()
        ns.alter_table_backfill_columns.return_value = MagicMock(job_id="j")
        recorded: dict = {}

        class _RecordingRequest:
            model_fields = {
                "id": None,
                "column": None,
                "where": None,
                "_skip_checkpoint_index_scan": None,
            }

            def __init__(self, **kwargs) -> None:
                recorded.update(kwargs)

        monkeypatch.setattr(
            lance_namespace, "AlterTableBackfillColumnsRequest", _RecordingRequest
        )

        table.backfill_async("a", where="1=1")

        ns.alter_table_backfill_columns.assert_called_once()
        assert recorded["where"] == "1=1"
        assert recorded["_skip_checkpoint_index_scan"] is True

    def test_backfill_async_rejects_checkpoint_index_skip_when_unsupported(
        self, table
    ) -> None:
        ns = table._conn.namespace_client()
        ns.alter_table_backfill_columns.return_value = MagicMock(job_id="j")

        with pytest.raises(NotImplementedError, match="_skip_checkpoint_index_scan"):
            table.backfill_async("a", _skip_checkpoint_index_scan=True)

        ns.alter_table_backfill_columns.assert_not_called()

    def test_backfill_async_normalizes_list_column(self, table) -> None:
        """A single-element list is accepted and normalized to a string."""
        ns = table._conn.namespace_client()
        ns.alter_table_backfill_columns.return_value = MagicMock(job_id="j")

        table.backfill_async(["a"])

        req = ns.alter_table_backfill_columns.call_args[0][0]
        assert req.column == "a"

    def test_backfill_async_rejects_nested_output_target(
        self, tmp_path, monkeypatch
    ) -> None:
        import pyarrow as pa

        from geneva import connect

        db = connect(str(tmp_path))
        schema = pa.schema(
            [
                pa.field(
                    "MetaData",
                    pa.struct([pa.field("UserId", pa.int64())]),
                )
            ]
        )
        tbl = db.create_table(
            "nested",
            pa.table(
                {"MetaData": [{"UserId": 1}]},
                schema=schema,
            ),
        )
        table_uri = tbl.uri
        monkeypatch.setattr(type(tbl._conn), "is_remote_uri", lambda self: True)
        tbl._conn._ns_client_mock = MagicMock()
        tbl._conn._ns_client_mock.describe_table.return_value.location = table_uri
        monkeypatch.setattr(
            type(tbl._conn), "namespace_client", lambda self: self._ns_client_mock
        )
        tbl._conn._history = MagicMock()

        with pytest.raises(ValueError, match="Nested backfill output target"):
            tbl.backfill_async("metadata.userid")

        tbl._conn.namespace_client().alter_table_backfill_columns.assert_not_called()
        tbl._conn._history.launch.assert_not_called()

    def test_backfill_async_returns_job_with_correct_fields(self, table) -> None:
        from geneva.jobs.types import BackfillJobResult, Job
        from geneva.remote_v2 import RemoteJobFuture

        ns = table._conn.namespace_client()
        ns.alter_table_backfill_columns.return_value = MagicMock(job_id="job-456")

        job = table.backfill_async("a")

        assert isinstance(job, Job)
        assert job.job_id == "job-456"
        assert job.column_names == ["a"]
        assert job._result_cls is BackfillJobResult
        assert isinstance(job.future, RemoteJobFuture)

    def test_backfill_async_records_job_in_history(self, table) -> None:
        ns = table._conn.namespace_client()
        ns.alter_table_backfill_columns.return_value = MagicMock(job_id="j99")

        table.backfill_async("a")

        table._conn._history.launch.assert_called_once_with(
            "t",
            "a",
            job_id="j99",
            input_columns=None,
            output_columns=["a"],
        )

    def test_refresh_async_forwards_source_task_size_when_supported(
        self, table, monkeypatch
    ) -> None:
        """When the namespace model carries ``source_task_size``, the remote
        refresh forwards it onto the request."""
        import lance_namespace

        recorded: dict = {}

        class _RecordingRequest:
            model_fields = {
                "id": None,
                "src_version": None,
                "max_rows_per_fragment": None,
                "concurrency": None,
                "intra_applier_concurrency": None,
                "source_task_size": None,
                "cluster": None,
                "output_limit": None,
                "manifest": None,
            }

            def __init__(self, **kwargs) -> None:
                recorded.update(kwargs)

        monkeypatch.setattr(
            lance_namespace, "RefreshMaterializedViewRequest", _RecordingRequest
        )
        ns = table._conn.namespace_client()
        ns.refresh_materialized_view.return_value = MagicMock(job_id="job-rib")

        table.refresh_async(source_task_size=512)

        ns.refresh_materialized_view.assert_called_once()
        assert recorded["source_task_size"] == 512

    def test_refresh_async_skips_source_task_size_when_unsupported(
        self, table, monkeypatch, caplog
    ) -> None:
        """An older namespace model without the field degrades gracefully: the
        param is dropped (not crashed) and a warning is logged."""
        import lance_namespace

        recorded: dict = {}

        class _OldRequest:
            model_fields = {  # intentionally missing source_task_size
                "id": None,
                "src_version": None,
                "max_rows_per_fragment": None,
                "concurrency": None,
                "intra_applier_concurrency": None,
                "cluster": None,
                "output_limit": None,
                "manifest": None,
            }

            def __init__(self, **kwargs) -> None:
                recorded.update(kwargs)

        monkeypatch.setattr(
            lance_namespace, "RefreshMaterializedViewRequest", _OldRequest
        )
        ns = table._conn.namespace_client()
        ns.refresh_materialized_view.return_value = MagicMock(job_id="job-old")

        with caplog.at_level("WARNING"):
            table.refresh_async(source_task_size=512)

        ns.refresh_materialized_view.assert_called_once()
        assert "source_task_size" not in recorded
        assert any("source_task_size" in r.getMessage() for r in caplog.records)

    def test_refresh_async_omits_source_task_size_when_none(
        self, table, monkeypatch
    ) -> None:
        """When ``source_task_size`` is not supplied it is never added to the
        request, even on a model that supports it."""
        import lance_namespace

        recorded: dict = {}

        class _RecordingRequest:
            model_fields = {"id": None, "source_task_size": None}

            def __init__(self, **kwargs) -> None:
                recorded.update(kwargs)

        monkeypatch.setattr(
            lance_namespace, "RefreshMaterializedViewRequest", _RecordingRequest
        )
        ns = table._conn.namespace_client()
        ns.refresh_materialized_view.return_value = MagicMock(job_id="j")

        table.refresh_async()

        assert "source_task_size" not in recorded

    def test_add_columns_sql_expression(self, table) -> None:
        """SQL expression columns build correct request."""
        ns = table._conn.namespace_client()

        table.add_columns({"new_col": "cast(null as string)"})

        ns.alter_table_add_columns.assert_called_once()
        req = ns.alter_table_add_columns.call_args[0][0]
        assert req.id == table._table_id
        assert len(req.new_columns) == 1
        assert req.new_columns[0].name == "new_col"
        assert req.new_columns[0].expression == "cast(null as string)"
        assert req.new_columns[0].virtual_column is None

    def test_add_columns_refreshes_to_latest(self, table, monkeypatch) -> None:
        """add_columns must refresh the in-memory handle to the new version.

        alter_table_add_columns commits a new server-side version; without a
        refresh, self._ltbl stays pinned at the pre-add version and the new
        column is invisible to subsequent reads (schema / search / backfill),
        forcing callers to call checkout_latest() explicitly. Regression test
        for that stale-handle bug.
        """
        ns = table._conn.namespace_client()
        refresh = MagicMock()
        monkeypatch.setattr(table, "checkout_latest", refresh)

        table.add_columns({"new_col": "cast(null as string)"})

        ns.alter_table_add_columns.assert_called_once()
        refresh.assert_called_once()

    def test_create_chunker_view_does_not_open_source_lance_client_side(
        self, table, monkeypatch
    ) -> None:
        """Remote chunker create should route through namespace API only."""
        import pyarrow as pa

        import geneva

        def fail_to_lance() -> NoReturn:
            raise AssertionError("remote create should not call source.to_lance()")

        monkeypatch.setattr(table, "to_lance", fail_to_lance)
        table._conn.open_table = MagicMock(return_value=MagicMock())

        @geneva.chunker(output_schema=pa.schema([pa.field("b", pa.int64())]))
        def duplicate(a: int) -> Iterator[dict[str, int]]:
            yield {"b": a}

        query = table.search(None).select(["a"])
        table._conn.create_udtf_view("remote_chunks", query, duplicate)

        ns = table._conn.namespace_client()
        ns.create_materialized_view.assert_called_once()
        req = ns.create_materialized_view.call_args[0][0]
        assert req.kind == "chunker"
        assert req.id == ["remote_chunks"]

    def test_add_columns_udf(self, table) -> None:
        """UDF columns are marshaled into AddVirtualColumnEntry."""
        import cloudpickle
        import pyarrow as pa

        from geneva import udf
        from geneva.packager import DockerUDFSpecV1, UDFSpec

        @udf(data_type=pa.int32())
        def my_udf(a: int) -> int:
            return a + 1

        table._conn._packager = MagicMock()
        table._conn._packager.marshal.return_value = UDFSpec(
            name="my_udf",
            backend="DockerUDFSpecV1",
            udf_payload=DockerUDFSpecV1(
                image="test-image",
                tag="latest",
                workspace_checksum=None,
                udf_pickle=cloudpickle.dumps(my_udf),
            ).to_bytes(),
        )

        ns = table._conn.namespace_client()
        table.add_columns({"b": my_udf})

        ns.alter_table_add_columns.assert_called_once()
        req = ns.alter_table_add_columns.call_args[0][0]
        col = req.new_columns[0]
        assert col.name == "b"
        assert col.virtual_column is not None
        vc = col.virtual_column
        assert vc.udf_name == "my_udf"
        assert vc.image == "test-image:latest"
        assert vc.input_columns == ["a"]
        assert len(vc.outputs) == 1
        output = vc.outputs[0]
        assert output.column == "b"
        assert output.struct_field == ""
        assert output.data_type == {"type": "int32"}
        assert output.nullable is True
        table_ref = table._conn._packager.marshal.call_args.kwargs["table_ref"]
        assert table_ref.table_id == table._table_id

    def test_add_columns_udf_canonicalizes_nested_input_paths(
        self, tmp_path, monkeypatch
    ) -> None:
        import cloudpickle
        import pyarrow as pa

        from geneva import connect, udf
        from geneva.packager import DockerUDFSpecV1, UDFSpec

        db = connect(str(tmp_path))
        tbl = db.create_table(
            "nested",
            pa.table(
                {
                    "MetaData": [
                        {"UserId": 1},
                        {"UserId": 2},
                    ]
                },
                schema=pa.schema(
                    [
                        pa.field(
                            "MetaData",
                            pa.struct([pa.field("UserId", pa.int64())]),
                        )
                    ]
                ),
            ),
        )
        table_uri = tbl.uri
        monkeypatch.setattr(type(tbl._conn), "is_remote_uri", lambda self: True)
        tbl._conn._ns_client_mock = MagicMock()
        tbl._conn._ns_client_mock.describe_table.return_value.location = table_uri
        monkeypatch.setattr(
            type(tbl._conn), "namespace_client", lambda self: self._ns_client_mock
        )

        @udf(data_type=pa.int64(), input_columns=["metadata.userid"])
        def identity(user_id: int) -> int:
            return user_id

        tbl._conn._packager = MagicMock()
        tbl._conn._packager.marshal.return_value = UDFSpec(
            name="identity",
            backend="DockerUDFSpecV1",
            udf_payload=DockerUDFSpecV1(
                image="test-image",
                tag="latest",
                workspace_checksum=None,
                udf_pickle=cloudpickle.dumps(identity),
            ).to_bytes(),
        )

        ns = tbl._conn.namespace_client()
        tbl.add_columns({"user_id": identity})

        req = ns.alter_table_add_columns.call_args[0][0]
        assert req.new_columns[0].virtual_column.input_columns == ["MetaData.UserId"]

    def test_add_columns_unpacked_udf_not_supported(self, table) -> None:
        """Remote multi-output UDF support is tracked separately in GEN-468."""
        from typing import NamedTuple

        from geneva import Columns, udf

        class Dimensions(NamedTuple):
            height: int
            width: int

        @udf
        def dimensions(a: int) -> Columns[Dimensions]:
            return Dimensions(a + 1, a + 2)

        with pytest.raises(NotImplementedError, match="does not yet support"):
            table.add_columns(dimensions)

        ns = table._conn.namespace_client()
        ns.alter_table_add_columns.assert_not_called()

    @pytest.mark.skip(
        reason="manifest/auto_backfill fields not yet in AddVirtualColumnEntry schema"
    )
    def test_add_columns_udf_with_manifest(self, table) -> None:
        """UDFs with @udf(manifest=...) forward manifest JSON."""
        import cloudpickle
        import pyarrow as pa

        from geneva import udf
        from geneva.manifest.mgr import GenevaManifest
        from geneva.packager import DockerUDFSpecV1, UDFSpec

        manifest = GenevaManifest(
            name="m1",
            pip=["numpy==1.26"],
            zips=[["s3://bucket/_geneva_uploads/workspace.zip"]],
        )

        @udf(data_type=pa.int32(), manifest=manifest)
        def with_manifest(a: int) -> int:
            return a + 1

        table._conn._packager = MagicMock()
        table._conn._packager.marshal.return_value = UDFSpec(
            name="with_manifest",
            backend="DockerUDFSpecV1",
            udf_payload=DockerUDFSpecV1(
                image="img",
                tag="v1",
                workspace_checksum=None,
                udf_pickle=cloudpickle.dumps(with_manifest),
            ).to_bytes(),
        )

        ns = table._conn.namespace_client()
        table.add_columns({"b": with_manifest})

        req = ns.alter_table_add_columns.call_args[0][0]
        vc = req.new_columns[0].virtual_column
        assert vc.manifest == manifest.to_json()
        assert vc.manifest_checksum == manifest.compute_checksum()

    def test_alter_columns_udf_dispatches_correctly(self, table) -> None:
        """alter_columns with UDF builds correct AlterColumnsEntry."""
        import cloudpickle
        import pyarrow as pa

        from geneva import udf
        from geneva.packager import DockerUDFSpecV1, UDFSpec

        @udf(data_type=pa.int32())
        def my_udf_v2(a: int) -> int:
            return a * 2

        table._conn._packager = MagicMock()
        table._conn._packager.marshal.return_value = UDFSpec(
            name="my_udf_v2",
            backend="DockerUDFSpecV1",
            udf_payload=DockerUDFSpecV1(
                image="img",
                tag="v2",
                workspace_checksum=None,
                udf_pickle=cloudpickle.dumps(my_udf_v2),
            ).to_bytes(),
        )

        ns = table._conn.namespace_client()
        table.alter_columns({"path": "a", "udf": my_udf_v2})

        ns.alter_table_alter_columns.assert_called_once()
        req = ns.alter_table_alter_columns.call_args[0][0]
        assert req.id == table._table_id
        assert len(req.alterations) == 1
        alt = req.alterations[0]
        assert alt.path == "a"
        assert alt.virtual_column is not None
        assert alt.virtual_column.udf_name == "my_udf_v2"
        assert alt.virtual_column.image == "img:v2"
        assert alt.virtual_column.input_columns == ["a"]
        table_ref = table._conn._packager.marshal.call_args.kwargs["table_ref"]
        assert table_ref.table_id == table._table_id

    def test_alter_columns_requires_path(self, table) -> None:
        with pytest.raises(ValueError, match="path is required"):
            table.alter_columns({"udf": MagicMock()})

    def test_alter_columns_rejects_both_keys(self, table) -> None:
        with pytest.raises(ValueError, match="not both"):
            table.alter_columns(
                {"path": "a", "udf": MagicMock(), "virtual_column": MagicMock()}
            )

    def test_alter_columns_forwards_non_udf_alterations(self, table) -> None:
        """Non-UDF alterations (rename etc.) pass through."""
        ns = table._conn.namespace_client()
        table.alter_columns({"path": "a", "rename": "a_new", "data_type": {}})

        req = ns.alter_table_alter_columns.call_args[0][0]
        alt = req.alterations[0]
        assert alt.path == "a"
        assert alt.rename == "a_new"

    def test_refresh_async_builds_correct_request(self, table) -> None:
        """refresh_async builds RefreshMaterializedViewRequest and POSTs it
        through the namespace client."""
        ns = table._conn.namespace_client()
        ns.refresh_materialized_view.return_value = MagicMock(job_id="refresh-1")

        from geneva.jobs.types import Job

        job = table.refresh_async(
            src_version=42,
            concurrency=16,
            intra_applier_concurrency=4,
            max_rows_per_fragment=1000,
            cluster="my_cluster",
            manifest="my_manifest",
        )

        ns.refresh_materialized_view.assert_called_once()
        req = ns.refresh_materialized_view.call_args[0][0]
        assert req.id == table._table_id
        assert req.src_version == 42
        assert req.concurrency == 16
        assert req.intra_applier_concurrency == 4
        assert req.max_rows_per_fragment == 1000
        assert req.cluster == "my_cluster"
        assert req.manifest == "my_manifest"
        assert req.output_limit is None
        assert isinstance(job, Job)
        assert job.job_id == "refresh-1"

    def test_refresh_async_records_job_in_history(self, table) -> None:
        ns = table._conn.namespace_client()
        ns.refresh_materialized_view.return_value = MagicMock(job_id="refresh-hist")

        table.refresh_async()

        table._conn._history.launch.assert_called_once_with(
            table.name, "", job_id="refresh-hist"
        )

    def test_refresh_blocks_on_job_result(self, table, monkeypatch) -> None:
        from datetime import timedelta

        from geneva.jobs.types import DONE, RefreshJobResult

        ns = table._conn.namespace_client()
        ns.refresh_materialized_view.return_value = MagicMock(job_id="refresh-sync")

        # Skip the live _geneva_jobs poll — return a fake terminal record
        # directly so ``Job._build_result`` constructs a RefreshJobResult.
        monkeypatch.setattr(
            "geneva.remote_v2.RemoteJobFuture.result",
            lambda self, timeout=None: MagicMock(status=DONE, job_id="refresh-sync"),
        )

        result = table.refresh(timeout=timedelta(seconds=30))

        assert isinstance(result, RefreshJobResult)
        assert result.job_id == "refresh-sync"

    def test_refresh_refreshes_to_latest(self, table, monkeypatch) -> None:
        """refresh() must refresh the in-memory handle after the job completes,
        so the materialized rows are visible without an explicit
        checkout_latest() — mirrors backfill() and the local _refresh path.
        Regression test: the remote refresh path used to return the job result
        without refreshing self._ltbl.
        """
        from datetime import timedelta

        from geneva.jobs.types import DONE

        ns = table._conn.namespace_client()
        ns.refresh_materialized_view.return_value = MagicMock(job_id="refresh-cl")
        monkeypatch.setattr(
            "geneva.remote_v2.RemoteJobFuture.result",
            lambda self, timeout=None: MagicMock(status=DONE, job_id="refresh-cl"),
        )
        refresh = MagicMock()
        monkeypatch.setattr(table, "checkout_latest", refresh)

        table.refresh(timeout=timedelta(seconds=30))

        ns.refresh_materialized_view.assert_called_once()
        refresh.assert_called_once()

    def test_refresh_output_limit_rejected_for_non_chunker_view(self, table) -> None:
        ns = table._conn.namespace_client()

        with pytest.raises(ValueError, match="chunker"):
            table.refresh(output_limit=10)

        ns.refresh_materialized_view.assert_not_called()
