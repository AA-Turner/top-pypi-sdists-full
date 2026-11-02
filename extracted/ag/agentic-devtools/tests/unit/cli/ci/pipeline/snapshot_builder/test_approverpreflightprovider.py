"""Runtime-checkable optional provider contract."""

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.pipeline.snapshot_builder import ApproverPreflightProvider


def test_github_supports_optional_protocol() -> None:
    assert isinstance(GitHubActionsProvider(repo="o/r"), ApproverPreflightProvider)
    assert not isinstance(object(), ApproverPreflightProvider)
