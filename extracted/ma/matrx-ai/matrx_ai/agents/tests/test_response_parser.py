"""Tests for the unified JSON-extraction surface in matrx-ai.

These run pure — no DB, no network — so they belong with package-internal tests.
Run with::

    uv run pytest packages/matrx-ai/matrx_ai/agents/tests/test_response_parser.py
"""

from __future__ import annotations

import pytest

from matrx_ai.agents.output import parse_agent_output, resolve_output_schema
from matrx_ai.agents.response_parser import (
    JsonExtraction,
    extract_json,
    extract_model,
)
from pydantic import BaseModel


# ---------------------------------------------------------------------------
# Fixtures — anchored to the real WC Medical & Legal failure case
# ---------------------------------------------------------------------------

WC_MEDICAL_RESPONSE = """**Defining Data Extraction Scope**

I'm now zeroing in on defining the precise data fields needed, specifically for medical and legal information. I'm structuring this as a JSON array of objects, focusing on key elements like dates, descriptions, body parts, and details.

```json
[
  {
    "DATE": "11/16/2023",
    "DESCRIPTION": "Ultrasound Exam",
    "BODY PART(S)": "Pelvis",
    "DOI": "Not stated",
    "DETAILS": "Ultrasound Pelvis W Transvaginal; Dysfunctional uterine bleeding",
    "PAGE(S)": "13",
    "SOURCE": "Theresa M Franks, MD",
    "DOCUMENT": "WC Medical & Legal",
    "PAGE": "13"
  },
  {
    "DATE": "11/08/2023",
    "DESCRIPTION": "Medical Referral/Authorization",
    "BODY PART(S)": "Pelvis",
    "DOI": "Not stated",
    "DETAILS": "Authorization for 76856 and 76830 requested by Theresa M. Franks, MD",
    "PAGE(S)": "14, 20",
    "SOURCE": "Theresa M. Franks, MD; St Jude Heritage Medical Group",
    "DOCUMENT": "WC Medical & Legal",
    "PAGE": "14, 20"
  }
]
```
"""

WC_MEDICAL_SCHEMA = {
    "name": "combined_sdt_index",
    "schema": {
        "type": "object",
        "required": ["items"],
        "properties": {
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["date", "description"],
                    "properties": {
                        "date": {"type": "string"},
                        "description": {"type": "string"},
                    },
                },
            }
        },
    },
    "strict": True,
}


# ---------------------------------------------------------------------------
# extract_json — backward compatibility
# ---------------------------------------------------------------------------


def test_extract_json_simple_dict() -> None:
    assert extract_json('{"a": 1}') == {"a": 1}


def test_extract_json_simple_array() -> None:
    assert extract_json("[1, 2, 3]") == [1, 2, 3]


def test_extract_json_returns_none_on_empty() -> None:
    assert extract_json("") is None
    assert extract_json("   ") is None
    assert extract_json("no json here at all") is None


def test_extract_json_strips_thinking() -> None:
    text = "<thinking>plotting</thinking>{\"x\": 5}"
    assert extract_json(text) == {"x": 5}


def test_extract_json_strips_reasoning_tag() -> None:
    """Provider streamers wrap reasoning in <reasoning>, not <thinking>."""
    text = "\n<reasoning>\n mulling it over \n</reasoning>\n{\"x\": 5}"
    assert extract_json(text) == {"x": 5}


def test_extract_json_ignores_json_draft_inside_reasoning() -> None:
    """A model that drafts JSON inside its reasoning must not have that draft
    win over the real final answer. Regression for the Gemini flashcards case:
    a complete ```json fence lived inside a <reasoning> block, followed by the
    real bare-JSON answer."""
    text = (
        "<reasoning>\n"
        "Let me draft the structure:\n"
        "```json\n"
        '{"set_title": "DRAFT", "cards": []}\n'
        "```\n"
        "That looks incomplete, let me finalize.\n"
        "</reasoning>\n"
        '{"set_title": "FINAL", "cards": [{"front": "Q", "back": "A"}]}'
    )
    result = extract_json(text)
    assert isinstance(result, dict)
    assert result["set_title"] == "FINAL"
    assert result["cards"] == [{"front": "Q", "back": "A"}]


def test_extract_json_schema_match_skips_reasoning_draft() -> None:
    """Even when the draft inside reasoning matches the schema shape, the real
    answer must win because the reasoning region is stripped first."""
    schema = {
        "type": "object",
        "required": ["set_title", "cards"],
        "properties": {"set_title": {"type": "string"}, "cards": {"type": "array"}},
    }
    text = (
        "<reasoning>\n"
        '```json\n{"set_title": "DRAFT", "cards": []}\n```\n'
        "</reasoning>\n"
        '{"set_title": "FINAL", "cards": [{"front": "Q", "back": "A"}]}'
    )
    result = extract_json(text, schema=schema)
    assert result["set_title"] == "FINAL"


def test_extract_json_recovers_from_fenced_block_with_prose() -> None:
    """The exact failing case from production."""
    result = extract_json(WC_MEDICAL_RESPONSE)
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["DATE"] == "11/16/2023"


def test_extract_json_handles_trailing_commas() -> None:
    assert extract_json('{"a": 1, "b": 2,}') == {"a": 1, "b": 2}


def test_extract_json_brace_walks_embedded_json() -> None:
    text = "preamble {\"k\": [1, 2]} and trailing words here"
    assert extract_json(text) == {"k": [1, 2]}


# ---------------------------------------------------------------------------
# Multi-block + Nth + return_all
# ---------------------------------------------------------------------------


MULTI_BLOCK = """
First chunk:
```json
{"id": 1}
```
Second chunk:
```json
{"id": 2}
```
Third chunk:
```json
[{"id": 3}, {"id": 4}]
```
"""


def test_return_all_collects_distinct_blocks() -> None:
    matches = extract_json(MULTI_BLOCK, return_all=True)
    assert isinstance(matches, list)
    assert {"id": 1} in matches
    assert {"id": 2} in matches
    assert [{"id": 3}, {"id": 4}] in matches


def test_nth_picks_the_right_one() -> None:
    assert extract_json(MULTI_BLOCK, nth=0) == {"id": 1}
    assert extract_json(MULTI_BLOCK, nth=1) == {"id": 2}


def test_nth_out_of_range_returns_none() -> None:
    assert extract_json(MULTI_BLOCK, nth=99) is None


def test_detailed_carries_reason_when_nothing_found() -> None:
    result = extract_json("just prose, no JSON", detailed=True)
    assert isinstance(result, JsonExtraction)
    assert result.success is False
    assert result.data is None
    assert "no valid JSON" in result.reason


def test_detailed_reports_success_on_match() -> None:
    result = extract_json('{"x": 1}', detailed=True)
    assert result.success is True
    assert result.data == {"x": 1}
    assert result.reason == ""


# ---------------------------------------------------------------------------
# Schema-aware filtering + normalization
# ---------------------------------------------------------------------------


def test_schema_filters_to_matching_shape() -> None:
    text = '{"foo": 1}\n\n```json\n{"items": [{"date": "x", "description": "y"}]}\n```'
    result = extract_json(text, schema=WC_MEDICAL_SCHEMA["schema"])
    assert isinstance(result, dict)
    assert "items" in result
    assert result["items"][0]["date"] == "x"


def test_schema_normalizes_bare_array_into_wrapper() -> None:
    """Schema wants {items: array}; model returned the bare array — auto-wrap."""
    result = extract_json(WC_MEDICAL_RESPONSE, schema=WC_MEDICAL_SCHEMA["schema"])
    assert isinstance(result, dict)
    assert "items" in result
    assert len(result["items"]) == 2
    assert result["items"][0]["DATE"] == "11/16/2023"


def test_schema_normalizes_wrapper_into_bare_array() -> None:
    """Schema wants array; model returned {key: array} — auto-unwrap."""
    text = '```json\n{"items": [{"a": 1}, {"a": 2}]}\n```'
    schema = {"type": "array", "items": {"type": "object", "required": ["a"]}}
    result = extract_json(text, schema=schema)
    assert isinstance(result, list)
    assert result == [{"a": 1}, {"a": 2}]


def test_schema_returns_none_when_no_candidate_matches() -> None:
    text = '{"only": "object", "no": "items"}'
    result = extract_json(text, schema=WC_MEDICAL_SCHEMA["schema"], detailed=True)
    assert result.success is False
    assert "did not match" in result.reason or "no JSON candidate" in result.reason


# ---------------------------------------------------------------------------
# parse_agent_output + resolve_output_schema
# ---------------------------------------------------------------------------


def test_resolve_output_schema_from_raw_jsonschema() -> None:
    s = {"type": "object", "required": ["a"], "properties": {"a": {"type": "string"}}}
    assert resolve_output_schema(s) is s


def test_resolve_output_schema_from_agent_db_record() -> None:
    record = {"output_schema": WC_MEDICAL_SCHEMA}
    resolved = resolve_output_schema(record)
    assert resolved is WC_MEDICAL_SCHEMA["schema"]


def test_resolve_output_schema_from_response_format_envelope() -> None:
    envelope = {
        "type": "json_schema",
        "json_schema": WC_MEDICAL_SCHEMA,
    }
    resolved = resolve_output_schema(envelope)
    assert resolved is WC_MEDICAL_SCHEMA["schema"]


def test_resolve_output_schema_returns_none_on_garbage() -> None:
    assert resolve_output_schema(None) is None
    assert resolve_output_schema(42) is None
    assert resolve_output_schema({"unrelated": "dict"}) is None


def test_parse_agent_output_with_full_agent_record() -> None:
    """The end-to-end shape the page_extraction route now uses."""
    result = parse_agent_output(WC_MEDICAL_RESPONSE, WC_MEDICAL_SCHEMA)
    assert result.success is True
    assert isinstance(result.data, dict)
    assert "items" in result.data
    assert len(result.data["items"]) == 2


def test_parse_agent_output_without_schema_still_works() -> None:
    """Calling with no source falls back to first-match extraction."""
    result = parse_agent_output(WC_MEDICAL_RESPONSE)
    assert result.success is True
    assert isinstance(result.data, list)


def test_parse_agent_output_never_raises_on_garbage_input() -> None:
    for bad in ["", "   ", "no json", "{{{{ unbalanced", "][", None]:
        result = parse_agent_output(bad or "", WC_MEDICAL_SCHEMA)
        assert isinstance(result, JsonExtraction)
        assert result.success is False
        assert result.data is None


# ---------------------------------------------------------------------------
# extract_model — public surface unchanged
# ---------------------------------------------------------------------------


class _Sample(BaseModel):
    name: str
    count: int


def test_extract_model_validates_pydantic() -> None:
    text = 'noise {"name": "ok", "count": 3} trailing'
    model = extract_model(text, _Sample)
    assert model is not None
    assert model.name == "ok"
    assert model.count == 3


def test_extract_model_returns_none_on_invalid_shape() -> None:
    assert extract_model('{"name": "ok"}', _Sample) is None  # missing count
    assert extract_model("", _Sample) is None
