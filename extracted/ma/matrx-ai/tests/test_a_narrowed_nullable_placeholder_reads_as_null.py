"""A nullable field the boundary NARROWED to non-null comes back as the null the author allows.

Anthropic caps a request at 16 union parameters, and a "compiled grammar too large" refusal
narrows EVERY nullable field (`collapse_nullable_unions(keep=0)`). The wire then forces an
object where the author allowed `null`, and the wire copy has lost `minLength` / `minItems`
(stripped as unsupported), so the model fills an empty placeholder: `{"source": "",
"key_path": []}`. That placeholder fails the declared branch, and 33 answers of
`extend.formula_author` (claude-sonnet-5-5, 2026-11-12..19) were filed
`structured_output.answer_off_contract` for the boundary's own compromise — "the translated
wire schema and the declared schema have diverged; the divergence is the bug".

The reader's half (like `prune_optional_nulls` for `enforce_all_required`): a value that
carries no information, fails the declared schema, at a property whose declared schema admits
`null`, reads as `null`. Anything carrying content, or a property that does not allow `null`,
is still judged and still reported.
"""

from __future__ import annotations

from matrx_ai.schema.answer_contract import verify_answer
from matrx_ai.schema.rules import prune_optional_nulls

SCHEMA = {
    "type": "object",
    "properties": {
        "mode": {"type": "string", "enum": ["next_data", "manual_css"]},
        "next_data": {"anyOf": [{"$ref": "#/$defs/NextData"}, {"type": "null"}]},
        "manual_css": {"anyOf": [{"$ref": "#/$defs/ManualCss"}, {"type": "null"}]},
        "required_block": {"$ref": "#/$defs/NextData"},
    },
    "required": ["mode", "next_data", "manual_css"],
    "additionalProperties": False,
    "$defs": {
        "NextData": {
            "type": "object",
            "properties": {
                "source": {"type": "string", "minLength": 1},
                "key_path": {"type": "array", "items": {"type": "string"}, "minItems": 1},
            },
            "required": ["source", "key_path"],
            "additionalProperties": False,
        },
        "ManualCss": {
            "type": "object",
            "properties": {
                "list_root_selector": {"type": "string", "minLength": 1},
                "fields": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "minLength": 1},
                            "is_list": {"type": "boolean"},
                        },
                        "required": ["name", "is_list"],
                    },
                },
            },
            "required": ["list_root_selector", "fields"],
            "additionalProperties": False,
        },
    },
}


def test_live_placeholders_at_narrowed_nullable_fields_are_on_contract() -> None:
    # The exact answer shape filed 2026-11-19 04:00Z / 04:54Z.
    answer = {
        "mode": "next_data",
        "next_data": {"source": "__NEXT_DATA__", "key_path": ["props"]},
        "manual_css": {"fields": [{"name": "", "is_list": False}], "list_root_selector": ""},
    }
    assert verify_answer(answer, SCHEMA) == []
    pruned = prune_optional_nulls(answer, SCHEMA)
    assert pruned["manual_css"] is None
    assert pruned["next_data"] == {"source": "__NEXT_DATA__", "key_path": ["props"]}

    both_empty = {
        "mode": "manual_css",
        "next_data": {"source": "", "key_path": []},
        "manual_css": {"fields": [], "list_root_selector": ""},
    }
    assert verify_answer(both_empty, SCHEMA) == []


def test_a_placeholder_with_content_is_still_reported() -> None:
    answer = {
        "mode": "next_data",
        "next_data": {"source": "", "key_path": ["props"]},  # content: not a placeholder
        "manual_css": None,
    }
    problems = verify_answer(answer, SCHEMA)
    assert problems and problems[0].startswith("$.next_data")


def test_an_empty_value_where_null_is_not_allowed_is_still_reported() -> None:
    answer = {
        "mode": "next_data",
        "next_data": None,
        "manual_css": None,
        "required_block": {"source": "", "key_path": []},
    }
    problems = verify_answer(answer, SCHEMA)
    assert problems and problems[0].startswith("$.required_block")


def test_an_empty_value_the_declared_schema_accepts_is_kept() -> None:
    schema = {
        "type": "object",
        "properties": {"tags": {"anyOf": [{"type": "array", "items": {"type": "string"}}, {"type": "null"}]}},
    }
    assert prune_optional_nulls({"tags": []}, schema) == {"tags": []}
