"""Tests for is_valid_github_repository."""

import pytest

from agentic_devtools.adapters.base import is_valid_github_repository


@pytest.mark.parametrize(
    "repository",
    [
        "owner/repo",
        "my-org/my-repo",
        "org123/repo.name",
        "a/b",
        "Owner/Repo",
        "org/repo-with-dashes",
        "org/repo_with_underscores",
        "org/repo.with.dots",
        "org1/repo2",
        "_hidden/repo",
        "org/.github",
        "org/a..b",
    ],
)
def test_accepts_valid_repository(repository: str) -> None:
    assert is_valid_github_repository(repository) is True


@pytest.mark.parametrize(
    "repository",
    [
        "repo",
        "",
        "/repo",
        "owner/",
        "owner/repo/extra",
        "owner /repo",
        "owner/repo name",
        "owner/repo?action=delete",
        "owner/repo#anchor",
        "owner/repo&other=1",
        "owner/repo%2Fother",
        "../owner/repo",
        "owner/../repo",
        "./owner/repo",
        "owner/./repo",
        "owner/repo/../../etc/passwd",
        "owner/repo\n",
        "owner\n/repo",
    ],
)
def test_rejects_invalid_repository(repository: str) -> None:
    assert is_valid_github_repository(repository) is False
