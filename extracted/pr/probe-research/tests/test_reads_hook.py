"""Claude Code delivery of the daemon's `[Probe]` messages (daemon reads, plan T3).

`plugins/probe-research/hooks/reads_hook.py` is stdlib-only and cannot import
`probe`, so it mirrors `probe.daemon.mailbox`. Every test here runs the hook the
way Claude Code does -- a subprocess with a real payload on stdin and the state
folder in XDG_STATE_HOME -- except the few that need a short waiter timeout,
which call it in-process. The parity tests publish with the real mailbox and
check the hook reads and renders those files exactly as the mailbox does.

Facts about Claude Code 2.1.283 these tests encode (re-checked 2026-09-28 on the
installed binary and in live sessions; see the CHANGELOG entry):
- a hook fired inside a helper agent carries `agent_id` (and `agent_type`); the
  main thread never does, and `transcript_path` is the MAIN transcript either way;
- every hook's environment has CLAUDE_CODE_SESSION_ATTENDED: "1" in an
  interactive session, "0" under `claude -p`, where an `asyncRewake` hook runs in
  the foreground and would hold the exit for its whole wait;
- `asyncRewake: true` backgrounds a hook; exit 2 wakes the model with stderr.
"""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

from probe.daemon import mailbox
from probe.daemon.mailbox import Kind

AGENT_ROOT = Path(__file__).resolve().parents[1]
PLUGIN = AGENT_ROOT / "plugins" / "probe-research"
HOOK = PLUGIN / "hooks" / "reads_hook.py"
SID = "11111111-2222-3333-4444-555555555555"
OTHER = "99999999-8888-7777-6666-555555555555"
HELPER = {"agent_id": "ad9edf1c958d1bebc", "agent_type": "general-purpose"}
#: The interpreter the hook runs under; point it at a Python 3.9 to check the
#: hook's floor (`PROBE_HOOK_PYTHON=$(uv python find 3.9) pytest ...`).
PY = os.environ.get("PROBE_HOOK_PYTHON") or sys.executable


@pytest.fixture(autouse=True)
def _state(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.delenv("PROBE_AGENT", raising=False)
    monkeypatch.delenv("CLAUDE_CODE_SESSION_ATTENDED", raising=False)


def _env(**extra: str) -> dict:
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": os.environ.get("HOME", "/tmp"),
           "XDG_STATE_HOME": os.environ["XDG_STATE_HOME"]}
    env.update(extra)
    return env


def _payload(event: str, sid: str = SID, **fields) -> str:
    body = {"hook_event_name": event, "session_id": sid, "cwd": "/tmp",
            "transcript_path": f"/home/u/.claude/projects/-tmp/{sid}.jsonl", "permission_mode": "default"}
    if event == "PostToolUse":
        body.update(tool_name="Bash", tool_input={"command": "ls"}, tool_response={"stdout": ""}, tool_use_id="t1")
    body.update(fields)
    return json.dumps(body)


def _start(event: str, sid: str = SID, env: "dict | None" = None, **fields) -> subprocess.Popen:
    proc = subprocess.Popen([PY, str(HOOK)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, env=_env(**(env or {})))
    proc.stdin.write(_payload(event, sid, **fields))
    proc.stdin.close()
    proc.stdin = None  # sent: `communicate` must not flush it again
    return proc


def _run(event: str, sid: str = SID, env: "dict | None" = None, **fields) -> subprocess.CompletedProcess:
    return subprocess.run([PY, str(HOOK)], input=_payload(event, sid, **fields), capture_output=True,
                          text=True, env=_env(**(env or {})), timeout=30)


def _context(result, event: str) -> "str | None":
    """The `additionalContext` a prompt / tool hook handed over (None: nothing)."""
    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    if not result.stdout:
        return None
    out = json.loads(result.stdout)
    assert set(out) == {"hookSpecificOutput"}
    assert out["hookSpecificOutput"]["hookEventName"] == event
    return out["hookSpecificOutput"]["additionalContext"]


def _msg(kind: str = Kind.MESSAGE, sid: str = SID, **kw) -> mailbox.Message:
    return mailbox.Message(id=kw.pop("id", mailbox.new_message_id()), session=sid, kind=kind, **kw)


def _answer(ask: str = "a1b2c3", text: str = "digits-sweep: best val_acc 0.989 at C=10 (run digits-7)", **kw):
    return _msg(Kind.ANSWER, ask=ask, question=kw.pop("question", "what did the last sweep find?"), text=text, **kw)


def _waiting_ids(sid: str = SID) -> list[str]:
    return [m.id for _, m in mailbox.waiting(sid)]


def _log(sid: str = SID) -> list[dict]:
    path = mailbox.claimed_dir(sid) / "log.jsonl"
    return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []


def _load():
    spec = importlib.util.spec_from_file_location("_reads_hook_under_test", HOOK)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------------------
# The prompt and after-tool-call hooks.
# ---------------------------------------------------------------------------


def test_a_prompt_delivers_every_answer_and_one_unasked_message():
    now = time.time()
    answer = _answer(made_at=now - 4)
    nothing = _msg(Kind.NOTHING, ask="a222222", question="any OOM on 8xA100?", made_at=now - 3)
    failed = _msg(Kind.FAILED, ask="a333333", question="who owns the eval?", reason="the Probe MCP refused the key",
                  made_at=now - 2)
    unasked = _msg(text="The team's `digits-sweep` already covered C in [0.1, 10].", made_at=now - 1)
    for m in (answer, nothing, failed, unasked):
        mailbox.publish(m)

    got = _context(_run("UserPromptSubmit", prompt="go on"), "UserPromptSubmit")

    assert got == "\n\n".join(m.rendered() for m in (answer, nothing, failed, unasked))
    assert _waiting_ids() == []
    assert sorted(e["id"] for e in _log()) == sorted(m.id for m in (answer, nothing, failed, unasked))
    assert {e["by"] for e in _log()} == {"UserPromptSubmit"}
    # And nothing is handed over twice.
    assert _context(_run("UserPromptSubmit", prompt="again"), "UserPromptSubmit") is None


def test_a_tool_call_delivers_an_answer_mid_turn():
    _context(_run("UserPromptSubmit", prompt="train it"), "UserPromptSubmit")
    answer = _answer()
    mailbox.publish(answer)
    got = _context(_run("PostToolUse"), "PostToolUse")
    assert got == answer.rendered()
    assert got.startswith('[Probe] Answer to your ask a1b2c3 ("what did the last sweep find?") - evidence')
    assert _log()[-1]["by"] == "PostToolUse"


def test_a_second_unasked_message_waits_for_the_next_turn():
    first = _msg(text="first: the LR sweep ran last week")
    mailbox.publish(first)
    assert _context(_run("UserPromptSubmit"), "UserPromptSubmit") == first.rendered()

    second = _msg(text="second: that sweep diverged above 1e-3")
    mailbox.publish(second)
    answer = _answer()
    mailbox.publish(answer)
    # Same turn: the answer goes out, the second unasked message waits.
    assert _context(_run("PostToolUse"), "PostToolUse") == answer.rendered()
    assert _context(_run("PostToolUse"), "PostToolUse") is None
    assert _waiting_ids() == [second.id]

    # The next prompt is a new turn.
    assert _context(_run("UserPromptSubmit"), "UserPromptSubmit") == second.rendered()
    assert _waiting_ids() == []


def test_a_tool_call_before_any_prompt_still_counts_one_unasked_message():
    """A plugin installed mid-session, or a resumed one: no turn token yet."""
    first, second = _msg(text="one"), _msg(text="two")
    mailbox.publish(first)
    assert _context(_run("PostToolUse"), "PostToolUse") == first.rendered()
    mailbox.publish(second)
    assert _context(_run("PostToolUse"), "PostToolUse") is None
    assert _context(_run("UserPromptSubmit"), "UserPromptSubmit") == second.rendered()


def test_old_turn_slots_are_cleared_when_a_new_turn_starts():
    for n in range(3):
        mailbox.publish(_msg(text=f"note {n}"))
        _context(_run("UserPromptSubmit"), "UserPromptSubmit")
    turns = mailbox.turn_path(SID).parent
    assert len(list(turns.glob(f"{SID}.unasked-*"))) == 1


def test_a_held_answer_waits_for_its_probe_ask_wait_then_goes_out_once_the_wait_is_gone():
    mailbox.touch_heartbeat(SID, "a1b2c3")
    answer = _answer(ask="a1b2c3")
    mailbox.publish(answer)
    assert _context(_run("PostToolUse"), "PostToolUse") is None
    assert _context(_run("UserPromptSubmit"), "UserPromptSubmit") is None
    assert _waiting_ids() == [answer.id]

    stale = time.time() - mailbox.HOLD_FRESH_S - 1
    os.utime(mailbox.heartbeat_path(SID, "a1b2c3"), (stale, stale))
    assert _context(_run("PostToolUse"), "PostToolUse") == answer.rendered()


def test_another_sessions_messages_are_never_delivered():
    theirs = _answer(sid=OTHER)
    mailbox.publish(theirs)
    mailbox.publish(_msg(sid=OTHER, text="for the other session"))
    assert _context(_run("UserPromptSubmit"), "UserPromptSubmit") is None
    assert _context(_run("PostToolUse"), "PostToolUse") is None
    assert len(_waiting_ids(OTHER)) == 2
    assert _log(OTHER) == []


def test_a_helper_agents_tool_call_never_claims():
    answer, unasked = _answer(), _msg(text="note for the main agent")
    mailbox.publish(answer)
    mailbox.publish(unasked)
    # Claude Code 2.1.283's marker: `agent_id` on a hook fired inside a subagent.
    assert _context(_run("PostToolUse", **HELPER), "PostToolUse") is None
    # Belt and braces: a transcript path inside a subagents folder.
    sub = f"/home/u/.claude/projects/-tmp/{SID}/subagents/agent-ad9edf1c958d1bebc.jsonl"
    assert _context(_run("PostToolUse", transcript_path=sub), "PostToolUse") is None
    assert sorted(_waiting_ids()) == sorted([answer.id, unasked.id])
    # The main agent's next tool call gets both.
    got = _context(_run("PostToolUse"), "PostToolUse")
    assert got == answer.rendered() + "\n\n" + unasked.rendered()


def test_expired_messages_are_skipped():
    old = time.time() - mailbox.UNASKED_TTL_S - 60
    stale = _msg(text="too old", made_at=old)
    mailbox.publish(stale)
    stale_answer = _answer(made_at=time.time() - mailbox.ANSWER_TTL_S - 60)
    mailbox.publish(stale_answer)
    assert _context(_run("UserPromptSubmit"), "UserPromptSubmit") is None
    assert _log() == []


def test_malformed_files_are_ignored_and_never_claimed():
    folder = mailbox.messages_dir(SID)
    folder.mkdir(parents=True)
    bad = {
        "00000000000000000001-bad1.json": "{not json",
        "00000000000000000002-bad2.json": "[]",
        "00000000000000000003-bad3.json": json.dumps({"id": "m1", "kind": "answer"}),  # no session
        "00000000000000000004-bad4.json": json.dumps({"id": "m2", "session": SID, "kind": "answer",
                                                       "question": 42, "ask": "a1"}),
        "00000000000000000005-bad5.json": json.dumps({"id": "m3", "session": SID, "kind": "answer",
                                                       "made_at": "yesterday"}),
    }
    for name, body in bad.items():
        (folder / name).write_text(body)
    good = _answer()
    mailbox.publish(good)
    assert _context(_run("UserPromptSubmit"), "UserPromptSubmit") == good.rendered()
    assert sorted(p.name for p in folder.glob("*.json")) == sorted(bad)
    # A payload that is not what Claude Code sends is ignored too.
    for body in ("not json", "[]", "{}", json.dumps({"hook_event_name": "PostToolUse", "session_id": 7})):
        result = subprocess.run([PY, str(HOOK)], input=body, capture_output=True, text=True,
                                env=_env(), timeout=30)
        assert (result.returncode, result.stdout, result.stderr) == (0, "", "")


def test_codex_gets_messages_at_prompts_and_after_tool_calls_but_no_wake():
    """Codex (plan T11): the same `additionalContext` delivery from the shared
    hooks.json; no rewake, so an open ask's answer waits for the next prompt or
    tool call. A 1,200-character unasked message sits under Codex's default
    additionalContext budget (thousands of characters); a longer answer spills to
    a file with a preview, as on Claude Code. Unverified live: this box's Codex
    trusts hooks per entry in the real ~/.codex (a temp CODEX_HOME runs none)."""
    codex = {"PROBE_AGENT": "codex", "CLAUDE_CODE_SESSION_ATTENDED": "1"}
    mailbox.write_ask(SID, "what did the last sweep find?")
    mailbox.publish(_answer(ask="aq1"))
    result = _run("Stop", env=codex)
    assert (result.returncode, result.stdout, result.stderr) == (0, "", ""), "no wake on Codex"
    assert "Answer to your ask aq1" in _context(_run("PostToolUse", env=codex), "PostToolUse")
    mailbox.publish(_msg(text="x" * 1200))
    assert _context(_run("UserPromptSubmit", env=codex), "UserPromptSubmit").startswith("[Probe] Team context")


def test_four_hooks_racing_deliver_each_message_once():
    for round_ in range(4):
        _context(_run("UserPromptSubmit"), "UserPromptSubmit")  # a fresh turn each round
        batch = [_answer(ask=f"a{round_}0000{n}", text=f"answer {round_}.{n}") for n in range(3)]
        batch.append(_msg(text=f"unasked {round_}"))
        for m in batch:
            mailbox.publish(m)
        procs = [_start("PostToolUse", tool_use_id=f"t{n}") for n in range(4)]
        outs = []
        for proc in procs:
            stdout, stderr = proc.communicate(timeout=30)
            assert proc.returncode == 0, stderr
            if stdout:
                outs.extend(json.loads(stdout)["hookSpecificOutput"]["additionalContext"].split("\n\n"))
        assert sorted(outs) == sorted(m.rendered() for m in batch)
        assert _waiting_ids() == []

    # Parallel tool calls in ONE turn: only one unasked message between them.
    _context(_run("UserPromptSubmit"), "UserPromptSubmit")
    mailbox.publish(_msg(text="one per turn"))
    procs = [_start("PostToolUse") for _ in range(4)]
    delivered = [p.communicate(timeout=30)[0] for p in procs]
    assert sum(1 for out in delivered if out) == 1
    mailbox.publish(_msg(text="the same turn: waits"))
    procs = [_start("PostToolUse") for _ in range(4)]
    assert [p.communicate(timeout=30)[0] for p in procs] == ["", "", "", ""]
    assert len(_waiting_ids()) == 1


# ---------------------------------------------------------------------------
# The Stop waiter (the wake).
# ---------------------------------------------------------------------------

ATTENDED = {"CLAUDE_CODE_SESSION_ATTENDED": "1"}


def test_the_waiter_wakes_the_agent_with_the_answer():
    ask = mailbox.write_ask(SID, "what LR did the last sweep use?")
    waiter = _start("Stop", env=ATTENDED, stop_hook_active=False, last_assistant_message="done")
    time.sleep(1.0)
    assert waiter.poll() is None, "the waiter must wait while the ask is open"
    answer = _answer(ask=ask.id, question=ask.question, text="lr=3e-4, from run digits-7")
    mailbox.publish(answer)
    stdout, stderr = waiter.communicate(timeout=15)
    assert waiter.returncode == 2
    assert stdout == ""
    assert stderr == answer.rendered()
    assert (_log()[-1]["id"], _log()[-1]["by"]) == (answer.id, "Stop")
    assert mailbox.open_asks(SID) == []


def test_the_waiter_takes_an_answer_already_waiting_at_once():
    ask = mailbox.write_ask(SID, "any OOM on 8xA100?")
    nothing = _msg(Kind.NOTHING, ask=ask.id, question=ask.question)
    mailbox.publish(nothing)
    started = time.monotonic()
    result = _run("Stop", env=ATTENDED)
    assert time.monotonic() - started < 5
    assert (result.returncode, result.stderr) == (2, nothing.rendered())


def test_the_waiter_exits_at_once_with_no_open_ask():
    mailbox.publish(_msg(text="an unasked message never wakes the agent"))
    started = time.monotonic()
    result = _run("Stop", env=ATTENDED)
    assert time.monotonic() - started < 5
    assert (result.returncode, result.stdout, result.stderr) == (0, "", "")
    assert len(_waiting_ids()) == 1


@pytest.mark.parametrize("attended", [None, "0"])
def test_the_waiter_never_waits_in_a_headless_session(attended):
    """Under `claude -p` an asyncRewake hook is not backgrounded: a wait would
    hold the exit (measured: an 8 s Stop hook added 8 s to `claude -p`)."""
    mailbox.write_ask(SID, "what LR?")
    env = {} if attended is None else {"CLAUDE_CODE_SESSION_ATTENDED": attended}
    started = time.monotonic()
    result = _run("Stop", env=env)
    assert time.monotonic() - started < 5
    assert (result.returncode, result.stdout, result.stderr) == (0, "", "")


def test_the_waiter_exits_quietly_when_a_new_prompt_arrives():
    mailbox.write_ask(SID, "what LR?")
    waiter = _start("Stop", env=ATTENDED)
    time.sleep(1.0)
    assert waiter.poll() is None
    _context(_run("UserPromptSubmit", prompt="never mind"), "UserPromptSubmit")
    stdout, stderr = waiter.communicate(timeout=10)
    assert (waiter.returncode, stdout, stderr) == (0, "", "")


def test_the_waiter_exits_quietly_when_someone_else_took_the_answer():
    ask = mailbox.write_ask(SID, "what LR?", wait=True)
    mailbox.touch_heartbeat(SID, ask.id)  # a `probe ask --wait` still waits: the waiter must not take it
    waiter = _start("Stop", env=ATTENDED)
    time.sleep(0.8)
    mailbox.publish(_answer(ask=ask.id))
    time.sleep(0.8)
    assert waiter.poll() is None
    assert mailbox.claim_answer(SID, ask.id) is not None  # the `--wait` took it
    stdout, stderr = waiter.communicate(timeout=10)
    assert (waiter.returncode, stdout, stderr) == (0, "", "")


def test_the_waiter_gives_up_at_its_ceiling_and_leaves_unasked_messages(monkeypatch):
    hook = _load()
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ATTENDED", "1")
    mailbox.write_ask(SID, "what LR?")
    unasked = _msg(text="unasked: never a wake")
    mailbox.publish(unasked)
    started = time.monotonic()
    assert hook.on_stop({"session_id": SID}, max_s=0.6, poll_s=0.1) == 0
    assert 0.5 < time.monotonic() - started < 5
    assert _waiting_ids() == [unasked.id]


def test_the_waiter_stops_before_its_hook_timeout():
    wiring = json.loads((PLUGIN / "hooks" / "claude-reads.json").read_text())["hooks"]
    hook = wiring["Stop"][0]["hooks"][0]
    assert hook["asyncRewake"] is True
    assert hook["timeout"] > _load().WAKE_MAX_S + 5


# ---------------------------------------------------------------------------
# Parity with probe.daemon.mailbox.
# ---------------------------------------------------------------------------


def _every_shape() -> list[mailbox.Message]:
    long_q = "which of the team's sweeps " + "over learning rate and batch size " * 6 + "diverged?"
    now = time.time()
    return [
        _msg(text="The team's `digits-sweep` covered C in [0.1, 10]; best 0.989.", made_at=now - 9),
        _answer(ask="a000001", question=long_q, text="three did: lr 1e-2, 3e-3, 1e-3", made_at=now - 8),
        _answer(ask="a000002", question="naïve Bayes baseline — ünïcode?", text="yes: 0.83 ✓", made_at=now - 7),
        _answer(ask="a000003", question=None, text="", made_at=now - 6),
        _msg(Kind.NOTHING, ask="a000004", question=long_q, made_at=now - 5),
        _msg(Kind.FAILED, ask="a000005", question="who owns eval?", reason="reader model failing twice",
             made_at=now - 4),
        _msg(Kind.FAILED, ask="a000006", question="q", reason=None, made_at=now - 3),
        _msg(Kind.ANSWER, ask="a000007", question="x" * 120, text="exactly at the cut", made_at=now - 2),
        _msg(Kind.ANSWER, ask="a000008", question="y" * 121, text="one past the cut", made_at=now - 1),
    ]


def test_the_hook_mirrors_the_mailbox_constants():
    hook = _load()
    assert hook.HOLD_FRESH_S == mailbox.HOLD_FRESH_S
    assert hook.ANSWER_TTL_S == mailbox.ANSWER_TTL_S
    assert hook.LABEL_QUESTION_CHARS == mailbox.LABEL_QUESTION_CHARS
    assert (hook.KIND_MESSAGE, hook.KIND_ANSWER, hook.KIND_NOTHING, hook.KIND_FAILED) == tuple(Kind)
    assert (hook.TEXT_MESSAGE, hook.TEXT_ANSWER, hook.TEXT_NOTHING, hook.TEXT_FAILED) == (
        mailbox.TEXT_MESSAGE, mailbox.TEXT_ANSWER, mailbox.TEXT_NOTHING, mailbox.TEXT_FAILED)


def test_published_files_render_exactly_as_the_mailbox_renders_them():
    hook = _load()
    shapes = _every_shape()
    # Unasked messages replace each other on publish: one of them, plus every end.
    for m in shapes:
        mailbox.publish(m)
    theirs = mailbox.waiting(SID)
    ours = hook.waiting(SID)
    assert [p for p, _ in ours] == [p for p, _ in theirs]
    assert [hook.rendered(m) for _, m in ours] == [m.rendered() for _, m in theirs]
    # ...and through the real hook, end to end.
    got = _context(_run("UserPromptSubmit"), "UserPromptSubmit")
    assert got == "\n\n".join(m.rendered() for _, m in theirs)


def test_open_asks_and_holds_read_the_same_as_the_mailbox():
    hook = _load()
    asks = [mailbox.write_ask(SID, f"question {n}", now=time.time() - 10 + n) for n in range(4)]
    mailbox.take_ask(SID, asks[1].id)
    mailbox.write_ask(SID, "too old", now=time.time() - mailbox.ANSWER_TTL_S - 5)
    mailbox.publish(_answer(ask=asks[2].id))
    mailbox.claim_answer(SID, asks[2].id)
    mailbox.touch_heartbeat(SID, asks[3].id)
    assert hook.open_asks(SID) == mailbox.open_asks(SID) == [asks[0].id, asks[1].id, asks[3].id]
    for a in asks:
        assert hook.held(SID, a.id) == mailbox.held(SID, a.id)
    assert hook._safe("../x y") == mailbox._safe("../x y")


# ---------------------------------------------------------------------------
# The wiring and the bash fast path.
# ---------------------------------------------------------------------------


def _reads_commands(path: Path, event: str) -> list[tuple[dict, dict]]:
    hooks = json.loads(path.read_text())["hooks"]
    return [(group, h) for group in hooks.get(event, []) for h in group["hooks"] if "reads_hook.py" in h["command"]]


def test_the_hooks_are_wired_where_claude_code_reads_them():
    shared = PLUGIN / "hooks" / "hooks.json"
    for event in ("UserPromptSubmit", "PostToolUse"):
        [(group, hook)] = _reads_commands(shared, event)
        assert hook["timeout"] == 5
        assert "matcher" not in group, "every tool call, every prompt"
    assert _reads_commands(shared, "Stop") == []  # asyncRewake is Claude Code's alone
    [(_, stop)] = _reads_commands(PLUGIN / "hooks" / "claude-reads.json", "Stop")
    assert stop["asyncRewake"] is True
    claude = json.loads((PLUGIN / ".claude-plugin" / "plugin.json").read_text())
    codex = json.loads((PLUGIN / ".codex-plugin" / "plugin.json").read_text())
    assert claude["hooks"] == "./hooks/claude-reads.json"
    assert "claude-reads" not in json.dumps(codex)


@pytest.fixture
def fake_python(tmp_path):
    """A `python3` first on PATH that only records it was started."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    marker = tmp_path / "python-started"
    script = bin_dir / "python3"
    script.write_text(f'#!/bin/sh\necho started >> "{marker}"\ncat > /dev/null\n')
    script.chmod(0o755)
    return bin_dir, marker


def _bash(command: str, bin_dir: Path, **env: str) -> subprocess.CompletedProcess:
    full = {"PATH": f"{bin_dir}:/usr/bin:/bin", "HOME": os.environ.get("HOME", "/tmp"),
            "XDG_STATE_HOME": os.environ["XDG_STATE_HOME"], "CLAUDE_PLUGIN_ROOT": str(PLUGIN), **env}
    return subprocess.run(["/bin/bash", "-c", command], input=_payload("PostToolUse"), capture_output=True,
                          text=True, env=full, timeout=30)


def _command(name: str, event: str) -> str:
    [(_, hook)] = _reads_commands(PLUGIN / "hooks" / name, event)
    return hook["command"]


@pytest.mark.parametrize("event", ["UserPromptSubmit", "PostToolUse"])
def test_the_fast_path_starts_no_python_while_nothing_waits(fake_python, event):
    bin_dir, marker = fake_python
    command = _command("hooks.json", event)

    assert _bash(command, bin_dir).returncode == 0  # no session id at all
    assert _bash(command, bin_dir, CLAUDE_CODE_SESSION_ID=SID).returncode == 0  # no folder
    mailbox.messages_dir(SID).mkdir(parents=True)
    assert _bash(command, bin_dir, CLAUDE_CODE_SESSION_ID=SID).returncode == 0  # empty folder
    mailbox.publish(_answer(sid=OTHER))
    assert _bash(command, bin_dir, CLAUDE_CODE_SESSION_ID=SID).returncode == 0  # another session's mail
    assert not marker.exists(), "python started with nothing waiting for this session"

    mailbox.publish(_answer())
    assert _bash(command, bin_dir, CLAUDE_CODE_SESSION_ID=SID).returncode == 0
    assert marker.read_text() == "started\n"
    assert _bash(command, bin_dir, CODEX_THREAD_ID=SID, PLUGIN_ROOT=str(PLUGIN)).returncode == 0
    assert marker.read_text() == "started\n" * 2


def test_a_prompt_with_nothing_waiting_still_starts_a_new_turn_in_the_shell(fake_python):
    """Found live (2.1.283): with the turn token written only by Python, a prompt
    with nothing waiting left the old token in place -- a Stop waiter kept
    waiting through the new turn, and the last turn's unasked slot stayed taken."""
    bin_dir, marker = fake_python
    prompt = _command("hooks.json", "UserPromptSubmit")
    assert _bash(prompt, bin_dir, CLAUDE_CODE_SESSION_ID=SID).returncode == 0
    assert not mailbox.turn_path(SID).parent.exists(), "no state for a session the reader never served"

    first, second = _msg(text="first"), _msg(text="second")
    mailbox.publish(first)
    assert _context(_run("PostToolUse"), "PostToolUse") == first.rendered()
    before = mailbox.turn_path(SID).read_text() if mailbox.turn_path(SID).exists() else None

    result = _bash(prompt, bin_dir, CLAUDE_CODE_SESSION_ID=SID)
    assert (result.returncode, result.stdout, result.stderr) == (0, "", "")
    assert not marker.exists(), "nothing waited: no python"
    token = mailbox.turn_path(SID).read_text()
    assert token.isdigit() and token != before

    mailbox.publish(second)
    assert _context(_run("PostToolUse"), "PostToolUse") == second.rendered()


def test_a_prompt_with_nothing_waiting_ends_the_waiter(fake_python):
    bin_dir, _ = fake_python
    mailbox.write_ask(SID, "what LR?")
    waiter = _start("Stop", env=ATTENDED)
    time.sleep(1.0)
    assert waiter.poll() is None
    assert _bash(_command("hooks.json", "UserPromptSubmit"), bin_dir, CLAUDE_CODE_SESSION_ID=SID).returncode == 0
    stdout, stderr = waiter.communicate(timeout=10)
    assert (waiter.returncode, stdout, stderr) == (0, "", "")
    assert mailbox.open_asks(SID) != []  # still open: its answer goes out at the next hook


def test_the_stop_fast_path_starts_no_python_without_an_ask_or_in_a_headless_session(fake_python):
    bin_dir, marker = fake_python
    command = _command("claude-reads.json", "Stop")
    base = {"CLAUDE_CODE_SESSION_ID": SID}

    assert _bash(command, bin_dir, **base, **ATTENDED).returncode == 0  # no ask
    ask = mailbox.write_ask(SID, "what LR?")
    assert _bash(command, bin_dir, **base).returncode == 0  # an ask, but headless (unset)
    assert _bash(command, bin_dir, **base, CLAUDE_CODE_SESSION_ATTENDED="0").returncode == 0
    assert not marker.exists()

    assert _bash(command, bin_dir, **base, **ATTENDED).returncode == 0
    assert marker.read_text() == "started\n"
    mailbox.take_ask(SID, ask.id)  # taken by the worker: still an ask the waiter can wait for
    assert _bash(command, bin_dir, **base, **ATTENDED).returncode == 0
    assert marker.read_text() == "started\n" * 2


def test_the_wrapper_runs_the_real_hook_with_the_payload(tmp_path):
    [(_, hook)] = _reads_commands(PLUGIN / "hooks" / "hooks.json", "PostToolUse")
    answer = _answer()
    mailbox.publish(answer)
    result = subprocess.run(["/bin/bash", "-c", hook["command"]], input=_payload("PostToolUse"), capture_output=True,
                            text=True, timeout=30,
                            env=_env(CLAUDE_CODE_SESSION_ID=SID, CLAUDE_PLUGIN_ROOT=str(PLUGIN) + "/"))
    assert _context(result, "PostToolUse") == answer.rendered()


# ---------------------------------------------------------------------------
# What the researcher is told (T9): one systemMessage per change of state.
# ---------------------------------------------------------------------------


def _notice(result) -> "str | None":
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout).get("systemMessage") if result.stdout else None


def _status(state: str, reason: str = "", since: float = 1.0) -> None:
    path = mailbox.status_path(SID)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"state": state, "reason": reason, "since": since}))


def _lease(reason: "str | None", expires_in: float = 200.0, state: str = "daemon") -> None:
    sessions = Path(os.environ["XDG_STATE_HOME"]) / "probe" / "sessions"
    sessions.mkdir(parents=True, exist_ok=True)
    (sessions / f"{SID}.state").write_text(state)
    (sessions / f"{SID}.writer").write_text(json.dumps(
        {"v": 1, "writer": "daemon", "pid": 1, "expires_at": time.time() + expires_in, "reason": reason}))


def test_the_researcher_lines_mirror_the_mailbox():
    hook = _load()
    assert hook.FAILURE_MESSAGES == {str(k): v for k, v in mailbox.FAILURE_MESSAGES.items()}
    assert set(hook.OUTAGES) == {str(s) for s in mailbox.OUTAGES}
    assert hook.DAEMON_STOPPED == mailbox.DAEMON_STOPPED


def test_a_reader_failure_is_shown_once_and_its_end_once():
    _status("ok")
    assert _notice(_run("UserPromptSubmit")) is None, "a healthy reader says nothing"
    _status("reader_failing", "RuntimeError: gateway 502")
    assert _notice(_run("PostToolUse")) == "Probe daemon's reader failing: RuntimeError: gateway 502."
    assert _notice(_run("PostToolUse")) is None, "once per change"
    assert _notice(_run("UserPromptSubmit")) is None
    _status("ok")
    assert _notice(_run("UserPromptSubmit")) == "Probe daemon is running again."
    assert _notice(_run("UserPromptSubmit")) is None


def test_each_stopped_turn_is_shown_and_needs_no_all_clear():
    _status("reader_turn_stopped", "8 model rounds", since=10.0)
    assert _notice(_run("PostToolUse")) == "Probe daemon's reader stopped a turn: 8 model rounds."
    _status("reader_turn_stopped", "8 model rounds", since=20.0)
    assert _notice(_run("PostToolUse")) == "Probe daemon's reader stopped a turn: 8 model rounds."
    _status("ok")
    assert _notice(_run("UserPromptSubmit")) is None, "a stopped turn is an event, not an outage"


def test_a_daemon_that_stopped_is_shown_and_a_quiet_release_is_not():
    _status("ok")
    _lease("gateway")
    assert _notice(_run("UserPromptSubmit")) == (
        "Probe daemon stopped: gateway. Recording and reads resume when it restarts.")
    _lease(None)
    assert _notice(_run("UserPromptSubmit")) == "Probe daemon is running again."
    _lease("handover")
    assert _notice(_run("UserPromptSubmit")) is None, "a resumed session's worker taking over"
    _lease(None, expires_in=-5)
    assert "not running" in _notice(_run("UserPromptSubmit"))
    _lease("gateway", state="full")
    assert _notice(_run("UserPromptSubmit")) == "Probe daemon is running again.", "not a daemon session"


def test_the_fast_path_starts_python_for_a_new_status_only(fake_python):
    bin_dir, marker = fake_python
    tool = _command("hooks.json", "PostToolUse")
    prompt = _command("hooks.json", "UserPromptSubmit")
    _status("ok")
    shown = mailbox.status_path(SID).with_suffix(".shown")
    assert _notice(_run("PostToolUse")) is None
    assert shown.read_text() == "ok|", "the hook writes the baseline itself, so the fast path goes quiet"
    os.utime(shown, (time.time() + 5, time.time() + 5))
    assert _bash(tool, bin_dir, CLAUDE_CODE_SESSION_ID=SID).returncode == 0
    assert not marker.exists(), "nothing new: no python after a tool call"
    _status("reader_failing", "x")
    os.utime(mailbox.status_path(SID), (time.time() + 10, time.time() + 10))
    assert _bash(tool, bin_dir, CLAUDE_CODE_SESSION_ID=SID).returncode == 0
    assert marker.read_text() == "started\n"
    assert _bash(prompt, bin_dir, CLAUDE_CODE_SESSION_ID=SID).returncode == 0
    assert marker.read_text() == "started\n" * 2, "a session the reader serves: every prompt checks"


def test_the_pi_extension_mirrors_the_mailbox_texts():
    """pi delivers from TypeScript (`probe-research-pi/src/core/reads.ts`); its
    copies of the texts are the mailbox's, word for word."""
    import re

    source = (AGENT_ROOT / "plugins" / "probe-research-pi" / "src" / "core" / "reads.ts").read_text()

    def ts(name: str) -> str:
        return json.loads(re.search(rf'export const {name} = ("(?:[^"\\]|\\.)*");', source).group(1))

    assert (ts("TEXT_MESSAGE"), ts("TEXT_ANSWER"), ts("TEXT_NOTHING"), ts("TEXT_FAILED")) == (
        mailbox.TEXT_MESSAGE, mailbox.TEXT_ANSWER, mailbox.TEXT_NOTHING, mailbox.TEXT_FAILED)
    assert (ts("KIND_MESSAGE"), ts("KIND_ANSWER"), ts("KIND_NOTHING"), ts("KIND_FAILED")) == tuple(Kind)
    lines = mailbox.FAILURE_MESSAGES
    assert ts("MSG_DAEMON_STOPPED") == lines[mailbox.DAEMON_STOPPED]
    assert ts("MSG_READER_FAILING") == lines[mailbox.Status.FAILING]
    assert ts("MSG_TURN_STOPPED") == lines[mailbox.Status.TURN_STOPPED]
    assert ts("MSG_READS_UNAVAILABLE") == lines[mailbox.Status.READS_UNAVAILABLE]
    assert ts("MSG_BACK_TO_NORMAL") == lines[mailbox.Status.OK]
    assert int(re.search(r"export const HOLD_FRESH_S = (\d+);", source).group(1)) == mailbox.HOLD_FRESH_S
    assert int(re.search(r"export const LABEL_QUESTION_CHARS = (\d+);", source).group(1)) == mailbox.LABEL_QUESTION_CHARS


def test_a_long_turn_gets_one_more_unasked_message_every_ten_minutes():
    """One unasked message per researcher turn, and one more per
    UNASKED_WINDOW_S of a long turn (Richard 2026-09-28): a one-prompt autonomous
    session must not lose every later finding and correction."""
    hook = _load()
    assert hook.UNASKED_WINDOW_S == mailbox.UNASKED_WINDOW_S == 600
    mailbox.publish(_msg(text="first"))
    assert "first" in _context(_run("UserPromptSubmit"), "UserPromptSubmit")
    mailbox.publish(_msg(text="second"))
    assert _context(_run("PostToolUse"), "PostToolUse") is None, "same window: it waits"
    turn = mailbox.turn_path(SID)
    started = time.time() - mailbox.UNASKED_WINDOW_S - 5
    os.utime(turn, (started, started))
    assert "second" in _context(_run("PostToolUse"), "PostToolUse"), "ten minutes into the turn: one more"
    mailbox.publish(_msg(text="third"))
    assert _context(_run("PostToolUse"), "PostToolUse") is None, "and only one per window"


def test_the_pi_extension_mirrors_the_unasked_window():
    import re

    source = (AGENT_ROOT / "plugins" / "probe-research-pi" / "src" / "core" / "reads.ts").read_text()
    assert int(re.search(r"export const UNASKED_WINDOW_S = (\d+);", source).group(1)) == mailbox.UNASKED_WINDOW_S


def test_codex_without_its_thread_id_in_the_hook_env_still_gets_its_messages(fake_python):
    """If Codex does not export CODEX_THREAD_ID to hooks, the fast path cannot
    key on the session: it starts Python whenever any message waits, and the
    hook reads the session from the payload."""
    bin_dir, marker = fake_python
    command = _command("hooks.json", "PostToolUse")
    assert _bash(command, bin_dir, PLUGIN_ROOT=str(PLUGIN)).returncode == 0
    assert not marker.exists(), "nothing waits anywhere: no python"
    mailbox.publish(_answer())
    assert _bash(command, bin_dir, PLUGIN_ROOT=str(PLUGIN)).returncode == 0
    assert marker.read_text() == "started\n"
    got = _context(_run("PostToolUse", env={"PROBE_AGENT": "codex"}), "PostToolUse")
    assert "Answer to your ask" in got, "the payload's session id is enough"


def test_a_codex_prompt_starts_a_new_turn_though_codex_passes_no_session_id(fake_python):
    """Codex puts the session id only in the payload, never in the hook's env
    (live Codex 0.158.0, 2026-09-29), so the shell cannot write the turn token
    and the one-per-turn pacing fell back to 10-minute windows. A prompt with
    no session id in env now starts Python whenever a reader has served a
    session here; the tool-call path is unchanged."""
    bin_dir, marker = fake_python
    prompt, tool = _command("hooks.json", "UserPromptSubmit"), _command("hooks.json", "PostToolUse")
    codex = {"PLUGIN_ROOT": str(PLUGIN)}
    assert _bash(prompt, bin_dir, **codex).returncode == 0
    assert not marker.exists(), "no reader ever ran here: no python"

    _status("ok")
    assert _bash(prompt, bin_dir, **codex).returncode == 0
    assert marker.read_text() == "started\n"
    assert _bash(tool, bin_dir, **codex).returncode == 0
    assert marker.read_text() == "started\n", "a tool call with nothing waiting still starts nothing"

    # The real hook, as Codex runs it: the payload names the session, the env does not.
    env = {"PATH": "/usr/bin:/bin", "HOME": os.environ.get("HOME", "/tmp"),
           "XDG_STATE_HOME": os.environ["XDG_STATE_HOME"], "PLUGIN_ROOT": str(PLUGIN)}
    before = mailbox.turn_path(SID).read_text() if mailbox.turn_path(SID).exists() else None
    done = subprocess.run(["/bin/bash", "-c", prompt], input=_payload("UserPromptSubmit", prompt="go"),
                          capture_output=True, text=True, env=env, timeout=30)
    assert done.returncode == 0, done.stderr
    token = mailbox.turn_path(SID).read_text()
    assert token and token != before


def test_the_woken_turn_is_the_same_turn_and_gets_no_second_unasked_message():
    """Live end-to-end test (Claude Code 2.1.283): the Stop waiter's wake runs
    through the prompt hook, which started a new turn and handed over another
    unasked message. The wake now leaves a marker; the prompt it causes keeps
    the turn (and its used unasked slot)."""
    first = _msg(text="first unasked")
    mailbox.publish(first)
    assert _context(_run("UserPromptSubmit"), "UserPromptSubmit") == first.rendered()
    token = mailbox.turn_path(SID).read_text()

    ask = mailbox.write_ask(SID, "what LR?")
    answer = _answer(ask=ask.id, question=ask.question)
    mailbox.publish(answer)
    assert _run("Stop", env=ATTENDED).returncode == 2  # the wake

    second = _msg(text="second unasked")
    mailbox.publish(second)
    assert _context(_run("UserPromptSubmit"), "UserPromptSubmit") is None, "the woken turn's slot is used"
    assert mailbox.turn_path(SID).read_text() == token

    # The researcher's next prompt is a new turn again.
    assert _context(_run("UserPromptSubmit"), "UserPromptSubmit") == second.rendered()
    assert mailbox.turn_path(SID).read_text() != token


def test_a_stale_wake_marker_does_not_swallow_a_new_turn():
    rh = _load()
    mailbox.write_ask(SID, "q")
    marker = mailbox.turn_path(SID).with_name(f"{SID}.woke")
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text("0")
    old = time.time() - rh.WOKE_PROMPT_S - 5
    os.utime(marker, (old, old))
    msg = _msg(text="for the new turn")
    mailbox.publish(msg)
    assert _context(_run("UserPromptSubmit"), "UserPromptSubmit") == msg.rendered()
    assert not marker.exists()
