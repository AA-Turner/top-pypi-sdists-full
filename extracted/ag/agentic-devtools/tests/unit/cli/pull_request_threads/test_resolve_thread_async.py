from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.adapters.pull_request_threads import ThreadResolutionRequest
from agentic_devtools.cli.pull_request_threads import resolve_thread_async

_MINIMAL_ADO_REQUEST = ThreadResolutionRequest(
    provider="azure_devops",
    repository="my-repo",
    pull_request_id=123,
    azure_devops_thread_id=456,
    azure_devops_organization="https://dev.azure.com/myorg",
    azure_devops_project="MyProject",
)


def test_rejects_unexpected_positional_arguments() -> None:
    with (
        patch("sys.argv", ["agdt-resolve-thread", "123", "456"]),
        patch("agentic_devtools.cli.pull_request_threads.run_function_in_background") as mock_background,
    ):
        with pytest.raises(SystemExit) as exc_info:
            resolve_thread_async()

    assert exc_info.value.code == 2
    mock_background.assert_not_called()


def test_passes_immutable_snapshot_through_func_kwargs() -> None:
    mock_task = MagicMock()
    with (
        patch(
            "agentic_devtools.cli.pull_request_threads.build_thread_resolution_request",
            return_value=_MINIMAL_ADO_REQUEST,
        ),
        patch(
            "agentic_devtools.cli.pull_request_threads.run_function_in_background", return_value=mock_task
        ) as mock_bg,
        patch("agentic_devtools.cli.pull_request_threads.print_task_tracking_info"),
    ):
        resolve_thread_async(pull_request_id="123", thread_id="456", provider="azure_devops")

    _, call_kwargs = mock_bg.call_args
    assert call_kwargs["func_kwargs"] == {"request": _MINIMAL_ADO_REQUEST.as_dict()}


def test_does_not_write_shared_state() -> None:
    mock_task = MagicMock()
    with (
        patch(
            "agentic_devtools.cli.pull_request_threads.build_thread_resolution_request",
            return_value=_MINIMAL_ADO_REQUEST,
        ),
        patch("agentic_devtools.cli.pull_request_threads.run_function_in_background", return_value=mock_task),
        patch("agentic_devtools.cli.pull_request_threads.print_task_tracking_info"),
        patch("agentic_devtools.cli.pull_request_threads.read_modify_write_state") as mock_set,
    ):
        resolve_thread_async(pull_request_id="123", thread_id="456", provider="azure_devops")

    mock_set.assert_not_called()


def test_parses_cli_arguments_from_argv() -> None:
    mock_task = MagicMock()
    with (
        patch("sys.argv", ["agdt-resolve-thread", "-p", "99", "-t", "77", "--provider", "azure_devops"]),
        patch(
            "agentic_devtools.cli.pull_request_threads.build_thread_resolution_request",
            return_value=_MINIMAL_ADO_REQUEST,
        ) as mock_build,
        patch("agentic_devtools.cli.pull_request_threads.run_function_in_background", return_value=mock_task),
        patch("agentic_devtools.cli.pull_request_threads.print_task_tracking_info"),
    ):
        resolve_thread_async()

    _, call_kwargs = mock_build.call_args
    assert call_kwargs["pull_request_id"] == "99"
    assert call_kwargs["thread_id"] == "77"
    assert call_kwargs["provider"] == "azure_devops"


def test_exits_with_error_on_invalid_request(capsys) -> None:
    with (
        patch("sys.argv", ["agdt-resolve-thread"]),
        patch("agentic_devtools.cli.pull_request_threads.run_function_in_background") as mock_bg,
    ):
        with pytest.raises(SystemExit) as exc_info:
            resolve_thread_async(provider="unknown_provider")

    assert exc_info.value.code == 1
    mock_bg.assert_not_called()
    captured = capsys.readouterr()
    assert '"success": false' in captured.out.lower() or '"success":false' in captured.out.lower()
