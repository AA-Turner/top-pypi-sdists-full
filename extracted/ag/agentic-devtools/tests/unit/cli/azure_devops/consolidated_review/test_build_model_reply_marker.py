"""Tests for build_model_reply_marker and is_model_reply_comment."""

from agentic_devtools.cli.azure_devops.consolidated_review import (
    build_model_reply_marker,
    is_consolidated_comment,
    is_continuation_comment,
    is_model_reply_comment,
)


class TestBuildModelReplyMarker:
    """Tests for build_model_reply_marker."""

    def test_includes_type_pr_commit_and_model(self):
        marker = build_model_reply_marker(42, "abc123def", "gpt-5")
        assert "type:model-review" in marker
        assert "pr:42" in marker
        assert "commit:abc123def" in marker
        assert "model:gpt-5" in marker
        assert marker.startswith("<!-- agdt-review:v2 ")

    def test_omits_commit_when_none(self):
        marker = build_model_reply_marker(42, None, "gpt-5")
        assert "commit:" not in marker
        assert "model:gpt-5" in marker


class TestIsModelReplyComment:
    """Tests for is_model_reply_comment."""

    def test_true_for_model_reply_marker(self):
        marker = build_model_reply_marker(1, "abc", "claude")
        assert is_model_reply_comment(marker) is True

    def test_false_for_none_and_empty(self):
        assert is_model_reply_comment(None) is False
        assert is_model_reply_comment("") is False

    def test_does_not_match_other_marker_types(self):
        marker = build_model_reply_marker(1, "abc", "claude")
        # The model-reply marker must not be mistaken for consolidated/continuation.
        assert is_consolidated_comment(marker) is False
        assert is_continuation_comment(marker) is False
