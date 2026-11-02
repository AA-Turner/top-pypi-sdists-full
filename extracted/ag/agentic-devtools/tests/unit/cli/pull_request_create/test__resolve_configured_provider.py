from unittest.mock import patch

import pytest

from agentic_devtools.cli.pull_request_create import _resolve_configured_provider


def test_resolves_from_state() -> None:
    with patch("agentic_devtools.cli.pull_request_create.get_value", return_value="github"):
        assert _resolve_configured_provider() == "github"


def test_rejects_unknown_state_value() -> None:
    with patch("agentic_devtools.cli.pull_request_create.get_value", return_value="gitlab"):
        with pytest.raises(ValueError, match="platform.code_hosting"):
            _resolve_configured_provider()


def test_rejects_unhashable_state_value() -> None:
    with patch("agentic_devtools.cli.pull_request_create.get_value", return_value=[]):
        with pytest.raises(ValueError, match="platform.code_hosting"):
            _resolve_configured_provider()


def test_returns_none_when_state_and_repository_config_unset() -> None:
    with (
        patch("agentic_devtools.cli.pull_request_create.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_create.get_repo_root", return_value=None),
        patch("agentic_devtools.cli.pull_request_create.load_platform_config", return_value={}),
    ):
        assert _resolve_configured_provider() is None


def test_resolves_from_repository_config_when_state_unset() -> None:
    with (
        patch("agentic_devtools.cli.pull_request_create.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_create.get_repo_root", return_value=None),
        patch(
            "agentic_devtools.cli.pull_request_create.load_platform_config",
            return_value={"code_hosting": "azure_devops"},
        ),
    ):
        assert _resolve_configured_provider() == "azure_devops"


def test_returns_none_when_repository_config_is_other() -> None:
    with (
        patch("agentic_devtools.cli.pull_request_create.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_create.get_repo_root", return_value=None),
        patch(
            "agentic_devtools.cli.pull_request_create.load_platform_config",
            return_value={"code_hosting": "other"},
        ),
    ):
        assert _resolve_configured_provider() is None


@pytest.mark.parametrize("raw_platform", [None, {}])
def test_returns_none_when_raw_repository_provider_is_unset(raw_platform: object) -> None:
    with (
        patch("agentic_devtools.cli.pull_request_create.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_create.get_repo_root", return_value="/repo"),
        patch(
            "agentic_devtools.cli.pull_request_create.load_repo_config",
            return_value={"platform": raw_platform},
        ),
        patch(
            "agentic_devtools.cli.pull_request_create.load_platform_config",
            return_value={"code_hosting": "other"},
        ),
    ):
        assert _resolve_configured_provider() is None


@pytest.mark.parametrize("raw_provider", ["gitub", []])
def test_rejects_invalid_raw_repository_provider_normalized_to_other(raw_provider: object) -> None:
    with (
        patch("agentic_devtools.cli.pull_request_create.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_create.get_repo_root", return_value="/repo"),
        patch(
            "agentic_devtools.cli.pull_request_create.load_repo_config",
            return_value={"platform": {"code_hosting": raw_provider}},
        ),
        patch(
            "agentic_devtools.cli.pull_request_create.load_platform_config",
            return_value={"code_hosting": "other"},
        ),
    ):
        with pytest.raises(ValueError, match="repository platform.code_hosting"):
            _resolve_configured_provider()


def test_rejects_invalid_repository_config() -> None:
    with (
        patch("agentic_devtools.cli.pull_request_create.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_create.get_repo_root", return_value=None),
        patch(
            "agentic_devtools.cli.pull_request_create.load_platform_config",
            return_value={"code_hosting": "gitlab"},
        ),
    ):
        with pytest.raises(ValueError, match="repository platform.code_hosting"):
            _resolve_configured_provider()


def test_rejects_unhashable_repository_config() -> None:
    with (
        patch("agentic_devtools.cli.pull_request_create.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_create.get_repo_root", return_value=None),
        patch(
            "agentic_devtools.cli.pull_request_create.load_platform_config",
            return_value={"code_hosting": []},
        ),
    ):
        with pytest.raises(ValueError, match="repository platform.code_hosting"):
            _resolve_configured_provider()
