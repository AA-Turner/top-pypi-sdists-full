"""DD-135 — an acting run must act on ANY turn AND be able to just talk.

The structured-output chokepoint used to fire only while ``config.response_format``
was the ``json_schema`` envelope. The send boundary relaxes that envelope to text
after the first satisfied structured answer, so from turn 2 an agent whose output
IS its action (aidream's output-directive seam) was never parsed and never
dispatched — the model emitted the directive, the user got silence (live repro
2026-09-12, conversation 0a40ffc3-d5c2-441b-8d95-5cb7c815d8ce).

Forcing the schema back on fixes the action and breaks the person: the same agent
then answers "what is the difference between a project and a task?" with an empty
directive and an Approve button for nothing (V-34, live, same day). So the wire
format stays relaxed and the DISPATCH is keyed on the host's declared standing
contract instead. These are the two halves, and neither may regress:

* a relaxed turn whose text IS the contract  → parsed, emitted, dispatched
* a relaxed turn that is prose              → nothing emitted, nothing dispatched
"""

from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

CONTRACT = {
    "type": "json_schema",
    "json_schema": {
        "name": "directive_v1_action_create_project_with_tasks",
        "strict": True,
        "schema": {
            "type": "object",
            "additionalProperties": False,
            "required": ["__kind", "items"],
            "properties": {
                "__kind": {
                    "type": "string",
                    "const": "directive_v1_action_create_project_with_tasks",
                },
                "items": {"type": "array", "items": {"type": "object"}},
            },
        },
    },
}

DIRECTIVE_TEXT = json.dumps(
    {
        "__kind": "directive_v1_action_create_project_with_tasks",
        "items": [{"name": "Later Turn Project", "tasks": []}],
    }
)


class _Emitter:
    """Captures structured-output payloads; tolerates every other emitter call."""

    def __init__(self) -> None:
        self.structured: list[object] = []

    async def send_structured_output(self, payload: object) -> None:
        self.structured.append(payload)

    def __getattr__(self, _name: str):
        async def _noop(*_a, **_k):
            return None

        return _noop


def _completed(final_text: str):
    config = SimpleNamespace(
        response_format={"type": "text"},  # relaxed, exactly as turn 2+ arrives
        get_last_output=lambda: final_text,
    )
    return SimpleNamespace(request=SimpleNamespace(config=config))


def _install_ctx(emitter, *, standing: bool):
    from matrx_connect.context.app_context import AppContext, set_app_context

    metadata = {"standing_output_contract": CONTRACT} if standing else {}
    set_app_context(AppContext(emitter=emitter, user_id="dd135", metadata=metadata))


@pytest.mark.asyncio
async def test_a_relaxed_turn_that_acts_is_parsed_and_handed_on() -> None:
    from matrx_ai.orchestrator.executor import _emit_structured_output_if_schema

    emitter = _Emitter()
    _install_ctx(emitter, standing=True)
    try:
        parsed = await _emit_structured_output_if_schema(_completed(DIRECTIVE_TEXT))
    finally:
        _install_ctx(_Emitter(), standing=False)

    assert isinstance(parsed, dict), (
        "the later turn's directive must reach the output-apply dispatcher even though "
        "the wire format had relaxed to text"
    )
    assert parsed["__kind"] == "directive_v1_action_create_project_with_tasks"
    assert parsed["items"][0]["name"] == "Later Turn Project"
    assert len(emitter.structured) == 1


@pytest.mark.asyncio
async def test_a_relaxed_turn_that_only_talks_dispatches_nothing() -> None:
    from matrx_ai.orchestrator.executor import _emit_structured_output_if_schema

    emitter = _Emitter()
    _install_ctx(emitter, standing=True)
    try:
        parsed = await _emit_structured_output_if_schema(
            _completed(
                "A project is the container; a task is one piece of work inside it."
            )
        )
    finally:
        _install_ctx(_Emitter(), standing=False)

    assert parsed is None, "prose is an answer, not an action — nothing may be dispatched"
    assert emitter.structured == [], (
        "and no failed structured-output event may be painted over a good prose answer"
    )


@pytest.mark.asyncio
async def test_without_the_declaration_a_relaxed_turn_is_untouched() -> None:
    """The ordinary agent's behaviour is unchanged: no contract, no parse."""
    from matrx_ai.orchestrator.executor import _emit_structured_output_if_schema

    emitter = _Emitter()
    _install_ctx(emitter, standing=False)
    parsed = await _emit_structured_output_if_schema(_completed(DIRECTIVE_TEXT))

    assert parsed is None
    assert emitter.structured == []
