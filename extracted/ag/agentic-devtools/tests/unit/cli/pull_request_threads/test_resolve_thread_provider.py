from unittest.mock import patch

import pytest

from agentic_devtools.cli.pull_request_threads import resolve_thread_provider


@pytest.mark.parametrize(
    ("context", "expected"),
    [
        ({"code_hosting": "github"}, "github"),
        ({"platform_code_hosting": "azure_devops"}, "azure_devops"),
    ],
)
@patch("agentic_devtools.cli.pull_request_threads.get_value", return_value=None)
@patch("agentic_devtools.cli.pull_request_threads.get_repo_root", return_value=None)
def test_provider_uses_workflow_context(mock_root, mock_get_value, context, expected) -> None:
    with patch(
        "agentic_devtools.cli.pull_request_threads.get_workflow_state",
        return_value={"context": context},
    ):
        assert resolve_thread_provider() == expected


@patch("agentic_devtools.cli.pull_request_threads.get_value", return_value=None)
@patch("agentic_devtools.cli.pull_request_threads.get_workflow_state", return_value={})
@patch("agentic_devtools.cli.pull_request_threads.get_repo_root", return_value="/repo")
@patch(
    "agentic_devtools.cli.pull_request_threads.load_platform_config",
    return_value={"code_hosting": "github"},
)
def test_provider_uses_repository_configuration(mock_config, mock_root, mock_workflow, mock_get_value) -> None:
    assert resolve_thread_provider() == "github"


def test_provider_state_other_falls_back_to_repository_configuration() -> None:
    with (
        patch("agentic_devtools.cli.pull_request_threads.get_value", return_value="other"),
        patch("agentic_devtools.cli.pull_request_threads.get_repo_root", return_value="/repo"),
        patch(
            "agentic_devtools.cli.pull_request_threads.load_platform_config",
            return_value={"code_hosting": "github"},
        ),
    ):
        assert resolve_thread_provider() == "github"


@pytest.mark.parametrize("value", [None, "bitbucket"])
def test_provider_rejects_missing_or_unknown_value(value: str | None) -> None:
    with (
        patch("agentic_devtools.cli.pull_request_threads.get_value", return_value=value),
        patch("agentic_devtools.cli.pull_request_threads.get_workflow_state", return_value={}),
        patch("agentic_devtools.cli.pull_request_threads.get_repo_root", return_value=None),
    ):
        with pytest.raises(ValueError, match="platform.code_hosting"):
            resolve_thread_provider()


def test_provider_uses_legacy_azure_fallback_only_when_unconfigured() -> None:
    with (
        patch("agentic_devtools.cli.pull_request_threads.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_threads.get_workflow_state", return_value={}),
        patch("agentic_devtools.cli.pull_request_threads.get_repo_root", return_value=None),
        patch(
            "agentic_devtools.cli.pull_request_threads.get_azure_devops_context_from_git_remote",
            return_value=("https://dev.azure.com/org", "project", "repo"),
        ),
    ):
        assert resolve_thread_provider(allow_legacy_azure_fallback=True) == "azure_devops"


@pytest.mark.parametrize(
    ("workflow", "root", "platform_config"),
    [
        ({"context": {"code_hosting": "other"}}, None, {}),
        ({}, "/repo", {"code_hosting": "other"}),
    ],
)
def test_provider_does_not_fallback_for_unsupported_workflow_or_root_configuration(
    workflow, root, platform_config
) -> None:
    with (
        patch("agentic_devtools.cli.pull_request_threads.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_threads.get_workflow_state", return_value=workflow),
        patch("agentic_devtools.cli.pull_request_threads.get_repo_root", return_value=root),
        patch("agentic_devtools.cli.pull_request_threads.load_platform_config", return_value=platform_config),
        patch(
            "agentic_devtools.cli.pull_request_threads.load_repo_config",
            return_value={"platform": {"code_hosting": "other"}},
        ),
        patch("agentic_devtools.cli.pull_request_threads.get_azure_devops_context_from_git_remote") as azure_remote,
    ):
        with pytest.raises(ValueError, match="platform.code_hosting"):
            resolve_thread_provider(allow_legacy_azure_fallback=True)
    azure_remote.assert_not_called()


def test_provider_rejects_legacy_azure_fallback_without_azure_configuration() -> None:
    with (
        patch("agentic_devtools.cli.pull_request_threads.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_threads.get_workflow_state", return_value={}),
        patch("agentic_devtools.cli.pull_request_threads.get_repo_root", return_value=None),
        patch("agentic_devtools.cli.pull_request_threads.get_azure_devops_context_from_git_remote", return_value=None),
    ):
        with pytest.raises(ValueError, match="platform.code_hosting"):
            resolve_thread_provider(allow_legacy_azure_fallback=True)


def test_provider_uses_legacy_azure_fallback_for_root_azure_configuration() -> None:
    with (
        patch("agentic_devtools.cli.pull_request_threads.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_threads.get_workflow_state", return_value={}),
        patch("agentic_devtools.cli.pull_request_threads.get_repo_root", return_value="/repo"),
        patch(
            "agentic_devtools.cli.pull_request_threads.load_platform_config",
            return_value={"code_hosting": "other", "azure_devops": {}},
        ),
        patch(
            "agentic_devtools.cli.pull_request_threads.load_repo_config",
            return_value={
                "platform": {
                    "azure_devops": {
                        "organization": "https://dev.azure.com/myorg",
                        "project": "MyProject",
                    }
                }
            },
        ),
        patch("agentic_devtools.cli.pull_request_threads.get_azure_devops_context_from_git_remote", return_value=None),
    ):
        assert resolve_thread_provider(allow_legacy_azure_fallback=True) == "azure_devops"


def test_provider_does_not_fallback_for_explicit_unsupported_root_with_azure_remote() -> None:
    with (
        patch("agentic_devtools.cli.pull_request_threads.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_threads.get_workflow_state", return_value={}),
        patch("agentic_devtools.cli.pull_request_threads.get_repo_root", return_value="/repo"),
        patch(
            "agentic_devtools.cli.pull_request_threads.load_platform_config",
            return_value={"code_hosting": "other"},
        ),
        patch(
            "agentic_devtools.cli.pull_request_threads.load_repo_config",
            return_value={"platform": {"code_hosting": "other"}},
        ),
        patch(
            "agentic_devtools.cli.pull_request_threads.get_azure_devops_context_from_git_remote",
            return_value=("https://dev.azure.com/org", "project", "repo"),
        ) as azure_remote,
    ):
        with pytest.raises(ValueError, match="platform.code_hosting"):
            resolve_thread_provider(allow_legacy_azure_fallback=True)
    azure_remote.assert_not_called()


def test_provider_rejects_root_default_without_real_azure_configuration() -> None:
    with (
        patch("agentic_devtools.cli.pull_request_threads.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_threads.get_workflow_state", return_value={}),
        patch("agentic_devtools.cli.pull_request_threads.get_repo_root", return_value="/repo"),
        patch(
            "agentic_devtools.cli.pull_request_threads.load_platform_config",
            return_value={"code_hosting": "other"},
        ),
        patch(
            "agentic_devtools.cli.pull_request_threads.load_repo_config",
            return_value={"platform": {}},
        ),
        patch("agentic_devtools.cli.pull_request_threads.get_azure_devops_context_from_git_remote", return_value=None),
    ):
        with pytest.raises(ValueError, match="platform.code_hosting"):
            resolve_thread_provider(allow_legacy_azure_fallback=True)
