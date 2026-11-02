"""Tests for the provider-neutral pull-request thread reply result."""

from agentic_devtools.adapters.base import PullRequestThreadReplyResult


class TestPullRequestThreadReplyResult:
    """Validate normalized operation result serialization."""

    def test_to_dict_preserves_partial_resolution(self) -> None:
        result = PullRequestThreadReplyResult(
            provider="github",
            repository="owner/repo",
            pull_request_number=12,
            discussion_id=34,
            resolution_requested=True,
            mutation_status="partial_success",
            reply_id=56,
            resolution_status="unsupported",
            diagnostics=("review thread ID was not supplied",),
        )
        assert result.to_dict()["resolutionStatus"] == "unsupported"
        assert result.to_dict()["replyId"] == 56
