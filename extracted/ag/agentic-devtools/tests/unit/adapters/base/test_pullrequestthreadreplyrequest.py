"""Tests for PullRequestThreadReplyRequest."""

import pytest

from agentic_devtools.adapters.base import PullRequestThreadReplyRequest


class TestPullRequestThreadReplyRequest:
    """Validate immutable request values and provider-specific identifiers."""

    def test_accepts_azure_devops_request(self) -> None:
        request = PullRequestThreadReplyRequest(
            provider="azure_devops",
            repository="repo",
            pull_request_number=12,
            discussion_id=34,
            body="reply",
        )
        assert request.pull_request_id == 12
        assert request.discussion_id == 34

    def test_rejects_github_thread_id_as_reply_target(self) -> None:
        with pytest.raises(ValueError, match="numeric"):
            PullRequestThreadReplyRequest(
                provider="github",
                repository="owner/repo",
                pull_request_number=12,
                discussion_id="PRRT_kwDO",
                body="reply",
            )

    def test_rejects_empty_body(self) -> None:
        with pytest.raises(ValueError, match="body"):
            PullRequestThreadReplyRequest(
                provider="github",
                repository="owner/repo",
                pull_request_number=12,
                discussion_id=34,
                body=" \n",
            )

    @pytest.mark.parametrize(
        ("kwargs", "message"),
        [
            ({"provider": "bitbucket"}, "provider"),
            ({"repository": ""}, "repository"),
            ({"repository": "owner/"}, "owner/repo"),
            ({"repository": "/repo"}, "owner/repo"),
            ({"repository": "owner/repo/extra"}, "owner/repo"),
            ({"repository": "owner /repo"}, "owner/repo"),
            ({"repository": "owner/repo name"}, "owner/repo"),
            ({"pull_request_number": 0}, "positive"),
            ({"pull_request_number": "12"}, "positive"),
            ({"pull_request_number": None}, "positive"),
            ({"pull_request_number": True}, "positive"),
            ({"discussion_id": 0}, "positive"),
            ({"discussion_id": True}, "positive"),
            ({"review_thread_id": "123"}, "non-numeric"),
            ({"review_thread_id": ""}, "non-numeric"),
            ({"resolve": "false"}, "resolve"),
            ({"resolve": 1}, "resolve"),
            ({"dry_run": "false"}, "dry_run"),
            ({"dry_run": 0}, "dry_run"),
        ],
    )
    def test_rejects_invalid_request_values(self, kwargs: dict[str, object], message: str) -> None:
        values: dict[str, object] = {
            "provider": "github",
            "repository": "owner/repo",
            "pull_request_number": 12,
            "discussion_id": 34,
            "body": "reply",
        }
        values.update(kwargs)
        with pytest.raises(ValueError, match=message):
            PullRequestThreadReplyRequest(**values)  # type: ignore[arg-type]

    def test_serializes_request_for_task_snapshot(self) -> None:
        request = PullRequestThreadReplyRequest(
            provider="github",
            repository="owner/repo",
            pull_request_number=12,
            discussion_id=34,
            body="reply",
            resolve=True,
            review_thread_id="PRRT_kwDO",
            dry_run=True,
        )

        assert request.to_dict() == {
            "provider": "github",
            "repository": "owner/repo",
            "pull_request_number": 12,
            "discussion_id": 34,
            "body": "reply",
            "resolve": True,
            "review_thread_id": "PRRT_kwDO",
            "dry_run": True,
        }

    def test_rejects_non_numeric_azure_thread_id(self) -> None:
        with pytest.raises(ValueError, match="Azure DevOps"):
            PullRequestThreadReplyRequest(
                provider="azure_devops",
                repository="repo",
                pull_request_number=12,
                discussion_id="thread",
                body="reply",
            )

    def test_serializes_azure_context_for_worker_snapshot(self) -> None:
        request = PullRequestThreadReplyRequest(
            provider="azure_devops",
            repository="repo",
            pull_request_number=12,
            discussion_id=34,
            body="reply",
            azure_organization="org",
            azure_project="project",
        )

        assert request.to_dict()["azure_organization"] == "org"
        assert request.to_dict()["azure_project"] == "project"
