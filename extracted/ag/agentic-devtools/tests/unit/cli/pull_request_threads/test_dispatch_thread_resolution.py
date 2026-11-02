from unittest.mock import MagicMock, patch

from agentic_devtools.adapters.pull_request_threads import ThreadResolutionRequest, ThreadResolutionResult
from agentic_devtools.cli.pull_request_threads import dispatch_thread_resolution


def test_fails_closed_when_azure_snapshot_omits_coordinates() -> None:
    request = ThreadResolutionRequest(
        provider="azure_devops",
        repository="repo",
        pull_request_id=7,
        azure_devops_thread_id=11,
    )

    with patch("agentic_devtools.cli.pull_request_threads.AzureDevOpsConfig.from_state") as mock_from_state:
        result = dispatch_thread_resolution(request)

    mock_from_state.assert_not_called()
    assert not result.success
    assert result.status == "failed"
    assert result.diagnostics and "snapshot must include organization and project" in result.diagnostics[0]


def test_uses_only_snapshot_coordinates_for_azure_resolution() -> None:
    request = ThreadResolutionRequest(
        provider="azure_devops",
        repository="repo",
        pull_request_id=7,
        azure_devops_thread_id=11,
        azure_devops_organization="https://dev.azure.com/org",
        azure_devops_project="project",
    )
    expected = ThreadResolutionResult(
        True,
        "azure_devops",
        "repo",
        7,
        status="resolved",
        azure_devops_thread_id=11,
    )

    with (
        patch("agentic_devtools.cli.pull_request_threads.AzureDevOpsConfig.from_state") as mock_from_state,
        patch("agentic_devtools.cli.pull_request_threads.AzureDevOpsThreadResolutionAdapter") as mock_adapter_cls,
        patch("agentic_devtools.cli.pull_request_threads.get_pat", return_value="pat"),
    ):
        mock_adapter = MagicMock()
        mock_adapter.resolve.return_value = expected
        mock_adapter_cls.return_value = mock_adapter

        result = dispatch_thread_resolution(request)

    mock_from_state.assert_not_called()
    assert result is expected
