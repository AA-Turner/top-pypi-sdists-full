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


def test_the_tap_reads_the_inline_marker_the_cli_writes(writer):
    """`<sid>.inline` is a contract between the CLI (`session_marker.enter_inline`)
    and the tap's supervisor (`companion_lease.inline`): written with one, read
    with the other, so the supervisor keeps the worker exactly while the CLI
    says the agent holds Probe."""
    session_marker.mark_session_profile(SID, session_marker.RECORDER_DAEMON)
    assert set(writer.INLINE_FROM) == set(session_marker.INLINE_FROM)
    assert writer.INLINE_SUFFIX == session_marker.INLINE_SUFFIX
    for start in session_marker.INLINE_FROM:
        session_marker.set_session_state(SID, start)
        assert not writer.inline(SID)
        assert session_marker.enter_inline(SID) is None
        assert writer.inline(SID)
        assert session_marker.leave_inline(SID) == (start, None)
        assert not writer.inline(SID)
    assert session_marker.enter_inline(SID) is None
    session_marker.set_session_state(SID, session_marker.STATE_OFF)
    assert not writer.inline(SID)


def test_the_tap_and_the_cli_refuse_the_same_malformed_markers(writer):
    session_marker.mark_session_profile(SID, session_marker.RECORDER_DAEMON)
    session_marker.set_session_state(SID, session_marker.STATE_FULL)
    for body in ('{"from": "daemon", "since": 1.5}', '{"from": "daemon"}', '{"from": "daemon", "since": "1"}',
                 '{"from": "daemon", "since": true}', '{"from": "off", "since": 1}', "not json"):
        session_marker.inline_path(SID).write_text(body)
        assert writer.inline(SID) == session_marker.is_inline(SID), body
