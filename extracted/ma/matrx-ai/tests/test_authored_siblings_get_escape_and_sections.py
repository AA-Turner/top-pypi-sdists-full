"""THE VARIABLE RULE reaches the Holder's own authored text (``HeldCall.authored_text``): the escape
``{{!name}}`` and the sections run on it, the same as on a text part."""

from __future__ import annotations

from matrx_ai.mandates import HeldCall


def _held(text: str) -> HeldCall:
    return HeldCall(
        mandate_key="t", model="m", system="", temperature=None, max_output_tokens=None,
        turns=[], config=None, metadata={}, holder_values={"nudge": text},
    )


def test_holder_text_unescapes_and_fills_in_one_pass() -> None:
    out = _held("Write {{!word}} as {{word}}").authored_text("nudge", word="tea")
    assert out == "Write {{word}} as tea"


def test_holder_text_evaluates_sections() -> None:
    held = _held("A{{#extra}} plus {{extra}}{{/extra}}{{^extra}} alone{{/extra}}")
    assert held.authored_text("nudge", extra="") == "A alone"
    assert held.authored_text("nudge", extra="x") == "A plus x"


def test_holder_text_escape_runs_with_no_values() -> None:
    assert _held("keep {{!word}}").authored_text("nudge", word="") == "keep {{word}}"
    assert _held("keep {{!word}}").authored_text("nudge") == "keep {{word}}"
