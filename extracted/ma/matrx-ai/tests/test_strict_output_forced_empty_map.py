"""A REQUIRED dynamic-key map in a bound Output Schema is never sent to a strict decoder.

2026-10-24 live (server 4b26943bec72): an agent whose Output Schema is the ``visual_map``
kind (``spec`` is ``dict[str, Any]``) answered ``"spec": {}`` on Haiku 5.5 and Sonnet 5.5.
The Anthropic translator narrows every map to ``{}`` with ``additionalProperties: false``,
so the grammar FORCED the empty spec; the repair loop then only ever checked
``{diagram_type, schema_version}`` (the identity it fills) and nothing could be drawn.
The schema below is the live agent's stored ``output_schema``, verbatim in shape.
"""

from __future__ import annotations

import asyncio
import contextlib
import io
from types import SimpleNamespace
from typing import Any

LIVE_VISUAL_MAP_OUTPUT_SCHEMA: dict[str, Any] = {
    "name": "visual_map",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            "spec": {"type": "object", "properties": {}, "required": [], "additionalProperties": True,
                     "description": "The typed diagram spec for that type."},
            "type": {"type": "string", "enum": ["architecture", "workflow", "sequence", "dataflow", "lifecycle",
                                                 "erd", "class", "tree", "timeline", "waterfall"]},
            "issues": {"type": "number"},
            "receipt": {"type": ["object", "null"], "properties": {}, "required": [],
                        "additionalProperties": True, "default": None},
            "verified": {"type": "boolean"},
            "inspection_id": {"type": ["string", "null"], "default": None},
            "__kind": {"type": "string", "const": "visual_map"},
        },
        "required": ["__kind", "spec", "type", "issues", "verified"],
        "additionalProperties": False,
    },
}


def _quiet(fn: Any, *args: Any, **kwargs: Any) -> Any:
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return fn(*args, **kwargs)


def _caps(features: list[str]) -> Any:
    from matrx_ai.providers.resolved_capabilities import resolve_model_capabilities

    return resolve_model_capabilities(SimpleNamespace(
        name="test-model", capabilities={"input": ["text"], "output": ["text"], "features": features}))


def test_forced_empty_maps_names_every_map() -> None:
    from matrx_ai.schema.rules import forced_empty_maps

    # `receipt` is a nullable map: the strict decoder empties it too, so it is named as well.
    assert forced_empty_maps(LIVE_VISUAL_MAP_OUTPUT_SCHEMA["schema"]) == ["$.spec", "$.receipt"]
    assert forced_empty_maps({"type": "object", "properties": {"a": {"type": "string"}}, "required": ["a"]}) == []


def _final_wire_spec(wire_format: str) -> tuple[Any, dict[str, Any] | None]:
    """What the provider would be told ``spec`` may hold, after the capability gate ran."""
    from matrx_ai.config import UnifiedConfig
    from matrx_ai.providers.anthropic.translator import AnthropicTranslator
    from matrx_ai.providers.unified_client import _downgrade_response_format

    config = UnifiedConfig(model="test-model", messages=[],
                           response_format={"type": "json_schema", "json_schema": LIVE_VISUAL_MAP_OUTPUT_SCHEMA})
    _quiet(_downgrade_response_format, config, _caps(["function_calling", "structured_output"]), wire_format)
    fmt = _quiet(AnthropicTranslator._build_anthropic_output_format, config.response_format)
    return config, (fmt or {}).get("schema", {}).get("properties", {}).get("spec") if fmt else None


def test_a_required_map_is_never_handed_to_the_strict_decoder() -> None:
    async def drive() -> tuple[Any, Any]:
        import matrx_ai.providers.structured_output_findings as findings

        recorded: list[tuple[str, dict[str, Any]]] = []
        original = findings.record_structured_output_finding

        async def capture(key: str, **kwargs: Any) -> None:
            recorded.append((key, kwargs))

        findings.record_structured_output_finding = capture  # type: ignore[assignment]
        try:
            config, wire_spec = _final_wire_spec("anthropic_chat")
            await findings.flush_translation_findings(model="test-model", succeeded=True)
            return (config, wire_spec), recorded
        finally:
            findings.record_structured_output_finding = original  # type: ignore[assignment]

    (config, wire_spec), recorded = asyncio.run(drive())
    # Today's code sent `spec` as {"properties": {}, "additionalProperties": false}: forced empty.
    assert wire_spec is None, f"the strict decoder was still told spec must be empty: {wire_spec}"
    assert config.response_format == {"type": "json_object"}, config.response_format
    staged = config.messages.render_turn_context() or ""
    assert "JSON Schema:" in staged and '"spec"' in staged, "the declared contract never reached the prompt"
    actions = [kw.get("detail", {}).get("action", "") for k, kw in recorded if k.endswith("enforcement_dropped")]
    assert any("$.spec" in a for a in actions), f"the downgrade was not recorded by name: {recorded}"


def test_a_schema_without_required_maps_stays_strict() -> None:
    from matrx_ai.config import UnifiedConfig
    from matrx_ai.providers.unified_client import _downgrade_response_format

    schema = {"type": "object", "required": ["verdict"], "properties": {"verdict": {"type": "string"}}}
    rf = {"type": "json_schema", "name": "verdict", "schema": schema}
    config = UnifiedConfig(model="test-model", messages=[], response_format=dict(rf))
    _quiet(_downgrade_response_format, config, _caps(["function_calling", "structured_output"]), "anthropic_chat")
    assert config.response_format == rf
