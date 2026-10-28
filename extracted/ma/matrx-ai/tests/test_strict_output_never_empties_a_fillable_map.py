"""No dynamic-key map a model is asked to fill is ever handed to a strict decoder — optional ones included.

2026-10-27 live: ``research.suggest_setup`` answered ``keyword_goals: {}`` on every run. Its kind's map
was OPTIONAL, and the reroute to prompt-guided JSON only looked at REQUIRED, non-null maps — so the
strict decoder (which narrows every map to ``{}``) left the model no way to write a single key. The
same hole emptied ``list_change_proposal_v1``'s optional ``patch`` (``flashcards.fix_giveaway_cards``:
an "update" that cannot name a changed column), ``keyword_classification_batch_v1``'s nullable
``site_facets``, ``quiz_set``'s ``additionalDetails``, the Workflow Recovery Advisor's ``patch.ops[].data``
and every map reached through ``$defs`` or a union branch. The OpenAI-compatible wires run the same
strict pass whenever the envelope says ``strict: true`` (every kind binding does), and were never checked.
"""

from __future__ import annotations

import contextlib
import io
from types import SimpleNamespace
from typing import Any

import pytest

ANY_MAP: dict[str, Any] = {"type": "object", "additionalProperties": True}
STRING_MAP: dict[str, Any] = {"type": "object", "additionalProperties": {"type": "string"}}

#: Shapes taken from live kinds and agents (census 2026-10-27), each with ONE map a model must fill.
CASES: dict[str, tuple[dict[str, Any], str]] = {
    # research_setup_suggestion before v9: the map was optional.
    "optional map": (
        {"type": "object", "required": ["suggested_keywords"],
         "properties": {"suggested_keywords": {"type": "array", "items": {"type": "string"}},
                        "keyword_goals": STRING_MAP}},
        "$.keyword_goals",
    ),
    # keyword_classification_batch_v1: results[].site_facets is optional AND nullable.
    "nullable map in array items": (
        {"type": "object", "required": ["results"],
         "properties": {"results": {"type": "array", "items": {
             "type": "object", "required": ["keyword"],
             "properties": {"keyword": {"type": "string"},
                            "site_facets": {"type": ["object", "null"],
                                            "additionalProperties": {"type": ["string", "null"]}}}}}}},
        "$.results[].site_facets",
    ),
    # list_change_proposal_v1: the item (with its optional `patch` map) lives in $defs.
    "map inside $defs": (
        {"type": "object", "required": ["items"],
         "properties": {"items": {"type": "array", "items": {"$ref": "#/$defs/item"}}},
         "$defs": {"item": {"type": "object", "required": ["op"],
                            "properties": {"op": {"type": "string"}, "patch": ANY_MAP}}}},
        "$.$defs.item.patch",
    ),
    # Optional[dict[str, str]] spelled as a union.
    "map inside anyOf": (
        {"type": "object", "required": ["name"],
         "properties": {"name": {"type": "string"},
                        "headers": {"anyOf": [STRING_MAP, {"type": "null"}]}}},
        "$.headers.anyOf[0]",
    ),
}


def _quiet(fn: Any, *args: Any, **kwargs: Any) -> Any:
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return fn(*args, **kwargs)


def _caps() -> Any:
    from matrx_ai.providers.resolved_capabilities import resolve_model_capabilities

    return resolve_model_capabilities(SimpleNamespace(
        name="test-model",
        capabilities={"input": ["text"], "output": ["text"], "features": ["function_calling", "structured_output"]}))


def _sent(schema: dict[str, Any], wire_format: str, *, strict: bool = True) -> dict[str, Any]:
    from matrx_ai.config import UnifiedConfig
    from matrx_ai.providers.structured_output_findings import simulating_gates
    from matrx_ai.providers.unified_client import _downgrade_response_format

    rf = {"type": "json_schema", "json_schema": {"name": "probe", "schema": schema, "strict": strict}}
    config = UnifiedConfig(model="test-model", messages=[], response_format=rf)
    # A gate run leaves its finding pending for the call's flush; there is no call here, so none is kept.
    with simulating_gates():
        _quiet(_downgrade_response_format, config, _caps(), wire_format)
    return config.response_format


@pytest.mark.parametrize("case", sorted(CASES))
def test_every_fillable_map_is_named(case: str) -> None:
    from matrx_ai.schema.rules import forced_empty_maps

    schema, path = CASES[case]
    assert path in forced_empty_maps(schema), f"{case}: {path} would be emptied without anyone saying so"


@pytest.mark.parametrize("wire_format", ["anthropic_chat", "openai_chat", "groq_chat", "cerebras_chat", "xai_chat"])
@pytest.mark.parametrize("case", sorted(CASES))
def test_a_fillable_map_never_reaches_a_strict_decoder(case: str, wire_format: str) -> None:
    schema, path = CASES[case]
    sent = _sent(schema, wire_format)
    assert sent == {"type": "json_object"}, (
        f"{case} on {wire_format}: {path} was sent to a decoder that narrows it to {{}}: {sent}")


def test_a_non_strict_openai_compatible_request_keeps_its_schema() -> None:
    # Without `strict: true` these endpoints accept a map as declared, so it stays enforceable.
    schema, _ = CASES["optional map"]
    assert _sent(schema, "groq_chat", strict=False)["type"] == "json_schema"


def test_an_unreferenced_defs_map_does_not_cost_the_schema_its_grammar() -> None:
    # The translators prune an unreferenced $defs entry before the wire, so its map is never narrowed.
    schema = {"type": "object", "required": ["verdict"], "properties": {"verdict": {"type": "string"}},
              "$defs": {"unused": {"type": "object", "properties": {"m": ANY_MAP}}}}
    from matrx_ai.schema.rules import forced_empty_maps

    assert forced_empty_maps(schema) == []
    assert _sent(schema, "anthropic_chat")["type"] == "json_schema"


def test_a_schema_without_maps_stays_strict() -> None:
    schema = {"type": "object", "required": ["verdict"],
              "properties": {"verdict": {"type": "string"}, "notes": {"type": ["string", "null"]},
                             "closed": {"type": "object", "properties": {"a": {"type": "string"}}}}}
    from matrx_ai.schema.rules import forced_empty_maps

    assert forced_empty_maps(schema) == []
    for wire_format in ("anthropic_chat", "openai_chat", "groq_chat"):
        assert _sent(schema, wire_format)["type"] == "json_schema"
