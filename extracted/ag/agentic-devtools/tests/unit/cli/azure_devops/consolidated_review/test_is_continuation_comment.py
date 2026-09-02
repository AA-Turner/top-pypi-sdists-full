"""Tests for is_continuation_comment."""

from agentic_devtools.cli.azure_devops.consolidated_review import (
    build_continuation_marker,
    is_continuation_comment,
)


class TestIsContinuationComment:
    """Tests for the v2 continuation-marker detector."""

    def test_true_for_continuation_marker(self):
        content = "body\n" + build_continuation_marker(42, "abc", 1)
        assert is_continuation_comment(content) is True

    def test_false_for_none(self):
        assert is_continuation_comment(None) is False

    def test_false_for_empty(self):
        assert is_continuation_comment("") is False

    def test_false_for_unrelated_content(self):
        assert is_continuation_comment("just a regular comment") is False
