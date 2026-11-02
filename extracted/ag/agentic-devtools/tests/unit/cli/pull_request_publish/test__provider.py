from unittest.mock import patch

import pytest

from agentic_devtools.cli.pull_request_publish import _provider


@patch("agentic_devtools.cli.pull_request_publish.get_value", return_value="github")
def test_reads_provider_from_state(mock_get) -> None:
    assert _provider() == "github"
    mock_get.assert_called_once_with("platform.code_hosting")


@patch("agentic_devtools.cli.pull_request_publish.get_value", return_value="unknown")
def test_rejects_unknown_provider(mock_get) -> None:
    with pytest.raises(ValueError, match="platform.code_hosting"):
        _provider()


@patch("agentic_devtools.cli.pull_request_publish.get_value")
def test_rejects_explicit_empty_provider(mock_get) -> None:
    with pytest.raises(ValueError, match="provider"):
        _provider("")
    mock_get.assert_not_called()


@patch("agentic_devtools.cli.pull_request_publish.get_value", return_value=None)
@patch("agentic_devtools.cli.pull_request_publish.get_repo_root", return_value=None)
def test_defaults_to_azure_when_provider_is_unconfigured(mock_root, mock_get) -> None:
    assert _provider() == "azure_devops"


@patch(
    "agentic_devtools.cli.pull_request_publish.load_repo_config",
    return_value={"platform": {"code_hosting": "github"}},
)
@patch("agentic_devtools.cli.pull_request_publish.load_platform_config", return_value={"code_hosting": "github"})
@patch("agentic_devtools.cli.pull_request_publish.get_value", return_value=None)
@patch("agentic_devtools.cli.pull_request_publish.get_repo_root", return_value="/repo")
def test_reads_provider_from_platform_config(mock_root, mock_get, mock_config, mock_repo_config) -> None:
    assert _provider() == "github"


@patch(
    "agentic_devtools.cli.pull_request_publish.load_repo_config",
    return_value={"platform": {"code_hosting": "github"}},
)
@patch("agentic_devtools.cli.pull_request_publish.load_platform_config", return_value={"code_hosting": "github"})
@patch("agentic_devtools.cli.pull_request_publish.get_value", return_value="other")
@patch("agentic_devtools.cli.pull_request_publish.get_repo_root", return_value="/repo")
def test_state_other_falls_back_to_platform_config(mock_root, mock_get, mock_config, mock_repo_config) -> None:
    assert _provider() == "github"


@patch(
    "agentic_devtools.cli.pull_request_publish.load_repo_config",
    return_value={"platform": {"issue_adapter": "jira"}},
)
@patch("agentic_devtools.cli.pull_request_publish.get_value", return_value=None)
@patch("agentic_devtools.cli.pull_request_publish.get_repo_root", return_value="/repo")
def test_defaults_to_azure_when_platform_has_no_code_hosting(mock_root, mock_get, mock_repo_config) -> None:
    assert _provider() == "azure_devops"


@patch(
    "agentic_devtools.cli.pull_request_publish.load_repo_config",
    return_value={"platform": {"code_hosting": "other"}},
)
@patch("agentic_devtools.cli.pull_request_publish.load_platform_config", return_value={"code_hosting": "other"})
@patch("agentic_devtools.cli.pull_request_publish.get_value", return_value=None)
@patch("agentic_devtools.cli.pull_request_publish.get_repo_root", return_value="/repo")
def test_rejects_explicit_other_provider(mock_root, mock_get, mock_config, mock_repo_config) -> None:
    with pytest.raises(ValueError, match="platform.code_hosting"):
        _provider()


@patch("agentic_devtools.cli.pull_request_publish.get_value", return_value=["github"])
def test_rejects_non_string_provider_from_state(mock_get) -> None:
    with pytest.raises(ValueError, match="platform.code_hosting"):
        _provider()
