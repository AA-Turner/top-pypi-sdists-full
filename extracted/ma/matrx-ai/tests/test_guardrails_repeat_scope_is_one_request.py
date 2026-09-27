"""The repeat guards judge ONE request, never the person's whole thread.

A stuck loop is a model repeating itself inside a single turn. The duplicate
and loop guards used to count every identical call the conversation had ever
made, so a person on a long-lived thread (a Personal Staff text thread is one
per person, forever) who asked "what files are in my workspace?" three times
over an afternoon got the third answer blocked as a "Triplicate call" — the
2026-09-26 Lane AU3 battery, turn 12 (12:35, 12:44, 12:51 UTC, three separate
texts). Identical calls in DIFFERENT requests are a person asking again, not
a loop. Inside one request both guards must still trip.
"""

from __future__ import annotations

from contextlib import contextmanager

from matrx_connect.context.app_context import (
    AppContext,
    clear_app_context,
    set_app_context,
)

from matrx_ai.tools.guardrails import GuardrailEngine
from matrx_ai.tools.models import ToolContext, ToolDefinition

_TOOL = ToolDefinition(
    name="fs_list",
    description="test tool",
    parameters={"path": {"type": "string", "required": True}},
)
_ARGS = {"path": "."}


@contextmanager
def _request(request_id: str):
    token = set_app_context(
        AppContext(
            emitter=None,
            user_id="test-user",
            is_authenticated=True,
            conversation_id="staff-thread",
            request_id=request_id,
        )
    )
    try:
        yield ToolContext(call_id=f"call-{request_id}", conversation_id="staff-thread")
    finally:
        clear_app_context(token)


def _one_call(guard: GuardrailEngine, ctx: ToolContext) -> str | None:
    for result in (
        guard._check_duplicate(_TOOL.name, _ARGS, ctx, _TOOL),
        guard._check_loop_detection(_TOOL.name, _ARGS, ctx, _TOOL),
    ):
        if result.blocked:
            return result.error_type
    guard.record_call(_TOOL.name, _ARGS, ctx)
    return None


def test_the_same_question_in_twelve_separate_texts_is_never_blocked() -> None:
    guard = GuardrailEngine()
    outcomes = []
    for turn in range(12):
        with _request(f"req-{turn}") as ctx:
            outcomes.append(_one_call(guard, ctx))
    assert outcomes == [None] * 12


def test_inside_one_request_a_triplicate_is_still_blocked() -> None:
    guard = GuardrailEngine()
    with _request("req-loop") as ctx:
        outcomes = [_one_call(guard, ctx) for _ in range(3)]
    assert outcomes == [None, None, "duplicate"]


def test_inside_one_request_an_interleaved_loop_is_still_blocked() -> None:
    guard = GuardrailEngine()
    other = ToolDefinition(name="fs_read", description="t", parameters={})
    outcomes = []
    with _request("req-loop") as ctx:
        for _ in range(6):
            outcomes.append(_one_call(guard, ctx))
            guard.record_call(other.name, {"path": "x"}, ctx)
    assert outcomes[:5] == [None] * 5
    assert outcomes[5] == "loop_detected"
