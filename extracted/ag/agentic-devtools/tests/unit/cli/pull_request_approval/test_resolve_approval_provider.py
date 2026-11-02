from __future__ import annotations

from pathlib import Path

import pytest

from agentic_devtools.cli import pull_request_approval as commands


def test_resolves_from_state_then_config(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    state = {"platform.code_hosting": "github"}
    monkeypatch.setattr(commands, "get_value", state.get)
    assert commands.resolve_approval_provider() == "github"
    state.clear()
    monkeypatch.setattr(commands, "get_repo_root", lambda: tmp_path)
    monkeypatch.setattr(commands, "load_platform_config", lambda _: {"code_hosting": "azure_devops"})
    assert commands.resolve_approval_provider() == "azure_devops"


def test_defaults_to_azure_for_legacy_repository_config(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(commands, "get_value", lambda _: None)
    monkeypatch.setattr(commands, "get_repo_root", lambda: tmp_path)
    monkeypatch.setattr(commands, "load_platform_config", lambda _: {"code_hosting": "other"})
    assert commands.resolve_approval_provider() == "azure_devops"


def test_defaults_to_azure_for_legacy_state_provider(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(commands, "get_value", lambda _: "other")
    monkeypatch.setattr(commands, "get_repo_root", lambda: None)
    assert commands.resolve_approval_provider() == "azure_devops"


def test_state_other_falls_back_to_repository_config(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(commands, "get_value", lambda _: "other")
    monkeypatch.setattr(commands, "get_repo_root", lambda: tmp_path)
    monkeypatch.setattr(commands, "load_platform_config", lambda _: {"code_hosting": "github"})
    assert commands.resolve_approval_provider() == "github"
    assert (
        commands.resolve_approval_provider(
            state={"platform": {"code_hosting": "other"}},
        )
        == "github"
    )


def test_rejects_missing_or_unknown_provider(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(commands, "get_value", lambda _: None)
    monkeypatch.setattr(commands, "get_repo_root", lambda: None)
    with pytest.raises(ValueError, match="platform.code_hosting"):
        commands.resolve_approval_provider()
    with pytest.raises(ValueError, match="platform.code_hosting"):
        commands.resolve_approval_provider("other")
