from unittest.mock import patch

from agentic_devtools.adapters.pull_request_threads import ThreadResolutionResult
from agentic_devtools.cli.pull_request_threads import _resolve_thread_task

_MINIMAL_ADO_REQUEST = {
    "provider": "azure_devops",
    "repository": "my-repo",
    "pull_request_id": 123,
    "azure_devops_thread_id": 456,
    "azure_devops_organization": "https://dev.azure.com/myorg",
    "azure_devops_project": "MyProject",
}


def test_returns_zero_on_success() -> None:
    success_result = ThreadResolutionResult(
        True,
        "azure_devops",
        "my-repo",
        123,
        status="resolved",
    )
    with patch("agentic_devtools.cli.pull_request_threads.resolve_thread", return_value=success_result):
        code = _resolve_thread_task(request=_MINIMAL_ADO_REQUEST)

    assert code == 0


def test_returns_one_on_failure() -> None:
    failure_result = ThreadResolutionResult(
        False,
        "azure_devops",
        "my-repo",
        123,
        status="failed",
        diagnostics=("credentials_required",),
    )
    with patch("agentic_devtools.cli.pull_request_threads.resolve_thread", return_value=failure_result):
        code = _resolve_thread_task(request=_MINIMAL_ADO_REQUEST)

    assert code == 1
