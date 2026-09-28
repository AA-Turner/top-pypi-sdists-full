"""A BATCH payload passes the same capability gates as a live call.

THE FAILURE THIS EXISTS TO CATCH. ``UnifiedAIClient.translate_request`` is the
build-only chokepoint the platform's Batch system sends through:

    matrx_ai.agents.batch_render.render_agent_provider_request
      → aidream.services.mandates.batch_lane / ai_execution.run_policies
      → matrx_batch.{anthropic,openai,google}_batch  (the real POST)

Until 2026-09-27 it applied NONE of the capability gates ``_execute_dispatch``
applies — no ``_downgrade_response_format``, no web-search/JSON-mode resolution,
no tool/structured-output conflict, no leaked-tool guard. So an agent bound to a
schema and assigned a model whose ``structured_output_mode`` is not ``SCHEMA``
produced a batch item carrying a raw ``json_schema``: a provider 400 on a paid,
deferred item, discovered hours later, with no finding naming the agent.

Arman, 2026-09-27: *the shape we hold is modified by each provider's translator;
a provider rejecting our request is OUR translator's bug.*

These tests render through the REAL batch-render seam and the REAL translators,
with only the catalog resolve stubbed (the model's declared capabilities are the
input under test). They fail on the pre-fix ``unified_client.py``.
"""

from __future__ import annotations

import json

import pytest

from matrx_ai.agents import Agent
from matrx_ai.catalog.controls import CompiledControlsMap
from matrx_ai.catalog.models import ResolvedCallProfile
from matrx_ai.config import UnifiedConfig
from matrx_ai.providers.resolved_capabilities import (
    ResolvedModelCapabilities,
    StructuredOutputMode,
)

SCHEMA = {
    "type": "object",
    "properties": {"answer": {"type": "string"}},
    "required": ["answer"],
    "additionalProperties": False,
}


def _capabilities(
    mode: StructuredOutputMode, *, supports_function_calling: bool = True
) -> ResolvedModelCapabilities:
    return ResolvedModelCapabilities(
        model_name="probe-model",
        supports_text_input=True,
        supports_vision=False,
        supports_audio_input=False,
        produces_text=True,
        produces_image=False,
        produces_video=False,
        produces_audio=False,
        produces_embedding=False,
        produces_decision=False,
        supports_function_calling=supports_function_calling,
        supports_web_search=False,
        native_capabilities=frozenset(),
        structured_output_mode=mode,
        interaction="turn",
        multilingual=True,
    )


def _profile(
    mode: StructuredOutputMode,
    *,
    wire_format: str = "openai_chat",
    supports_function_calling: bool = True,
) -> ResolvedCallProfile:
    return ResolvedCallProfile(
        model_id="m1",
        model_name="probe-model",
        provider_model_id="probe-model",
        offering_id="off1",
        endpoint_id="ep1",
        api_id="api1",
        provider_name="Probe",
        vendor="openai",
        wire_format=wire_format,
        client_attr=wire_format,
        capabilities=_capabilities(mode, supports_function_calling=supports_function_calling),
        controls=CompiledControlsMap(),
    )


def _stub_resolve(monkeypatch, profile: ResolvedCallProfile) -> None:
    async def _fake(model_ref, offering_id=None, **kwargs):
        return profile

    monkeypatch.setattr("matrx_ai.catalog.resolve.resolve_call_profile", _fake)


def _schema_bound_agent() -> Agent:
    config = UnifiedConfig(model="probe-model", messages=[])
    config.append_user_message("hi")
    config.response_format = {
        "type": "json_schema",
        "json_schema": {"name": "answer", "schema": SCHEMA, "strict": True},
    }
    return Agent(config=config)


async def _rendered_payload(monkeypatch, profile: ResolvedCallProfile) -> dict:
    from matrx_ai.agents.batch_render import render_agent_provider_request

    _stub_resolve(monkeypatch, profile)
    rendered = await render_agent_provider_request(_schema_bound_agent())
    return rendered.payload


@pytest.mark.asyncio
async def test_batch_payload_for_a_json_mode_model_carries_no_raw_schema(monkeypatch):
    """A model declaring ``json`` (json_object only) must receive json_object.

    Pre-fix this payload carried ``text.format.type == "json_schema"`` with the
    full schema — the exact body the provider refuses.
    """
    payload = await _rendered_payload(monkeypatch, _profile(StructuredOutputMode.JSON))
    blob = json.dumps(payload)
    assert "json_schema" not in blob, f"raw schema reached a json-mode batch payload: {blob}"
    assert payload["text"]["format"] == {"type": "json_object"}


@pytest.mark.asyncio
async def test_batch_payload_for_a_text_only_model_carries_no_schema(monkeypatch):
    """``structured_output_mode = text`` → no output contract on the wire at all."""
    payload = await _rendered_payload(monkeypatch, _profile(StructuredOutputMode.TEXT))
    blob = json.dumps(payload)
    assert "json_schema" not in blob, f"raw schema reached a text-only batch payload: {blob}"
    assert payload.get("text", {}).get("format", {}).get("type") != "json_schema"


@pytest.mark.asyncio
async def test_batch_payload_for_a_schema_model_keeps_the_schema(monkeypatch):
    """The gate ADJUSTS, it does not strip: a SCHEMA model still gets the schema.

    Without this half, `assert "json_schema" not in blob` above would pass on a
    translate path that dropped every contract.
    """
    payload = await _rendered_payload(monkeypatch, _profile(StructuredOutputMode.SCHEMA))
    assert payload["text"]["format"]["type"] == "json_schema"
    assert payload["text"]["format"]["schema"]["properties"]["answer"]["type"] == "string"


@pytest.mark.asyncio
async def test_a_batch_translation_records_its_structured_output_finding(monkeypatch):
    """Nothing fails silently: a narrowing made while rendering a BATCH payload
    lands in the same ``structured_output.*`` issue class a live call produces.

    The live path opens the findings buffer in ``_dispatch_with_billing_net``,
    which a build-only translate never reaches — so pre-fix a translator's
    ``note_translation`` during a batch render went into a closed buffer and was
    dropped on the floor.
    """
    from matrx_ai.providers import OpenAITranslator
    from matrx_ai.providers.structured_output_findings import note_translation

    recorded: list[tuple[str, dict]] = []

    async def _fake_capture(key, **kwargs):
        recorded.append((key, kwargs))

    monkeypatch.setattr("matrx_ai.ops.issue_capture.capture_issue", _fake_capture)

    real_build = OpenAITranslator.build_request

    def _build(self, config, profile):
        note_translation(
            "openai",
            narrowed=["probe.narrowed_field"],
            response_format=getattr(config, "response_format", None),
        )
        return real_build(self, config, profile)

    monkeypatch.setattr(OpenAITranslator, "build_request", _build)

    await _rendered_payload(monkeypatch, _profile(StructuredOutputMode.SCHEMA))

    assert [key for key, _ in recorded] == ["structured_output.narrowed"], (
        f"a batch render's translation finding was not recorded: {recorded}"
    )
    detail = recorded[0][1]["detail"]
    assert detail["narrowed"] == ["probe.narrowed_field"]
    assert detail["schema_name"] == "answer"
