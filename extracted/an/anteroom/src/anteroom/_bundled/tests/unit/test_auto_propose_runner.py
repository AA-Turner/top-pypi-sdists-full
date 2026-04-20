"""Unit tests for the auto-propose runner (#1454)."""

from __future__ import annotations

import json
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from anteroom.config import (
    AppConfig,
    MemoryAutoProposeConfig,
    MemoryConfig,
    MemoryPromotionConfig,
    UserIdentity,
)
from anteroom.services.auto_propose_runner import (
    AutoProposeCooldown,
    AutoProposeResult,
    ProposedItem,
    run_auto_propose,
)
from anteroom.services.memory_promotion import (
    PromotionAgentDisabledError,
    PromotionRateLimitError,
)


def _config(**overrides: Any) -> AppConfig:
    """Build an AppConfig with auto-propose enabled by default."""
    cfg = MagicMock(spec=AppConfig)
    cfg.memory = MagicMock(spec=MemoryConfig)
    cfg.memory.auto_propose = MemoryAutoProposeConfig(enabled=True, max_candidates_per_turn=2)
    cfg.memory.promotion = MemoryPromotionConfig()
    cfg.identity = MagicMock(spec=UserIdentity)
    cfg.identity.user_id = "user-123"
    for k, v in overrides.items():
        if k == "ap_enabled":
            cfg.memory.auto_propose = MemoryAutoProposeConfig(enabled=v)
        elif k == "ap_config":
            cfg.memory.auto_propose = v
    return cfg


def _ai_with_candidates(candidates: list[dict[str, Any]]) -> Any:
    svc = AsyncMock()
    svc.complete = AsyncMock(return_value=json.dumps({"candidates": candidates}))
    return svc


@pytest.mark.asyncio
async def test_disabled_returns_disabled_quickly() -> None:
    cfg = _config(ap_enabled=False)
    db = MagicMock()
    result = await run_auto_propose(
        assistant_text="x" * 200,
        ai_service=AsyncMock(),
        db=db,
        audit_writer=None,
        config=cfg,
        identity_user_id="user-123",
        recalled_memories=[],
        conversation_id="conv-1",
        message_id="msg-1",
        cooldown=AutoProposeCooldown(),
    )
    assert result.reason == "disabled"
    assert result.items == []


@pytest.mark.asyncio
async def test_no_extraction_results_returns_empty() -> None:
    cfg = _config()
    ai = _ai_with_candidates([])  # extractor will return no_results
    result = await run_auto_propose(
        assistant_text="x" * 200,
        ai_service=ai,
        db=MagicMock(),
        audit_writer=None,
        config=cfg,
        identity_user_id="user-123",
        recalled_memories=[],
        conversation_id="conv-1",
        message_id="msg-1",
        cooldown=AutoProposeCooldown(),
    )
    assert result.items == []
    assert result.reason == "no_results"


@pytest.mark.asyncio
async def test_ok_path_emits_one_audit_per_item() -> None:
    cfg = _config()
    ai = _ai_with_candidates(
        [
            {"category": "preference", "content": "User prefers tabs.", "confidence": 0.95},
            {"category": "decision", "content": "Use linkerd.", "confidence": 0.95},
        ]
    )
    fake_mem_a = {"fqn": "@user/memory/pref-aaa"}
    fake_mem_b = {"fqn": "@user/memory/deci-bbb"}
    with (
        patch(
            "anteroom.services.auto_propose_runner.propose_candidate",
            side_effect=[fake_mem_a, fake_mem_b],
        ) as mock_propose,
        patch("anteroom.services.auto_propose_runner.lineage.emit_memory_promotion") as mock_emit,
    ):
        result = await run_auto_propose(
            assistant_text="x" * 200,
            ai_service=ai,
            db=MagicMock(),
            audit_writer=MagicMock(),
            config=cfg,
            identity_user_id="user-123",
            recalled_memories=[],
            conversation_id="conv-1",
            message_id="msg-1",
            cooldown=AutoProposeCooldown(),
        )
    assert result.reason == "ok"
    assert len(result.items) == 2
    assert {it.fqn for it in result.items} == {"@user/memory/pref-aaa", "@user/memory/deci-bbb"}
    assert mock_propose.call_count == 2
    # One audit emission per successful proposal — the runner is the
    # single emission site for both web and CLI per the v3 contract.
    assert mock_emit.call_count == 2
    for call in mock_emit.call_args_list:
        # Real signature: emit_memory_promotion(audit_writer, event, *, fqn, reviewer_id, details)
        kwargs = call.kwargs
        assert call.args[1] == "proposed"
        assert kwargs["reviewer_id"] == "user-123"
        assert kwargs["details"] == {"proposer": "agent", "auto_propose": True}


@pytest.mark.asyncio
async def test_rate_limit_stops_loop_returns_rate_limited() -> None:
    cfg = _config()
    ai = _ai_with_candidates(
        [
            {"category": "preference", "content": "X.", "confidence": 0.95},
            {"category": "preference", "content": "Y.", "confidence": 0.95},
        ]
    )
    with patch(
        "anteroom.services.auto_propose_runner.propose_candidate",
        side_effect=PromotionRateLimitError(conversation_id="conv-1", cap=10, current=10),
    ):
        result = await run_auto_propose(
            assistant_text="x" * 200,
            ai_service=ai,
            db=MagicMock(),
            audit_writer=None,
            config=cfg,
            identity_user_id="user-123",
            recalled_memories=[],
            conversation_id="conv-1",
            message_id="msg-1",
            cooldown=AutoProposeCooldown(),
        )
    assert result.items == []
    assert result.reason == "rate_limited"


@pytest.mark.asyncio
async def test_agent_disabled_stops_loop_returns_agent_disabled() -> None:
    cfg = _config()
    ai = _ai_with_candidates([{"category": "preference", "content": "X.", "confidence": 0.95}])
    with patch(
        "anteroom.services.auto_propose_runner.propose_candidate",
        side_effect=PromotionAgentDisabledError("agent disabled"),
    ):
        result = await run_auto_propose(
            assistant_text="x" * 200,
            ai_service=ai,
            db=MagicMock(),
            audit_writer=None,
            config=cfg,
            identity_user_id="user-123",
            recalled_memories=[],
            conversation_id="conv-1",
            message_id="msg-1",
            cooldown=AutoProposeCooldown(),
        )
    assert result.items == []
    assert result.reason == "agent_disabled"


@pytest.mark.asyncio
async def test_propose_other_exception_skipped_continues() -> None:
    cfg = _config()
    ai = _ai_with_candidates(
        [
            {"category": "preference", "content": "Bad.", "confidence": 0.95},
            {"category": "preference", "content": "Good.", "confidence": 0.95},
        ]
    )
    with patch(
        "anteroom.services.auto_propose_runner.propose_candidate",
        side_effect=[ValueError("boom"), {"fqn": "@user/memory/pref-zzz"}],
    ):
        result = await run_auto_propose(
            assistant_text="x" * 200,
            ai_service=ai,
            db=MagicMock(),
            audit_writer=None,
            config=cfg,
            identity_user_id="user-123",
            recalled_memories=[],
            conversation_id="conv-1",
            message_id="msg-1",
            cooldown=AutoProposeCooldown(),
        )
    assert result.reason == "ok"
    assert len(result.items) == 1
    assert result.items[0].fqn == "@user/memory/pref-zzz"


@pytest.mark.asyncio
async def test_cooldown_skips_repeat_in_same_conversation() -> None:
    cfg = _config()
    ai = _ai_with_candidates([{"category": "preference", "content": "User prefers tabs.", "confidence": 0.95}])
    cooldown = AutoProposeCooldown()
    cooldown.remember("conv-1", "User prefers tabs.", max_items=10)
    with (
        patch("anteroom.services.auto_propose_runner.propose_candidate") as mock_propose,
        patch("anteroom.services.auto_propose_runner.lineage.emit_memory_promotion"),
    ):
        result = await run_auto_propose(
            assistant_text="x" * 200,
            ai_service=ai,
            db=MagicMock(),
            audit_writer=None,
            config=cfg,
            identity_user_id="user-123",
            recalled_memories=[],
            conversation_id="conv-1",
            message_id="msg-1",
            cooldown=cooldown,
        )
    assert result.reason == "cooldown_skipped"
    assert mock_propose.call_count == 0


@pytest.mark.asyncio
async def test_audit_failure_does_not_block_propose() -> None:
    cfg = _config()
    ai = _ai_with_candidates([{"category": "preference", "content": "Pref.", "confidence": 0.95}])
    with (
        patch(
            "anteroom.services.auto_propose_runner.propose_candidate",
            return_value={"fqn": "@user/memory/pref-x"},
        ),
        patch(
            "anteroom.services.auto_propose_runner.lineage.emit_memory_promotion",
            side_effect=RuntimeError("audit broken"),
        ),
    ):
        result = await run_auto_propose(
            assistant_text="x" * 200,
            ai_service=ai,
            db=MagicMock(),
            audit_writer=MagicMock(),
            config=cfg,
            identity_user_id="user-123",
            recalled_memories=[],
            conversation_id="conv-1",
            message_id="msg-1",
            cooldown=AutoProposeCooldown(),
        )
    # Audit failure is non-blocking — proposal still lands.
    assert result.reason == "ok"
    assert len(result.items) == 1


@pytest.mark.asyncio
async def test_provenance_includes_conversation_and_message_ids() -> None:
    cfg = _config()
    ai = _ai_with_candidates([{"category": "preference", "content": "Pref.", "confidence": 0.95}])
    with (
        patch(
            "anteroom.services.auto_propose_runner.propose_candidate",
            return_value={"fqn": "@user/memory/pref-x"},
        ) as mock_propose,
        patch("anteroom.services.auto_propose_runner.lineage.emit_memory_promotion"),
    ):
        await run_auto_propose(
            assistant_text="x" * 200,
            ai_service=ai,
            db=MagicMock(),
            audit_writer=None,
            config=cfg,
            identity_user_id="user-123",
            recalled_memories=[],
            conversation_id="conv-1",
            message_id="msg-99",
            cooldown=AutoProposeCooldown(),
        )
    kwargs = mock_propose.call_args.kwargs
    assert kwargs["proposer"] == "agent"
    assert kwargs["proposer_id"] == "user-123"
    assert kwargs["provenance"]["conversation_id"] == "conv-1"
    assert kwargs["provenance"]["message_id"] == "msg-99"
    assert kwargs["provenance"]["source"] == "auto_propose"


def test_cooldown_already_seen_returns_false_for_new_content() -> None:
    cd = AutoProposeCooldown()
    assert cd.already_seen("conv-1", "fresh content") is False


def test_cooldown_remember_then_seen_returns_true() -> None:
    cd = AutoProposeCooldown()
    cd.remember("conv-1", "user prefers tabs.", max_items=5)
    assert cd.already_seen("conv-1", "user prefers tabs.") is True


def test_cooldown_normalizes_whitespace_and_case() -> None:
    cd = AutoProposeCooldown()
    cd.remember("conv-1", "User prefers tabs.", max_items=5)
    assert cd.already_seen("conv-1", "  user prefers tabs.  ") is True


def test_cooldown_separates_conversations() -> None:
    cd = AutoProposeCooldown()
    cd.remember("conv-1", "X.", max_items=5)
    assert cd.already_seen("conv-2", "X.") is False


def test_cooldown_max_items_evicts_oldest() -> None:
    cd = AutoProposeCooldown()
    cd.remember("conv-1", "A.", max_items=2)
    cd.remember("conv-1", "B.", max_items=2)
    cd.remember("conv-1", "C.", max_items=2)
    assert cd.already_seen("conv-1", "A.") is False
    assert cd.already_seen("conv-1", "C.") is True


def test_cooldown_empty_conversation_id_no_op() -> None:
    cd = AutoProposeCooldown()
    cd.remember("", "X.", max_items=5)
    assert cd.already_seen("", "X.") is False


def test_proposed_item_is_frozen() -> None:
    item = ProposedItem(fqn="@user/memory/x", category="preference", content_preview="X.")
    with pytest.raises(Exception):
        item.fqn = "y"  # type: ignore[misc]


def test_auto_propose_result_default_empty() -> None:
    r = AutoProposeResult()
    assert r.items == []
    assert r.reason == "no_results"


@pytest.mark.asyncio
async def test_empty_identity_user_id_still_proposes() -> None:
    """Edge case: identity_user_id="" lands a candidate with empty proposer_id.

    Some unauthenticated/dev contexts may have no resolved user id.  The
    runner shouldn't crash; the propose call still runs with the empty
    string and audit emission carries reviewer_id="".
    """
    cfg = _config()
    ai = _ai_with_candidates([{"category": "preference", "content": "Pref.", "confidence": 0.95}])
    with (
        patch(
            "anteroom.services.auto_propose_runner.propose_candidate",
            return_value={"fqn": "@user/memory/pref-x"},
        ) as mock_propose,
        patch("anteroom.services.auto_propose_runner.lineage.emit_memory_promotion") as mock_emit,
    ):
        result = await run_auto_propose(
            assistant_text="x" * 200,
            ai_service=ai,
            db=MagicMock(),
            audit_writer=MagicMock(),
            config=cfg,
            identity_user_id="",
            recalled_memories=[],
            conversation_id="conv-1",
            message_id="msg-1",
            cooldown=AutoProposeCooldown(),
        )
    assert result.reason == "ok"
    assert mock_propose.call_args.kwargs["proposer_id"] == ""
    assert mock_emit.call_args.kwargs["reviewer_id"] == ""


@pytest.mark.asyncio
async def test_audit_writer_none_does_not_block_propose() -> None:
    """audit_writer=None must still allow propose_candidate to run.

    The lineage emitter is None-safe by contract; the runner must pass
    None straight through without short-circuiting the propose itself.
    """
    cfg = _config()
    ai = _ai_with_candidates([{"category": "preference", "content": "Pref.", "confidence": 0.95}])
    with (
        patch(
            "anteroom.services.auto_propose_runner.propose_candidate",
            return_value={"fqn": "@user/memory/pref-x"},
        ) as mock_propose,
        patch("anteroom.services.auto_propose_runner.lineage.emit_memory_promotion") as mock_emit,
    ):
        result = await run_auto_propose(
            assistant_text="x" * 200,
            ai_service=ai,
            db=MagicMock(),
            audit_writer=None,
            config=cfg,
            identity_user_id="user-123",
            recalled_memories=[],
            conversation_id="conv-1",
            message_id="msg-1",
            cooldown=AutoProposeCooldown(),
        )
    assert result.reason == "ok"
    assert mock_propose.call_count == 1
    # The runner still calls the lineage emitter — it's the helper's job
    # to no-op on None, not the runner's.
    assert mock_emit.call_count == 1
    assert mock_emit.call_args.args[0] is None


@pytest.mark.asyncio
async def test_empty_conversation_id_skips_cooldown_but_proposes() -> None:
    """Empty conversation_id bypasses cooldown bookkeeping and still proposes.

    AutoProposeCooldown.{already_seen, remember} no-op on empty
    conversation_id.  The runner must still call propose_candidate so a
    no-conversation-bound flow doesn't lose its candidates.
    """
    cfg = _config()
    ai = _ai_with_candidates([{"category": "preference", "content": "Pref.", "confidence": 0.95}])
    with (
        patch(
            "anteroom.services.auto_propose_runner.propose_candidate",
            return_value={"fqn": "@user/memory/pref-x"},
        ) as mock_propose,
        patch("anteroom.services.auto_propose_runner.lineage.emit_memory_promotion"),
    ):
        result = await run_auto_propose(
            assistant_text="x" * 200,
            ai_service=ai,
            db=MagicMock(),
            audit_writer=None,
            config=cfg,
            identity_user_id="user-123",
            recalled_memories=[],
            conversation_id="",
            message_id="msg-1",
            cooldown=AutoProposeCooldown(),
        )
    assert result.reason == "ok"
    assert mock_propose.call_count == 1
    assert mock_propose.call_args.kwargs["provenance"]["conversation_id"] == ""
