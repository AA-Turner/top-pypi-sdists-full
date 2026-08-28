# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Progress-based writer stall detection.

``FragmentWriterManager.drain_sessions()`` must distinguish a
slow-but-progressing writer (never killed, no matter how long the write takes)
from a genuinely wedged one (restarted within ~one no-progress deadline).
Liveness comes from probing the actor's ``progress()`` counter, not from the
write future resolving.

These drove ``FragmentWriterSession.drain()`` until teardown moved to a shared
drain over every session at once -- a serial per-session drain deadlocks when
writers contend for memory. The guarantees are unchanged; only the loop that
enforces them moved up to the manager, so the tests drive it there.
"""

import logging
import time
from pathlib import Path

import lance.fragment
import pyarrow as pa
import pytest
import ray
from lance.file import LanceFileReader
from ray_pipeline_test_utils import (
    attach_started_writer_future,
    make_fragment_writer_manager,
    make_fragment_writer_session,
)
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


def _drain(*sessions: FragmentWriterSession) -> list[FragmentWriteResult]:
    """Drain sessions through the manager, the way teardown does.

    Liveness is enforced by ``FragmentWriterManager.drain_sessions()``, which
    waits on every session's futures together and ticks each session's
    no-progress watchdog. Wrapping a lone session keeps these tests focused on
    the watchdog rather than on the multi-session scheduling.
    """
    manager = make_fragment_writer_manager(
        sessions={s.frag_id: s for s in sessions},
    )
    return list(manager.drain_sessions())


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
        results = _drain(sess)

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
        results = _drain(sess)

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
        results = _drain(sess)

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
        results = _drain(sess)

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
        _drain(sess)  # nothing inflight: warns and returns immediately
        _drain(sess)

    warnings = [
        r for r in caplog.records if "GENEVA_WRITER_STALL_IDLE_ROUNDS" in r.getMessage()
    ]
    assert len(warnings) == 1
    assert "GENEVA_WRITER_NO_PROGRESS_TIMEOUT_S" in warnings[0].getMessage()


class _Method:
    """A stand-in for an actor method handle, counting its calls."""

    def __init__(self, ref: object) -> None:
        self.ref = ref
        self.calls = 0

    def remote(self, *_args: object, **_kw: object) -> object:
        self.calls += 1
        return self.ref


class _UnplacedHandle:
    """An actor handle Ray has returned but not yet scheduled.

    A plain class rather than ``MagicMock``: mock refuses to synthesize dunder
    attributes, and ``__ray_ready__`` is the one that matters here.
    """

    def __init__(self) -> None:
        self.ready_ref = object()
        self.__ray_ready__ = _Method(self.ready_ref)
        self.progress = _Method(object())


def _unplaced_writer(sess: FragmentWriterSession) -> None:
    """Give ``sess`` an actor handle Ray has not scheduled.

    A queued writer is indistinguishable from a running one by handle alone:
    ``started`` is True the moment ``.remote()`` returns. What separates them
    is ``__ray_ready__``, which resolves only once the actor is alive.
    """
    from unittest.mock import MagicMock

    sess.queue = MagicMock()
    sess.actor = _UnplacedHandle()
    sess.sealed = True
    sess._begin_placement_window()


def test_a_queued_writer_is_not_charged_the_progress_deadline(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Writers take turns; waiting for a slot is not a stall.

    Sessions are drained together, so a writer still queued for memory is
    polled alongside the one holding the slot. It cannot answer a progress
    probe -- nothing is running yet -- so charging it the no-progress deadline
    spends its whole restart budget waiting for a turn it was always going to
    get, while the healthy writer ahead of it runs its legitimate 30-70
    minutes.
    """
    monkeypatch.setattr(pipeline_mod, "WRITER_NO_PROGRESS_TIMEOUT_S", 1.0)

    now = [0.0]
    # Patched before the session exists: both deadlines are computed from this
    # clock, so a real ``monotonic`` reading cannot leave them in the future.
    monkeypatch.setattr(pipeline_mod.time, "monotonic", lambda: now[0])
    # Ray never reports this actor ready: it is queued for memory the whole time.
    monkeypatch.setattr(pipeline_mod.ray, "wait", lambda fs, **kw: ([], list(fs)))

    sess = make_fragment_writer_session()
    _unplaced_writer(sess)
    sess.begin_liveness_window()

    # Far past the progress deadline, many times over.
    for i in range(1, pipeline_mod.MAX_WRITER_RESTARTS + 3):
        now[0] = i * 2.0
        sess.poll_liveness()

    assert sess._restart_count == 0, "a queued writer must keep its retry budget"
    # And it never probed for progress, because there is nothing to probe.
    assert sess.actor.progress.calls == 0


def _sealed_session_placed(frag_id: int):  # noqa: ANN202
    """A sealed session whose actor Ray has placed and which is writing."""
    sess = make_fragment_writer_session(frag_id=frag_id)
    sess.sealed = True
    fut = attach_started_writer_future(sess)  # marks it placed
    return sess, fut


def _drain_manager(*sessions: FragmentWriterSession):  # noqa: ANN202
    return make_fragment_writer_manager(sessions={s.frag_id: s for s in sessions})


def test_one_placed_writer_keeps_the_whole_drain_alive(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The liveness invariant: if a writer is placed, the job completes.

    That writer runs for however long its fragment takes -- legitimately
    30-70+ minutes for large blobs -- then finishes, is reaped, and hands its
    reservation to the next in line. So a queued writer sitting behind it is
    not evidence of anything wrong, however long it waits.
    """
    now = [0.0]
    monkeypatch.setattr(pipeline_mod.time, "monotonic", lambda: now[0])
    monkeypatch.setattr(pipeline_mod, "WRITER_PLACEMENT_STALL_S", 100.0)

    running, _fut = _sealed_session_placed(0)
    queued = make_fragment_writer_session(frag_id=1)
    _unplaced_writer(queued)
    manager = _drain_manager(running, queued)

    # Far past the stall window, many times over: one writer is placed the
    # whole time, so the drain is alive no matter how long the other waits.
    for i in range(1, 20):
        now[0] = i * 500.0
        manager._check_drain_liveness()


def test_no_writer_placed_at_all_is_the_deadlock(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Nobody running means nobody will ever free anything.

    This is the only state the drain cannot resolve on its own: with no writer
    placed, no reservation is returned, so no queued writer becomes placeable.
    """
    now = [0.0]
    monkeypatch.setattr(pipeline_mod.time, "monotonic", lambda: now[0])
    monkeypatch.setattr(pipeline_mod, "WRITER_PLACEMENT_STALL_S", 100.0)

    a = make_fragment_writer_session(frag_id=0)
    b = make_fragment_writer_session(frag_id=1)
    for sess in (a, b):
        _unplaced_writer(sess)
    manager = _drain_manager(a, b)
    manager._note_writer_turnover()

    now[0] = 50.0
    manager._check_drain_liveness()  # inside the window: still patient

    now[0] = 101.0
    with pytest.raises(RuntimeError, match="No FragmentWriter has been placed"):
        manager._check_drain_liveness()


def test_a_completion_counts_as_turnover(monkeypatch: pytest.MonkeyPatch) -> None:
    """A finished writer restarts the clock even if nothing is placed yet.

    Between one writer being reaped and the next being placed there is a
    moment with none running. That is the queue moving, not stalling.
    """
    now = [0.0]
    monkeypatch.setattr(pipeline_mod.time, "monotonic", lambda: now[0])
    monkeypatch.setattr(pipeline_mod, "WRITER_PLACEMENT_STALL_S", 100.0)

    sess = make_fragment_writer_session(frag_id=0)
    _unplaced_writer(sess)
    manager = _drain_manager(sess)
    manager._note_writer_turnover()

    # A completion lands at 80s, well inside the window.
    now[0] = 80.0
    manager._note_writer_turnover()

    # 90s later it is still fine: the clock restarted at the completion.
    now[0] = 170.0
    manager._check_drain_liveness()

    # Only a full window with nothing placed and nothing finishing fails.
    now[0] = 181.0
    with pytest.raises(RuntimeError, match="No FragmentWriter has been placed"):
        manager._check_drain_liveness()


def test_placement_arms_the_progress_deadline(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Once placed, the writer is watched -- and the clock starts there."""
    monkeypatch.setattr(pipeline_mod, "WRITER_NO_PROGRESS_TIMEOUT_S", 10.0)

    now = [0.0]
    monkeypatch.setattr(pipeline_mod.time, "monotonic", lambda: now[0])

    sess = make_fragment_writer_session()
    _unplaced_writer(sess)
    sess.begin_liveness_window()

    ready_fut = sess.actor.ready_ref
    monkeypatch.setattr(
        pipeline_mod.ray,
        "wait",
        lambda fs, **kw: (list(fs), []) if fs == [ready_fut] else ([], list(fs)),
    )

    # Queued for a long time, then placed.
    now[0] = 500.0
    sess.poll_liveness()

    assert sess._placed is True
    # The progress deadline starts at placement, not at seal, so the 500s of
    # queueing is not counted against it.
    assert sess._live_last_advance == 500.0
    assert sess._restart_count == 0
