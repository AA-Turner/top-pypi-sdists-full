"""A BATCH answer passes the SAME answer step a live answer does.

THE FAILURE THIS EXISTS TO CATCH. Every live answer passes
``UnifiedAIClient._dispatch_with_billing_net``, where
``conform_answer_to_contract`` rewrites it to the AUTHOR's shape (a ``null`` the
provider boundary asked for becomes the absence the author declared) and
``verify_answer_and_record`` judges it against the author's contract. A batch
answer never passes that seam: it is rendered by
``batch_render.render_agent_provider_request``, sent by matrx-batch, and read
hours later by a result handler through ``output_text_from_batch_result``. Until
2026-09-28 nothing in between conformed or checked it, so every batch consumer
received ``null`` where the author said "absent" (the kind validator rejects
that) and an off-contract batch answer was never recorded
(SCHEMA-TRANSLATION.md §12 "Not verified", §13).

These drive the REAL render seam (catalog resolve stubbed) and the REAL answer
step on provider-shaped batch results.
"""

from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

from matrx_ai.agents import Agent
from matrx_ai.catalog.controls import CompiledControlsMap
from matrx_ai.catalog.models import ResolvedCallProfile
from matrx_ai.config import UnifiedConfig
from matrx_ai.providers.resolved_capabilities import (
    ResolvedModelCapabilities,
    StructuredOutputMode,
)

#: The AUTHOR's schema: ``note`` is optional and does not admit null.
AUTHOR_SCHEMA = {
    "type": "object",
    "properties": {"answer": {"type": "string"}, "note": {"type": "string"}},
    "required": ["answer"],
    "additionalProperties": False,
}


def _profile() -> ResolvedCallProfile:
    caps = ResolvedModelCapabilities(
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
        supports_function_calling=True,
        supports_web_search=False,
        native_capabilities=frozenset(),
        structured_output_mode=StructuredOutputMode.SCHEMA,
        interaction="turn",
        multilingual=True,
    )
    return ResolvedCallProfile(
        model_id="m1",
        model_name="probe-model",
        provider_model_id="probe-model",
        offering_id="off1",
        endpoint_id="ep1",
        api_id="api1",
        provider_name="Probe",
        vendor="openai",
        wire_format="openai_chat",
        client_attr="openai_chat",
        capabilities=caps,
        controls=CompiledControlsMap(),
    )


def _agent() -> Agent:
    config = UnifiedConfig(model="probe-model", messages=[])
    config.append_user_message("hi")
    config.response_format = {
        "type": "json_schema",
        "json_schema": {"name": "answer_with_note", "schema": AUTHOR_SCHEMA, "strict": True},
    }
    agent = Agent(config=config, name="Probe Answerer")
    agent.source_id = "11111111-1111-1111-1111-111111111111"
    return agent


@pytest.mark.asyncio
async def test_render_carries_the_authors_contract_not_the_wire_copy(monkeypatch):
    from matrx_ai.agents.batch_render import render_agent_provider_request

    async def _fake(model_ref, offering_id=None, **kwargs):
        return _profile()

    monkeypatch.setattr("matrx_ai.catalog.resolve.resolve_call_profile", _fake)
    rendered = await render_agent_provider_request(_agent())

    contract = getattr(rendered, "answer_contract", None)
    assert contract is not None, "the rendered batch request carries no answer contract"
    assert contract["schema"] == AUTHOR_SCHEMA, "the contract is not the AUTHOR's schema"
    assert contract["agent_id"] == "11111111-1111-1111-1111-111111111111"
    assert contract["agent_name"] == "Probe Answerer"
    # The wire copy is the portable one — all-required, optional widened — which
    # is exactly why the contract must be carried separately.
    wire = rendered.payload["text"]["format"]["schema"]
    assert sorted(wire["required"]) == ["answer", "note"]


def _item(provider: str, result: dict, **extra) -> SimpleNamespace:
    return SimpleNamespace(
        id="wi-1",
        custom_id="probe-1",
        purpose="probe.purpose",
        provider=provider,
        model="probe-model",
        result=result,
        answer_contract={
            "schema": AUTHOR_SCHEMA,
            "name": "answer_with_note",
            "enforced": True,
            "agent_id": "11111111-1111-1111-1111-111111111111",
            "agent_name": "Probe Answerer",
        },
        **extra,
    )


NULLED = json.dumps({"answer": "yes", "note": None})

RESULTS = {
    "anthropic": {"message": {"content": [{"type": "text", "text": NULLED}], "stop_reason": "end_turn"}},
    "openai": {
        "response": {
            "body": {
                "output": [
                    {"type": "reasoning", "summary": []},
                    {"type": "message", "content": [{"type": "output_text", "text": NULLED}]},
                ]
            }
        }
    },
    "gemini": {
        "response": {
            "candidates": [
                {"content": {"parts": [{"text": "thinking…", "thought": True}, {"text": NULLED}]}}
            ]
        }
    },
}


@pytest.mark.asyncio
@pytest.mark.parametrize("provider", sorted(RESULTS))
async def test_a_batch_answer_reaches_the_handler_in_the_authors_shape(provider, monkeypatch):
    from matrx_ai.agents.batch_render import conform_batch_answer, output_text_from_batch_result

    recorded: list = []

    async def _fake_capture(key, **kwargs):
        recorded.append((key, kwargs))

    monkeypatch.setattr("matrx_ai.ops.issue_capture.capture_issue", _fake_capture)

    item = _item(provider, json.loads(json.dumps(RESULTS[provider])))
    await conform_batch_answer(item)

    delivered = json.loads(output_text_from_batch_result(provider, item.result))
    assert delivered == {"answer": "yes"}, f"{provider}: handler received {delivered}"
    assert recorded == [], f"a conformed answer was reported off-contract: {recorded}"


@pytest.mark.asyncio
async def test_an_off_contract_batch_answer_is_recorded_naming_agent_and_shape(monkeypatch):
    from matrx_ai.agents.batch_render import conform_batch_answer

    recorded: list = []

    async def _fake_capture(key, **kwargs):
        recorded.append((key, kwargs))

    monkeypatch.setattr("matrx_ai.ops.issue_capture.capture_issue", _fake_capture)

    bad = {"message": {"content": [{"type": "text", "text": json.dumps({"note": "x"})}]}}
    item = _item("anthropic", bad)
    problems = await conform_batch_answer(item)

    assert problems, "an answer missing a required key passed the batch check"
    assert [k for k, _ in recorded] == ["structured_output.answer_off_contract"]
    detail = recorded[0][1]["detail"]
    assert detail["schema_name"] == "answer_with_note"
    assert detail["agent_id"] == "11111111-1111-1111-1111-111111111111"
    assert detail["agent_name"] == "Probe Answerer"
    assert detail["lane"] == "batch" and detail["batch_custom_id"] == "probe-1"


@pytest.mark.asyncio
async def test_a_tool_call_batch_turn_is_not_judged_as_the_answer(monkeypatch):
    from matrx_ai.agents.batch_render import conform_batch_answer

    recorded: list = []

    async def _fake_capture(key, **kwargs):
        recorded.append((key, kwargs))

    monkeypatch.setattr("matrx_ai.ops.issue_capture.capture_issue", _fake_capture)
    turn = {
        "message": {
            "stop_reason": "tool_use",
            "content": [
                {"type": "text", "text": "I will look that up."},
                {"type": "tool_use", "id": "t1", "name": "x", "input": {}},
            ],
        }
    }
    assert await conform_batch_answer(_item("anthropic", turn)) == []
    assert recorded == []
