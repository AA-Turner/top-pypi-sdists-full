"""Notes parity (2026-10-28): inline and the daemon use Probe notes the same way.

  N1  an inline agent gets the three skills the daemon's writer reads, whole
      (`session_marker.next_inline_skills_part`, the lean plugin's guard and
      SessionStart; pi's notice)
  N2  the first write a session makes to an entity prints the opening of its
      note and its Open / Don't repeat lines, or nothing (`cli.first_touch`)
  N3  one owed ledger, kept by the CLI (`cli.owed`): the daemon's validator
      and an inline agent's end-of-turn hook both read it, in the same words

Driven through the real CLI (`cli.main`) against the repo's FakeApp, the real
hooks of the lean plugin, and the daemon's real writer with a scripted model.
"""

from __future__ import annotations

import asyncio
import importlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import threading
import time
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

import pytest

from probe import cli, skill_versions
from probe.cli import first_touch, owed, summary_cli
from probe.daemon import bite, tools
from probe.sdk import errors, session_marker
from tests.conftest import make_client, open_run
from tests.test_cli_summary import SummaryServer

cli_main = importlib.import_module("probe.cli.main")
AGENT_ROOT = Path(__file__).resolve().parents[1]
DAEMON_PLUGIN = AGENT_ROOT / "plugins" / "probe-research-daemon"
PI_PACKAGE = AGENT_ROOT / "plugins" / "probe-research-pi"
SID = "11111111-2222-3333-4444-555555555555"
OTHER = "22222222-3333-4444-5555-666666666666"
NOTE = (
    "Distils the 7B teacher into a 1B student.\n"
    "Started 10-20 after the int8 port.\n\n"
    "## Where it stands\n- loss flat at 1.9\n\n"
    "## Don’t repeat\n- lr 3e-4 diverges by step 400\n\n"
    "## Open\n- does int8 hold past 2k steps?\n"
)


@pytest.fixture(autouse=True)
def _env(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "cache"))
    for name in ("PROBE_DAEMON_SESSION", "PROBE_RUN_ID", "CLAUDE_CODE_SESSION_ID", "CODEX_THREAD_ID",
                 "PI_SESSION_ID", "PROBE_PLUGIN_PROFILE", "PROBE_SESSION_STATE", "PROBE_HOOK_QUIET"):
        monkeypatch.delenv(name, raising=False)


@pytest.fixture
def server(app, tmp_path, monkeypatch):
    """Project `p` (with NOTE), experiment `e` (no note) and a run, made with no
    session; summary routes as CONTRACT.md has them."""
    fake = SummaryServer(app)
    monkeypatch.setattr(cli, "Client", lambda **_kw: make_client(app, tmp_spool=tmp_path / "spool"))
    assert cli.main(["project", "create", "--kind", "general", "p"]) == 0
    assert cli.main(["experiment", "create", "e", "--question", "does it work?", "--project", "p"]) == 0
    assert cli.main(["notes", "append", "--project", "p", "--text", NOTE]) == 0
    fake.run = open_run(make_client(app, tmp_spool=tmp_path / "s"), experiment="e", name="r1")
    return fake


def _agent(monkeypatch, sid: str = SID) -> None:
    monkeypatch.setenv("CLAUDECODE", "1")
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", sid)


def _err(capsys, *argv: str) -> str:
    capsys.readouterr()
    assert cli.main(list(argv)) == 0, argv
    return capsys.readouterr().err


# ---------------------------------------------------------------------------
# N1: the skills, whole, only inline
# ---------------------------------------------------------------------------


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
def guard(monkeypatch, tmp_path):
    """The lean plugin's guard as Claude Code runs it, in a daemon-profile session."""
    session_marker.mark_session_profile(SID, session_marker.RECORDER_DAEMON)
    session_marker.set_session_state(SID, session_marker.STATE_DAEMON)
    probe = tmp_path / "probe-cli"
    probe.write_text("#!/bin/sh\necho 'probe 0.300.0'\n")
    probe.chmod(0o755)
    monkeypatch.setenv("PROBE_PLUGIN_PROFILE", "daemon")
    monkeypatch.setenv("PROBE_BIN", str(probe))
    monkeypatch.setenv("PROBE_AGENT", "claude_code")
    sys.modules.pop("_probe_hooks.version_check", None)
    return _load("_guard_parity", DAEMON_PLUGIN / "hooks" / "tracking_guard.py")


def _hook(guard, monkeypatch, capsys, event: str, **fields) -> str:
    payload = {"hook_event_name": event, "session_id": SID, **fields}
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
    guard.main()
    out = capsys.readouterr().out
    return json.loads(out)["hookSpecificOutput"]["additionalContext"] if out else ""


def _parts(text: str) -> list[str]:
    head = session_marker.INLINE_SKILLS_PART.split(" (", 1)[0]
    return [chunk.split("\n\n", 1)[1] for chunk in text.split(head)[1:]]


DAEMONS_TEXT = bite.skills_text(bite.SHARED_SKILLS, reader=skill_versions.MAIN_AGENT)


def test_the_inline_skills_are_the_daemons_text_for_a_main_agent():
    """The lean plugin's `inline/` copies and pi's package render the text the
    daemon's loader gives a main agent (`backfill_record.py` uses it too)."""
    assert tuple(name.split("/", 1)[0] for name in session_marker.INLINE_SKILL_FILES) == bite.SHARED_SKILLS
    assert DAEMONS_TEXT and session_marker.inline_skills_text(DAEMON_PLUGIN / "inline") == DAEMONS_TEXT
    assert session_marker.inline_skills_text(PI_PACKAGE / "skills") == DAEMONS_TEXT
    parts = session_marker.split_parts(DAEMONS_TEXT)
    assert "".join(parts) == DAEMONS_TEXT and len(parts) > 1
    assert all(len(p) <= session_marker.INLINE_SKILLS_PART_CHARS for p in parts)


def test_an_inline_agent_gets_them_whole_in_parts_that_fit_a_hook(guard, monkeypatch, capsys):
    """Claude Code: the notice and part 1 at the typed `/probe inline`, then a
    part with each tool call, under its 10,000-character hook cap, then nothing."""
    first = _hook(guard, monkeypatch, capsys, "UserPromptSubmit", prompt="/probe inline")
    assert first.startswith("Probe is `on (inline)`") and len(first) < 10_000
    seen = [first]
    for _ in range(6):
        seen.append(_hook(guard, monkeypatch, capsys, "PostToolUse", tool_name="Bash",
                          tool_input={"command": "ls"}))
    got = [p for text in seen for p in _parts(text)]
    assert got == [p.strip("\n") for p in session_marker.split_parts(DAEMONS_TEXT)]
    assert all(len(text) < 10_000 for text in seen)
    assert not seen[-1], "every part went once"


@pytest.mark.parametrize("state", [session_marker.STATE_DAEMON, session_marker.STATE_READ_ONLY,
                                   session_marker.STATE_OFF])
def test_no_skills_while_the_daemon_records_reads_or_probe_is_off(guard, monkeypatch, capsys, state):
    session_marker.set_session_state(SID, state)
    said = [_hook(guard, monkeypatch, capsys, "UserPromptSubmit", prompt="carry on")]
    said += [_hook(guard, monkeypatch, capsys, "PostToolUse", tool_name="Bash", tool_input={"command": "ls"})
             for _ in range(3)]
    assert not any(_parts(text) for text in said)


def test_read_only_inline_gets_no_skills(guard, monkeypatch, capsys):
    session_marker.set_session_state(SID, session_marker.STATE_READ_ONLY)
    assert session_marker.inline_on_budget(SID, session_marker.STATE_READ_ONLY)
    said = _hook(guard, monkeypatch, capsys, "UserPromptSubmit", prompt="go on")
    assert "Record nothing new" in said and not _parts(said)


def test_codex_hears_notice_and_parts_after_its_tool_calls(guard, monkeypatch, capsys):
    monkeypatch.setenv("PROBE_AGENT", "codex")
    assert not _hook(guard, monkeypatch, capsys, "UserPromptSubmit", prompt="/probe inline")
    after = _hook(guard, monkeypatch, capsys, "PostToolUse", tool_name="Bash", tool_input={"command": "ls"})
    assert after.startswith("Probe is `on (inline)`") and _parts(after)
    assert not _hook(guard, monkeypatch, capsys, "UserPromptSubmit", prompt="next"), "no prompt context"


def test_a_compaction_sends_them_again_from_part_one(guard, monkeypatch, capsys):
    _hook(guard, monkeypatch, capsys, "UserPromptSubmit", prompt="/probe inline")
    hook = _load("_vc_parity", DAEMON_PLUGIN / "hooks" / "version_check.py")
    monkeypatch.setattr(hook, "_daemon_profile_notice", lambda: None)
    monkeypatch.setenv(hook.SESSION_ID_ENV, SID)
    monkeypatch.setenv(hook.SESSION_SOURCE_ENV, "compact")
    monkeypatch.delenv(hook.HOOK_EVENT_ENV, raising=False)
    with pytest.raises(SystemExit):
        hook._final({"continue": True})
    said = json.loads(capsys.readouterr().out)["hookSpecificOutput"]["additionalContext"]
    assert _parts(said) == [session_marker.split_parts(DAEMONS_TEXT)[0].strip("\n")]


# ---------------------------------------------------------------------------
# N2: the note, on the first write
# ---------------------------------------------------------------------------


def test_the_first_write_prints_the_notes_opening_and_open_lines_once(server, capsys, monkeypatch):
    _agent(monkeypatch)
    err = _err(capsys, "project", "set", "p", "--name", "P")
    assert ("Note on project p (all of it: probe notes show --project p):\n"
            "Distils the 7B teacher into a 1B student. Started 10-20 after the int8 port.\n"
            "Don't repeat: - lr 3e-4 diverges by step 400\n"
            "Open: - does int8 hold past 2k steps?") in err
    assert "loss flat" not in err, "only the opening and the two sections"
    assert "Note on" not in _err(capsys, "project", "set", "p", "--name", "P2"), "once per session"
    _agent(monkeypatch, OTHER)
    assert "Note on project p" in _err(capsys, "project", "set", "p", "--name", "P3"), "another session"
    monkeypatch.delenv("CLAUDE_CODE_SESSION_ID")
    monkeypatch.setenv("PROBE_DAEMON_SESSION", OTHER)
    assert "Note on project p" in _err(capsys, "project", "set", "p", "--name", "P4"), "the daemon's own"


def test_an_entity_with_no_note_prints_nothing(server, capsys, monkeypatch):
    _agent(monkeypatch)
    assert "Note on" not in _err(capsys, "experiment", "set", "e", "--question", "still?")
    assert "Note on" not in _err(capsys, "experiment", "create", "x2", "--question", "q", "--project", "p")


def test_a_failed_read_is_silent_and_the_write_stands(server, capsys, monkeypatch):
    _agent(monkeypatch)

    def down(*_a, **_kw):
        raise errors.ServerError("Probe answered 503", status=503)

    monkeypatch.setattr(cli_main, "_entity_notes_row", down)
    err = _err(capsys, "project", "set", "p", "--name", "P")
    assert "Note on" not in err and "503" not in err and "Traceback" not in err


def test_what_is_printed_is_bounded():
    long = "word " * 400 + "\n\n**Open:** " + "q " * 400
    text = first_touch.render("run", "r1", long)
    assert len(text) <= first_touch.MAX_CHARS and text.endswith("…")
    assert first_touch.render("run", "r1", "") is None and first_touch.render("run", "r1", "  \n") is None
    assert first_touch.excerpt("**Don't repeat:** int4\n")["don't repeat"] == ["int4"]


# ---------------------------------------------------------------------------
# N3: one owed ledger
# ---------------------------------------------------------------------------


def _owed(sid: str = SID) -> list[tuple[str, str, str, str]]:
    return [(i["why"], i["kind"], i["ref"], i["by"]) for i in owed.owed(sid)]


def _edit_and_push(capsys, *flags: str) -> int:
    capsys.readouterr()
    assert cli.main(["summary", "checkout", *flags]) == 0
    path = Path(json.loads(capsys.readouterr().out)["path"])
    path.write_text(path.read_text() + "\nThe answer: yes.\n")
    return cli.main(["summary", "push", *flags])


def test_creating_or_concluding_owes_the_summary_until_a_push_lands(server, capsys, monkeypatch):
    _agent(monkeypatch)
    assert cli.main(["experiment", "create", "x2", "--question", "q", "--project", "p"]) == 0
    assert cli.main(["experiment", "set", "e", "--conclusion", "it works"]) == 0
    assert cli.main(["experiment", "set", "e", "--question", "renamed"]) == 0, "no conclusion: owes nothing new"
    assert _owed() == [("summary", "experiment", "x2", "agent"), ("summary", "experiment", "e", "agent")]
    capsys.readouterr()
    assert cli.main(["summary", "checkout", "--experiment", "e", "--project", "p"]) == 0
    assert cli.main(["summary", "push", "--experiment", "e", "--project", "p"]) == 0  # no edits: nothing sent
    assert ("summary", "experiment", "e", "agent") in _owed(), "a push that sent nothing settles nothing"
    assert _edit_and_push(capsys, "--experiment", "e", "--project", "p") == 0
    assert _owed() == [("summary", "experiment", "x2", "agent")]
    assert cli.main(["experiment", "set", "e", "--conclusion", "it works, twice"]) == 0
    assert ("summary", "experiment", "e", "agent") in _owed(), "a conclusion after the push owes it again"


def test_a_run_tagged_invalid_owes_a_note_until_one_lands(server, capsys, monkeypatch):
    _agent(monkeypatch)
    run = server.run.id
    assert cli.main(["run", "tag", run, "done"]) == 0
    assert _owed() == []
    assert cli.main(["run", "tag", run, "invalid"]) == 0
    assert _owed() == [("note", "run", run, "agent")]
    assert cli.main(["notes", "append", "--project", "p", "--text", "elsewhere"]) == 0
    assert _owed() == [("note", "run", run, "agent")], "a note on another entity is not it"
    assert cli.main(["notes", "append", "--run", run, "--text", "Believe the rerun r2, not this."]) == 0
    assert _owed() == []
    assert cli.main(["run", "tag", run, "invalid"]) == 0
    assert _owed() == [], "already invalid: nothing new is owed"


def _inline(sid: str = SID) -> None:
    session_marker.mark_session_profile(sid, session_marker.RECORDER_DAEMON)
    session_marker.set_session_state(sid, session_marker.STATE_DAEMON)
    assert session_marker.switch_to_inline(sid)


def _owing(server, capsys, monkeypatch) -> str:
    """An inline session that concluded `e` (recorder mode seen) and tagged its run invalid."""
    _inline()
    _agent(monkeypatch)
    assert cli.main(["experiment", "set", "e", "--conclusion", "it works"]) == 0
    assert cli.main(["run", "tag", server.run.id, "invalid"]) == 0
    summary_cli.record_mode(summary_cli.MODE_RECORDER)
    return server.run.id


def test_an_inline_agent_is_sent_back_in_the_daemons_words_at_most_twice(server, capsys, monkeypatch):
    pytest.importorskip("pydantic_ai")  # the `daemon` extra: CI runs without it
    from probe.daemon import agent as agent_mod

    run = _owing(server, capsys, monkeypatch)
    expected = (agent_mod.SUMMARY_OWED.format(entities="experiment e").removesuffix(", then end with final_result.")
                + ".\n" + agent_mod.NOTE_OWED.format(entities=f"run {run}").removesuffix(
                    ", then end with final_result.") + ".")
    for _ in range(owed.MAX_ASKS):
        capsys.readouterr()
        assert cli.main(["session", "owed", "--send-back", "--session", SID]) in (0, None)
        assert capsys.readouterr().out.strip() == expected
    capsys.readouterr()
    assert cli.main(["session", "owed", "--send-back", "--session", SID]) in (0, None)
    assert capsys.readouterr().out == "", "then quiet"


def test_no_send_back_outside_inline_or_before_recorder_mode_is_seen(server, capsys, monkeypatch):
    _agent(monkeypatch)
    assert cli.main(["experiment", "set", "e", "--conclusion", "it works"]) == 0
    summary_cli.record_mode(summary_cli.MODE_RECORDER)
    capsys.readouterr()
    assert cli.main(["session", "owed", "--send-back", "--session", SID]) in (0, None)
    assert capsys.readouterr().out == "", "not inline: the agent profile's own rules"
    assert owed.send_back(SID) and not owed.send_back(OTHER)
    summary_cli.record_mode(summary_cli.MODE_LANE)
    assert owed.send_back(SID) is None, "a lane team's push is refused: no summary asked"


def test_the_stop_hook_blocks_with_the_clis_words_then_stays_quiet(server, capsys, monkeypatch, tmp_path):
    """The lean plugin's Stop route as Claude Code runs it, beside the real CLI."""
    _owing(server, capsys, monkeypatch)
    expected = owed.send_back(SID)
    ledger = owed.read(SID)
    owed._update(SID, lambda data: data.update(asks={}))  # that look counted; start again
    probe = tmp_path / "probe"
    calls = tmp_path / "cli-calls"
    probe.write_text(f"#!/bin/sh\necho x >> {calls}\nexec {sys.executable} -m probe.cli \"$@\"\n")
    probe.chmod(0o755)
    env = {**os.environ, "PROBE_BIN": str(probe), "PROBE_PLUGIN_PROFILE": "daemon", "HOME": str(tmp_path),
           "PROBE_TELEMETRY": "off", "PYTHONPATH": str(AGENT_ROOT / "src")}
    hook = DAEMON_PLUGIN / "hooks" / "owed_hook.py"

    def stop() -> str:
        return subprocess.run([sys.executable, str(hook)], input=json.dumps({"session_id": SID,
                              "hook_event_name": "Stop"}), capture_output=True, text=True, env=env,
                              timeout=60).stdout

    for _ in range(owed.MAX_ASKS):
        assert json.loads(stop()) == {"decision": "block", "reason": expected}
    assert stop() == ""
    assert calls.read_text().count("x") == owed.MAX_ASKS, "an exhausted ledger starts no CLI"
    assert owed.read(SID)["items"] == ledger["items"], "the hook only asks; the ledger stands"
    session_marker.set_session_state(SID, session_marker.STATE_DAEMON)  # back to the daemon
    owed._update(SID, lambda data: data.update(asks={}))
    assert stop() == ""


def test_the_cheap_check_skips_what_the_cli_would_not_say(server, capsys, monkeypatch):
    """`session_marker.agent_owes`, which decides whether a Stop starts the CLI
    at all: never for items asked twice, a summary only in recorder mode."""
    _owing(server, capsys, monkeypatch)
    assert session_marker.agent_owes(SID)
    summary_cli.record_mode(summary_cli.MODE_LANE)
    assert session_marker.agent_owes(SID), "the run's note is still owed"
    owed._update(SID, lambda data: data.update(asks={f"note run {server.run.id}": owed.MAX_ASKS}))
    assert not session_marker.agent_owes(SID), "a lane team's summary is not asked; the note was, twice"
    summary_cli.record_mode(summary_cli.MODE_RECORDER)
    assert session_marker.agent_owes(SID) and owed.send_back(SID).startswith("Not ended: these summaries")
    assert owed.MAX_ASKS == session_marker.OWED_MAX_ASKS
    assert "export const OWED_MAX_ASKS = 2;" in (PI_PACKAGE / "src" / "owed.ts").read_text(), "pi's copy"


def test_taking_the_invalid_tag_off_settles_the_note(server, capsys, monkeypatch):
    _agent(monkeypatch)
    run = server.run.id
    assert cli.main(["run", "tag", run, "invalid"]) == 0
    assert _owed() == [("note", "run", run, "agent")]
    assert cli.main(["run", "tag", run, "--remove", "invalid"]) == 0
    assert _owed() == []
    assert cli.main(["run", "tag", run, "invalid", "done"]) == 0
    assert cli.main(["run", "tag", run, "--set", "done"]) == 0
    assert _owed() == [], "--set without it too"


def test_a_ctrl_c_during_the_notes_read_still_records_what_is_owed(server, capsys, monkeypatch):
    _agent(monkeypatch)

    def interrupted(*_a, **_kw):
        raise KeyboardInterrupt

    monkeypatch.setattr(first_touch, "_read", interrupted)
    assert cli.main(["experiment", "set", "e", "--conclusion", "it works"]) == 0
    assert _owed() == [("summary", "experiment", "e", "agent")]


def _first_touch_requests(app, *, hang: float = 0.0) -> list[str]:
    """Every request the first-touch read makes (its own thread), each made to
    wait `hang` seconds first: a server that answers nothing."""
    seen: list[str] = []
    inner = app.handler

    def handler(request):
        if threading.current_thread().name == "probe-first-touch":
            seen.append(f"{request.method} {request.url.path}")
            time.sleep(hang)
        return inner(request)

    app.handler = handler
    return seen


def test_a_hanging_server_holds_the_write_no_longer_than_the_bound(server, app, capsys, monkeypatch):
    _agent(monkeypatch)
    monkeypatch.setattr(first_touch, "READ_S", 0.5)
    seen = _first_touch_requests(app, hang=5.0)
    started = time.monotonic()
    err = _err(capsys, "project", "set", "p", "--name", "P")
    assert time.monotonic() - started < 3.0, "a stalled read is left behind at the bound"
    assert seen and "Note on" not in err


def test_a_write_only_queued_offline_reads_no_note(server, app, capsys, monkeypatch):
    """Probe did not answer the write (`probe log` queued it): the read is not tried."""
    import httpx

    _agent(monkeypatch)
    run = server.run.id
    assert first_touch.target(["log", run, "acc=0.9"]) == ("run", run, False), "a write on the run"
    seen = _first_touch_requests(app)
    inner = app.handler

    def down(request):
        if request.method != "GET":
            raise httpx.ConnectError("Probe is unreachable", request=request)
        return inner(request)

    app.handler = down
    capsys.readouterr()
    assert cli.main(["log", run, "acc=0.9"]) == 0
    assert cli_main._UNDELIVERED.total == 1, "queued, not sent"
    assert seen == []


def test_a_subagents_tool_calls_take_no_part(guard, monkeypatch, capsys):
    """Claude Code marks a hook fired inside a subagent with `agent_id`: a part
    landing there would be marked sent and never reach the agent."""
    first = _hook(guard, monkeypatch, capsys, "UserPromptSubmit", prompt="/probe inline")
    assert _parts(first)
    assert not _hook(guard, monkeypatch, capsys, "PostToolUse", tool_name="Bash", tool_input={"command": "ls"},
                     agent_id="a1b2", agent_type="general-purpose")
    second = _hook(guard, monkeypatch, capsys, "PostToolUse", tool_name="Bash", tool_input={"command": "ls"})
    assert _parts(second) == [session_marker.split_parts(DAEMONS_TEXT)[1].strip("\n")], "part 2 is still the next"


def test_parallel_tool_calls_never_send_a_part_twice(guard, monkeypatch, capsys):
    from concurrent.futures import ThreadPoolExecutor

    _hook(guard, monkeypatch, capsys, "UserPromptSubmit", prompt="/probe inline")
    root = DAEMON_PLUGIN / "inline"
    with ThreadPoolExecutor(8) as pool:
        got = list(pool.map(lambda _: session_marker.next_inline_skills_part(SID, root), range(8)))
    sent = [_parts(text)[0] for text in got if text]
    assert sent == sorted(set(sent), key=sent.index) and len(sent) == len(session_marker.split_parts(DAEMONS_TEXT)) - 1


def test_pis_fixture_is_the_daemons_text():
    """pi's vitest compares its own rendering to this file (`make sync-pi-skills`)."""
    fixture = PI_PACKAGE / "tests" / "fixtures" / "inline-skills.md"
    assert fixture.read_text(encoding="utf-8") == DAEMONS_TEXT, "run `make sync-pi-skills`"


# The daemon's writer, at the real CLI.


class RealCli:
    """`tools.run_probe_process` running the real `probe` CLI in this process,
    with what the daemon gives it (`PROBE_DAEMON_SESSION`): what it prints and
    what it keeps in the owed ledger are the CLI's own."""

    def __init__(self) -> None:
        self.ran: list[list[str]] = []

    async def __call__(self, deps, argv, op_id, **kw):
        self.ran.append(list(argv))
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.dict(os.environ, {"PROBE_DAEMON_SESSION": deps.session_id}), \
                redirect_stdout(out), redirect_stderr(err):
            code = cli.main(list(argv))
        return tools.ProbeResult(code, out.getvalue(), err.getvalue())


def _writer(tmp_path, monkeypatch, *commands: str, deps=None):
    """A writer run whose model runs `commands`, then ends, then ends again;
    `deps`: the next run of the same session (its store, fresh flags)."""
    pytest.importorskip("pydantic_ai")  # the `daemon` extra
    from pydantic_ai.messages import ModelResponse, ToolCallPart
    from pydantic_ai.models.function import FunctionModel

    from probe.daemon import agent as agent_mod
    from probe.daemon import probe_api
    from test_daemon_same_response_end import _deps, _retries

    async def recorder(env, kind, ref):
        return "recorder"

    monkeypatch.setattr(probe_api, "summaries_mode", recorder)
    monkeypatch.setattr(tools, "run_probe_process", RealCli())
    first = ModelResponse(parts=[ToolCallPart("shell", {"command": c}) for c in commands])
    end = ModelResponse(parts=[ToolCallPart("final_result", {"summary": "recorded"})])
    responses = [first, end, end, end, end]
    seen: list = []

    def model(messages, info):
        seen.append(messages)
        return responses[min(len(seen), len(responses)) - 1]

    deps = deps or _deps(tmp_path)
    result = asyncio.run(agent_mod.build_agent("instructions", model=FunctionModel(model)).run("record", deps=deps))
    return _retries(result.all_messages()), deps


def test_the_daemons_writer_is_sent_back_from_the_same_ledger(server, tmp_path, monkeypatch):
    pytest.importorskip("pydantic_ai")  # the `daemon` extra: CI runs without it
    from probe.daemon import agent as agent_mod

    run = server.run.id
    retries, deps = _writer(tmp_path, monkeypatch, "probe experiment set e --conclusion 'it works'",
                            f"probe run tag {run} invalid")
    assert retries == [agent_mod.NOTE_OWED.format(entities=f"run {run}"),
                       agent_mod.SUMMARY_OWED.format(entities="experiment e")]
    assert [(w, k, r, b) for w, k, r, b in _owed(deps.session_id)] == [
        ("summary", "experiment", "e", "daemon"), ("note", "run", run, "daemon")]
    assert owed.send_back(deps.session_id) is None, "an inline agent is never sent back for the daemon's"


def test_a_writer_that_wrote_the_note_ends_at_once(server, tmp_path, monkeypatch):
    run = server.run.id
    retries, deps = _writer(tmp_path, monkeypatch, f"probe run tag {run} invalid",
                            f"probe notes append --run {run} --text 'Believe r2 instead.'")
    assert retries == [] and _owed(deps.session_id) == []


def test_a_run_owes_only_what_it_left_since_it_began(server, tmp_path, monkeypatch):
    """`tally_settled` moves the run's start: what an earlier run left is its
    own, as the daemon's per-run tally always was."""
    import dataclasses

    first, deps = _writer(tmp_path, monkeypatch, "probe experiment set e --conclusion 'it works'")
    assert len(first) == 1, "sent back once, then the end stood"
    later = dataclasses.replace(deps, bite_id=2, ledger_from=0, summaries_owed_asked=False, notes_owed_asked=False,
                                visuals_owed_asked=False, tally_loaded=False)
    retries, _ = _writer(tmp_path, monkeypatch, "probe experiment set e --question 'and now?'", deps=later)
    assert retries == [] and _owed(SID) == [("summary", "experiment", "e", "daemon")]
