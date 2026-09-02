from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.orchestrator.executor import _capture_missing_provider_usage


@pytest.mark.asyncio
async def test_missing_provider_usage_creates_structured_error(monkeypatch) -> None:
    captured: list[tuple[BaseException, dict[str, object]]] = []

    async def fake_capture(exc: BaseException, **fields: object) -> None:
        captured.append((exc, fields))

    monkeypatch.setattr("matrx_connect.streaming.error_capture.capture_error", fake_capture)
    request = SimpleNamespace(
        request_id="request-1",
        conversation_id="conversation-1",
        config=SimpleNamespace(model="model-1"),
    )
    ctx = SimpleNamespace(user_id="user-1")

    await _capture_missing_provider_usage(
        exec_ctx=ctx, current_request=request, provider="provider-1", iteration=2
    )

    assert len(captured) == 1
    assert captured[0][1]["kind"] == "provider_usage_missing"
    assert captured[0][1]["route"] == "orchestrator/provider_response"
    assert captured[0][1]["payload"] == {
        "provider": "provider-1",
        "model": "model-1",
        "iteration": 2,
    }
