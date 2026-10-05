"""Kimi Code capture: real 2.1.1 wires -> the shared Claude Code event shape.

Every wire here was written by the real Kimi Code CLI against the scripted
mock model (tests/fixtures/kimi_code/README.md). The sanitizer reads ONE of
the wire's two record families (the engine's `context.*` records), so each
assertion below also pins that nothing arrives twice.
"""

from __future__ import annotations

import json
import shutil
from contextlib import closing
from pathlib import Path

import pytest

from probe.tap_core import kimi_sanitize
from probe.tap_core import session_journal as sj
from tests.test_backfill_transcripts_upload import FakeWire

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "kimi_code"
SESSIONS = FIXTURES / "sessions" / "wd_proj_846899122802"
RUN_WRITE = SESSIONS / "session_9b40c4c4-d58a-4ed7-9372-cfecf8469b05"  # print mode, resumed
SUBAGENT = SESSIONS / "session_e240efe5-da6a-4407-9c61-91d8a3a53d24"
TUI = SESSIONS / "session_0d2f2223-e34e-4cd1-87e3-b8d8d39aa229"  # ask, queued message, /compact

#: Recorded from the real Kimi Code 2.1.1 CLI (`kimi -p "RUN: echo hi"` against
#: tests/kimi_mock, with a config `[[hooks]]` UserPromptSubmit entry running
#: `echo PROBE-HOOK-CONTEXT-LINE`): the hook's stdout, which Kimi injects as a
#: user-role message. None of the four fixture sessions has one.
HOOK_RESULT_LINE = (
    '{"type":"context.append_message","agentId":"main","message":{"role":"user",'
    '"content":[{"type":"text","text":"<hook_result hook_event=\\"UserPromptSubmit\\">\\n'
    'PROBE-HOOK-CONTEXT-LINE\\n</hook_result>"}],"toolCalls":[],'
    '"origin":{"kind":"hook_result","event":"UserPromptSubmit"}},"time":1791170640485}'
)


def _records(session: Path, agent: str = "main") -> list[dict]:
    wire = session / "agents" / agent / "wire.jsonl"
    return [json.loads(line) for line in wire.read_text(encoding="utf-8").splitlines() if line]


def _sanitized(session: Path, agent: str = "main") -> list[dict]:
    out = []
    for record in _records(session, agent):
        event = kimi_sanitize.sanitize_event(record)
        if event is not None:
            out.extend(event if isinstance(event, list) else [event])
    return out


def _blocks(events: list[dict], role: str, kind: str) -> list[dict]:
    return [
        block
        for event in events
        if event["type"] == role
        for block in event["message"]["content"]
        if block["type"] == kind
    ]


def _user_texts(events: list[dict]) -> list[str]:
    return [b["text"] for b in _blocks(events, "user", "text")]


def test_user_prompts_are_the_researcher_s_words_once_each() -> None:
    events = _sanitized(RUN_WRITE)
    assert _user_texts(events) == [
        "RUN: echo hello-from-kimi\nWRITE: notes.txt :: lr sweep notes\nSAY: Both steps ran.",
        "RUN: ls\nSAY: Listed.",  # the resumed leg, appended to the same wire
    ]


def test_assistant_text_and_thinking_arrive_once_in_order() -> None:
    events = _sanitized(RUN_WRITE)
    texts = [b["text"] for b in _blocks(events, "assistant", "text")]
    thinking = [b["thinking"] for b in _blocks(events, "assistant", "thinking")]
    # Each also sits in an `agent.message.appended` record; reading one family
    # is what keeps these from doubling.
    assert texts == [
        "Running a command.", "Writing a file.", "Both steps ran.", "Running a command.", "Listed.",
    ]
    assert thinking == [
        "Run: echo hello-from-kimi", "Write notes.txt", "Every step ran; wrap up.",
        "Run: ls", "Every step ran; wrap up.",
    ]
    assert all(set(b) == {"type", "thinking"} for b in _blocks(events, "assistant", "thinking"))


def test_tool_calls_carry_a_summary_and_counts_never_content() -> None:
    events = _sanitized(RUN_WRITE)
    calls = _blocks(events, "assistant", "tool_use")
    assert [(c["id"], c["name"], c.get("summary")) for c in calls] == [
        ("call_1", "Bash", "echo hello-from-kimi"),
        ("call_2", "Write", "notes.txt"),
        ("call_7", "Bash", "ls"),
    ]
    write = calls[1]
    assert write["stats"] == {"op": "write", "added_lines": 1, "added_bytes": 14}
    # The prompt names the content; the call that wrote it must not carry it.
    assert "lr sweep notes" not in json.dumps(calls), "the written file's content left the machine"
    assert set(write) == {"type", "id", "name", "summary", "stats"}


def test_tool_results_carry_size_and_never_output() -> None:
    events = _sanitized(RUN_WRITE)
    results = _blocks(events, "user", "tool_result")
    assert [r["tool_use_id"] for r in results] == ["call_1", "call_2", "call_7"]
    assert results[0]["result_bytes"] == len("hello-from-kimi\n")
    # Exactly these keys: no output, no note, no duration.
    assert all(set(r) == {"type", "tool_use_id", "result_bytes"} for r in results)
    # A tool result rides alone in its own user event, never inside a prompt.
    for event in events:
        kinds = {b["type"] for b in event.get("message", {}).get("content", [])}
        assert not ("tool_result" in kinds and len(kinds) > 1)


def test_a_message_typed_mid_turn_is_one_prompt() -> None:
    events = _sanitized(TUI)
    assert _user_texts(events) == [
        "ASK ;; RUN: sleep 12; echo slept ;; SAY: Sweep starts from your pick.",
        "also log the val loss please",
    ]


def test_compaction_becomes_one_system_event_with_its_summary() -> None:
    events = _sanitized(TUI)
    compactions = [e for e in events if e["type"] == "system" and e["subtype"] == "compaction"]
    assert len(compactions) == 1
    assert compactions[0]["content"] == "Hello from the mock model."
    assert compactions[0]["_kimi_extras"]["compacted_count"] == 9
    # The model-facing preamble around the summary is not shipped.
    assert "compacted to free up context" not in json.dumps(events)


def test_injected_user_role_text_is_not_a_researcher_prompt() -> None:
    records = _records(TUI)
    injected = [
        r for r in records
        if r.get("type") == "context.append_message"
        and r["message"]["origin"]["kind"] == "injection"
    ]
    assert injected, "the fixture lost its system reminders; this test would prove nothing"
    assert all(kimi_sanitize.sanitize_event(r) is None for r in injected)
    events = _sanitized(TUI)
    assert "<system-reminder>" not in json.dumps(events)


def test_hook_output_kimi_injects_is_not_a_researcher_prompt() -> None:
    assert kimi_sanitize.sanitize_event(json.loads(HOOK_RESULT_LINE)) is None


def test_a_subagent_s_trigger_is_not_a_researcher_prompt() -> None:
    triggers = [
        r for r in _records(SUBAGENT, "agent-0")
        if r.get("type") == "context.append_message"
        and r["message"]["origin"]["kind"] == "system_trigger"
    ]
    assert triggers, "the fixture lost the subagent's prompt"
    assert all(kimi_sanitize.sanitize_event(r) is None for r in triggers)


def test_a_skill_activation_ships_its_name_never_its_body() -> None:
    # Built from a real user-role record: only `origin` differs, set to the
    # shape Kimi 2.1.1's Skill tool writes (no fixture session loads a skill).
    record = json.loads(HOOK_RESULT_LINE)
    record["message"]["content"] = [{"type": "text", "text": "SKILL BODY: never ship me"}]
    record["message"]["origin"] = {
        "kind": "skill_activation", "activationId": "a1", "skillName": "track-work",
        "trigger": "model-tool", "skillType": "inline", "skillPath": "/x/SKILL.md",
    }
    event = kimi_sanitize.sanitize_event(record)
    assert event["type"] == "system" and event["subtype"] == "skill_activation"
    assert event["_kimi_extras"] == {"skill_name": "track-work", "trigger": "model-tool"}
    assert "never ship me" not in json.dumps(event)


def test_the_main_wire_keeps_the_subagent_call_and_result_only() -> None:
    events = _sanitized(SUBAGENT)
    calls = _blocks(events, "assistant", "tool_use")
    assert [(c["name"], c.get("summary")) for c in calls] == [("Agent", "quick check")]
    assert len(_blocks(events, "user", "tool_result")) == 1
    assert _user_texts(events) == ["SUB\nSAY: The subagent replied."]
    # The subagent's own prompt and reply live in agents/agent-0 only.
    assert "Reply with ok." not in json.dumps(events)


def test_ui_records_and_bookkeeping_are_dropped() -> None:
    dropped = {
        r["type"] for r in _records(TUI) if kimi_sanitize.sanitize_event(r) is None
    }
    assert {"agent.message.appended", "profile.bind", "llm.request", "usage.record",
            "permission.set_mode", "interaction.request", "turn.prompt"} <= dropped
    events = _sanitized(TUI)
    assert "You are Kimi Code CLI" not in json.dumps(events), "the system prompt left the machine"


def test_timestamps_are_iso_utc() -> None:
    first_prompt = next(e for e in _sanitized(TUI) if e["type"] == "user")
    assert first_prompt["timestamp"] == "2026-10-05T03:11:53.462Z"


def test_non_objects_and_unknown_records_fail_closed() -> None:
    assert kimi_sanitize.sanitize_event(["a", "list"]) is None
    assert kimi_sanitize.sanitize_event("text") is None
    assert kimi_sanitize.sanitize_event({"type": "goal.started", "secret": "x"}) is None


@pytest.fixture
def journal_dir(tmp_path, monkeypatch):
    monkeypatch.setenv("PROBE_TRANSCRIPT_STATE_DIR", str(tmp_path / "state"))
    return tmp_path


def _copy_wire(tmp_path: Path, session: Path) -> Path:
    target = tmp_path / "sessions" / "wd_proj_x" / session.name / "agents" / "main" / "wire.jsonl"
    target.parent.mkdir(parents=True)
    shutil.copy(session / "agents" / "main" / "wire.jsonl", target)
    return target


def test_a_torn_last_line_is_not_consumed_until_it_is_complete(journal_dir) -> None:
    """Kimi appends whole records; a half-written last line is still being
    written (or will be repaired), so the journal stops before it."""
    path = _copy_wire(journal_dir, RUN_WRITE)
    whole = path.read_bytes()
    lines = whole.splitlines(keepends=True)
    last_prompt = next(
        i for i, line in enumerate(lines) if b'"RUN: ls' in line and b"context.append_message" in line
    )
    complete = b"".join(lines[:last_prompt])
    path.write_bytes(complete + lines[last_prompt][:40])  # torn mid-record, no newline

    session_id = "9b40c4c4-d58a-4ed7-9372-cfecf8469b05"
    wire = FakeWire(source="kimi_code")
    with closing(sj.Journal(wire.base_url, "synthetic", "kimi_code")) as journal:
        journal.ensure(session_id, path, wire.receipts(session_id), historical=False, cwd="/w")
        body = json.loads(journal.stage(session_id, cwd="/w"))
        assert body["source_byte_end"] == len(complete)
        texts = [
            b.get("text") for e in body["events"] for b in e["raw"].get("message", {}).get("content", [])
        ]
        assert "RUN: ls\nSAY: Listed." not in texts
        journal.deliver(session_id, wire)

        path.write_bytes(whole)  # the record is finished
        body = json.loads(journal.stage(session_id, cwd="/w"))
        assert body["source_byte_start"] == len(complete)
        texts = [
            b.get("text") for e in body["events"] for b in e["raw"].get("message", {}).get("content", [])
        ]
        assert "RUN: ls\nSAY: Listed." in texts


# --- privacy branches the fixtures do not reach (review, 2026-10-05) --------
# Shapes read from Kimi Code 2.1.1's source (origin kinds plugin_command and
# shell_command); a regression here would ship text the shared shape drops.


def _user_line(origin: dict, text: str) -> dict:
    return {"type": "context.append_message", "agentId": "main", "time": 1791170640485,
            "message": {"role": "user", "content": [{"type": "text", "text": text}], "origin": origin}}


def test_a_plugin_command_ships_its_typed_line_never_its_expanded_body() -> None:
    event = kimi_sanitize.sanitize_event(_user_line(
        {"kind": "plugin_command", "pluginId": "probe-research", "commandName": "probe", "commandArgs": "off"},
        "EXPANDED-COMMAND-BODY-SECRET instructions the plugin injected",
    ))
    text = json.dumps(event)
    assert "/probe-research:probe off" in text
    assert "EXPANDED-COMMAND-BODY-SECRET" not in text


def test_a_shell_command_s_output_ships_as_a_size_only() -> None:
    typed = kimi_sanitize.sanitize_event(_user_line({"kind": "shell_command", "phase": "input"}, "ls -la"))
    assert "ls -la" in json.dumps(typed)
    output = kimi_sanitize.sanitize_event(_user_line(
        {"kind": "shell_command", "phase": "output", "isError": True}, "SHELL-OUTPUT-SECRET token=abc"))
    text = json.dumps(output)
    assert "SHELL-OUTPUT-SECRET" not in text
    assert '"result_bytes": 29' in text and '"is_error": true' in text
