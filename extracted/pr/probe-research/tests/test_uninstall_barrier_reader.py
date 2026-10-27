"""The uninstall barrier as every installer reads it (plan clean-uninstall-reinstall, Build contract).

LIVE: its owner (pid + start) runs, OR its phase is anything but "planned",
"stopping" or "draining" (an unknown or missing phase included). A file that
cannot be read or parsed is LIVE for 60 min after its mtime, then STALE.
STALE: owner gone at a reversible phase; an installer may clear it.
"""

from __future__ import annotations

import json
import os
import time

import pytest

from probe._shared import uninstall_barrier as barrier
from probe.service import procid

GONE_PID = 2 ** 22 - 3  # above the default pid_max: no process has it


def _write(**fields) -> None:
    path = barrier.path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"v": 1, "at": time.time(), "plan": "x", **fields}))


def _mine() -> dict:
    return {"pid": os.getpid(), "start": procid.start_time(os.getpid())}


def test_no_barrier_is_absent():
    assert barrier.state() == barrier.State.ABSENT and barrier.refusal() is None
    barrier.check()
    assert barrier.clear_stale() is None


@pytest.mark.parametrize("phase", barrier.PHASES)
def test_a_running_owner_is_live_at_every_phase(phase):
    _write(phase=phase, **_mine())
    assert barrier.state() == barrier.State.LIVE
    with pytest.raises(barrier.UninstallRunning, match="running"):
        barrier.check()
    assert barrier.clear_stale() is None and barrier.path().exists()


@pytest.mark.parametrize("phase", barrier.REVERSIBLE)
def test_a_dead_owner_at_a_reversible_phase_is_stale_and_cleared(phase):
    _write(phase=phase, pid=GONE_PID, start="1")
    assert barrier.state() == barrier.State.STALE and barrier.refusal() is None
    assert "cleared a stale uninstall barrier" in barrier.clear_stale()
    assert not barrier.path().exists()


@pytest.mark.parametrize("phase", ["server", "integrations", "state", "finishing", "something-new", None])
def test_a_dead_owner_past_the_reversible_phases_is_live_and_must_be_finished(phase):
    fields = {"pid": GONE_PID, "start": "1"}
    if phase is not None:
        fields["phase"] = phase
    _write(**fields)
    assert barrier.state() == barrier.State.LIVE
    assert "must be finished first" in barrier.refusal() and "probe uninstall" in barrier.refusal()
    assert barrier.clear_stale() is None


def test_an_unreadable_barrier_is_live_for_an_hour_then_stale():
    path = barrier.path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('{"v": 1, "pid": ')
    assert barrier.state() == barrier.State.LIVE and "cannot be read" in barrier.refusal()
    old = time.time() - barrier.UNREADABLE_LIVE_S - 60
    os.utime(path, (old, old))
    assert barrier.state() == barrier.State.STALE
    assert "unreadable" in barrier.clear_stale() and not path.exists()


def test_another_schema_is_live():
    _write(phase="planned", pid=GONE_PID, start="1")
    data = json.loads(barrier.path().read_text())
    barrier.path().write_text(json.dumps({**data, "v": 2}))
    assert barrier.state() == barrier.State.LIVE
