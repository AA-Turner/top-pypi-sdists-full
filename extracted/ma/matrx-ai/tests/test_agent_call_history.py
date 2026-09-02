"""Conversation-aware agent_call — history_mode (snapshot/fork) + remember.

Covers the collaboration contract: arg validation (no implied durable writes,
no ambiguous history), owner-only conversation gating with 404 semantics,
snapshot seeding order, fork-mode execution inside the fork, the injected
forker seam, and the turn-end inbox write-back with provenance.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

USER_ID = "11111111-1111-4111-8111-111111111111"
AGENT_ID = "22222222-2222-4222-8222-222222222222"
CALLER_CONV = "33333333-3333-4333-8333-333333333333"
SOURCE_CONV = "44444444-4444-4444-8444-444444444444"
FORK_CONV = "55555555-5555-4555-8555-555555555555"


async def _async_value(value):
    return value


class _FakeAgent:
    name = "child"
    output_schema = None

    def __init__(self) -> None:
        self.config = SimpleNamespace(messages=[SimpleNamespace(role="user", authored=True)])


def _history(*positions: int) -> list[SimpleNamespace]:
    return [SimpleNamespace(role="user", position=p, authored=False) for p in positions]


@pytest.fixture
def harness(monkeypatch: pytest.MonkeyPatch):
    """Wire every seam agent_call touches; return the mutable capture bag."""
    import matrx_ai.db as db_pkg
    from matrx_ai.agents import executor as executor_mod
    from matrx_ai.agents import resolver as resolver_mod
    from matrx_ai.agents.definition import Agent
    from matrx_ai.agents.executor import AgentRunResult
    from matrx_ai.db.agx_manager import AgxDefinition

    bag: dict[str, Any] = {
        "agent": _FakeAgent(),
        "owned_rows": [SimpleNamespace(id=SOURCE_CONV)],
        "history": _history(0, 1, 2),
        "run_kwargs": None,
        "ownership_queries": [],
        "history_loads": [],
        "enqueues": [],
        "run_result": AgentRunResult(
            success=True,
            output="child answer",
            metadata={"conversation_id": "child-conv-id"},
        ),
        "enqueue_error": None,
    }

    monkeypatch.setattr(
        AgxDefinition,
        "load_by_id_or_none",
        classmethod(
            lambda _cls, _agent_id: _async_value(
                SimpleNamespace(
                    id=AGENT_ID, created_by=USER_ID, is_active=True, is_archived=False
                )
            )
        ),
    )
    monkeypatch.setattr(
        Agent, "from_agent", classmethod(lambda _cls, *_a, **_k: _async_value(bag["agent"]))
    )

    async def fake_run_agent(_agent, **kwargs):
        bag["run_kwargs"] = kwargs
        return bag["run_result"]

    monkeypatch.setattr(executor_mod, "run_agent", fake_run_agent)

    async def fake_filter_items(**kwargs):
        bag["ownership_queries"].append(kwargs)
        return bag["owned_rows"]

    async def fake_enqueue(**kwargs):
        if bag["enqueue_error"] is not None:
            raise bag["enqueue_error"]
        bag["enqueues"].append(kwargs)
        return SimpleNamespace(id=kwargs["injection_id"])

    fake_cxm = SimpleNamespace(
        conversation=SimpleNamespace(filter_items=fake_filter_items),
        pending_injection=SimpleNamespace(enqueue=fake_enqueue),
    )
    monkeypatch.setattr(db_pkg, "cxm", fake_cxm, raising=False)

    async def fake_load_unified_config(conversation_id: str):
        bag["history_loads"].append(conversation_id)
        return SimpleNamespace(messages=list(bag["history"]))

    monkeypatch.setattr(resolver_mod, "_load_unified_config", fake_load_unified_config)
    return bag


async def _call(
    args: dict[str, Any],
    *,
    conversation_id: str | None = CALLER_CONV,
    request_id: str | None = None,
):
    from matrx_connect.context.app_context import (
        AppContext,
        clear_app_context,
        set_app_context,
    )

    from matrx_ai.tools.implementations.agent_call import agent_call
    from matrx_ai.tools.models import ToolContext

    token = set_app_context(
        AppContext(
            emitter=None,
            user_id=USER_ID,
            conversation_id=conversation_id,
            request_id=request_id,
        )
    )
    try:
        return await agent_call({"agent_id": AGENT_ID, **args}, ToolContext(call_id="call-1"))
    finally:
        clear_app_context(token)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "args",
    [
        {"history_conversation_id": SOURCE_CONV},
        {"history_up_to_position": 3},
        {"remember": True},
        {"remember_visible_to_user": True},
        {"history_mode": "snapshot", "remember_visible_to_user": True},
    ],
)
async def test_history_knobs_require_explicit_mode_and_optin(harness, args) -> None:
    result = await _call(args)
    assert result.success is False
    assert result.error is not None
    assert result.error.error_type == "invalid_arguments"
    assert harness["run_kwargs"] is None  # the child never ran


@pytest.mark.asyncio
async def test_plain_call_untouched_by_collab_paths(harness) -> None:
    result = await _call({})
    assert result.success is True
    assert harness["ownership_queries"] == []
    assert harness["history_loads"] == []
    out = result.output
    assert "history" not in out and "remember" not in out
    assert harness["run_kwargs"]["conversation_id"] is None


@pytest.mark.asyncio
async def test_snapshot_seeds_history_before_authored_messages(harness) -> None:
    result = await _call({"history_mode": "snapshot"})
    assert result.success is True
    # Ownership was checked on the DEFAULT source — the caller's conversation.
    assert harness["ownership_queries"] == [{"id": CALLER_CONV, "created_by": USER_ID}]
    assert harness["history_loads"] == [CALLER_CONV]
    seeded = harness["agent"].config.messages
    assert [getattr(m, "authored", None) for m in seeded] == [False, False, False, True]
    # Snapshot runs in the fresh child conversation — no override.
    assert harness["run_kwargs"]["conversation_id"] is None
    assert result.output["history"] == {
        "mode": "snapshot",
        "source_conversation_id": CALLER_CONV,
        "messages_included": 3,
    }
    assert result.output["child_conversation_id"] == "child-conv-id"


@pytest.mark.asyncio
async def test_snapshot_up_to_position_is_inclusive(harness) -> None:
    result = await _call(
        {
            "history_mode": "snapshot",
            "history_conversation_id": SOURCE_CONV,
            "history_up_to_position": 1,
        }
    )
    assert result.success is True
    assert result.output["history"]["messages_included"] == 2  # positions 0 and 1


@pytest.mark.asyncio
async def test_unowned_conversation_is_not_found_and_never_runs(harness) -> None:
    harness["owned_rows"] = []
    result = await _call({"history_mode": "snapshot", "history_conversation_id": SOURCE_CONV})
    assert result.success is False
    assert result.error.error_type == "not_found"
    assert harness["run_kwargs"] is None
    assert harness["history_loads"] == []


@pytest.mark.asyncio
async def test_snapshot_without_any_conversation_fails_clean(harness) -> None:
    result = await _call({"history_mode": "snapshot"}, conversation_id=None)
    assert result.success is False
    assert result.error.error_type == "invalid_arguments"


@pytest.mark.asyncio
async def test_fork_runs_child_inside_fork(harness, monkeypatch) -> None:
    import matrx_ai._ext as ext

    fork_calls: list[dict] = []

    async def forker(**kwargs):
        fork_calls.append(kwargs)
        return {"conversation_id": FORK_CONV, "message_count": 3}

    before = ext._registry.get("conversation_forker")
    ext.configure_ext(conversation_forker=forker)
    try:
        result = await _call(
            {
                "history_mode": "fork",
                "history_conversation_id": SOURCE_CONV,
                "history_up_to_position": 5,
            }
        )
    finally:
        if before is None:
            ext._registry.pop("conversation_forker", None)
        else:
            ext._registry["conversation_forker"] = before

    assert result.success is True
    assert fork_calls == [
        {
            "source_conversation_id": SOURCE_CONV,
            "user_id": USER_ID,
            "up_to_position": 5,
            "parent_conversation_id": CALLER_CONV,
            "conversation_type": "subagent",
            "title": None,
        }
    ]
    # History is read from the FORK (the cut already applied by the copy) and
    # the child runs INSIDE it.
    assert harness["history_loads"] == [FORK_CONV]
    assert harness["run_kwargs"]["conversation_id"] == FORK_CONV
    assert result.output["history"]["mode"] == "fork"


@pytest.mark.asyncio
async def test_fork_without_forker_fails_feature_unavailable(harness) -> None:
    import matrx_ai._ext as ext

    assert ext._registry.get("conversation_forker") is None
    result = await _call({"history_mode": "fork", "history_conversation_id": SOURCE_CONV})
    assert result.success is False
    assert result.error.error_type == "feature_unavailable"
    assert harness["run_kwargs"] is None


@pytest.mark.asyncio
async def test_remember_enqueues_turn_end_with_provenance(harness) -> None:
    result = await _call(
        {
            "history_mode": "snapshot",
            "history_conversation_id": SOURCE_CONV,
            "remember": True,
        }
    )
    assert result.success is True
    assert len(harness["enqueues"]) == 1
    q = harness["enqueues"][0]
    assert q["conversation_id"] == SOURCE_CONV
    assert q["created_by"] == USER_ID
    assert q["kind"] == "system_message"
    assert q["delivery"] == "turn_end"
    assert q["source"] == "agent_collab"
    assert q["is_visible_to_model"] is True
    assert q["is_visible_to_user"] is False
    assert "child answer" in q["content"]["text"]
    prov = q["metadata"]["agent_collab"]
    assert prov["caller_conversation_id"] == CALLER_CONV
    assert prov["child_conversation_id"] == "child-conv-id"
    assert prov["agent_id"] == AGENT_ID
    assert prov["call_id"] == "call-1"
    assert result.output["remember"]["status"] == "queued"
    assert result.output["remember"]["injection_id"] == q["injection_id"]


@pytest.mark.asyncio
async def test_remember_visible_to_user_flag_rides_through(harness) -> None:
    result = await _call(
        {
            "history_mode": "snapshot",
            "history_conversation_id": SOURCE_CONV,
            "remember": True,
            "remember_visible_to_user": True,
        }
    )
    assert result.success is True
    assert harness["enqueues"][0]["is_visible_to_user"] is True


@pytest.mark.asyncio
async def test_remember_failure_surfaces_without_failing_the_call(harness) -> None:
    harness["enqueue_error"] = RuntimeError("db down")
    result = await _call(
        {
            "history_mode": "snapshot",
            "history_conversation_id": SOURCE_CONV,
            "remember": True,
        }
    )
    # The child already ran (paid) — the call succeeds but the model is told
    # the write-back did NOT land.
    assert result.success is True
    assert result.output["remember"] == {"status": "failed", "error": "db down"}


@pytest.mark.asyncio
async def test_remember_note_is_capped(harness) -> None:
    from matrx_ai.agents.executor import AgentRunResult
    from matrx_ai.tools.implementations.agent_call import REMEMBER_NOTE_MAX_CHARS

    harness["run_result"] = AgentRunResult(
        success=True,
        output="x" * (REMEMBER_NOTE_MAX_CHARS + 5_000),
        metadata={"conversation_id": "child-conv-id"},
    )
    result = await _call(
        {
            "history_mode": "snapshot",
            "history_conversation_id": SOURCE_CONV,
            "remember": True,
        }
    )
    assert result.success is True
    text = harness["enqueues"][0]["content"]["text"]
    assert "[truncated]" in text
    assert len(text) < REMEMBER_NOTE_MAX_CHARS + 500


@pytest.mark.asyncio
async def test_remember_into_internal_conversation_is_rejected_before_run(harness) -> None:
    harness["owned_rows"] = [
        SimpleNamespace(id=SOURCE_CONV, conversation_type="subagent")
    ]
    result = await _call(
        {
            "history_mode": "snapshot",
            "history_conversation_id": SOURCE_CONV,
            "remember": True,
        }
    )
    assert result.success is False
    assert result.error.error_type == "invalid_arguments"
    assert "never drains an inbox" in result.error.message
    assert harness["run_kwargs"] is None  # rejected BEFORE spending money


@pytest.mark.asyncio
async def test_snapshot_of_internal_conversation_without_remember_is_allowed(harness) -> None:
    harness["owned_rows"] = [
        SimpleNamespace(id=SOURCE_CONV, conversation_type="subagent")
    ]
    result = await _call(
        {"history_mode": "snapshot", "history_conversation_id": SOURCE_CONV}
    )
    assert result.success is True  # reading a child transcript is legit


@pytest.mark.asyncio
async def test_soft_deleted_conversation_is_not_found(harness) -> None:
    harness["owned_rows"] = [SimpleNamespace(id=SOURCE_CONV, deleted_at="2026-08-10")]
    result = await _call(
        {"history_mode": "snapshot", "history_conversation_id": SOURCE_CONV}
    )
    assert result.success is False
    assert result.error.error_type == "not_found"


@pytest.mark.asyncio
async def test_history_with_no_new_turn_is_rejected(harness) -> None:
    harness["agent"].config.messages = []  # agent with no authored messages
    result = await _call({"history_mode": "snapshot"})
    assert result.success is False
    assert result.error.error_type == "invalid_arguments"
    assert "user_input" in (result.error.suggested_action or "")
    # user_input unblocks it
    harness["agent"].config.messages = []
    result2 = await _call({"history_mode": "snapshot", "user_input": "review this"})
    assert result2.success is True


@pytest.mark.asyncio
async def test_remember_stamps_enqueued_by_request_id(harness) -> None:
    result = await _call(
        {
            "history_mode": "snapshot",
            "history_conversation_id": SOURCE_CONV,
            "remember": True,
        },
        request_id="req-123",
    )
    assert result.success is True
    meta = harness["enqueues"][0]["metadata"]
    # The self-drain exclusion key: claim_next_turn_end skips items the
    # current run enqueued itself.
    assert meta.get("enqueued_by_request_id") == "req-123"


@pytest.mark.asyncio
async def test_run_agent_threads_conversation_id_into_child_context() -> None:
    from types import SimpleNamespace as NS

    from matrx_connect import ConsoleEmitter
    from matrx_connect.context.app_context import (
        AppContext,
        get_app_context,
        set_app_context,
    )

    from matrx_ai.agents.executor import run_agent
    from matrx_ai.config import UnifiedConfig

    set_app_context(AppContext(emitter=ConsoleEmitter(), user_id=USER_ID))
    config = UnifiedConfig.from_dict(
        {"model": "test-model", "messages": [{"role": "user", "content": "go"}]}
    )
    seen: dict[str, str | None] = {}

    async def execute(user_input=None):
        seen["conversation_id"] = get_app_context().conversation_id
        return NS(
            output="done",
            assistant_response=None,
            config=config,
            usage=None,
            usage_history=[],
            metadata={},
        )

    agent = NS(
        name="collab-child",
        config=config,
        output_schema=None,
        source_id=None,
        source_is_version=False,
        execute=execute,
    )
    result = await run_agent(
        agent,
        label="collab",
        source_app="test",
        source_feature="agent_call",
        conversation_id=FORK_CONV,
        emit_lifecycle=False,
    )
    # The child ran INSIDE the designated conversation (no phantom id), and
    # the result surfaces it for provenance consumers.
    assert seen["conversation_id"] == FORK_CONV
    assert result.metadata["conversation_id"] == FORK_CONV
