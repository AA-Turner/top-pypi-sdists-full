"""Tests for _normalized_severity_key."""

from agentic_devtools.cli.azure_devops.consolidated_review import _normalized_severity_key


class TestNormalizedSeverityKey:
    """Tests for _normalized_severity_key."""

    def test_lowercases_and_strips(self):
        assert _normalized_severity_key("  HIGH  ") == "high"

    def test_already_normalized(self):
        assert _normalized_severity_key("medium") == "medium"

    def test_non_string_returns_empty(self):
        assert _normalized_severity_key(None) == ""
        assert _normalized_severity_key(5) == ""
