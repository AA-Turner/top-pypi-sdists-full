"""A provider call stopped mid-generation still bills: its usage joins the request.

The person (or a tree budget / deadline) stops a run WHILE the model is generating.
``_execute_stoppable`` cancels the call and raises ``ProviderCallStopped`` carrying the
usage the adapter stamped on the cancelled call. The loop's stop handler must record it
on the request it finalizes — otherwise the stopped run's cost record says $0.

SUT: ``_execute_until_complete_inner`` (send_once → _execute_stoppable → the stop
handler → finalize). Doubles replace only what the loop CALLS: the provider client
(generates until cancelled, stamping billed usage as a real adapter does), the DB gates,
the mid-loop message queue seam, the turn-boundary inbox, and the durable persistence
sink (``_finalize_and_persist`` — we read the request it is handed). Breaks named:
removing ``_record_billed_usage_on_failure(current_request, _stopped, ...)`` from the
stop handler, or ``_execute_stoppable`` dropping the cancelled call's usage.
"""

from __future__ import annotations

import asyncio
from typing import Any

import pytest
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context
from matrx_connect.request_controls import RequestControlRegistry

import matrx_ai.orchestrator.executor as executor_mod
from matrx_ai.config import MessageList, UnifiedConfig
from matrx_ai.config.usage_config import TokenUsage
from matrx_ai.orchestrator.execution_state import ExecutionState
from matrx_ai.orchestrator.requests import AIMatrixRequest
from matrx_ai.providers.errors import attach_billed_usage

_CONVERSATION_ID = "4d2c1f0e-7a3b-4c5d-9e8f-0a1b2c3d4e5f"
_REQUEST_ID = "8e7d6c5b-4a39-4281-9f0e-1d2c3b4a5968"
_USER_ID = "e4687a9c-acf7-469f-aa12-860eb4d948d0"


class _Emitter:
    def reset_turn_text(self) -> None:
        return None

    def get_turn_text(self) -> str:
        return ""

    def get_seen_turn_text(self) -> str:
        return ""

    def __getattr__(self, name: str) -> Any:
        async def _noop(*a: Any, **k: Any) -> None:
            return None

        return _noop


class _StubTracker:
    async def reserve(self, *a: Any, **k: Any) -> None:
        return None

    async def mark_active(self, *a: Any, **k: Any) -> None:
        return None

    def register_existing(self, *a: Any, **k: Any) -> None:
        return None


class _GeneratingClient:
    """Streams until cancelled; on cancel stamps the tokens already billed, as the
    provider adapters do (``stream_with_billed_usage``)."""

    def __init__(self, billed: TokenUsage) -> None:
        self.billed = billed

    async def execute(self, *a: Any, **k: Any) -> Any:
        try:
            await asyncio.sleep(30)
        except asyncio.CancelledError as exc:
            attach_billed_usage(exc, self.billed)
            raise


@pytest.mark.asyncio
async def test_a_stopped_call_records_what_it_billed(monkeypatch: pytest.MonkeyPatch) -> None:
    finalized: list[dict[str, Any]] = []

    async def finalize(**kwargs: Any) -> str:
        finalized.append(kwargs)
        return "completed-request"

    async def _noop_async(*a: Any, **k: Any) -> None:
        return None

    async def _empty_inbox(config: Any, app_ctx: Any) -> Any:
        return app_ctx

    import matrx_ai.persistence.queue_helpers as queue_helpers

    monkeypatch.setattr(queue_helpers, "queue_message_create", lambda **k: None)
    monkeypatch.setattr(queue_helpers, "queue_message_update", lambda *a, **k: None)
    monkeypatch.setattr(queue_helpers, "get_coordinator", lambda: None)
    monkeypatch.setattr(executor_mod, "_finalize_and_persist", finalize)
    monkeypatch.setattr(executor_mod, "_persist_turn_and_commit", _noop_async)
    monkeypatch.setattr(executor_mod, "ensure_conversation_exists", _noop_async)
    monkeypatch.setattr(executor_mod, "ensure_user_request_exists", _noop_async)
    monkeypatch.setattr(executor_mod, "get_tracker", lambda: _StubTracker())
    monkeypatch.setattr(executor_mod, "_spine_meter_call", lambda _usage: None)
    monkeypatch.setattr("matrx_ai.tools.dynamic_drain.drain_pending", _empty_inbox)

    ctx = AppContext(emitter=_Emitter(), user_id=_USER_ID, request_id=_REQUEST_ID,  # type: ignore[arg-type]
                     conversation_id=_CONVERSATION_ID, store=True, debug=False, snapshot=False)
    monkeypatch.setattr(executor_mod, "get_app_context", lambda: ctx)

    messages = MessageList()
    messages.append_or_extend_user_text("Write the full migration runbook.")
    request = AIMatrixRequest(conversation_id=_CONVERSATION_ID, request_id=_REQUEST_ID,
                              config=UnifiedConfig(model="gemini-test", messages=messages))
    billed = TokenUsage(input_tokens=1200, output_tokens=321, matrx_model_name="gemini-test",
                        api="google")

    async def press_stop() -> None:
        await asyncio.sleep(0.5)
        await RequestControlRegistry.get_instance().cancel(_REQUEST_ID)

    token = set_app_context(ctx)
    stopper = asyncio.create_task(press_stop())
    try:
        await executor_mod._execute_until_complete_inner(
            exec_ctx=ctx, state=ExecutionState(), initial_request=request,
            client=_GeneratingClient(billed), max_iterations=1, max_retries_per_iteration=0,
        )
    finally:
        await stopper
        clear_app_context(token)

    assert finalized, "the stopped run was never finalized"
    assert finalized[-1]["metadata"]["status"] == "cancelled"
    history = finalized[-1]["current_request"].usage_history
    assert any(u.input_tokens == 1200 and u.output_tokens == 321 for u in history), (
        "the stopped call's billed tokens never reached the request — its cost record says $0"
    )
