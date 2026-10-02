"""An out-of-credit provider refusal ends the turn at once, names itself to the
person and the operator, and keeps its exception for in-process callers.

SUT: ``_execute_until_complete_inner`` — the provider-exception branch:
classification → billing alarm (``_capture_provider_out_of_credit``) → reroute
decision → retry decision → terminal capture → stream error → finalize, then
the returned result carrying ``terminal_exception``. Doubles replace only what
the loop CALLS: the provider client (raises the exact SDK error production
saw), the catalog reads (vendor, overload policy, offering ladder — "no
fallback configured"), the DB gates, the durable finalize sink, the queue
seam, and ``capture_error`` (the system_error writer).

Breaks these tests name (live 2026-10-01, request 5c4a458e…, GPT 5.4 Nano):
* the refusal is retried — the client is called more than once;
* the operator row is filed under the generic ``provider_request_failed`` kind
  (or not at all) instead of its own collapsible class;
* the person reads "An unexpected OpenAI error occurred" or a billing URL;
* the returned result drops the exception, so ``agent_call`` can only
  stringify the failure ("the tool swallowed its exception").
"""

from __future__ import annotations

from typing import Any

import httpx
import openai
import pytest
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

import matrx_ai.orchestrator.executor as executor_mod
from matrx_ai.config import MessageList, UnifiedConfig
from matrx_ai.orchestrator.execution_state import ExecutionState
from matrx_ai.orchestrator.overload_reroute import OverloadPolicy
from matrx_ai.orchestrator.requests import AIMatrixRequest

# Literal the error surfaces collapse by — never imported from the SUT.
_OUT_OF_CREDIT_KIND = "provider_account_out_of_credit"
_GENERIC_KIND = "provider_request_failed"

_CONVERSATION_ID = "825b59b0-541c-4758-b72d-165459164c54"
_REQUEST_ID = "5c4a458e-2ba6-48cc-b54b-4e8eaf54733b"
_USER_ID = "e4687a9c-acf7-469f-aa12-860eb4d948d0"
_MODEL_ID = "98a2638a-27ef-434c-80a9-96368b22e0f8"
_NO_CREDITS = (
    "You have no credits remaining. Add credits to continue using the API at "
    "https://platform.openai.com/settings/organization/billing/."
)
_REQ = httpx.Request("POST", "https://api.openai.com/v1/responses")


class _RecordingEmitter:
    def __init__(self) -> None:
        self.errors: list[dict[str, Any]] = []
        self.infos: list[Any] = []

    async def send_error(self, **kwargs: Any) -> None:
        self.errors.append(kwargs)

    async def send_info(self, payload: Any, *a: Any, **k: Any) -> None:
        self.infos.append(payload)

    def reset_turn_text(self) -> None:
        return None

    def get_turn_text(self) -> str:
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


class _RaisingClient:
    def __init__(self, exc: Exception) -> None:
        self.exc = exc
        self.calls = 0

    async def execute(self, *a: Any, **k: Any) -> Any:
        self.calls += 1
        raise self.exc


class _Finalized:
    """Stands in for CompletedRequest — the loop sets attributes on it."""

    terminal_exception: BaseException | None = None


async def _run(monkeypatch: pytest.MonkeyPatch, exc: Exception) -> dict[str, Any]:
    captured: list[dict[str, Any]] = []
    finalized: list[dict[str, Any]] = []
    emitter = _RecordingEmitter()

    async def capture_error(exc: BaseException, **kwargs: Any) -> None:
        captured.append({"exc": exc, **kwargs})

    async def finalize(**kwargs: Any) -> _Finalized:
        finalized.append(kwargs)
        return _Finalized()

    async def _noop_async(*a: Any, **k: Any) -> None:
        return None

    async def _vendor(*a: Any, **k: Any) -> str:
        return "openai"

    async def _policy(model_ref: str, state: Any) -> OverloadPolicy:
        return OverloadPolicy(retry_max_attempts=2, fallback_ref=None)

    async def _no_ladder(*a: Any, **k: Any) -> None:
        return None

    async def _empty_inbox(config: Any, app_ctx: Any) -> Any:
        return app_ctx

    import matrx_ai.persistence.queue_helpers as queue_helpers

    monkeypatch.setattr(queue_helpers, "queue_message_create", lambda **k: None)
    monkeypatch.setattr(queue_helpers, "queue_message_update", lambda *a, **k: None)
    monkeypatch.setattr(queue_helpers, "get_coordinator", lambda: None)
    monkeypatch.setattr("matrx_connect.streaming.error_capture.capture_error", capture_error)
    monkeypatch.setattr(executor_mod, "_finalize_and_persist", finalize)
    monkeypatch.setattr(executor_mod, "_persist_turn_and_commit", _noop_async)
    monkeypatch.setattr(executor_mod, "ensure_conversation_exists", _noop_async)
    monkeypatch.setattr(executor_mod, "ensure_user_request_exists", _noop_async)
    monkeypatch.setattr(executor_mod, "get_tracker", lambda: _StubTracker())
    monkeypatch.setattr(executor_mod, "capture_issue", _noop_async)
    monkeypatch.setattr(executor_mod, "_catalog_vendor_for", _vendor)
    monkeypatch.setattr("matrx_ai.orchestrator.overload_reroute.load_overload_policy", _policy)
    monkeypatch.setattr("matrx_ai.orchestrator.overload_reroute.load_offering_ladder", _no_ladder)
    monkeypatch.setattr("matrx_ai.tools.dynamic_drain.drain_pending", _empty_inbox)

    ctx = AppContext(
        emitter=emitter,  # type: ignore[arg-type]
        user_id=_USER_ID,
        request_id=_REQUEST_ID,
        conversation_id=_CONVERSATION_ID,
        store=True,
        debug=False,
        snapshot=False,
    )
    monkeypatch.setattr(executor_mod, "get_app_context", lambda: ctx)
    messages = MessageList()
    messages.append_or_extend_user_text("Summarize the three open action items from this call.")
    request = AIMatrixRequest(
        conversation_id=_CONVERSATION_ID,
        request_id=_REQUEST_ID,
        config=UnifiedConfig(model=_MODEL_ID, messages=messages),
    )
    client = _RaisingClient(exc)
    token = set_app_context(ctx)
    try:
        result = await executor_mod._execute_until_complete_inner(
            exec_ctx=ctx,
            state=ExecutionState(),
            initial_request=request,
            client=client,
            max_iterations=1,
            max_retries_per_iteration=3,
        )
    finally:
        clear_app_context(token)
    return {
        "result": result,
        "client": client,
        "captured": captured,
        "finalized": finalized,
        "errors": emitter.errors,
    }


@pytest.mark.asyncio
async def test_out_of_credit_refusal_is_called_once_and_never_retried(monkeypatch) -> None:
    run = await _run(monkeypatch, openai.APIError(_NO_CREDITS, _REQ, body=None))
    assert run["client"].calls == 1


@pytest.mark.asyncio
async def test_out_of_credit_files_its_own_operator_class(monkeypatch) -> None:
    exc = openai.APIError(_NO_CREDITS, _REQ, body=None)
    run = await _run(monkeypatch, exc)

    kinds = [row["kind"] for row in run["captured"]]
    assert kinds == [_OUT_OF_CREDIT_KIND], kinds
    row = run["captured"][0]
    assert row["exc"] is exc
    assert row["error_type"] == "openai.billing_error"
    assert row["request_id"] == _REQUEST_ID
    assert row["conversation_id"] == _CONVERSATION_ID
    assert row["payload"]["provider_message"] == _NO_CREDITS


@pytest.mark.asyncio
async def test_the_person_reads_one_plain_sentence(monkeypatch) -> None:
    run = await _run(monkeypatch, openai.APIError(_NO_CREDITS, _REQ, body=None))

    sentence = "OpenAI refused this request: the platform's OpenAI account is out of credit."
    assert [e["user_message"] for e in run["errors"]] == [sentence]
    meta = run["finalized"][0]["metadata"]
    assert meta["status"] == "failed"
    assert meta["error"] == sentence
    assert meta["error_type"] == "billing_error"


@pytest.mark.asyncio
async def test_the_failed_result_carries_the_child_exception(monkeypatch) -> None:
    exc = openai.APIError(_NO_CREDITS, _REQ, body=None)
    run = await _run(monkeypatch, exc)
    assert run["result"].terminal_exception is exc


@pytest.mark.asyncio
async def test_a_generic_terminal_failure_keeps_the_generic_class(monkeypatch) -> None:
    """Control: a non-billing terminal refusal is NOT filed as out of credit."""
    exc = openai.BadRequestError(
        "Error code: 400 - Invalid 'input[2].content': empty array.",
        response=httpx.Response(400, request=_REQ),
        body=None,
    )
    run = await _run(monkeypatch, exc)
    assert [row["kind"] for row in run["captured"]] == [_GENERIC_KIND]
    assert run["client"].calls == 1
    assert run["result"].terminal_exception is exc
