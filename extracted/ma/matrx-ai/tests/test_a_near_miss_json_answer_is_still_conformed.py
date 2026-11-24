"""An answer the parse funnel can read is conformed to the author's contract, even when strict JSON can't read it.

2026-11-18 live (system_error c9559cdf, ``flashcards.generate_cards`` on gemini-3.8-flash with grounding): the
reply was a GROUNDED RESEARCH DIGEST plus one fenced ```json block, and every optional
``additionalDetails`` came back ``null``. One card's ``back`` wrote LaTeX as ``\\(68\\\\text{--}69\\\\%\\)``.
``\\(`` is not a legal JSON escape, so ``conform_answer_to_contract`` (strict ``json.loads``) skipped the
block and pruned nothing. The mandate's reader then parsed the same text through the funnel's faithful
repair, got the nulls, and filed ``mandate_output_contract_drift`` ("additionalDetails: None is not of type
'object'") on a correct deck. The seam must read the answer the way every consumer downstream reads it.
"""

from __future__ import annotations

import contextlib
import io
import json
from typing import Any

FLASHCARD_SET: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["__kind", "title", "cards"],
    "properties": {
        "__kind": {"type": "string", "const": "flashcard_set"},
        "title": {"type": "string"},
        "additionalDetails": {"type": "object", "additionalProperties": True},
        "cards": {"type": "array", "items": {"anyOf": [{"$ref": "#/$defs/flashcard"}]}},
    },
    "$defs": {
        "flashcard": {
            "type": "object",
            "additionalProperties": False,
            "required": ["__kind", "front", "back"],
            "properties": {
                "__kind": {"type": "string", "const": "flashcard"},
                "front": {"type": "string"},
                "back": {"type": "string"},
                "additionalDetails": {"type": "object", "additionalProperties": True},
            },
        }
    },
}

# The live reply's shape: digest prose, then a fenced block whose LaTeX uses the illegal escape ``\(``.
LIVE_SHAPE_ANSWER = (
    "GROUNDED RESEARCH DIGEST\nMore than \\(96.5\\%\\) of water is saline.\n\n"
    "```json\n"
    '{\n  "__kind": "flashcard_set",\n  "title": "The Water Cycle",\n  "additionalDetails": null,\n'
    '  "cards": [\n    {\n      "__kind": "flashcard",\n      "front": "Where is most freshwater?",\n'
    '      "back": "In ice (roughly \\(68\\\\text{--}69\\\\%\\) of it).",\n      "additionalDetails": null\n    }\n  ]\n}\n'
    "```"
)


def _conformed(answer_text: str) -> tuple[str, list[str]]:
    from matrx_ai.config import Role, UnifiedMessage, UnifiedResponse
    from matrx_ai.config.unified_content import TextContent
    from matrx_ai.schema.answer_contract import (
        bind_declared_output_contract,
        conform_answer_to_contract,
        release_declared_output_contract,
    )

    response = UnifiedResponse(
        messages=[UnifiedMessage(role=Role.ASSISTANT, content=[TextContent(text=answer_text)])],
        usage=None,
        finish_reason="stop",
    )
    token = bind_declared_output_contract(
        {"type": "json_schema", "json_schema": {"name": "flashcard_set", "schema": FLASHCARD_SET}}
    )
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            notes = conform_answer_to_contract(response)
    finally:
        release_declared_output_contract(token)
    return response.messages[0].content[0].text, notes


def _fenced_body(text: str) -> str:
    return text.split("```json\n", 1)[1].rsplit("```", 1)[0]


def test_the_live_answer_is_strictly_unreadable_but_funnel_readable() -> None:
    """Fixture sanity: the block really is the near-miss shape (strict refuses, the funnel reads it)."""
    from matrx_ai.agents.response_parser import parse_json_document

    body = _fenced_body(LIVE_SHAPE_ANSWER)
    try:
        json.loads(body)
    except json.JSONDecodeError:
        pass
    else:  # pragma: no cover — the fixture lost its point
        raise AssertionError("the fixture must hold an escape strict JSON refuses")
    assert parse_json_document(body) is not None


def test_a_near_miss_answer_loses_the_boundarys_nulls() -> None:
    text, notes = _conformed(LIVE_SHAPE_ANSWER)
    assert notes, "nothing was conformed: the nulls reach the kind validator"
    delivered = json.loads(_fenced_body(text))
    assert "additionalDetails" not in delivered
    assert "additionalDetails" not in delivered["cards"][0]
    # Nothing the model wrote is lost: the prose stays, and the LaTeX keeps its characters.
    assert text.startswith("GROUNDED RESEARCH DIGEST")
    assert "68" in delivered["cards"][0]["back"] and "69" in delivered["cards"][0]["back"]
    import jsonschema

    jsonschema.validate(delivered, FLASHCARD_SET)


def test_a_cut_off_answer_is_never_rewritten() -> None:
    """A block that ends mid-object is a lost tail, not a near miss: the seam leaves it for the check to report."""
    cut = "```json\n" + '{"__kind": "flashcard_set", "title": "T", "additionalDetails": null, "cards": [{"front": "x'
    text, notes = _conformed(cut)
    assert notes == []
    assert text == cut
