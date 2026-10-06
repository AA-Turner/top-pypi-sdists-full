"""The agent takes Probe over from the daemon (Richard 2026-10-05).

    "within the daemon mode, the agent should be able to switch to on if the user
    has set it to not off (read or on) for daemon mode, the agent should be able
    to switch to inline and start reading and writing inline and then return
    control to the daemon eventually"

`probe session inline` from `on (daemon)` or `read only (daemon)`, never `off`;
`probe session daemon` hands back to the state it was taken from; any move of the
researcher's switch ends it. Stored as `full` plus the `<sid>.inline` marker, so a
`full` without one opens nothing. The daemon's side (which events are the
agent's) is in test_daemon_loop.py.
"""

from __future__ import annotations

import importlib.util
import io
import json
import sys
import threading
import time
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
def daemon_session():
    """A session the lean plugin started, at `on (daemon)`."""
    session_marker.mark_session_profile(SID, session_marker.RECORDER_DAEMON)
    session_marker.set_session_state(SID, session_marker.STATE_DAEMON)


@pytest.fixture
def guard(monkeypatch, daemon_session):
    monkeypatch.setenv("PROBE_PLUGIN_PROFILE", "daemon")
    return _load("_guard_inline", HOOKS / "tracking_guard.py")


def _run(guard, monkeypatch, capsys, payload) -> str:
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
    guard.main()
    return capsys.readouterr().out


def _pre(command: str = "", *, tool: str = "Bash", tool_input: dict | None = None) -> dict:
    return {"hook_event_name": "PreToolUse", "session_id": SID, "tool_name": tool,
            "tool_input": tool_input if tool_input is not None else {"command": command}}


def _prompt(text: str) -> dict:
    return {"hook_event_name": "UserPromptSubmit", "session_id": SID, "prompt": text}


def _denied(out: str) -> bool:
    return bool(out) and json.loads(out)["hookSpecificOutput"]["permissionDecision"] == "deny"


# ---------------------------------------------------------------------------
# The switch: in from on and read, never from off; back to where it came from.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("start", [session_marker.STATE_DAEMON, session_marker.STATE_READ_ONLY])
def test_the_agent_takes_over_from_on_or_read_and_hands_back_to_the_same(daemon_session, start):
    session_marker.set_session_state(SID, start)
    assert session_marker.enter_inline(SID, now=100.0) is None
    assert session_marker.session_state(SID) == session_marker.STATE_FULL
    assert session_marker.is_inline(SID) and session_marker.inline_from(SID) == start
    assert session_marker.enter_inline(SID) is None, "already inline: unchanged"
    assert session_marker.inline_from(SID) == start

    assert session_marker.leave_inline(SID, now=200.0) == (start, None)
    assert session_marker.session_state(SID) == start, "never `on (daemon)` from read"
    assert not session_marker.is_inline(SID)
    assert session_marker.inline_intervals(SID) == [(100.0, 200.0)]


def test_off_is_the_researchers_alone(daemon_session):
    session_marker.set_session_state(SID, session_marker.STATE_OFF)
    assert session_marker.enter_inline(SID) == session_marker.INLINE_REFUSED_OFF
    assert session_marker.session_state(SID) == session_marker.STATE_OFF
    assert not session_marker.inline_path(SID).exists(), "nothing written"


def test_a_marker_or_log_with_impossible_times_claims_nothing(daemon_session):
    """A marker or log line is data the daemon trusts to skip events: a
    non-finite or inverted time must not hand every event to nobody (review:
    security)."""
    session_marker.set_session_state(SID, session_marker.STATE_FULL)
    for bad in ('{"from": "daemon", "since": Infinity}', '{"from": "daemon", "since": "1.0"}',
                '{"from": "daemon", "since": true}', '{"from": "daemon"}'):
        session_marker.inline_path(SID).write_text(bad)
        assert not session_marker.is_inline(SID), bad
    session_marker.inline_log_path(SID).write_text(
        '{"since": -Infinity, "until": Infinity, "from": "daemon"}\n'
        '{"since": 5, "until": 1, "from": "daemon"}\n'
        'not json\n'
        '{"since": 1, "until": 2, "from": "daemon"}\n')
    assert session_marker.inline_intervals(SID) == [(1.0, 2.0)]


def test_a_hand_back_that_cannot_be_logged_keeps_the_takeover(daemon_session, monkeypatch):
    """The log is the daemon's only record of the stretch once the marker goes:
    a hand-back that cannot write it stays inline and says so (review: Codex)."""
    assert session_marker.enter_inline(SID) is None
    monkeypatch.setattr(session_marker, "_log_inline_interval", lambda *a, **k: False)
    assert session_marker.leave_inline(SID) == (None, session_marker.INLINE_LOG_FAILED)
    assert session_marker.is_inline(SID)


def test_a_researcher_switch_waits_for_a_takeover_in_flight_then_wins(daemon_session):
    """`/probe off` made while a takeover holds the lock lands after it, so the
    takeover can never overwrite it (review of the fixes: a bounded wait let a
    paused takeover write `full` over a landed `off`)."""
    done: list = []
    started = threading.Event()

    def researcher_moves() -> None:
        started.set()
        done.append(session_marker.set_session_state(SID, session_marker.STATE_OFF))

    with session_marker._StateLock(SID):
        researcher = threading.Thread(target=researcher_moves)
        researcher.start()
        assert started.wait(5)
        # Held past any timeout a fallback might use (an earlier fix wrote
        # unlocked after 1 s, and this takeover then overwrote the `off`).
        time.sleep(1.5)
        assert researcher.is_alive(), "the researcher's move waits for the lock"
        session_marker._publish_atomically(
            session_marker.inline_path(SID), json.dumps({"from": "daemon", "since": time.time()}) + "\n")
        session_marker._set_state_unlocked(SID, session_marker.STATE_FULL)
    researcher.join(5)
    assert done == [True]
    assert session_marker.session_state(SID) == session_marker.STATE_OFF
    assert not session_marker.inline_path(SID).exists()


def test_a_row_torn_by_a_short_write_does_not_swallow_the_next(daemon_session):
    """Each logged interval starts on a fresh line (review of the fixes)."""
    session_marker.inline_log_path(SID).write_text('{"since": 1, "unt')
    assert session_marker.enter_inline(SID, now=10.0) is None
    assert session_marker.leave_inline(SID, now=20.0) == (session_marker.STATE_DAEMON, None)
    assert session_marker.inline_intervals(SID) == [(10.0, 20.0)]


def test_handing_back_after_the_researcher_turned_probe_off_changes_nothing(daemon_session):
    """CRITICAL (review, Codex): a hand-back with no live takeover must never
    restore anything, or the agent could undo the researcher's `off`."""
    assert session_marker.enter_inline(SID) is None
    assert session_marker.set_session_state(SID, session_marker.STATE_OFF)
    assert not session_marker.inline_path(SID).exists()
    assert session_marker.leave_inline(SID) == (None, None)
    assert session_marker.session_state(SID) == session_marker.STATE_OFF


def test_outside_the_daemon_profile_there_is_nothing_to_take_over():
    session_marker.set_session_state(SID, session_marker.STATE_FULL)
    assert session_marker.enter_inline(SID) == session_marker.INLINE_REFUSED_PROFILE
    assert not session_marker.inline_path(SID).exists()


def test_a_full_without_the_marker_is_not_inline(daemon_session):
    """An older CLI's `probe session track` stored `full` here: that must not
    open the CLI to the agent."""
    session_marker.set_session_state(SID, session_marker.STATE_FULL)
    assert not session_marker.is_inline(SID)
    assert session_marker.inline_intervals(SID) == []


def test_any_switch_move_ends_inline_and_closes_the_interval(daemon_session):
    assert session_marker.enter_inline(SID, now=time.time() - 5) is None
    assert session_marker.set_session_state(SID, session_marker.STATE_READ_ONLY)
    assert not session_marker.inline_path(SID).exists()
    (interval,) = session_marker.inline_intervals(SID)
    assert interval[1] is not None and interval[0] < interval[1]


def test_a_marker_from_a_crashed_entry_claims_no_turns(daemon_session):
    """The marker is written before the state: a crash between them leaves a
    marker beside `daemon`. It is not inline, and clearing it logs nothing."""
    session_marker._publish_atomically(
        session_marker.inline_path(SID), json.dumps({"from": "daemon", "since": 1.0}) + "\n")
    assert not session_marker.is_inline(SID)
    assert session_marker.inline_intervals(SID) == []
    assert session_marker.set_session_state(SID, session_marker.STATE_DAEMON)
    assert not session_marker.inline_path(SID).exists()
    assert session_marker.inline_intervals(SID) == []


def test_a_takeover_racing_the_researchers_off_loses(daemon_session):
    """Entry re-reads the state inside the per-session lock: an `off` written
    while it waits is never overwritten (review, Codex)."""
    result: list = []
    with session_marker._StateLock(SID):
        worker = threading.Thread(target=lambda: result.append(session_marker.enter_inline(SID)))
        worker.start()
        time.sleep(0.2)
        assert worker.is_alive(), "the takeover waits for the lock"
        session_marker._set_state_unlocked(SID, session_marker.STATE_OFF)
    worker.join(5)
    assert result == [session_marker.INLINE_REFUSED_OFF]
    assert session_marker.session_state(SID) == session_marker.STATE_OFF


def test_the_words_a_person_reads(daemon_session):
    assert session_marker.enter_inline(SID) is None
    assert session_marker.state_display(session_marker.STATE_FULL, True, True) == "on (inline)"
    line = session_marker.render(None, configured=True, tracking=True, color=False,
                                 session_state=session_marker.STATE_FULL, daemon=True, inline=True)
    assert "on (inline)" in line


# ---------------------------------------------------------------------------
# The guard (Claude Code, Codex, Kimi Code): open only for a marked session.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("start", [session_marker.STATE_DAEMON, session_marker.STATE_READ_ONLY])
def test_the_guard_lets_the_agent_take_over(guard, monkeypatch, capsys, start):
    session_marker.set_session_state(SID, start)
    assert not _denied(_run(guard, monkeypatch, capsys, _pre("probe session inline")))


@pytest.mark.parametrize("start", [session_marker.STATE_DAEMON, session_marker.STATE_READ_ONLY])
def test_a_takeover_does_not_open_the_rest_of_its_line(guard, monkeypatch, capsys, start):
    """The guard checks a line before any of it runs, so a takeover chained with
    a write cannot vouch for it: it may fail, target another session, or never
    run (`false && ...`). The refusal says to run the takeover first (review:
    security, testing, red team)."""
    session_marker.set_session_state(SID, start)
    for line in ("probe session inline && probe project create my-sweep",
                 "false && probe session inline; probe run list",
                 "probe session inline --session 99999999-0000-0000-0000-000000000000; probe run list"):
        out = _run(guard, monkeypatch, capsys, _pre(line))
        assert _denied(out), line
        assert "`probe session inline` first" in json.loads(out)["hookSpecificOutput"]["permissionDecisionReason"]


def test_handing_back_is_never_refused(guard, monkeypatch, capsys):
    """`probe session daemon` writes nothing outside a takeover, so an agent told
    to hand back after the researcher already ended it hears `not inline`, not a
    refusal telling it to take Probe over (review: red team)."""
    assert not _denied(_run(guard, monkeypatch, capsys, _pre("probe session daemon")))


@pytest.mark.parametrize("command", ["probe session toggle; probe session inline", "probe session state read",
                                     "probe session track", "probe session default on"])
def test_under_off_the_agent_cannot_walk_out_of_the_opt_out(guard, monkeypatch, capsys, command):
    """CRITICAL (review, security): under `off`, `probe session toggle` moved the
    switch to read only, from where `probe session inline` gave the agent the
    whole CLI. The switch is the researcher's: refused before it runs."""
    session_marker.set_session_state(SID, session_marker.STATE_OFF)
    assert _denied(_run(guard, monkeypatch, capsys, _pre(command))), command
    assert session_marker.session_state(SID) == session_marker.STATE_OFF


def test_while_inline_only_the_researchers_switch_is_refused(guard, monkeypatch, capsys):
    assert _denied(_run(guard, monkeypatch, capsys, _pre("probe project create my-sweep")))
    assert session_marker.enter_inline(SID) is None
    for command in ("probe project create my-sweep", "probe run list", "probe search 'lr sweep'",
                    "probe notes push --file n.md", "probe session daemon", "probe session status"):
        assert not _denied(_run(guard, monkeypatch, capsys, _pre(command))), command
    assert not _denied(_run(guard, monkeypatch, capsys, _pre(tool="mcp__probe-research__search", tool_input={})))
    for command in ("probe session state on", "probe session default on --folder .", "probe session toggle",
                    "probe run list; probe session untrack"):
        out = _run(guard, monkeypatch, capsys, _pre(command))
        assert _denied(out), command
        assert "`probe session daemon`" in json.loads(out)["hookSpecificOutput"]["permissionDecisionReason"]
    assert session_marker.is_inline(SID)


def test_while_inline_the_question_folder_stays_the_researchers(guard, monkeypatch, capsys, tmp_path):
    assert session_marker.enter_inline(SID) is None
    answers = tmp_path / "state" / "probe" / "approvals" / "answers" / "x.json"
    out = _run(guard, monkeypatch, capsys, _pre(tool="Write", tool_input={"file_path": str(answers)}))
    assert _denied(out)


def test_a_full_without_the_marker_stays_closed(guard, monkeypatch, capsys):
    session_marker.set_session_state(SID, session_marker.STATE_FULL)
    out = _run(guard, monkeypatch, capsys, _pre("probe project create my-sweep"))
    assert _denied(out)
    assert "`probe session inline`" in json.loads(out)["hookSpecificOutput"]["permissionDecisionReason"]


def test_the_researchers_switch_ends_inline(guard, monkeypatch, capsys):
    assert session_marker.enter_inline(SID) is None
    _run(guard, monkeypatch, capsys, _prompt("/probe on"))
    assert session_marker.session_state(SID) == session_marker.STATE_DAEMON
    assert not session_marker.is_inline(SID)
    assert _denied(_run(guard, monkeypatch, capsys, _pre("probe project create my-sweep")))


# ---------------------------------------------------------------------------
# The CLI.
# ---------------------------------------------------------------------------


def test_probe_session_inline_says_how_to_hand_back_and_carries_the_skills(daemon_session, capsys):
    assert cli.main(["session", "inline"]) in (0, None)
    out = capsys.readouterr().out
    assert out.startswith("Probe is `on (inline)` for this conversation")
    assert "`probe session daemon` hands control back" in out
    assert "This session has no Probe MCP tools" in out
    assert "# Skill: track-work" in out and "# Skill: edit-notes" in out
    assert session_marker.is_inline(SID)


def test_probe_session_inline_under_off_is_refused_with_nothing_written(daemon_session, capsys):
    session_marker.set_session_state(SID, session_marker.STATE_OFF)
    assert cli.main(["session", "inline"]) == 2
    assert session_marker.INLINE_REFUSED_OFF in capsys.readouterr().err
    assert session_marker.session_state(SID) == session_marker.STATE_OFF


def test_probe_session_daemon_hands_back(daemon_session, capsys):
    session_marker.set_session_state(SID, session_marker.STATE_READ_ONLY)
    assert cli.main(["session", "inline"]) in (0, None)
    capsys.readouterr()
    assert cli.main(["session", "status"]) in (0, None)
    assert json.loads(capsys.readouterr().out)["label"] == "on (inline)"
    assert cli.main(["session", "daemon"]) in (0, None)
    assert "`read only (daemon)`" in capsys.readouterr().out
    assert session_marker.session_state(SID) == session_marker.STATE_READ_ONLY

    assert cli.main(["session", "daemon"]) in (0, None)
    assert session_marker.NOT_INLINE in capsys.readouterr().out
    assert session_marker.session_state(SID) == session_marker.STATE_READ_ONLY


def test_probe_session_daemon_hands_back_to_on_daemon_and_says_if_it_is_down(daemon_session, capsys):
    assert cli.main(["session", "inline"]) in (0, None)
    capsys.readouterr()
    assert cli.main(["session", "daemon"]) in (0, None)
    out = capsys.readouterr().out
    # No worker holds a lease in a test: the agent is told the daemon is not
    # running rather than that it records again (review: red team).
    assert "`on (daemon)`" in out and "but the daemon is not running" in out
    assert session_marker.session_state(SID) == session_marker.STATE_DAEMON
    assert not session_marker.is_inline(SID)


@pytest.mark.parametrize("verb", ["inline", "daemon"])
def test_another_conversation_cannot_be_taken_over(daemon_session, capsys, verb):
    """From inside an agent, `--session` naming another conversation is refused:
    that session's agent was never told it holds Probe (review: security)."""
    other = "22222222-3333-4444-5555-666666666666"
    session_marker.mark_session_profile(other, session_marker.RECORDER_DAEMON)
    session_marker.set_session_state(other, session_marker.STATE_DAEMON)
    assert cli.main(["session", verb, "--session", other]) == 2
    assert "acts only on this conversation" in capsys.readouterr().err
    assert session_marker.session_state(other) == session_marker.STATE_DAEMON


def test_the_skills_missing_from_an_install_are_named(daemon_session, capsys, monkeypatch):
    from probe.daemon import bite

    monkeypatch.setattr(bite, "skills_root", lambda: None)
    assert cli.main(["session", "inline"]) in (0, None)
    assert "These skills were not found in this install: track-work, edit-notes." in capsys.readouterr().out
    assert session_marker.is_inline(SID)


def test_the_status_line_says_on_inline(daemon_session, monkeypatch, tmp_path):
    """The wiring, not just `render` (review: testing)."""
    statusline = _load("_statusline_inline", HOOKS / "statusline.py")
    monkeypatch.setattr(statusline, "_load", lambda _name: session_marker)
    monkeypatch.setenv("PROBE_TOKEN", "configured")
    assert session_marker.enter_inline(SID) is None
    assert "on (inline)" in statusline.segment({"session_id": SID, "cwd": str(tmp_path)})


def test_pis_session_initialize_leaves_an_inline_session_inline(capsys, monkeypatch, tmp_path):
    """pi runs `session initialize` on every start, resume and reload, and heals
    an `on` session to its profile: an inline one must not be handed back."""
    monkeypatch.delenv("CLAUDE_CODE_SESSION_ID", raising=False)
    monkeypatch.setenv("PI_SESSION_ID", SID)
    session_marker.write_recorder("pi", session_marker.RECORDER_DAEMON)
    session_marker.mark_session_profile(SID, session_marker.RECORDER_DAEMON)
    session_marker.set_session_state(SID, session_marker.STATE_DAEMON)
    assert session_marker.enter_inline(SID) is None
    assert cli.main(["session", "initialize", "--cwd", str(tmp_path)]) in (0, None)
    capsys.readouterr()
    assert session_marker.session_state(SID) == session_marker.STATE_FULL
    assert session_marker.is_inline(SID)
