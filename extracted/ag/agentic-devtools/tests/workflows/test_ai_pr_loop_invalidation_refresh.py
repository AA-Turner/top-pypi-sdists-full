"""End-to-end runner test for the invalidation-refresh path of the AI PR loop.

This is an *integration* test (it crosses the runner, three real pipeline actions,
the snapshot builder and the real ``GitHubActionsProvider`` thread-signals cache),
so it lives in ``tests/workflows/`` rather than under the 1:1:1 ``tests/unit/`` tree.

It reproduces the "Run A" defect end to end: ``resolve_threads`` resolves the last
open Copilot thread, ``squash`` collapses the branch and invalidates the snapshot,
the runner refreshes the snapshot, and ``request_review`` must then see **zero**
unresolved threads and request a fresh Copilot review on the squashed HEAD.

The only seam that stays real between the resolution and the refresh is the
provider's ``_thread_signals_cache``: ``finalize_post_repair`` refills it with
pre-resolution state while pre-filtering already-resolved threads, so it must be
invalidated *after* the resolve/unresolve mutations. Reverting that invalidation
makes the refreshed snapshot re-count the just-resolved thread and this test fails
with ``request_review`` skipping.
"""

from __future__ import annotations

import json
from contextlib import ExitStack
from typing import Any
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.ci.actionable_checks import DEFAULT_ACTIONABLE_CHECK_NAMES
from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.models import (
    COPILOT_REVIEWER_LOGIN,
    CheckRunStatus,
    PRMetadata,
    ReviewCommentInfo,
    ReviewInfo,
    SquashResult,
    VerificationVerdict,
)
from agentic_devtools.cli.ci.pipeline.actions import (
    RequestReviewAction,
    ResolveThreadsAction,
    SquashAction,
)
from agentic_devtools.cli.ci.pipeline.gate_verdict import CopilotGateVerdict
from agentic_devtools.cli.ci.pipeline.models import ActionDecision
from agentic_devtools.cli.ci.pipeline.runner import run_pipeline
from agentic_devtools.cli.ci.pipeline.snapshot import build_pr_state_snapshot

PR_NUMBER = 4242
REVIEW_ID = 100
COMMENT_ID = 101
REVIEW_SHA = "reviewsha0000000000000000000000000000000"
PRE_SQUASH_SHA = "presquash000000000000000000000000000000a"
POST_SQUASH_SHA = "postsquash00000000000000000000000000000b"


class _FakeGitHub:
    """Minimal GitHub state backing the provider's real GraphQL thread query."""

    def __init__(self) -> None:
        self.head_sha = PRE_SQUASH_SHA
        self.thread_resolved = False
        self.graphql_calls = 0

    def thread_signals_payload(self) -> str:
        """Render the ``reviewThreads`` GraphQL payload for the single open thread."""
        self.graphql_calls += 1
        return json.dumps(
            {
                "data": {
                    "repository": {
                        "pullRequest": {
                            "reviewThreads": {
                                "nodes": [
                                    {
                                        "id": "THREAD_1",
                                        "isResolved": self.thread_resolved,
                                        "isOutdated": False,
                                        "comments": {
                                            "nodes": [
                                                {
                                                    "databaseId": COMMENT_ID,
                                                    "body": "Please fix this",
                                                    "author": {"login": "Copilot"},
                                                }
                                            ],
                                            "pageInfo": {"hasNextPage": False},
                                        },
                                    }
                                ],
                                "pageInfo": {"hasNextPage": False},
                            }
                        }
                    }
                }
            }
        )

    def pr_metadata(self, _pr_number: int) -> PRMetadata:
        return PRMetadata(
            number=PR_NUMBER,
            title="feat(#1): a change",
            head_branch="feature",
            head_sha=self.head_sha,
            base_branch="main",
            head_repo_full_name="org/repo",
            base_repo_full_name="org/repo",
            labels=["ai-auto-merge-allowed"],
            requested_reviewers=[],
            is_draft=False,
            mergeable=True,
            mergeable_state="clean",
        )

    def squash(self, **_kwargs: Any) -> SquashResult:
        self.head_sha = POST_SQUASH_SHA
        return SquashResult(before_tree="tree1", after_tree="tree1", after_sha=POST_SQUASH_SHA)

    def resolve_review_threads(self, *_args: Any, **_kwargs: Any) -> dict[str, Any]:
        self.thread_resolved = True
        return {
            "threadsResolved": 1,
            "threadsFailed": 0,
            "verified": True,
            "details": [{"threadId": "THREAD_1", "commentId": COMMENT_ID, "status": "resolved"}],
        }


def _install_provider_seams(stack: ExitStack, github: _FakeGitHub) -> MagicMock:
    """Patch every network seam except the real thread-signals cache path.

    Returns the ``request_reviewer`` mock so the caller can assert on it.
    """

    def _patch(name: str, **kwargs: Any) -> MagicMock:
        return stack.enter_context(patch.object(GitHubActionsProvider, name, **kwargs))

    # --- Snapshot inputs -------------------------------------------------
    _patch("get_pr_metadata", side_effect=github.pr_metadata)
    _patch("get_commit_author_login", return_value="a-human")
    _patch("list_pr_files", return_value=["src/main.py"])
    _patch(
        "list_check_runs",
        return_value=[
            CheckRunStatus(id=1, name=name, status="completed", conclusion="success")
            for name in sorted(DEFAULT_ACTIONABLE_CHECK_NAMES)
        ],
    )
    _patch(
        "list_reviews",
        return_value=[
            ReviewInfo(
                id=REVIEW_ID,
                user="Copilot",
                state="CHANGES_REQUESTED",
                commit_sha=REVIEW_SHA,
                submitted_at="2026-01-01T00:00:00Z",
            )
        ],
    )
    _patch(
        "list_review_comments",
        return_value=[
            ReviewCommentInfo(id=COMMENT_ID, path="src/main.py", body="Please fix this", html_url="http://c/101")
        ],
    )
    _patch("get_approver_login", return_value="")
    _patch("count_commits_above_merge_base", return_value=2)
    _patch("count_commits_behind", return_value=0)
    _patch("list_pr_issue_events", return_value=[])
    _patch("list_issue_comments", return_value=[])

    # --- finalize_post_repair seams (the method body itself stays real) --
    _patch("_build_verification_context_diff", return_value="diff content")
    _patch("_list_addressed_reply_parent_comment_ids", return_value=set())
    _patch("_list_abandoned_reply_parent_comment_ids", return_value=set())
    _patch("_list_unresolve_reply_parent_comment_ids", return_value=set())
    _patch("_list_unconfirmed_resolved_comment_ids", return_value=set())
    _patch("_reply_to_review_comment", return_value=None)
    _patch(
        "_verify_comments_via_tiered_engine",
        return_value={COMMENT_ID: VerificationVerdict.COMMENT_RESOLVE},
    )

    # --- Side effects ----------------------------------------------------
    _patch("squash_post_repair", side_effect=github.squash)
    request_reviewer = _patch("request_reviewer", return_value=None)

    # Real GraphQL thread query, faked transport: this is what fills the cache.
    stack.enter_context(
        patch(
            "agentic_devtools.cli.ci.github_provider._gh_api",
            side_effect=lambda *_a, **_kw: github.thread_signals_payload(),
        )
    )
    stack.enter_context(
        patch(
            "agentic_devtools.cli.ci.github_provider._resolve_review_threads",
            side_effect=github.resolve_review_threads,
        )
    )

    # Gate verdict: clean, but with no specific verdict review_id (review_id=0)
    # so that the single CHANGES_REQUESTED review on the prior commit is counted
    # as a "prior" actionable review by count_unresolved_prior_threads.  Using
    # review_id=REVIEW_ID would cause the review to be excluded (it IS the
    # verdict's review), yielding 0 unresolved threads and defeating the test
    # scenario, which requires exactly one unresolved prior-commit thread.
    stack.enter_context(
        patch(
            "agentic_devtools.cli.ci.pipeline.snapshot.evaluate_copilot_gate_verdict",
            return_value=CopilotGateVerdict(passed=True, reason="clean", review_id=0),
        )
    )
    for module in (
        "agentic_devtools.cli.ci.pipeline.actions.squash",
        "agentic_devtools.cli.ci.pipeline.actions.request_review",
    ):
        stack.enter_context(patch(f"{module}.is_copilot_session_active_via_agent_task", return_value=False))

    return request_reviewer


class TestInvalidationRefreshPath:
    """resolve_threads → squash (invalidate) → refresh → request_review, in one run."""

    def test_resolve_squash_refresh_requests_review_once(self) -> None:
        """All three actions EXECUTE and a review is requested once on the squashed HEAD."""
        github = _FakeGitHub()
        provider = GitHubActionsProvider(repo="org/repo")

        with ExitStack() as stack:
            request_reviewer = _install_provider_seams(stack, github)

            snapshot = build_pr_state_snapshot(provider, PR_NUMBER)
            # Pre-conditions of the scenario: one open prior-commit thread, two commits.
            assert snapshot.unresolved_threads == 1
            assert snapshot.commit_count == 2

            summary = run_pipeline(
                provider,
                snapshot,
                # Production relative order (see run_ai_pr_loop_v2).
                [ResolveThreadsAction(), SquashAction(), RequestReviewAction()],
            )

        decisions = {result.name: result.decision for result in summary.results}
        assert decisions == {
            "resolve_threads": ActionDecision.EXECUTE,
            "squash": ActionDecision.EXECUTE,
            "request_review": ActionDecision.EXECUTE,
        }, [(r.name, r.decision, r.details) for r in summary.results]

        # The refreshed snapshot must reflect the resolution, not the pre-resolution
        # thread-signals cache that finalize_post_repair repopulated.
        assert summary.snapshot is not None
        assert summary.snapshot.head_sha == POST_SQUASH_SHA
        assert summary.snapshot.unresolved_threads == 0
        request_reviewer.assert_called_once_with(PR_NUMBER, COPILOT_REVIEWER_LOGIN)
