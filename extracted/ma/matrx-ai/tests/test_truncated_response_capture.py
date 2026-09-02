from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.orchestrator.executor import (
    TRUNCATED_RESPONSE_KIND,
    _capture_truncated_response,
)
from matrx_ai.orchestrator.requests import AIMatrixRequest


@pytest.mark.asyncio
async def test_truncation_creates_bounded_structured_error(monkeypatch: pytest.MonkeyPatch) -> None:
    capture = AsyncMock()
    monkeypatch.setattr("matrx_connect.streaming.error_capture.capture_error", capture)
    request = AIMatrixRequest(
        request_id="79e68e55-e1d8-4de5-b15f-585587d57b02",
        conversation_id="33c2198e-e068-463d-831e-995f78a794ab",
        config=UnifiedConfig(messages=[], model="gemini-test", max_output_tokens=321),
    )

    await _capture_truncated_response(
        exec_ctx=SimpleNamespace(user_id="e4687a9c-acf7-469f-aa12-860eb4d948d0"),
        current_request=request,
        iteration=4,
    )

    capture.assert_awaited_once()
    args, kwargs = capture.await_args
    assert isinstance(args[0], RuntimeError)
    assert kwargs["kind"] == TRUNCATED_RESPONSE_KIND
    assert kwargs["error_type"] == "truncated_response"
    assert kwargs["route"] == "orchestrator/provider_response"
    assert kwargs["payload"] == {
        "model": "gemini-test",
        "max_output_tokens": 321,
        "iteration": 4,
    }
    assert "raw_response" not in kwargs["payload"]
