"""Tests for glyph_with_mods in generate_epic_progress_report."""

from __future__ import annotations

from tests.scripts.generate_epic_progress_report import NOW, _node, report


def test_failed_and_blocked_shows_both_indicators():
    """A node that is both speckit:failed and speckit:blocked renders as 🔴🚧."""
    node = _node(1, labels=["speckit:failed", "speckit:blocked"])
    result = report.glyph_with_mods(node, NOW)
    assert result == "🔴🚧", f"Expected 🔴🚧 but got {result!r}"


def test_failed_only_shows_red_prefix():
    """A failed-only open node shows 🔴 prefix with its normal base glyph."""
    node = _node(1, labels=["speckit:failed"])
    result = report.glyph_with_mods(node, NOW)
    assert result.startswith("🔴"), f"Expected 🔴 prefix but got {result!r}"


def test_blocked_only_shows_no_red_prefix():
    """A blocked-only node shows 🚧 without a 🔴 prefix."""
    node = _node(1, labels=["speckit:blocked"])
    result = report.glyph_with_mods(node, NOW)
    assert result == "🚧", f"Expected 🚧 but got {result!r}"
