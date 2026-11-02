"""Tests for TraceRecord frozen dataclass."""

from __future__ import annotations

import pytest

from agentic_devtools.orchestration.execution.trace_persistence import TraceRecord


class TestTraceRecord:
    """Tests for TraceRecord construction."""

    def test_basic_construction(self) -> None:
        """All fields stored correctly."""
        record = TraceRecord(
            node_name="test_node",
            start_time=1234567890.0,
            end_time=1234567891.0,
            duration_ms=1000.0,
            model_id="gpt-4",
            prompt_tokens=100,
            completion_tokens=50,
            outcome="success",
        )
        assert record.node_name == "test_node"
        assert record.duration_ms == 1000.0
        assert record.model_id == "gpt-4"
        assert record.outcome == "success"
        assert record.prompt_tokens == 100

    def test_frozen(self) -> None:
        """TraceRecord is frozen."""
        record = TraceRecord(
            node_name="n",
            start_time=0.0,
            end_time=0.0,
            duration_ms=0.0,
        )
        with pytest.raises(AttributeError):
            record.outcome = "error"  # type: ignore[misc]

    def test_defaults(self) -> None:
        """Default values are applied for optional fields."""
        record = TraceRecord(
            node_name="n",
            start_time=0.0,
            end_time=0.0,
            duration_ms=0.0,
        )
        assert record.model_id == ""
        assert record.prompt_tokens == 0
        assert record.completion_tokens == 0
        assert record.tool_id == ""
        assert record.outcome == "success"
