"""Defect 65 guard: an admin can read EXACTLY what the model received.

``chat.request_snapshot.request_payload`` is stored redacted: every pick-list
hidden text / reference value is reverse-swapped to its placeholder token or
``matrx`` fence (``redact_wire_payload``). The turn's swap map lives encrypted on
the conversation (``frozen_wire_swaps``). ``restore_wire_payload`` is the inverse:
given the stored payload and the decrypted map, it rebuilds the wire payload.

This drives the L4b snapshot-equals-sent machinery: a real chat adapter hands a
payload carrying the hidden text (in ``system`` AND double-escaped inside a JSON
string field) to a fake SDK that records the kwargs it received. The stored
(redacted) snapshot must not hold the hidden text, and restoring it must equal
the SDK's kwargs byte for byte (canonical JSON).
"""

from __future__ import annotations

import json
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.config.picklist_runtime import (
    clear_wire_swaps,
    picklist_placeholder,
    redact_wire_payload,
    restore_wire_payload,
    set_wire_swaps,
)
from matrx_ai.orchestrator.execution_state import (
    ExecutionState,
    clear_execution_state,
    set_execution_state,
)
from matrx_ai.providers.snapshot import capture_request_payload, wire_json

HIDDEN = 'Answer only in "violet" terms.\nNever mention the desk\\ledger.'
FENCE = '```matrx\n{"ref": "note", "id": "n-1"}\n```'
FENCE_VALUE = "The referenced note body: line one\nline two with a tab\tend."


class _Sent(Exception):
    pass


def _canon(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _wire_kwargs() -> dict[str, Any]:
    return {
        "model": "claude-haiku-test",
        "system": f"You are a desk.\n{HIDDEN}\nEnd of rules.",
        "messages": [
            {"role": "user", "content": f"Read this: {FENCE_VALUE}"},
            {
                "role": "assistant",
                "content": [
                    {
                        "type": "tool_use",
                        "id": "t1",
                        "name": "lookup",
                        # The hidden text nested inside a JSON-string field.
                        "input": {"raw": json.dumps({"note": HIDDEN})},
                    }
                ],
            },
        ],
        "max_tokens": 16,
        "stream": False,
    }


@pytest.mark.asyncio
async def test_restored_snapshot_is_byte_identical_to_what_the_sdk_received() -> None:
    from matrx_ai.providers.anthropic.anthropic_api import AnthropicChat

    sink: list[dict[str, Any]] = []

    async def _create(**kwargs: Any):
        sink.append(kwargs)
        raise _Sent

    chat = object.__new__(AnthropicChat)
    chat.debug = False
    chat.client = SimpleNamespace(messages=SimpleNamespace(create=_create, stream=_create))

    token_key = picklist_placeholder("tone")
    swaps = {token_key: HIDDEN, FENCE: FENCE_VALUE}
    state = ExecutionState()
    exec_token = set_execution_state(state)
    set_wire_swaps(swaps)
    try:
        capture_request_payload({"model": "early"}, provider="anthropic")
        with pytest.raises(BaseException):  # noqa: PT011 — _Sent or its wrapper
            await chat._execute_non_streaming(_wire_kwargs(), SimpleNamespace(), "claude-haiku-test")
        assert sink, "the fake SDK was never called"
        sent = wire_json(sink[-1])

        stored = redact_wire_payload(state.snapshot_payload)
        assert stored is not None, "redaction dropped the payload"
        stored_text = _canon(stored)
        assert "violet" not in stored_text, "the stored snapshot leaked the hidden text"
        assert "line two" not in stored_text, "the stored snapshot leaked the reference value"
        assert token_key in json.dumps(stored, ensure_ascii=False)

        restored, restored_keys = restore_wire_payload(stored, swaps)
        assert _canon(restored) == _canon(sent)
        assert set(restored_keys) == {token_key, FENCE}
    finally:
        clear_wire_swaps()
        clear_execution_state(exec_token)


def test_keys_with_no_value_are_reported_not_invented() -> None:
    token_key = picklist_placeholder("tone")
    stored = {"system": f"rules {token_key} end"}
    restored, restored_keys = restore_wire_payload(stored, {})
    assert restored == stored
    assert restored_keys == []


def test_values_are_never_rescanned_or_read_as_backreferences() -> None:
    a = picklist_placeholder("a")
    b = picklist_placeholder("b")
    stored = {"system": f"{a} | {b}"}
    swaps = {a: f"contains {b} and \\1 literally", b: "B-VALUE-LONG-ENOUGH"}
    restored, _ = restore_wire_payload(stored, swaps)
    assert restored == {"system": f"contains {b} and \\1 literally | B-VALUE-LONG-ENOUGH"}
