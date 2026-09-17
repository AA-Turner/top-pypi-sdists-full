from __future__ import annotations

import pytest

from agentic_devtools.cli import pull_request_draft as commands


def test_resolves_explicit_provider() -> None:
    assert commands.resolve_draft_provider("github", lambda _: None) == "github"


def test_resolves_state_provider(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(commands, "get_value", lambda key: "azure_devops" if key == "platform.code_hosting" else None)
    assert commands.resolve_draft_provider() == "azure_devops"


def test_rejects_unknown_provider() -> None:
    with pytest.raises(ValueError, match="platform.code_hosting"):
        commands.resolve_draft_provider("jira", lambda _: None)


def test_reads_platform_config_when_state_is_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(commands, "get_repo_root", lambda: "/repo")
    monkeypatch.setattr(commands, "load_platform_config", lambda _: {"code_hosting": "github"})
    assert commands.resolve_draft_provider(state_lookup=lambda _: None) == "github"


def test_rejects_missing_provider_when_repository_root_is_unavailable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(commands, "get_repo_root", lambda: None)
    with pytest.raises(ValueError, match="platform.code_hosting"):
        commands.resolve_draft_provider(state_lookup=lambda _: None)
