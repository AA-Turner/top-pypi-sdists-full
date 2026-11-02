"""Tests for matches_chain in speckit/phase0/comments.py (FR-006)."""

from __future__ import annotations

from agentic_devtools.cli.speckit.phase0.comments import MarkerAttributes, matches_chain


def _marker(**overrides: object) -> MarkerAttributes:
    defaults: dict[str, str] = dict(
        schema_version="1.0",
        chain_operation_id="gh-event:abc",
        operation_id="gh-event:abc",
        run_id="gh:owner/repo:1:1",
        issue_id="owner/repo#1",
        attempt_started_at="2026-01-01T00:00:00Z",
    )
    defaults.update({key: value for key, value in overrides.items() if isinstance(value, str)})
    return MarkerAttributes(**defaults)  # type: ignore[arg-type]


class TestMatchesChain:
    """Tests for the matches_chain function."""

    def test_matches_same_chain_and_issue(self) -> None:
        marker = _marker()
        assert matches_chain(marker, chain_operation_id="gh-event:abc", issue_id="owner/repo#1") is True

    def test_rejects_different_chain(self) -> None:
        marker = _marker()
        assert matches_chain(marker, chain_operation_id="gh-event:other", issue_id="owner/repo#1") is False

    def test_rejects_different_issue(self) -> None:
        marker = _marker()
        assert matches_chain(marker, chain_operation_id="gh-event:abc", issue_id="owner/repo#2") is False
