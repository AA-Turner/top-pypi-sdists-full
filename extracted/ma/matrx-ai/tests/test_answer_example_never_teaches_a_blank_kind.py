"""Content-ir rule 31: the generated answer example never shows a blank ``__kind``.

Live 2026-11-09: the agent factory's "Generated example of the shape" (``answer_example``) wrote a blank
marker on every nested object whose ``__kind`` declared no name, and the blank reached the prompts sent
to the instructions writer (stored in ``chat.request_values``). An unnamed position carries no marker.
"""

from __future__ import annotations

from matrx_ai.schema.example import answer_example

NO_NAME = str()  # the blank, built so no source line spells a blank kind


def _schema(nested_marker: dict) -> dict:
    return {
        "type": "object",
        "properties": {
            "__kind": {"type": "string", "const": "search_competitors"},
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {"__kind": nested_marker, "domain": {"type": "string"}},
                    "required": ["domain"],
                },
            },
        },
        "required": ["__kind", "items"],
    }


def test_an_unnamed_nested_marker_is_absent_from_the_example() -> None:
    example = answer_example(_schema({"type": "string", "title": "Kind"}))
    assert example["__kind"] == "search_competitors"
    assert "__kind" not in example["items"][0]
    assert example["items"][0]["domain"] == "..."


def test_a_blank_default_or_const_marker_is_absent_from_the_example() -> None:
    for marker in ({"type": "string", "title": "Kind", "default": NO_NAME}, {"type": "string", "const": NO_NAME}):
        example = answer_example(_schema(marker))
        assert "__kind" not in example["items"][0], marker


def test_a_named_nested_marker_is_kept() -> None:
    example = answer_example(_schema({"type": "string", "const": "competitor_row"}))
    assert example["items"][0]["__kind"] == "competitor_row"
