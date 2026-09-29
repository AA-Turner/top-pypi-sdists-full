"""The Gemini BATCH request is spelled by the ONE Google translator — and loses
nothing silently.

THE BUG (verified 2026-09-27). The batch transport (``matrx_batch.google_batch``)
carried its own second Google schema translator, ``_mirror_response_schema``: it
deleted every keyword on a deny-list, so ``additionalProperties`` vanished from
3,823 and ``$ref`` from 565 of 4,000 live schemas, 809 live schemas came out in a
shape the SDK's own ``Schema`` validator refuses, and nothing was recorded. The
batch spelling now lives in ``GoogleTranslator.to_batch_request`` (Arman,
2026-09-27: "we have translators for each schema type … Fix it at the core").

Why a batch spelling exists at all, measured live 2026-09-27: the Batch API
accepts ``response_json_schema`` and ignores it (0/26 conforming on
gemini-3.6/3.8-flash, the 2026-08-15 CRM failure re-run), and its
``response_schema`` is the OpenAPI ``Schema`` message, which has no
``additionalProperties`` field (``400 Unknown name "additional_properties"``).

The Schema-message field list below is restated from Google's refusal and the
v1beta ``Schema`` message — deliberately NOT imported from the code under test.
"""

from __future__ import annotations

import json
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.agents import Agent
from matrx_ai.catalog.controls import CompiledControlsMap
from matrx_ai.catalog.models import ResolvedCallProfile
from matrx_ai.config import UnifiedConfig
from matrx_ai.providers.resolved_capabilities import (
    ResolvedModelCapabilities,
    StructuredOutputMode,
)

GEMINI_SCHEMA_MESSAGE_FIELDS = {
    "type", "format", "title", "description", "nullable", "enum", "items",
    "minItems", "maxItems", "properties", "required", "minProperties",
    "maxProperties", "minLength", "maxLength", "pattern", "minimum", "maximum",
    "anyOf", "propertyOrdering", "default", "example",
}

# The exact schema whose loss dead-lettered 12 CRM items on 2026-08-15.
PARTY_KIND = {
    "type": "object",
    "required": ["verdict", "confidence", "rationale"],
    "additionalProperties": False,
    "properties": {
        "verdict": {"enum": ["person", "organization", "unknown"], "type": "string"},
        "confidence": {"enum": ["high", "medium", "low"], "type": "string"},
        "rationale": {"type": "string"},
    },
}

REF_AND_MAP = {
    "type": "object",
    "additionalProperties": False,
    "required": ["person", "scores"],
    "$defs": {
        "Name": {
            "type": "object",
            "additionalProperties": False,
            "required": ["given", "family"],
            "properties": {"given": {"type": "string"}, "family": {"type": ["string", "null"]}},
        }
    },
    "properties": {
        "person": {"$ref": "#/$defs/Name", "description": "who"},
        "scores": {"type": "object", "additionalProperties": {"type": "number"}},
        "shape": {"oneOf": [{"const": "circle"}, {"const": "square"}]},
    },
}


def to_gemini_batch_schema(schema: dict[str, Any], **notes: Any) -> dict[str, Any]:
    # Imported per call so the render-path tests below still run (and fail by
    # assertion) on a revision that has no batch spelling at all.
    from matrx_ai.providers.google.batch_schema import to_gemini_batch_schema as convert

    return convert(schema, **notes)


def _foreign_fields(node: Any, path: str = "$") -> list[str]:
    bad: list[str] = []
    if isinstance(node, dict):
        bad += [f"{path}.{k}" for k in node if k not in GEMINI_SCHEMA_MESSAGE_FIELDS]
        for name, sub in (node.get("properties") or {}).items():
            bad += _foreign_fields(sub, f"{path}.properties.{name}")
        if isinstance(node.get("items"), dict):
            bad += _foreign_fields(node["items"], f"{path}.items")
        for i, branch in enumerate(node.get("anyOf") or []):
            bad += _foreign_fields(branch, f"{path}.anyOf[{i}]")
    return bad


def _sdk_batch_wire(schema: dict[str, Any]) -> dict[str, Any]:
    """Google's own Batch wire converter — raises on what it cannot send."""
    from google.genai import batches, types

    req = types.InlinedRequest(
        contents=[{"role": "user", "parts": [{"text": "x"}]}],
        config={"response_mime_type": "application/json", "response_schema": json.loads(json.dumps(schema))},
        metadata={"custom_id": "t"},
    )
    return batches._InlinedRequest_to_mldev(SimpleNamespace(vertexai=False), req)


# ── the converter ─────────────────────────────────────────────────────────


def test_the_party_kind_contract_survives_whole() -> None:
    out = to_gemini_batch_schema(PARTY_KIND)
    assert out["required"] == ["verdict", "confidence", "rationale"]
    assert out["properties"]["verdict"]["enum"] == ["person", "organization", "unknown"]
    assert set(out["properties"]) == {"verdict", "confidence", "rationale"}
    assert _foreign_fields(out) == []


def test_refs_are_inlined_and_closed_objects_stay_closed_without_a_finding() -> None:
    narrowed: list[str] = []
    relaxed: list[str] = []
    out = to_gemini_batch_schema(REF_AND_MAP, narrowed=narrowed, relaxed=relaxed)

    person = out["properties"]["person"]
    assert person["required"] == ["given", "family"], "the $ref body was not inlined"
    assert person["description"] == "who", "a sibling beside $ref must refine the target"
    assert person["properties"]["family"] == {"type": "string", "nullable": True}
    assert "$ref" not in json.dumps(out)
    assert _foreign_fields(out) == []
    # additionalProperties:false is carried by the closed Schema object — lossless.
    assert not any("person" in n or n.startswith("$.additionalProperties") for n in narrowed + relaxed)


def test_what_the_schema_message_cannot_say_is_recorded_by_path() -> None:
    narrowed: list[str] = []
    relaxed: list[str] = []
    out = to_gemini_batch_schema(REF_AND_MAP, narrowed=narrowed, relaxed=relaxed)

    assert any(n.startswith("$.properties.scores.additionalProperties") for n in narrowed), narrowed
    assert any(n.startswith("$.properties.shape.oneOf") for n in relaxed), relaxed
    assert out["properties"]["shape"]["anyOf"] == [
        {"type": "string", "enum": ["circle"]},
        {"type": "string", "enum": ["square"]},
    ]


def test_recursion_is_unrolled_and_recorded() -> None:
    tree = {
        "type": "object",
        "required": ["root"],
        "$defs": {
            "Node": {
                "type": "object",
                "required": ["label"],
                "properties": {
                    "label": {"type": "string"},
                    "children": {"type": "array", "items": {"$ref": "#/$defs/Node"}},
                },
            }
        },
        "properties": {"root": {"$ref": "#/$defs/Node"}},
    }
    relaxed: list[str] = []
    out = to_gemini_batch_schema(tree, relaxed=relaxed)
    assert "$ref" not in json.dumps(out)
    assert out["properties"]["root"]["properties"]["children"]["items"]["properties"]["label"]
    assert any("unrolled" in n for n in relaxed), relaxed
    _sdk_batch_wire(out)


@pytest.mark.parametrize("schema", [PARTY_KIND, REF_AND_MAP])
def test_googles_own_batch_wire_converter_accepts_the_output(schema: dict[str, Any]) -> None:
    wire = _sdk_batch_wire(to_gemini_batch_schema(schema))
    assert wire["request"]["generationConfig"]["responseSchema"].properties
    assert "responseJsonSchema" not in wire["request"]["generationConfig"]


def test_the_input_is_never_mutated() -> None:
    before = json.dumps(REF_AND_MAP, sort_keys=True)
    to_gemini_batch_schema(REF_AND_MAP)
    assert json.dumps(REF_AND_MAP, sort_keys=True) == before


# ── through the real batch render seam ─────────────────────────────────────


def _google_profile() -> ResolvedCallProfile:
    caps = ResolvedModelCapabilities(
        model_name="gemini-probe",
        supports_text_input=True,
        supports_vision=False,
        supports_audio_input=False,
        produces_text=True,
        produces_image=False,
        produces_video=False,
        produces_audio=False,
        produces_embedding=False,
        produces_decision=False,
        supports_function_calling=False,
        supports_web_search=False,
        native_capabilities=frozenset(),
        structured_output_mode=StructuredOutputMode.SCHEMA,
        interaction="turn",
        multilingual=True,
    )
    return ResolvedCallProfile(
        model_id="m1",
        model_name="gemini-probe",
        provider_model_id="gemini-probe",
        offering_id="off1",
        endpoint_id="ep1",
        api_id="api1",
        provider_name="Google",
        vendor="google",
        wire_format="google_chat",
        client_attr="google_chat",
        capabilities=caps,
        controls=CompiledControlsMap(),
    )


def _agent(schema: dict[str, Any], name: str) -> Agent:
    config = UnifiedConfig(model="gemini-probe", messages=[])
    config.append_user_message("hi")
    config.response_format = {
        "type": "json_schema",
        "json_schema": {"name": name, "schema": schema, "strict": True},
    }
    return Agent(config=config)


def _stub_resolve(monkeypatch) -> None:
    async def _fake(model_ref, offering_id=None, **kwargs):
        return _google_profile()

    monkeypatch.setattr("matrx_ai.catalog.resolve.resolve_call_profile", _fake)


@pytest.mark.asyncio
async def test_a_google_batch_render_carries_the_schema_on_the_field_batch_enforces(monkeypatch):
    from matrx_ai.agents.batch_render import render_agent_provider_request

    _stub_resolve(monkeypatch)
    rendered = await render_agent_provider_request(_agent(PARTY_KIND, "party_kind"))
    config = rendered.payload["config"]
    assert config.response_json_schema is None, (
        "the Batch API accepts response_json_schema and IGNORES it — 12 dead items, 2026-08-15"
    )
    assert config.response_schema["properties"]["verdict"]["enum"] == ["person", "organization", "unknown"]
    assert config.response_mime_type == "application/json"


@pytest.mark.asyncio
async def test_a_google_batch_render_records_what_it_could_not_say(monkeypatch):
    from matrx_ai.agents.batch_render import render_agent_provider_request

    recorded: list[tuple[str, dict]] = []

    async def _fake_capture(key, **kwargs):
        recorded.append((key, kwargs))

    monkeypatch.setattr("matrx_ai.ops.issue_capture.capture_issue", _fake_capture)
    _stub_resolve(monkeypatch)
    await render_agent_provider_request(_agent(REF_AND_MAP, "person_scores"))

    # One finding per call, classed by its worst entry (here `relaxed`, the oneOf),
    # carrying both lists — the map narrowing included.
    assert [key for key, _ in recorded] == ["structured_output.relaxed"], recorded
    detail = recorded[0][1]["detail"]
    assert detail["schema_name"] == "person_scores"
    assert any("scores" in n for n in detail["narrowed"]), detail
    assert any("shape.oneOf" in n for n in detail["relaxed"]), detail


@pytest.mark.asyncio
async def test_the_live_request_is_unchanged(monkeypatch):
    """Only the batch spelling moves the schema; a live call keeps the raw field."""
    from matrx_ai.orchestrator.requests import AIMatrixRequest
    from matrx_ai.providers.unified_client import UnifiedAIClient

    _stub_resolve(monkeypatch)
    agent = _agent(PARTY_KIND, "party_kind")
    payload = await UnifiedAIClient().translate_request(
        AIMatrixRequest(conversation_id="t", config=agent.config)
    )
    assert payload["config"].response_json_schema["required"] == ["verdict", "confidence", "rationale"]
    assert payload["config"].response_schema is None
