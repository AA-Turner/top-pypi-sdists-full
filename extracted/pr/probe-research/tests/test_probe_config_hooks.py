"""`.probe.config` in the plugin hooks: the parent question (held first call,
the daemon session's first message, a typed `/probe on`), the session-start
line, and the status-line segment.

The hooks load the vendored `_session_marker` / `_probe_config` copies, exactly
as the dispatcher does (hooks dir first on sys.path)."""

from __future__ import annotations

import importlib.util
import io
import json
import sys
from pathlib import Path

import pytest

PLUGIN = Path(__file__).resolve().parents[1] / "plugins" / "probe-research"
HOOKS = PLUGIN / "hooks"
SID = "aaaaaaaa-bbbb-cccc-dddd-ffffffffffff"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(path.parent))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.remove(str(path.parent))
    return module


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    for name in ("PROBE_CONFIG_PATH", "PROBE_SESSION_TRACKING", "PROBE_SESSION_STATE", "PROBE_PLUGIN_PROFILE",
                 "PROBE_HOOK_QUIET", "CODEX_THREAD_ID", "KIMI_SESSION_ID", "PI_SESSION_ID"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", SID)
    sys.modules.pop("_session_marker", None)
    sys.modules.pop("_probe_hooks._probe_config", None)
    code = tmp_path / "home" / "code"
    launch = code / "repo-a"
    launch.mkdir(parents=True)
    (code / ".probe.config").write_text("/*\n")
    return launch


def _marker():
    return _load("_session_marker", HOOKS / "_session_marker.py")


def _guard():
    return _load("_guard_probe_config", HOOKS / "tracking_guard.py")


def _run(guard, monkeypatch, capsys, payload) -> dict:
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
    guard.main()
    out = capsys.readouterr().out
    return json.loads(out) if out.strip() else {}


def _bash(command: str, cwd: Path) -> dict:
    return {"session_id": SID, "hook_event_name": "PreToolUse", "tool_name": "Bash",
            "tool_input": {"command": command}, "cwd": str(cwd)}


def test_first_probe_call_is_held_once_for_the_question(env, monkeypatch, capsys):
    marker = _marker()
    marker.set_session_state(SID, marker.STATE_FULL)
    marker.record_launch_dir(SID, str(env))
    guard = _guard()

    out = _run(guard, monkeypatch, capsys, _bash("probe run list", env))
    reason = out["hookSpecificOutput"]["permissionDecisionReason"]
    assert out["hookSpecificOutput"]["permissionDecision"] == "deny"
    assert reason.startswith("`probe run list` was held back so you ask this first")
    assert "code/.probe.config" in reason and "--directed" in reason

    # Asked: the next call goes through.
    assert _run(guard, monkeypatch, capsys, _bash("probe run list", env)) == {}
    assert marker.parent_question_open(SID)


def test_the_answer_commands_are_never_held(env, monkeypatch, capsys):
    marker = _marker()
    marker.set_session_state(SID, marker.STATE_FULL)
    marker.record_launch_dir(SID, str(env))
    guard = _guard()
    for command in ("probe session parent ignore --directed", "probe ignore check x", "probe session status"):
        assert _run(guard, monkeypatch, capsys, _bash(command, env)) == {}
    assert not marker.parent_question_open(SID)


def test_nothing_is_held_without_a_parent_file_or_under_read(env, monkeypatch, capsys):
    marker = _marker()
    marker.set_session_state(SID, marker.STATE_READ_ONLY)
    marker.record_launch_dir(SID, str(env))
    guard = _guard()
    out = _run(guard, monkeypatch, capsys, _bash("probe run list", env))
    assert "held back" not in json.dumps(out)
    (env.parent / ".probe.config").unlink()
    marker.set_session_state(SID, marker.STATE_FULL)
    assert _run(guard, monkeypatch, capsys, _bash("probe run list", env)) == {}


def test_a_daemon_session_asks_with_its_first_message(env, monkeypatch, capsys):
    monkeypatch.setenv("PROBE_PLUGIN_PROFILE", "daemon")
    marker = _marker()
    marker.mark_session_profile(SID, marker.RECORDER_DAEMON)
    marker.set_session_state(SID, marker.STATE_DAEMON)
    marker.record_launch_dir(SID, str(env))
    guard = _guard()
    payload = {"session_id": SID, "hook_event_name": "UserPromptSubmit", "prompt": "hi", "cwd": str(env)}
    out = _run(guard, monkeypatch, capsys, payload)
    assert "Ask the researcher once" in out["hookSpecificOutput"]["additionalContext"]
    assert _run(guard, monkeypatch, capsys, payload) == {}  # once


def test_typed_probe_on_carries_the_question(env, monkeypatch, capsys):
    marker = _marker()
    marker.set_session_state(SID, marker.STATE_READ_ONLY)
    marker.record_launch_dir(SID, str(env))
    guard = _guard()
    payload = {"session_id": SID, "hook_event_name": "UserPromptSubmit", "prompt": "/probe on", "cwd": str(env)}
    out = _run(guard, monkeypatch, capsys, payload)
    text = out["hookSpecificOutput"]["additionalContext"]
    assert text.startswith("Probe is now ON") and "Ask the researcher once" in text


def test_session_start_line(env, monkeypatch):
    (env / "data").mkdir()
    (env / ".probe.config").write_text("data/\n")
    monkeypatch.setenv("PROBE_SESSION_ID", SID)
    monkeypatch.setenv("PROBE_SESSION_CWD", str(env))
    check = _load("_version_check_probe_config", HOOKS / "version_check.py")
    check._seed_tracking_signal()
    line = check._excluded_context()
    assert line.startswith("`.probe.config` keeps Probe from recording: ")
    assert "this folder (" in line  # the parent's `/*` covers the launch folder
    assert "data/ under " in line
    assert line.endswith("Reads are unaffected.")
    marker = _marker()
    assert marker.probe_config().launch_dir(marker.sessions_dir(), SID) == str(env)


def test_status_line_shows_the_open_question(env, monkeypatch):
    marker = _marker()
    marker.set_session_state(SID, marker.STATE_FULL)
    marker.record_launch_dir(SID, str(env))
    pc = marker.probe_config()
    status, parents = marker.parent_config_status(SID)
    pc.mark_asked(marker.sessions_dir(), SID, parents)
    assert marker.parent_question_open(SID)
    pc.record_answer(marker.sessions_dir(), SID, pc.FOLLOW)
    assert not marker.parent_question_open(SID)


def test_vendored_matcher_loads_by_explicit_path(env, tmp_path, monkeypatch):
    """A `_probe_config.py` on sys.path (the user's project) is never what loads."""
    rogue = tmp_path / "rogue"
    rogue.mkdir()
    (rogue / "_probe_config.py").write_text("raise SystemExit('rogue module imported')\n")
    monkeypatch.syspath_prepend(str(rogue))
    marker = _marker()
    assert marker.probe_config().__file__.endswith("hooks/_probe_config.py")
