"""Tests for provider-neutral pull-request comment command."""

from __future__ import annotations

import pytest

from agentic_devtools.cli import pull_request_comments as commands


def test_repository_resolution(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(commands, "get_value", lambda key: None)
    monkeypatch.setattr(commands, "resolve_github_repo_safe", lambda _state=None: "owner/repo")
    monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
    assert commands._resolve_repository("github", None) == "owner/repo"
    assert commands._resolve_repository("github", " owner/explicit ") == "owner/explicit"
    with pytest.raises(ValueError, match="owner/repo"):
        commands._resolve_repository("github", "invalid")
    assert commands._resolve_repository("azure_devops", None)
    monkeypatch.setattr(commands, "get_value", lambda key: "")
    monkeypatch.setattr(commands, "resolve_github_repo_safe", lambda _state=None: "")
    with pytest.raises(ValueError, match="repository"):
        commands._resolve_repository("github", None)


def test_github_resolution_ignores_generic_repository_state(monkeypatch: pytest.MonkeyPatch) -> None:
    state = {"repository": "ado/repository", "github.repo": "owner/repo"}
    monkeypatch.setattr(commands, "get_value", lambda key: state.get(key))
    monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
    assert commands._resolve_repository("github", None) == "owner/repo"


def test_non_string_repository_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(commands, "get_value", lambda key: 42 if key == "github.repo" else None)
    monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
    with pytest.raises(ValueError, match="string"):
        commands._resolve_repository("github", None)
    monkeypatch.setattr(commands, "get_value", lambda key: ["a", "b"] if key == "repository" else None)
    monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
    with pytest.raises(ValueError, match="string"):
        commands._resolve_repository("azure_devops", None)


def test_repository_fallback_uses_supplied_state_snapshot(monkeypatch: pytest.MonkeyPatch) -> None:
    github_snapshot = {"github": {"repo": "snapshot-org/snapshot-repo"}}
    monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
    monkeypatch.setattr(commands, "resolve_github_repo_safe", lambda state=None: state["github"]["repo"])

    assert commands._resolve_repository("github", None, state_lookup=lambda key: None, state=github_snapshot) == (
        "snapshot-org/snapshot-repo"
    )

    azure_snapshot = {"repository": "snapshot-repo"}
    monkeypatch.setattr(
        commands.AzureDevOpsConfig,
        "from_state",
        classmethod(
            lambda cls, state=None: type(
                "Config",
                (),
                {"organization": "org", "project": "project", "repository": state["repository"]},
            )()
        ),
    )
    assert commands._resolve_repository("azure_devops", None, state_lookup=lambda key: None, state=azure_snapshot) == (
        "snapshot-repo"
    )
