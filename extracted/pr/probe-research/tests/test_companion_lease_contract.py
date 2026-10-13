"""The daemon's lease file is a contract between two packages that cannot import
each other: the tap plugin's worker WRITES it (`tap/companion_lease.py`), the
probe CLI's gate, hooks and status line READ it (`session_marker`). This writes
with the one and reads with the other, so a format change on either side fails
here instead of silently reading every live lease as degraded (or worse, every
dead one as live).
"""

from __future__ import annotations

import importlib.util
import json
import time
from pathlib import Path

import pytest

from probe.sdk import session_marker

TAP = Path(__file__).resolve().parents[1] / "plugins" / "probe-research-tap" / "tap"
SID = "11111111-2222-3333-4444-555555555555"


@pytest.fixture
def writer(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    spec = importlib.util.spec_from_file_location("_tap_companion_lease", TAP / "companion_lease.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_the_two_sides_agree_on_names():
    source = (TAP / "companion_lease.py").read_text()
    assert f"LEASE_VERSION = {session_marker.LEASE_VERSION}" in source
    assert f'LEASE_SUFFIX = "{session_marker.LEASE_SUFFIX}"' in source


def test_a_renewed_lease_reads_live(writer):
    assert session_marker.set_session_state(SID, session_marker.STATE_DAEMON)
    assert writer.lease_path(SID) == session_marker.lease_path(SID)
    writer.renew(SID)
    assert session_marker.daemon_status(SID) == (session_marker.DAEMON_LIVE, None)
    assert not session_marker.agent_writes_freely(SID)


def test_a_released_lease_reads_degraded_with_its_reason(writer):
    session_marker.set_session_state(SID, session_marker.STATE_DAEMON)
    for reason in (writer.REASON_UNAUTHORIZED, writer.REASON_BUDGET, writer.REASON_GATEWAY, writer.REASON_STOPPED):
        writer.release(SID, reason)
        assert session_marker.daemon_status(SID) == (session_marker.DAEMON_DEGRADED, reason)
        assert session_marker.agent_writes_freely(SID)


def test_an_expired_lease_reads_degraded(writer):
    session_marker.set_session_state(SID, session_marker.STATE_DAEMON)
    writer.renew(SID, now=time.time() - 1000, ttl=10)
    assert session_marker.daemon_status(SID) == (session_marker.DAEMON_DEGRADED, "expired")


def test_the_worker_reads_the_state_the_cli_writes(writer):
    for state in session_marker.STATES:
        session_marker.set_session_state(SID, state)
        assert writer.session_state(SID) == state


def test_the_written_bytes_match_the_documented_shape(writer):
    writer.renew(SID, now=100.0, ttl=60)
    data = json.loads(session_marker.lease_path(SID).read_text())
    assert set(data) == {"v", "writer", "pid", "expires_at", "renewed_at", "reason"}
    assert session_marker.read_lease(SID) == data


def test_the_tap_tells_its_workers_it_follows_inline():
    """Tap 0.9.12 sets it on every worker it spawns; the worker reads the same
    name to choose a plain exit over EXIT_DO_NOT_RESPAWN when inline starts."""
    from probe.daemon import worker

    # The name both sides read; the tap's own tests prove every spawn carries it.
    source = (TAP / "companion_supervisor.py").read_text()
    assert f'FOLLOWS_INLINE_ENV = "{worker.SUPERVISOR_FOLLOWS_INLINE_ENV}"' in source

def test_the_tap_and_the_worker_agree_on_the_missing_libraries_retry():
    """Tap 0.9.19 retries after EXIT_RETRY_LIBS and says so with the env name the
    worker reads; a worker that sends 6 to a tap that treats it as a crash, or a
    tap that never tells it, would undo the fix."""
    from probe.daemon import worker

    source = (TAP / "companion_supervisor.py").read_text()
    assert f'RETRIES_LIBS_ENV = "{worker.SUPERVISOR_RETRIES_LIBS_ENV}"' in source
    assert f"EXIT_RETRY_LIBS = {worker.EXIT_RETRY_LIBS}" in source
