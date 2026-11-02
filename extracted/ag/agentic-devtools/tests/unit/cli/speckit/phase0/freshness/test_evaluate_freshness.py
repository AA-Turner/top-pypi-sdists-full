"""Tests for evaluate_freshness in speckit/phase0/freshness.py (FR-007, FR-007a, FR-007b)."""

from __future__ import annotations

from datetime import UTC, datetime

from agentic_devtools.cli.speckit.phase0.freshness import evaluate_freshness

_NOW = datetime(2026, 6, 1, tzinfo=UTC)


class TestEvaluateFreshness:
    """Tests for the evaluate_freshness function."""

    def test_first_run_suppresses_warning(self) -> None:
        result = evaluate_freshness(
            project_metadata_exists=False,
            last_refreshed="2020-01-01T00:00:00Z",
            threshold_days=30,
            run_started_at=_NOW,
        )
        assert result == "not-evaluated"

    def test_within_threshold_is_fresh(self) -> None:
        result = evaluate_freshness(
            project_metadata_exists=True,
            last_refreshed="2026-05-30T00:00:00Z",
            threshold_days=30,
            run_started_at=_NOW,
        )
        assert result == "fresh"

    def test_beyond_threshold_is_stale(self) -> None:
        result = evaluate_freshness(
            project_metadata_exists=True,
            last_refreshed="2026-01-01T00:00:00Z",
            threshold_days=30,
            run_started_at=_NOW,
        )
        assert result == "stale"

    def test_missing_timestamp_is_unknown_freshness(self) -> None:
        result = evaluate_freshness(
            project_metadata_exists=True,
            last_refreshed=None,
            threshold_days=30,
            run_started_at=_NOW,
        )
        assert result == "unknown-freshness"

    def test_future_timestamp_is_unknown_freshness(self) -> None:
        result = evaluate_freshness(
            project_metadata_exists=True,
            last_refreshed="2027-01-01T00:00:00Z",
            threshold_days=30,
            run_started_at=_NOW,
        )
        assert result == "unknown-freshness"

    def test_non_positive_threshold_disables_comparison(self) -> None:
        result = evaluate_freshness(
            project_metadata_exists=True,
            last_refreshed="2020-01-01T00:00:00Z",
            threshold_days=0,
            run_started_at=_NOW,
        )
        assert result == "not-evaluated"

    def test_unknown_freshness_takes_precedence_over_disabled_threshold(self) -> None:
        result = evaluate_freshness(
            project_metadata_exists=True,
            last_refreshed="not-a-timestamp",
            threshold_days=0,
            run_started_at=_NOW,
        )
        assert result == "unknown-freshness"

    def test_first_run_takes_precedence_over_everything(self) -> None:
        result = evaluate_freshness(
            project_metadata_exists=False,
            last_refreshed=None,
            threshold_days=0,
            run_started_at=_NOW,
        )
        assert result == "not-evaluated"
