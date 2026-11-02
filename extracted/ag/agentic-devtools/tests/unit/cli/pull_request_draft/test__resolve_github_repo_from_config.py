from __future__ import annotations

import pytest

from agentic_devtools.cli import pull_request_draft as commands


def test_returns_none_when_repo_root_is_unresolved(monkeypatch) -> None:
    monkeypatch.setattr(commands, "get_repo_root", lambda: None)

    assert commands._resolve_github_repo_from_config() is None


def test_returns_none_when_github_section_is_missing_or_invalid(monkeypatch) -> None:
    monkeypatch.setattr(commands, "get_repo_root", lambda: "/repo")
    monkeypatch.setattr(commands, "load_platform_config", lambda _root: {"github": None})

    assert commands._resolve_github_repo_from_config() is None


def test_returns_none_when_repo_value_is_blank(monkeypatch) -> None:
    monkeypatch.setattr(commands, "get_repo_root", lambda: "/repo")
    monkeypatch.setattr(commands, "load_platform_config", lambda _root: {"github": {"repo": "  "}})

    assert commands._resolve_github_repo_from_config() is None


def test_returns_configured_repo(monkeypatch) -> None:
    monkeypatch.setattr(commands, "get_repo_root", lambda: "/repo")
    monkeypatch.setattr(commands, "load_platform_config", lambda _root: {"github": {"repo": "o/r"}})

    assert commands._resolve_github_repo_from_config() == "o/r"


def test_raises_when_repo_value_is_not_a_string(monkeypatch) -> None:
    monkeypatch.setattr(commands, "get_repo_root", lambda: "/repo")
    monkeypatch.setattr(commands, "load_platform_config", lambda _root: {"github": {"repo": ["o/r"]}})

    with pytest.raises(ValueError, match="platform.github.repo must be a string"):
        commands._resolve_github_repo_from_config()
