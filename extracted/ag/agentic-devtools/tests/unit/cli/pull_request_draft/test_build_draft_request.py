from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli import pull_request_draft as commands


def test_builds_github_request_from_explicit_values(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(commands, "is_dry_run", lambda: False)
    request = commands.build_draft_request(provider="github", repository="o/r", pull_request_id="8")
    assert request.pull_request_id == 8


def test_builds_github_request_from_state_and_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    values = {"platform.code_hosting": "github", "pull_request_id": None, "github.pull_request_number": 9}
    monkeypatch.setattr(commands, "get_value", values.get)
    monkeypatch.setenv("GITHUB_REPOSITORY", "o/r")
    request = commands.build_draft_request()
    assert request.repository == "o/r"


def test_builds_azure_request(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(commands, "resolve_draft_provider", lambda *_args, **_kwargs: "azure_devops")
    monkeypatch.setattr(commands, "get_value", lambda key: 9 if key == "pull_request_id" else None)
    config = MagicMock(repository="repo", organization="org", project="proj")
    monkeypatch.setattr(commands.AzureDevOpsConfig, "from_state", lambda: config)
    request = commands.build_draft_request()
    assert request.provider == "azure_devops"
    assert request.organization == "org"
    assert request.project == "proj"


def test_azure_does_not_fall_back_to_github_pull_request_number(monkeypatch: pytest.MonkeyPatch) -> None:
    """An Azure DevOps request must not silently reuse a stale GitHub PR number."""
    monkeypatch.setattr(commands, "resolve_draft_provider", lambda *_args, **_kwargs: "azure_devops")
    values = {"pull_request_id": None, "github.pull_request_number": 999}
    monkeypatch.setattr(commands, "get_value", values.get)
    config = MagicMock(repository="repo", organization="org", project="proj")
    monkeypatch.setattr(commands.AzureDevOpsConfig, "from_state", lambda: config)
    with pytest.raises(ValueError, match="pull_request_id"):
        commands.build_draft_request()


@pytest.mark.parametrize("raw_id", [None, "bad", True, []])
def test_rejects_missing_or_invalid_id(monkeypatch: pytest.MonkeyPatch, raw_id: object) -> None:
    monkeypatch.setattr(commands, "resolve_draft_provider", lambda *_args, **_kwargs: "github")
    values = {"pull_request_id": raw_id, "github.pull_request_number": None}
    monkeypatch.setattr(commands, "get_value", values.get)
    with pytest.raises(ValueError, match="pull_request_id"):
        commands.build_draft_request(repository="o/r")


def test_rejects_missing_repository(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(commands, "resolve_draft_provider", lambda *_args, **_kwargs: "github")
    monkeypatch.setattr(commands, "get_value", lambda key: 9 if key == "pull_request_id" else None)
    monkeypatch.setattr(commands, "resolve_github_repo_safe", lambda: None)
    monkeypatch.setattr(commands, "_resolve_github_repo_from_config", lambda: None)
    monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
    with pytest.raises(ValueError, match="repository"):
        commands.build_draft_request()


def test_falls_back_to_repository_config_when_no_origin_remote(monkeypatch: pytest.MonkeyPatch) -> None:
    """A checkout without an origin remote should still resolve via ``platform.github.repo``."""
    monkeypatch.setattr(commands, "resolve_draft_provider", lambda *_args, **_kwargs: "github")
    monkeypatch.setattr(commands, "get_value", lambda key: 9 if key == "pull_request_id" else None)
    monkeypatch.setattr(commands, "resolve_github_repo_safe", lambda: None)
    monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
    monkeypatch.setattr(commands, "get_repo_root", lambda: "/repo")
    monkeypatch.setattr(commands, "load_platform_config", lambda _root: {"github": {"repo": "o/r"}})
    request = commands.build_draft_request()
    assert request.repository == "o/r"


def test_rejects_non_string_explicit_repository(monkeypatch: pytest.MonkeyPatch) -> None:
    """A non-string ``repository`` argument must not be silently treated as missing."""
    monkeypatch.setattr(commands, "resolve_draft_provider", lambda *_args, **_kwargs: "github")
    monkeypatch.setattr(commands, "get_value", lambda key: 9 if key == "pull_request_id" else None)
    with pytest.raises(ValueError, match="repository must be a string"):
        commands.build_draft_request(repository=123)  # type: ignore[arg-type]


def test_rejects_non_string_github_repo_state(monkeypatch: pytest.MonkeyPatch) -> None:
    """A non-string ``github.repo`` state value must not be silently treated as missing."""
    monkeypatch.setattr(commands, "resolve_draft_provider", lambda *_args, **_kwargs: "github")
    values = {"pull_request_id": 9, "github.repo": ["o/r"]}
    monkeypatch.setattr(commands, "get_value", values.get)
    with pytest.raises(ValueError, match="github.repo must be a string"):
        commands.build_draft_request()


def test_skips_whitespace_only_repository_candidates(monkeypatch: pytest.MonkeyPatch) -> None:
    """A blank ``repository`` arg, ``github.repo`` state, or env var must not block later fallbacks."""
    monkeypatch.setattr(commands, "resolve_draft_provider", lambda *_args, **_kwargs: "github")
    values = {"pull_request_id": 9, "github.repo": "   "}
    monkeypatch.setattr(commands, "get_value", values.get)
    monkeypatch.setenv("GITHUB_REPOSITORY", "  ")
    monkeypatch.setattr(commands, "_resolve_github_repo_from_config", lambda: None)
    monkeypatch.setattr(commands, "resolve_github_repo_safe", lambda: "o/r")
    request = commands.build_draft_request(repository="  ")
    assert request.repository == "o/r"
