"""The daemon's Kimi Code adapter against real Kimi Code 2.1.1 wires.

`fixtures/daemon_adapters/kimi_code/session{1,2,3}.jsonl` are the main wires of
three sessions in `fixtures/kimi_code/` (recorded against the scripted mock
model, so they hold no one's words), trimmed of two record types the adapter
never reads (`llm.tools_snapshot`, `profile.bind`: Kimi's tool schemas and system
prompt) and otherwise byte for byte:

    session1  `kimi -p` (auto mode), resumed: Bash + Write, thinking, two turns
    session2  the TUI (manual mode): AskUserQuestion answered, a Bash approval, a
              message typed mid-turn (queued, then its own turn), /compact
    session3  `kimi -p`: an Agent call that ran a helper agent (agent-0)
"""

from __future__ import annotations

import collections
import json
from pathlib import Path

import pytest

from probe.daemon import adapters
from probe.daemon.adapters.base import MODE_BYPASS, MODE_DEFAULT
from probe.daemon.events import Kind

FIXTURES = Path(__file__).parent / "fixtures"
WIRES = FIXTURES / "daemon_adapters" / "kimi_code"
SESSIONS = FIXTURES / "kimi_code" / "sessions" / "wd_proj_846899122802"


def _adapter():
    return adapters.for_source("kimi_code")


def _events(lines: list[bytes], stream: str = "main"):
    a = _adapter()
    out, off = [], 0
    for raw in lines:
        off += len(raw) + 1
        out.extend(a.parse_bytes(raw, stream=stream, offset=off))
    return out


def _wire(n: int) -> list[bytes]:
    return (WIRES / f"session{n}.jsonl").read_bytes().splitlines()


def _records(n: int) -> list[dict]:
    return [json.loads(raw) for raw in _wire(n)]


def _line(obj: dict) -> bytes:
    return json.dumps(obj).encode()


def test_the_fixtures_are_the_recorded_wires_trimmed_only():
    """Every line of a fixture is a line of the real wire, unchanged and in order."""
    sources = {1: "session_9b40c4c4-d58a-4ed7-9372-cfecf8469b05", 2: "session_0d2f2223-e34e-4cd1-87e3-b8d8d39aa229",
               3: "session_e240efe5-da6a-4407-9c61-91d8a3a53d24"}
    for n, sid in sources.items():
        real = (SESSIONS / sid / "agents" / "main" / "wire.jsonl").read_bytes().splitlines()
        dropped = [r for r in real if json.loads(r)["type"] in ("llm.tools_snapshot", "profile.bind")]
        assert [r for r in real if r not in dropped] == _wire(n)


@pytest.mark.parametrize("n,expected", [
    (1, {Kind.PROMPT: 2, Kind.TOOL_CALL: 3, Kind.TOOL_OUTPUT: 3, Kind.AGENT_REASONING: 5, Kind.AGENT_TEXT: 5,
         Kind.META: 3, Kind.TURN_END: 2}),
    (2, {Kind.PROMPT: 2, Kind.TOOL_CALL: 2, Kind.TOOL_OUTPUT: 2, Kind.AGENT_REASONING: 4, Kind.AGENT_TEXT: 4,
         Kind.META: 1, Kind.TURN_END: 2, Kind.COMPACTION: 1}),
    (3, {Kind.PROMPT: 1, Kind.TOOL_CALL: 1, Kind.TOOL_OUTPUT: 1, Kind.AGENT_REASONING: 2, Kind.AGENT_TEXT: 2,
         Kind.META: 2, Kind.TURN_END: 1}),
])
def test_one_record_family_is_read_so_nothing_is_doubled(n, expected):
    """The wire repeats each message whole in `agent.message.appended`; only the
    context family is read: one event per prompt, part, call and result."""
    events = _events(_wire(n))
    assert collections.Counter(e.kind for e in events) == expected
    records = _records(n)
    loop = [r["event"] for r in records if r["type"] == "context.append_loop_event"]
    assert sum(1 for ev in loop if ev["type"] == "tool.call") == expected[Kind.TOOL_CALL]
    calls = [e.call_id for e in events if e.kind == Kind.TOOL_CALL]
    outputs = [e.call_id for e in events if e.kind == Kind.TOOL_OUTPUT]
    assert len(set(calls)) == len(calls) and sorted(calls) == sorted(outputs)
    assert sum(1 for r in records if r["type"] == "turn.ended") == expected[Kind.TURN_END]
    # The other family is all there, and none of it is read.
    whole = [r for r in records if r.get("kind") == "event"]
    assert whole and _events([_line(r) for r in whole]) == []


def test_prompts_are_what_the_researcher_typed_and_the_rest_is_meta():
    events = _events(_wire(2))
    prompts = [e.text for e in events if e.kind == Kind.PROMPT]
    # The second was typed while the first turn ran: queued, then a turn of its own.
    assert prompts == ["ASK ;; RUN: sleep 12; echo slept ;; SAY: Sweep starts from your pick.",
                       "also log the val loss please"]
    for n in (1, 2, 3):
        for e in _events(_wire(n)):
            if e.kind == Kind.META:
                assert e.text.startswith("<system-reminder>"), e.text  # Kimi's injections


@pytest.mark.parametrize("origin", [
    {"kind": "injection", "variant": "permission_mode"},
    {"kind": "hook_result", "event": "UserPromptSubmit"},
    {"kind": "system_trigger", "name": "stop_hook"},
    {"kind": "skill_activation", "trigger": "user-slash"},
    None,
])
def test_a_user_message_kimi_or_a_hook_made_is_not_a_prompt(origin):
    message = {"role": "user", "content": [{"type": "text", "text": "[Probe] Answer to your ask a1"}]}
    if origin is not None:
        message["origin"] = origin
    [ev] = _events([_line({"type": "context.append_message", "agentId": "main", "message": message})])
    assert ev.kind == Kind.META


def test_a_message_steered_into_the_running_turn_is_one_prompt():
    """Kimi 2.1.1's steer, as its source writes it (`turn.steer`, `prompt.steered`,
    then the message itself with origin "user"; not recorded in a run): ONE
    prompt, from the message, never also from the steer records."""
    content = [{"type": "text", "text": "stop - use lr 1e-4 instead"}]
    lines = [
        _line({"type": "prompt.steered", "agentId": "main", "activePromptId": "msg_A", "promptIds": ["msg_B"],
               "content": content, "steeredAt": "2026-10-05T03:12:00.000Z", "messageId": "msg_B",
               "time": 1791169930000}),
        _line({"type": "turn.steer", "agentId": "main", "input": content, "origin": {"kind": "user"},
               "messageId": "msg_B", "promptIds": ["msg_B"], "turnId": 0, "time": 1791169930001}),
        _line({"type": "context.append_message", "agentId": "main", "message": {
            "role": "user", "content": content, "id": "msg_B", "toolCalls": [],
            "origin": {"kind": "user", "inTurn": True}}, "time": 1791169930002}),
    ]
    events = _events(lines)
    assert [(e.kind, e.text) for e in events] == [(Kind.PROMPT, "stop - use lr 1e-4 instead")]
    assert events[0].ts == "2026-10-05T03:12:10.002Z"


def test_tool_calls_carry_name_and_args_and_results_carry_output_and_errors():
    events = _events(_wire(1))
    bash, write, ls = [e for e in events if e.kind == Kind.TOOL_CALL]
    assert (bash.tool, bash.command(), bash.call_id) == ("Bash", "echo hello-from-kimi", "call_1")
    assert bash.cwd == "/home/researcher/kimi-fixture/proj"
    assert write.tool == "Write" and write.tool_input == {"path": "notes.txt", "content": "lr sweep notes"}
    outputs = {e.call_id: e for e in events if e.kind == Kind.TOOL_OUTPUT}
    assert outputs["call_1"].text == "hello-from-kimi\n" and not outputs["call_1"].is_error
    assert outputs["call_2"].text == "Wrote 14 bytes to notes.txt"
    # A Write a PreToolUse hook denied (recorded in the facts run, 2026-10-05).
    denied = _line({"type": "context.append_loop_event", "agentId": "main", "event": {
        "type": "tool.result", "parentUuid": "947d0047-72f0-480b-9cb4-ee6534106ae3", "toolCallId": "call_3",
        "result": {"output": "WRITE-DENIED-BY-HOOK", "isError": True, "durationMs": 1}}})
    [ev] = _events([denied])
    assert (ev.kind, ev.text, ev.is_error, ev.call_id) == (Kind.TOOL_OUTPUT, "WRITE-DENIED-BY-HOOK", True, "call_3")
    # Output as content parts: their text, never an image's data.
    parts = _line({"type": "context.append_loop_event", "agentId": "main", "event": {
        "type": "tool.result", "toolCallId": "call_4", "result": {"output": [
            {"type": "text", "text": "plot.png"},
            {"type": "image_url", "imageUrl": {"url": "data:image/png;base64," + "A" * 5000}}]}}})
    [ev] = _events([parts])
    assert ev.text == "plot.png"


def test_the_question_tool_and_its_answer_are_read():
    events = _events(_wire(2))
    [ask] = [e for e in events if e.kind == Kind.TOOL_CALL and e.tool == _adapter().question_tool_name]
    assert ask.tool_input["questions"][0]["question"] == "Which learning rate should the sweep start from?"
    [answer] = [e for e in events if e.kind == Kind.TOOL_OUTPUT and e.call_id == ask.call_id]
    assert json.loads(answer.text) == {"answers": {"Which learning rate should the sweep start from?": "1e-3"}}


def test_thinking_is_reasoning():
    reasoning = [e.text for e in _events(_wire(1)) if e.kind == Kind.AGENT_REASONING]
    assert reasoning[:2] == ["Run: echo hello-from-kimi", "Write notes.txt"]


def test_compaction_and_clear_are_compactions():
    [compaction] = [e for e in _events(_wire(2)) if e.kind == Kind.COMPACTION]
    assert compaction.text == "Hello from the mock model."  # the summary Kimi kept
    [cleared] = _events([_line({"type": "context.clear", "agentId": "main", "time": 1791169950000})])
    assert cleared.kind == Kind.COMPACTION and "cleared" in cleared.text


@pytest.mark.parametrize("mode,expected", [("auto", MODE_BYPASS), ("manual", MODE_DEFAULT),
                                           ("yolo", MODE_DEFAULT), ("plan", MODE_DEFAULT), ("", None),
                                           (None, None)])
def test_only_auto_mode_is_bypass(mode, expected):
    assert _adapter().permission_mode({"type": "permission.set_mode", "agentId": "main", "mode": mode}) == expected
    assert _adapter().permission_mode({"type": "turn.prompt", "mode": "auto"}) is None


def test_the_recorded_modes():
    a = _adapter()
    modes = {n: [a.permission_mode(r) for r in _records(n) if a.permission_mode(r)] for n in (1, 2, 3)}
    assert modes == {1: [MODE_BYPASS], 2: [MODE_DEFAULT], 3: [MODE_BYPASS]}


def test_helper_agent_wires_are_not_read():
    """The helper agent's wire sits beside the main one; only the main wire is input."""
    main = SESSIONS / "session_e240efe5-da6a-4407-9c61-91d8a3a53d24" / "agents" / "main" / "wire.jsonl"
    assert (main.parent.parent / "agent-0" / "wire.jsonl").is_file()
    files = _adapter().session_files(main)
    assert files.main == main and files.subagents == []
    assert not _adapter().capabilities.subagent_logs
    # Its spawn records on the main wire add nothing: the Agent call and its result say it.
    spawned = [r for r in _records(3) if r["type"].startswith("subagent.")]
    assert len(spawned) == 3 and _events([_line(r) for r in spawned]) == []


def test_the_instruction_files_kimi_reads(tmp_path, monkeypatch):
    home = tmp_path / "home"
    repo = home / "repo"
    work = repo / "train"
    (repo / ".git").mkdir(parents=True)
    work.mkdir()
    for path in (repo / "AGENTS.md", repo / ".kimi-code" / "AGENTS.md", work / "AGENTS.md",
                 home / ".kimi-code" / "AGENTS.md", home / ".kimi-code" / "config.toml"):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("x")
    monkeypatch.delenv("KIMI_CODE_HOME", raising=False)
    found = {f.path for f in _adapter().context_files(work, home)}
    assert found == {work / "AGENTS.md", repo / "AGENTS.md", repo / ".kimi-code" / "AGENTS.md",
                     home / ".kimi-code" / "AGENTS.md"}
    moved = tmp_path / "kimi-home"
    moved.mkdir()
    (moved / "AGENTS.md").write_text("x")
    monkeypatch.setenv("KIMI_CODE_HOME", str(moved))
    found = {f.path for f in _adapter().context_files(work, home)}
    assert moved / "AGENTS.md" in found and home / ".kimi-code" / "AGENTS.md" not in found
