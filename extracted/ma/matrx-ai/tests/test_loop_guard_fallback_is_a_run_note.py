"""A standoff decided by the count rule (no holder on the standoff mandate) leaves a typed run note, not only a log."""

from matrx_ai.orchestrator.loop_guard import (
    STANDOFF_FALLBACK_CODE,
    STANDOFF_MANDATE_KEY,
    StandoffVerdict,
    fallback_standoff_verdict,
    standoff_fallback_note,
)


def test_a_fallback_verdict_yields_a_typed_note():
    note = standoff_fallback_note(fallback_standoff_verdict("x"), tool_name="t", iteration=3)
    assert note == {
        "code": STANDOFF_FALLBACK_CODE,
        "mandate_key": STANDOFF_MANDATE_KEY,
        "decided_by": "count_rule",
        "action": "disable_this_tool",
        "tool": "t",
        "iteration": 3,
    }


def test_a_mandate_verdict_yields_no_note():
    v = StandoffVerdict(action="continue", confidence=0.9, source="mandate", reason="")
    assert standoff_fallback_note(v, tool_name="t", iteration=1) is None
