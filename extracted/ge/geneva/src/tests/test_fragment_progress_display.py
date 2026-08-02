# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Unit tests for the always-on backfill progress display in RayJobFuture.

These exercise the render logic in ``RayJobFuture._sync_bars`` directly with a
synthetic metrics snapshot, so no Ray cluster is required.
"""

from geneva.runners.ray.pipeline import (
    CNT_WORKERS_ACTIVE,
    METRIC_AVG_BATCH_NUM_ROWS,
    METRIC_AVG_BATCH_SIZE,
    METRIC_PLAN_READ_TIME,
    METRIC_READ_IO_TIME,
    METRIC_ROWS_SKIPPED,
    METRIC_UDF_PROCESSING_TIME,
    RayJobFuture,
)

_DIAG_KEYS = {
    "_diag_heartbeat",
    "_diag_phase",
    "_diag_stages",
    "_diag_throughput",
    "_diag_writer",
}


def _metric(n: int, total: int, desc: str) -> dict:
    return {"n": n, "total": total, "done": False, "desc": desc}


def _snapshot() -> dict[str, dict]:
    return {
        "rows_checkpointed": _metric(10, 100, "Rows checkpointed"),
        "rows_ready_for_commit": _metric(5, 100, "Rows ready for commit"),
        "rows_committed": _metric(1, 100, "Rows committed"),
        "tasks_completed": _metric(7, 20, "Tasks completed"),
        "writer_fragments": _metric(3, 20, "Fragments written"),
        "fragments": _metric(15, 20, "Tasks scheduled"),
        METRIC_UDF_PROCESSING_TIME: _metric(800, 0, "udf"),
        METRIC_READ_IO_TIME: _metric(200, 0, "io"),
    }


def _diag_snapshot() -> dict[str, dict]:
    """Snapshot enriched with the metrics the diagnostic lines read."""
    snap = _snapshot()
    snap.update(
        {
            # active appliers / configured concurrency -> worker utilization
            CNT_WORKERS_ACTIVE: {"n": 2, "total": 4, "done": False, "desc": "workers"},
            # reconciled batch shape
            METRIC_AVG_BATCH_NUM_ROWS: _metric(480, 0, "avg batch rows"),
            METRIC_AVG_BATCH_SIZE: _metric(13_000_000, 0, "avg batch bytes"),
        }
    )
    return snap


def _make_future(job_id: str = "test-job") -> RayJobFuture:
    # ray_obj_ref/job_tracker are only used by other methods; _sync_bars reads
    # neither, so a sentinel object is sufficient here.
    return RayJobFuture(ray_obj_ref=object(), job_tracker=None, job_id=job_id)


def _diag_future(snapshot: dict | None = None) -> RayJobFuture:
    fut = _make_future()
    fut._sync_bars(_diag_snapshot() if snapshot is None else snapshot)
    return fut


def test_shows_all_bars() -> None:
    # The display is always-on: the job line, the three row bars, and the two
    # fragment/task bars are all rendered. "fragments" (scheduled) is the one
    # snapshot metric intentionally never given its own bar.
    fut = _make_future()

    fut._sync_bars(_snapshot())

    assert set(fut._pbars) >= {
        fut._JOB_ID_KEY,
        "rows_checkpointed",
        "rows_ready_for_commit",
        "rows_committed",
        "tasks_completed",
        "writer_fragments",
    }
    assert "fragments" not in fut._pbars
    assert set(fut._pbars) >= _DIAG_KEYS

    bar = fut._pbars["tasks_completed"]
    assert bar.n == 7
    assert bar.total == 20


def test_fragment_bar_clamps_overshoot() -> None:
    # Retried/bisected ReadTasks can push tasks_completed past its plan-time
    # total; the rendered bar must clamp to the total rather than exceed 100%.
    fut = _make_future()

    snapshot = _snapshot()
    snapshot["tasks_completed"] = {
        "n": 25,
        "total": 20,
        "done": True,
        "desc": "Tasks completed",
    }
    fut._sync_bars(snapshot)

    bar = fut._pbars["tasks_completed"]
    assert bar.total == 20
    assert bar.n == 20  # clamped, not 25


def test_job_id_line_shown() -> None:
    fut = _make_future()

    fut._sync_bars(_snapshot())

    assert fut._JOB_ID_KEY in fut._pbars
    assert "test-job" in fut._pbars[fut._JOB_ID_KEY].desc


def test_job_id_line_absent_without_job_id() -> None:
    fut = _make_future(job_id="")

    fut._sync_bars(_snapshot())

    assert fut._JOB_ID_KEY not in fut._pbars


def test_diagnostic_worker_utilization() -> None:
    fut = _diag_future()
    # 2 active appliers of 4 configured slots.
    assert "workers 2/4 (50%)" in fut._pbars[fut._HEARTBEAT_KEY].desc


def test_diagnostic_batch_shape() -> None:
    fut = _diag_future()
    desc = fut._pbars[fut._THROUGHPUT_KEY].desc
    assert "batch ~480 rows" in desc
    assert "MiB" in desc  # 13 MB -> binary-suffix formatting


def test_diagnostic_stage_bottleneck() -> None:
    fut = _diag_future()
    # udf (800ms) dominates io (200ms) in the snapshot.
    assert "slowest udf" in fut._pbars[fut._STAGES_KEY].desc


def test_diagnostic_commit_lag() -> None:
    fut = _diag_future()
    # rows_checkpointed=10, rows_committed=1 -> lag 9.
    assert "commit-lag 9 rows" in fut._pbars[fut._WRITER_KEY].desc


def test_diagnostic_skipped_line_reflects_count() -> None:
    # Always present (stable layout); shows the running count.
    fut = _diag_future()
    assert fut._SKIPPED_KEY in fut._pbars
    assert "skipped" in fut._pbars[fut._SKIPPED_KEY].desc
    assert "0 rows" in fut._pbars[fut._SKIPPED_KEY].desc

    snap = _diag_snapshot()
    snap[METRIC_ROWS_SKIPPED] = _metric(5, 0, "rows skipped")
    fut2 = _diag_future(snap)
    assert "5 rows" in fut2._pbars[fut2._SKIPPED_KEY].desc


def test_diagnostic_plan_time_after_planning() -> None:
    snap = _diag_snapshot()
    snap[METRIC_PLAN_READ_TIME] = _metric(8200, 0, "plan/read")
    fut = _diag_future(snap)
    assert "8.2s to plan/read" in fut._pbars[fut._PLAN_KEY].desc


def test_diagnostic_plan_time_shows_planning_before_rows() -> None:
    # Before planning records its time and before any rows move, the line names
    # the phase instead of leaving dead air.
    snap = _diag_snapshot()
    snap["rows_checkpointed"] = _metric(0, 100, "Rows checkpointed")
    fut = _diag_future(snap)
    assert "planning..." in fut._pbars[fut._PLAN_KEY].desc


def test_workers_line_unconditional() -> None:
    # The workers line is created even when the first snapshot lacks the
    # cluster-status counters (they land a poll or two later), so it keeps its
    # alphabetical slot between throughput and stages rather than surfacing
    # below the row bars on a later poll.
    fut = _make_future()
    fut._sync_bars(_snapshot())  # _snapshot() carries no CNT_WORKERS_* counters

    keys = list(fut._pbars)
    assert fut._RAY_LINE_KEY in keys
    assert keys.index(fut._THROUGHPUT_KEY) < keys.index(fut._RAY_LINE_KEY)
    assert keys.index(fut._RAY_LINE_KEY) < keys.index(fut._STAGES_KEY)
    assert keys.index(fut._RAY_LINE_KEY) < keys.index("rows_checkpointed")


def test_line_order() -> None:
    # Layout: job on top, the non-bar status lines (alphabetical by label) in
    # the middle, all progress bars at the bottom. Everything is unconditional,
    # so the order is stable for the whole run.
    fut = _make_future()
    fut._sync_bars(_diag_snapshot())
    assert list(fut._pbars) == [
        fut._JOB_ID_KEY,
        fut._HEARTBEAT_KEY,  # geneva | heartbeat
        fut._PHASE_KEY,  # geneva | phase
        fut._PLAN_KEY,  # geneva | plan
        fut._SKIPPED_KEY,  # geneva | skipped
        fut._THROUGHPUT_KEY,  # geneva | throughput
        fut._RAY_LINE_KEY,  # geneva | workers
        fut._STAGES_KEY,  # stages |
        fut._WRITER_KEY,  # writer |
        "rows_checkpointed",
        "rows_ready_for_commit",
        "rows_committed",
        "tasks_completed",
        "writer_fragments",
    ]


def _drain_snapshot() -> dict[str, dict]:
    """Reads finished; the writer is still sealing/committing fragments."""
    snap = _diag_snapshot()
    snap["tasks_completed"] = {"n": 20, "total": 20, "done": True, "desc": "reads"}
    snap["fragments"] = {"n": 20, "total": 20, "done": True, "desc": "scheduled"}
    snap["rows_checkpointed"] = _metric(100, 100, "Rows checkpointed")
    snap["rows_ready_for_commit"] = _metric(75, 100, "Rows ready for commit")
    snap["rows_committed"] = {"n": 60, "total": 100, "done": False, "desc": "committed"}
    snap["writer_fragments"] = {"n": 15, "total": 20, "done": False, "desc": "frags"}
    return snap


def test_phase_line_reading() -> None:
    # Reads still in flight (tasks 7/20) -> compute phase.
    fut = _diag_future()
    assert "computing" in fut._pbars[fut._PHASE_KEY].desc


def test_phase_line_draining() -> None:
    # Reads done, commits still draining -> explicit drain message with the
    # fragment count, commit lag, and the "suspension expected" note.
    fut = _diag_future(_drain_snapshot())
    desc = fut._pbars[fut._PHASE_KEY].desc
    assert "writing & committing" in desc
    assert "15/20 fragments" in desc
    assert "commit-lag 40 rows" in desc  # checkpointed 100 - committed 60
    assert "worker suspension expected" in desc


def test_phase_line_done() -> None:
    # Everything committed -> terminal state, not a stale "computing" flash.
    snap = _drain_snapshot()
    snap["rows_committed"] = {"n": 100, "total": 100, "done": True, "desc": "committed"}
    fut = _diag_future(snap)
    assert "all fragments committed" in fut._pbars[fut._PHASE_KEY].desc


def test_throughput_relabels_to_committing_in_drain() -> None:
    # While reading, the line tracks checkpointed rows under "throughput:";
    # once draining it tracks committed rows under "committing:".
    reading = _diag_future()
    assert "throughput:" in reading._pbars[reading._THROUGHPUT_KEY].desc
    fut = _diag_future(_drain_snapshot())
    assert "committing:" in fut._pbars[fut._THROUGHPUT_KEY].desc


def test_heartbeat_fresh_when_only_commits_advance() -> None:
    # During the drain tail rows_checkpointed is pinned at its total; the
    # liveness baseline must still advance as committed rows climb, so the
    # heartbeat does not read as stalled while the writer is working.
    fut = _make_future()
    snap = _drain_snapshot()
    fut._sync_bars(snap)
    base = fut._last_progress_n

    snap["rows_committed"] = {"n": 80, "total": 100, "done": False, "desc": "committed"}
    fut._sync_bars(snap)
    assert fut._last_progress_n > base
