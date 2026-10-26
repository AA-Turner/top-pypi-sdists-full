"""probe-events/1: what the four tap sanitizers upload, pinned.

`src/probe/tap_core/probe-events-1.schema.json` is the contract. The engine
(prbe-knowledge) renders and builds its ATIF trajectories from these events,
so a change here is a change to what every reader downstream receives.

GOLDENS: `tests/fixtures/probe_events/<harness>/raw.jsonl` -> `expected.jsonl`,
one sanitizer output per raw line, as JSON: `null` when the line is dropped, a
list when one line becomes several events (pi's bashExecution). After an
INTENDED change, regenerate and review the diff:

    PROBE_EVENTS_REGEN=1 pytest tests/test_probe_events_contract.py

Where each raw.jsonl comes from (no real customer or machine content):
  claude_code  synthetic, shaped like real Claude Code 2.x lines (keys and
               nesting checked against real transcripts, every word invented),
               with markers planted wherever file content or tool output sits
  codex        tests/fixtures/rollout-sample.jsonl of the tap plugin (a real
               "say hello" session) with one `token_usage_record` in the
               shape Codex 0.160-0.164 writes, then a synthetic continuation
               covering the tool, image, compaction and dropped variants
  pi           a real pi session from the tap plugin's fixtures/pi/, then a
               synthetic tail: both bashExecution shapes, compaction, branch
               summary, label, custom entries and a fork's unknown entry type
  kimi_code    tests/fixtures/kimi_code's resumed print-mode session (mock
               model) trimmed to the record families the sanitizer reads plus
               one of each it drops, its sibling session's compaction, then
               synthetic shell / plugin / skill / undo / clear records
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft202012Validator

from probe.tap_core import codex_sanitize, kimi_sanitize, pi_sanitize, sanitize
from probe.tap_core.sanitize import CallModels, call_models
from tests.test_capture_privacy import _HARNESS_FIXTURES

_AGENT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = _AGENT / "src" / "probe" / "tap_core" / "probe-events-1.schema.json"
GOLDENS = _AGENT / "tests" / "fixtures" / "probe_events"
SANITIZERS = {
    "claude_code": sanitize,
    "codex": codex_sanitize,
    "pi": pi_sanitize,
    "kimi_code": kimi_sanitize,
}
VALIDATOR = Draft202012Validator(json.loads(SCHEMA_PATH.read_text()))


def _lines(path: Path) -> list[Any]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def _events(output: Any) -> list[Any]:
    return output if isinstance(output, list) else [] if output is None else [output]


def _read_file(module: Any, lines: list[Any]) -> list[Any]:
    """Each line's output, read in order as one file (the journal's
    `call_models` memory, which a usage line's model comes from)."""
    with call_models(CallModels()):
        return [module.sanitize_event(line) for line in lines]


def _assert_valid(event: Any, where: str) -> None:
    errors = sorted(VALIDATOR.iter_errors(event), key=lambda e: list(e.absolute_path))
    assert not errors, f"{where}: " + "; ".join(
        f"{'/'.join(map(str, e.absolute_path))}: {e.message[:160]}" for e in errors[:5]
    )


def test_the_schema_is_a_valid_draft_2020_12_schema() -> None:
    Draft202012Validator.check_schema(json.loads(SCHEMA_PATH.read_text()))


# ---------------------------------------------------------------------------
# Goldens: raw -> sanitizer -> exactly the expected events
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("harness", sorted(SANITIZERS))
def test_golden_raw_sanitizes_to_exactly_the_expected_events(harness: str) -> None:
    raw = _lines(GOLDENS / harness / "raw.jsonl")
    assert 0 < len(raw) <= 60, "a golden stays small enough to review line by line"
    actual = _read_file(SANITIZERS[harness], raw)
    expected_path = GOLDENS / harness / "expected.jsonl"
    if os.environ.get("PROBE_EVENTS_REGEN") == "1":
        expected_path.write_text("".join(json.dumps(a, ensure_ascii=False) + "\n" for a in actual))
    expected = _lines(expected_path)
    assert len(expected) == len(raw), "one expected line per raw line"
    for i, (got, want) in enumerate(zip(actual, expected)):
        assert got == want, f"{harness} raw line {i + 1}"


@pytest.mark.parametrize("harness", sorted(SANITIZERS))
def test_every_golden_shows_what_its_harness_drops_and_keeps(harness: str) -> None:
    """A golden that never drops a line, or never ships one, pins nothing."""
    expected = _lines(GOLDENS / harness / "expected.jsonl")
    if harness != "pi":  # pi drops nothing: an unknown entry ships as a system event
        assert any(e is None for e in expected), "the golden has no dropped line"
    assert sum(len(_events(e)) for e in expected) >= 10


def _all_fixture_paths() -> list[pytest.param]:
    params = []
    for harness, module in SANITIZERS.items():
        paths = [GOLDENS / harness / "raw.jsonl", *_HARNESS_FIXTURES[harness][1]]
        for path in dict.fromkeys(paths):
            params.append(pytest.param(module, path, id=f"{harness}:{path.relative_to(_AGENT)}"))
    return params


@pytest.mark.parametrize("module,path", _all_fixture_paths())
def test_every_sanitized_event_validates_against_the_schema(module: Any, path: Path) -> None:
    for i, output in enumerate(_read_file(module, _lines(path))):
        for event in _events(output):
            _assert_valid(event, f"{path.name} line {i + 1}")


# ---------------------------------------------------------------------------
# inference_id / usage / origin: present where the harness has them, absent
# where it does not
# ---------------------------------------------------------------------------

_CC_USAGE = {
    "input_tokens": 1200, "output_tokens": 90, "cache_read_input_tokens": 4000,
    "cache_creation_input_tokens": 300, "service_tier": "standard",
    "cache_creation": {"ephemeral_5m_input_tokens": 300}, "iterations": [{"input_tokens": 1200}],
}


def _cc_assistant(**message: Any) -> dict:
    return {"type": "assistant", "uuid": "u", "message": {
        "role": "assistant", "content": [{"type": "text", "text": "ok"}], **message}}


def _pi_message(role: str, entry_id: str | None = "e1", **message: Any) -> dict:
    entry = {"type": "message", "timestamp": "2026-08-26T19:20:00.000Z", "parentId": "e0",
             "message": {"role": role, **message}}
    if entry_id is not None:
        entry["id"] = entry_id
    return entry


def _kimi_loop(event: dict) -> dict:
    return {"type": "context.append_loop_event", "agentId": "main", "time": 1791170700000, "event": event}


def _kimi_user(origin: dict, text: str) -> dict:
    return {"type": "context.append_message", "agentId": "main", "time": 1791170700000,
            "message": {"role": "user", "content": [{"type": "text", "text": text}], "origin": origin}}


_PART = {"type": "text", "text": "hi"}

#: (row id, sanitizer, raw line, {field: value} on every event, fields absent from every event)
_ROWS = [
    ("cc assistant: message id and the four counts", sanitize,
     _cc_assistant(id="msg_01A", usage=_CC_USAGE),
     {"inference_id": "msg_01A", "usage": {k: _CC_USAGE[k] for k in sanitize.USAGE_KEYS}}, {"origin"}),
    ("cc assistant: a partial usage keeps only what was reported", sanitize,
     _cc_assistant(id="msg_01A", usage={"output_tokens": 7, "input_tokens": "12", "cache_read_input_tokens": True}),
     {"inference_id": "msg_01A", "usage": {"output_tokens": 7}}, set()),
    ("cc assistant: no id, no usage (an API error line)", sanitize,
     _cc_assistant(), {}, {"inference_id", "usage", "origin"}),
    ("cc assistant: usage with no count at all", sanitize,
     _cc_assistant(id="msg_01A", usage={"service_tier": "standard"}), {"inference_id": "msg_01A"}, {"usage"}),
    ("cc user: never an inference", sanitize,
     {"type": "user", "message": {"role": "user", "content": "hi", "id": "msg_x", "usage": _CC_USAGE}},
     {}, {"inference_id", "usage", "origin"}),
    ("cc: a raw top-level origin or usage is not copied", sanitize,
     {"type": "user", "origin": {"kind": "human"}, "usage": {"input_tokens": 1}, "inference_id": "forged",
      "message": {"role": "user", "content": "hi"}},
     {}, {"inference_id", "usage", "origin"}),
    ("pi assistant: entry id and mapped counts", pi_sanitize,
     _pi_message("assistant", content=[_PART], usage={
         "input": 10, "output": 116, "cacheRead": 0, "cacheWrite": 10014, "totalTokens": 10140,
         "cost": {"total": 0.013}, "reasoning": 60}),
     {"inference_id": "e1", "usage": {"input_tokens": 10, "output_tokens": 116,
                                      "cache_read_input_tokens": 0, "cache_creation_input_tokens": 10014}},
     {"origin"}),
    ("pi assistant: no id, no usage", pi_sanitize,
     _pi_message("assistant", entry_id=None, content=[_PART]), {}, {"inference_id", "usage", "origin"}),
    ("pi bashExecution: both halves are the researcher's shell", pi_sanitize,
     _pi_message("bashExecution", command="ls", output="a\n", exitCode=0),
     {"origin": "user_shell"}, {"inference_id", "usage"}),
    ("pi user: a prompt has no origin", pi_sanitize,
     _pi_message("user", content="hi"), {}, {"inference_id", "usage", "origin"}),
    ("kimi content.part: turn:step", kimi_sanitize,
     _kimi_loop({"type": "content.part", "turnId": "1", "step": 2, "part": _PART}),
     {"inference_id": "1:2"}, {"usage", "origin"}),
    ("kimi tool.call: turn:step", kimi_sanitize,
     _kimi_loop({"type": "tool.call", "turnId": "0", "step": 1, "toolCallId": "t1", "name": "Bash",
                 "args": {"command": "ls"}}),
     {"inference_id": "0:1"}, {"usage", "origin"}),
    ("kimi content.part without a step", kimi_sanitize,
     _kimi_loop({"type": "content.part", "turnId": "1", "part": _PART}), {}, {"inference_id"}),
    ("kimi tool.result: an observation, not an inference", kimi_sanitize,
     _kimi_loop({"type": "tool.result", "turnId": "0", "step": 1, "toolCallId": "t1", "result": {"output": "x"}}),
     {}, {"inference_id", "usage", "origin"}),
    ("kimi shell input", kimi_sanitize,
     _kimi_user({"kind": "shell_command", "phase": "input"}, "<bash-input>ls</bash-input>"),
     {"origin": "user_shell"}, {"inference_id", "usage"}),
    ("kimi shell output: a size, no origin", kimi_sanitize,
     _kimi_user({"kind": "shell_command", "phase": "output"}, "a\n"), {}, {"origin", "inference_id"}),
    ("kimi plugin command: typed, but not a shell", kimi_sanitize,
     _kimi_user({"kind": "plugin_command", "pluginId": "p", "commandName": "c"}, "BODY"), {}, {"origin"}),
    ("kimi user prompt", kimi_sanitize,
     _kimi_user({"kind": "user"}, "hi"), {}, {"inference_id", "usage", "origin"}),
    ("kimi step.end: the step's usage, under its turn:step", kimi_sanitize,
     _kimi_loop({"type": "step.end", "turnId": "4", "step": 2, "finishReason": "end_turn",
                 "usage": {"inputOther": 1200, "output": 90, "inputCacheRead": 4000, "inputCacheCreation": 300},
                 "llmFirstTokenLatencyMs": 19, "messageId": "chatcmpl-6"}),
     {"inference_id": "4:2", "usage": {"input_tokens": 1200, "output_tokens": 90,
                                       "cache_read_input_tokens": 4000, "cache_creation_input_tokens": 300}},
     {"origin"}),
    ("codex token_usage_record: the turn's running total, cache taken out of input", codex_sanitize,
     {"type": "token_usage_record", "timestamp": "t",
      "payload": {"thread_id": "s", "turn_id": "turn-row", "response_id": "resp_1",
                  "usage": {"input_tokens": 34682, "cached_input_tokens": 32640, "output_tokens": 83},
                  "turn_token_usage": {"input_tokens": 67267, "cached_input_tokens": 32640,
                                       "cache_write_input_tokens": 0, "output_tokens": 302,
                                       "reasoning_output_tokens": 0, "total_tokens": 67569},
                  "thread_token_usage": {"input_tokens": 99999}}},
     {"inference_id": "turn:turn-row", "usage": {"input_tokens": 34627, "output_tokens": 302,
                                                 "cache_read_input_tokens": 32640,
                                                 "cache_creation_input_tokens": 0}},
     {"origin"}),
    ("codex assistant: none of the three", codex_sanitize,
     {"type": "response_item", "timestamp": "t",
      "payload": {"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": "hi"}]}},
     {}, {"inference_id", "usage", "origin"}),
    ("codex shell call: none of the three", codex_sanitize,
     {"type": "response_item", "timestamp": "t",
      "payload": {"type": "local_shell_call", "call_id": "c", "status": "completed",
                  "action": {"type": "exec", "command": ["ls"]}}},
     {}, {"inference_id", "usage", "origin"}),
]


def test_a_usage_event_names_the_model_its_turn_or_step_ran_on() -> None:
    """Codex's usage record and Kimi's step.end do not name the model; the
    turn's `turn_context` / the step's `llm.request` earlier in the same file
    does. Outside a file's memory (`call_models`) the event names none."""
    codex_usage = {"type": "token_usage_record", "timestamp": "t",
                   "payload": {"turn_id": "turn-model", "turn_token_usage": {"output_tokens": 1}}}
    codex_context = {"type": "turn_context", "payload": {"turn_id": "turn-model", "model": "gpt-6.1"}}
    kimi_request = {"type": "llm.request", "agentId": "main", "model": "kimi-k3", "modelAlias": "k",
                    "turnStep": "7.3"}
    kimi_end = _kimi_loop({"type": "step.end", "turnId": "7", "step": 3, "usage": {"output": 1}})
    codex_sanitize.sanitize_event(codex_context)
    kimi_sanitize.sanitize_event(kimi_request)
    assert "model" not in codex_sanitize.sanitize_event(codex_usage)["message"], "no file: no memory"
    assert "model" not in kimi_sanitize.sanitize_event(kimi_end)["message"]
    codex_out, kimi_out = _read_file(codex_sanitize, [codex_context, codex_usage]), _read_file(
        kimi_sanitize, [kimi_request, kimi_end])
    assert codex_out[1]["message"]["model"] == "gpt-6.1"
    assert kimi_out[0] is None, "the request itself still ships nothing"
    assert kimi_out[1]["message"]["model"] == "kimi-k3"
    _assert_valid(kimi_out[1], "kimi usage with its model")


def test_a_compaction_ships_its_usage_and_a_turns_records_do_not_count_twice() -> None:
    """Kimi writes a `usage.record` per call; a turn's calls also end in a
    step.end (counted there), a compaction's in nothing else."""
    request = {"type": "llm.request", "agentId": "main", "kind": "compaction", "model": "kimi-k3",
               "modelAlias": "k", "time": 1791169948083}
    record = {"type": "usage.record", "agentId": "main", "model": "k", "usageScope": "session",
              "usage": {"inputOther": 100, "output": 10, "inputCacheRead": 5, "inputCacheCreation": 0},
              "time": 1791169948091}
    turn_record = {**record, "usageScope": "turn", "time": 1791169948095}
    out = _read_file(kimi_sanitize, [request, record, turn_record])
    assert out[0] is None and out[2] is None
    assert out[1]["inference_id"] == "session:1791169948091"
    assert out[1]["usage"] == {"input_tokens": 100, "output_tokens": 10, "cache_read_input_tokens": 5,
                               "cache_creation_input_tokens": 0}
    assert out[1]["message"]["model"] == "kimi-k3"
    _assert_valid(out[1], "kimi compaction usage")


def test_a_usage_record_with_no_turn_or_no_count_ships_nothing() -> None:
    assert codex_sanitize.sanitize_event(
        {"type": "token_usage_record", "payload": {"turn_token_usage": {"output_tokens": 1}}}) is None
    assert codex_sanitize.sanitize_event(
        {"type": "token_usage_record", "payload": {"turn_id": "t", "turn_token_usage": {"total_tokens": 9}}}) is None
    assert codex_sanitize.sanitize_event(
        {"type": "event_msg", "payload": {"type": "token_count", "info": {"total_token_usage": {"input_tokens": 1}}}}
    ) is None, "token_count stays dropped: token_usage_record carries the same counts with the turn"
    assert kimi_sanitize.sanitize_event(_kimi_loop({"type": "step.end", "turnId": "0", "step": 1})) is None
    assert kimi_sanitize.sanitize_event(
        _kimi_loop({"type": "step.end", "turnId": "0", "usage": {"output": 1}})) is None, "no step: no call to name"


@pytest.mark.parametrize("module,raw,present,absent", [r[1:] for r in _ROWS], ids=[r[0] for r in _ROWS])
def test_probe_event_fields_present_and_absent(module: Any, raw: dict, present: dict, absent: set) -> None:
    events = _events(module.sanitize_event(raw))
    assert events
    for event in events:
        _assert_valid(event, "row")
        for key, value in present.items():
            assert event.get(key) == value, key
        for key in absent:
            assert key not in event, key


# ---------------------------------------------------------------------------
# The schema itself refuses what must not ship
# ---------------------------------------------------------------------------

_ASSISTANT = {"type": "assistant", "message": {"role": "assistant", "content": []}}


def _with_block(block: dict) -> dict:
    return {"type": "user", "message": {"role": "user", "content": [block]}}


_REFUSED = [
    ("toolUseResult", {**_ASSISTANT, "toolUseResult": {"stdout": "x"}}),
    ("tool_result body", _with_block({"type": "tool_result", "tool_use_id": "t", "content": "OUTPUT"})),
    ("tool_use input", _with_block({"type": "tool_use", "id": "t", "name": "Edit", "input": {"old_string": "x"}})),
    ("command over the cap", _with_block({"type": "tool_use", "id": "t", "name": "Bash", "summary": "x" * 4001})),
    ("unknown block with content", _with_block({"type": "document", "source": {"data": "x"}})),
    ("image bytes", _with_block({"type": "image", "source": {"type": "base64", "data": "iVBOR"}})),
    ("image data URL", _with_block({"type": "image", "source": {"type": "url", "url": "data:image/png;base64,x"}})),
    ("image digest that is not a sha256", _with_block({"type": "image", "mimeType": "image/png", "bytes": 4, "sha256": "iVBOR"})),
    ("image digest in capitals", _with_block({"type": "image", "mimeType": "image/png", "bytes": 4, "sha256": "AB" * 32})),
    ("image bytes beside a digest", _with_block({"type": "image", "mimeType": "image/png", "bytes": 4, "sha256": "ab" * 32, "data": "iVBOR"})),
    ("file attachment", {"type": "attachment", "attachment": {"type": "file", "content": "x"}}),
    ("attachment content key", {"type": "attachment", "attachment": {"type": "compact_file_reference", "content": "x"}}),
    ("codex action", {**_ASSISTANT, "_codex_extras": {"action": {"command": ["ls"]}}}),
    ("unknown top-level key", {**_ASSISTANT, "wireToolInputs": {}}),
    ("unknown message key", {"type": "assistant", "message": {"role": "assistant", "usage": {}}}),
    ("usage on a user event", {"type": "user", "usage": {"input_tokens": 1}}),
    ("usage beyond the four counts", {**_ASSISTANT, "usage": {"input_tokens": 1, "service_tier": "x"}}),
    ("an origin other than user_shell", {**_ASSISTANT, "origin": "human"}),
    ("no type", {"message": {"role": "user", "content": "hi"}}),
]


@pytest.mark.parametrize("event", [r[1] for r in _REFUSED], ids=[r[0] for r in _REFUSED])
def test_the_schema_refuses_what_capture_must_not_send(event: dict) -> None:
    assert list(VALIDATOR.iter_errors(event)), "the schema would accept this"


def test_a_pasted_image_may_carry_its_digest_and_nothing_more() -> None:
    """Tap 0.9.17: an image the researcher pasted names its uploaded bytes by
    SHA-256 (the engine's copy of this schema took the field first)."""
    event = _with_block({"type": "image", "mimeType": "image/png", "bytes": 4, "sha256": "ab" * 32})
    assert not list(VALIDATOR.iter_errors(event))


def test_the_oversize_line_marker_is_a_probe_event() -> None:
    from probe.tap_core.session_journal import oversize_line_event

    assert not list(VALIDATOR.iter_errors(oversize_line_event(70 * 1024 * 1024)))
