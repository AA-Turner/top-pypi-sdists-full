"""Offline real-provider preflight rate-limit responses."""

from types import SimpleNamespace
from typing import cast
from unittest.mock import MagicMock

from agentic_devtools.cli.ci.approver_preflight import ApproverPreflightResult, CapabilityEvidence, EvidenceStatus
from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.models import PRMetadata
from agentic_devtools.cli.ci.pipeline.actions.approval_entry import preflight_block
from agentic_devtools.cli.ci.pipeline.models import ActionResult, PipelineRunSummary
from agentic_devtools.cli.ci.pipeline.snapshot_models import PRStateSnapshot


def _preflight_rate_limit_case(endpoint: str) -> tuple[GitHubActionsProvider, PRMetadata, list[SimpleNamespace]]:
    """Arrange a denial at identity or repository lookup with real gh headers."""
    response = SimpleNamespace(
        returncode=1,
        stderr="private response offline-credential",
        stdout="HTTP/1.1 403 Forbidden\nRetry-After: 42\nX-RateLimit-Reset: 123\nX-RateLimit-Remaining: 0\n\n",
    )
    responses = (
        [response]
        if endpoint == "/user"
        else [
            SimpleNamespace(returncode=0, stderr="", stdout='{"login":"bot"}'),
            response,
        ]
    )
    metadata = PRMetadata(
        number=1,
        title="Test",
        head_branch="feature",
        base_branch="main",
        head_sha="head",
        base_repo_full_name="base/target",
    )
    return GitHubActionsProvider(repo="head/fork"), metadata, responses


def _ignored_pr_provider() -> MagicMock:
    """Arrange the existing command-level ignore-label guard regression."""
    provider = MagicMock()
    provider.get_pr_metadata.return_value = MagicMock(
        head_sha="abc",
        base_branch="main",
        head_branch="feat",
        labels=["ai-pr-loop-ignore"],
        requested_reviewers=[],
        is_draft=False,
        mergeable=True,
        title="test",
        head_repo_full_name="o/r",
        base_repo_full_name="o/r",
        number=1,
    )
    provider.list_pr_files.return_value = ["src/main.py"]
    provider.list_check_runs.return_value = []
    provider.list_reviews.return_value = []
    provider.list_pr_issue_events.return_value = []
    provider.count_commits_above_merge_base.return_value = 1
    provider.find_comment.return_value = None
    return provider


def _blocked_preflight_summary() -> PipelineRunSummary:
    """Use the real capability guard result as command-level pipeline output."""
    preflight = ApproverPreflightResult(
        identity=CapabilityEvidence(EvidenceStatus.VERIFIED, "bot", 200),
        repository_visibility=CapabilityEvidence(EvidenceStatus.UNAVAILABLE, http_status=404),
    )
    result = cast(ActionResult, preflight_block(preflight))
    return PipelineRunSummary(
        results=[result],
        snapshot=PRStateSnapshot(approver_preflight=preflight, ci_status="passing"),
    )
