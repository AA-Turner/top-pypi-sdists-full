# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Unit tests for the enterprise (db://) remote progress display.

Exercises ``RemoteJob._poll_until_done`` with a mocked connection and a fake
tqdm, so no phalanx/cluster is needed. Locks in that the remote client:

  * renders ``record.events`` as a dedicated always-latest line (so the
    provisioning / planning / executing phases surface, not just RUNNING),
  * shows the ``plan_fragments`` planning metric (allow-listed) and refreshes
    its sub-step description each poll instead of freezing it at creation.
"""

from unittest.mock import MagicMock

import pytest

from geneva.jobs.jobs import JobMetric, JobRecord, JobStatus
from geneva.jobs.remote import _VISIBLE_METRICS, RemoteJob


class _FakeBar:
    """Minimal tqdm stand-in that records its description over time."""

    instances: list["_FakeBar"] = []

    def __init__(
        self,
        *,
        total: int = 0,
        desc: str = "",
        bar_format: str = "",
        position: int = 0,
        leave: bool = True,
    ) -> None:
        self.total = total
        self.desc = desc
        self.bar_format = bar_format
        self.position = position
        self.n = 0
        self.closed = False
        self.desc_history = [desc]
        _FakeBar.instances.append(self)

    def refresh(self) -> None:
        self.desc_history.append(self.desc)

    def close(self) -> None:
        self.closed = True


def _rec(status: JobStatus, events: list[str], metrics: list[JobMetric]) -> JobRecord:
    return JobRecord(
        table_name="t",
        column_name="c",
        job_id="j1",
        status=status,
        events=events,
        metrics=metrics,
    )


def test_plan_fragments_is_client_visible() -> None:
    assert "plan_fragments" in _VISIBLE_METRICS


def test_remote_poll_renders_events_and_planning(monkeypatch) -> None:
    monkeypatch.setattr("geneva.tqdm.tqdm", _FakeBar)
    _FakeBar.instances.clear()

    plan_scanning = JobMetric(
        name="plan_fragments", n=0, total=0, done=False, desc="scanning checkpoints"
    )
    plan_building = JobMetric(
        name="plan_fragments", n=3, total=10, done=False, desc="building tasks"
    )
    # A non-allow-listed metric must never produce a bar.
    hidden = JobMetric(
        name="batch_checkpointing_time", n=1, total=0, done=False, desc="hidden"
    )

    records = [
        _rec(
            JobStatus.RUNNING,
            ["Entering phase: Cluster provisioning"],
            [plan_scanning, hidden],
        ),
        _rec(
            JobStatus.RUNNING,
            ["Entering phase: Cluster provisioning", "Entering phase: Job planning"],
            [plan_building, hidden],
        ),
        _rec(
            JobStatus.DONE,
            ["Entering phase: Job planning", "Entering phase: Executing backfill"],
            [],
        ),
    ]
    conn = MagicMock()
    conn.get_job.side_effect = records

    job = RemoteJob(job_id="j1", table_name="t", conn=conn)
    result = job._poll_until_done(refresh_secs=0.0)
    assert _status_value(result.status) == "DONE"

    # Bars are distinguishable by bar_format: events line uses "{desc}",
    # the status line uses "{desc} [{elapsed}]", metric bars pass neither.
    events_bars = [b for b in _FakeBar.instances if b.bar_format == "{desc}"]
    metric_bars = [b for b in _FakeBar.instances if b.bar_format == ""]

    assert len(events_bars) == 1
    events_history = " || ".join(events_bars[0].desc_history)
    # The events line advances through the phases (not frozen at creation).
    assert "Cluster provisioning" in events_history
    assert "Executing backfill" in events_history

    # Exactly one metric bar (plan_fragments); the hidden metric is filtered out.
    assert len(metric_bars) == 1
    plan_history = " || ".join(metric_bars[0].desc_history)
    assert "scanning checkpoints" in plan_history  # first sub-step
    assert "building tasks" in plan_history  # desc refreshed, not frozen


def test_sync_driver_status_ticks_render_live_and_share_bars(monkeypatch) -> None:
    """Table.backfill's sync loop polls done()+status() then result(). The
    status() ticks must render live, and result() must reuse the same renderer
    (one set of bars), not draw a second set at the end."""
    from geneva.remote_v2 import RemoteJobFuture

    monkeypatch.setattr("geneva.tqdm.tqdm", _FakeBar)
    _FakeBar.instances.clear()

    plan_scanning = JobMetric(
        name="plan_fragments", n=0, total=0, done=False, desc="scanning checkpoints"
    )
    plan_building = JobMetric(
        name="plan_fragments", n=5, total=10, done=False, desc="building tasks"
    )
    running1 = _rec(
        JobStatus.RUNNING, ["Entering phase: Cluster provisioning"], [plan_scanning]
    )
    running2 = _rec(
        JobStatus.RUNNING, ["Entering phase: Job planning"], [plan_building]
    )
    done = _rec(JobStatus.DONE, ["Entering phase: Executing backfill"], [])

    conn = MagicMock()
    # Two live status() reads, then result()'s poll reads the terminal record.
    conn.get_job.side_effect = [running1, running2, done]

    fut = RemoteJobFuture(RemoteJob(job_id="j1", table_name="t", conn=conn))
    fut.status()  # live tick 1 (provisioning + scanning)
    fut.status()  # live tick 2 (planning + building)
    fut.result()  # blocking finish, reusing the same renderer

    events_bars = [b for b in _FakeBar.instances if b.bar_format == "{desc}"]
    metric_bars = [b for b in _FakeBar.instances if b.bar_format == ""]

    # Shared renderer across status()+result(): exactly one of each, not two.
    assert len(events_bars) == 1
    assert len(metric_bars) == 1

    events_history = " || ".join(events_bars[0].desc_history)
    assert "Cluster provisioning" in events_history  # from the first live tick
    assert "Executing backfill" in events_history  # from result()'s final poll
    plan_history = " || ".join(metric_bars[0].desc_history)
    assert "scanning checkpoints" in plan_history
    assert "building tasks" in plan_history


def test_remote_future_initializes_inherited_span_slots() -> None:
    # JobFuture is a slotted @attrs.define with init=False _otel_span /
    # _span_closed fields; the hand-written RemoteJobFuture.__init__ must call
    # super().__init__ or reading those slots (e.g. _close_span) AttributeErrors.
    from geneva.remote_v2 import RemoteJobFuture

    rj = MagicMock(spec=RemoteJob)
    rj.job_id = "j1"
    fut = RemoteJobFuture(rj)

    assert fut.job_id == "j1"
    assert fut._otel_span is None
    assert fut._span_closed is False
    fut._close_span(None)  # exercises the slot reads; must not raise


def test_thread_future_initializes_inherited_span_slots() -> None:
    import threading

    from geneva.table import _ThreadJobFuture

    fut = _ThreadJobFuture("j1", threading.Event(), {}, {})
    assert fut.job_id == "j1"
    assert fut._otel_span is None
    assert fut._span_closed is False
    fut._close_span(None)  # must not raise


def test_result_timeout_keeps_renderer_open_for_retry(monkeypatch) -> None:
    # A bounded-timeout poll must not tear down the cached renderer, so a retry
    # reuses it instead of ticking into closed bars.
    from geneva.remote_v2 import RemoteJobFuture

    monkeypatch.setattr("geneva.tqdm.tqdm", _FakeBar)
    _FakeBar.instances.clear()

    rj = MagicMock(spec=RemoteJob)
    rj.job_id = "j1"
    rj.result.side_effect = [
        TimeoutError("still running"),
        _rec(JobStatus.DONE, [], []),
    ]
    fut = RemoteJobFuture(rj)

    with pytest.raises(TimeoutError):
        fut.result(timeout=0.01)
    bars = fut._bars
    assert bars is not None
    assert bars._closed is False  # kept open on timeout

    fut.result()  # retry
    assert fut._bars is bars  # same renderer reused
    assert bars._closed is True  # closed once the job resolves


def _status_value(status: object) -> str:
    return status.value if hasattr(status, "value") else str(status)


if __name__ == "__main__":
    pytest.main([__file__, "-q"])
