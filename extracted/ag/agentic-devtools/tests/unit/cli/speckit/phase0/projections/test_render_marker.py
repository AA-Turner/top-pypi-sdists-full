"""Tests for render_marker in speckit/phase0/projections.py (FR-004)."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.speckit.phase0.projections import render_marker


class TestRenderMarker:
    """Tests for the render_marker function."""

    def test_renders_exact_marker_shape(self) -> None:
        result = render_marker(
            chain_operation_id="gh-event:abc",
            operation_id="gh-event:abc",
            run_id="gh:owner/repo:1:1",
            issue_id="owner/repo#1",
            attempt_started_at="2026-01-01T00:00:00Z",
        )
        assert result == (
            "<!-- agdt:phase0-status schemaVersion=1.0 chainOperationId=gh-event:abc "
            "operationId=gh-event:abc runId=gh:owner/repo:1:1 issueId=owner/repo#1 "
            "attemptStartedAt=2026-01-01T00:00:00Z -->"
        )

    def test_retry_marker_shows_distinct_operation_and_chain_ids(self) -> None:
        result = render_marker(
            chain_operation_id="gh-event:abc",
            operation_id="gh-retry:gh-event:abc:20260102T000000Z:2:1",
            run_id="gh:owner/repo:2:1",
            issue_id="owner/repo#1",
            attempt_started_at="2026-01-02T00:00:00Z",
        )
        assert "chainOperationId=gh-event:abc" in result
        assert "operationId=gh-retry:gh-event:abc:20260102T000000Z:2:1" in result

    def test_accepts_issue_id_containing_consecutive_hyphens(self) -> None:
        result = render_marker(
            chain_operation_id="gh-event:abc",
            operation_id="gh-event:abc",
            run_id="gh:owner/repo:1:1",
            issue_id="owner/my--repo#1",
            attempt_started_at="2026-01-01T00:00:00Z",
        )
        assert "issueId=owner/my--repo#1" in result

    def test_rejects_chain_operation_id_with_html_comment_closer(self) -> None:

        with pytest.raises(ValueError, match="chain_operation_id"):
            render_marker(
                chain_operation_id="x-->injected",
                operation_id="gh-event:abc",
                run_id="gh:owner/repo:1:1",
                issue_id="owner/repo#1",
                attempt_started_at="2026-01-01T00:00:00Z",
            )

    def test_rejects_chain_operation_id_with_html_comment_bang_closer(self) -> None:
        with pytest.raises(ValueError, match="chain_operation_id"):
            render_marker(
                chain_operation_id="x--!>injected",
                operation_id="gh-event:abc",
                run_id="gh:owner/repo:1:1",
                issue_id="owner/repo#1",
                attempt_started_at="2026-01-01T00:00:00Z",
            )

    def test_rejects_operation_id_with_whitespace(self) -> None:

        with pytest.raises(ValueError, match="operation_id"):
            render_marker(
                chain_operation_id="gh-event:abc",
                operation_id="has space",
                run_id="gh:owner/repo:1:1",
                issue_id="owner/repo#1",
                attempt_started_at="2026-01-01T00:00:00Z",
            )

    def test_rejects_empty_run_id(self) -> None:

        with pytest.raises(ValueError, match="run_id"):
            render_marker(
                chain_operation_id="gh-event:abc",
                operation_id="gh-event:abc",
                run_id="",
                issue_id="owner/repo#1",
                attempt_started_at="2026-01-01T00:00:00Z",
            )

    def test_rejects_noncanonical_operation_id(self) -> None:
        with pytest.raises(ValueError, match="operation_id"):
            render_marker(
                chain_operation_id="gh-event:abc",
                operation_id="gh/event:abc",
                run_id="gh:owner/repo:1:1",
                issue_id="owner/repo#1",
                attempt_started_at="2026-01-01T00:00:00Z",
            )

    def test_rejects_noncanonical_chain_operation_id(self) -> None:
        with pytest.raises(ValueError, match="chain_operation_id"):
            render_marker(
                chain_operation_id="gh/event:abc",
                operation_id="gh-event:abc",
                run_id="gh:owner/repo:1:1",
                issue_id="owner/repo#1",
                attempt_started_at="2026-01-01T00:00:00Z",
            )

    def test_rejects_noncanonical_issue_id(self) -> None:
        with pytest.raises(ValueError, match="issue_id"):
            render_marker(
                chain_operation_id="gh-event:abc",
                operation_id="gh-event:abc",
                run_id="gh:owner/repo:1:1",
                issue_id="%ZZ",
                attempt_started_at="2026-01-01T00:00:00Z",
            )

    def test_rejects_noncanonical_run_id(self) -> None:
        with pytest.raises(ValueError, match="runId"):
            render_marker(
                chain_operation_id="gh-event:abc",
                operation_id="gh-event:abc",
                run_id="gh:owner/repo:0:1",
                issue_id="owner/repo#1",
                attempt_started_at="2026-01-01T00:00:00Z",
            )

    def test_rejects_noncanonical_attempt_timestamp(self) -> None:
        with pytest.raises(ValueError, match="attemptStartedAt"):
            render_marker(
                chain_operation_id="gh-event:abc",
                operation_id="gh-event:abc",
                run_id="gh:owner/repo:1:1",
                issue_id="owner/repo#1",
                attempt_started_at="not-a-date",
            )

    def test_rejects_inconsistent_delivery_chain(self) -> None:
        with pytest.raises(ValueError, match="must match operation_id"):
            render_marker(
                chain_operation_id="gh-event:a",
                operation_id="gh-event:b",
                run_id="gh:owner/repo:1:1",
                issue_id="owner/repo#1",
                attempt_started_at="2026-01-01T00:00:00Z",
            )

    def test_rejects_inconsistent_retry_chain(self) -> None:
        with pytest.raises(ValueError, match="does not match the chain"):
            render_marker(
                chain_operation_id="gh-event:other",
                operation_id="gh-retry:gh-event:abc:20260101T000000Z:1:1",
                run_id="gh:owner/repo:1:1",
                issue_id="owner/repo#1",
                attempt_started_at="2026-01-01T00:00:00Z",
            )
