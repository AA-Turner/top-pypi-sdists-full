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
ORG_ID = "33333333-3333-4333-8333-333333333333"
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
        # How many messages the config held when the first-turn pass ran.
        self.pass_saw: list[int] = []

    async def run_first_turn_pass(self) -> _FakeAgent:
        # Idempotent, like the real pass: only the first call fills.
        if not self.pass_saw:
            self.pass_saw.append(len(self.config.messages))
        return self


def _history(*positions: int) -> list[SimpleNamespace]:
    return [SimpleNamespace(role="user", position=p, authored=False) for p in positions]


@pytest.fixture
def harness(monkeypatch: pytest.MonkeyPatch):
    """Wire every seam agent_call touches; return the mutable capture bag."""
    import contextlib

    import matrx_ai.db as db_pkg
    from matrx_ai import _ext
    from matrx_ai.agents import executor as executor_mod
    from matrx_ai.agents import resolver as resolver_mod
    from matrx_ai.agents.definition import Agent
    from matrx_ai.agents.executor import AgentRunResult
    from matrx_ai.db.agx_manager import AgxDefinition

    bag: dict[str, Any] = {
        "in_person_session": False,
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

    @contextlib.asynccontextmanager
    async def acting_as_caller(_ctx: Any = None):
        # The host's seam: RLS decides inside it. Reads outside it are defects.
        bag["in_person_session"] = True
        try:
            yield
        finally:
            bag["in_person_session"] = False

    monkeypatch.setitem(_ext._registry, "acting_as_caller", acting_as_caller)

    async def load_agent(_cls, _agent_id):
        assert bag["in_person_session"], "agent row read outside the person's session"
        return SimpleNamespace(id=AGENT_ID, created_by=USER_ID, is_active=True, is_archived=False)

    monkeypatch.setattr(AgxDefinition, "load_by_id_or_none", classmethod(load_agent))
    monkeypatch.setattr(
        Agent, "from_agent", classmethod(lambda _cls, *_a, **_k: _async_value(bag["agent"]))
    )

    async def fake_run_agent(_agent, **kwargs):
        bag["run_kwargs"] = kwargs
        return bag["run_result"]

    monkeypatch.setattr(executor_mod, "run_agent", fake_run_agent)

    async def fake_filter_items(**kwargs):
        assert bag["in_person_session"], "conversation read outside the person's session"
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
            organization_id=ORG_ID,
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
    # Visibility was asked of the DEFAULT source — the caller's conversation —
    # by id only, inside the person's session: RLS decides, never created_by.
    assert harness["ownership_queries"] == [{"id": CALLER_CONV}]
    assert harness["history_loads"] == [CALLER_CONV]
    seeded = harness["agent"].config.messages
    # The borrowed past (ending on a user turn) is closed by the platform's assistant turn (PB-08).
    assert [getattr(m, "authored", None) for m in seeded] == [False, False, False, None, True]
    # The child's first-turn pass ran over its authored message ALONE, before the
    # borrowed history joined — history is data and is never filled.
    assert harness["agent"].pass_saw == [1]
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
            # the fork is saved in the caller's organization, carried — never the source's
            "organization_id": ORG_ID,
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

    async def execute(user_input=None, *, max_iterations=None, **_kw):
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


# ── run_in_conversation_id: the host names the child's conversation ─────────

CHILD_CONV = "66666666-6666-4666-8666-666666666666"


async def _call_pinned(args: dict[str, Any], *, pinned: str, extra: dict | None = None):
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
            organization_id=ORG_ID,
            conversation_id=CALLER_CONV,
            metadata={"steerable_child": True},  # inherited from a steerable parent
        )
    )
    try:
        return await agent_call(
            {"agent_id": AGENT_ID, **args},
            ToolContext(call_id="call-pinned"),
            run_in_conversation_id=pinned,
            extra_child_metadata=extra,
        )
    finally:
        clear_app_context(token)


@pytest.fixture
def child_metadata(harness, monkeypatch: pytest.MonkeyPatch):
    """The metadata the child actually ran under."""
    from matrx_ai.agents import executor as executor_mod

    seen: list[dict] = []

    async def fake_run_agent(_agent, **kwargs):
        from matrx_connect.context.app_context import get_app_context

        harness["run_kwargs"] = kwargs
        seen.append(dict(get_app_context().metadata))
        return harness["run_result"]

    monkeypatch.setattr(executor_mod, "run_agent", fake_run_agent)
    return seen


@pytest.mark.asyncio
async def test_a_new_pinned_conversation_starts_the_child_there(harness, child_metadata) -> None:
    harness["owned_rows"] = []  # the id does not exist yet
    result = await _call_pinned({"user_input": "go"}, pinned=CHILD_CONV)
    assert result.success is True
    assert harness["run_kwargs"]["conversation_id"] == CHILD_CONV
    assert harness["history_loads"] == []  # nothing to continue
    # Steerability is never inherited: the parent's marker did not ride down.
    assert "steerable_child" not in child_metadata[0]


@pytest.mark.asyncio
async def test_an_existing_pinned_conversation_is_continued_with_its_history(
    harness, child_metadata
) -> None:
    from types import SimpleNamespace as NS

    harness["owned_rows"] = [NS(id=CHILD_CONV)]
    harness["agent"].config.messages = [
        NS(role="system", authored=True),
        NS(role="user", authored=True),  # the authored opening turn, already asked
    ]
    result = await _call_pinned(
        {"user_input": "follow-up"}, pinned=CHILD_CONV, extra={"steerable_child": True}
    )
    assert result.success is True
    assert harness["history_loads"] == [CHILD_CONV]
    assert harness["run_kwargs"]["conversation_id"] == CHILD_CONV
    seeded = harness["agent"].config.messages
    # history first, then ONLY the instructions — the opening turn is not re-asked
    assert [m.role for m in seeded] == ["user", "user", "user", "system"]
    assert child_metadata[0]["steerable_child"] is True


@pytest.mark.asyncio
async def test_a_child_cannot_run_inside_its_caller(harness) -> None:
    result = await _call_pinned({"user_input": "x"}, pinned=CALLER_CONV)
    assert result.success is False and result.error.error_type == "invalid_arguments"
    assert harness["run_kwargs"] is None


@pytest.mark.asyncio
async def test_pinned_conversation_refuses_fork(harness) -> None:
    result = await _call_pinned({"user_input": "x", "history_mode": "fork"}, pinned=CHILD_CONV)
    assert result.success is False and result.error.error_type == "invalid_arguments"
    assert harness["run_kwargs"] is None


@pytest.mark.asyncio
async def test_new_pinned_conversation_may_borrow_a_snapshot(harness, child_metadata) -> None:
    from types import SimpleNamespace as NS

    # The pinned id is absent (a new child); the snapshot source is visible.
    original = harness["owned_rows"]

    import matrx_ai.db as db_pkg

    async def filter_items(**kwargs):
        harness["ownership_queries"].append(kwargs)
        return [] if kwargs.get("id") == CHILD_CONV else original or [NS(id=CALLER_CONV)]

    db_pkg.cxm.conversation.filter_items = filter_items
    result = await _call_pinned(
        {"user_input": "look at this", "history_mode": "snapshot"}, pinned=CHILD_CONV
    )
    assert result.success is True
    assert harness["run_kwargs"]["conversation_id"] == CHILD_CONV
    assert harness["history_loads"] == [CALLER_CONV]


async def _call_as(caller_agent_id: str, args: dict[str, Any]):
    from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

    from matrx_ai.tools.implementations.agent_call import agent_call
    from matrx_ai.tools.models import ToolContext

    token = set_app_context(
        AppContext(
            emitter=None,
            user_id=USER_ID,
            organization_id=ORG_ID,
            conversation_id=CALLER_CONV,
            agent_id=caller_agent_id,
        )
    )
    try:
        return await agent_call({"agent_id": AGENT_ID, **args}, ToolContext(call_id="call-1"))
    finally:
        clear_app_context(token)


def _stored_fork_turn(harness) -> None:
    """Conversation aba87e5b as sent: the borrowed past ends on the person's own request to start
    the fork, and the fork's prompt lands right behind it."""
    from matrx_ai.config.message_config import MessageList, TextContent, UnifiedMessage

    start_fork = (
        "Start a fork of yourself in the foreground and have it summarize this conversation in "
        "exactly three bullets. Show me its bullets."
    )
    harness["history"] = [UnifiedMessage(role="user", content=[TextContent(text=start_fork)])]
    own = MessageList()
    own.append(UnifiedMessage(role="user", content=[TextContent(text="Summarize this conversation in exactly three bullets.")]))
    harness["agent"].config.messages = own


@pytest.mark.asyncio
async def test_a_fork_is_told_the_inherited_conversation_is_its_own(harness) -> None:
    _stored_fork_turn(harness)
    result = await _call_as(AGENT_ID, {"history_mode": "snapshot"})
    assert result.success is True
    frame = harness["agent"].config.messages.render_turn_context()
    assert frame is not None and "your own" in frame
    assert "already" in frame


@pytest.mark.asyncio
async def test_another_agent_shown_history_is_not_told_it_lived_it(harness) -> None:
    _stored_fork_turn(harness)
    result = await _call_as("11111111-1111-4111-8111-111111111111", {"history_mode": "snapshot"})
    assert result.success is True
    frame = harness["agent"].config.messages.render_turn_context()
    assert frame is not None and "your own" not in frame and "not addressed to you" in frame


# ── A fork's inherited history is the same on every path (PB-08 B7 follow-ups) ──────────────────
PARENT_CONV = "17eb435a-000f-4f5c-8f8d-e351591140cf"
FIRST_FORK = "aba87e5b-0a8e-4073-a269-dd3caf1abc52"


def _msg(text: str, position: int) -> Any:
    from matrx_ai.config.message_config import TextContent, UnifiedMessage

    m = UnifiedMessage(role="user", content=[TextContent(text=text)])
    m.position = position
    return m


def _two_conversations(harness, monkeypatch, *, fork_metadata: dict[str, Any]) -> None:
    """The parent (positions 0-1, the stored batch label and the request to fork) and the first
    fork, whose own row stores only its prompt (aba87e5b, metadata as the gate now writes it)."""
    from matrx_ai.agents import resolver as resolver_mod
    from matrx_ai.config.message_config import MessageList

    stored = {
        PARENT_CONV: [_msg("File it under batch label Juniper-0714.", 0), _msg("Start a fork of yourself.", 1)],
        FIRST_FORK: [_msg("Summarize this conversation in exactly three bullets.", 0)],
    }
    rows = {
        PARENT_CONV: SimpleNamespace(id=PARENT_CONV, metadata={}, deleted_at=None),
        FIRST_FORK: SimpleNamespace(id=FIRST_FORK, metadata=fork_metadata, deleted_at=None),
    }

    async def load(conversation_id: str):
        return SimpleNamespace(messages=list(stored.get(conversation_id, [])))

    async def filter_items(**kw):
        row = rows.get(kw.get("id"))
        return [row] if row is not None else []

    monkeypatch.setattr(resolver_mod, "_load_unified_config", load)
    import matrx_ai.db as db_pkg

    db_pkg.cxm.conversation.filter_items = filter_items
    own = MessageList()
    own.append(_msg("What was the batch label?", 0))
    harness["agent"].config.messages = own


def _texts(messages: Any) -> list[str]:
    return [m.content[0].text for m in messages]


@pytest.mark.asyncio
async def test_a_continued_fork_reads_its_inherited_history_and_the_note(harness, monkeypatch) -> None:
    from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

    from matrx_ai.agents.conversation_type import INHERITED_HISTORY_KEY
    from matrx_ai.tools.implementations.agent_call import agent_call
    from matrx_ai.tools.models import ToolContext

    _two_conversations(
        harness, monkeypatch,
        fork_metadata={INHERITED_HISTORY_KEY: {"conversation_id": PARENT_CONV, "up_to_position": 1}},
    )
    token = set_app_context(AppContext(emitter=None, user_id=USER_ID, organization_id=ORG_ID,
                                       conversation_id=PARENT_CONV, agent_id=AGENT_ID))
    try:
        result = await agent_call({"agent_id": AGENT_ID, "user_input": "What was the batch label?"},
                                  ToolContext(call_id="call-1"), run_in_conversation_id=FIRST_FORK)
    finally:
        clear_app_context(token)
    assert result.success is True
    seen = _texts(harness["agent"].config.messages)
    assert seen[:3] == ["File it under batch label Juniper-0714.", "Start a fork of yourself.",
                        "Summarize this conversation in exactly three bullets."]
    frame = harness["agent"].config.messages.render_turn_context() or ""
    assert "your own" in frame


@pytest.mark.asyncio
async def test_a_fork_of_a_fork_gets_the_whole_inherited_history(harness, monkeypatch) -> None:
    from matrx_connect.context.app_context import (
        AppContext,
        clear_app_context,
        get_app_context,
        set_app_context,
    )

    from matrx_ai.agents import executor as executor_mod
    from matrx_ai.agents.conversation_type import INHERITED_HISTORY_KEY
    from matrx_ai.tools.implementations.agent_call import agent_call
    from matrx_ai.tools.models import ToolContext

    _two_conversations(
        harness, monkeypatch,
        fork_metadata={INHERITED_HISTORY_KEY: {"conversation_id": PARENT_CONV, "up_to_position": 1}},
    )
    child_meta: dict[str, Any] = {}

    async def run(_agent, **kwargs):
        child_meta.update(get_app_context().metadata)
        return harness["run_result"]

    monkeypatch.setattr(executor_mod, "run_agent", run)
    token = set_app_context(AppContext(emitter=None, user_id=USER_ID, organization_id=ORG_ID,
                                       conversation_id=FIRST_FORK, agent_id=AGENT_ID))
    try:
        result = await agent_call({"agent_id": AGENT_ID, "user_input": "Summarize.", "history_mode": "snapshot"},
                                  ToolContext(call_id="call-2"),
                                  run_in_conversation_id="6568c8b5-529b-452c-9466-42fb7273aa70")
    finally:
        clear_app_context(token)
    assert result.success is True
    seen = _texts(harness["agent"].config.messages)
    assert seen[:3] == ["File it under batch label Juniper-0714.", "Start a fork of yourself.",
                        "Summarize this conversation in exactly three bullets."]
    # A fork of a fork borrows the first fork's history, which ends on the first fork's own prompt: that is
    # closed too, so the nested fork's prompt is its own turn (the close is a marked, never-stored turn).
    roles = [str(getattr(m.role, "value", m.role)) for m in harness["agent"].config.messages]
    assert roles[-2:] == ["assistant", "user"]
    assert harness["agent"].config.messages[-2].metadata.get("inherited_history_close") is True
    # The nested fork's row records where ITS history comes from: the first fork, to its last turn.
    assert child_meta[INHERITED_HISTORY_KEY] == {"conversation_id": FIRST_FORK, "up_to_position": 0}


def test_the_gate_writes_where_the_inherited_history_comes_from() -> None:
    from matrx_ai.agents.conversation_type import INHERITED_HISTORY_KEY
    from matrx_ai.db.conversation_gate import with_inherited_history

    lineage = {"conversation_id": PARENT_CONV, "up_to_position": 33}
    ctx = SimpleNamespace(metadata={INHERITED_HISTORY_KEY: lineage})
    assert with_inherited_history({}, ctx) == {INHERITED_HISTORY_KEY: lineage}
    assert with_inherited_history({}, SimpleNamespace(metadata={})) == {}


def test_the_inherited_history_note_is_its_own_labelled_platform_part(harness) -> None:
    import importlib

    from matrx_ai.config.message_config import MessageList
    from matrx_ai.config.platform_parts import platform_parts_in_request

    mod = importlib.import_module("matrx_ai.tools.implementations.agent_call")
    messages = MessageList()
    messages.attach_turn_context(mod._inherited_history_note(own=True), slot=mod._INHERITED_HISTORY_SLOT)
    found = platform_parts_in_request({"messages": [{"content": [{"text": messages.render_turn_context()}]}]})
    assert "inherited_history" in [p["id"] for p in found]
    part = next(p for p in found if p["id"] == "inherited_history")
    assert "always on" in part["purpose"] and "your own" in part["text"]


def test_the_inherited_history_note_sits_in_the_standard_instruction_frame(harness) -> None:
    """Live PB-08 (fork 1418545f): under its own slot frame the fork forked again in 6 of 6 replays
    of the stored request; inside the standard frame it answered in 6 of 6."""
    import importlib

    from matrx_ai.config.message_config import TURN_CONTEXT_OPEN, MessageList

    mod = importlib.import_module("matrx_ai.tools.implementations.agent_call")
    messages = MessageList()
    messages.attach_turn_context(mod._inherited_history_note(own=True), slot=mod._INHERITED_HISTORY_SLOT)
    frame = messages.render_turn_context() or ""
    assert frame.startswith(TURN_CONTEXT_OPEN) and 'slot="inherited_history"' not in frame
    assert mod._INHERITED_HISTORY_SLOT not in __import__(
        "matrx_ai.config.message_config", fromlist=["TURN_CONTEXT_SLOT_NOTES"]
    ).TURN_CONTEXT_SLOT_NOTES


@pytest.mark.asyncio
async def test_a_nesting_refusal_is_never_called_a_swallowed_exception(harness) -> None:
    """PB-08 B10 (app_log c7500692): agent_call refused a fork at depth 3 of 3. The refusal is a
    decision built without any exception, yet the executor's banner said the tool "swallowed its
    exception and stringified it". recursion_limit stays a red failure (it is not on the expected
    list, owner ruling 2026-11-08); only the false claim goes. A failure with no traceback that is
    NOT a declared refusal keeps the swallowed-exception line."""
    from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

    from matrx_ai.tools.executor import _is_expected_domain_failure
    from matrx_ai.tools.implementations.agent_call import MAX_AGENT_CALL_DEPTH, agent_call
    from matrx_ai.tools.models import AGENT_DEPTH_METADATA_KEY, ToolContext, ToolError

    token = set_app_context(
        AppContext(emitter=None, user_id=USER_ID, organization_id=ORG_ID, conversation_id=CALLER_CONV,
                   agent_id=AGENT_ID, metadata={AGENT_DEPTH_METADATA_KEY: MAX_AGENT_CALL_DEPTH})
    )
    try:
        result = await agent_call({"agent_id": AGENT_ID, "user_input": "Summarize."},
                                  ToolContext(call_id="call-depth"))
    finally:
        clear_app_context(token)
    assert result.success is False and result.error.error_type == "recursion_limit"
    assert harness["run_kwargs"] is None  # nothing ran
    assert result.error.traceback is None and result.error.refusal is True
    assert not _is_expected_domain_failure(tool_name="agent", error_type="recursion_limit")
    from matrx_ai.tools.executor import _missing_traceback_line

    line = _missing_traceback_line("agent", result.error, expected=False)
    assert "swallowed" not in line and "refusal" in line
    plain = ToolError(error_type="execution", message="boom")
    assert "swallowed its exception" in _missing_traceback_line("agent", plain, expected=False)


def _real(role: str, *blocks: Any, position: int) -> Any:
    from matrx_ai.config.message_config import UnifiedMessage

    return UnifiedMessage(role=role, content=list(blocks), position=position)


@pytest.mark.asyncio
async def test_a_snapshot_never_borrows_the_call_that_started_the_child(harness) -> None:
    """Live class sec_8deaee54 (2026-11-09): a snapshot mandate_call read the caller's conversation
    while its own call was in flight; the child's sanitizer repaired that call as never answered and
    filed an orphan row on every step. The in-flight calls stay out; an older orphan stays in."""
    from matrx_ai.config.message_config import MessageList
    from matrx_ai.config.tools_config import ToolCallContent, ToolResultContent
    from matrx_ai.config.unified_content import TextContent

    harness["history"] = [
        _real("user", TextContent(text="build the tables"), position=0),
        # An older call that really was never answered: still the sanitizer's to repair.
        _real("assistant", ToolCallContent(id="old-lost", name="records"), position=1),
        _real("user", TextContent(text="go on"), position=2),
        _real(
            "assistant",
            TextContent(text="Handing it to the desk."),
            ToolCallContent(id="call-1", name="mandate_call"),
            ToolCallContent(id="sibling-done", name="records"),
            position=3,
        ),
        _real("tool", ToolResultContent(tool_use_id="sibling-done", name="records"), position=4),
    ]
    result = await _call({"history_mode": "snapshot"})
    assert result.success is True
    seeded = harness["agent"].config.messages
    call_ids = [
        b.id for m in seeded for b in (getattr(m, "content", None) or []) if isinstance(b, ToolCallContent)
    ]
    assert "call-1" not in call_ids
    assert call_ids == ["old-lost", "sibling-done"]
    # The trimmed message keeps its text; the stored history was not mutated.
    assert any(
        isinstance(b, TextContent) and b.text == "Handing it to the desk."
        for m in seeded
        for b in (getattr(m, "content", None) or [])
    )
    assert len(harness["history"][3].content) == 3

    borrowed = MessageList([m for m in seeded if getattr(m, "position", None) is not None])
    borrowed.sanitize()
    repaired = [
        b.tool_use_id
        for m in borrowed
        for b in m.content
        if isinstance(b, ToolResultContent) and (b.metadata or {}).get("reason") == "orphan_tool_use"
    ]
    assert repaired == ["old-lost"]


@pytest.mark.asyncio
async def test_a_snapshot_drops_a_message_left_with_nothing(harness) -> None:
    from matrx_ai.config.tools_config import ToolCallContent
    from matrx_ai.config.unified_content import TextContent

    harness["history"] = [
        _real("user", TextContent(text="ask the desk"), position=0),
        _real("assistant", ToolCallContent(id="call-1", name="mandate_call"), position=1),
    ]
    result = await _call({"history_mode": "snapshot"})
    assert result.success is True
    assert result.output["history"]["messages_included"] == 1


# ── The borrowed history never ends inside the child's own turn (PB-08 2026-11-15) ───────────────
def _role_of(message: Any) -> str:
    return str(getattr(message.role, "value", message.role))


def _text_of(message: Any) -> str:
    return " ".join(getattr(b, "text", "") or "" for b in (getattr(message, "content", None) or []))


@pytest.mark.asyncio
@pytest.mark.parametrize("caller", [AGENT_ID, "11111111-1111-4111-8111-111111111111"])
async def test_the_request_that_started_a_child_is_never_part_of_its_turn(harness, caller: str) -> None:
    """Fork 218a3c9d's first request (live, build c564379807): ONE user message held the person's
    "Start a fork of yourself ...", the platform note and the fork's prompt, and the fork called
    agent(fork) again (2 of 2 smokes, 9 of 30 in the k=30 run). The provider merges consecutive user
    turns, so the borrowed history must close with an assistant turn before the child's prompt."""
    _stored_fork_turn(harness)
    result = await _call_as(caller, {"history_mode": "snapshot"})
    assert result.success is True
    seeded = list(harness["agent"].config.messages)
    start = next(i for i, m in enumerate(seeded) if "Start a fork of yourself" in _text_of(m))
    prompt = next(i for i, m in enumerate(seeded) if _text_of(m) == "Summarize this conversation in exactly three bullets.")
    between = [_role_of(m) for m in seeded[start + 1 : prompt]]
    assert "assistant" in between, [(_role_of(m), _text_of(m)[:40]) for m in seeded]
    # The child's prompt is the newest user turn, alone.
    assert _role_of(seeded[-1]) == "user" and "Start a fork" not in _text_of(seeded[-1])
