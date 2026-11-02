"""Tests for durable Agent Task first-observed timestamps."""

import hashlib
import json
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.models import IssueCommentInfo


def _marker(*, session_id: str, head_branch: str, expected_head_sha: str = "") -> str:
    identity = json.dumps(
        {
            "branch": head_branch,
            "expected_head_sha": expected_head_sha,
            "pr": 42,
            "repo": "owner/repo",
            "session": session_id,
            "task": "task-1",
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    digest = hashlib.sha256(identity.encode("utf-8")).hexdigest()
    return f"<!-- agdt:agent-task-first-observed:v1:{digest} -->"


def test_records_and_reads_back_first_observed_marker() -> None:
    """Persists a scoped marker and returns its provider-created timestamp."""
    provider = GitHubActionsProvider(repo="owner/repo")
    posted: dict[str, str] = {}
    with (
        patch.object(provider, "get_pr_token_login", return_value="workflow-writer"),
        patch("agentic_devtools.cli.ci.github_provider._require_default_workflow_token", return_value="token"),
        patch.object(
            provider,
            "_list_issue_comments_with_token",
            side_effect=lambda _pr, *, token: (
                [
                    IssueCommentInfo(
                        id=10,
                        author="workflow-writer",
                        body=posted["body"],
                        created_at="2026-10-16T09:00:00Z",
                    )
                ]
                if posted
                else []
            ),
        ) as list_comments,
        patch.object(
            provider,
            "post_comment_as_pr_token",
            side_effect=lambda _pr, body: posted.update(body=body) or 10,
        ) as post_comment,
    ):
        first_seen = provider.get_or_record_agent_task_first_observed_at(
            42,
            task_id="task-1",
            session_id="session-1",
            head_branch="copilot/pr-42",
        )

    assert first_seen == "2026-10-16T09:00:00Z"
    post_comment.assert_called_once()
    assert "agdt:agent-task-first-observed:v1:" in post_comment.call_args.args[1]
    assert list_comments.call_count == 2


def test_ignores_untrusted_marker_author_and_requires_readback() -> None:
    """Does not trust another author's marker or claim an unverified write."""
    provider = GitHubActionsProvider(repo="owner/repo")
    foreign = IssueCommentInfo(
        id=9,
        author="someone-else",
        body=_marker(session_id="", head_branch=""),
        created_at="2026-10-16T08:00:00Z",
    )
    with (
        patch.object(provider, "get_pr_token_login", return_value="workflow-writer"),
        patch("agentic_devtools.cli.ci.github_provider._require_default_workflow_token", return_value="token"),
        patch.object(
            provider,
            "_list_issue_comments_with_token",
            side_effect=[[foreign], [foreign]],
        ) as list_comments,
        patch.object(provider, "post_comment_as_pr_token") as post_comment,
    ):
        first_seen = provider.get_or_record_agent_task_first_observed_at(42, task_id="task-1")

    assert first_seen is None
    post_comment.assert_called_once()
    assert list_comments.call_count == 2


def test_does_not_write_marker_without_resolved_writer_identity() -> None:
    """Returns no durable timestamp when the marker author cannot be verified."""
    provider = GitHubActionsProvider(repo="owner/repo")
    with (
        patch.object(provider, "get_pr_token_login", return_value=""),
        patch.object(provider, "list_issue_comments") as list_comments,
        patch.object(provider, "_list_issue_comments_with_token") as list_with_token,
        patch.object(provider, "post_comment_as_pr_token") as post_comment,
    ):
        first_seen = provider.get_or_record_agent_task_first_observed_at(42, task_id="task-1")

    assert first_seen is None
    list_comments.assert_not_called()
    list_with_token.assert_not_called()
    post_comment.assert_not_called()


def test_head_change_requires_a_new_verified_first_observed_marker() -> None:
    """Both cached and durable clocks from another HEAD must not age the current HEAD."""
    provider = GitHubActionsProvider(repo="owner/repo")
    comments = [
        IssueCommentInfo(
            id=10,
            author="workflow-writer",
            body=_marker(session_id="session-1", head_branch="copilot/pr-42", expected_head_sha="a" * 40),
            created_at="2026-10-15T09:00:00Z",
        )
    ]

    def post(_pr: int, body: str) -> int:
        comments.append(IssueCommentInfo(id=11, author="workflow-writer", body=body, created_at="2026-10-16T09:00:00Z"))
        return 11

    with (
        patch.object(provider, "get_pr_token_login", return_value="workflow-writer"),
        patch("agentic_devtools.cli.ci.github_provider._require_default_workflow_token", return_value="token"),
        patch.object(provider, "_list_issue_comments_with_token", side_effect=lambda *a, **kw: list(comments)),
        patch.object(provider, "post_comment_as_pr_token", side_effect=post) as post_comment,
    ):
        scope = {"task_id": "task-1", "session_id": "session-1", "head_branch": "copilot/pr-42"}
        old = provider.get_agent_task_first_observed_at(42, **scope, expected_head_sha="a" * 40)
        assert old == "2026-10-15T09:00:00Z"
        assert provider.get_agent_task_first_observed_at(42, **scope, expected_head_sha="b" * 40) is None
        new = provider.get_or_record_agent_task_first_observed_at(42, **scope, expected_head_sha="b" * 40)
        assert new == "2026-10-16T09:00:00Z"
        assert provider.get_agent_task_first_observed_at(42, **scope, expected_head_sha="a" * 40) == old
        assert provider.get_agent_task_first_observed_at(42, **scope, expected_head_sha="b" * 40) == new
    post_comment.assert_called_once()
    assert comments[0].body != comments[1].body


def test_reads_existing_first_observed_marker_without_writing() -> None:
    """The read-only supervisor can consume an existing clock without adding a comment."""
    provider = GitHubActionsProvider(repo="owner/repo")
    marker = _marker(session_id="session-1", head_branch="copilot/pr-42")
    comment = IssueCommentInfo(
        id=10,
        author="workflow-writer",
        body=marker,
        created_at="2026-10-16T09:00:00Z",
    )
    with (
        patch.object(provider, "get_pr_token_login", return_value="workflow-writer"),
        patch("agentic_devtools.cli.ci.github_provider._require_default_workflow_token", return_value="token"),
        patch.object(provider, "_list_issue_comments_with_token", return_value=[comment]) as list_comments,
        patch.object(provider, "post_comment_as_pr_token") as post_comment,
    ):
        first_seen = provider.get_agent_task_first_observed_at(
            42,
            task_id="task-1",
            session_id="session-1",
            head_branch="copilot/pr-42",
        )
        cached = provider.get_agent_task_first_observed_at(
            42,
            task_id="task-1",
            session_id="session-1",
            head_branch="copilot/pr-42",
        )
        provider.invalidate_agent_task_inventory(42)
        refreshed = provider.get_agent_task_first_observed_at(
            42,
            task_id="task-1",
            session_id="session-1",
            head_branch="copilot/pr-42",
        )

    assert first_seen == "2026-10-16T09:00:00Z"
    assert cached == first_seen
    assert refreshed == first_seen
    assert list_comments.call_count == 2
    post_comment.assert_not_called()


def test_get_or_record_returns_existing_marker_without_writing() -> None:
    """An already persisted clock avoids posting a duplicate marker."""
    provider = GitHubActionsProvider(repo="owner/repo")
    with (
        patch.object(provider, "get_agent_task_first_observed_at", return_value="2026-10-16T09:00:00Z"),
        patch.object(provider, "post_comment_as_pr_token") as post_comment,
    ):
        first_seen = provider.get_or_record_agent_task_first_observed_at(
            42,
            task_id="task-1",
            session_id="session-1",
            head_branch="copilot/pr-42",
        )

    assert first_seen == "2026-10-16T09:00:00Z"
    post_comment.assert_not_called()


@pytest.mark.parametrize(("pr_number", "task_id"), [(0, "task-1"), (42, ""), (True, "task-1")])
def test_first_observed_methods_validate_scope(pr_number: int, task_id: str) -> None:
    """Both read and write methods reject invalid PR or task identifiers."""
    provider = GitHubActionsProvider(repo="owner/repo")
    with pytest.raises(ValueError):
        provider.get_or_record_agent_task_first_observed_at(pr_number, task_id=task_id)
    with pytest.raises(ValueError):
        provider.get_agent_task_first_observed_at(pr_number, task_id=task_id)


def test_read_first_observed_without_writer_identity_is_cached_as_absent() -> None:
    """A missing token identity returns no marker without requesting credentials or comments."""
    provider = GitHubActionsProvider(repo="owner/repo")
    with (
        patch.object(provider, "get_pr_token_login", return_value=""),
        patch("agentic_devtools.cli.ci.github_provider._require_default_workflow_token") as require_token,
        patch.object(provider, "_list_issue_comments_with_token") as list_comments,
    ):
        first_seen = provider.get_agent_task_first_observed_at(42, task_id="task-1")
        cached = provider.get_agent_task_first_observed_at(42, task_id="task-1")

    assert first_seen is None
    assert cached is None
    require_token.assert_not_called()
    list_comments.assert_not_called()
