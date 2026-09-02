"""Tests for _has_structured_http_403 in hierarchy_detector.py."""

from __future__ import annotations

from agentic_devtools.cli.speckit.hierarchy_detector import _has_structured_http_403


class TestHasStructuredHttp403:
    """Tests for _has_structured_http_403."""

    def test_returns_false_for_none(self) -> None:
        """None stderr is not treated as a structured 403."""
        assert _has_structured_http_403(None) is False
