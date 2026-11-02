"""Tests for IdempotencyEntry frozen dataclass."""

from __future__ import annotations

import pytest

from agentic_devtools.orchestration.execution.idempotency import IdempotencyEntry


class TestIdempotencyEntry:
    """Tests for IdempotencyEntry construction and immutability."""

    def test_construction_happy_path(self) -> None:
        """Entry created with all fields stores values correctly."""
        entry = IdempotencyEntry(
            key="tool:abc123:node:run1",
            timestamp=1234567890.0,
            result_summary='{"success": true}',
            status="success",
        )
        assert entry.key == "tool:abc123:node:run1"
        assert entry.timestamp == 1234567890.0
        assert entry.result_summary == '{"success": true}'
        assert entry.status == "success"

    def test_frozen_immutability(self) -> None:
        """Entry is frozen — attribute assignment raises."""
        entry = IdempotencyEntry(key="k", timestamp=0.0, result_summary="r", status="success")
        with pytest.raises(AttributeError):
            entry.status = "error"  # type: ignore[misc]

    def test_equality(self) -> None:
        """Two entries with same fields are equal."""
        e1 = IdempotencyEntry(key="k", timestamp=1.0, result_summary="r", status="s")
        e2 = IdempotencyEntry(key="k", timestamp=1.0, result_summary="r", status="s")
        assert e1 == e2
