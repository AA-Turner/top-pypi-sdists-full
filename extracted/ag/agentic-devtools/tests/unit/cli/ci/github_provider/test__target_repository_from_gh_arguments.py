"""Tests for extracting explicit repository targets from GitHub CLI arguments."""

import pytest

from agentic_devtools.cli.ci.github_provider import _target_repository_from_gh_arguments


@pytest.mark.parametrize(
    ("arguments", "expected"),
    [
        (["run", "view", "--repo", "owner/private"], "owner/private"),
        (["run", "view", "--repo=owner/private"], "owner/private"),
        (["api", "repos/owner/private/issues/1"], "owner/private"),
        (["api", "/agents/repos/owner/private/tasks"], "owner/private"),
        (
            ["api", "graphql", "-F", "query=query", "-F", "owner=owner", "-F", "repo=private"],
            "owner/private",
        ),
        (["api", "graphql", "-F", "owner=owner", "-F", "repo="], None),
        (["api", "graphql", "-F"], None),
        (["api", "graphql", "-F", "query=query", "-F", "owner=owner"], None),
        (["workflow", "list"], None),
        (["run", "view", "--repo"], None),
    ],
)
def test_extracts_repository_target(arguments: list[str], expected: str | None) -> None:
    """Explicit REST, GraphQL, and CLI repository targets are recognized."""
    assert _target_repository_from_gh_arguments(arguments) == expected
