"""Defect 97: a snapshot links to the user_request of the call that produced it, on every door.

Live 2026-10-21..23: 363 completed ``package_code_call`` requests had no ``chat.request_snapshot``
linked by ``user_request_id`` (the snapshots sat in the child conversation, linked to the CALLER's
request) and every ``workflow_step`` request was findable only by conversation.

Root: a held code call (the ``package_code_call`` door) ran under ``with_overrides(conversation_id=...)``
and kept the caller's ``request_id``. The snapshot writer, the cx_request rows and the run record all
key on that id, so a fanned-out batch (a table column fill) wrote N conversations' snapshots under ONE
request, and the run record minted a zero-token ``uuid5`` row beside it, which is the row the door and
mandate key are stamped on, so it never had a snapshot.

Census over the doors that reach the model with a mandate:
  package_code_call (held call, with and without a named conversation) |
  run_mandate / mandate_call / try (``run_agent`` child fork) | workflow_step (``run_step_agent``).
Each must run under a request id of its own, name its caller as ``parent_request_id`` and keep the
caller's tree root, and a conversation must exist for it (a stored run).
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.config import UnifiedConfig

CALLER_CONVERSATION = "11111111-1111-1111-1111-111111111111"
USER_ID = "22222222-2222-2222-2222-222222222222"
CALLER_REQUEST = "33333333-3333-3333-3333-333333333333"
NAMED_CONVERSATION = "44444444-4444-4444-4444-444444444444"
KEY = "rag.page_cleaner"


def _held() -> Any:
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
                "held_call_id": "held-census-1",
            },
        },
        complete=None,
    )
    mandates._register_held_run("held-census-1", held.run_ids)
    return held


def _caller_ctx() -> Any:
    from matrx_connect import ConsoleEmitter
    from matrx_connect.context.app_context import AppContext

    return AppContext(
        emitter=ConsoleEmitter(),
        user_id=USER_ID,
        request_id=CALLER_REQUEST,
        conversation_id=CALLER_CONVERSATION,
        store=True,
    )


async def _what_the_model_call_ran_under(monkeypatch: pytest.MonkeyPatch, **kwargs: Any) -> dict[str, Any]:
    from matrx_connect.context.app_context import get_app_context, set_app_context

    from matrx_ai.orchestrator import executor

    set_app_context(_caller_ctx())
    seen: dict[str, Any] = {}

    async def _loop(request: Any, client: Any, *a: Any, **k: Any) -> Any:
        live = get_app_context()
        seen.update(
            ctx_request=live.request_id,
            request=request.request_id,
            parent=live.parent_request_id,
            root=live.tree_request_id,
            conversation=request.conversation_id,
        )
        return SimpleNamespace(request=request)

    monkeypatch.setattr(executor, "execute_until_complete", _loop)
    held = _held()
    await executor.execute_ai_request(
        UnifiedConfig.from_dict({"model": "test-model", "messages": []}),
        max_iterations=1,
        metadata=dict(held.metadata),
        **kwargs,
    )
    return seen


def _assert_own_turn(seen: dict[str, Any], door: str) -> None:
    assert seen["request"] and seen["request"] != CALLER_REQUEST, (
        f"{door}: ran under the caller's request id {CALLER_REQUEST} - its snapshots would link to the caller"
    )
    assert seen["ctx_request"] == seen["request"], (
        f"{door}: the snapshot writer reads the context's request id ({seen['ctx_request']}) but the "
        f"call's own request is {seen['request']}"
    )
    assert seen["parent"] == CALLER_REQUEST, f"{door}: does not name its caller as parent_request_id"
    assert seen["root"] == CALLER_REQUEST, f"{door}: left the caller's tree (cost cap and stop key on the root)"
    assert seen["conversation"], f"{door}: ran with no conversation"


@pytest.mark.asyncio
async def test_package_code_call_runs_as_its_own_request(monkeypatch: pytest.MonkeyPatch) -> None:
    _assert_own_turn(await _what_the_model_call_ran_under(monkeypatch), "package_code_call")


@pytest.mark.asyncio
async def test_package_code_call_naming_its_conversation_runs_as_its_own_request(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen = await _what_the_model_call_ran_under(monkeypatch, conversation_id=NAMED_CONVERSATION, store=True)
    assert seen["conversation"] == NAMED_CONVERSATION
    _assert_own_turn(seen, "package_code_call(named conversation)")


@pytest.mark.parametrize("door", ["run_mandate", "mandate_call", "try"])
def test_run_agent_doors_fork_their_own_request(door: str) -> None:
    child = _caller_ctx().fork_for_child_agent(NAMED_CONVERSATION)
    assert child.request_id and child.request_id != CALLER_REQUEST, door
    assert child.parent_request_id == CALLER_REQUEST, door
    assert child.tree_request_id == CALLER_REQUEST, door


def test_workflow_step_runs_under_its_own_request(monkeypatch: pytest.MonkeyPatch) -> None:
    import asyncio

    from matrx_connect import ConsoleEmitter
    from matrx_connect.context.app_context import AppContext, get_app_context

    from matrx_ai.graph_nodes import agent_action

    seen: list[str] = []

    async def fake_runner(agent_id: str, request: Any, ctx: Any) -> str:
        seen.append(get_app_context().request_id)
        return "ok"

    class _Emitter(ConsoleEmitter):
        async def send_record_reserved(self, payload: Any) -> None:
            return None

    root = AppContext(emitter=_Emitter(), user_id=USER_ID, request_id=CALLER_REQUEST)
    # Scoped: a bare assignment outlived this test and handed every later
    # build_agent_request a function as its AgentStartRequest.
    monkeypatch.setattr(agent_action, "get_ext", lambda name: fake_runner)
    monkeypatch.setattr(agent_action, "has_ext", lambda name: False)
    step = SimpleNamespace(app=root.fork_for_workflow_step(NAMED_CONVERSATION), node_id="n")
    asyncio.run(agent_action.run_step_agent(step, "agent", object(), mandate_key=KEY))  # type: ignore[arg-type]
    assert seen and seen[0] != CALLER_REQUEST
