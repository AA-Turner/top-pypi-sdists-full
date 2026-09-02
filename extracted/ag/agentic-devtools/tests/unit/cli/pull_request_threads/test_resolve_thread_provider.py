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


@pytest.mark.parametrize("value", [None, "bitbucket"])
def test_provider_rejects_missing_or_unknown_value(value: str | None) -> None:
    with (
        patch("agentic_devtools.cli.pull_request_threads.get_value", return_value=value),
        patch("agentic_devtools.cli.pull_request_threads.get_workflow_state", return_value={}),
        patch("agentic_devtools.cli.pull_request_threads.get_repo_root", return_value=None),
    ):
        with pytest.raises(ValueError, match="platform.code_hosting"):
            resolve_thread_provider()
