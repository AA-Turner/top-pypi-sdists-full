"""A child agent's failure reaches the tool executor as its REAL exception.

Live 2026-10-01 (request 5c4a458e…): a child run failed on an OpenAI
out-of-credit refusal and ``agent_call`` reported only "Agent 'X' failed:
<sentence>" — the tool executor's TOOL CALL FAILED block said "the tool
swallowed its exception and stringified it", and the operator never saw
``openai.APIError`` or its stack.

SUTs: ``Agent.execute`` → ``run_agent`` (the chain that turns the executor's
contained ``CompletedRequest`` into an ``AgentRunResult``) and ``agent_call``
(which turns that result into a ``ToolError``). Doubles replace only what they
CALL: ``execute_ai_request`` (returns the failed CompletedRequest the executor
builds — its own carriage is guarded in test_provider_out_of_credit_terminal),
the agent loader, and the access check.

Breaks named: any hop drops the exception (Agent._clean_up_response,
run_agent's failed-result build, agent_call's _fail) → no traceback, no type.
"""

from __future__ import annotations

import contextlib
from types import SimpleNamespace
from typing import Any

import httpx
import openai
import pytest
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

_NO_CREDITS = (
    "You have no credits remaining. Add credits to continue using the API at "
    "https://platform.openai.com/settings/organization/billing/."
)
_SENTENCE = "OpenAI refused this request: the platform's OpenAI account is out of credit."
_USER_ID = "e4687a9c-acf7-469f-aa12-860eb4d948d0"
_AGENT_ID = "3b1f6c1e-7d0a-4f0e-9a51-2f4c8f0d9e21"


class _QuietEmitter:
    def __getattr__(self, name: str) -> Any:
        async def _noop(*a: Any, **k: Any) -> None:
            return None

        return _noop


def _raised_no_credits() -> openai.APIError:
    # Raised and caught so it carries a real __traceback__, as in production.
    try:
        raise openai.APIError(
            _NO_CREDITS, httpx.Request("POST", "https://api.openai.com/v1/responses"), body=None
        )
    except openai.APIError as exc:
        return exc


def _failed_completed_request(exc: BaseException) -> Any:
    from matrx_ai.config import MessageList, UnifiedConfig
    from matrx_ai.config.unified_config import UnifiedResponse
    from matrx_ai.orchestrator.requests import AIMatrixRequest, CompletedRequest

    messages = MessageList()
    messages.append_or_extend_user_text("List the open action items from the Harbor Dental call.")
    return CompletedRequest(
        request=AIMatrixRequest(
            conversation_id="825b59b0-541c-4758-b72d-165459164c54",
            config=UnifiedConfig(model="gpt-5.4-nano", messages=messages),
        ),
        iterations=1,
        final_response=UnifiedResponse(messages=[]),
        metadata={"status": "failed", "error": _SENTENCE, "error_type": "billing_error"},
        terminal_exception=exc,
    )


@pytest.mark.asyncio
async def test_run_agent_returns_the_childs_terminal_exception(monkeypatch) -> None:
    import matrx_ai.agents.definition as definition
    from matrx_ai.agents.definition import Agent
    from matrx_ai.agents.executor import run_agent
    from matrx_ai.config import MessageList, UnifiedConfig

    exc = _raised_no_credits()

    async def fake_execute_ai_request(config: Any, **kwargs: Any) -> Any:
        return _failed_completed_request(exc)

    monkeypatch.setattr(definition, "execute_ai_request", fake_execute_ai_request)
    agent = Agent(UnifiedConfig(model="gpt-5.4-nano", messages=MessageList()), name="Action items")
    token = set_app_context(AppContext(emitter=_QuietEmitter(), user_id=_USER_ID, store=False))  # type: ignore[arg-type]
    try:
        result = await run_agent(agent, label="action-items", source_feature="agent_call")
    finally:
        clear_app_context(token)

    assert result.success is False
    assert result.error == _SENTENCE
    assert result.exception is exc
    # Never serialized: the exception is a carrier, not a field of the result.
    assert "exception" not in result.model_dump()


@pytest.mark.asyncio
async def test_agent_call_hands_the_child_exception_to_the_tool_error(monkeypatch) -> None:
    import matrx_ai._ext as ext
    from matrx_ai.agents import executor as executor_mod
    from matrx_ai.agents.definition import Agent
    from matrx_ai.agents.executor import AgentRunResult
    from matrx_ai.db.agx_manager import AgxDefinition
    from matrx_ai.tools.implementations.agent_call import agent_call
    from matrx_ai.tools.models import ToolContext

    @contextlib.asynccontextmanager
    async def acting_as_caller(_ctx: Any = None):
        yield

    async def _value(v: Any) -> Any:
        return v

    monkeypatch.setitem(ext._registry, "acting_as_caller", acting_as_caller)
    monkeypatch.setattr(
        AgxDefinition,
        "load_by_id_or_none",
        classmethod(
            lambda _cls, _id: _value(
                SimpleNamespace(id=_AGENT_ID, created_by=_USER_ID, is_active=True, is_archived=False)
            )
        ),
    )

    class _ChildAgent:
        name = "Action items"
        output_schema = None

    monkeypatch.setattr(
        Agent, "from_agent", classmethod(lambda _cls, *a, **k: _value(_ChildAgent()))
    )
    exc = _raised_no_credits()

    async def fake_run_agent(_agent: Any, **kwargs: Any) -> AgentRunResult:
        return AgentRunResult(
            success=False,
            error=_SENTENCE,
            error_kind="execution",
            metadata={"status": "failed", "error_type": "billing_error"},
            exception=exc,
        )

    monkeypatch.setattr(executor_mod, "run_agent", fake_run_agent)
    token = set_app_context(AppContext(emitter=None, user_id=_USER_ID))
    try:
        result = await agent_call({"agent_id": _AGENT_ID}, ToolContext(call_id="call-1"))
    finally:
        clear_app_context(token)

    assert result.success is False
    error = result.error
    assert error is not None
    assert error.message == f"Agent 'Action items' failed (billing_error): {_SENTENCE}"
    assert error.traceback is not None
    assert "openai.APIError: You have no credits remaining" in error.traceback
    assert "_raised_no_credits" in error.traceback  # the child's real frame
    # …for the operator only: the calling model sees the child's plain
    # sentence, never the provider's billing URL or our stack.
    model_view = error.to_agent_message()
    assert "http" not in model_view
    assert "Traceback" not in model_view
    assert _SENTENCE in model_view
