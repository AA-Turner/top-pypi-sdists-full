"""Feedback about Probe for the Probe team: asked first, sent only on a yes.

`probe.feedback` holds the text as a `feedback.send` question on the approvals
board; the answer hook, pi's dialog or `probe approvals` records the person's
pick; `probe feedback flush` sends what they said yes to. These tests run the
board, the CLI, the hook and the daemon's settle path against a temporary state
folder and a recording client: nothing reaches a server.
"""

from __future__ import annotations

import asyncio
import importlib
import json
import os
import stat
import subprocess
import sys
import time
from pathlib import Path

import pytest
from typer.testing import CliRunner

from probe import __version__
from probe import feedback as fb
from probe.daemon import approvals as appr
from probe.harness.registry import get_registry
from probe.sdk import errors, session_marker

cli_main = importlib.import_module("probe.cli.main")
SID = "11111111-2222-3333-4444-555555555555"
HOOK = Path(__file__).resolve().parents[1] / "plugins" / "probe-research" / "hooks" / "approvals_hook.py"
TEXT = "query_sql returned runs from other projects for a project-scoped question; I re-filtered by project_id."


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "no-config.json"))
    # This test may itself run inside a coding agent: no harness variable leaks in.
    for harness in get_registry().all():
        for name in (*harness.detect_env, harness.session_env):
            if name:
                monkeypatch.delenv(name, raising=False)
    for name in ("PROBE_DAEMON_SESSION", "PROBE_AGENT_SESSION", fb.ASKED_ENV, "PROBE_IDEMPOTENCY_KEY", "PROBE_AGENT"):
        monkeypatch.delenv(name, raising=False)


class Client:
    """Records each write; answers like the server (`landed`), queues (None) or refuses."""

    def __init__(self, landed: dict | None | Exception = None) -> None:
        self.landed = {"id": "f-1", "duplicate": False} if landed is None else landed
        self.calls: list[tuple[str, str, dict, dict]] = []

    def write(self, method, path, body=None, **kwargs):
        self.calls.append((method, path, body, kwargs))
        if isinstance(self.landed, Exception):
            raise self.landed
        return self.landed


def _board() -> appr.Board:
    return appr.Board()


def _hold(text: str = TEXT, *, session_id: str = SID, source=fb.Source.AGENT, harness="claude_code"):
    return fb.hold(text, session_id=session_id, source=source, harness=harness)


# ---------------------------------------------------------------------------
# The question
# ---------------------------------------------------------------------------


def test_the_question_shows_the_whole_text_and_everything_else_that_is_sent():
    req = _hold()
    q = req.question
    assert req.state == appr.WAITING and req.policy == appr.FEEDBACK
    assert q.header == f"Probe {req.id}"
    assert q.question == (f"Send this feedback to the Probe team?\n\nYour coding agent wrote:\n{TEXT}\n\n"
                          f"Also sent: your name and team, Claude Code, CLI {__version__}, this session's id.")
    assert q.options() == ["Send it", "Don't send"]
    assert appr.verify_held(_board().get(req.id))


def test_every_agent_source_is_named_in_the_question():
    assert set(appr.FEEDBACK_AUTHORS) == {s.value for s in fb.Source} - {fb.Source.ASSISTANT.value}


def test_feedback_is_asked_even_in_bypass_mode():
    """Richard 2026-10-13 (T1=A): the one policy bypass mode does not auto-approve."""
    req = _hold()
    assert req.state == appr.WAITING and req.channel is None
    assert (appr.approvals_dir() / "requests" / f"{req.id}.json").exists()


def test_credentials_are_redacted_before_the_person_sees_the_text():
    secret = "ros_ing_" + "0123456789abcdef" * 2
    req = _hold(f"the CLI printed my token {secret} in an error")
    assert secret not in req.question.question and secret not in json.dumps(req.facts)


@pytest.mark.parametrize("raw", [
    "visible\x1b[8mhidden part\x1b[0m end",   # an ANSI conceal code
    "hidden part\rvisible end",                # a carriage return overwrites the line
    "visible \u202ehidden part\u202c end",     # a bidi override
    "visible\u200b end",                        # a zero-width space
    "visible\U000e0041\U000e0042 end",           # Unicode tag characters
    "visible\ufe0f\u00ad\u2028 end",             # a variation selector, a soft hyphen, a line separator
])
def test_nothing_in_the_text_can_hide_itself_from_the_person(raw):
    req = _hold(raw)
    shown = req.question.question
    assert not any(ch in shown for ch in "\x1b\r\u202e\u202c\u200b\U000e0041\U000e0042\ufe0f\u00ad\u2028")
    assert req.facts["text"] in shown


def test_what_the_person_sees_is_what_the_transport_sends():
    """The question's redaction and the transport's scrub catch different shapes
    (a credential URI's host and port): the shown text is both, so the body the
    transport scrubs again is unchanged."""
    from probe.sdk.stamp_scrub import scrub_body

    req = _hold("the run failed on postgresql://app:hunter2@research-pg:5432/control and retried")
    body = fb.request_body(req)
    assert scrub_body(body)["text"] == body["text"] == req.facts["text"]
    assert "hunter2" not in req.question.question and body["text"] in req.question.question


@pytest.mark.parametrize("text, why", [("   ", "empty"), ("x" * (fb.MAX_CHARS + 1), "keep it under")])
def test_empty_or_too_long_feedback_is_refused(text, why):
    with pytest.raises(fb.Refused, match=why):
        _hold(text)
    assert not list((appr.approvals_dir() / "requests").glob("*.json"))


def test_one_feedback_question_waits_per_session():
    first = _hold()
    assert _hold().id == first.id  # the same text again is the same question
    with pytest.raises(fb.Refused, match=first.question.header):
        _hold("something else")
    assert _hold("something else", session_id="22222222-3333-4444-5555-666666666666").id != first.id


def test_an_answered_question_no_longer_blocks_the_next_one():
    """A no settles at the next `send`: the session is not stuck, and the same
    text again stays refused (asked once; a no stands)."""
    first = _hold()
    _board().answer(first.id, "Don't send", channel="question-tool")
    assert _hold().state == appr.DENIED
    assert _board().get(first.id).state == appr.DENIED
    assert _hold("something else").state == appr.WAITING


def test_the_account_it_was_asked_under_is_kept(monkeypatch):
    from probe.sdk import config

    monkeypatch.setattr(config, "current_context_name", lambda data=None: "lab-b")
    assert _hold().held == {"kind": "feedback", "context": "lab-b"}


def test_a_daemon_question_does_not_block_feedback():
    _board().hold(policy="shell.unsafe_command", session_id=SID, facts={"command": "make", "cwd": "/w"},
                  held={"kind": "shell", "command": "make", "cwd": "/w"}, bypass=False)
    assert _hold().state == appr.WAITING


# ---------------------------------------------------------------------------
# Sending
# ---------------------------------------------------------------------------


def test_a_yes_sends_it_once_keyed_by_the_question():
    req = _hold()
    board = _board()
    assert board.answer(req.id, "Send it", channel="question-tool")
    client = Client()
    assert fb.flush(lambda context: client) == [(req.id, fb.SENT)]
    method, path, body, kwargs = client.calls[0]
    assert (method, path, kwargs) == ("POST", fb.ROUTE, {"durable": False})
    # The harness goes on the wire as its registry id; the question shows its label.
    assert body == {"key": f"q-{req.id}-{req.fingerprint[:fb.KEY_FINGERPRINT_CHARS]}", "text": TEXT,
                    "source": "agent", "harness": "claude_code", "client_version": __version__, "session_id": SID}
    settled = board.get(req.id)
    assert (settled.state, settled.outcome, settled.channel) == (appr.APPROVED, fb.SENT, "question-tool")
    assert fb.flush(lambda context: client) == [] and len(client.calls) == 1


def test_each_yes_goes_with_the_account_it_was_asked_under(monkeypatch):
    from probe.sdk import config

    monkeypatch.setattr(config, "current_context_name", lambda data=None: "lab-a")
    first = _hold()
    monkeypatch.setattr(config, "current_context_name", lambda data=None: "lab-b")
    second = _hold("other", session_id="22222222-3333-4444-5555-666666666666")
    for req in (first, second):
        _board().answer(req.id, "Send it", channel="terminal")
    clients: dict = {}
    fb.flush(lambda context: clients.setdefault(context, Client()))
    assert {ctx: [c[2]["text"] for c in client.calls] for ctx, client in clients.items()} == {
        "lab-a": [TEXT], "lab-b": ["other"]}


def test_a_no_sends_nothing():
    req = _hold()
    _board().answer(req.id, "Don't send", channel="question-tool")
    client = Client()
    assert fb.flush(lambda context: client) == [(req.id, "no")]
    assert client.calls == [] and _board().get(req.id).state == appr.DENIED
    assert _hold().state == appr.DENIED  # asked once; a no stands


def test_nothing_to_send_builds_no_client():
    _hold()

    def factory(context):
        raise AssertionError("a flush with nothing answered must not build a client")

    assert fb.flush(factory) == []


def test_an_unanswered_question_expires_unsent():
    req = _hold()
    later = appr.Board(clock=lambda: req.expires_at + 1)
    assert fb.flush(lambda context: Client(), later) == [(req.id, "expired")]
    assert later.get(req.id).state == appr.EXPIRED


def test_a_yes_given_in_time_is_sent_by_a_late_flush():
    req = _hold()
    _board().answer(req.id, "Send it", channel="terminal")
    later = appr.Board(clock=lambda: req.expires_at + 3600)
    client = Client()
    assert fb.flush(lambda context: client, later) == [(req.id, fb.SENT)]


def test_a_refusal_is_recorded_and_not_retried():
    req = _hold()
    _board().answer(req.id, "Send it", channel="terminal")
    client = Client(errors.RosError("text too long", status=422))
    assert fb.flush(lambda context: client) == [(req.id, "yes: refused (422: text too long)")]
    assert fb.flush(lambda context: client) == [] and len(client.calls) == 1


@pytest.mark.parametrize("failure, shown", [
    (errors.RosError("not found", status=404), "404"),    # a server without the route yet
    (errors.RosError("slow down", status=429), "429"),
    (errors.RosError("bad gateway", status=502), "502"),
    (errors.TransportError("no route to host"), "TransportError"),
    (RuntimeError("no credential"), "RuntimeError"),
])
def test_a_send_that_can_land_later_is_tried_again(failure, shown):
    req = _hold()
    _board().answer(req.id, "Send it", channel="terminal")
    assert fb.flush(lambda context: Client(failure)) == [(req.id, f"{fb.UNSENT} ({shown})")]
    assert _board().get(req.id).outcome == fb.UNSENT
    client = Client()
    assert fb.flush(lambda context: client) == [(req.id, fb.SENT)]


def test_a_client_that_cannot_be_built_leaves_every_yes_for_later():
    first, second = _hold(), _hold("other", session_id="22222222-3333-4444-5555-666666666666")
    for req in (first, second):
        _board().answer(req.id, "Send it", channel="terminal")

    def broken(context):
        raise RuntimeError("no usable account")

    assert sorted(fb.flush(broken)) == sorted([(first.id, f"{fb.UNSENT} (RuntimeError)"),
                                               (second.id, f"{fb.UNSENT} (RuntimeError)")])
    client = Client()
    assert len(fb.flush(lambda context: client)) == 2 and len(client.calls) == 2


def test_a_question_edited_on_disk_after_it_was_asked_is_void():
    req = _hold()
    path = appr.approvals_dir() / "requests" / f"{req.id}.json"
    data = json.loads(path.read_text())
    data["facts"]["text"] = "something the person never saw"
    path.write_text(json.dumps(data))
    _board().answer(req.id, "Send it", channel="question-tool")
    client = Client()
    assert fb.flush(lambda context: client) == [(req.id, "void")]
    assert client.calls == []


# ---------------------------------------------------------------------------
# The CLI
# ---------------------------------------------------------------------------


def _cli(*args: str, env: dict | None = None):
    return CliRunner().invoke(cli_main.app, ["feedback", *args], env=env, catch_exceptions=False)


def test_a_claude_code_agent_is_told_to_ask_word_for_word(monkeypatch):
    monkeypatch.setenv("CLAUDECODE", "1")
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", SID)
    out = _cli("send", TEXT)
    assert out.exit_code == 0, out.output
    assert "AskUserQuestion tool, word for word" in out.output
    req = _board().all(session_id=SID)[0]
    fields = json.loads(out.output[out.output.index("{"):].strip())
    assert fields == {"header": req.question.header, "question": req.question.question,
                      "options": ["Send it", "Don't send"]}


def test_a_codex_agent_points_the_person_at_probe_approvals(monkeypatch):
    monkeypatch.setenv("CODEX_SANDBOX", "seatbelt")
    monkeypatch.setenv("CODEX_THREAD_ID", SID)
    out = _cli("send", TEXT)
    assert out.exit_code == 0, out.output
    assert "`probe approvals`" in out.output
    assert _board().all(session_id=SID)[0].facts["harness"] == "Codex"


def test_off_refuses_and_holds_nothing(monkeypatch):
    monkeypatch.setenv("CLAUDECODE", "1")
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", SID)
    session_marker.state_path(SID).parent.mkdir(parents=True, exist_ok=True)
    session_marker.state_path(SID).write_text(session_marker.STATE_OFF)
    out = _cli("send", TEXT)
    assert out.exit_code == 1 and "Probe is off" in out.output
    assert _board().all() == []


def test_no_session_to_ask_in_refuses():
    out = _cli("send", TEXT)
    assert out.exit_code == 1 and "no coding-agent session" in out.output
    assert _board().all() == []


def test_the_daemon_writer_holds_it_for_the_agents_session(monkeypatch):
    monkeypatch.setenv("PROBE_DAEMON_SESSION", SID)
    monkeypatch.setenv("PROBE_AGENT_SESSION", f"claude_code:{SID}")
    out = _cli("send", TEXT)
    assert out.exit_code == 0, out.output
    assert "asks the researcher at their next prompt" in out.output
    req = _board().all(session_id=SID)[0]
    assert (req.facts["source"], req.facts["harness"]) == ("daemon_writer", "Claude Code")
    assert "\n\nThe Probe daemon wrote:\n" in req.question.question


def test_the_dashboard_assistant_sends_at_once(monkeypatch):
    """Its approval card asked; its CLI child carries the env (`cli_supervisor`)."""
    client = Client()
    monkeypatch.setattr(cli_main, "_new_client", lambda **kw: client)
    monkeypatch.setenv(fb.ASKED_ENV, "assistant")
    monkeypatch.setenv("PROBE_IDEMPOTENCY_KEY", "op-123")
    out = _cli("send", TEXT)
    assert out.exit_code == 0, out.output
    _, path, body, kwargs = client.calls[0]
    assert path == fb.ROUTE and kwargs == {"durable": False}
    assert body == {"key": "op-123", "text": TEXT, "source": "assistant", "client_version": __version__}
    assert _board().all() == []


def test_the_same_feedback_after_a_no_is_refused(monkeypatch):
    monkeypatch.setenv("CLAUDECODE", "1")
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", SID)
    req = _hold()
    _board().answer(req.id, "Don't send", channel="question-tool")
    out = _cli("send", TEXT)
    assert out.exit_code == 1 and "already said no" in out.output


def test_probe_approvals_sends_a_yes_it_records(monkeypatch):
    """Codex has no question tool: the person answers in a terminal, and that
    command sends what they said yes to at once."""
    import io

    import typer

    from probe.cli import daemon_cli

    class Terminal(io.StringIO):
        def isatty(self):
            return True

    req = _hold()
    client = Client()
    monkeypatch.setattr(cli_main, "_new_client", lambda **kw: client)
    monkeypatch.setattr(sys, "stdin", Terminal())
    monkeypatch.setattr(sys, "stdout", Terminal())
    monkeypatch.setattr(typer, "prompt", lambda *a, **kw: "y")
    daemon_cli.approvals_cmd(list_only=False)
    assert [c[2]["key"] for c in client.calls] == [fb.request_body(_board().get(req.id))["key"]]
    assert _board().get(req.id).outcome == fb.SENT


def test_flush_sends_what_was_said_yes_to(monkeypatch):
    req = _hold()
    _board().answer(req.id, "Send it", channel="terminal")
    client = Client()
    monkeypatch.setattr(cli_main, "_new_client", lambda **kw: client)
    out = _cli("flush")
    assert out.exit_code == 0 and f"{req.id}: {fb.SENT}" in out.output
    assert len(client.calls) == 1


def test_the_daemon_profile_lets_the_agent_send_feedback():
    assert session_marker.daemon_profile_allows(["feedback", "send", TEXT]) == (True, "probe feedback send")
    # It sends only what the person said yes to (`probe.feedback`).
    assert session_marker.daemon_profile_allows(["feedback", "flush"]) == (True, "probe feedback flush")


# ---------------------------------------------------------------------------
# The answer hook (Claude Code / Kimi) and the daemon
# ---------------------------------------------------------------------------


def _fake_probe(tmp_path: Path) -> tuple[Path, Path]:
    log = tmp_path / "probe-calls.log"
    binary = tmp_path / "bin" / "probe"
    binary.parent.mkdir(parents=True, exist_ok=True)
    binary.write_text(f'#!/bin/sh\necho "$@" >> {log}\n')
    binary.chmod(binary.stat().st_mode | stat.S_IEXEC)
    return binary, log


def _hook(tmp_path, payload: dict, binary: Path) -> str:
    env = {**os.environ, "XDG_STATE_HOME": str(tmp_path / "state"), "PROBE_BIN": str(binary)}
    env.pop("PROBE_AGENT", None)
    out = subprocess.run([sys.executable, str(HOOK)], input=json.dumps(payload), capture_output=True, text=True,
                         env=env, timeout=30)
    assert out.returncode == 0, out.stderr
    return out.stdout


def _ask(tmp_path, req, choice: str, binary: Path) -> None:
    q = req.question
    tool_input = {"questions": [{"header": q.header, "question": q.question,
                                 "options": [{"label": q.yes_label}, {"label": q.no_label}]}]}
    _hook(tmp_path, {"hook_event_name": "PreToolUse", "tool_name": "AskUserQuestion", "session_id": SID,
                     "tool_input": tool_input, "tool_use_id": "tu-1"}, binary)
    _hook(tmp_path, {"hook_event_name": "PostToolUse", "tool_name": "AskUserQuestion", "session_id": SID,
                     "tool_input": tool_input, "tool_response": {"answers": {q.question: choice}},
                     "tool_use_id": "tu-1"}, binary)


def _wait_for(path: Path) -> str:
    for _ in range(100):
        if path.exists() and path.read_text():
            return path.read_text()
        time.sleep(0.05)
    return ""


def test_the_hook_starts_a_flush_after_a_yes_to_feedback(tmp_path):
    binary, log = _fake_probe(tmp_path)
    req = _hold()
    nudge = json.loads(_hook(tmp_path, {"hook_event_name": "UserPromptSubmit", "session_id": SID,
                                        "permission_mode": "bypassPermissions"}, binary))
    assert nudge["hookSpecificOutput"]["additionalContext"].startswith("Probe is holding a question")
    _ask(tmp_path, req, "Send it", binary)
    assert _board().take_answer(req.id)["answer"] == appr.YES
    assert _wait_for(log).strip() == "feedback flush"


def test_the_hook_starts_a_flush_only_after_a_yes_to_feedback(tmp_path):
    binary, log = _fake_probe(tmp_path)
    _ask(tmp_path, _hold(), "Don't send", binary)
    shell = _board().hold(policy="shell.unsafe_command", session_id=SID, facts={"command": "make", "cwd": "/w"},
                          held={"kind": "shell", "command": "make", "cwd": "/w"}, bypass=False)
    _ask(tmp_path, shell, shell.question.yes_label, binary)
    # The control: a feedback yes after them spawns, and the log holds that one alone.
    _ask(tmp_path, _hold("other feedback"), "Send it", binary)
    assert _wait_for(log).splitlines() == ["feedback flush"]
    time.sleep(0.3)
    assert log.read_text().splitlines() == ["feedback flush"]


def test_the_daemon_leaves_feedback_questions_alone(tmp_path):
    pytest.importorskip("pydantic_ai")
    from probe.daemon import lease
    from probe.daemon import worker as worker_mod

    lease.sessions_dir().mkdir(parents=True, exist_ok=True)
    (lease.sessions_dir() / f"{SID}.state").write_text("daemon")
    work = tmp_path / "home" / "work"
    work.mkdir(parents=True)
    transcript = tmp_path / f"{SID}.jsonl"
    transcript.write_text("")
    w = worker_mod.Worker(worker_mod.Session(SID, transcript, work, "claude_code", home=tmp_path / "home"))
    req = _hold()
    _board().answer(req.id, "Send it", channel="question-tool")
    asyncio.run(w.settle_answers())
    assert _board().get(req.id).state == appr.WAITING  # not voided: `probe feedback flush` sends it
    assert _board().take_answer(req.id)["answer"] == appr.YES


def test_an_answered_question_is_not_asked_again_nor_expired_by_the_terminal_list():
    req = _hold()
    _board().answer(req.id, "Send it", channel="question-tool")
    later = appr.Board(clock=lambda: req.expires_at + 1)
    assert later.waiting() == []
    assert later.get(req.id).state == appr.WAITING  # the flush reads the yes first
    client = Client()
    assert fb.flush(lambda context: client, later) == [(req.id, fb.SENT)]


def test_a_yes_for_an_account_no_longer_saved_stays_unsent(monkeypatch):
    from probe.cli import feedback_cli
    from probe.sdk import config

    monkeypatch.setattr(config, "current_context_name", lambda data=None: "lab-a")
    monkeypatch.setattr(config, "load_context", lambda name=None: {})
    with pytest.raises(RuntimeError, match="lab-b"):
        feedback_cli.client_for("lab-b")


def test_the_agents_shell_never_answers_probe_approvals(monkeypatch):
    """A pseudo-terminal (`script -qc 'probe approvals'`) keeps the agent's
    session in its environment: the questions are listed, nothing is answered."""
    import io

    import typer

    from probe.cli import daemon_cli

    class Terminal(io.StringIO):
        def isatty(self):
            return True

    req = _hold()
    monkeypatch.setenv("CLAUDECODE", "1")
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", SID)
    monkeypatch.setattr(sys, "stdin", Terminal())
    out = Terminal()
    monkeypatch.setattr(sys, "stdout", out)

    def never(*a, **kw):
        raise AssertionError("the agent's shell was asked to answer")

    monkeypatch.setattr(typer, "prompt", never)
    daemon_cli.approvals_cmd(list_only=False)
    assert "belongs to a coding agent" in out.getvalue()
    assert _board().take_answer(req.id) is None


def test_the_daemon_variable_in_an_agents_shell_does_not_make_it_the_daemons(monkeypatch):
    monkeypatch.setenv("CLAUDECODE", "1")
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", SID)
    monkeypatch.setenv("PROBE_DAEMON_SESSION", "22222222-3333-4444-5555-666666666666")
    out = _cli("send", TEXT)
    assert out.exit_code == 0, out.output
    (req,) = _board().all()
    assert (req.session_id, req.facts["source"]) == (SID, "agent")


def test_a_yes_an_older_daemon_voided_is_still_sent():
    """A daemon from before `feedback.send` cannot verify the question and
    voids it (`worker._settle`); the yes is still the person's, so it is sent."""
    req = _hold()
    _board().answer(req.id, "Send it", channel="question-tool")
    board = _board()
    board.resolve(board.get(req.id), state=appr.VOID, outcome=fb.OLD_DAEMON_VOID)
    client = Client()
    assert fb.flush(lambda context: client, board) == [(req.id, fb.SENT)]


def test_a_void_this_code_wrote_stays_void():
    req = _hold()
    _board().answer(req.id, "Send it", channel="question-tool")
    board = _board()
    board.resolve(board.get(req.id), state=appr.VOID, outcome="void: the question changed on disk")
    client = Client()
    assert fb.flush(lambda context: client, board) == [] and client.calls == []


@pytest.mark.parametrize("options, asked", [
    ([{"label": "Send it", "description": ""}, {"label": "Don't send", "description": ""}], True),
    ([{"label": "Send it"}, {"label": "Don't send"}], True),
    # Repeating the label shows every option twice in the dialog.
    ([{"label": "Send it", "description": "Send it"}, {"label": "Don't send", "description": ""}], False),
    ([{"label": "Send it", "description": "Recommended: also uploads your notes"}, {"label": "Don't send"}], False),
    ([{"label": "Send it", "preview": "anything"}, {"label": "Don't send"}], False),
])
def test_an_option_says_only_its_label(tmp_path, options, asked):
    binary, _log = _fake_probe(tmp_path)
    req = _hold()
    q = req.question
    out = _hook(tmp_path, {"hook_event_name": "PreToolUse", "tool_name": "AskUserQuestion", "session_id": SID,
                           "tool_input": {"questions": [{"header": q.header, "question": q.question,
                                                         "options": options}]}, "tool_use_id": "tu-opt"}, binary)
    denied = bool(out) and json.loads(out)["hookSpecificOutput"].get("permissionDecision") == "deny"
    assert denied is not asked


@pytest.mark.parametrize("extra", [{"description": "Note: answering yes also uploads your notes"}, {"preview": "x"}])
def test_a_probe_question_carries_nothing_beyond_its_words_and_options(tmp_path, extra):
    binary, _log = _fake_probe(tmp_path)
    q = _hold().question
    question = {"header": q.header, "question": q.question,
                "options": [{"label": q.yes_label}, {"label": q.no_label}], **extra}
    out = _hook(tmp_path, {"hook_event_name": "PreToolUse", "tool_name": "AskUserQuestion", "session_id": SID,
                           "tool_input": {"questions": [question]}, "tool_use_id": "tu-x"}, binary)
    assert json.loads(out)["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_a_title_around_a_probe_question_is_refused(tmp_path):
    binary, _log = _fake_probe(tmp_path)
    q = _hold().question
    out = _hook(tmp_path, {"hook_event_name": "PreToolUse", "tool_name": "AskUserQuestion", "session_id": SID,
                           "tool_input": {"title": "Approve to keep your work safe",
                                          "questions": [{"header": q.header, "question": q.question,
                                                         "options": [{"label": q.yes_label},
                                                                     {"label": q.no_label}]}]},
                           "tool_use_id": "tu-t"}, binary)
    assert json.loads(out)["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_an_agent_marker_alone_keeps_probe_approvals_from_answering(monkeypatch):
    """An older harness sets its marker without a session id."""
    import io

    import typer

    from probe.cli import daemon_cli

    class Terminal(io.StringIO):
        def isatty(self):
            return True

    _hold()
    monkeypatch.setenv("CLAUDECODE", "1")
    monkeypatch.setattr(sys, "stdin", Terminal())
    out = Terminal()
    monkeypatch.setattr(sys, "stdout", out)
    monkeypatch.setattr(typer, "prompt", lambda *a, **kw: (_ for _ in ()).throw(AssertionError("asked")))
    daemon_cli.approvals_cmd(list_only=False)
    assert "belongs to a coding agent" in out.getvalue() and "probe deny" in out.getvalue()


@pytest.mark.parametrize("list_only", [True, False])
def test_an_agents_listing_sends_both_answers_to_the_researchers_terminal(monkeypatch, list_only):
    """The daemon profile lets the agent list the questions and refuses its
    `probe deny`: "anyone may say no" read as an invitation it could not take."""
    import io

    from probe.cli import daemon_cli

    _hold()
    monkeypatch.setenv("CLAUDECODE", "1")
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", SID)
    out = io.StringIO()
    monkeypatch.setattr(sys, "stdout", out)
    daemon_cli.approvals_cmd(list_only=list_only)
    text = out.getvalue()
    assert "belongs to a coding agent" in text and "says no with `probe deny <id>` there" in text, text
    assert "anyone may say no" not in text and "answer in your own terminal" not in text


def test_the_note_audit_hook_finds_probe_as_the_other_hooks_do(tmp_path, monkeypatch):
    """`note_audit` shares `version_check._probe_bin`: PROBE_BIN first, a bare
    name looked up on PATH, and None when there is no `probe` at all."""
    import importlib.util

    path = HOOK.parent / "note_audit.py"
    spec = importlib.util.spec_from_file_location("_feedback_test_note_audit", path)
    note_audit = importlib.util.module_from_spec(spec)
    monkeypatch.syspath_prepend(str(HOOK.parent))
    spec.loader.exec_module(note_audit)
    binary, _log = _fake_probe(tmp_path)
    monkeypatch.setenv("PATH", str(binary.parent))
    monkeypatch.setenv("PROBE_BIN", "probe")
    assert note_audit._probe_bin() == str(binary)
    monkeypatch.setenv("PROBE_BIN", str(binary))
    assert note_audit._probe_bin() == str(binary)
    monkeypatch.delenv("PROBE_BIN")
    monkeypatch.setenv("PATH", str(tmp_path / "nowhere"))
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setattr(sys.modules["_probe_hooks.version_check"], "_PROBE_FALLBACKS", ())
    assert note_audit._probe_bin() is None


def test_kimis_question_shape_is_asked(tmp_path):
    """Kimi Code's question tool sends `multi_select` and option descriptions
    (its recorded payload): a Probe question in that shape is not refused."""
    fixture = Path(__file__).parent / "fixtures" / "kimi_code" / "hook_payloads" / "tui-ask-PreToolUse.json"
    recorded = json.loads(fixture.read_text())["tool_input"]["questions"][0]
    binary, _log = _fake_probe(tmp_path)
    q = _hold().question
    question = {**recorded, "header": q.header, "question": q.question,
                "options": [{"label": q.yes_label, "description": ""},
                            {"label": q.no_label, "description": ""}]}
    assert "multi_select" in question

    def decision(tool_input: dict) -> str | None:
        out = _hook(tmp_path, {"hook_event_name": "PreToolUse", "tool_name": "AskUserQuestion", "session_id": SID,
                               "tool_input": tool_input, "tool_use_id": "tu-kimi"}, binary)
        return json.loads(out)["hookSpecificOutput"].get("permissionDecision") if out else None

    assert decision({"questions": [question]}) != "deny"
    # The controls: the hook did find and check this question.
    assert decision({"questions": [{**question, "description": "a line under it"}]}) == "deny"
    assert decision({"questions": [question], "background": True}) == "deny"

