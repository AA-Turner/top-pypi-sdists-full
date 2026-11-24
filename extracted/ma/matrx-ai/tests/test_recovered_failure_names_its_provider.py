"""A provider failure the retry RECOVERED from is filed under the provider that failed, never ``unknown``.

SUT: the recovered-failure capture in ``_execute_until_complete_inner``. A classifier that does not put
``details.provider`` on its ``RetryableError`` (most do not) used to be filed as ``unknown.<type>`` with a
null provider, while the TERMINAL path for the very same error named the catalog vendor. Live 2026-11-12:
Google 504 DEADLINE_EXCEEDED, Groq tool-call validation and a connection error sat in the ops queue as
``unknown.server_error`` / ``unknown.structured_output_invalid`` / ``unknown.connection_error``.

Doubles replace only what the loop CALLS: the provider client (fails once, then answers), the catalog
vendor lookup (the routing identity a real config resolves to), the persistence seams, and
``capture_issue`` (recorded).
"""

from __future__ import annotations

from typing import Any

import pytest
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

import matrx_ai.orchestrator.executor as executor_mod
from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.config.unified_config import UnifiedResponse
from matrx_ai.config.usage_config import TokenUsage
from matrx_ai.orchestrator.execution_state import ExecutionState
from matrx_ai.orchestrator.requests import AIMatrixRequest
from matrx_ai.providers.errors import RetryableError

_CONVERSATION_ID = "5f0f2f8e-3a52-4b0e-9a57-2f7b3c8d1e64"
_REQUEST_ID = "0b7e9a3c-61d4-4f2a-8c1e-9d5a7b3f2e10"
_USER_ID = "a3c5e7f9-1b2d-4e6f-8a0c-2e4f6a8c0b1d"


class _Emitter:
    def get_turn_text(self) -> str:
        return ""

    def reset_turn_text(self) -> None:
        return None

    def __getattr__(self, name: str) -> Any:
        async def _noop(*a: Any, **k: Any) -> None:
            return None

        return _noop


class _Tracker:
    async def reserve(self, *a: Any, **k: Any) -> None:
        return None

    async def mark_active(self, *a: Any, **k: Any) -> None:
        return None

    def register_existing(self, *a: Any, **k: Any) -> None:
        return None


class _FailsOnceClient:
    """First call raises a classified, retryable 504 WITHOUT details.provider; the retry answers."""

    def __init__(self) -> None:
        self.calls = 0

    async def execute(self, *a: Any, **k: Any) -> UnifiedResponse:
        self.calls += 1
        if self.calls == 1:
            exc = RuntimeError("504 DEADLINE_EXCEEDED")
            exc.error_info = RetryableError(  # type: ignore[attr-defined]
                error_type="server_error",
                message="Google internal server error (504): DEADLINE_EXCEEDED",
                status_code=504,
                is_retryable=True,
                retry_after=0,
            )
            raise exc
        return UnifiedResponse(
            messages=[UnifiedMessage(role="assistant", content=[TextContent(text="Here is the answer.")])],
            usage=TokenUsage(
                input_tokens=10, output_tokens=5, matrx_model_name="gemini-test",
                provider_model_name="gemini-test", api="google",
            ),
            finish_reason="stop",
        )


@pytest.mark.asyncio
async def test_a_recovered_failure_is_filed_under_the_catalog_vendor(monkeypatch: pytest.MonkeyPatch) -> None:
    issues: list[dict[str, Any]] = []

    async def _capture_issue(key: str, **kwargs: Any) -> None:
        issues.append({"key": key, **kwargs})

    async def _noop_async(*a: Any, **k: Any) -> None:
        return None

    async def _finalize(**kwargs: Any) -> str:
        return "completed-request"

    async def _vendor(config: Any) -> str:
        return "google"

    async def _no_wait(*a: Any, **k: Any) -> None:
        return None

    import matrx_ai.persistence.queue_helpers as queue_helpers

    monkeypatch.setattr(queue_helpers, "queue_message_create", lambda **k: None)
    monkeypatch.setattr(queue_helpers, "queue_message_update", lambda *a, **k: None)
    monkeypatch.setattr(queue_helpers, "get_coordinator", lambda: None)
    monkeypatch.setattr("matrx_connect.streaming.error_capture.capture_error", _noop_async)
    monkeypatch.setattr(executor_mod, "capture_issue", _capture_issue)
    monkeypatch.setattr(executor_mod, "_catalog_vendor_for", _vendor)
    monkeypatch.setattr(executor_mod, "_finalize_and_persist", _finalize)
    monkeypatch.setattr(executor_mod, "_persist_turn_and_commit", _noop_async)
    monkeypatch.setattr(executor_mod, "ensure_conversation_exists", _noop_async)
    monkeypatch.setattr(executor_mod, "ensure_user_request_exists", _noop_async)
    monkeypatch.setattr(executor_mod, "get_tracker", lambda: _Tracker())
    monkeypatch.setattr(executor_mod.asyncio, "sleep", _no_wait)

    async def _no_inbox(config: Any, app_ctx: Any, **k: Any) -> Any:
        return app_ctx

    monkeypatch.setattr("matrx_ai.tools.dynamic_drain.drain_pending", _no_inbox)
    monkeypatch.setattr("matrx_ai.tools.dynamic_drain.drain_pending_injections", _noop_async)

    ctx = AppContext(
        emitter=_Emitter(),  # type: ignore[arg-type]
        user_id=_USER_ID,
        request_id=_REQUEST_ID,
        conversation_id=_CONVERSATION_ID,
        store=True,
        debug=False,
        snapshot=False,
    )
    monkeypatch.setattr(executor_mod, "get_app_context", lambda: ctx)
    messages = MessageList()
    messages.append_or_extend_user_text("Summarize the quarter.")
    request = AIMatrixRequest(
        conversation_id=_CONVERSATION_ID,
        request_id=_REQUEST_ID,
        config=UnifiedConfig(model="gemini-test", messages=messages),
    )
    client = _FailsOnceClient()
    token = set_app_context(ctx)
    try:
        await executor_mod._execute_until_complete_inner(
            exec_ctx=ctx,
            state=ExecutionState(),
            initial_request=request,
            client=client,  # type: ignore[arg-type]
            max_iterations=1,
            max_retries_per_iteration=2,
        )
    finally:
        clear_app_context(token)

    assert client.calls == 2, "the retry must have answered (the recovered path is the SUT)"
    recovered = [i for i in issues if i.get("was_recovered") is True and i.get("error_type") == "server_error"]
    assert len(recovered) == 1, issues
    assert recovered[0]["key"] == "google.server_error"
    assert recovered[0]["provider"] == "google"
