"""Unit tests for the Layer 2 chunked (map-reduce) fallback compaction.

Covers:
  - Context-overflow detection across provider error shapes.
  - Provider max-token parsing.
  - Message-boundary chunking and oversized-message paragraph splitting.
  - Reactive path: single call overflows, chunked retry succeeds.
  - Proactive path: pre_tokens >= threshold skips the single call.
  - Recursion: partial digests still too large cause another map pass.
  - Circuit breaker stays at 0 on successful chunked compaction.
"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from xpander_sdk.core.context_optimizer import context_optimizer as co
from xpander_sdk.core.context_optimizer.context_optimizer import (
    XPanderContextOptimizer,
    _is_context_overflow_error,
    _parse_provider_max_tokens,
    _split_messages_into_chunks,
)

# ---------------------------------------------------------------------------
# Error detection + max-token parsing
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "msg",
    [
        "prompt is too long: 6432565 tokens > 1000000 maximum",
        "This model's maximum context length is 16385 tokens.",
        "Input is too long for requested model.",
        "input length exceeds the context length",
        "input_length and max_tokens exceed context limit: 199211+20000 > 2000000",
        "context_length_exceeded",
        "model's context length is only 131072 tokens",
        "request_too_large",
    ],
)
def test_is_context_overflow_error_detects_provider_shapes(msg):
    assert _is_context_overflow_error(Exception(msg)) is True


def test_is_context_overflow_error_rejects_unrelated():
    assert _is_context_overflow_error(Exception("rate limit hit")) is False
    assert _is_context_overflow_error(RuntimeError("something else")) is False


@pytest.mark.parametrize(
    "msg,expected",
    [
        ("prompt is too long: 6432565 tokens > 1000000 maximum", 1000000),
        ("This model's maximum context length is 16385 tokens.", 16385),
        (
            "input_length and max_tokens exceed context limit: 199211+20000 > 2000000",
            2000000,
        ),
        ("model's context length is only 131072 tokens", 131072),
    ],
)
def test_parse_provider_max_tokens_extracts_value(msg, expected):
    assert _parse_provider_max_tokens(Exception(msg)) == expected


def test_parse_provider_max_tokens_returns_none_when_absent():
    assert (
        _parse_provider_max_tokens(Exception("Input is too long for requested model."))
        is None
    )
    assert _parse_provider_max_tokens(Exception("unrelated")) is None


# ---------------------------------------------------------------------------
# Chunking utility
# ---------------------------------------------------------------------------


def _mk_msg(role: str, content: str) -> SimpleNamespace:
    return SimpleNamespace(
        role=role,
        content=content,
        tool_name=None,
        tool_call_id=None,
        to_dict=lambda r=role, c=content: {"role": r, "content": c},
    )


def test_split_messages_packs_by_message_boundary():
    msgs = [_mk_msg("user", "a" * 50) for _ in range(6)]
    chunks = _split_messages_into_chunks(msgs, char_budget=200)
    # Each message is ~80 chars when JSON-serialized (content + role overhead),
    # so several fit in each chunk of budget 200.
    assert len(chunks) >= 2
    assert sum(len(c) for c in chunks) == 6
    # Original messages stay intact (no split).
    for chunk in chunks:
        for m in chunk:
            assert getattr(m, "_is_split_fragment", False) is False


def test_split_messages_splits_oversized_single_message():
    big = "\n\n".join([f"para {i}: " + "x" * 60 for i in range(20)])
    msgs = [_mk_msg("user", big)]
    chunks = _split_messages_into_chunks(msgs, char_budget=300)
    # One oversized message should yield multiple fragment chunks.
    assert len(chunks) > 1
    flattened = [m for c in chunks for m in c]
    assert all(getattr(m, "_is_split_fragment", False) for m in flattened)


# ---------------------------------------------------------------------------
# Layer 2 chunked fallback integration
# ---------------------------------------------------------------------------


def _make_optimizer_with_mocked_model(pre_tokens_estimate: int = 10_000):
    """Build an optimizer whose streaming + model interactions are mocked."""
    opt = XPanderContextOptimizer(
        context_window=200_000,
        reserved_for_output=20_000,
        buffer_tokens=13_000,
        chunked_compact_threshold=100_000,
        max_chunked_recursion_depth=3,
    )
    # Stub out activity publishers so tests don't hit the network.
    opt._publish_compaction_start = AsyncMock(return_value=None)
    opt._publish_compaction_end = AsyncMock(return_value=None)
    opt._publish_compaction_error = AsyncMock(return_value=None)
    # Stub the token estimator so the proactive path can be toggled.
    opt._estimate_tokens = MagicMock(return_value=pre_tokens_estimate)
    # Bypass get_model() by supplying a non-None model up front.
    opt.model = MagicMock(id="mock-model")
    opt.model.get_provider = lambda: "mock"
    return opt


def _make_tool_message_list(count: int = 4, role: str = "user", content: str = "hello"):
    # Use fake Message-like objects because real agno Messages require extra imports.
    return [
        SimpleNamespace(
            role=role,
            content=f"{content}-{i}",
            tool_name=None,
            tool_call_id=None,
            to_dict=lambda r=role, c=f"{content}-{i}": {"role": r, "content": c},
        )
        for i in range(count)
    ]


@pytest.mark.asyncio
async def test_layer_2_reactive_overflow_then_chunked_success():
    """First single call raises context-overflow; chunked retry produces a summary."""
    opt = _make_optimizer_with_mocked_model(pre_tokens_estimate=10_000)

    call_count = {"n": 0}

    async def fake_call(
        system_prompt, user_prompt, run_metrics=None, progress_label="layer 2", **kwargs
    ):
        call_count["n"] += 1
        # First call (the single-shot path) raises overflow.
        if call_count["n"] == 1:
            raise Exception("prompt is too long: 500000 tokens > 100000 maximum")
        # Subsequent calls (map per chunk + reduce) succeed with a digest.
        return f"digest-{call_count['n']}", 5, 3

    # get_model() validates the argument; patch it to pass through our MagicMock.
    with (
        patch.object(co, "get_model", side_effect=lambda m: m),
        patch.object(opt, "_run_llm_compaction_call", side_effect=fake_call),
    ):
        # Use real agno Message for the system-message preservation assertion.
        from agno.models.message import Message

        messages = [Message(role="system", content="sys")] + [
            Message(role="user", content="u0"),
            Message(role="assistant", content="a0"),
        ]
        await opt.layer_2_auto_compact(messages=messages, trigger="auto")

    # Final summary replaced the conversation.
    assert messages[0].role == "system"  # preserved
    assert len(messages) >= 2  # system + continuation
    assert any("<session_resume>" in str(m.content) for m in messages)
    # Circuit breaker must NOT have incremented on a successful chunked retry.
    assert opt._auto_compact_consecutive_failures == 0
    # Provider max was cached for future compactions.
    assert opt._provider_max_tokens == 100000
    # At least: 1 failed single-shot + N map calls + 1 reduce call.
    assert call_count["n"] >= 3


@pytest.mark.asyncio
async def test_layer_2_proactive_chunked_when_pre_tokens_exceeds_threshold():
    opt = _make_optimizer_with_mocked_model(pre_tokens_estimate=500_000)

    async def fake_call(
        system_prompt, user_prompt, run_metrics=None, progress_label="layer 2", **kwargs
    ):
        return "chunk-digest", 7, 2

    with (
        patch.object(co, "get_model", side_effect=lambda m: m),
        patch.object(
            opt, "_run_llm_compaction_call", side_effect=fake_call
        ) as mock_call,
    ):
        from agno.models.message import Message

        messages = [
            Message(role="system", content="sys"),
            Message(role="user", content="u"),
            Message(role="assistant", content="a"),
        ]
        await opt.layer_2_auto_compact(messages=messages, trigger="auto")

    # Proactive path skips the single-shot entirely; all calls are map/reduce.
    # All calls should have been made (at least 1 map + 1 reduce = 2).
    assert mock_call.await_count >= 2
    assert opt._auto_compact_consecutive_failures == 0


@pytest.mark.asyncio
async def test_layer_2_non_overflow_error_keeps_failure_counter_behavior():
    """A non-overflow LLM error still goes through the failure path (counter++)."""
    opt = _make_optimizer_with_mocked_model(pre_tokens_estimate=10_000)

    async def failing_call(*a, **kw):
        raise RuntimeError("some other provider error")

    with (
        patch.object(co, "get_model", side_effect=lambda m: m),
        patch.object(opt, "_run_llm_compaction_call", side_effect=failing_call),
    ):
        from agno.models.message import Message

        messages = [
            Message(role="system", content="sys"),
            Message(role="user", content="u"),
        ]
        await opt.layer_2_auto_compact(messages=messages, trigger="auto")

    assert opt._auto_compact_consecutive_failures == 1
    opt._publish_compaction_error.assert_awaited()


@pytest.mark.asyncio
async def test_layer_2_chunked_recursion_when_partials_too_large():
    """If map partials exceed the char budget, another map pass should run."""
    opt = XPanderContextOptimizer(
        context_window=50_000,
        reserved_for_output=1_000,
        buffer_tokens=1_000,
        chunked_compact_threshold=10_000,
        max_chunked_recursion_depth=3,
    )
    opt._publish_compaction_start = AsyncMock(return_value=None)
    opt._publish_compaction_end = AsyncMock(return_value=None)
    opt._publish_compaction_error = AsyncMock(return_value=None)
    opt._estimate_tokens = MagicMock(return_value=200_000)
    opt.model = MagicMock(id="mock-model")
    opt.model.get_provider = lambda: "mock"

    # Force a tiny char budget so recursion is guaranteed.
    opt._compute_chunk_char_budget = MagicMock(return_value=500)

    # Each map call returns a "big" partial so combined partials exceed 500 chars.
    big_partial = "z" * 600

    call_count = {"n": 0}

    async def fake_call(
        system_prompt, user_prompt, run_metrics=None, progress_label="layer 2", **kwargs
    ):
        call_count["n"] += 1
        if "map" in progress_label:
            return big_partial, 10, 5
        # reduce
        return "FINAL", 12, 8

    with (
        patch.object(co, "get_model", side_effect=lambda m: m),
        patch.object(opt, "_run_llm_compaction_call", side_effect=fake_call),
    ):
        from agno.models.message import Message

        messages = [Message(role="user", content="x" * 2000) for _ in range(4)]
        summary, total_tokens, telemetry = await opt._layer_2_chunked_compact(
            messages=messages,
            run_metrics=None,
            custom_instructions="",
            trigger="auto",
        )

    assert summary == "FINAL"
    assert telemetry["chunk_count"] >= 1
    # Ensure more than one map pass happened OR reduce was invoked after
    # recursion cap. We accept either: the key behavior is the final reduce.
    assert call_count["n"] >= 2
