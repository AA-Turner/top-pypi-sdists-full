"""A turn parked on a person has no answer yet — it never emits structured output.

The break this guards: the Applet builder's `ask_person` turn suspended
(`suspended_awaiting_client`), and `_emit_structured_output_if_schema` parsed the
parked tool call (``get_last_output()`` serialises it as JSON) as the run's
declared answer. The page received ``{"__kind": "applet_build_result", "type":
"tool_call", ...}`` and said "The builder answered without an app" over a question
it never showed (live, www.aimatrx.com v0.4.3078, 2026-10-09).
"""

from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

SCHEMA = {
    "type": "object",
    "additionalProperties": True,
    "properties": {"type": {"type": "string"}, "name": {"type": "string"}},
}

PARKED_CALL_TEXT = json.dumps(
    {"type": "tool_call", "call_id": "gemini_1", "name": "ask_person", "arguments": {"kind": "choose_one"}}
)


class _Emitter:
    def __init__(self) -> None:
        self.structured: list[object] = []

    async def send_structured_output(self, payload: object) -> None:
        self.structured.append(payload)

    def __getattr__(self, _name: str):
        async def _noop(*_a, **_k):
            return None

        return _noop


def _completed(status: str | None):
    config = SimpleNamespace(
        response_format={"type": "json_schema", "json_schema": {"name": "build", "strict": False, "schema": SCHEMA}},
        get_last_output=lambda: PARKED_CALL_TEXT,
    )
    return SimpleNamespace(request=SimpleNamespace(config=config), metadata={"status": status} if status else {})


def _install(emitter):
    from matrx_connect.context.app_context import AppContext, set_app_context

    set_app_context(
        AppContext(
            emitter=emitter,
            user_id="parked-turn-test",
            conversation_id="11111111-1111-4111-8111-111111111111",
            request_id="22222222-2222-4222-8222-222222222222",
            store=False,
        )
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("status", ["suspended_awaiting_client", "suspended_awaiting_human_browser"])
async def test_a_parked_turn_emits_nothing(status: str) -> None:
    from matrx_ai.orchestrator.executor import _emit_structured_output_if_schema

    emitter = _Emitter()
    _install(emitter)
    assert await _emit_structured_output_if_schema(_completed(status)) is None
    assert emitter.structured == []


@pytest.mark.asyncio
async def test_a_finished_turn_still_emits_its_answer() -> None:
    """The control: the same text on a turn that FINISHED is parsed and emitted."""
    from matrx_ai.orchestrator.executor import _emit_structured_output_if_schema

    emitter = _Emitter()
    _install(emitter)
    data = await _emit_structured_output_if_schema(_completed(None))
    assert isinstance(data, dict) and data.get("name") == "ask_person"
    assert len(emitter.structured) == 1
