"""Structured-output schema sanitization for constrained-decoding providers.

Regression for the Cerebras 400 ``wrong_api_format`` — "Invalid fields for
schema with types ['array']: {'minItems', 'maxItems'}" — a schema that works
verbatim on Gemini blew up on a Cerebras model because the ``response_format``
path shipped the schema RAW, unlike the tool-schema path which already strips
these keywords. The fix strips constrained-decoding-unsupported keywords at the
shared OpenAI-compatible ``response_format`` boundary and in the linter's
portable schema. Standalone — imports only matrx_ai.schema + the base translator.
"""

from __future__ import annotations

import pytest

from matrx_ai.providers.anthropic.translator import AnthropicTranslator
from matrx_ai.providers.base_translator import BaseTranslator
from matrx_ai.providers.google.translator import GoogleTranslator
from matrx_ai.providers.openai.translator import OpenAITranslator
from matrx_ai.schema import lint_output_schema
from matrx_ai.schema.rules import (
    STRUCTURED_OUTPUT_UNSUPPORTED_KEYWORDS,
    strip_unsupported_keywords,
    unsupported_structured_output_keywords,
)

# The exact schema shape from the failing /v2/ai/manual request (flashcards).
FAILING_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "cards": {
            "type": "array",
            "items": {"$ref": "#/$defs/flashcard"},
        },
    },
    "required": ["title", "cards"],
    "additionalProperties": False,
    "$defs": {
        "flashcard": {
            "type": "object",
            "properties": {
                "front": {"type": "string"},
                "card_kind": {"type": "string", "enum": ["basic", "cloze"]},
                "tags": {
                    "type": "array",
                    "minItems": 2,
                    "maxItems": 5,
                    "items": {"type": "string", "pattern": "^[a-z0-9\\s_-]+$"},
                },
            },
            "required": ["front", "card_kind", "tags"],
            "additionalProperties": False,
        }
    },
}


def _walk(node):
    yield node
    if isinstance(node, dict):
        for v in node.values():
            yield from _walk(v)
    elif isinstance(node, list):
        for v in node:
            yield from _walk(v)


def _keys_present(schema) -> set[str]:
    present: set[str] = set()
    for node in _walk(schema):
        if isinstance(node, dict):
            present |= set(node.keys())
    return present


def test_strip_removes_unsupported_recursively_including_defs() -> None:
    out = strip_unsupported_keywords(FAILING_SCHEMA)
    present = _keys_present(out)
    assert "minItems" not in present
    assert "maxItems" not in present
    assert "pattern" not in present
    assert "$schema" not in present
    # Structural keywords that DRIVE the grammar must survive.
    assert "$defs" in present and "$ref" in present
    assert "enum" in present and "required" in present
    assert out["$defs"]["flashcard"]["properties"]["tags"]["items"] == {"type": "string"}


def test_strip_does_not_mutate_input() -> None:
    before = FAILING_SCHEMA["$defs"]["flashcard"]["properties"]["tags"]
    assert before["minItems"] == 2  # sanity
    strip_unsupported_keywords(FAILING_SCHEMA)
    assert FAILING_SCHEMA["$defs"]["flashcard"]["properties"]["tags"]["minItems"] == 2


def test_property_named_like_a_keyword_survives() -> None:
    # A user property literally named "pattern" / "default" must NOT be stripped —
    # only schema *keywords* are removed, never property NAMES.
    schema = {
        "type": "object",
        "properties": {
            "pattern": {"type": "string"},
            "default": {"type": "integer"},
        },
        "required": ["pattern", "default"],
    }
    out = strip_unsupported_keywords(schema)
    assert set(out["properties"].keys()) == {"pattern", "default"}
    assert out["properties"]["pattern"] == {"type": "string"}


def _rf(schema: dict) -> dict:
    return {
        "type": "json_schema",
        "json_schema": {"name": "flashcard_set_generator", "schema": schema, "strict": True},
    }


def test_openai_compatible_response_format_has_no_rejected_keywords() -> None:
    # cerebras / groq / xai / together / generic-openai all route through the same
    # shared builder — one assertion covers every OpenAI-compatible provider.
    for provider in ("cerebras", "groq", "xai", "together", "generic_openai"):
        built = BaseTranslator.build_openai_chat_response_format(_rf(FAILING_SCHEMA), provider)
        assert built is not None, provider
        assert built["type"] == "json_schema"
        present = _keys_present(built["json_schema"]["schema"])
        assert not (STRUCTURED_OUTPUT_UNSUPPORTED_KEYWORDS & present), provider
        # Still schema-enforced: object root, defs, strict preserved.
        assert built["json_schema"]["strict"] is True
        assert "$defs" in built["json_schema"]["schema"]


def test_anthropic_output_format_strips_minitems() -> None:
    # The exact production crash: "minItems values other than 0 or 1 are not
    # supported (got: [2, 5])". Must not reach the wire.
    built = AnthropicTranslator._build_anthropic_output_format(_rf(FAILING_SCHEMA))
    assert built is not None
    assert built["type"] == "json_schema"
    present = _keys_present(built["schema"])
    assert "minItems" not in present and "maxItems" not in present and "pattern" not in present
    # Anthropic's own hard rule still enforced (additionalProperties on objects).
    assert built["schema"]["additionalProperties"] is False


def test_openai_responses_text_format_strips_unsupported() -> None:
    built = OpenAITranslator._build_openai_text_format(_rf(FAILING_SCHEMA))
    assert built is not None
    assert built["type"] == "json_schema"
    present = _keys_present(built["schema"])
    assert not (STRUCTURED_OUTPUT_UNSUPPORTED_KEYWORDS & present)


def test_google_keeps_rich_schema_unstripped() -> None:
    # Gemini accepts the rich schema (the original request worked on Gemini) —
    # so "google" strips NOTHING: enforce the most the provider supports.
    assert unsupported_structured_output_keywords("google") == frozenset()
    built = GoogleTranslator._build_google_response_schema(_rf(FAILING_SCHEMA))
    assert built is not None
    present = _keys_present(built)
    assert "minItems" in present and "maxItems" in present and "pattern" in present


def test_every_constrained_provider_default_gets_full_strip() -> None:
    # No constrained provider may silently fall through with the keywords intact.
    for provider in ("cerebras", "groq", "xai", "together", "generic_openai", "anthropic", "openai"):
        assert unsupported_structured_output_keywords(provider) == STRUCTURED_OUTPUT_UNSUPPORTED_KEYWORDS
        sanitized = BaseTranslator.sanitize_structured_output_schema(FAILING_SCHEMA, provider)
        assert not (STRUCTURED_OUTPUT_UNSUPPORTED_KEYWORDS & _keys_present(sanitized)), provider


def test_expected_schema_sanitization_does_not_print(
    capsys: pytest.CaptureFixture[str],
) -> None:
    sanitized = BaseTranslator.sanitize_structured_output_schema(FAILING_SCHEMA, "openai")

    assert sanitized != FAILING_SCHEMA
    assert capsys.readouterr() == ("", "")


def test_linter_portable_schema_keeps_rich_keywords() -> None:
    # Platform intent: SAVE the richest schema untouched; strip only at the
    # provider boundary. The linter's portable schema must therefore PRESERVE
    # advisory keywords (minItems/maxItems/pattern) — they are dropped per-request
    # for the providers that reject them, never baked out of the stored schema.
    report = lint_output_schema(FAILING_SCHEMA)
    portable = report.portable_schema
    assert portable is not None
    present = _keys_present(portable)
    assert "minItems" in present and "maxItems" in present and "pattern" in present
