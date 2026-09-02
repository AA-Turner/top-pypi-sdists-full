"""Tests for the Turn-Boundary Inbox drain (drain_pending_injections) and the
Anthropic consecutive-role merge that makes injected user turns valid.

DB stubs are configured by the top-level conftest before collection; the inbox
manager's ``claim_pending`` is monkeypatched so no live DB is needed.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from matrx_ai.tools import dynamic_drain


class _CapturingEmitter:
    def __init__(self) -> None:
        self.injection_payloads: list[Any] = []

    async def send_injection_consumed(self, payload: Any) -> None:
        self.injection_payloads.append(payload)


def _ctx(conversation_id: str | None, emitter: Any = None) -> SimpleNamespace:
    return SimpleNamespace(
        conversation_id=conversation_id,
        request_id="req-1",
        emitter=emitter,
    )


def _config() -> SimpleNamespace:
    # The drain only needs ``.messages`` to support append + len; a list does both.
    return SimpleNamespace(messages=[])


def _row(injection_id: str, text: str, kind: str = "user_message", seq: int = 1) -> SimpleNamespace:
    return SimpleNamespace(id=injection_id, kind=kind, content={"text": text}, enqueued_seq=seq)


async def test_drain_appends_messages_and_emits(monkeypatch):
    rows = [_row("a", "first", seq=1), _row("b", "second", seq=2)]

    async def _claim(conversation_id, *, request_id=None):
        assert conversation_id == "conv-1"
        assert request_id == "req-1"
        return rows

    import matrx_ai.db.cx_managers as cxm_mod

    monkeypatch.setattr(cxm_mod.cxm, "pending_injection", SimpleNamespace(claim_pending=_claim))

    emitter = _CapturingEmitter()
    config = _config()
    ctx = _ctx("conv-1", emitter)

    await dynamic_drain.drain_pending_injections(config, ctx)

    # Two user-role messages appended at sequential positions.
    assert len(config.messages) == 2
    assert [m.role for m in config.messages] == ["user", "user"]
    # One batched event carrying both items with their positions.
    assert len(emitter.injection_payloads) == 1
    payload = emitter.injection_payloads[0]
    assert payload.count == 2
    assert [it.position for it in payload.items] == [0, 1]
    assert {it.injection_id for it in payload.items} == {"a", "b"}


async def test_drain_handles_stringified_jsonb_content(monkeypatch):
    """claim_pending returns raw asyncpg rows where JSONB content is a STRING
    (RETURNING * doesn't parse it). The drain must coerce it, not crash."""
    import json as _json

    rows = [
        SimpleNamespace(
            id="x",
            kind="user_message",
            enqueued_seq=1,
            content=_json.dumps({"text": "stringified!"}),  # ← a JSON string, not a dict
            is_visible_to_user=True,
        )
    ]

    async def _claim(conversation_id, *, request_id=None):
        return rows

    import matrx_ai.db.cx_managers as cxm_mod

    monkeypatch.setattr(cxm_mod.cxm, "pending_injection", SimpleNamespace(claim_pending=_claim))

    emitter = _CapturingEmitter()
    config = _config()
    await dynamic_drain.drain_pending_injections(config, _ctx("conv-1", emitter))

    assert len(config.messages) == 1
    # The text was correctly extracted from the stringified content.
    assert emitter.injection_payloads[0].items[0].text == "stringified!"


async def test_drain_empty_is_noop(monkeypatch):
    async def _claim(conversation_id, *, request_id=None):
        return []

    import matrx_ai.db.cx_managers as cxm_mod

    monkeypatch.setattr(cxm_mod.cxm, "pending_injection", SimpleNamespace(claim_pending=_claim))

    emitter = _CapturingEmitter()
    config = _config()
    await dynamic_drain.drain_pending_injections(config, _ctx("conv-1", emitter))

    assert config.messages == []
    assert emitter.injection_payloads == []


async def test_drain_no_conversation_id_is_noop():
    config = _config()
    emitter = _CapturingEmitter()
    await dynamic_drain.drain_pending_injections(config, _ctx(None, emitter))
    assert config.messages == []
    assert emitter.injection_payloads == []


async def test_drain_skips_internal_agents_without_db_hit(monkeypatch):
    """Internal / sub-agent forks have no Turn-Boundary Inbox — the drain must
    NOT issue the cx_pending_injection claim UPDATE for them. Under a concurrent
    internal fan-out those repeated UPDATEs were causing QueryTimeoutError on the
    pool. The skip must short-circuit BEFORE any DB call."""
    claimed = False

    async def _claim(conversation_id, *, request_id=None):
        nonlocal claimed
        claimed = True
        return []

    import matrx_ai.db.cx_managers as cxm_mod

    monkeypatch.setattr(cxm_mod.cxm, "pending_injection", SimpleNamespace(claim_pending=_claim))

    config = _config()
    emitter = _CapturingEmitter()
    ctx = _ctx("conv-1", emitter)
    ctx.is_internal_agent = True  # a child-agent fork

    await dynamic_drain.drain_pending_injections(config, ctx)

    assert claimed is False  # no DB claim issued
    assert config.messages == []
    assert emitter.injection_payloads == []


def test_anthropic_translator_merges_consecutive_user_turns():
    """A tool-result turn (role='tool' → 'user') followed by an injected user
    turn must collapse into ONE user turn so Anthropic's role alternation holds."""
    from matrx_ai.config import TextContent, UnifiedConfig, UnifiedMessage
    from matrx_ai.providers.anthropic.translator import AnthropicTranslator
    from matrx_ai.testing.profile_factory import make_profile

    config = UnifiedConfig(
        model="claude-opus-4-7",
        messages=[
            UnifiedMessage(role="user", content=[TextContent(text="do the thing")]),
            UnifiedMessage(role="assistant", content=[TextContent(text="working")]),
            # A tool-result turn (role="tool" collapses to "user")...
            UnifiedMessage(role="tool", content=[TextContent(text="tool output")]),
            # ...immediately followed by an injected user message.
            UnifiedMessage(role="user", content=[TextContent(text="actually, focus on X")]),
        ],
    )
    out = AnthropicTranslator().to_anthropic(
        config, make_profile(model_name="claude-opus-4-7", wire_format="anthropic_chat")
    )
    roles = [m["role"] for m in out["messages"]]
    # Must strictly alternate — no consecutive 'user'.
    assert roles == ["user", "assistant", "user"], roles
    # The merged final user turn carries BOTH the tool output and the injection.
    assert len(out["messages"][-1]["content"]) == 2


async def test_turn_end_items_wait_for_the_final_boundary(monkeypatch):
    """QUEUE items (delivery='turn_end') never drain mid-run: the default drain
    claims only steers; ``include_turn_end=True`` (the run's final boundary)
    additionally claims exactly ONE queued item — one queued message per turn,
    per the three-send-modes ruling."""
    steer = _row("s1", "steer me", seq=1)
    queued = _row("q1", "queued until the end", seq=2)
    turn_end_calls: list[str] = []

    async def _claim(conversation_id, *, request_id=None):
        return [steer]

    async def _claim_turn_end(conversation_id, *, request_id=None):
        turn_end_calls.append(conversation_id)
        return [queued]

    import matrx_ai.db.cx_managers as cxm_mod

    monkeypatch.setattr(
        cxm_mod.cxm,
        "pending_injection",
        SimpleNamespace(claim_pending=_claim, claim_next_turn_end=_claim_turn_end),
    )

    # Mid-run drain: steers only, the queued item untouched.
    emitter = _CapturingEmitter()
    config = _config()
    await dynamic_drain.drain_pending_injections(config, _ctx("conv-1", emitter))
    assert [m.content[0].text for m in config.messages] == ["steer me"]
    assert turn_end_calls == []

    # Final boundary: the queued item delivers too.
    emitter2 = _CapturingEmitter()
    config2 = _config()
    await dynamic_drain.drain_pending_injections(
        config2, _ctx("conv-1", emitter2), include_turn_end=True
    )
    assert [m.content[0].text for m in config2.messages] == [
        "steer me",
        "queued until the end",
    ]
    assert turn_end_calls == ["conv-1"]
    assert {it.injection_id for it in emitter2.injection_payloads[0].items} == {"s1", "q1"}


async def test_hidden_injection_stamps_message_visibility_metadata(monkeypatch):
    """A hidden inbox item (is_visible_to_user=false — steering notes,
    agent_collab write-backs) must stay hidden on the DURABLE row: persistence
    lifts metadata['is_visible_to_user'] into the typed column, so the drain
    must stamp it on the appended message, not just the transient event."""
    rows = [
        SimpleNamespace(
            id="hidden-1",
            kind="system_message",
            content={"text": "secret steer"},
            enqueued_seq=1,
            is_visible_to_user=False,
        ),
        _row("visible-1", "normal message", seq=2),
    ]

    async def _claim(conversation_id, *, request_id=None):
        return rows

    import matrx_ai.db.cx_managers as cxm_mod

    monkeypatch.setattr(cxm_mod.cxm, "pending_injection", SimpleNamespace(claim_pending=_claim))

    config = _config()
    ctx = _ctx("conv-1", _CapturingEmitter())
    await dynamic_drain.drain_pending_injections(config, ctx)

    assert len(config.messages) == 2
    hidden, visible = config.messages
    assert hidden.metadata.get("is_visible_to_user") is False
    assert "is_visible_to_user" not in (visible.metadata or {})


async def test_claim_next_turn_end_skips_items_enqueued_by_the_claiming_run():
    """Self-drain exclusion: a run never delivers a turn_end item it enqueued
    itself (metadata.enqueued_by_request_id) — the item waits for the NEXT run.
    Items from other requests (or with no stamp) are claimed normally."""
    from matrx_ai.db._cx_managers_impl import CxPendingInjectionManager

    own = SimpleNamespace(
        id="own-1",
        enqueued_seq=1,
        metadata={"enqueued_by_request_id": "req-1"},
    )
    other = SimpleNamespace(
        id="other-1",
        enqueued_seq=2,
        metadata={"enqueued_by_request_id": "someone-else"},
    )
    updates: list[dict] = []

    async def filter_items(**kwargs):
        return [own, other]

    async def update_where(where, **fields):
        updates.append({"where": where, **fields})
        return SimpleNamespace(updated_rows=[other])

    fake_self = SimpleNamespace(filter_items=filter_items, update_where=update_where)

    claimed = await CxPendingInjectionManager.claim_next_turn_end(
        fake_self, "conv-1", request_id="req-1"
    )
    # The run's own item is skipped; the OTHER request's item (later seq) wins.
    assert [r.id for r in claimed] == ["other-1"]
    assert updates[0]["where"]["id"] == "other-1"

    # With only the run's own item pending, nothing is claimed at all.
    async def filter_only_own(**kwargs):
        return [own]

    fake_self_own = SimpleNamespace(filter_items=filter_only_own, update_where=update_where)
    claimed_own = await CxPendingInjectionManager.claim_next_turn_end(
        fake_self_own, "conv-1", request_id="req-1"
    )
    assert claimed_own == []
