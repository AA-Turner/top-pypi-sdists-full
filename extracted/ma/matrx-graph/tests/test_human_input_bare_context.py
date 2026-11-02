"""Guard (2026-09-11, expert-book challenge W23): a Pause & Ask step whose
``context`` is wired from a plain text (the usual case — a summary line) must
not die with a dict_type error at the pause. The person needs to SEE the
context; a bare value is carried under the name ``context``.
"""

from __future__ import annotations

from matrx_graph.nodes.control.human_input import HumanInputInput


def test_bare_text_context_is_carried_not_refused():
    parsed = HumanInputInput.model_validate(
        {"context": "AUTOMATED GOOGLE LENS RESULT: 18 exact matches"}
    )
    assert parsed.context == {"context": "AUTOMATED GOOGLE LENS RESULT: 18 exact matches"}


def test_list_context_is_carried_under_one_name():
    parsed = HumanInputInput.model_validate({"context": ["a", "b"]})
    assert parsed.context == {"context": ["a", "b"]}


def test_named_values_pass_through_unchanged():
    parsed = HumanInputInput.model_validate({"context": {"__kind": "note", "text": "x"}})
    assert parsed.context == {"__kind": "note", "text": "x"}


def test_missing_context_is_still_empty():
    assert HumanInputInput.model_validate({}).context == {}
