"""The Observer / Reflector provider call gets the platform's transient retry.

Context (2026-10-22): provider SDK retries are off (``NO_SDK_RETRIES``); the one
classifier-aware retry lives at ``UnifiedAIClient._dispatch_with_billing_net``
and is opt-in (``transient_retries=N``). The memory adapter's call never opted
in, so one dropped connection lost the whole observation / reflection pass.

Breaks named:
* a dropped connection on the memory call is not retried (one blip = no memory);
* an out-of-credit refusal is retried (it never recovers) or loses its sentence;
* ``send_once`` / ``UnifiedAIClient.execute`` cannot carry the opt-in to the seam.

Real code: ``MemoryLLMAdapter`` -> the real dispatch seam and shared classifier.
Doubles: the vendor wire (raises the SDK's own exception types), ``capture_error``,
sleep, the Holder lookup and the event writers.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any

import httpx
import openai
import pytest

import matrx_ai.mandates as mandates
from matrx_ai.code_call_mandate_keys import MEMORY_OBSERVER_MANDATE
from matrx_ai.memory import llm_adapter
from matrx_ai.providers.unified_client import UnifiedAIClient

_REQ = httpx.Request("POST", "https://api.openai.com/v1/chat/completions")
_PROFILE = SimpleNamespace(
    vendor="openai", model_name="gpt-5.4-nano", endpoint_id="openai-test", base_url=None,
    offering_metadata={},
)
_OK = SimpleNamespace(
    messages=[SimpleNamespace(role="assistant", content=[SimpleNamespace(text="observed")])],
    usage=None,
)
_NO_CREDIT = "You have no credits remaining on this account."


@pytest.fixture
def sleeps(monkeypatch: pytest.MonkeyPatch) -> list[float]:
    waited: list[float] = []

    async def _capture_error(_exc: BaseException, **_kw: Any) -> None:
        return None

    async def _sleep(seconds: float) -> None:
        waited.append(seconds)

    monkeypatch.setattr("matrx_connect.streaming.error_capture.capture_error", _capture_error)
    monkeypatch.setattr("matrx_ai.providers.unified_client._transient_retry_sleep", _sleep)
    return waited


def _wire(monkeypatch: pytest.MonkeyPatch, *outcomes: Any) -> list[int]:
    """Hold + client doubles. The client runs the REAL dispatch seam, with the
    retry budget ``execute`` was handed — exactly what the real client does."""
    sends: list[int] = []
    script = list(outcomes)

    async def _hold(mandate_key, **_kw):
        return mandates.HeldCall(
            mandate_key=mandate_key, model="holder-model", system="HOLDER", temperature=0.0,
            max_output_tokens=16000, turns=[{"role": "user", "content": "HOLDER TURN"}],
            config=SimpleNamespace(), metadata={},
        )

    class _Client:
        async def execute(self, request, *, transient_retries: int = 0):
            async def _send():
                sends.append(1)
                outcome = script.pop(0)
                if isinstance(outcome, BaseException):
                    raise outcome
                return outcome

            return await UnifiedAIClient._dispatch_with_billing_net(
                _send, profile=_PROFILE, transient_retries=transient_retries
            )

    async def _nothing(**_kw):
        return None

    monkeypatch.setattr(mandates, "hold_code_call", _hold)
    monkeypatch.setattr(llm_adapter, "_get_client", lambda: _Client())
    monkeypatch.setattr(llm_adapter, "_write_event", _nothing)
    monkeypatch.setattr(llm_adapter, "_emit_event", _nothing)
    return sends


async def _observe() -> str:
    adapter = llm_adapter.MemoryLLMAdapter(ctx=SimpleNamespace(), conversation_id="c")
    try:
        return await adapter(mandate_key=MEMORY_OBSERVER_MANDATE, messages=[], variables={"m": "x"})
    finally:
        for _ in range(10):
            await asyncio.sleep(0)


async def test_a_dropped_connection_on_the_memory_call_is_retried_and_succeeds(
    monkeypatch, sleeps
) -> None:
    sends = _wire(monkeypatch, openai.APIConnectionError(request=_REQ), _OK)
    assert await _observe() == "observed"
    assert len(sends) == 2
    assert len(sleeps) == 1


async def test_an_out_of_credit_refusal_on_the_memory_call_surfaces_once_with_its_sentence(
    monkeypatch, sleeps
) -> None:
    exc = openai.APIError(_NO_CREDIT, _REQ, body=None)
    sends = _wire(monkeypatch, exc, _OK)
    with pytest.raises(RuntimeError) as raised:
        await _observe()
    assert _NO_CREDIT in str(raised.value)
    assert len(sends) == 1
    assert sleeps == []


async def test_execute_and_send_once_carry_the_retry_budget_to_the_dispatch(monkeypatch) -> None:
    """The opt-in is a real parameter all the way down: ``send_once`` hands it to
    ``execute``, and ``execute`` hands it to ``_execute_dispatch``."""
    seen: list[int] = []

    async def _dispatch(self, request, *, transient_retries: int = 0):
        seen.append(transient_retries)
        return {"ok": True}

    monkeypatch.setattr(UnifiedAIClient, "_execute_dispatch", _dispatch)
    client = UnifiedAIClient()
    request = SimpleNamespace(config=SimpleNamespace(metadata={}))
    assert await client.execute(request, transient_retries=3) == {"ok": True}
    assert await client.execute(request) == {"ok": True}
    assert seen == [3, 0]

    from matrx_ai.orchestrator import send_once as so

    got: list[Any] = []

    class _Fake:
        async def execute(self, request, **kw):
            got.append(kw)
            return "r"

    async def _prep(*_a, **_kw):
        return SimpleNamespace(wire_config=None)

    monkeypatch.setattr("matrx_ai.config.send_boundary.prepare_for_send", _prep)
    monkeypatch.setattr("matrx_ai.mandate_taps.observe_first_send", lambda *a, **k: None)
    req = SimpleNamespace(config=None, conversation_id="c", request_id="r")
    await so.send_once(_Fake(), req, state=SimpleNamespace(), iteration=1, transient_retries=2)
    await so.send_once(_Fake(), req, state=SimpleNamespace(), iteration=1)
    assert got == [{"transient_retries": 2}, {}]
