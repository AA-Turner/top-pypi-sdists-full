"""Regression tests for the CLI whole-request token estimate (#1339).

The CLI auto-compact / warn gate uses full-request accounting (messages +
system prompt + tool schemas + extra_system_prompt), with the fixed portion
(system prompt + tool schemas) precomputed once at REPL startup and cached
in a `_FixedRequestOverhead` value. The per-turn helper adds the cached
overhead to the freshly tokenized messages + pending user turn and returns
a full `RequestTokenBreakdown`.

These tests verify:

1. The fixed overhead precompute pulls system_prompt_tokens and
   tool_schema_tokens from `estimate_request_tokens`.
2. The per-turn helper appends the pending user turn to the message list,
   adds cached overhead, and returns the correct totals.
3. Large pending turns push the total above a given warn threshold
   (regression: the previous call site omitted the pending turn entirely).
4. The helper does not mutate the input `ai_messages` list.

Both fast paths are exercised; tiktoken is not mocked because the message
counts are small enough to keep runtime negligible.
"""

from __future__ import annotations

from typing import Any

from anteroom.cli.repl import (
    _compute_fixed_request_overhead,
    _estimate_full_request_with_pending_user,
    _FixedRequestOverhead,
)
from anteroom.services.token_estimator import RequestTokenBreakdown


class TestComputeFixedRequestOverhead:
    def test_overhead_matches_full_estimator(self, monkeypatch: Any) -> None:
        """_compute_fixed_request_overhead must pull system_prompt_tokens
        and tool_schema_tokens from estimate_request_tokens verbatim."""
        captured: dict[str, Any] = {}

        def fake_estimate(**kwargs: Any) -> Any:
            captured.update(kwargs)
            return RequestTokenBreakdown(
                message_tokens=0,
                system_prompt_tokens=77,
                tool_schema_tokens=33,
                total=110,
            )

        monkeypatch.setattr(
            "anteroom.services.token_estimator.estimate_request_tokens",
            fake_estimate,
        )

        overhead = _compute_fixed_request_overhead(
            system_prompt="SYS",
            tool_schemas=[{"function": {"name": "t", "parameters": {}}}],
        )
        assert overhead.system_prompt_tokens == 77
        assert overhead.tool_schema_tokens == 33
        # Must pass empty messages so the per-turn message work isn't
        # double-counted.
        assert captured["messages"] == []
        assert captured["system_prompt"] == "SYS"
        assert captured["extra_system_prompt"] == ""

    def test_empty_inputs_produce_zero_overhead(self) -> None:
        overhead = _compute_fixed_request_overhead(system_prompt="", tool_schemas=None)
        assert overhead.system_prompt_tokens == 0
        assert overhead.tool_schema_tokens == 0


class TestFullRequestWithPendingUser:
    def test_total_includes_messages_cached_overhead_and_extra(self, monkeypatch: Any) -> None:
        """Verify the helper sums message tokens, cached fixed overhead,
        and extra_system_prompt into the full breakdown, and that the
        pending user turn is appended to the messages list."""
        captured_msgs: dict[str, Any] = {}

        def fake_count_messages(messages: list[dict[str, Any]]) -> int:
            captured_msgs["messages"] = list(messages)
            return 100

        def fake_count_text(text: str) -> int:
            return len(text)  # 1 token per char, deterministic

        monkeypatch.setattr(
            "anteroom.services.token_estimator.count_message_tokens",
            fake_count_messages,
        )
        monkeypatch.setattr(
            "anteroom.services.token_estimator.count_text_tokens",
            fake_count_text,
        )

        history = [
            {"role": "user", "content": "hi"},
            {"role": "assistant", "content": "hello"},
        ]
        overhead = _FixedRequestOverhead(system_prompt_tokens=500, tool_schema_tokens=50)

        breakdown = _estimate_full_request_with_pending_user(
            ai_messages=history,
            pending_user_content="PENDING",
            extra_system_prompt="EXTRA",  # len 5, +4 overhead = 9
            fixed_overhead=overhead,
        )

        # Pending user turn must be appended to the message list.
        passed = captured_msgs["messages"]
        assert len(passed) == 3
        assert passed[:2] == history
        assert passed[2] == {"role": "user", "content": "PENDING"}

        # Per-turn message tokens from the mock = 100.
        assert breakdown.message_tokens == 100
        # System prompt = cached fixed (500) + extra_system_prompt (5 + 4) = 509.
        assert breakdown.system_prompt_tokens == 509
        # Tool schemas = cached fixed (50).
        assert breakdown.tool_schema_tokens == 50
        # Total = 100 + 509 + 50 = 659.
        assert breakdown.total == 659

    def test_empty_extra_system_prompt_does_not_add_overhead(self, monkeypatch: Any) -> None:
        monkeypatch.setattr(
            "anteroom.services.token_estimator.count_message_tokens",
            lambda messages: 0,
        )
        monkeypatch.setattr(
            "anteroom.services.token_estimator.count_text_tokens",
            lambda text: len(text),
        )

        overhead = _FixedRequestOverhead(system_prompt_tokens=10, tool_schema_tokens=0)
        breakdown = _estimate_full_request_with_pending_user(
            ai_messages=[],
            pending_user_content="",
            extra_system_prompt="",
            fixed_overhead=overhead,
        )
        # Empty extra must not add the +4 constant overhead.
        assert breakdown.system_prompt_tokens == 10

    def test_pending_turn_does_not_mutate_input(self, monkeypatch: Any) -> None:
        monkeypatch.setattr(
            "anteroom.services.token_estimator.count_message_tokens",
            lambda messages: 0,
        )
        monkeypatch.setattr(
            "anteroom.services.token_estimator.count_text_tokens",
            lambda text: 0,
        )

        history = [{"role": "user", "content": "hello"}]
        overhead = _FixedRequestOverhead(system_prompt_tokens=0, tool_schema_tokens=0)
        _estimate_full_request_with_pending_user(
            ai_messages=history,
            pending_user_content="pending",
            extra_system_prompt="",
            fixed_overhead=overhead,
        )
        assert history == [{"role": "user", "content": "hello"}]

    def test_large_pending_turn_crosses_threshold(self) -> None:
        """End-to-end with the real tokenizer on modestly-sized inputs.

        Regression: under the old call site, a large pending user turn was
        excluded from the estimate entirely. With the fix, a large pending
        turn pushes the total well above a small threshold. Kept modest
        (~10k chars) so tiktoken cost stays negligible in the unit suite.
        """
        history = [{"role": "user", "content": "ok"}]
        overhead = _FixedRequestOverhead(system_prompt_tokens=500, tool_schema_tokens=0)

        small = _estimate_full_request_with_pending_user(
            ai_messages=history,
            pending_user_content="x",
            extra_system_prompt="",
            fixed_overhead=overhead,
        )
        large = _estimate_full_request_with_pending_user(
            ai_messages=history,
            pending_user_content="y " * 5000,  # ~10k chars
            extra_system_prompt="",
            fixed_overhead=overhead,
        )
        assert large.total > small.total
        # Large pending turn tokens (~2500) should dominate over small (~1).
        assert large.message_tokens > small.message_tokens + 1000
        # Fixed overhead is the same in both.
        assert small.system_prompt_tokens == large.system_prompt_tokens == 500
