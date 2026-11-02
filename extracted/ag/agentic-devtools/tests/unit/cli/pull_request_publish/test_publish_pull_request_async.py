from unittest.mock import patch

import pytest

from agentic_devtools.cli.pull_request_publish import publish_pull_request_async


@patch("agentic_devtools.cli.pull_request_publish.is_dry_run", return_value=False)
@patch("agentic_devtools.cli.pull_request_publish._provider", return_value="azure_devops")
@patch("agentic_devtools.cli.pull_request_publish.get_value", return_value=42)
@patch("agentic_devtools.cli.pull_request_publish.run_function_in_background")
def test_starts_background_task(mock_run, mock_get_id, mock_provider, mock_dry_run) -> None:
    mock_run.return_value = "task"
    with patch("agentic_devtools.cli.pull_request_publish.print_task_tracking_info"):
        publish_pull_request_async()
    mock_run.assert_called_once()
    assert mock_run.call_args.kwargs["func_kwargs"]["dry_run"] is False
    assert mock_run.call_args.kwargs["func_kwargs"]["pull_request_id"] == 42
    assert mock_run.call_args.kwargs["func_kwargs"]["skip_auto_complete"] is False
    assert mock_get_id.call_args_list == [
        (("pull_request_id",), {"required": True}),
        (("skip_auto_complete",), {}),
    ]


@patch("agentic_devtools.cli.pull_request_publish.is_dry_run", return_value=False)
@patch("agentic_devtools.cli.pull_request_publish._provider", return_value="azure_devops")
@patch("agentic_devtools.cli.pull_request_publish.run_function_in_background")
def test_snapshots_explicit_azure_pull_request_id(mock_run, mock_provider, mock_dry_run) -> None:
    mock_run.return_value = "task"
    with patch("agentic_devtools.cli.pull_request_publish.print_task_tracking_info"):
        publish_pull_request_async(pull_request_id="123")
    assert mock_run.call_args.kwargs["func_kwargs"]["pull_request_id"] == 123
    assert mock_run.call_args.kwargs["func_kwargs"]["skip_auto_complete"] is False


@patch("agentic_devtools.cli.pull_request_publish.get_value", return_value="true")
@patch("agentic_devtools.cli.pull_request_publish.is_dry_run", return_value=False)
@patch("agentic_devtools.cli.pull_request_publish._provider", return_value="azure_devops")
@patch("agentic_devtools.cli.pull_request_publish.run_function_in_background")
def test_snapshots_skip_auto_complete_before_enqueue(mock_run, mock_provider, mock_dry_run, mock_get_value) -> None:
    mock_run.return_value = "task"
    with patch("agentic_devtools.cli.pull_request_publish.print_task_tracking_info"):
        publish_pull_request_async(pull_request_id="123")
    assert mock_run.call_args.kwargs["func_kwargs"]["skip_auto_complete"] is True
    assert mock_get_value.call_args_list == [
        (("skip_auto_complete",), {}),
    ]


@pytest.mark.parametrize("raw_id", [True, 1.5])
@patch("agentic_devtools.cli.pull_request_publish._provider", return_value="azure_devops")
@patch("agentic_devtools.cli.pull_request_publish.is_dry_run", return_value=False)
@patch("agentic_devtools.cli.pull_request_publish.get_value")
@patch("agentic_devtools.cli.pull_request_publish.run_function_in_background")
def test_rejects_coerced_state_pull_request_id_before_enqueue(
    mock_run, mock_get_value, mock_dry_run, mock_provider, raw_id
) -> None:
    mock_get_value.return_value = raw_id

    with patch("agentic_devtools.cli.pull_request_publish.print_task_tracking_info"):
        with pytest.raises(ValueError, match="pull_request_id must be a positive integer"):
            publish_pull_request_async()

    mock_run.assert_not_called()
    mock_get_value.assert_called_once_with("pull_request_id", required=True)


@patch("agentic_devtools.cli.pull_request_publish._github_request")
@patch("agentic_devtools.cli.pull_request_publish._provider", return_value="github")
@patch("agentic_devtools.cli.pull_request_publish.run_function_in_background")
def test_snapshots_github_request(mock_run, mock_provider, mock_request) -> None:
    mock_run.return_value = "task"
    mock_request.return_value = type("Request", (), {"repository": "owner/repo", "pull_request_id": 1})()
    with patch("agentic_devtools.cli.pull_request_publish.print_task_tracking_info"):
        publish_pull_request_async(dry_run=True)
    assert mock_run.call_args.kwargs["func_kwargs"]["repository"] == "owner/repo"
    assert mock_run.call_args.kwargs["func_kwargs"]["dry_run"] is True
