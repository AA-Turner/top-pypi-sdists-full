from __future__ import annotations

import pytest

from agentic_devtools.cli import pull_request_approval as commands


def test_github_repository_falls_back_to_remote(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(commands, "get_value", lambda _: None)
    monkeypatch.setattr(commands, "resolve_github_repo_safe", lambda: "owner/repo")
    assert commands._resolve_approval_repository("github", None) == "owner/repo"


def test_azure_repository_uses_config(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(commands, "get_value", lambda _: None)
    monkeypatch.setattr(
        commands,
        "AzureDevOpsConfig",
        type("Config", (), {"from_state": type("State", (), {"repository": " repo "})}),
    )
    assert commands._resolve_approval_repository("azure_devops", None) == "repo"


def test_azure_repository_prefers_explicit_config_snapshot(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(commands, "get_value", lambda _: "stale-state-repo")
    config = type("ConfigSnapshot", (), {"repository": " snapshot-repo "})()
    assert commands._resolve_approval_repository("azure_devops", None, azure_config=config) == "snapshot-repo"


@pytest.mark.parametrize("repository", ["", 4])
def test_rejects_invalid_explicit_repository(monkeypatch: pytest.MonkeyPatch, repository: object) -> None:
    monkeypatch.setattr(commands, "get_value", lambda _: None)
    with pytest.raises(ValueError, match="repository"):
        commands._resolve_approval_repository("github", repository)  # type: ignore[arg-type]


def test_rejects_missing_repository(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(commands, "get_value", lambda _: None)
    monkeypatch.setattr(commands, "resolve_github_repo_safe", lambda: None)
    with pytest.raises(ValueError, match="repository"):
        commands._resolve_approval_repository("github", None)
