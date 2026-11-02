from unittest.mock import patch

from agentic_devtools.adapters.pull_request_threads import ThreadResolutionRequest, ThreadResolutionResult
from agentic_devtools.cli.pull_request_threads import resolve_thread


def test_rejects_malformed_request_snapshot_without_falling_back_to_state_builder() -> None:
    with (
        patch("agentic_devtools.cli.pull_request_threads.build_thread_resolution_request") as mock_builder,
        patch("agentic_devtools.cli.pull_request_threads.dispatch_thread_resolution") as mock_dispatch,
        patch("agentic_devtools.cli.pull_request_threads.read_modify_write_state"),
    ):
        result = resolve_thread(request="invalid")

    mock_builder.assert_not_called()
    mock_dispatch.assert_not_called()
    assert result.success is False
    assert result.status == "invalid"
    assert result.diagnostics == ("request snapshot must be a dictionary",)


def test_dispatches_valid_request_snapshot() -> None:
    request = ThreadResolutionRequest(
        provider="github",
        repository="owner/repo",
        pull_request_id=1,
        github_thread_node_id="PRRT_node",
    )
    expected = ThreadResolutionResult(True, "github", "owner/repo", 1, status="resolved")
    with (
        patch("agentic_devtools.cli.pull_request_threads.dispatch_thread_resolution", return_value=expected),
        patch("agentic_devtools.cli.pull_request_threads.read_modify_write_state"),
    ):
        result = resolve_thread(request=request.as_dict())

    assert result is expected


def test_builds_and_dispatches_state_request() -> None:
    expected = ThreadResolutionResult(True, "github", "owner/repo", 1, status="resolved")
    with (
        patch("agentic_devtools.cli.pull_request_threads.build_thread_resolution_request") as mock_builder,
        patch("agentic_devtools.cli.pull_request_threads.dispatch_thread_resolution", return_value=expected),
        patch("agentic_devtools.cli.pull_request_threads.read_modify_write_state"),
    ):
        result = resolve_thread(provider="github")

    mock_builder.assert_called_once_with(provider="github")
    assert result is expected
