from unittest.mock import patch

import pytest

from agentic_devtools.cli.pull_request_create import resolve_create_provider


@pytest.mark.parametrize("provider", ["azure_devops", "github"])
def test_resolve_create_provider_accepts_explicit_provider_when_unconfigured(provider: str) -> None:
    with (
        patch("agentic_devtools.cli.pull_request_create.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_create.get_repo_root", return_value=None),
        patch("agentic_devtools.cli.pull_request_create.load_platform_config", return_value={}),
    ):
        assert resolve_create_provider(provider) == provider


def test_resolve_create_provider_rejects_invalid_explicit_provider() -> None:
    with pytest.raises(ValueError, match="--provider"):
        resolve_create_provider("gitlab")


def test_resolve_create_provider_rejects_unhashable_explicit_provider() -> None:
    with pytest.raises(ValueError, match="--provider"):
        resolve_create_provider([])  # type: ignore[arg-type]


def test_resolve_create_provider_accepts_override_matching_configured_state() -> None:
    with patch("agentic_devtools.cli.pull_request_create.get_value", return_value="github"):
        assert resolve_create_provider("github") == "github"


def test_resolve_create_provider_rejects_override_conflicting_with_configured_state() -> None:
    with patch("agentic_devtools.cli.pull_request_create.get_value", return_value="github"):
        with pytest.raises(ValueError, match="conflicts with the configured"):
            resolve_create_provider("azure_devops")


def test_resolve_create_provider_rejects_override_conflicting_with_repository_config() -> None:
    with (
        patch("agentic_devtools.cli.pull_request_create.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_create.get_repo_root", return_value=None),
        patch(
            "agentic_devtools.cli.pull_request_create.load_platform_config",
            return_value={"code_hosting": "azure_devops"},
        ),
    ):
        with pytest.raises(ValueError, match="conflicts with the configured"):
            resolve_create_provider("github")


def test_resolve_create_provider_accepts_override_matching_repository_config() -> None:
    with (
        patch("agentic_devtools.cli.pull_request_create.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_create.get_repo_root", return_value=None),
        patch(
            "agentic_devtools.cli.pull_request_create.load_platform_config",
            return_value={"code_hosting": "github"},
        ),
    ):
        assert resolve_create_provider("github") == "github"


def test_resolve_create_provider_uses_state() -> None:
    with patch("agentic_devtools.cli.pull_request_create.get_value", return_value="github"):
        assert resolve_create_provider() == "github"


def test_resolve_create_provider_rejects_unknown_provider() -> None:
    with patch("agentic_devtools.cli.pull_request_create.get_value", return_value="gitlab"):
        with pytest.raises(ValueError, match="platform.code_hosting"):
            resolve_create_provider()


def test_resolve_create_provider_rejects_unhashable_state_value() -> None:
    with patch("agentic_devtools.cli.pull_request_create.get_value", return_value=[]):
        with pytest.raises(ValueError, match="platform.code_hosting"):
            resolve_create_provider()


def test_resolve_create_provider_uses_repository_config() -> None:
    with (
        patch("agentic_devtools.cli.pull_request_create.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_create.get_repo_root", return_value=None),
        patch(
            "agentic_devtools.cli.pull_request_create.load_platform_config",
            return_value={"code_hosting": "azure_devops"},
        ),
    ):
        assert resolve_create_provider() == "azure_devops"


def test_resolve_create_provider_defaults_legacy_repositories_to_azure() -> None:
    with (
        patch("agentic_devtools.cli.pull_request_create.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_create.get_repo_root", return_value=None),
        patch(
            "agentic_devtools.cli.pull_request_create.load_platform_config",
            return_value={"code_hosting": "other"},
        ),
    ):
        assert resolve_create_provider() == "azure_devops"


def test_resolve_create_provider_rejects_invalid_repository_config() -> None:
    with (
        patch("agentic_devtools.cli.pull_request_create.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_create.get_repo_root", return_value=None),
        patch(
            "agentic_devtools.cli.pull_request_create.load_platform_config",
            return_value={"code_hosting": "gitlab"},
        ),
    ):
        with pytest.raises(ValueError, match="repository platform.code_hosting"):
            resolve_create_provider()


def test_resolve_create_provider_rejects_unhashable_repository_config() -> None:
    with (
        patch("agentic_devtools.cli.pull_request_create.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_create.get_repo_root", return_value=None),
        patch(
            "agentic_devtools.cli.pull_request_create.load_platform_config",
            return_value={"code_hosting": []},
        ),
    ):
        with pytest.raises(ValueError, match="repository platform.code_hosting"):
            resolve_create_provider()
