"""Unit tests for the perf-oriented context optimizer changes (PRO-1137).

Covers:
  - ``_compute_chunk_char_budget`` honors ``max_chunk_input_tokens``.
  - The map phase runs concurrently — wall-clock < serial budget.
  - Post-compaction hysteresis: ``_should_auto_compact`` returns False on the
    turn immediately after a successful compaction.
  - ``_layer_2_chunked_compact`` returns the (summary, tokens, telemetry)
    triple and ``layer_2_auto_compact`` forwards the telemetry to the end event.
"""

from __future__ import annotations

import asyncio
import time
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from xpander_sdk.core.context_optimizer import context_optimizer as co
from xpander_sdk.core.context_optimizer.context_optimizer import (
    XPanderContextOptimizer,
)


def _make_optimizer(
    pre_tokens_estimate: int = 10_000,
    map_concurrency: int = 5,
    max_chunk_input_tokens: int = 40_000,
) -> XPanderContextOptimizer:
    opt = XPanderContextOptimizer(
        context_window=200_000,
        reserved_for_output=20_000,
        buffer_tokens=13_000,
        chunked_compact_threshold=100_000,
        max_chunked_recursion_depth=3,
        max_chunk_input_tokens=max_chunk_input_tokens,
        map_phase_max_concurrency=map_concurrency,
    )
    opt._publish_compaction_start = AsyncMock(return_value=None)
    opt._publish_compaction_end = AsyncMock(return_value=None)
    opt._publish_compaction_error = AsyncMock(return_value=None)
    opt._publish_compaction_progress = AsyncMock(return_value=None)
    opt._estimate_tokens = MagicMock(return_value=pre_tokens_estimate)
    opt.model = MagicMock(id="mock-model")
    opt.model.get_provider = lambda: "mock"
    return opt


# ---------------------------------------------------------------------------
# Chunk budget cap
# ---------------------------------------------------------------------------


def test_chunk_budget_caps_at_max_chunk_input_tokens():
    opt = _make_optimizer(max_chunk_input_tokens=10_000)
    # 200K context - 20K out - 13K buf = 167K → would normally translate to
    # ~556K char budget. Cap should pull it down to ~33K chars (10K * 4 / 1.2).
    budget = opt._compute_chunk_char_budget()
    assert budget <= int(10_000 * 4 / 1.2) + 1


def test_chunk_budget_unbounded_when_max_chunk_input_tokens_zero():
    opt = _make_optimizer(max_chunk_input_tokens=0)
    # With cap disabled, budget reflects full provider budget.
    budget = opt._compute_chunk_char_budget()
    assert budget > 100_000  # well above any 10K cap


# ---------------------------------------------------------------------------
# Hysteresis grace window
# ---------------------------------------------------------------------------


def test_post_compact_grace_blocks_back_to_back_compaction():
    opt = _make_optimizer()
    # Right at the trigger threshold (167K = 200K - 20K - 13K).
    opt._estimate_tokens = MagicMock(return_value=opt._auto_compact_threshold)
    # Without grace, this should fire.
    assert opt._should_auto_compact(messages=[]) is True

    # Simulate a fresh successful compaction.
    opt._post_compact_grace_remaining = 1
    # Right at the normal threshold, still below grace-raised threshold (+5%).
    opt._estimate_tokens = MagicMock(return_value=opt._auto_compact_threshold)
    assert opt._should_auto_compact(messages=[]) is False
    # Grace consumed.
    assert opt._post_compact_grace_remaining == 0
    # Next turn fires normally.
    assert opt._should_auto_compact(messages=[]) is True


def test_post_compact_grace_still_fires_well_above_raised_threshold():
    opt = _make_optimizer()
    opt._post_compact_grace_remaining = 1
    # Way above even the raised threshold — should still fire.
    opt._estimate_tokens = MagicMock(
        return_value=opt._auto_compact_threshold + int(opt.context_window * 0.5)
    )
    assert opt._should_auto_compact(messages=[]) is True


# ---------------------------------------------------------------------------
# Parallel map phase
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_map_phase_runs_in_parallel():
    """5 chunks at 0.2s each must finish in well under 5*0.2s when concurrent."""
    opt = _make_optimizer(map_concurrency=5, max_chunk_input_tokens=1_000)

    per_chunk_delay = 0.2

    async def fake_call(
        system_prompt,
        user_prompt,
        run_metrics=None,
        progress_label="layer 2",
        **kwargs,
    ):
        await asyncio.sleep(per_chunk_delay)
        return f"partial-{progress_label}", 4, 2

    with (
        patch.object(co, "get_model", side_effect=lambda m: m),
        patch.object(opt, "_run_llm_compaction_call", side_effect=fake_call),
    ):
        # Force 5 chunks by giving 5 reasonably sized messages and a tiny budget.
        messages = [
            SimpleNamespace(
                role="user",
                content="x" * 800,
                tool_name=None,
                tool_call_id=None,
                to_dict=lambda c="x" * 800: {"role": "user", "content": c},
            )
            for _ in range(5)
        ]
        opt._compute_chunk_char_budget = MagicMock(return_value=900)

        start = time.monotonic()
        partials, tokens = await opt._run_chunked_map(
            messages=messages,
            char_budget=900,
            trigger="auto",
            run_metrics=None,
            recursion_depth=0,
        )
        elapsed = time.monotonic() - start

    assert len(partials) == 5
    # Serial would be 1.0s; parallel with concurrency=5 should be near 0.2-0.4s.
    assert (
        elapsed < 0.7
    ), f"map phase too slow ({elapsed:.2f}s) — parallelism not active"
    # Token totals accumulated.
    assert tokens == 5 * (4 + 2)


@pytest.mark.asyncio
async def test_map_phase_concurrency_one_runs_serial():
    opt = _make_optimizer(map_concurrency=1, max_chunk_input_tokens=1_000)

    per_chunk_delay = 0.1

    async def fake_call(*a, **kw):
        await asyncio.sleep(per_chunk_delay)
        return "p", 1, 1

    with (
        patch.object(co, "get_model", side_effect=lambda m: m),
        patch.object(opt, "_run_llm_compaction_call", side_effect=fake_call),
    ):
        messages = [
            SimpleNamespace(
                role="user",
                content="y" * 800,
                tool_name=None,
                tool_call_id=None,
                to_dict=lambda c="y" * 800: {"role": "user", "content": c},
            )
            for _ in range(4)
        ]
        opt._compute_chunk_char_budget = MagicMock(return_value=900)
        start = time.monotonic()
        partials, _ = await opt._run_chunked_map(
            messages=messages,
            char_budget=900,
            trigger="auto",
            run_metrics=None,
            recursion_depth=0,
        )
        elapsed = time.monotonic() - start

    assert len(partials) == 4
    # Serial of 4 × 0.1s ≈ 0.4s; allow generous floor.
    assert elapsed >= 0.35


# ---------------------------------------------------------------------------
# Telemetry plumbing
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_layer_2_chunked_compact_returns_telemetry_triple():
    opt = _make_optimizer(map_concurrency=2, max_chunk_input_tokens=1_000)

    async def fake_call(*a, **kw):
        return "digest", 3, 2

    with (
        patch.object(co, "get_model", side_effect=lambda m: m),
        patch.object(opt, "_run_llm_compaction_call", side_effect=fake_call),
    ):
        messages = [
            SimpleNamespace(
                role="user",
                content="z" * 600,
                tool_name=None,
                tool_call_id=None,
                to_dict=lambda c="z" * 600: {"role": "user", "content": c},
            )
            for _ in range(3)
        ]
        opt._compute_chunk_char_budget = MagicMock(return_value=700)
        summary, tokens, telemetry = await opt._layer_2_chunked_compact(
            messages=messages,
            run_metrics=None,
            custom_instructions="",
            trigger="auto",
        )

    assert summary == "digest"
    assert tokens > 0
    assert telemetry["chunk_count"] == 3
    assert telemetry["map_phase_seconds"] >= 0
    assert telemetry["reduce_phase_seconds"] >= 0


@pytest.mark.asyncio
async def test_layer_2_auto_compact_publishes_mode_and_chunk_count():
    """Proactive chunked path should record mode + chunk_count on the end event."""
    opt = _make_optimizer(
        pre_tokens_estimate=150_000,  # above the 100K chunked threshold
        map_concurrency=2,
        max_chunk_input_tokens=1_000,
    )

    async def fake_call(*a, **kw):
        return "ok", 5, 3

    with (
        patch.object(co, "get_model", side_effect=lambda m: m),
        patch.object(opt, "_run_llm_compaction_call", side_effect=fake_call),
    ):
        from agno.models.message import Message

        messages = [
            Message(role="system", content="sys"),
            Message(role="user", content="u" * 200),
            Message(role="assistant", content="a" * 200),
        ]
        await opt.layer_2_auto_compact(messages=messages, trigger="auto")

    assert opt._publish_compaction_end.await_count == 1
    kwargs = opt._publish_compaction_end.await_args.kwargs
    assert kwargs["mode"] == "chunked-proactive"
    assert kwargs["chunk_count"] is not None
    assert kwargs["chunk_count"] >= 1
    assert kwargs["map_phase_seconds"] is not None
    assert kwargs["reduce_phase_seconds"] is not None
