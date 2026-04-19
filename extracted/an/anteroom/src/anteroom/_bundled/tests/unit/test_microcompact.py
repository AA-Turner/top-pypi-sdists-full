"""Unit tests for the proactive microcompact service (#1266).

Covers the pure-function API (`microcompact`, `MicroCompactResult`, the
`STRATEGIES` registry, and the `oversized_tool_outputs` strategy) plus
the single-source-of-truth invariant with reactive Strategy 1.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from anteroom.services.microcompact import (
    STRATEGIES,
    MicroCompactResult,
    microcompact,
)


def _tool_msg(tool_call_id: str, content: str) -> dict[str, Any]:
    return {"role": "tool", "tool_call_id": tool_call_id, "content": content}


def _assistant_with_tool_call(tc_id: str, tool_name: str) -> dict[str, Any]:
    return {
        "role": "assistant",
        "content": "",
        "tool_calls": [{"id": tc_id, "type": "function", "function": {"name": tool_name, "arguments": "{}"}}],
    }


def _pad(size: int) -> str:
    return "X" * size


class TestNoOpPaths:
    def test_empty_history_returns_success_false(self) -> None:
        result = microcompact([], tool_output_max_chars=100)
        assert result.success is False
        assert result.strategies_applied == []
        assert result.bytes_saved == 0

    def test_below_min_messages_is_noop(self) -> None:
        # Default min_messages=4; three messages should skip all work.
        messages = [
            {"role": "user", "content": _pad(500)},
            _assistant_with_tool_call("tc1", "bash"),
            _tool_msg("tc1", _pad(10_000)),
        ]
        before = deepcopy(messages)
        result = microcompact(messages, tool_output_max_chars=100)
        assert result.success is False
        assert messages == before  # untouched

    def test_no_oversized_messages_is_noop(self) -> None:
        messages = [
            {"role": "user", "content": "q"},
            _assistant_with_tool_call("tc1", "bash"),
            _tool_msg("tc1", "small output"),
            {"role": "user", "content": "next"},
        ]
        before = deepcopy(messages)
        result = microcompact(messages, tool_output_max_chars=1000)
        assert result.success is False
        assert result.strategies_applied == []
        assert messages == before


class TestOversizedToolOutputs:
    def test_single_oversized_tool_message_trimmed(self) -> None:
        messages = [
            {"role": "user", "content": "run"},
            _assistant_with_tool_call("tc1", "bash"),
            _tool_msg("tc1", _pad(5_000)),
            {"role": "user", "content": "continue"},
        ]
        result = microcompact(messages, tool_output_max_chars=100)
        assert result.success is True
        assert result.strategies_applied == ["oversized_tool_outputs"]
        assert result.bytes_saved > 0
        # Trimmed content includes the retry-hint marker.
        trimmed = messages[2]["content"]
        assert "TRUNCATED" in trimmed
        assert "bash" in trimmed  # tool name surfaces in hint
        assert "retry" in trimmed.lower()

    def test_multiple_oversized_messages_all_trimmed(self) -> None:
        messages = [
            _assistant_with_tool_call("tc1", "bash"),
            _tool_msg("tc1", _pad(3_000)),
            _assistant_with_tool_call("tc2", "read_file"),
            _tool_msg("tc2", _pad(4_000)),
            {"role": "user", "content": "ok"},
        ]
        result = microcompact(messages, tool_output_max_chars=50)
        assert result.success is True
        assert result.bytes_saved > 0
        assert "bash" in messages[1]["content"]
        assert "read_file" in messages[3]["content"]

    def test_unknown_tool_name_falls_back(self) -> None:
        """Orphaned tool_call_id (no assistant referencing it) gets 'unknown tool'."""
        messages = [
            {"role": "user", "content": "q"},
            _tool_msg("orphan", _pad(3_000)),
            _tool_msg("orphan2", _pad(3_000)),
            {"role": "user", "content": "next"},
        ]
        result = microcompact(messages, tool_output_max_chars=100)
        assert result.success is True
        assert "unknown tool" in messages[1]["content"]

    def test_non_tool_messages_never_touched(self) -> None:
        """Only role=tool messages are candidates — user/system/assistant untouched."""
        messages = [
            {"role": "system", "content": _pad(10_000)},
            {"role": "user", "content": _pad(10_000)},
            {"role": "assistant", "content": _pad(10_000)},
            _tool_msg("tc1", _pad(10_000)),
        ]
        result = microcompact(messages, tool_output_max_chars=100)
        assert result.success is True
        # Only the role=tool message was trimmed.
        assert len(messages[0]["content"]) == 10_000
        assert len(messages[1]["content"]) == 10_000
        assert len(messages[2]["content"]) == 10_000
        assert "TRUNCATED" in messages[3]["content"]

    def test_exact_boundary_not_trimmed(self) -> None:
        """Content of length == max_chars is NOT trimmed (strict > comparison)."""
        messages = [
            _assistant_with_tool_call("tc1", "bash"),
            _tool_msg("tc1", _pad(100)),  # exactly at threshold
            {"role": "user", "content": "q"},
            {"role": "user", "content": "r"},
        ]
        before = deepcopy(messages)
        result = microcompact(messages, tool_output_max_chars=100)
        assert result.success is False
        assert messages == before

    def test_one_byte_over_threshold_skipped_when_hint_longer(self) -> None:
        """A 1-byte-over trim is a net loss after the retry hint is appended — skip it."""
        messages = [
            _assistant_with_tool_call("tc1", "bash"),
            _tool_msg("tc1", _pad(101)),
            {"role": "user", "content": "q"},
            {"role": "user", "content": "r"},
        ]
        before = deepcopy(messages)
        result = microcompact(messages, tool_output_max_chars=100)
        assert result.success is False
        assert messages == before  # untouched

    def test_large_trim_is_net_win(self) -> None:
        """A trim that produces a significantly smaller message is applied."""
        messages = [
            _assistant_with_tool_call("tc1", "bash"),
            _tool_msg("tc1", _pad(10_000)),
            {"role": "user", "content": "q"},
            {"role": "user", "content": "r"},
        ]
        result = microcompact(messages, tool_output_max_chars=100)
        assert result.success is True
        assert result.bytes_saved > 0


class TestStrategyFilter:
    def test_strategies_filter_selects_only_named(self) -> None:
        messages = [
            _assistant_with_tool_call("tc1", "bash"),
            _tool_msg("tc1", _pad(3_000)),
            {"role": "user", "content": "q"},
            {"role": "user", "content": "r"},
        ]
        result = microcompact(messages, tool_output_max_chars=100, strategies=["oversized_tool_outputs"])
        assert result.strategies_applied == ["oversized_tool_outputs"]

    def test_strategies_filter_with_unknown_logs_and_skips(self) -> None:
        """Unknown strategy name is ignored; other strategies still run."""
        messages = [
            _assistant_with_tool_call("tc1", "bash"),
            _tool_msg("tc1", _pad(3_000)),
            {"role": "user", "content": "q"},
            {"role": "user", "content": "r"},
        ]
        result = microcompact(
            messages,
            tool_output_max_chars=100,
            strategies=["does_not_exist", "oversized_tool_outputs"],
        )
        assert result.strategies_applied == ["oversized_tool_outputs"]

    def test_empty_strategies_list_runs_nothing(self) -> None:
        messages = [
            _assistant_with_tool_call("tc1", "bash"),
            _tool_msg("tc1", _pad(3_000)),
            {"role": "user", "content": "q"},
            {"role": "user", "content": "r"},
        ]
        before = deepcopy(messages)
        result = microcompact(messages, tool_output_max_chars=100, strategies=[])
        assert result.success is False
        assert result.strategies_applied == []
        assert messages == before


class TestResultDataclass:
    def test_result_is_frozen(self) -> None:
        result = MicroCompactResult(success=True, strategies_applied=["oversized_tool_outputs"])
        import dataclasses

        assert dataclasses.is_dataclass(result)
        # Frozen dataclass raises on assignment.
        try:
            result.success = False  # type: ignore[misc]
        except dataclasses.FrozenInstanceError:
            pass
        else:
            raise AssertionError("MicroCompactResult must be frozen")


class TestRegistry:
    def test_registry_keys_are_stable(self) -> None:
        """Phase 1 ships exactly one strategy — guard against accidental renames."""
        assert "oversized_tool_outputs" in STRATEGIES


class TestStrategyOneAgreesWithMicrocompact:
    """Pins the single-source-of-truth invariant (#1266 review)."""

    def test_strategy_1_and_microcompact_agree(self) -> None:
        """Reactive Strategy 1 delegates to microcompact — same input produces same output."""
        from anteroom.services.agent_loop import _truncate_large_tool_outputs

        messages_a = [
            _assistant_with_tool_call("tc1", "bash"),
            _tool_msg("tc1", _pad(5_000)),
            _assistant_with_tool_call("tc2", "read_file"),
            _tool_msg("tc2", _pad(8_000)),
            {"role": "user", "content": "ok"},
        ]
        messages_b = deepcopy(messages_a)

        _ret_a = _truncate_large_tool_outputs(messages_a, max_chars=100)
        result_b = microcompact(
            messages_b,
            tool_output_max_chars=100,
            min_messages=1,
            strategies=["oversized_tool_outputs"],
        )
        assert _ret_a is True
        assert result_b.success is True
        assert messages_a == messages_b
