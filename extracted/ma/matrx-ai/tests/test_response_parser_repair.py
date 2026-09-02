"""The repair tier of the JSON extraction funnel.

Regression cover for the `study_pack_v1` `parse_notes` failures of 2026-08-19
(workflow runs cc0ed65a… and 5285c24c…): the notes agent returned a complete,
correct study-notes document whose long `overview` prose contained an
unescaped nested quote — `called the "powerhouse of the cell."` — so strict
`json.loads` rejected the whole document. The brace-walker then surfaced only
the inner `sections`/`glossary` arrays, none of which satisfy a schema
requiring a top-level `sections` key, and the run died on a good answer.

The rules these tests pin:
  1. A strictly-parseable candidate always wins; repair never outranks it.
  2. Repair fires when nothing STRICT matched the schema — not merely when
     nothing parsed at all (the failure above parsed fragments just fine).
  3. Repair never invents a match out of text that holds no JSON.
"""

from __future__ import annotations

from matrx_ai.agents.response_parser import extract_json

NOTES_SCHEMA = {"type": "object", "required": ["sections"]}

# The exact malformation, both shapes seen in production.
UNESCAPED_INNER_QUOTE = (
    '{"title": "Cellular Respiration",'
    ' "overview": "The mitochondria are called the "powerhouse of the cell."",'
    ' "sections": [{"heading": "Glycolysis", "key_points": ["Occurs in the cytosol."]}],'
    ' "glossary": [{"term": "ATP", "definition": "Energy currency."}]}'
)

EARLY_OBJECT_CLOSE = (
    '{"title":"Cellular Respiration",'
    '"overview":"...considered the "powerhouse of the cell."},'
    '"sections":[{"heading":"Glycolysis","key_points":["Occurs in the cytosol."]}],'
    '"glossary":[{"term":"ATP","definition":"Energy currency."}]}'
)


def test_recovers_unescaped_nested_quote_against_schema() -> None:
    result = extract_json(UNESCAPED_INNER_QUOTE, schema=NOTES_SCHEMA, detailed=True)
    assert result.success, result.reason
    assert result.data["title"] == "Cellular Respiration"
    assert len(result.data["sections"]) == 1
    assert result.data["sections"][0]["heading"] == "Glycolysis"


def test_recovers_object_closed_one_key_early() -> None:
    result = extract_json(EARLY_OBJECT_CLOSE, schema=NOTES_SCHEMA, detailed=True)
    assert result.success, result.reason
    assert len(result.data["sections"]) == 1
    assert result.data["glossary"][0]["term"] == "ATP"


def test_repair_fires_even_when_fragments_parsed_strictly() -> None:
    """The real defect: strict candidates existed, they just missed the schema."""
    from matrx_ai.agents.response_parser import _collect_candidates

    strict = _collect_candidates(UNESCAPED_INNER_QUOTE)
    assert strict, "precondition: the brace-walker finds the inner arrays"
    assert not any(
        isinstance(c, dict) and "sections" in c for c in strict
    ), "precondition: no strict candidate satisfies the schema"

    assert extract_json(UNESCAPED_INNER_QUOTE, schema=NOTES_SCHEMA) is not None


def test_strict_parse_still_wins() -> None:
    clean = '{"sections": [{"heading": "Strict"}]}'
    assert extract_json(clean, schema=NOTES_SCHEMA)["sections"][0]["heading"] == "Strict"


def test_fenced_block_unaffected() -> None:
    fenced = '```json\n{"sections": [1, 2]}\n```'
    assert extract_json(fenced, schema=NOTES_SCHEMA) == {"sections": [1, 2]}


def test_prose_with_no_json_still_fails() -> None:
    result = extract_json("There is no JSON here at all.", schema=NOTES_SCHEMA, detailed=True)
    assert not result.success
    # The reason must name the repair tier as the thing that ran and came back
    # empty — a bare "no JSON found" would read as "we never tried". The exact
    # wording changed with the repair-never-fabricates fix (ca2b1b225); assert
    # the two facts that matter, not one frozen sentence.
    assert "json-repair" in result.reason
    assert "nothing faithful" in result.reason


def test_prose_with_no_json_and_no_schema_still_fails() -> None:
    assert extract_json("There is no JSON here at all.") is None


def test_empty_input_short_circuits_before_repair() -> None:
    result = extract_json("   ", detailed=True)
    assert not result.success
    assert result.reason == "empty input"
