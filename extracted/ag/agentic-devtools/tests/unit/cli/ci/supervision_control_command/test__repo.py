"""Tests for the _repo symbol."""

from __future__ import annotations

from argparse import Namespace

import pytest

from agentic_devtools.cli.ci.supervision_control_command import _repo


def test_repo_uses_explicit_argument_over_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GITHUB_REPOSITORY", "env/repo")
    assert _repo(Namespace(repo="explicit/repo")) == "explicit/repo"


def test_repo_falls_back_to_environment_variable(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GITHUB_REPOSITORY", "env/repo")
    assert _repo(Namespace(repo=None)) == "env/repo"


def test_repo_rejects_missing_repository(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
    with pytest.raises(ValueError, match="owner/repo"):
        _repo(Namespace(repo=None))


@pytest.mark.parametrize(
    "repo",
    [
        "not-owner-slash-repo",
        "/repo",
        "owner/",
        "owner /repo",
        "owner/ repo",
        "owner/repo/extra",
        "owner//repo",
    ],
)
def test_repo_rejects_malformed_repository(monkeypatch: pytest.MonkeyPatch, repo: str) -> None:
    monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
    with pytest.raises(ValueError, match="owner/repo"):
        _repo(Namespace(repo=repo))
