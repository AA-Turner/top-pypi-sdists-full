"""Guard: no provider path may leave the request snapshot body empty.

chat.request_snapshot.request_payload must equal the JSON the provider was
sent. The executor reads ``ExecutionState.snapshot_payload`` (stamped by
``capture_request_payload`` at the send seam) and writes ``{}`` when nothing was
stamped. TypeSafe (decision), Fastino (extraction) and Google Deep Research
never stamped, so every one of their snapshot rows had an empty body (69 of the
last 200 production rows were TypeSafe).

Each test drives the REAL transport function with a fake wire under a live
ExecutionState and asserts the stamped payload equals the body the wire saw.
"""

from __future__ import annotations

import json
from typing import Any

import httpx
import pytest

import matrx_ai.providers.fastino.fastino_api as fastino_api
import test_google_research_agent as gra_suite
from matrx_ai.orchestrator.execution_state import (
    ExecutionState,
    clear_execution_state,
    set_execution_state,
)
from matrx_ai.providers.fastino import FastinoExtraction
from matrx_ai.providers.typesafe import call_system_one
from test_fastino_extraction import _mock_transport
from test_typesafe_provider import _request, _result


@pytest.fixture
def state():
    st = ExecutionState()
    token = set_execution_state(st)
    try:
        yield st
    finally:
        clear_execution_state(token)


async def test_typesafe_decision_call_stamps_the_wire_body(state) -> None:
    seen: dict[str, Any] = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        seen["json"] = json.loads(request.content)
        return httpx.Response(200, json=_result())

    http = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    try:
        await call_system_one(_request(), api_key="test-key", http=http)
    finally:
        await http.aclose()

    assert state.snapshot_payload, "TypeSafe call left the snapshot body empty"
    assert state.snapshot_payload == seen["json"]
    assert state.snapshot_provider == "typesafe"


async def test_fastino_extraction_call_stamps_the_wire_body(state, monkeypatch) -> None:
    monkeypatch.setenv("PIONEER_API_KEY", "test-key-123")
    monkeypatch.setattr(fastino_api, "_permanent_refusal", None, raising=False)
    capture: dict[str, Any] = {}
    async with httpx.AsyncClient(transport=_mock_transport(capture)) as client:
        await FastinoExtraction(client=client).extract(
            "OpenAI CEO Sam Altman announced GPT-5.",
            ["company", "person"],
            model_class="fastino/gliner2-large-v1",
        )

    assert state.snapshot_payload, "Fastino call left the snapshot body empty"
    assert state.snapshot_payload == capture["body"]


def test_google_research_agent_stamps_the_create_body(state) -> None:
    fake = gra_suite._FakeInteractions(gra_suite._finished())
    gra_suite._run(gra_suite.gra.GoogleDeepResearchAgent(), fake, gra_suite._Emitter())

    assert state.snapshot_payload, "Deep Research call left the snapshot body empty"
    assert state.snapshot_payload == fake.created
    assert state.snapshot_provider == "google"
