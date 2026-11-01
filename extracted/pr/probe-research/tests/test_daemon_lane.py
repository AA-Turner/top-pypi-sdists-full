"""Every lane the worker runs beside the writer has the Lane shape (daemon/lane.py)."""

from __future__ import annotations

import inspect
import time
from types import SimpleNamespace

import pytest

from probe.daemon.lane import Lane
from probe.daemon.lanes.audit import AuditLane
from probe.daemon.lanes.reader import ReaderLane
from probe.daemon.lanes.run_alerts import RunAlertLane

LANES = [ReaderLane, RunAlertLane, AuditLane]


@pytest.mark.parametrize("lane", LANES, ids=lambda cls: cls.__name__)
def test_a_lane_runs_and_stops_as_coroutines(lane):
    assert inspect.iscoroutinefunction(lane.run)
    assert inspect.iscoroutinefunction(lane.stop)


@pytest.mark.parametrize("lane", LANES, ids=lambda cls: cls.__name__)
def test_a_new_lane_is_a_lane_with_no_task_yet(lane, tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    store = SimpleNamespace(on_read_turn_closed=None)
    worker = SimpleNamespace(store=store, session=SimpleNamespace(session_id="lane-shape", transcript=tmp_path / "t.jsonl"),
                             clock=time.time, replay=None, stopping=False)
    made = lane(worker)
    assert isinstance(made, Lane)
    assert made.task is None
