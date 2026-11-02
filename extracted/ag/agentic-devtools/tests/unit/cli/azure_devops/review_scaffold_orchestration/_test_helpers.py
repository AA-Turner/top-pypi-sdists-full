"""Fixtures for orchestration helper tests."""

from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig
from agentic_devtools.cli.azure_devops.review_state import OverallSummary, ReviewState


def make_state():
    return ReviewState(
        prId=123,
        repoId="repo",
        repoName="repo",
        project="project",
        organization="https://dev.azure.com/org",
        latestIterationId=1,
        scaffoldedUtc="2026-01-01T00:00:00+00:00",
        overallSummary=OverallSummary(threadId=1, commentId=1),
        commitHash="commit",
    )


def make_config():
    return AzureDevOpsConfig(organization="https://dev.azure.com/org", project="project", repository="repo")
