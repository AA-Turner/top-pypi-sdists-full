"""``{"$optional": ref, "default": v}`` — a field a kind carries only sometimes.

A quiz's multiple-choice question has ``options``; a short-answer one does not. Reshaping
both into rows used to need custom code, because a plain ref that does not resolve fails
the step (rightly). The optional form declares the absence in the template.
"""

from __future__ import annotations

import pytest

from matrx_graph.errors import ExecutionError
from matrx_graph.nodes._template import substitute_template

QUESTIONS = [
    {"type": "multiple_choice", "question": "Q1", "options": ["a", "b"]},
    {"type": "short_answer", "question": "Q2"},
]


def test_an_optional_field_resolves_when_present_and_defaults_when_absent() -> None:
    template = {"prompt": "$item.question", "options": {"$optional": "$item.options", "default": []}}
    rows = [substitute_template(template, q, index=i, extra={}) for i, q in enumerate(QUESTIONS)]
    assert rows == [{"prompt": "Q1", "options": ["a", "b"]}, {"prompt": "Q2", "options": []}]


def test_the_default_is_null_when_not_given() -> None:
    assert substitute_template({"$optional": "$item.options"}, QUESTIONS[1], index=1, extra={}) is None


def test_a_plain_ref_still_fails_loudly() -> None:
    with pytest.raises(ExecutionError):
        substitute_template({"options": "$item.options"}, QUESTIONS[1], index=1, extra={})


def test_a_dict_with_other_keys_is_an_ordinary_dict() -> None:
    value = substitute_template({"$optional": "x", "other": 1}, {}, index=0, extra={})
    assert value == {"$optional": "x", "other": 1}


def test_a_wiring_error_inside_optional_still_fails_loudly() -> None:
    # Only a missing path falls back to the default; a broken template is the author's bug.
    with pytest.raises(ExecutionError, match=r"\$cycle"):
        substitute_template({"$optional": {"$cycle": []}, "default": "x"}, {"a": 1})


@pytest.mark.parametrize(
    ("ref", "kwargs"),
    [
        pytest.param({"$optional": "$index"}, {}, id="index-with-no-position"),
        pytest.param({"$optional": "$in.x"}, {"extra": None}, id="input-with-no-namespace"),
        pytest.param({"$optional": "$item.{$item}"}, {}, id="item-segment-on-a-dict"),
    ],
)
def test_optional_never_hides_a_wiring_mistake(ref: dict, kwargs: dict) -> None:
    with pytest.raises(ExecutionError):
        substitute_template(ref, {"a": 1}, **kwargs)


def test_count_placeholder_renders_how_many() -> None:
    """``{path:count}`` — how many entries (red before 2026-10-27: the brace was left as written)."""
    from matrx_graph.nodes._template import render_template_string

    root = {"made": {"failed_calls": [{"call": 1}, {"call": 2}]}, "none": None, "word": "abc"}
    assert render_template_string("failed ({made.failed_calls:count})", root)[0] == "failed (2)"
    assert render_template_string("{none:count}", root)[0] == "0"
    assert render_template_string("{word:count}", root)[0] == "3"
    assert render_template_string("{made:count}", root)[0] == "1"


def test_join_placeholder_renders_a_list_as_plain_text() -> None:
    """``{path:join}`` — list entries joined with " · " (red before 2026-10-29: JSON brackets showed)."""
    from matrx_graph.nodes._template import render_template_string

    root = {"w": ["schema.org sameAs", "x profile"], "one": ["a"], "none": None, "word": "abc"}
    assert render_template_string("Found via: {w:join}", root)[0] == "Found via: schema.org sameAs · x profile"
    assert render_template_string("{one:join}", root)[0] == "a"
    assert render_template_string("{none:join}|{word:join}", root)[0] == "|abc"
