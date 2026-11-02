"""Tests for _build_side_failure_reason helper."""

from __future__ import annotations

from agentic_devtools.orchestration.review.nodes.source_context import _build_side_failure_reason


class TestBuildSideFailureReason:
    """Tests for _build_side_failure_reason."""

    def test_handles_missing_result(self) -> None:
        """Missing retrieval result gets an explicit reason."""
        assert _build_side_failure_reason("source", None) == "source: missing_result"

    def test_falls_back_to_status_when_reason_empty(self) -> None:
        """Empty reason falls back to status-only formatting."""

        class _Result:
            context_status = "unavailable"
            context_status_reason = ""

        assert _build_side_failure_reason("target", _Result()) == "target: unavailable"

    def test_includes_status_reason_when_present(self) -> None:
        """Non-empty reason is appended after status."""

        class _Result:
            context_status = "unavailable"
            context_status_reason = "auth_failed"

        assert _build_side_failure_reason("source", _Result()) == "source: unavailable (auth_failed)"
