"""Tests for render_freshness_for_humans in speckit/phase0/freshness.py (FR-003, FR-004)."""

from __future__ import annotations

from agentic_devtools.cli.speckit.phase0.freshness import render_freshness_for_humans


class TestRenderFreshnessForHumans:
    """Tests for the render_freshness_for_humans function."""

    def test_not_evaluated_renders_as_two_words(self) -> None:
        assert render_freshness_for_humans("not-evaluated") == "not evaluated"

    def test_fresh_is_unchanged(self) -> None:
        assert render_freshness_for_humans("fresh") == "fresh"

    def test_stale_is_unchanged(self) -> None:
        assert render_freshness_for_humans("stale") == "stale"

    def test_unknown_freshness_is_unchanged(self) -> None:
        assert render_freshness_for_humans("unknown-freshness") == "unknown-freshness"
