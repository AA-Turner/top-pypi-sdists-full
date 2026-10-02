"""The daemon is a wizard setting, not a switch position (Richard 2026-09-29).

    "the /probe command should not be able to switch to the daemon - the daemon
    should only be swappable through the wizard - and, in that daemon state, the
    states should say on (daemon), read only (daemon), and off"

Two settings: "Who records" (the wizard, `defaults.recorders` + the lean plugin's
`<sid>.profile` mark) and the switch (on / read / off). `on` where the daemon
records is STORED as `daemon`; a typed `daemon` moves nothing anywhere.
"""

from __future__ import annotations

import importlib.util
import io
import json
import os
import sys
from pathlib import Path

import pytest

from probe import cli
from probe.sdk import session_marker

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
    monkeypatch.delenv("PROBE_CONFIG_PATH", raising=False)
    monkeypatch.delenv("PROBE_SESSION_STATE", raising=False)
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)
    monkeypatch.delenv("PROBE_PLUGIN_PROFILE", raising=False)
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", SID)
    monkeypatch.delenv("CODEX_THREAD_ID", raising=False)
    monkeypatch.delenv("PI_SESSION_ID", raising=False)


@pytest.fixture
def guard():
    return _load("_guard_wizard_daemon", HOOKS / "tracking_guard.py")


@pytest.fixture
def daemon_session():
    """A session the lean plugin started: the daemon records and reads for it."""
    session_marker.mark_session_profile(SID, session_marker.RECORDER_DAEMON)


def _run(guard, monkeypatch, capsys, payload) -> str:
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
    guard.main()
    return capsys.readouterr().out


def _prompt(text: str) -> dict:
    return {"hook_event_name": "UserPromptSubmit", "session_id": SID, "prompt": text}


def _context(out: str) -> str:
    return json.loads(out)["hookSpecificOutput"]["additionalContext"]


# ---------------------------------------------------------------------------
# The words.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("state", "daemon", "shown"),
    [
        (session_marker.STATE_FULL, False, "on"),
        (session_marker.STATE_READ_ONLY, False, "read"),
        (session_marker.STATE_OFF, False, "off"),
        (session_marker.STATE_DAEMON, True, "on (daemon)"),
        (session_marker.STATE_READ_ONLY, True, "read only (daemon)"),
        (session_marker.STATE_OFF, True, "off"),
        # A stored `daemon` is `on (daemon)` wherever it is read.
        (session_marker.STATE_DAEMON, False, "on (daemon)"),
    ],
)
def test_what_a_person_reads_for_each_state(state, daemon, shown):
    assert session_marker.state_display(state, daemon) == shown


def test_the_switch_offers_three_words_and_json_keeps_daemon():
    assert session_marker.STATE_WORDS == ("on", "read", "off")
    # pi's parseState and older hooks read the JSON word: it stays `daemon`.
    assert session_marker.state_label(session_marker.STATE_DAEMON) == "daemon"


def test_on_is_stored_by_who_records(monkeypatch):
    assert session_marker.on_state(SID) == session_marker.STATE_FULL
    assert session_marker.switch_target(SID, session_marker.STATE_FULL) == session_marker.STATE_FULL
    session_marker.mark_session_profile(SID, session_marker.RECORDER_DAEMON)
    assert session_marker.on_state(SID) == session_marker.STATE_DAEMON
    assert session_marker.switch_target(SID, session_marker.STATE_FULL) == session_marker.STATE_DAEMON
    for kept in (session_marker.STATE_READ_ONLY, session_marker.STATE_OFF):
        assert session_marker.switch_target(SID, kept) == kept
    assert session_marker.switch_target(SID, session_marker.STATE_DAEMON) is None, "daemon BY NAME is refused"


def test_without_a_mark_the_machines_setting_for_the_agent_decides():
    other = "22222222-3333-4444-5555-666666666666"
    assert session_marker.on_state(other, "claude_code") == session_marker.STATE_FULL
    session_marker.write_recorder("claude_code", session_marker.RECORDER_DAEMON)
    assert session_marker.on_state(other, "claude_code") == session_marker.STATE_DAEMON
    assert session_marker.on_state(other, "codex") == session_marker.STATE_FULL
    assert session_marker.on_state(other) == session_marker.STATE_FULL, "no agent named: the mark alone decides"


# ---------------------------------------------------------------------------
# /probe: the agent plugin.
# ---------------------------------------------------------------------------


def test_a_typed_probe_daemon_moves_nothing_and_says_where_the_daemon_is_set(guard, monkeypatch, capsys):
    session_marker.set_session_state(SID, session_marker.STATE_FULL)
    out = _run(guard, monkeypatch, capsys, _prompt("/probe daemon"))
    assert session_marker.session_state(SID) == session_marker.STATE_FULL
    assert _context(out) == session_marker.DAEMON_SWITCH_REFUSAL
    assert "probe wizard" in session_marker.DAEMON_SWITCH_REFUSAL


def test_a_skill_call_with_daemon_moves_nothing_either(guard, monkeypatch, capsys):
    session_marker.set_session_state(SID, session_marker.STATE_READ_ONLY)
    payload = {"hook_event_name": "PostToolUse", "session_id": SID, "tool_name": "Skill",
               "tool_input": {"skill": "probe-research:probe", "args": "daemon"}}
    out = _run(guard, monkeypatch, capsys, payload)
    assert session_marker.session_state(SID) == session_marker.STATE_READ_ONLY
    assert _context(out) == session_marker.DAEMON_SWITCH_REFUSAL


def test_on_in_the_agent_profile_is_full(guard, monkeypatch, capsys):
    session_marker.set_session_state(SID, session_marker.STATE_READ_ONLY)
    _run(guard, monkeypatch, capsys, _prompt("/probe on"))
    assert session_marker.session_state(SID) == session_marker.STATE_FULL


def test_a_stored_daemon_in_the_agent_profile_leaves_and_cannot_come_back(guard, monkeypatch, capsys):
    """A session flipped to `daemon` before this change keeps it until the switch moves."""
    session_marker.set_session_state(SID, session_marker.STATE_DAEMON)
    _run(guard, monkeypatch, capsys, _prompt("/probe"))
    assert session_marker.session_state(SID) == session_marker.STATE_READ_ONLY
    _run(guard, monkeypatch, capsys, _prompt("/probe"))
    assert session_marker.session_state(SID) == session_marker.STATE_FULL


# ---------------------------------------------------------------------------
# /probe: the lean plugin (daemon profile) gets on / read / off.
# ---------------------------------------------------------------------------


@pytest.fixture
def lean(monkeypatch, daemon_session):
    monkeypatch.setenv("PROBE_PLUGIN_PROFILE", "daemon")


def test_the_lean_plugins_switch_moves_between_the_daemon_words(guard, lean, monkeypatch, capsys):
    session_marker.set_session_state(SID, session_marker.STATE_DAEMON)
    out = _run(guard, monkeypatch, capsys, _prompt("/probe read"))
    assert session_marker.session_state(SID) == session_marker.STATE_READ_ONLY
    assert "`read only (daemon)`" in _context(out)

    out = _run(guard, monkeypatch, capsys, _prompt("/probe on"))
    assert session_marker.session_state(SID) == session_marker.STATE_DAEMON, "on is stored as daemon here"
    assert "`on (daemon)`" in _context(out)

    out = _run(guard, monkeypatch, capsys, _prompt("/probe off"))
    assert session_marker.session_state(SID) == session_marker.STATE_OFF
    assert "OFF" in _context(out)

    _run(guard, monkeypatch, capsys, _prompt("/probe"))  # off -> read
    _run(guard, monkeypatch, capsys, _prompt("/probe"))  # read -> on
    assert session_marker.session_state(SID) == session_marker.STATE_DAEMON


def test_the_lean_plugin_refuses_daemon_by_name_too(guard, lean, monkeypatch, capsys):
    session_marker.set_session_state(SID, session_marker.STATE_READ_ONLY)
    out = _run(guard, monkeypatch, capsys, _prompt("/probe daemon"))
    assert session_marker.session_state(SID) == session_marker.STATE_READ_ONLY
    assert _context(out) == session_marker.DAEMON_SWITCH_REFUSAL


def test_the_lean_plugin_writes_a_missing_mark_so_on_is_daemon(guard, monkeypatch, capsys):
    """The mark is best-effort at SessionStart; without it `on` would store `full`
    in a session whose agent cannot record (review of #2172)."""
    monkeypatch.setenv("PROBE_PLUGIN_PROFILE", "daemon")
    session_marker.set_session_state(SID, session_marker.STATE_READ_ONLY)
    _run(guard, monkeypatch, capsys, _prompt("/probe on"))
    assert session_marker.session_profile(SID) == session_marker.RECORDER_DAEMON
    assert session_marker.session_state(SID) == session_marker.STATE_DAEMON


def test_the_lean_plugin_says_nothing_on_an_ordinary_prompt(guard, lean, monkeypatch, capsys):
    session_marker.set_session_state(SID, session_marker.STATE_DAEMON)
    assert _run(guard, monkeypatch, capsys, _prompt("carry on")) == ""


def _pre_bash(command: str) -> dict:
    return {"hook_event_name": "PreToolUse", "session_id": SID, "tool_name": "Bash",
            "tool_input": {"command": command}}


def _denied(out: str) -> bool:
    return bool(out) and json.loads(out)["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_read_only_daemon_keeps_asks_and_exec_but_refuses_run_data(guard, lean, monkeypatch, capsys):
    session_marker.set_session_state(SID, session_marker.STATE_READ_ONLY)
    assert not _denied(_run(guard, monkeypatch, capsys, _pre_bash('probe ask "what lr did we use?"')))
    assert not _denied(_run(guard, monkeypatch, capsys, _pre_bash("probe exec -- python train.py")))
    assert _denied(_run(guard, monkeypatch, capsys, _pre_bash("probe run start --name x")))
    session_marker.set_session_state(SID, session_marker.STATE_DAEMON)
    assert not _denied(_run(guard, monkeypatch, capsys, _pre_bash("probe run start --name x")))


# ---------------------------------------------------------------------------
# The CLI.
# ---------------------------------------------------------------------------


def test_session_state_daemon_is_refused_with_nothing_written(capsys):
    session_marker.set_session_state(SID, session_marker.STATE_READ_ONLY)
    assert cli.main(["session", "state", "daemon"]) == 2
    assert session_marker.DAEMON_SWITCH_REFUSAL in capsys.readouterr().err
    assert session_marker.session_state(SID) == session_marker.STATE_READ_ONLY


def test_session_state_on_follows_who_records(capsys, daemon_session):
    session_marker.set_session_state(SID, session_marker.STATE_READ_ONLY)
    assert cli.main(["session", "state", "on"]) in (0, None)
    out = json.loads(capsys.readouterr().out)
    assert session_marker.session_state(SID) == session_marker.STATE_DAEMON
    assert (out["state"], out["label"]) == ("daemon", "on (daemon)")

    assert cli.main(["session", "state", "read"]) in (0, None)
    out = json.loads(capsys.readouterr().out)
    assert (out["state"], out["label"]) == ("read", "read only (daemon)")


def test_session_toggle_follows_who_records(capsys, daemon_session):
    session_marker.set_session_state(SID, session_marker.STATE_READ_ONLY)
    assert cli.main(["session", "toggle"]) in (0, None)
    assert json.loads(capsys.readouterr().out)["label"] == "on (daemon)"
    assert session_marker.session_state(SID) == session_marker.STATE_DAEMON


def test_pis_session_initialize_seeds_a_daemon_default_as_on(capsys, monkeypatch, tmp_path):
    """pi seeds through `probe session initialize`: the same rule as the hook
    (review of #2172), so an old `daemon` default does not start the daemon."""
    monkeypatch.delenv("CLAUDE_CODE_SESSION_ID", raising=False)
    monkeypatch.setenv("PI_SESSION_ID", SID)
    session_marker.write_default_state(session_marker.STATE_DAEMON)
    assert cli.main(["session", "initialize", "--cwd", str(tmp_path)]) in (0, None)
    capsys.readouterr()
    assert session_marker.session_state(SID) == session_marker.STATE_FULL


def test_session_default_daemon_is_refused(capsys, tmp_path):
    assert cli.main(["session", "default", "daemon"]) == 2
    assert session_marker.DAEMON_SWITCH_REFUSAL in capsys.readouterr().err
    folder = tmp_path / "repo"
    folder.mkdir()
    assert cli.main(["session", "default", "daemon", "--folder", str(folder)]) == 2
    assert not session_marker.folder_config_path(folder).exists()


# ---------------------------------------------------------------------------
# The wizard: two settings.
# ---------------------------------------------------------------------------


def test_the_new_session_default_row_is_on_read_off():
    from probe.cli import setup as wizard

    assert wizard.cycling_settings()[wizard.Setting.TRACKING_DEFAULT] == ("full", "read-only", "off")
    assert set(wizard.SETTINGS_STATE_COPY[wizard.Setting.TRACKING_DEFAULT]) == {"full", "read-only", "off"}
    assert not hasattr(wizard, "daemon_gated_order")


def test_a_stored_daemon_default_reads_as_on_on_the_row():
    from probe.cli import setup as wizard

    session_marker.write_default_state(session_marker.STATE_DAEMON)
    assert wizard.setting_state(session_marker.default_session_state()) == session_marker.STATE_FULL
    assert wizard.read_settings()[wizard.Setting.TRACKING_DEFAULT] == session_marker.STATE_FULL


# ---------------------------------------------------------------------------
# Session start: a stored `daemon` default follows who records.
# ---------------------------------------------------------------------------


@pytest.fixture
def start_hook(monkeypatch):
    module = _load("_start_wizard_daemon", HOOKS / "version_check.py")
    monkeypatch.setenv(module.SESSION_ID_ENV, SID)
    return module


def test_a_stored_daemon_default_starts_the_agent_profile_on(start_hook):
    session_marker.write_default_state(session_marker.STATE_DAEMON)
    start_hook._seed_tracking_signal()
    assert session_marker.session_state(SID) == session_marker.STATE_FULL


def test_the_daemon_profile_starts_on_as_daemon_and_read_as_read(start_hook, monkeypatch):
    monkeypatch.setenv(start_hook.PROFILE_ENV, start_hook.PROFILE_DAEMON)
    session_marker.write_default_state(session_marker.STATE_FULL)
    start_hook._seed_tracking_signal()
    assert session_marker.session_state(SID) == session_marker.STATE_DAEMON
    other = "33333333-4444-5555-6666-777777777777"
    monkeypatch.setenv(start_hook.SESSION_ID_ENV, other)
    session_marker.write_default_state(session_marker.STATE_READ_ONLY)
    start_hook._seed_tracking_signal()
    assert session_marker.session_state(other) == session_marker.STATE_READ_ONLY


# ---------------------------------------------------------------------------
# The status line.
# ---------------------------------------------------------------------------


def _render(**kwargs) -> str:
    return session_marker.render(None, configured=True, color=False, **kwargs)


def test_the_status_line_says_the_daemon_words():
    assert _render(tracking=True, session_state="daemon", daemon_live=True).endswith("on (daemon)")
    assert _render(tracking=True, session_state="daemon").endswith("on (daemon degraded)")
    assert _render(tracking=False, session_state="read-only", daemon=True).endswith("read only (daemon)")
    assert _render(tracking=False, session_state="read-only").endswith("read-only")
    assert _render(tracking=False, session_state="off", daemon=True).endswith("off")


# ---------------------------------------------------------------------------
# The skills.
# ---------------------------------------------------------------------------


def test_no_probe_skill_offers_a_daemon_position():
    for path in (
        AGENT_ROOT / "skills" / "probe" / "SKILL.md",
        AGENT_ROOT / "plugins" / "probe-research" / "skills" / "probe" / "SKILL.md",
        AGENT_ROOT / "plugins" / "probe-research-pi" / "skills" / "probe" / "SKILL.md",
        AGENT_ROOT / "plugins" / "probe-research-daemon" / "skills" / "probe" / "SKILL.md",
    ):
        text = path.read_text(encoding="utf-8")
        assert "/probe daemon  " not in text and "| `daemon` |" not in text, path


def test_the_lean_plugins_switch_skill_uses_the_daemon_words():
    text = (AGENT_ROOT / "plugins" / "probe-research-daemon" / "skills" / "probe" / "SKILL.md").read_text()
    assert text.startswith("---\nname: probe\n")
    for words in ("on (daemon)", "read only (daemon)", "probe wizard"):
        assert words in text


# ---------------------------------------------------------------------------
# The status line before SessionStart has seeded the session (Richard
# 2026-09-29: a NEW daemon session showed `read-only` until its first prompt).
# Claude Code draws the line once while the hook still runs, and not again
# until the conversation moves.
# ---------------------------------------------------------------------------


def _statusline(tmp_path, sid: str) -> str:
    import subprocess

    payload = json.dumps({"session_id": sid, "cwd": str(tmp_path), "transcript_path": str(tmp_path / f"{sid}.jsonl")})
    env = {**os.environ, "NO_COLOR": "1", "PROBE_TOKEN": "probe_pat_statusline_test"}
    out = subprocess.run([sys.executable, str(HOOKS / "statusline.py")], input=payload, capture_output=True,
                         text=True, env=env, timeout=30)
    return out.stdout.strip()


@pytest.mark.parametrize(
    ("default", "shown"),
    [(session_marker.STATE_READ_ONLY, "read only (daemon)"), (session_marker.STATE_FULL, "on (daemon)")],
)
def test_an_unseeded_session_reads_as_the_daemons_when_claude_code_records_by_it(tmp_path, default, shown):
    from probe.sdk.config import save_context

    sid = "44444444-5555-6666-7777-888888888888"
    save_context({"companion_token": "probe_pat_" + "0" * 32})  # the daemon can start
    session_marker.write_default_state(default)
    session_marker.write_recorder("claude_code", session_marker.RECORDER_DAEMON)
    assert session_marker.session_state(sid) is None and session_marker.session_profile(sid) is None
    assert shown in _statusline(tmp_path, sid)


def test_an_unseeded_session_reads_as_the_agents_when_the_agent_records(tmp_path):
    sid = "44444444-5555-6666-7777-888888888888"
    session_marker.write_default_state(session_marker.STATE_READ_ONLY)
    line = _statusline(tmp_path, sid)
    assert line.endswith("read-only") and "daemon" not in line


def test_a_daemon_that_cannot_start_still_reads_degraded(tmp_path):
    """No key: the worker never takes a lease, so `not-started` is an outage."""
    sid = "44444444-5555-6666-7777-888888888888"
    session_marker.write_default_state(session_marker.STATE_FULL)
    session_marker.write_recorder("claude_code", session_marker.RECORDER_DAEMON)
    assert "on (daemon degraded)" in _statusline(tmp_path, sid)
