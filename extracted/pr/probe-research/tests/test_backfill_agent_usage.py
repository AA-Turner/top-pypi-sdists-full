"""What an import agent's event stream says it cost, and whether it refused a setting.

`fold_event` reads both from the lines the real agents print
(`recorded_agent_events`, recorded on prbe-devbox 2026-10-25). Two failures
matter more than the arithmetic:

  * a run cut off before its terminal event must read as UNKNOWN usage, never
    0 -- an aborted import that looks free is the wrong answer to "what did
    this import cost";
  * a refusal must be recognised only from the agent's structured error and
    only for the setting it names, because `launch_agent` relaunches on it.
"""

from __future__ import annotations

import json

import pytest

from probe.cli import backfill as bf
from recorded_agent_events import (
    CLAUDE_BAD_MODEL,
    CLAUDE_OK,
    CODEX_BAD_EFFORT,
    CODEX_BAD_MODEL,
    CODEX_OK,
)


def _fold(lines, *, sent_effort=None) -> bf.Activity:
    state = bf.Activity(total=0, sent_effort=sent_effort)
    for line in lines:
        bf.fold_event(line + "\n", state)
    return state


def test_codex_usage_is_read_from_turn_completed():
    state = _fold(CODEX_OK)
    assert state.usage == {
        "input_tokens": 30047, "cached_input_tokens": 12288, "cache_write_input_tokens": 0,
        "output_tokens": 5, "reasoning_output_tokens": 0,
    }
    assert state.refused is None
    assert state.acted, "an agent message is the model having run"


def test_claude_usage_counts_cache_reads_and_writes_as_input():
    """Claude's `input_tokens` excludes the cache; Codex's includes it. Mapped
    so the two agents' numbers mean the same thing on one insight."""
    state = _fold(CLAUDE_OK)
    assert state.usage == {
        "input_tokens": 2 + 31298, "cached_input_tokens": 0, "cache_write_input_tokens": 31298,
        "output_tokens": 4, "reasoning_output_tokens": 0,
    }
    assert state.refused is None


def test_two_turns_are_summed():
    state = _fold([CODEX_OK[-1], CODEX_OK[-1]])
    assert state.usage["input_tokens"] == 2 * 30047


@pytest.mark.parametrize("lines", [CODEX_OK[:-1], [], ["not json at all"]])
def test_a_run_cut_before_its_terminal_event_has_unknown_usage_not_zero(lines):
    assert _fold(lines).usage is None


def test_codex_refusing_a_model_is_recognised_before_any_work():
    state = _fold(CODEX_BAD_MODEL)
    assert state.refused == "model"
    assert not state.acted, "Codex's own `error` item is a warning, not work"
    assert state.usage is None


def test_claude_refusing_a_model_is_recognised_before_any_work():
    state = _fold(CLAUDE_BAD_MODEL)
    assert state.refused == "model"
    assert not state.acted, "the synthetic reply carries no tool call"
    assert state.usage == dict.fromkeys(bf.USAGE_FIELDS, 0), "Claude reports its zero itself"


def test_an_effort_refusal_must_name_the_effort_this_launch_sent():
    assert _fold(CODEX_BAD_EFFORT, sent_effort="bogus").refused == "effort"
    # The same error about some OTHER value is not this launch's setting.
    assert _fold(CODEX_BAD_EFFORT, sent_effort="medium").refused is None
    assert _fold(CODEX_BAD_EFFORT).refused is None


def test_an_effort_error_naming_reasoning_is_recognised():
    message = json.dumps({"type": "error", "status": 400, "error": {
        "type": "invalid_request_error", "param": "reasoning.effort", "code": None,
        "message": "Unsupported value: 'xhigh' is not supported with this model.",
    }})
    line = json.dumps({"type": "turn.failed", "error": {"message": message}})
    assert _fold([line], sent_effort="xhigh").refused == "effort"


@pytest.mark.parametrize("error", [
    {"type": "invalid_request_error", "code": "context_length_exceeded",
     "message": "Your input exceeds the context window of this model."},
    {"type": "server_error", "code": None, "message": "An error occurred."},
])
def test_other_request_errors_are_not_refusals(error):
    message = json.dumps({"type": "error", "status": 400, "error": error})
    lines = [json.dumps({"type": "error", "message": message}),
             json.dumps({"type": "turn.failed", "error": {"message": message}})]
    assert _fold(lines, sent_effort="medium").refused is None


def test_a_claude_error_that_is_not_a_404_is_not_a_model_refusal():
    result = json.loads(CLAUDE_BAD_MODEL[-1])
    result.update(api_error_status=429, result="API Error: rate limited")
    assert _fold([json.dumps(result)]).refused is None


def test_tool_calls_mark_the_run_as_having_acted():
    codex = json.dumps({"type": "item.started", "item": {
        "id": "item_1", "type": "command_execution", "command": "/bin/bash -lc 'ls'",
    }})
    claude = json.dumps({"type": "assistant", "message": {"content": [
        {"type": "tool_use", "name": "Read", "input": {"file_path": "/x/a.py"}},
    ]}})
    assert _fold([codex]).acted and _fold([claude]).acted


def test_folding_still_reports_display_changes_as_before():
    """The cost half must not change what the live line shows."""
    state = bf.Activity(total=0)
    assert [bf.fold_event(line, state) for line in CODEX_OK] == [False, True, True, False]
    assert state.doing == "ok"
