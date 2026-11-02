from unittest.mock import patch

import pytest

from agentic_devtools.adapters.pull_request_publish import PullRequestPublishResult
from agentic_devtools.cli.pull_request_publish import publish_pull_request


@patch("agentic_devtools.cli.pull_request_publish._provider", return_value="azure_devops")
@patch("agentic_devtools.cli.pull_request_publish.is_dry_run", return_value=False)
@patch("agentic_devtools.cli.pull_request_publish.get_value", return_value=123)
@patch("agentic_devtools.cli.azure_devops.commands.publish_pull_request")
def test_delegates_azure(mock_azure, mock_get_id, mock_dry_run, mock_provider) -> None:
    assert publish_pull_request() is None
    mock_get_id.assert_called_once_with("pull_request_id", required=True)
    mock_azure.assert_called_once_with(dry_run=False, pull_request_id=123, skip_auto_complete=None)


@patch("agentic_devtools.cli.pull_request_publish._provider", return_value="azure_devops")
@patch("agentic_devtools.cli.pull_request_publish.is_dry_run", return_value=False)
@patch("agentic_devtools.cli.azure_devops.commands.publish_pull_request")
def test_delegates_explicit_pull_request_id_to_azure(mock_azure, mock_dry_run, mock_provider) -> None:
    assert publish_pull_request(pull_request_id="123") is None
    mock_azure.assert_called_once_with(dry_run=False, pull_request_id=123, skip_auto_complete=None)


@patch("agentic_devtools.cli.pull_request_publish._provider", return_value="azure_devops")
@patch("agentic_devtools.cli.pull_request_publish.is_dry_run", return_value=False)
@patch("agentic_devtools.cli.azure_devops.commands.publish_pull_request")
def test_passes_explicit_skip_auto_complete_to_azure(mock_azure, mock_dry_run, mock_provider) -> None:
    assert publish_pull_request(pull_request_id="123", skip_auto_complete=True) is None
    mock_azure.assert_called_once_with(dry_run=False, pull_request_id=123, skip_auto_complete=True)


@patch("agentic_devtools.cli.pull_request_publish._provider", return_value="azure_devops")
@patch("agentic_devtools.cli.pull_request_publish.is_dry_run", return_value=False)
@patch("agentic_devtools.cli.pull_request_publish.get_value", return_value=0)
@patch("agentic_devtools.cli.azure_devops.commands.publish_pull_request")
def test_rejects_non_positive_state_pull_request_id_for_azure(
    mock_azure, mock_get_id, mock_dry_run, mock_provider
) -> None:
    with pytest.raises(ValueError, match="pull_request_id must be a positive integer"):
        publish_pull_request()
    mock_azure.assert_not_called()
    mock_get_id.assert_called_once_with("pull_request_id", required=True)


@pytest.mark.parametrize("raw_id", [True, 1.5])
@patch("agentic_devtools.cli.pull_request_publish._provider", return_value="azure_devops")
@patch("agentic_devtools.cli.pull_request_publish.is_dry_run", return_value=False)
@patch("agentic_devtools.cli.pull_request_publish.get_value")
@patch("agentic_devtools.cli.azure_devops.commands.publish_pull_request")
def test_rejects_coerced_state_pull_request_id_for_azure(
    mock_azure, mock_get_value, mock_dry_run, mock_provider, raw_id
) -> None:
    mock_get_value.return_value = raw_id

    with pytest.raises(ValueError, match="pull_request_id must be a positive integer"):
        publish_pull_request()

    mock_azure.assert_not_called()
    mock_get_value.assert_called_once_with("pull_request_id", required=True)


@patch("agentic_devtools.cli.pull_request_publish.GitHubPullRequestPublishAdapter.publish")
@patch("agentic_devtools.cli.pull_request_publish._provider", return_value="github")
def test_publishes_github(mock_provider, mock_publish, capsys) -> None:
    mock_publish.return_value = PullRequestPublishResult(True, "github", "published")
    result = publish_pull_request(repository="owner/repo", pull_request_id=1)
    assert result is not None
    assert result.success
    assert "published successfully" in capsys.readouterr().out


@patch("agentic_devtools.cli.pull_request_publish.GitHubPullRequestPublishAdapter.publish")
@patch("agentic_devtools.cli.pull_request_publish._provider", return_value="github")
def test_reports_github_dry_run(mock_provider, mock_publish, capsys) -> None:
    mock_publish.return_value = PullRequestPublishResult(True, "github", "dry_run")
    result = publish_pull_request(repository="owner/repo", pull_request_id=1, dry_run=True)
    assert result is not None
    assert result.success
    captured = capsys.readouterr()
    assert "would be published" in captured.out
    assert "published successfully" not in captured.out


@patch("agentic_devtools.cli.pull_request_publish.GitHubPullRequestPublishAdapter.publish")
@patch("agentic_devtools.cli.pull_request_publish._provider", return_value="github")
def test_reports_github_failure(mock_provider, mock_publish, capsys) -> None:
    mock_publish.return_value = PullRequestPublishResult(False, "github", "failed", "denied")
    result = publish_pull_request(repository="owner/repo", pull_request_id=1)
    assert result is not None
    assert not result.success
    assert "denied" in capsys.readouterr().err
