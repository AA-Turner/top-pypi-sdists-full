"""The in-loop trim is cache-gated EXACTLY like the resolver's.

The hole this covers: the executor's per-iteration trim used to call
``trim_messages_context`` with no ``cache_state``, so it would rebuild a live
prompt-cache prefix on every iteration to reclaim a few thousand tokens — while
the resolver, calling the same function WITH ``cache_state``, would have
refused that trade. Both now go through ``prepare_for_send``.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import pytest

from matrx_ai.config import ToolResultContent, UnifiedMessage
from matrx_ai.config.send_boundary import (
    STAGE_LOOP,
    STAGE_RESOLVE,
    prepare_for_send,
    reset_loop_state,
)

CONVERSATION_ID = "conv-send-boundary"
REQUEST_ID = "req-send-boundary"


def _tool_result(chars: int) -> UnifiedMessage:
    return UnifiedMessage(
        role="tool",
        position=None,
        content=[
            ToolResultContent(
                tool_use_id=f"call-{chars}-{id(object())}",
                name="large_tool",
                content="x" * chars,
                output_chars=chars,
            )
        ],
    )


def _config(chars: int, count: int = 14) -> SimpleNamespace:
    # 14 loop turns: with the ruled tier 1 (12 positions back, >8000 chars)
    # exactly the first two results are eligible.
    return SimpleNamespace(
        messages=[_tool_result(chars) for _ in range(count)],
        system_instruction=None,
        prompt_cache_key=None,
    )


def _cache_state(age_secs: float) -> dict:
    return {
        "last_response_at": (datetime.now(UTC) - timedelta(seconds=age_secs)).isoformat(),
        "last_provider": "anthropic",
        "est_cache_ttl_secs": 300,
    }


@pytest.fixture(autouse=True)
def _clean_loop_state():
    reset_loop_state(CONVERSATION_ID, REQUEST_ID)
    yield
    reset_loop_state(CONVERSATION_ID, REQUEST_ID)


@pytest.mark.asyncio
async def test_in_loop_trim_skipped_when_cache_alive_and_savings_small() -> None:
    config = _config(2_000)  # ~1K tokens eligible — far below the 5K floor

    prep = await prepare_for_send(
        config,
        stage=STAGE_LOOP,
        conversation_id=CONVERSATION_ID,
        request_id=REQUEST_ID,
        iteration=2,
        cache_state=_cache_state(5),
    )

    assert prep.trim_report is not None
    assert prep.trim_report.eligible_but_skipped_reason == "cache_protect"
    assert prep.trim_report.blocks_rewritten == 0
    assert "tool result cleared" not in str(config.messages[0].content[0].content)


@pytest.mark.asyncio
async def test_in_loop_trim_runs_when_cache_is_dead() -> None:
    config = _config(9_000)

    prep = await prepare_for_send(
        config,
        stage=STAGE_LOOP,
        conversation_id=CONVERSATION_ID,
        request_id=REQUEST_ID,
        iteration=2,
        cache_state=_cache_state(3_600),  # far past the TTL
    )

    assert prep.trim_report is not None
    assert prep.trim_report.eligible_but_skipped_reason is None
    assert prep.trim_report.blocks_rewritten == 2
    assert "tool result cleared" in str(config.messages[0].content[0].content)


@pytest.mark.asyncio
async def test_in_loop_trim_runs_when_savings_are_large_even_with_live_cache() -> None:
    config = _config(20_000)  # ~10K tokens eligible — worth breaking the prefix

    prep = await prepare_for_send(
        config,
        stage=STAGE_LOOP,
        conversation_id=CONVERSATION_ID,
        request_id=REQUEST_ID,
        iteration=2,
        cache_state=_cache_state(5),
    )

    assert prep.trim_report is not None
    assert prep.trim_report.blocks_rewritten == 2
    assert prep.trim_report.freed_chars > 30_000


@pytest.mark.asyncio
async def test_live_loop_send_counts_as_a_fresh_cache() -> None:
    """cx_conversation.cache_state only refreshes when a request COMPLETES, so
    mid-loop it ages while the cache is actually being refreshed every round.
    The boundary's own record of the previous send is the accurate evidence."""
    first = await prepare_for_send(
        _config(9_000),
        stage=STAGE_LOOP,
        conversation_id=CONVERSATION_ID,
        request_id=REQUEST_ID,
        iteration=1,
        cache_state=_cache_state(3_600),
    )
    # Iteration 1 saw a dead persisted cache and trimmed.
    assert first.trim_report is not None
    assert first.trim_report.blocks_rewritten == 2

    second = await prepare_for_send(
        _config(9_000),
        stage=STAGE_LOOP,
        conversation_id=CONVERSATION_ID,
        request_id=REQUEST_ID,
        iteration=2,
    )

    # Iteration 2 knows a send just happened in this very loop.
    assert second.cache_state is not None
    assert second.cache_state.get("cache_state_source") == "live_loop_send"
    assert second.trim_report is not None
    assert second.trim_report.eligible_but_skipped_reason == "cache_protect"


@pytest.mark.asyncio
async def test_trim_audit_lands_in_the_shape_persistence_reads(monkeypatch) -> None:
    """``last_trim_report`` (iteration 1) and ``trim_reports_by_iteration``
    (iteration n) — see orchestrator/requests.py and db/persistence.py."""
    ctx = SimpleNamespace(metadata={})
    monkeypatch.setattr(
        "matrx_ai.context.app_context.try_get_app_context",
        lambda: ctx,
    )

    await prepare_for_send(
        _config(20_000),
        stage=STAGE_RESOLVE,
        conversation_id=CONVERSATION_ID,
        cache_state=_cache_state(3_600),
    )
    assert ctx.metadata["last_trim_report"]["blocks_rewritten"] == 2

    await prepare_for_send(
        _config(20_000),
        stage=STAGE_LOOP,
        conversation_id=CONVERSATION_ID,
        request_id=REQUEST_ID,
        iteration=4,
        cache_state=_cache_state(3_600),
    )
    by_iteration = ctx.metadata["trim_reports_by_iteration"]
    assert by_iteration[4]["blocks_rewritten"] == 2

    # A cache-protect SKIP is audited too — _refresh_cache_state accumulates
    # cumulative_trimmable_chars from exactly those reports.
    reset_loop_state(CONVERSATION_ID, REQUEST_ID)
    await prepare_for_send(
        _config(9_000),
        stage=STAGE_LOOP,
        conversation_id=CONVERSATION_ID,
        request_id=REQUEST_ID,
        iteration=5,
        cache_state=_cache_state(5),
    )
    assert by_iteration[5]["eligible_but_skipped_reason"] == "cache_protect"
    assert by_iteration[5]["policy"]["cache_gate"]["skipped"] is True
