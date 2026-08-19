# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Progress-based writer stall detection.

``FragmentWriterSession.drain()`` must distinguish a slow-but-progressing
writer (never killed, no matter how long the write takes) from a genuinely
wedged one (restarted within ~one no-progress deadline). Liveness comes from
probing the actor's ``progress()`` counter, not from the write future
resolving.
"""

import logging
import time
from pathlib import Path

import lance.fragment
import pyarrow as pa
import pytest
import ray
from lance.file import LanceFileReader
from ray_pipeline_test_utils import make_fragment_writer_session
from yarl import URL

import geneva.runners.ray.pipeline as pipeline_mod
from geneva import connect, udf
from geneva.checkpoint import CheckpointStore
from geneva.runners.ray.pipeline import FragmentWriterSession
from geneva.runners.ray.writer import FragmentWriteResult, WriterProgress

pytestmark = pytest.mark.ray


@udf(data_type=pa.int64())
def _liveness_udf(a: int) -> int:
    return a + 100


def _out_batch(start: int, end: int, value_base: int) -> pa.RecordBatch:
    return pa.RecordBatch.from_arrays(
        [
            pa.array(range(value_base + start, value_base + end), type=pa.int64()),
            pa.array(range(start, end), type=pa.uint64()),
        ],
        names=["out", "_rowaddr"],
    )


def _make_real_session(tmp_path: Path) -> tuple[FragmentWriterSession, str]:
    """Real table + checkpoints + session with both tasks ingested (not enqueued).

    Returns the session and the table URI. The caller controls how the writer
    starts and whether the seal sentinel is ever sent.
    """
    db = connect(str(tmp_path / "db"))
    tbl = db.create_table("t", pa.table({"a": list(range(16))}))
    tbl.add_columns({"out": _liveness_udf})
    dataset = tbl.to_lance()

    ckp_uri = str(URL(str(tmp_path)) / "ckp")
    store = CheckpointStore.from_uri(ckp_uri)
    store["ckptA_range-0-8"] = _out_batch(0, 8, 100)
    store["ckptB_range-8-16"] = _out_batch(8, 16, 100)

    sess = FragmentWriterSession(
        frag_id=0,
        ds_uri=tbl.uri,
        output_columns=["out"],
        checkpoint_store=store,
        where=None,
        read_version=dataset.version,
    )
    sess.ingest_task(0, "ckptA_range-0-8", 8)
    sess.ingest_task(8, "ckptB_range-8-16", 8)
    return sess, tbl.uri


def _read_staged(tbl_uri: str, result: FragmentWriteResult) -> pa.Table:
    staged_path = str(URL(tbl_uri) / "data" / result.new_file.path)
    return LanceFileReader(staged_path).read_all().to_table().sort_by("_rowaddr")


def test_drain_restarts_wedged_writer_and_recovers(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A writer wedged forever on ``queue.get`` (lost seal sentinel) makes no
    progress, so drain restarts it within ~one deadline; the restart replays
    the cached tasks and re-sends the sentinel, turning detection into
    recovery."""
    monkeypatch.setattr(pipeline_mod, "WRITER_NO_PROGRESS_TIMEOUT_S", 3.0)
    monkeypatch.setattr(pipeline_mod, "_DRAIN_POLL_INTERVAL_S", 0.2)

    sess, tbl_uri = _make_real_session(tmp_path)
    # Start the writer without replaying cached tasks and mark sealed without
    # sending the sentinel: write() blocks on the empty queue forever.
    sess._start_writer()
    sess.sealed = True
    try:
        results = list(sess.drain())

        # >= 1, not == 1: a cold replacement actor on a slow CI node can eat a
        # second deadline before its first bump.
        assert sess._restart_count >= 1
        assert len(results) == 1
        staged = _read_staged(tbl_uri, results[0])
        assert staged["_rowaddr"].to_pylist() == list(range(16))
        assert staged["out"].to_pylist() == list(range(100, 116))
    finally:
        sess.shutdown()


def test_drain_restarts_dead_actor_via_future_error_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Actor death must be detected by the write future failing with
    ``ActorDiedError`` (not by the no-progress deadline, set far above the
    test duration), and the fresh actor's reset counter must not trigger a
    spurious second restart."""
    monkeypatch.setattr(pipeline_mod, "WRITER_NO_PROGRESS_TIMEOUT_S", 60.0)
    monkeypatch.setattr(pipeline_mod, "_DRAIN_POLL_INTERVAL_S", 0.2)

    sess, tbl_uri = _make_real_session(tmp_path)
    # Wedged (no sentinel) so the write cannot finish before the kill lands.
    sess._start_writer()
    sess.sealed = True
    ray.kill(sess.actor)
    try:
        results = list(sess.drain())

        assert sess._restart_count == 1
        assert len(results) == 1
        staged = _read_staged(tbl_uri, results[0])
        assert staged["out"].to_pylist() == list(range(100, 116))
    finally:
        sess.shutdown()


_FAKE_DATA_FILE = lance.fragment.DataFile("fake.lance", [0], [0], 2, 0)


@ray.remote(num_cpus=0, max_concurrency=2)
class _FakeWriter:
    """Stand-in FragmentWriter: a timed write() with controllable progress."""

    def __init__(
        self,
        *,
        steps: int,
        step_s: float,
        probe_delay_s: float = 0.0,
        frozen: bool = False,
    ) -> None:
        self._snap = WriterProgress()
        self._steps = steps
        self._step_s = step_s
        self._probe_delay_s = probe_delay_s
        self._frozen = frozen

    def write(self) -> FragmentWriteResult:
        for i in range(self._steps):
            time.sleep(self._step_s)
            if not self._frozen:
                self._snap = WriterProgress(seq=i + 1, phase="write", batches_out=i + 1)
        return FragmentWriteResult(frag_id=0, new_file=_FAKE_DATA_FILE, rows_written=16)

    def progress(self) -> WriterProgress:
        if self._probe_delay_s:
            time.sleep(self._probe_delay_s)
        return self._snap


def _attach_fake_writer(
    sess: FragmentWriterSession, actor: "ray.actor.ActorHandle"
) -> None:
    from unittest.mock import MagicMock

    sess.queue = MagicMock()
    sess.actor = actor
    fut = actor.write.remote()
    sess.inflight[fut] = sess.frag_id
    sess.sealed = True


def test_drain_survives_slow_writer_with_progress(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The anti-livelock guarantee: a writer whose total runtime far exceeds
    the deadline is never restarted as long as its progress counter keeps
    advancing."""
    monkeypatch.setattr(pipeline_mod, "WRITER_NO_PROGRESS_TIMEOUT_S", 1.5)
    monkeypatch.setattr(pipeline_mod, "_DRAIN_POLL_INTERVAL_S", 0.1)

    sess = make_fragment_writer_session()
    actor = _FakeWriter.remote(steps=12, step_s=0.25)  # ~3s total, bump each step
    _attach_fake_writer(sess, actor)
    try:
        results = list(sess.drain())

        assert sess._restart_count == 0
        assert len(results) == 1
        assert results[0].rows_written == 16
    finally:
        ray.kill(actor)


def test_drain_tolerates_sluggish_frozen_probe(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A slow probe returning a never-advancing counter is 'no advance', never
    an instant kill, and drain keeps polling the write future while a probe is
    outstanding; the write finishes inside the deadline with no restart."""
    monkeypatch.setattr(pipeline_mod, "WRITER_NO_PROGRESS_TIMEOUT_S", 8.0)
    monkeypatch.setattr(pipeline_mod, "_DRAIN_POLL_INTERVAL_S", 0.1)

    sess = make_fragment_writer_session()
    actor = _FakeWriter.remote(steps=1, step_s=2.5, probe_delay_s=1.0, frozen=True)
    _attach_fake_writer(sess, actor)
    try:
        results = list(sess.drain())

        assert sess._restart_count == 0
        assert len(results) == 1
    finally:
        ray.kill(actor)


def test_removed_stall_rounds_env_var_warns_once(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    """GENEVA_WRITER_STALL_IDLE_ROUNDS is gone: setting it warns exactly once
    per process, pointing at the new escape hatch."""
    assert not hasattr(pipeline_mod, "GENEVA_WRITER_STALL_IDLE_ROUNDS")
    monkeypatch.setenv("GENEVA_WRITER_STALL_IDLE_ROUNDS", "360")
    monkeypatch.setattr(pipeline_mod, "_warned_stall_rounds_removed", False)

    with caplog.at_level(logging.WARNING, logger="geneva.runners.ray.pipeline"):
        sess = make_fragment_writer_session()
        list(sess.drain())  # nothing inflight: warns and returns immediately
        list(sess.drain())

    warnings = [
        r for r in caplog.records if "GENEVA_WRITER_STALL_IDLE_ROUNDS" in r.getMessage()
    ]
    assert len(warnings) == 1
    assert "GENEVA_WRITER_NO_PROGRESS_TIMEOUT_S" in warnings[0].getMessage()
