"""`/probe inline`: the researcher hands Probe to the agent (Richard 2026-10-06).

    "why not create like an inline mode ... that the user must toggle then rather
    than being changed from the daemon states through the will of the agent"
    T1 = A (the agent never changes who records; it asks), T2 = A (from any state,
    typed only, stops the daemon like `off`), T3 = A (track-work as written).

Only the researcher moves it: a typed prompt, pi's `/probe` command, or
`probe session state inline` from a terminal -- never a tool call the agent can
make. Stored as `full` plus the `<sid>.inline` marker, so a `full` without one
opens nothing; any other switch move ends it. The daemon's side (which events
are the agent's, the worker stopping) is in test_daemon_loop.py.
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
from probe.cli import daemon_cli
from probe.daemon import worker as worker_mod
from probe.sdk import session_marker

cli_main = importlib.import_module("probe.cli.main")  # `probe.cli.main` the attribute is the entry function
AGENT_ROOT = Path(__file__).resolve().parents[1]
HOOKS = AGENT_ROOT / "plugins" / "probe-research" / "hooks"
DAEMON_PLUGIN = AGENT_ROOT / "plugins" / "probe-research-daemon"
FIXTURES = Path(__file__).parent / "fixtures" / "daemon_prompts"
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


def _body(name: str) -> str:
    lines = (FIXTURES / name).read_text(encoding="utf-8").split("\n")
    return "\n".join(lines[lines.index("---", 1) + 1:]).rstrip("\n")


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


def _fake_probe(tmp_path: Path, version: str) -> str:
    """A `probe` whose `--version` prints `version` (what the notice's CLI floor reads)."""
    path = tmp_path / f"probe-{version or 'none'}"
    path.write_text(f"#!/bin/sh\necho 'probe {version}'\n")
    path.chmod(0o755)
    return str(path)


@pytest.fixture
def guard(monkeypatch, daemon_session, tmp_path):
    """The lean plugin's copy (what ships beside `inline/`; a byte copy of the
    canonical hook, held equal by test_daemon_plugin.py), as Claude Code runs it,
    beside a CLI with the read bridge."""
    monkeypatch.setenv("PROBE_PLUGIN_PROFILE", "daemon")
    monkeypatch.setenv("PROBE_BIN", _fake_probe(tmp_path, "0.220.0"))
    sys.modules.pop("_probe_hooks.version_check", None)
    monkeypatch.setenv("PROBE_AGENT", "claude_code")
    monkeypatch.delenv("PROBE_HOOK_QUIET", raising=False)
    return _load("_guard_inline", DAEMON_PLUGIN / "hooks" / "tracking_guard.py")


def _run(guard, monkeypatch, capsys, payload) -> str:
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
    guard.main()
    return capsys.readouterr().out


def _pre(command: str = "", *, tool: str = "Bash", tool_input: dict | None = None) -> dict:
    return {"hook_event_name": "PreToolUse", "session_id": SID, "tool_name": tool,
            "tool_input": tool_input if tool_input is not None else {"command": command}}


def _prompt(text: str) -> dict:
    return {"hook_event_name": "UserPromptSubmit", "session_id": SID, "prompt": text}


def _skill_call(args: str) -> dict:
    return {"hook_event_name": "PostToolUse", "session_id": SID, "tool_name": "Skill",
            "tool_input": {"skill": "probe-research-daemon:probe", "args": args}}


def _denied(out: str) -> bool:
    return bool(out) and json.loads(out)["hookSpecificOutput"]["permissionDecision"] == "deny"


def _context(out: str) -> str:
    return json.loads(out)["hookSpecificOutput"]["additionalContext"] if out else ""


# ---------------------------------------------------------------------------
# The switch: from any state, back by any other move.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("start", [session_marker.STATE_DAEMON, session_marker.STATE_READ_ONLY,
                                   session_marker.STATE_OFF])
def test_inline_is_reached_from_any_state_and_any_move_ends_it(daemon_session, start):
    session_marker.set_session_state(SID, start)
    assert session_marker.switch_to_inline(SID, now=100.0)
    assert session_marker.session_state(SID) == session_marker.STATE_FULL
    assert session_marker.is_inline(SID) and session_marker.inline_marker(SID)["from"] == start
    assert session_marker.switch_to_inline(SID, now=150.0), "already inline"
    assert session_marker.inline_marker(SID)["since"] == 100.0, "the stretch keeps its start"

    assert session_marker.set_session_state(SID, session_marker.STATE_DAEMON)
    assert not session_marker.is_inline(SID)
    assert not session_marker.inline_path(SID).exists()
    ((since, until),) = session_marker.inline_intervals(SID)
    assert since == 100.0 and until is not None and until >= since


def test_a_session_with_no_state_yet_goes_inline_from_off(daemon_session):
    session_marker.state_path(SID).unlink()
    assert session_marker.switch_to_inline(SID)
    assert session_marker.inline_marker(SID)["from"] == session_marker.STATE_OFF


def test_outside_the_daemon_profile_inline_is_on():
    """The agent already reads and writes Probe there: `inline` is `on`."""
    session_marker.set_session_state(SID, session_marker.STATE_READ_ONLY)
    assert session_marker.switch_to_inline(SID)
    assert session_marker.session_state(SID) == session_marker.STATE_FULL
    assert not session_marker.inline_path(SID).exists()


def test_a_leave_that_cannot_be_logged_keeps_the_stretch_the_agents(daemon_session, monkeypatch):
    """The log is the daemon's only record of the stretch once the marker goes:
    a move whose log fails keeps the marker, closed, so the next worker still
    skips the stretch; the next entry logs it (review: Codex)."""
    assert session_marker.switch_to_inline(SID, now=10.0)
    real = session_marker._log_inline_interval
    monkeypatch.setattr(session_marker, "_log_inline_interval", lambda *a, **k: False)
    assert session_marker.set_session_state(SID, session_marker.STATE_DAEMON)
    assert not session_marker.is_inline(SID), "the researcher's move still lands"
    ((since, until),) = session_marker.inline_intervals(SID)
    assert since == 10.0 and until is not None

    monkeypatch.setattr(session_marker, "_log_inline_interval", real)
    assert session_marker.switch_to_inline(SID, now=time.time() + 60)
    intervals = session_marker.inline_intervals(SID)
    assert intervals[0][1] is None and (10.0, until) in intervals, "logged now, and the new stretch open"


def test_a_closed_marker_is_logged_by_the_next_ordinary_move(daemon_session, monkeypatch):
    assert session_marker.switch_to_inline(SID, now=10.0)
    real = session_marker._log_inline_interval
    monkeypatch.setattr(session_marker, "_log_inline_interval", lambda *a, **k: False)
    assert session_marker.set_session_state(SID, session_marker.STATE_DAEMON, now=20.0)
    monkeypatch.setattr(session_marker, "_log_inline_interval", real)
    assert session_marker.set_session_state(SID, session_marker.STATE_READ_ONLY)
    assert not session_marker.inline_path(SID).exists()
    assert session_marker.inline_intervals(SID) == [(10.0, 20.0)]


def test_a_stretch_that_cannot_be_kept_anywhere_holds_the_switch(daemon_session, monkeypatch):
    """Neither the log nor the closed marker can be written: the move does not
    happen, rather than reopen recording over turns the agent recorded (review:
    Codex, Claude adversarial)."""
    assert session_marker.switch_to_inline(SID, now=10.0)
    real = session_marker._publish_atomically
    monkeypatch.setattr(session_marker, "_log_inline_interval", lambda *a, **k: False)
    monkeypatch.setattr(session_marker, "_publish_atomically",
                        lambda path, content: False if path == session_marker.inline_path(SID) else real(path, content))
    assert not session_marker.set_session_state(SID, session_marker.STATE_DAEMON)
    assert session_marker.is_inline(SID)


def test_an_unlogged_stretch_is_never_overwritten_by_the_next(daemon_session):
    """An unwritable log: inline, off (the marker kept closed), inline again must
    not overwrite that marker -- nothing moves (review: security, Codex)."""
    session_marker.inline_log_path(SID).mkdir(parents=True)
    assert session_marker.switch_to_inline(SID, now=1000.0)
    assert session_marker.set_session_state(SID, session_marker.STATE_OFF, now=1500.0)
    assert not session_marker.switch_to_inline(SID, now=2000.0)
    assert session_marker.session_state(SID) == session_marker.STATE_OFF
    assert session_marker.inline_intervals(SID) == [(1000.0, 1500.0)]


def test_a_stretch_keeps_its_log_when_the_profile_changes_under_it(daemon_session):
    """pi rewrites `<sid>.profile` on every start: an open stretch is still
    logged when the switch moves (review: Claude adversarial)."""
    assert session_marker.switch_to_inline(SID, now=10.0)
    session_marker.mark_session_profile(SID, "agent")
    assert session_marker.set_session_state(SID, session_marker.STATE_FULL, now=20.0)
    assert session_marker.inline_intervals(SID) == [(10.0, 20.0)]


def test_the_interval_reader_sees_a_leave_between_its_reads(daemon_session, monkeypatch):
    """A leave whose log failed lands after the reader saw the session inline:
    the reader keeps the open stretch it saw, never nothing (review: Codex on
    the fixes)."""
    assert session_marker.switch_to_inline(SID, now=10.0)
    real = session_marker.is_inline
    calls = []

    def racing(sid, state=None):
        answer = real(sid, state)
        if not calls:
            calls.append(answer)
            marker = session_marker.inline_marker(SID)
            session_marker._publish_atomically(session_marker.inline_path(SID),
                                               json.dumps({**marker, "until": 20.0}) + "\n")
            session_marker._set_state_unlocked(SID, session_marker.STATE_DAEMON)
        return answer

    monkeypatch.setattr(session_marker, "is_inline", racing)
    assert session_marker.inline_intervals(SID) == [(10.0, None)]
    monkeypatch.setattr(session_marker, "is_inline", real)
    assert session_marker.inline_intervals(SID) == [(10.0, 20.0)]


def test_the_interval_reader_sees_a_leave_that_closed_the_marker_under_it(daemon_session, monkeypatch):
    """The reader read the open marker; then a leave whose log failed closed it
    and moved the state. Read again, the stretch is still the agent's (review:
    Codex)."""
    assert session_marker.switch_to_inline(SID, now=10.0)
    real = session_marker.inline_marker
    reads = []

    def racing(sid):
        marker = real(sid)
        if not reads:
            reads.append(marker)
            session_marker._publish_atomically(session_marker.inline_path(SID),
                                               json.dumps({**marker, "until": 20.0}) + "\n")
            session_marker._set_state_unlocked(SID, session_marker.STATE_DAEMON)
        return marker

    monkeypatch.setattr(session_marker, "inline_marker", racing)
    assert session_marker.inline_intervals(SID) == [(10.0, 20.0)]


def test_a_marker_or_log_with_impossible_times_claims_nothing(daemon_session):
    """A marker or log line is data the daemon trusts to skip events: a
    non-finite or inverted time must not hand every event to nobody."""
    session_marker.set_session_state(SID, session_marker.STATE_FULL)
    for bad in ('{"from": "daemon", "since": Infinity}', '{"from": "daemon", "since": "1.0"}',
                '{"from": "daemon", "since": true}', '{"from": "daemon"}', '{"from": "elsewhere", "since": 1}',
                '{"from": "daemon", "since": 5, "until": 1}', '{"from": "daemon", "since": 1, "until": Infinity}'):
        session_marker.inline_path(SID).write_text(bad)
        assert not session_marker.is_inline(SID), bad
        assert session_marker.inline_intervals(SID) == [], bad
    session_marker.inline_path(SID).unlink()
    session_marker.inline_log_path(SID).write_text(
        '{"since": -Infinity, "until": Infinity, "from": "daemon"}\n'
        '{"since": 5, "until": 1, "from": "daemon"}\n'
        'not json\n'
        '{"since": 1, "until": 2, "from": "daemon"}\n')
    assert session_marker.inline_intervals(SID) == [(1.0, 2.0)]


def test_a_researcher_move_waits_for_a_switch_in_flight_then_wins(daemon_session):
    """Moves take the per-session lock: an `off` made while an entry holds it
    lands after it, never under it."""
    done: list = []
    started = threading.Event()

    def researcher_moves() -> None:
        started.set()
        done.append(session_marker.set_session_state(SID, session_marker.STATE_OFF))

    with session_marker._StateLock(SID):
        researcher = threading.Thread(target=researcher_moves)
        researcher.start()
        assert started.wait(5)
        # Held past any timeout a fallback might use: an earlier fix wrote
        # unlocked after 1 s, and the switch it waited for then overwrote `off`.
        time.sleep(1.5)
        assert researcher.is_alive(), "the move waits for the lock"
        session_marker._publish_atomically(
            session_marker.inline_path(SID), json.dumps({"from": "daemon", "since": time.time()}) + "\n")
        session_marker._set_state_unlocked(SID, session_marker.STATE_FULL)
    researcher.join(5)
    assert done == [True]
    assert session_marker.session_state(SID) == session_marker.STATE_OFF
    assert not session_marker.inline_path(SID).exists()


def test_a_row_torn_by_a_short_write_does_not_swallow_the_next(daemon_session):
    session_marker.inline_log_path(SID).write_text('{"since": 1, "unt')
    assert session_marker.switch_to_inline(SID, now=10.0)
    assert session_marker.set_session_state(SID, session_marker.STATE_DAEMON)
    ((since, _until),) = session_marker.inline_intervals(SID)
    assert since == 10.0


def test_a_full_without_the_marker_is_not_inline(daemon_session):
    """An older CLI's `probe session track` stored `full` here: that must not
    open the CLI to the agent."""
    session_marker.set_session_state(SID, session_marker.STATE_FULL)
    assert not session_marker.is_inline(SID)
    assert session_marker.inline_intervals(SID) == []


def test_a_marker_from_a_crashed_entry_claims_no_turns(daemon_session):
    """The marker is written before the state: a crash between them leaves an
    open marker beside `daemon`. It is not inline, and clearing it logs nothing."""
    session_marker._publish_atomically(
        session_marker.inline_path(SID), json.dumps({"from": "daemon", "since": 1.0}) + "\n")
    assert not session_marker.is_inline(SID)
    assert session_marker.inline_intervals(SID) == []
    assert session_marker.set_session_state(SID, session_marker.STATE_DAEMON)
    assert not session_marker.inline_path(SID).exists()
    assert session_marker.inline_intervals(SID) == []


def test_the_words_a_person_reads(daemon_session):
    assert session_marker.switch_to_inline(SID)
    assert session_marker.state_display(session_marker.STATE_FULL, True, True) == "on (inline)"
    line = session_marker.render(None, configured=True, tracking=True, color=False,
                                 session_state=session_marker.STATE_FULL, daemon=True, inline=True)
    assert "on (inline)" in line


# ---------------------------------------------------------------------------
# Who moves it: the researcher, never the agent.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("start", [session_marker.STATE_DAEMON, session_marker.STATE_READ_ONLY,
                                   session_marker.STATE_OFF])
@pytest.mark.parametrize("typed", ["/probe inline", "/probe-research-daemon:probe inline", "$probe inline",
                                   "<command-message>probe</command-message>\n<command-name>/probe</command-name>\n"
                                   "<command-args>inline</command-args>"])
def test_a_typed_probe_inline_hands_probe_to_the_agent(guard, monkeypatch, capsys, start, typed):
    session_marker.set_session_state(SID, start)
    out = _run(guard, monkeypatch, capsys, _prompt(typed))
    assert session_marker.is_inline(SID) and session_marker.inline_marker(SID)["from"] == start
    notice = _context(out)
    assert notice.startswith("Probe is `on (inline)` for this conversation")
    for name in session_marker.INLINE_SKILL_FILES:
        path = DAEMON_PLUGIN / "inline" / name
        assert str(path) in notice and path.is_file(), name
    assert not _context(_run(guard, monkeypatch, capsys, _prompt("carry on"))), "told once"
    assert not _context(_run(guard, monkeypatch, capsys, _prompt(typed))), "a second sighting says nothing new"


def test_kimi_drops_the_typed_line_so_the_next_prompt_tells_the_agent(guard, monkeypatch, capsys):
    """Kimi runs a typed `/probe` through a hook whose output it drops
    (harness_io's quiet path): nothing is marked told there (review: testing)."""
    monkeypatch.setenv("PROBE_AGENT", "kimi_code")
    monkeypatch.setenv("PROBE_HOOK_QUIET", "1")
    _run(guard, monkeypatch, capsys, _prompt("/probe inline"))
    assert session_marker.is_inline(SID)
    monkeypatch.delenv("PROBE_HOOK_QUIET")
    assert "`on (inline)`" in _context(_run(guard, monkeypatch, capsys, _prompt("carry on")))


def test_codex_hears_it_after_its_next_tool_call(guard, monkeypatch, capsys):
    """Codex adds no context at a prompt (registry: prompt_context false); its
    PostToolUse context lands, so the notice waits for the next tool call."""
    monkeypatch.setenv("PROBE_AGENT", "codex")
    assert not _context(_run(guard, monkeypatch, capsys, _prompt("/probe inline")))
    assert session_marker.is_inline(SID)
    after = {"hook_event_name": "PostToolUse", "session_id": SID, "tool_name": "Bash",
             "tool_input": {"command": "probe session status"}}
    assert "`on (inline)`" in _context(_run(guard, monkeypatch, capsys, after))
    assert not _context(_run(guard, monkeypatch, capsys, after)), "told once"


@pytest.mark.parametrize("call", [_skill_call("inline"),
                                  {"hook_event_name": "PostToolUse", "session_id": SID, "tool_name": "SlashCommand",
                                   "tool_input": {"command": "/probe inline"}},
                                  _prompt("<skill>\n<name>probe-research-daemon:probe</name>\n"
                                          "ARGUMENTS: inline\n</skill>")])
def test_the_agent_cannot_hand_probe_to_itself(guard, monkeypatch, capsys, call):
    """A Skill or SlashCommand call, and Codex's activation block, are shapes the
    model makes: `inline` there moves nothing (T1 = A: the agent asks)."""
    assert not _context(_run(guard, monkeypatch, capsys, call))
    assert session_marker.session_state(SID) == session_marker.STATE_DAEMON
    assert not session_marker.is_inline(SID)


@pytest.mark.parametrize("start", [session_marker.STATE_DAEMON, session_marker.STATE_READ_ONLY,
                                   session_marker.STATE_OFF, "inline"])
@pytest.mark.parametrize("command", ["probe session state inline", "probe run list; probe session state inline",
                                     "probe session toggle", "probe session default on"])
def test_the_agents_shell_never_moves_the_switch(guard, monkeypatch, capsys, start, command):
    if start == "inline":
        session_marker.switch_to_inline(SID)
    else:
        session_marker.set_session_state(SID, start)
    before = (session_marker.session_state(SID), session_marker.is_inline(SID))
    assert _denied(_run(guard, monkeypatch, capsys, _pre(command))), command
    assert (session_marker.session_state(SID), session_marker.is_inline(SID)) == before


@pytest.mark.parametrize("command", ["probe session inline", "probe session daemon"])
def test_the_agents_takeover_commands_are_gone(guard, monkeypatch, capsys, command):
    out = _run(guard, monkeypatch, capsys, _pre(command))
    assert _denied(out)
    assert "ask the researcher to type `/probe inline`" in json.loads(out)["hookSpecificOutput"][
        "permissionDecisionReason"]
    assert cli.main(command.split()[1:]) == 2, "no such command"


@pytest.mark.parametrize("start", [session_marker.STATE_DAEMON, session_marker.STATE_READ_ONLY])
@pytest.mark.parametrize("command", ["probe session state on", "probe session toggle", "probe session track",
                                     "probe run list; probe session default on"])
def test_the_switch_is_refused_as_the_switch(guard, monkeypatch, capsys, start, command):
    """Kimi runs a typed `/probe on` through a hook the model never hears from,
    so its agent ran `probe session state on` itself: the switch's refusal says
    the move already happened, and names `/probe inline` among the moves."""
    session_marker.set_session_state(SID, start)
    out = _run(guard, monkeypatch, capsys, _pre(command))
    assert _denied(out), command
    reason = json.loads(out)["hookSpecificOutput"]["permissionDecisionReason"]
    assert "`probe session status`" in reason and "`/probe inline`" in reason
    assert session_marker.session_state(SID) == start


def test_while_inline_only_the_switch_and_the_question_folder_are_refused(guard, monkeypatch, capsys, tmp_path):
    assert _denied(_run(guard, monkeypatch, capsys, _pre("probe project create my-sweep")))
    session_marker.switch_to_inline(SID)
    for command in ("probe project create my-sweep", "probe run list", "probe search 'lr sweep'",
                    "probe notes push --file n.md", "probe session status"):
        assert not _denied(_run(guard, monkeypatch, capsys, _pre(command))), command
    assert not _denied(_run(guard, monkeypatch, capsys, _pre(tool="mcp__probe-research__search", tool_input={})))
    for command in ("probe session state on", "probe session default on --folder .", "probe session toggle",
                    "probe run list; probe session untrack"):
        out = _run(guard, monkeypatch, capsys, _pre(command))
        assert _denied(out), command
        assert json.loads(out)["hookSpecificOutput"]["permissionDecisionReason"] == (
            session_marker.INLINE_SWITCH_DENY.format(matched=" ".join(command.split(";")[-1].split()[:3])))
    answers = tmp_path / "state" / "probe" / "approvals" / "answers" / "x.json"
    assert _denied(_run(guard, monkeypatch, capsys, _pre(tool="Write", tool_input={"file_path": str(answers)})))
    assert session_marker.is_inline(SID)


def test_a_full_without_the_marker_stays_closed(guard, monkeypatch, capsys):
    session_marker.set_session_state(SID, session_marker.STATE_FULL)
    out = _run(guard, monkeypatch, capsys, _pre("probe project create my-sweep"))
    assert _denied(out)
    assert "`/probe inline`" in json.loads(out)["hookSpecificOutput"]["permissionDecisionReason"]


def test_the_researchers_switch_ends_inline(guard, monkeypatch, capsys):
    session_marker.switch_to_inline(SID)
    _run(guard, monkeypatch, capsys, _prompt("/probe on"))
    assert session_marker.session_state(SID) == session_marker.STATE_DAEMON
    assert not session_marker.is_inline(SID)
    assert _denied(_run(guard, monkeypatch, capsys, _pre("probe project create my-sweep")))


# ---------------------------------------------------------------------------
# Telling the agent: a switch made elsewhere, a compaction, a resume.
# ---------------------------------------------------------------------------


def test_a_switch_from_a_terminal_reaches_the_agent_on_its_next_prompt(guard, monkeypatch, capsys):
    """`probe session state inline --session <sid>` from a terminal prints to
    the terminal: the agent hears it on its next prompt, once per stretch."""
    monkeypatch.delenv("CLAUDE_CODE_SESSION_ID")
    assert cli.main(["session", "state", "inline", "--session", SID]) in (0, None)
    assert json.loads(capsys.readouterr().out)["label"] == "on (inline)"
    assert "`on (inline)`" in _context(_run(guard, monkeypatch, capsys, _prompt("what next?")))
    assert not _context(_run(guard, monkeypatch, capsys, _prompt("and now?")))

    session_marker.set_session_state(SID, session_marker.STATE_DAEMON)
    session_marker.switch_to_inline(SID, now=time.time() + 5)
    assert "`on (inline)`" in _context(_run(guard, monkeypatch, capsys, _prompt("again?"))), "a new stretch"


def _version_check(monkeypatch):
    monkeypatch.setenv("PROBE_PLUGIN_PROFILE", "daemon")
    hook = _load("_vc_inline", HOOKS / "version_check.py")
    monkeypatch.setattr(hook, "_daemon_profile_notice", lambda: None)
    monkeypatch.setenv(hook.SESSION_ID_ENV, SID)
    monkeypatch.delenv(hook.HOOK_EVENT_ENV, raising=False)
    return hook


def _final(hook, capsys) -> dict:
    with pytest.raises(SystemExit):
        hook._final({"continue": True})
    return json.loads(capsys.readouterr().out)


@pytest.mark.parametrize("source", ["compact", "resume"])
def test_a_compaction_or_resume_while_inline_tells_the_agent_again(guard, monkeypatch, capsys, source):
    """Said at SessionStart (Claude Code's auto-compaction carries the turn on
    with no new prompt) AND re-armed, so a harness whose SessionStart context
    does not land hears it at the next chance."""
    _run(guard, monkeypatch, capsys, _prompt("/probe inline"))
    assert not _context(_run(guard, monkeypatch, capsys, _prompt("carry on")))
    hook = _load("_vc_inline", DAEMON_PLUGIN / "hooks" / "version_check.py")
    monkeypatch.setattr(hook, "_daemon_profile_notice", lambda: None)
    monkeypatch.setenv(hook.SESSION_ID_ENV, SID)
    monkeypatch.delenv(hook.HOOK_EVENT_ENV, raising=False)
    monkeypatch.setenv(hook.SESSION_SOURCE_ENV, source)
    said = _final(hook, capsys)["hookSpecificOutput"]
    assert said["hookEventName"] == "SessionStart" and said["additionalContext"].startswith("Probe is `on (inline)`")
    for name in session_marker.INLINE_SKILL_FILES:
        assert str(DAEMON_PLUGIN / "inline" / name) in said["additionalContext"]
    assert "`on (inline)`" in _context(_run(guard, monkeypatch, capsys, _prompt("where were we?")))


def test_a_fresh_start_rearms_nothing(guard, monkeypatch, capsys):
    _run(guard, monkeypatch, capsys, _prompt("/probe inline"))
    hook = _version_check(monkeypatch)
    monkeypatch.setenv(hook.SESSION_SOURCE_ENV, "startup")
    assert "hookSpecificOutput" not in _final(hook, capsys)
    assert not _context(_run(guard, monkeypatch, capsys, _prompt("carry on")))


@pytest.mark.parametrize(("version", "bridge"), [("0.220.0", True), ("0.231.4", True), ("0.219.9", False),
                                               ("garbled", False), (None, False)])
def test_the_notice_names_the_read_bridge_only_beside_a_cli_that_has_it(guard, monkeypatch, capsys, tmp_path,
                                                                       version, bridge):
    """The plugin and the CLI update on their own schedules: below
    `INLINE_BRIDGE_MIN_CLI`, or with no readable version (no `probe` at all
    included), the notice says the CLI is too old instead of naming commands it
    lacks. Both places it is said agree: the guard's prompt and SessionStart."""
    monkeypatch.setenv("PROBE_BIN", _fake_probe(tmp_path, version) if version else str(tmp_path / "missing"))
    reads = session_marker.INLINE_READS if bridge else session_marker.INLINE_READS_OLD_CLI
    told = _context(_run(guard, monkeypatch, capsys, _prompt("/probe inline")))
    assert told.startswith("Probe is `on (inline)`") and told.endswith(reads)
    assert len(told.encode()) < 2048

    hook = _version_check(monkeypatch)
    monkeypatch.setenv(hook.SESSION_SOURCE_ENV, "compact")
    assert hook.INLINE_BRIDGE_MIN_CLI == "0.220.0"
    assert _final(hook, capsys)["hookSpecificOutput"]["additionalContext"].endswith(reads)


def test_the_notice_fits_a_hook_and_names_files_that_ship():
    """Claude Code saves hook context over ~2 KB to a file and shows a preview
    (verified 2026-10-06): the notice stays well under it, and the files it
    names are the main agent's track-work and edit-notes, byte for byte."""
    long_root = "/home/someone-with-a-long-name/.claude/plugins/cache/probe-research/probe-research-daemon/0.120.0"
    for bridge in (True, False):
        notice = session_marker.inline_notice(f"{long_root}/inline/track-work/SKILL.md",
                                              f"{long_root}/inline/edit-notes/SKILL.md", bridge=bridge)
        assert len(notice) < 1000 and "{" not in notice
    full = AGENT_ROOT / "plugins" / "probe-research" / "agent-skills"
    for name in session_marker.INLINE_SKILL_FILES:
        assert (DAEMON_PLUGIN / "inline" / name).read_bytes() == (full / name).read_bytes(), (
            f"{name}: run `make sync-plugin`")
    assert (DAEMON_PLUGIN / "inline" / "track-work" / "reference.md").read_bytes() == (
        full / "track-work" / "reference.md").read_bytes(), "track-work cites the reference beside it"
    assert not (DAEMON_PLUGIN / "skills" / "track-work").exists(), "never listed as a skill"


def test_the_texts_are_the_approved_ones():
    assert session_marker.INLINE_NOTICE == _body("reads/agent-facing/inline-notice.NEW.md")
    assert session_marker.INLINE_READS == _body("reads/agent-facing/inline-reads.NEW.md")
    assert session_marker.INLINE_READS_OLD_CLI == _body("reads/agent-facing/inline-reads-old-cli.NEW.md")
    assert session_marker.INLINE_SWITCH_DENY == _body("reads/agent-facing/inline-switch-refusal.NEW.md")
    assert daemon_cli.ASK_SESSION_INLINE == _body("reads/agent-facing/ask-inline.NEW.md")
    assert worker_mod.INLINE_NOTICE == _body("bite/inline-skipped.PROPOSED.md")


# ---------------------------------------------------------------------------
# The CLI.
# ---------------------------------------------------------------------------


def test_probe_ask_is_refused_while_inline(daemon_session, capsys):
    session_marker.switch_to_inline(SID)
    assert cli.main(["ask", "what did we try?"]) == 1
    assert daemon_cli.ASK_SESSION_INLINE in capsys.readouterr().err


@pytest.mark.parametrize("env", ["CLAUDE_CODE_SESSION_ID", "CODEX_THREAD_ID", "PI_SESSION_ID"])
def test_session_state_inline_refuses_inside_an_agent(daemon_session, capsys, monkeypatch, env):
    """The agent asking for itself, however wrapped (`probe exec --`, `bash -lc`,
    `uv run`, a script): its shell carries its session variable (review:
    security, Codex, Claude adversarial)."""
    monkeypatch.delenv("CLAUDE_CODE_SESSION_ID")
    monkeypatch.setenv(env, "99999999-0000-0000-0000-000000000000")
    assert cli.main(["session", "state", "inline", "--session", SID]) == 2
    assert cli_main.INLINE_FROM_AGENT in capsys.readouterr().err
    assert session_marker.session_state(SID) == session_marker.STATE_DAEMON
    assert not session_marker.is_inline(SID)


@pytest.mark.parametrize("argv", [["session", "state", "off"], ["session", "state", "read"], ["session", "toggle"],
                                  ["session", "track"], ["session", "untrack"], ["session", "default", "off"]])
def test_no_switch_move_runs_inside_an_agent_the_daemon_records(daemon_session, capsys, argv):
    """Live smoke 2026-10-06: the agent ran `bash -lc 'probe session state off'`
    past the guard and turned Probe off. Inside a daemon-profile agent session the
    CLI refuses every switch move itself; a terminal (no agent variable) moves it."""
    assert cli.main(argv) == 2
    assert "moves the researcher's Probe switch" in capsys.readouterr().err
    assert session_marker.session_state(SID) == session_marker.STATE_DAEMON


def test_the_researchers_terminal_and_the_agent_profile_still_move_it(daemon_session, capsys, monkeypatch):
    monkeypatch.delenv("CLAUDE_CODE_SESSION_ID")
    assert cli.main(["session", "state", "read", "--session", SID]) in (0, None)
    assert session_marker.session_state(SID) == session_marker.STATE_READ_ONLY
    other = "22222222-3333-4444-5555-666666666666"
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", other)
    assert cli.main(["session", "state", "off"]) in (0, None), "an agent-profile session: the switch is the agent's too"
    assert session_marker.session_state(other) == session_marker.STATE_OFF
    assert cli.main(["session", "state", "on", "--session", SID]) == 2, "not another session the daemon records"


def test_session_state_inline_fails_loudly_when_nothing_went_inline(daemon_session, capsys, monkeypatch):
    monkeypatch.delenv("CLAUDE_CODE_SESSION_ID")
    monkeypatch.setattr(session_marker, "switch_to_inline", lambda *a, **k: False)
    assert cli.main(["session", "state", "inline", "--session", SID]) == 1
    assert "not inline" in capsys.readouterr().err


def test_session_state_offers_inline(daemon_session, capsys, monkeypatch):
    monkeypatch.delenv("CLAUDE_CODE_SESSION_ID")
    assert cli.main(["session", "state", "sideways", "--session", SID]) == 1
    assert "'inline'" in capsys.readouterr().err


def test_the_status_line_says_on_inline(daemon_session, monkeypatch, tmp_path):
    statusline = _load("_statusline_inline", HOOKS / "statusline.py")
    monkeypatch.setattr(statusline, "_load", lambda _name: session_marker)
    monkeypatch.setenv("PROBE_TOKEN", "configured")
    session_marker.switch_to_inline(SID)
    assert "on (inline)" in statusline.segment({"session_id": SID, "cwd": str(tmp_path)})


def test_pis_session_initialize_leaves_an_inline_session_inline(capsys, monkeypatch, tmp_path):
    """pi runs `session initialize` on every start, resume and reload, and heals
    an `on` session to its profile: an inline one must not be handed back."""
    monkeypatch.delenv("CLAUDE_CODE_SESSION_ID", raising=False)
    monkeypatch.setenv("PI_SESSION_ID", SID)
    session_marker.write_recorder("pi", session_marker.RECORDER_DAEMON)
    session_marker.mark_session_profile(SID, session_marker.RECORDER_DAEMON)
    session_marker.set_session_state(SID, session_marker.STATE_DAEMON)
    session_marker.switch_to_inline(SID)
    assert cli.main(["session", "initialize", "--cwd", str(tmp_path)]) in (0, None)
    capsys.readouterr()
    assert session_marker.session_state(SID) == session_marker.STATE_FULL
    assert session_marker.is_inline(SID)
