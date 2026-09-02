"""Tests for provider-neutral pull-request comment command."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentic_devtools.cli import pull_request_comments as commands


def test_provider_resolution_uses_state_then_config(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    state = {"platform.code_hosting": "github"}
    monkeypatch.setattr(commands, "get_value", lambda key: state.get(key))
    assert commands.resolve_comment_provider() == "github"

    state.clear()
    monkeypatch.setattr(commands, "get_repo_root", lambda: tmp_path)
    monkeypatch.setattr(commands, "load_platform_config", lambda root: {"code_hosting": "azure_devops"})
    assert commands.resolve_comment_provider() == "azure_devops"

    monkeypatch.setattr(commands, "get_repo_root", lambda: None)
    with pytest.raises(ValueError, match="platform.code_hosting"):
        commands.resolve_comment_provider()


def test_rejects_unknown_provider() -> None:
    with pytest.raises(ValueError, match="platform.code_hosting"):
        commands.resolve_comment_provider("other")
