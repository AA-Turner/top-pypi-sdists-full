"""Regression: a provider response id must NEVER become a cx_message PK.

The 2026-07-02 incident: ``AnthropicTranslator.from_anthropic`` stamped the
provider's ``msg_*`` response id onto ``UnifiedMessage.id``. Harmless for six
weeks — persistence always minted its own UUID for unreserved INSERTs — until
the handoff work added ``msg_id = _existing_id or uuid4()``. The first tool
loop (iteration-2 assistant at an unreserved position) then INSERTed with the
provider id as the UUID PK: ``invalid input syntax for type uuid: "msg_01…"``,
the turn 500'd, and the forensic capture died on a NOT NULL constraint.

The contract pinned here (both layers):
  1. Translators never put a provider id on ``UnifiedMessage.id`` — it belongs
     on ``TokenUsage.response_id`` only.
  2. Persistence keys rows off the reservation channel
     (``state.reserved_message_ids``) or mints a fresh UUID. An in-memory id
     that is neither pre-existing nor reserved is DISCARDED (loudly), never
     used as a PK.
  3. The handoff synthetic assistant row rides the same reservation channel
     as every other message.
"""

from __future__ import annotations

from typing import Any
from uuid import UUID, uuid4

import pytest

from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.config.message_config import ToolCallContent, ToolResultContent
from matrx_ai.config.unified_config import UnifiedResponse
from matrx_ai.db.message_positions import APPEND_MESSAGE_POSITION
from matrx_ai.orchestrator.execution_state import ExecutionState
from matrx_ai.orchestrator.requests import AIMatrixRequest, CompletedRequest

PROVIDER_ID = "msg_01QV7a9tmQppX5tFCdRm8dJ7"
CONVERSATION_ID = "11111111-1111-1111-1111-111111111111"
USER_ID = "22222222-2222-2222-2222-222222222222"


def _is_uuid(value: Any) -> bool:
    try:
        UUID(str(value))
        return True
    except (ValueError, TypeError):
        return False


# ── Layer 1: translators ────────────────────────────────────────────────────


def test_from_anthropic_leaves_message_id_none():
    from matrx_ai.providers.anthropic.translator import AnthropicTranslator

    response = {
        "id": PROVIDER_ID,
        "role": "assistant",
        "content": [{"type": "text", "text": "Here are the results."}],
        "stop_reason": "end_turn",
        "usage": {"input_tokens": 10, "output_tokens": 5},
    }
    unified = AnthropicTranslator().from_anthropic(response, matrx_model_name="claude-test")

    msg = unified.messages[0]
    assert msg.id is None, (
        f"UnifiedMessage.id must be cx_message.id only — translator stamped {msg.id!r}"
    )
    # The provider id still lands where it belongs.
    assert unified.usage.response_id == PROVIDER_ID


def test_no_provider_translator_stamps_unified_message_id():
    """Static sweep: no provider file constructs UnifiedMessage with a
    response-derived id. Cheap grep-level guard so a new provider can't
    reintroduce the pattern."""
    import re
    from pathlib import Path

    import matrx_ai.providers as providers_pkg

    providers_dir = Path(providers_pkg.__file__).parent
    pattern = re.compile(
        r"UnifiedMessage\([^)]*id\s*=\s*(response|message_id|response_id|text_message_id)",
        re.DOTALL,
    )
    offenders = []
    for py in providers_dir.rglob("*.py"):
        if pattern.search(py.read_text()):
            offenders.append(str(py))
    assert not offenders, (
        f"Provider file(s) stamp a provider id onto UnifiedMessage.id: {offenders}. "
        f"Provider response ids belong on TokenUsage.response_id."
    )


# ── Layer 2: persistence ────────────────────────────────────────────────────


class _StubModelManager:
    async def load_model_get_string_uuid(self, name):
        return "44444444-4444-4444-4444-444444444444"


class _StubCoordinator:
    def queue(self, *a, **k):
        return ""


class _AsyncAnything:
    """cxm stand-in: any attribute chain resolves to an async no-op."""

    def __getattr__(self, name):
        return _AsyncAnything()

    async def __call__(self, *a, **k):
        return []


def _build_tool_loop_completed() -> CompletedRequest:
    """The exact e-waste trace: user(0) → assistant+tool_use(1) → tool(2) →
    final assistant(3) carrying a polluted provider id."""
    messages = [
        UnifiedMessage(role="user", content=[TextContent(text="find e-waste drop-offs")]),
        UnifiedMessage(
            role="assistant",
            content=[ToolCallContent(id="toolu_1", name="research_web", arguments={"q": "x"})],
        ),
        UnifiedMessage(
            role="tool",
            content=[ToolResultContent(tool_use_id="toolu_1", content="results...")],
        ),
        UnifiedMessage(
            role="assistant",
            content=[TextContent(text="Here is what I found.")],
            id=PROVIDER_ID,  # simulated pollution — must never reach the PK
        ),
    ]
    cfg = UnifiedConfig(model="claude-test", messages=MessageList(_messages=messages))
    req = AIMatrixRequest(
        conversation_id=CONVERSATION_ID,
        config=cfg,
        request_id="33333333-3333-3333-3333-333333333333",
    )
    return CompletedRequest(
        request=req,
        iterations=2,
        final_response=UnifiedResponse(messages=[messages[-1]]),
        trigger_message_position=0,
        result_start_position=1,
        result_end_position=3,
    )


class _StubAppContext:
    user_id = USER_ID
    conversation_id = CONVERSATION_ID
    store = True


@pytest.fixture()
def persist_harness(monkeypatch):
    import matrx_ai.context.app_context as app_ctx_mod
    import matrx_ai.db.persistence as persistence_mod

    # AIMatrixRequest.user_id lazily resolves get_app_context(); persist itself
    # uses try_get_app_context (None → default persist behavior).
    monkeypatch.setattr(app_ctx_mod, "get_app_context", lambda: _StubAppContext())

    creates: list[dict[str, Any]] = []
    updates: list[tuple[str, dict[str, Any]]] = []

    monkeypatch.setattr(persistence_mod, "ai_model_manager_instance", _StubModelManager())
    monkeypatch.setattr(persistence_mod, "_get_coordinator", lambda: _StubCoordinator())
    monkeypatch.setattr(
        persistence_mod,
        "_queue_message_create",
        lambda **kw: creates.append(kw) or "",
    )
    monkeypatch.setattr(
        persistence_mod,
        "_queue_message_update",
        lambda mid, **kw: updates.append((mid, kw)) or "",
    )
    monkeypatch.setattr(persistence_mod, "_queue_conversation_update", lambda cid, **kw: "")
    monkeypatch.setattr(persistence_mod, "_queue_request_create", lambda **kw: "")
    monkeypatch.setattr(persistence_mod, "_queue_user_request_update", lambda rid, **kw: "")

    async def _no_hide(*a, **k):
        return 0

    async def _no_backfill(*a, **k):
        return []

    async def _no_cache(*a, **k):
        return None

    monkeypatch.setattr(persistence_mod, "_hide_superseded_failed_turns", _no_hide)
    monkeypatch.setattr(persistence_mod, "_backfill_tool_message", _no_backfill)
    monkeypatch.setattr(persistence_mod, "_refresh_cache_state", _no_cache)
    monkeypatch.setattr(persistence_mod, "_emit_context_state", _no_cache)
    monkeypatch.setattr(persistence_mod, "cxm", _AsyncAnything())
    monkeypatch.setattr(persistence_mod, "try_get_tracker", lambda: None)

    return persistence_mod, creates, updates


@pytest.mark.asyncio
async def test_unreserved_assistant_insert_mints_uuid_not_provider_id(persist_harness):
    persistence_mod, creates, updates = persist_harness
    completed = _build_tool_loop_completed()

    # Loop-start reservations exist for positions 0 and 1 ONLY — exactly the
    # live trace. Position 3 (iteration-2 final assistant) is unreserved.
    state = ExecutionState()
    state.reserved_message_ids = {0: str(uuid4()), 1: str(uuid4())}

    result = await persistence_mod.persist_completed_request(
        completed, conversation_id=CONVERSATION_ID, state=state
    )

    # Reserved positions rode the UPDATE path with their reserved ids.
    updated_ids = {mid for mid, _ in updates}
    assert state.reserved_message_ids[0] in updated_ids
    assert state.reserved_message_ids[1] in updated_ids

    # The unreserved rows (tool @2, assistant @3) were INSERTed with fresh
    # UUIDs — and the provider id appears NOWHERE.
    assert creates, "expected fresh INSERTs for the unreserved positions"
    for kw in creates:
        assert _is_uuid(kw["id"]), f"non-UUID cx_message PK queued: {kw['id']!r}"
        assert kw["id"] != PROVIDER_ID
    assert PROVIDER_ID not in result["message_ids"]
    assert all(_is_uuid(mid) for mid in result["message_ids"])


@pytest.mark.asyncio
async def test_reserved_id_matching_message_id_is_honored(persist_harness):
    """The handoff contract at the persistence layer: a message whose id IS
    this position's reservation (the synthetic assistant row) keeps that id
    via the UPDATE path — no duplicate INSERT, no fresh mint."""
    persistence_mod, creates, updates = persist_harness
    completed = _build_tool_loop_completed()

    synthetic_id = str(uuid4())
    completed.request.config.messages[3].id = synthetic_id

    state = ExecutionState()
    state.reserved_message_ids = {0: str(uuid4()), 1: str(uuid4()), 3: synthetic_id}

    result = await persistence_mod.persist_completed_request(
        completed, conversation_id=CONVERSATION_ID, state=state
    )

    assert synthetic_id in {mid for mid, _ in updates}
    assert synthetic_id in result["message_ids"]
    assert all(kw["id"] != synthetic_id for kw in creates)


@pytest.mark.asyncio
async def test_repeated_persist_sets_immutable_system_instruction_once(persist_harness, monkeypatch):
    """A second finalizer pass must not queue a duplicate immutable-column write
    before the first coordinator flush becomes visible to a DB read."""
    persistence_mod, _creates, _updates = persist_harness
    completed = _build_tool_loop_completed()
    completed.request.config.system_instruction = "You are concise."
    conversation_updates: list[dict[str, Any]] = []
    monkeypatch.setattr(
        persistence_mod,
        "_queue_conversation_update",
        lambda _cid, **fields: conversation_updates.append(fields) or "",
    )

    await persistence_mod.persist_completed_request(completed, conversation_id=CONVERSATION_ID)
    await persistence_mod.persist_completed_request(completed, conversation_id=CONVERSATION_ID)

    assert sum("system_instruction" in fields for fields in conversation_updates) == 1


# ── Layer 3: the handoff registers its synthetic row like every other message ─


@pytest.mark.asyncio
async def test_finalize_handoff_registers_synthetic_id_on_reservation_channel(monkeypatch):
    """_finalize_handoff must put the synthetic assistant id into
    state.reserved_message_ids AND queue the reservation INSERT — never rely
    on UnifiedMessage.id leaking through to persistence (that leak is the
    channel the provider-id bug rode in on)."""
    import matrx_ai.orchestrator.executor as executor_mod
    import matrx_ai.persistence.queue_helpers as qh

    creates: list[dict[str, Any]] = []
    monkeypatch.setattr(qh, "queue_message_create", lambda **kw: creates.append(kw) or "")
    monkeypatch.setattr(qh, "get_coordinator", lambda: _StubCoordinator())

    persisted: dict[str, Any] = {}

    async def _capture_persist(**kwargs):
        persisted.update(kwargs)
        return None

    async def _fake_finalize(**kwargs):
        return "completed-sentinel"

    monkeypatch.setattr(executor_mod, "_persist_turn_and_commit", _capture_persist)
    monkeypatch.setattr(executor_mod, "_finalize_and_persist", _fake_finalize)

    messages = [
        UnifiedMessage(role="user", content=[TextContent(text="ask the specialist")]),
        UnifiedMessage(
            role="assistant",
            content=[ToolCallContent(id="toolu_h", name="agent__specialist", arguments={})],
        ),
        UnifiedMessage(
            role="tool",
            content=[ToolResultContent(tool_use_id="toolu_h", content="handoff stub")],
        ),
    ]
    cfg = UnifiedConfig(model="claude-test", messages=MessageList(_messages=messages))
    req = AIMatrixRequest(conversation_id=CONVERSATION_ID, config=cfg)

    class _Outcome:
        final_text = "The specialist's answer."
        child_conversation_id = str(uuid4())
        child_execution_id = str(uuid4())
        agent_version_id = str(uuid4())
        agent_id = str(uuid4())
        model_id = str(uuid4())
        value_ref_key = None

    class _Emitter:
        async def send_info(self, *a, **k):
            return None

    class _ExecCtx:
        conversation_id = CONVERSATION_ID
        user_id = USER_ID
        store = True
        emitter = _Emitter()

    state = ExecutionState()
    state.reserved_message_ids = {0: str(uuid4()), 1: str(uuid4())}

    result = await executor_mod._finalize_handoff(
        handoff_outcome=_Outcome(),
        current_request=req,
        iteration=1,
        response=UnifiedResponse(messages=[messages[1]]),
        trigger_position=0,
        pre_execution_message_count=1,
        debug=False,
        state=state,
        exec_ctx=_ExecCtx(),
    )

    assert result == "completed-sentinel"
    # The synthetic message landed at position 3 with a UUID id...
    synthetic_position = 3
    synthetic_msg = persisted["current_request"].config.messages[synthetic_position]
    assert _is_uuid(synthetic_msg.id)
    # ...registered on the reservation channel persistence actually honors...
    assert state.reserved_message_ids.get(synthetic_position) == synthetic_msg.id
    # ...and its reservation INSERT was queued before the persist barrier.
    synthetic_creates = [kw for kw in creates if kw.get("id") == synthetic_msg.id]
    assert len(synthetic_creates) == 1
    assert synthetic_creates[0]["position"] == APPEND_MESSAGE_POSITION
