"""Tests for agentic_devtools.adapters.github_schema.canonicalize."""

from __future__ import annotations

from agentic_devtools.adapters.github_schema import canonicalize


class TestCanonicalize:
    """Tests for the canonicalize pure function."""

    def test_bug_report_maps_to_bug(self) -> None:
        """bug_report synonym collapses to bug."""
        assert canonicalize("bug_report") == "bug"

    def test_enhancement_maps_to_feature(self) -> None:
        """enhancement synonym collapses to feature."""
        assert canonicalize("enhancement") == "feature"

    def test_feature_request_maps_to_feature(self) -> None:
        """feature_request synonym collapses to feature."""
        assert canonicalize("feature_request") == "feature"

    def test_unknown_slug_passes_through(self) -> None:
        """Unknown slugs are returned unchanged."""
        assert canonicalize("documentation") == "documentation"

    def test_already_canonical_slug(self) -> None:
        """Already canonical slugs pass through."""
        assert canonicalize("bug") == "bug"

    def test_empty_string_passes_through(self) -> None:
        """Empty string passes through unchanged."""
        assert canonicalize("") == ""
