"""Tests for is_consolidated_comment."""

from agentic_devtools.cli.azure_devops.consolidated_review import (
    build_consolidated_marker,
    is_consolidated_comment,
)


class TestIsConsolidatedComment:
    """Tests for is_consolidated_comment."""

    def test_true_for_v2_consolidated_marker(self):
        marker = build_consolidated_marker(42, "abc123def456")
        assert is_consolidated_comment(f"{marker}\n## review") is True

    def test_true_for_marker_without_commit(self):
        marker = build_consolidated_marker(42, None)
        assert is_consolidated_comment(marker) is True

    def test_false_for_none(self):
        assert is_consolidated_comment(None) is False

    def test_false_for_empty(self):
        assert is_consolidated_comment("") is False

    def test_false_for_plain_text(self):
        assert is_consolidated_comment("Just a normal comment") is False

    def test_false_for_v1_marker(self):
        # Legacy v1 per-thread markers must NOT be recognized (no backwards compat).
        v1 = "<!-- agdt-review:v1 type:overall-summary pr:42 -->\n## old"
        assert is_consolidated_comment(v1) is False

    def test_false_when_version_matches_but_type_differs(self):
        # A hypothetical v2 marker with a different type must not match.
        content = "<!-- agdt-review:v2 type:something-else pr:42 -->"
        assert is_consolidated_comment(content) is False
