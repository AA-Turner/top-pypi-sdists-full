"""Tests for transform_replacement_code."""

from agentic_devtools.cli.azure_devops.pr_review_submit_mapper import transform_replacement_code


class TestTransformReplacementCode:
    def test_wraps_replacement_in_suggestion_fence(self):
        result = transform_replacement_code("Guard null.", "if (x == null) return;")
        assert result == "Guard null.\n\n```suggestion\nif (x == null) return;\n```"

    def test_none_replacement_returns_content_unchanged(self):
        assert transform_replacement_code("Just a comment.", None) == "Just a comment."

    def test_empty_replacement_returns_content_unchanged(self):
        assert transform_replacement_code("Comment", "") == "Comment"

    def test_whitespace_only_replacement_returns_content_unchanged(self):
        assert transform_replacement_code("Comment", "   \n  ") == "Comment"
