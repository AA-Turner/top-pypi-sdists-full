from __future__ import annotations

from agentic_devtools.adapters.pull_request_approval import PullRequestApprovalRequest
from agentic_devtools.cli import pull_request_approval as commands


def test_selects_github_adapter() -> None:
    assert isinstance(
        commands._adapter_for(PullRequestApprovalRequest("github", "owner/repo", 1, "x", "a" * 40)),
        commands.GitHubPullRequestApprovalAdapter,
    )


def test_selects_azure_adapter() -> None:
    assert isinstance(
        commands._adapter_for(PullRequestApprovalRequest("azure_devops", "repo", 1, "x")),
        commands.AzureDevOpsPullRequestApprovalAdapter,
    )
