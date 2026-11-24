"""An observation (screenshot, page read, wait) is never refused as a repeat when
an action ran since it last ran; a model truly stuck looking is still stopped.

Reported by a real agent in the Chrome extension: its screenshot after Cancel was
refused as a repeated call although the page had changed. Observation is decided
by the registry's classification (tier ``read``, ``read_only``, or an enum
argument's ``x-observation-values``), never a name list.
"""

from __future__ import annotations

from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

from matrx_ai.tools.guardrails import GuardrailEngine, is_observation_call
from matrx_ai.tools.models import ToolContext, ToolDefinition

COMPUTER = ToolDefinition(
    name="computer",
    description="t",
    tier="action",
    parameters={
        "action": {"type": "string", "enum": ["screenshot", "left_click"], "x-observation-values": ["screenshot"]},
        "ref": {"type": "string"},
    },
)
PAGE_TEXT = ToolDefinition(name="get_page_text", description="t", tier="read", parameters={})
SHOT = {"action": "screenshot"}


def _run(calls):
    token = set_app_context(
        AppContext(emitter=None, user_id="u", is_authenticated=True, conversation_id="c", request_id="r")
    )
    try:
        ctx = ToolContext(call_id="x", conversation_id="c")
        guard = GuardrailEngine()
        out = []
        for tool, args in calls:
            blocked = None
            for res in (
                guard._check_duplicate(tool.name, args, ctx, tool),
                guard._check_loop_detection(tool.name, args, ctx, tool),
            ):
                if res.blocked:
                    blocked = res
                    break
            out.append(blocked.error_type if blocked else None)
            if not blocked:
                guard.record_call(tool.name, args, ctx, tool)
        return out
    finally:
        clear_app_context(token)


def test_classification_comes_from_the_registry_row() -> None:
    assert is_observation_call(COMPUTER, SHOT)
    assert not is_observation_call(COMPUTER, {"action": "left_click", "ref": "a"})
    assert is_observation_call(PAGE_TEXT, {})
    assert not is_observation_call(None, SHOT)
    assert not is_observation_call(ToolDefinition(name="x", description="t", parameters={}), {})


def test_the_reported_sequence_is_never_refused() -> None:
    cancel = {"action": "left_click", "ref": "cancel"}
    seq = [(COMPUTER, SHOT), (COMPUTER, cancel), (COMPUTER, SHOT), (PAGE_TEXT, {}), (COMPUTER, SHOT)]
    assert _run(seq) == [None] * 5


def test_a_long_session_of_look_act_look_is_never_refused() -> None:
    seq = []
    for i in range(8):
        seq += [(COMPUTER, SHOT), (COMPUTER, {"action": "left_click", "ref": f"r{i}"})]
    seq.append((COMPUTER, SHOT))
    assert _run(seq) == [None] * len(seq)


def test_a_model_stuck_looking_with_no_action_is_still_stopped() -> None:
    assert _run([(COMPUTER, SHOT)] * 3) == [None, None, "duplicate"]


def test_an_action_loop_is_still_stopped_even_with_looks_between() -> None:
    click = {"action": "left_click", "ref": "same"}
    seq = []
    for _ in range(6):
        seq += [(COMPUTER, click), (COMPUTER, SHOT)]
    out = _run(seq)
    assert "loop_detected" in out or "duplicate" in out


def test_the_refusal_tells_an_observer_what_to_do() -> None:
    token = set_app_context(
        AppContext(emitter=None, user_id="u", is_authenticated=True, conversation_id="c", request_id="r")
    )
    try:
        ctx = ToolContext(call_id="x", conversation_id="c")
        guard = GuardrailEngine()
        for _ in range(2):
            guard.record_call("computer", SHOT, ctx, COMPUTER)
        res = guard._check_duplicate("computer", SHOT, ctx, COMPUTER)
        assert res.blocked and "Nothing has changed" in (res.suggested_action or "")
    finally:
        clear_app_context(token)
