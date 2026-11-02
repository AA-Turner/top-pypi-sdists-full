"""Tests for ``_resolve_repo_from_platform_config``."""

from unittest.mock import patch

from agentic_devtools.cli.github.repo_resolution import _resolve_repo_from_platform_config

_MOD = "agentic_devtools.cli.github.repo_resolution"


def test_returns_none_when_repo_root_is_missing() -> None:
    with patch(f"{_MOD}.get_repo_root", return_value=None):
        assert _resolve_repo_from_platform_config() is None


def test_returns_none_when_github_section_is_not_a_mapping() -> None:
    with (
        patch(f"{_MOD}.get_repo_root", return_value="/repo"),
        patch(f"{_MOD}.load_platform_config", return_value={"github": None}),
    ):
        assert _resolve_repo_from_platform_config() is None


def test_returns_none_when_config_loading_fails() -> None:
    with (
        patch(f"{_MOD}.get_repo_root", return_value="/repo"),
        patch(f"{_MOD}.load_platform_config", side_effect=RuntimeError("bad config")),
    ):
        assert _resolve_repo_from_platform_config() is None


def test_returns_none_when_repo_is_not_a_string() -> None:
    with (
        patch(f"{_MOD}.get_repo_root", return_value="/repo"),
        patch(f"{_MOD}.load_platform_config", return_value={"github": {"repo": ["bad"]}}),
    ):
        assert _resolve_repo_from_platform_config() is None


def test_returns_none_when_repo_is_invalid() -> None:
    with (
        patch(f"{_MOD}.get_repo_root", return_value="/repo"),
        patch(f"{_MOD}.load_platform_config", return_value={"github": {"repo": "invalid"}}),
    ):
        assert _resolve_repo_from_platform_config() is None


def test_returns_validated_repo() -> None:
    with (
        patch(f"{_MOD}.get_repo_root", return_value="/repo"),
        patch(f"{_MOD}.load_platform_config", return_value={"github": {"repo": " owner/repo.git "}}),
    ):
        assert _resolve_repo_from_platform_config() == "owner/repo"
