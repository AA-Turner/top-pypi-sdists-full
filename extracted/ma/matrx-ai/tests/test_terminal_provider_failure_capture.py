from types import SimpleNamespace

import pytest

from matrx_ai.config.message_config import MessageSanitizationError
from matrx_ai.orchestrator.executor import (
    MESSAGE_SANITIZATION_FAILURE_KIND,
    TERMINAL_PROVIDER_FAILURE_KIND,
    _capture_terminal_provider_failure,
)
from matrx_ai.providers.errors import RetryableError, classify_provider_error


def test_cerebras_archived_model_is_catalog_drift_not_generic_not_found() -> None:
    error = Exception(
        "Error code: 404 - {'message': 'Model zai-glm-4.7 is archived and unavailable', "
        "'type': 'model_archived_error', 'code': 'model_archived'}"
    )

    classified = classify_provider_error("cerebras", error)

    assert classified.error_type == "model_retired"
    assert classified.is_retryable is False
    assert classified.details["catalog_drift"] is True


@pytest.mark.asyncio
async def test_terminal_provider_failure_forces_structured_capture(monkeypatch) -> None:
    captured = []

    async def fake_capture(exc, **fields):
        captured.append((exc, fields))

    monkeypatch.setattr("matrx_connect.streaming.error_capture.capture_error", fake_capture)
    request = SimpleNamespace(
        request_id="request-id",
        conversation_id="conversation-id",
        config=SimpleNamespace(model="retired-model"),
    )
    context = SimpleNamespace(request_id="ctx-request", user_id="user-id", conversation_id="ctx-conv")
    failure = RuntimeError("provider rejected retired model")
    info = RetryableError(
        error_type="model_retired",
        message=str(failure),
        status_code=404,
        is_retryable=False,
        details={"provider": "Cerebras"},
    )

    await _capture_terminal_provider_failure(
        failure,
        exec_ctx=context,
        current_request=request,
        error_info=info,
        provider="cerebras",
        iteration=2,
        retry_attempt=0,
    )

    assert captured[0][0] is failure
    assert captured[0][1]["kind"] == TERMINAL_PROVIDER_FAILURE_KIND
    assert captured[0][1]["error_type"] == "model_retired"
    assert captured[0][1]["payload"] == {
        "provider": "Cerebras",
        "model": "retired-model",
        "status_code": 404,
        "iteration": 2,
        "retry_attempt": 0,
    }


def test_message_sanitization_is_local_and_never_retryable() -> None:
    failure = MessageSanitizationError(
        "MessageList.sanitize refused to collapse a non-empty conversation to zero provider messages"
    )

    classified = classify_provider_error("anthropic", failure)

    assert classified.error_type == "message_sanitization_error"
    assert classified.is_retryable is False
    assert "no AI provider request was attempted" in classified.user_message


@pytest.mark.asyncio
async def test_message_sanitization_forces_dedicated_structured_capture(monkeypatch) -> None:
    captured = []

    async def fake_capture(exc, **fields):
        captured.append((exc, fields))

    monkeypatch.setattr("matrx_connect.streaming.error_capture.capture_error", fake_capture)
    request = SimpleNamespace(
        request_id="request-id",
        conversation_id="conversation-id",
        config=SimpleNamespace(model="model-id"),
    )
    context = SimpleNamespace(request_id="ctx-request", user_id="user-id", conversation_id="ctx-conv")
    failure = MessageSanitizationError("empty provider message list")
    info = classify_provider_error("anthropic", failure)

    await _capture_terminal_provider_failure(
        failure,
        exec_ctx=context,
        current_request=request,
        error_info=info,
        provider="anthropic",
        iteration=1,
        retry_attempt=0,
    )

    assert captured[0][0] is failure
    assert captured[0][1]["kind"] == MESSAGE_SANITIZATION_FAILURE_KIND
    assert captured[0][1]["error_type"] == "message_sanitization_error"
    assert captured[0][1]["payload"]["retry_attempt"] == 0
