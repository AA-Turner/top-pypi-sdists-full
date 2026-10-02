"""The `daemon` state as the Claude Code / Codex hooks carry it.

    session start      -> DAEMON_CONTEXT (and the daemon's compaction line)
    each prompt        -> a notice ONLY when recording changes hands
    after a Bash call  -> MESSAGE_DAEMON when a write slipped past a live lease,
                          and nothing when the CLI itself refused the command
"""

from __future__ import annotations

import importlib.util
import io
import json
import sys
import time
from pathlib import Path

import pytest

AGENT_ROOT = Path(__file__).resolve().parents[1]
HOOKS = AGENT_ROOT / "plugins" / "probe-research" / "hooks"
SID = "11111111-2222-3333-4444-555555555555"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(path.parent))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.remove(str(path.parent))
    return module


@pytest.fixture(autouse=True)
def _env(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "cache"))
    monkeypatch.delenv("PROBE_SESSION_STATE", raising=False)
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)


def _key(tmp_path, present: bool = True) -> None:
    path = tmp_path / "config" / "probe" / "config.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    context = {"companion_token": "k"} if present else {}
    path.write_text(json.dumps({"current_context": "default", "contexts": {"default": context}}))


@pytest.fixture(autouse=True)
def _with_key(tmp_path):
    _key(tmp_path)


@pytest.fixture
def guard():
    return _load("_guard_daemon", HOOKS / "tracking_guard.py")


@pytest.fixture
def marker():
    return _load("_marker_daemon", HOOKS / "_session_marker.py")


def _lease(marker, *, live: bool = True, reason=None) -> None:
    path = marker.lease_path(SID)
    path.parent.mkdir(parents=True, exist_ok=True)
    now = time.time()
    path.write_text(json.dumps({"v": 1, "writer": "daemon", "pid": 1,
                                "expires_at": now + (60 if live else -1), "renewed_at": now,
                                "reason": reason}))


def _run(guard, monkeypatch, capsys, payload) -> str:
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
    guard.main()
    return capsys.readouterr().out


def _prompt(text="carry on"):
    return {"hook_event_name": "UserPromptSubmit", "session_id": SID, "prompt": text}


def _bash(command, response=None):
    return {"hook_event_name": "PostToolUse", "session_id": SID, "tool_name": "Bash",
            "tool_input": {"command": command}, "tool_response": response or {"stdout": "ok", "stderr": ""}}


# ---------------------------------------------------------------------------
# The per-prompt handback notice.
# ---------------------------------------------------------------------------


def test_a_live_daemon_is_announced_by_session_start_not_every_prompt(guard, marker, monkeypatch, capsys):
    marker.set_session_state(SID, marker.STATE_DAEMON)
    _lease(marker)
    assert _run(guard, monkeypatch, capsys, _prompt()) == ""
    assert _run(guard, monkeypatch, capsys, _prompt()) == ""


def test_a_lapsed_lease_hands_recording_back_once_and_a_recovery_takes_it(guard, marker, monkeypatch, capsys):
    marker.set_session_state(SID, marker.STATE_DAEMON)
    _lease(marker)
    _run(guard, monkeypatch, capsys, _prompt())
    _lease(marker, live=False)
    out = _run(guard, monkeypatch, capsys, _prompt())
    assert "the daemon is not responding, so recording is back with you" in out
    assert _run(guard, monkeypatch, capsys, _prompt()) == ""
    _lease(marker)
    assert guard.FLIP_NOTICE["daemon"] in json.loads(_run(guard, monkeypatch, capsys, _prompt()))["hookSpecificOutput"]["additionalContext"]


def test_a_worker_that_never_started_gets_one_prompt_of_grace(guard, marker, monkeypatch, capsys):
    marker.set_session_state(SID, marker.STATE_DAEMON)
    assert _run(guard, monkeypatch, capsys, _prompt()) == ""
    assert "the daemon is not running" in _run(guard, monkeypatch, capsys, _prompt())


def test_no_grace_when_the_daemon_has_no_key(guard, marker, monkeypatch, capsys, tmp_path):
    _key(tmp_path, present=False)
    marker.set_session_state(SID, marker.STATE_DAEMON)
    assert "the daemon is not running" in _run(guard, monkeypatch, capsys, _prompt())


def test_a_released_lease_says_why(guard, marker, monkeypatch, capsys):
    marker.set_session_state(SID, marker.STATE_DAEMON)
    _lease(marker, reason="unauthorized")
    # No grace here: only a worker that has not STARTED yet gets one prompt.
    assert "the daemon is not authorized" in _run(guard, monkeypatch, capsys, _prompt())
    assert _run(guard, monkeypatch, capsys, _prompt()) == ""


def test_other_states_say_nothing(guard, marker, monkeypatch, capsys):
    for state in (marker.STATE_FULL, marker.STATE_READ_ONLY):
        marker.set_session_state(SID, state)
        assert _run(guard, monkeypatch, capsys, _prompt()) == ""


# ---------------------------------------------------------------------------
# The flip. A session that moves to `daemon` mid-conversation never sees the
# session-start text, so the flip itself carries the whole statement of the split.
# ---------------------------------------------------------------------------


def _context(out: str) -> str:
    return json.loads(out)["hookSpecificOutput"]["additionalContext"]


def test_a_typed_daemon_is_refused_not_flipped(guard, marker, monkeypatch, capsys):
    """The daemon is the wizard's "Who records", never a switch position (Richard
    2026-09-29); tests/test_daemon_is_a_wizard_setting.py holds the rest."""
    marker.set_session_state(SID, marker.STATE_FULL)
    out = _run(guard, monkeypatch, capsys, _prompt("/probe daemon"))
    assert marker.session_state(SID) == marker.STATE_FULL
    assert _context(out) == marker.DAEMON_SWITCH_REFUSAL


def test_a_skill_call_with_daemon_is_refused_too(guard, marker, monkeypatch, capsys):
    marker.set_session_state(SID, marker.STATE_FULL)
    payload = {"hook_event_name": "PostToolUse", "session_id": SID, "tool_name": "Skill",
               "tool_input": {"skill": "probe-research:probe", "args": "daemon"}}
    assert _context(_run(guard, monkeypatch, capsys, payload)) == marker.DAEMON_SWITCH_REFUSAL
    assert marker.session_state(SID) == marker.STATE_FULL


def test_session_start_and_the_flip_say_the_same_thing(guard, start_hook):
    assert start_hook.DAEMON_CONTEXT == start_hook._session_marker.DAEMON_CONTEXT
    assert start_hook.DAEMON_CONTEXT in guard.FLIP_NOTICE["daemon"]


# ---------------------------------------------------------------------------
# After the fact.
# ---------------------------------------------------------------------------


def test_a_write_past_a_live_lease_is_named(guard, marker, monkeypatch, capsys):
    marker.set_session_state(SID, marker.STATE_DAEMON)
    _lease(marker)
    out = _run(guard, monkeypatch, capsys, _bash("probe notes push n.md"))
    assert "`probe notes push` just wrote to Probe directly" in out


@pytest.mark.parametrize("command", ["probe notes push n.md --directed", "probe exec -- python t.py", "probe run list"])
def test_directed_launches_and_reads_are_not_bypasses(guard, marker, monkeypatch, capsys, command):
    marker.set_session_state(SID, marker.STATE_DAEMON)
    _lease(marker)
    assert _run(guard, monkeypatch, capsys, _bash(command)) == ""


def test_a_command_the_cli_refused_is_not_reported_as_written(guard, marker, monkeypatch, capsys):
    refused = {"stdout": "", "stderr": marker.DENY_REASON_DAEMON.format(matched="probe notes push")}
    marker.set_session_state(SID, marker.STATE_DAEMON)
    _lease(marker)
    assert _run(guard, monkeypatch, capsys, _bash("probe notes push n.md", refused)) == ""
    marker.set_session_state(SID, marker.STATE_READ_ONLY)
    refused = {"stdout": "", "stderr": marker.DENY_REASON.format(matched="probe notes push")}
    assert _run(guard, monkeypatch, capsys, _bash("probe notes push n.md", refused)) == ""


def test_an_older_clis_shorter_refusal_still_counts(guard, marker, monkeypatch, capsys):
    """A CLI from before subgroups names `probe project code`, where this hook
    matched `probe project code attach`: still a refusal, not a landed write."""
    marker.set_session_state(SID, marker.STATE_DAEMON)
    _lease(marker)
    refused = {"stdout": "", "stderr": marker.DENY_REASON_DAEMON.format(matched="probe project code")}
    assert _run(guard, monkeypatch, capsys, _bash("probe project code attach p1 o/r", refused)) == ""
    # A refusal naming some OTHER command proves nothing about this one.
    other = {"stdout": "", "stderr": marker.DENY_REASON_DAEMON.format(matched="probe project create")}
    assert _run(guard, monkeypatch, capsys, _bash("probe project code attach p1 o/r", other)) != ""


# ---------------------------------------------------------------------------
# Session start.
# ---------------------------------------------------------------------------


@pytest.fixture
def start_hook(monkeypatch):
    monkeypatch.setenv("PROBE_BASE_URL", "http://127.0.0.1:9")
    monkeypatch.delenv("PROBE_HOOK_EVENT", raising=False)
    monkeypatch.setenv("PROBE_SESSION_ID", SID)
    module = _load("_vc_daemon", HOOKS / "version_check.py")
    module._team_note_cli_too_old = lambda _binary: None
    monkeypatch.setattr(module.subprocess, "Popen", lambda *a, **k: None)
    return module


def test_session_start_in_the_daemon_state(start_hook, monkeypatch):
    start_hook._session_marker.set_session_state(SID, start_hook._session_marker.STATE_DAEMON)
    monkeypatch.setenv("PROBE_SESSION_SOURCE", "startup")
    ctx = start_hook._start_context() or ""
    assert start_hook.DAEMON_CONTEXT in ctx
    assert start_hook.TRACKING_OFF_CONTEXT not in ctx


def test_session_start_says_a_keyless_daemon_cannot_record(start_hook, monkeypatch, tmp_path):
    _key(tmp_path, present=False)
    start_hook._session_marker.set_session_state(SID, start_hook._session_marker.STATE_DAEMON)
    monkeypatch.setenv("PROBE_SESSION_SOURCE", "startup")
    ctx = start_hook._start_context() or ""
    assert start_hook.DAEMON_CONTEXT not in ctx
    assert "the daemon is not authorized, so recording is back with you" in ctx


def test_compaction_in_the_daemon_state_swaps_the_reconcile_nudge(start_hook, monkeypatch):
    start_hook._session_marker.set_session_state(SID, start_hook._session_marker.STATE_DAEMON)
    _lease(start_hook._session_marker)
    monkeypatch.setenv("PROBE_SESSION_SOURCE", "compact")
    ctx = start_hook._start_context() or ""
    assert start_hook.COMPACT_CONTEXT_DAEMON in ctx
    assert start_hook.COMPACT_CONTEXT not in ctx


def test_compaction_never_re_announces_a_dead_daemon(start_hook, monkeypatch):
    start_hook._session_marker.set_session_state(SID, start_hook._session_marker.STATE_DAEMON)
    _lease(start_hook._session_marker, live=False)
    monkeypatch.setenv("PROBE_SESSION_SOURCE", "compact")
    ctx = start_hook._start_context() or ""
    assert start_hook.DAEMON_CONTEXT not in ctx
    assert "the daemon is not responding, so recording is back with you" in ctx


def test_the_hook_lets_exec_through_under_read(guard, marker, monkeypatch, capsys):
    marker.set_session_state(SID, marker.STATE_READ_ONLY)
    payload = {"hook_event_name": "PreToolUse", "session_id": SID, "tool_name": "Bash",
               "tool_input": {"command": "probe exec -- python train.py"}}
    assert _run(guard, monkeypatch, capsys, payload) == ""  # the CLI runs it unrecorded
    payload["tool_input"]["command"] = "probe notes push n.md"
    assert "READ-ONLY" in _run(guard, monkeypatch, capsys, payload)


def test_on_is_unchanged(start_hook, monkeypatch):
    start_hook._session_marker.set_session_state(SID, start_hook._session_marker.STATE_FULL)
    monkeypatch.setenv("PROBE_SESSION_SOURCE", "compact")
    ctx = start_hook._start_context() or ""
    assert start_hook.COMPACT_CONTEXT in ctx
    assert start_hook.DAEMON_CONTEXT not in ctx
