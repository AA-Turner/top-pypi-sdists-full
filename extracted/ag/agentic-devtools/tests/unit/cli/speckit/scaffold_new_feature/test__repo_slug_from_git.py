"""Tests for ``_repo_slug_from_git``."""

from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit import scaffold_new_feature


def test_repo_slug_from_git_normalizes_supported_remotes() -> None:
    for remote, expected in (
        ("git@github.com:owner/repo.git", "owner/repo"),
        ("https://github.com/owner/repo.git", "owner/repo"),
        ("ssh://git@github.com/owner/repo.git", "owner/repo"),
        ("git://github.com/owner/repo.git", "owner/repo"),
        ("https://token@github.com/owner/repo.git", "owner/repo"),
        # Repo name containing '.git' in the middle must not be corrupted
        ("git@github.com:owner/my.git-tools.git", "owner/my.git-tools"),
        ("https://github.com/owner/my.git-tools.git", "owner/my.git-tools"),
    ):
        with patch("subprocess.run", return_value=type("Completed", (), {"stdout": remote, "returncode": 0})()):
            assert scaffold_new_feature._repo_slug_from_git(Path(".")) == expected


def test_repo_slug_from_git_returns_gh_result_when_gh_succeeds() -> None:
    gh_result = type("Completed", (), {"stdout": "enterprise/team-repo\n", "returncode": 0})()
    with patch("subprocess.run", return_value=gh_result) as run:
        assert scaffold_new_feature._repo_slug_from_git(Path("/repo")) == "enterprise/team-repo"
    assert run.call_args_list[0].kwargs["cwd"] == Path("/repo")


def test_repo_slug_from_git_ignores_invalid_gh_result() -> None:
    gh_result = type("Completed", (), {"stdout": "not-a-slug", "returncode": 0})()
    remote_result = type("Completed", (), {"stdout": "", "returncode": 1})()
    with patch("subprocess.run", side_effect=[gh_result, remote_result]):
        assert scaffold_new_feature._repo_slug_from_git(Path("/repo")) is None


@pytest.mark.parametrize(
    "remote",
    [
        "ftp://example.com/owner/repo",
        "https://example.com/owner/repo",
        "https://token@example.com/owner/repo.git",
        "relative/repo",
    ],
)
def test_repo_slug_from_git_rejects_unsupported_remote_forms(remote: str) -> None:
    gh_result = type("Completed", (), {"stdout": "", "returncode": 1})()
    remote_result = type("Completed", (), {"stdout": remote, "returncode": 0})()
    with patch("subprocess.run", side_effect=[gh_result, remote_result]):
        assert scaffold_new_feature._repo_slug_from_git(Path("/repo")) is None
