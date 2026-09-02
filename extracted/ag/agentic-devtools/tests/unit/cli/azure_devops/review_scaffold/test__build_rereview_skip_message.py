"""Tests for _build_rereview_skip_message."""

from agentic_devtools.cli.azure_devops.review_scaffold import _build_rereview_skip_message


class TestBuildRereviewSkipMessage:
    """The skip notice posted for a duplicate review."""

    def test_contains_marker(self):
        msg = _build_rereview_skip_message("abc1234", "claude-opus-4.6", 42)
        assert "rereview-skipped" in msg

    def test_contains_commit_and_model(self):
        msg = _build_rereview_skip_message("abc1234", "claude-opus-4.6", 42)
        assert "abc1234" in msg
        assert "claude-opus-4.6" in msg

    def test_contains_force_rereview_command(self):
        msg = _build_rereview_skip_message("abc1234", "m", 42)
        assert "--force-rereview" in msg
        assert "--pull-request-id 42" in msg

    def test_references_initiate_workflow_command(self):
        msg = _build_rereview_skip_message("abc1234", "m", 42)
        assert "agdt-initiate-pull-request-review-workflow" in msg

    def test_explains_skip(self):
        msg = _build_rereview_skip_message("abc1234", "m", 42)
        assert "skipped" in msg.lower()
