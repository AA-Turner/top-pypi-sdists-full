"""Tests for parse_attempt_coordinate in speckit/phase0/comments.py (FR-004)."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.speckit.phase0.comments import parse_attempt_coordinate


class TestParseAttemptCoordinate:
    """Tests for the parse_attempt_coordinate function."""

    def test_extracts_run_and_attempt_numbers(self) -> None:
        coordinate = parse_attempt_coordinate(attempt_started_at="2026-01-01T00:00:00Z", run_id="gh:owner/repo:42:3")
        assert coordinate.attempt_started_at == "2026-01-01T00:00:00Z"
        assert coordinate.workflow_run_id == 42
        assert coordinate.workflow_run_attempt == 3

    def test_rejects_malformed_run_id(self) -> None:
        with pytest.raises(ValueError):
            parse_attempt_coordinate(attempt_started_at="2026-01-01T00:00:00Z", run_id="not-a-run-id")

    def test_rejects_run_id_with_trailing_newline(self) -> None:
        with pytest.raises(ValueError, match="runId is not in the canonical"):
            parse_attempt_coordinate(attempt_started_at="2026-01-01T00:00:00Z", run_id="gh:owner/repo:42:3\n")

    def test_rejects_malformed_attempt_started_at(self) -> None:
        with pytest.raises(ValueError, match="attemptStartedAt"):
            parse_attempt_coordinate(attempt_started_at="not-a-timestamp", run_id="gh:owner/repo:42:3")

    def test_rejects_empty_attempt_started_at(self) -> None:
        with pytest.raises(ValueError, match="attemptStartedAt"):
            parse_attempt_coordinate(attempt_started_at="", run_id="gh:owner/repo:42:3")

    def test_rejects_naive_attempt_started_at(self) -> None:
        with pytest.raises(ValueError, match="canonical"):
            parse_attempt_coordinate(attempt_started_at="2026-01-01T00:00:00", run_id="gh:owner/repo:42:3")

    def test_rejects_offset_attempt_started_at(self) -> None:
        with pytest.raises(ValueError, match="canonical"):
            parse_attempt_coordinate(attempt_started_at="2026-01-01T00:00:00+02:00", run_id="gh:owner/repo:42:3")
