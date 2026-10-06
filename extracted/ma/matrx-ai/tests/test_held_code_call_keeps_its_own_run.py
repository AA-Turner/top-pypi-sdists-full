"""A held code call is its OWN run, and its completion learns which one (AF-R).

Found 2026-10-05 (independent review M4): a held code call
(``hold_code_call`` + a site's funnel call) never reached the mandate run
record — ``HeldCall.finish`` handed the host an ``AgentRunResult`` with no
conversation id — and a call made inside a person's chat ran AS that chat's
conversation, so its prompt and answer would be written into the person's
thread (or a record stamped onto it).

The real ``execute_ai_request`` runs; only the provider loop
(``execute_until_complete``) is replaced. Asserted:

* the call runs as a NEW conversation linked to the one it ran inside, and the
  caller's context is unchanged afterwards;
* a machine context minted non-persisting still stores it; a person's own
  do-not-save request is honoured;
* ``HeldCall.finish`` hands the host the run's conversation + request ids —
  only for a stored run.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.config import UnifiedConfig

PERSON_CONVERSATION = "11111111-1111-1111-1111-111111111111"
USER_ID = "22222222-2222-2222-2222-222222222222"
REQUEST_ID = "33333333-3333-3333-3333-333333333333"
KEY = "rag.page_cleaner"


def _held(complete: Any) -> Any:
    from matrx_ai import mandates

    held = mandates.HeldCall(
        mandate_key=KEY,
        model="test-model",
        system="clean the page",
        temperature=None,
        max_output_tokens=None,
        turns=[],
        config=None,
        metadata={
            "mandate_key": KEY,
            "mandate_holder": {
                "mandate_key": KEY,
                "holder_type": "agent",
                "agent_id": "agent-1",
                "held_call_id": "held-test-1",
            },
        },
        complete=complete,
    )
    mandates._register_held_run("held-test-1", held.run_ids)
    return held


async def _run(monkeypatch: pytest.MonkeyPatch, ctx: Any) -> tuple[dict[str, Any], Any, Any]:
    from matrx_connect.context.app_context import get_app_context, set_app_context

    from matrx_ai.orchestrator import executor

    set_app_context(ctx)
    seen: dict[str, Any] = {}

    async def _loop(request: Any, client: Any, *a: Any, **k: Any) -> Any:
        live = get_app_context()
        seen.update(
            conversation_id=live.conversation_id,
            parent=live.parent_conversation_id,
            store=live.store,
            conversation_type=live.conversation_type,
            request_conversation=request.conversation_id,
        )
        return SimpleNamespace(request=request)

    monkeypatch.setattr(executor, "execute_until_complete", _loop)
    finished: dict[str, Any] = {}

    async def _complete(result: Any, variables: Any, user_input: Any) -> None:
        finished["metadata"] = dict(result.metadata)

    held = _held(_complete)
    await executor.execute_ai_request(
        UnifiedConfig.from_dict({"model": "test-model", "messages": []}),
        max_iterations=1,
        metadata=dict(held.metadata),
    )
    after = get_app_context()
    await held.finish("clean text")
    return seen, finished, after


def _ctx(**fields: Any) -> Any:
    from matrx_connect import ConsoleEmitter
    from matrx_connect.context.app_context import AppContext

    return AppContext(emitter=ConsoleEmitter(), user_id=USER_ID, request_id=REQUEST_ID, **fields)


@pytest.mark.asyncio
async def test_held_call_in_a_persons_chat_is_its_own_recorded_run(monkeypatch):
    seen, finished, after = await _run(
        monkeypatch, _ctx(conversation_id=PERSON_CONVERSATION, store=True)
    )

    assert seen["conversation_id"] != PERSON_CONVERSATION
    assert seen["request_conversation"] == seen["conversation_id"]
    assert seen["parent"] == PERSON_CONVERSATION
    assert after.conversation_id == PERSON_CONVERSATION, "the caller's context is restored"
    assert finished["metadata"] == {
        "conversation_id": seen["conversation_id"],
        "request_id": REQUEST_ID,
    }


@pytest.mark.asyncio
async def test_held_call_in_a_machine_context_is_stored(monkeypatch):
    seen, finished, _ = await _run(monkeypatch, _ctx(store=False, is_internal_agent=True))

    assert seen["store"] is True
    assert finished["metadata"]["conversation_id"] == seen["conversation_id"]


@pytest.mark.asyncio
async def test_a_persons_do_not_save_is_honoured(monkeypatch):
    seen, finished, _ = await _run(
        monkeypatch, _ctx(conversation_id=PERSON_CONVERSATION, store=False)
    )

    assert seen["store"] is False
    assert "conversation_id" not in finished["metadata"]


@pytest.mark.asyncio
async def test_held_call_conversation_is_a_hidden_subagent_not_a_chat_entry(monkeypatch):
    """Found 2026-10-05: the labeler's own run landed in the person's chat history as a
    second 'General Chat' conversation, because the held call's conversation was stamped
    ``standard``. ``subagent`` is the existing internal lane (chat.conversation_lane)."""
    seen, _, after = await _run(
        monkeypatch,
        _ctx(conversation_id=PERSON_CONVERSATION, store=True, source_feature="chat"),
    )

    assert seen["conversation_type"] == "subagent"
    assert after.conversation_type == "standard", "the caller's context is restored"


@pytest.mark.asyncio
async def test_held_call_keeps_a_more_specific_internal_type(monkeypatch):
    seen, _, _ = await _run(
        monkeypatch, _ctx(store=True, is_internal_agent=True, conversation_type="workflow")
    )

    assert seen["conversation_type"] == "workflow"
