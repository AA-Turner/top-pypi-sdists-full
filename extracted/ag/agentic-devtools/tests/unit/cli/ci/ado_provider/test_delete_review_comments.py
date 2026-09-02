"""Tests for AzureDevOpsProvider.delete_review_comments."""

from __future__ import annotations

from contextlib import contextmanager
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.ado_provider import AzureDevOpsProvider

_MARKER_COMMENT = "<!-- agdt-review:v1 type:file-summary -->\nFile summary body."


def _response(*, json_value: object = ..., status_code: int = 200, text: str = "") -> MagicMock:
    """Build a mock ``requests`` response."""
    resp = MagicMock()
    resp.raise_for_status = MagicMock()
    if json_value is not ...:
        resp.json.return_value = json_value
    resp.status_code = status_code
    resp.text = text
    return resp


def _requests_module(*, get_response: MagicMock, delete_response: MagicMock | None = None) -> MagicMock:
    """Build a mock ``requests`` module with canned get/delete responses."""
    module = MagicMock()
    module.get.return_value = get_response
    if delete_response is not None:
        module.delete.return_value = delete_response
    return module


@contextmanager
def _patched_ado(requests_module: MagicMock):
    """Patch the lazily-imported auth/helpers used by ``delete_review_comments``."""
    with (
        patch(
            "agentic_devtools.cli.azure_devops.helpers.require_requests",
            return_value=requests_module,
        ),
        patch(
            "agentic_devtools.cli.azure_devops.helpers.get_repository_id",
            return_value="repo-guid",
        ) as repo_id,
        patch("agentic_devtools.cli.azure_devops.auth.get_pat", return_value="pat"),
        patch(
            "agentic_devtools.cli.azure_devops.auth.get_auth_headers",
            return_value={"Authorization": "Basic x"},
        ),
    ):
        yield repo_id


def _provider() -> AzureDevOpsProvider:
    return AzureDevOpsProvider(
        organization="https://dev.azure.com/myorg",
        project="MyProject",
        repository="my-repo",
    )


class TestDeleteReviewComments:
    """Tests for the Azure DevOps delete_review_comments implementation."""

    def test_dry_run_selects_marker_comment_without_deleting(self) -> None:
        threads = {"value": [{"id": 7, "comments": [{"id": 3, "commentType": "text", "content": _MARKER_COMMENT}]}]}
        requests_module = _requests_module(get_response=_response(json_value=threads))

        with _patched_ado(requests_module) as repo_id:
            result = _provider().delete_review_comments(42, execute=False)

        assert result.executed is False
        assert result.selected_count == 1
        target = result.targets[0]
        assert target.thread_id == 7
        assert target.comment_id == 3
        assert target.marker_type == "file-summary"
        assert target.snippet == "File summary body."
        # No deletion in dry-run mode.
        requests_module.delete.assert_not_called()
        # Repository id resolved from the provider coordinates.
        repo_id.assert_called_once_with("https://dev.azure.com/myorg", "MyProject", "my-repo")
        # Threads listed via the PR threads endpoint.
        get_url = requests_module.get.call_args.args[0]
        assert "/_apis/git/repositories/repo-guid/pullRequests/42/threads" in get_url
        assert "api-version=7.1-preview.1" in get_url

    def test_execute_deletes_selected_comment(self) -> None:
        threads = {"value": [{"id": 7, "comments": [{"id": 3, "commentType": "text", "content": _MARKER_COMMENT}]}]}
        requests_module = _requests_module(
            get_response=_response(json_value=threads),
            delete_response=_response(status_code=204),
        )

        with _patched_ado(requests_module):
            result = _provider().delete_review_comments(42, execute=True)

        assert result.executed is True
        assert result.deleted_count == 1
        assert result.failed_count == 0
        assert result.targets[0].deleted is True
        delete_url = requests_module.delete.call_args.args[0]
        assert "/pullRequests/42/threads/7/comments/3" in delete_url

    def test_execute_reports_failure_with_detail(self) -> None:
        threads = {"value": [{"id": 1, "comments": [{"id": 2, "commentType": "text", "content": _MARKER_COMMENT}]}]}
        requests_module = _requests_module(
            get_response=_response(json_value=threads),
            delete_response=_response(status_code=500, text="boom"),
        )

        with _patched_ado(requests_module):
            result = _provider().delete_review_comments(9, execute=True)

        assert result.executed is True
        assert result.deleted_count == 0
        assert result.failed_count == 1
        assert result.targets[0].deleted is False
        assert result.targets[0].error == "HTTP 500: boom"

    def test_execute_reports_failure_without_detail(self) -> None:
        threads = {"value": [{"id": 1, "comments": [{"id": 2, "commentType": "text", "content": _MARKER_COMMENT}]}]}
        requests_module = _requests_module(
            get_response=_response(json_value=threads),
            delete_response=_response(status_code=403, text="   "),
        )

        with _patched_ado(requests_module):
            result = _provider().delete_review_comments(9, execute=True)

        assert result.targets[0].error == "HTTP 403"

    def test_execute_continues_when_delete_call_raises(self) -> None:
        threads = {
            "value": [
                {
                    "id": 1,
                    "comments": [
                        {"id": 2, "commentType": "text", "content": _MARKER_COMMENT},
                        {"id": 3, "commentType": "text", "content": _MARKER_COMMENT},
                    ],
                }
            ]
        }
        requests_module = _requests_module(get_response=_response(json_value=threads))
        requests_module.delete.side_effect = [RuntimeError("network boom"), _response(status_code=204)]

        with _patched_ado(requests_module):
            result = _provider().delete_review_comments(9, execute=True)

        assert result.executed is True
        assert result.selected_count == 2
        assert result.deleted_count == 1
        assert result.failed_count == 1
        assert result.targets[0].error == "RuntimeError: network boom"
        assert result.targets[1].deleted is True

    def test_execute_continues_when_delete_call_raises_connection_error(self) -> None:
        threads = {"value": [{"id": 1, "comments": [{"id": 2, "commentType": "text", "content": _MARKER_COMMENT}]}]}
        requests_module = _requests_module(get_response=_response(json_value=threads))
        requests_module.delete.side_effect = ConnectionError("connection dropped")

        with _patched_ado(requests_module):
            result = _provider().delete_review_comments(9, execute=True)

        assert result.executed is True
        assert result.selected_count == 1
        assert result.deleted_count == 0
        assert result.failed_count == 1
        assert result.targets[0].error == "ConnectionError: connection dropped"

    def test_no_threads_returns_empty_result(self) -> None:
        requests_module = _requests_module(get_response=_response(json_value={}))

        with _patched_ado(requests_module):
            result = _provider().delete_review_comments(5, execute=False)

        assert result.executed is False
        assert result.selected_count == 0

    def test_author_substring_fallback_selects_non_marker_comment(self) -> None:
        threads = {
            "value": [
                {
                    "id": 11,
                    "comments": [
                        {
                            "id": 4,
                            "commentType": "text",
                            "content": "Plain human comment.",
                            "author": {"displayName": "Jane Marsnik", "uniqueName": "jane@x"},
                        }
                    ],
                }
            ]
        }
        requests_module = _requests_module(get_response=_response(json_value=threads))

        with _patched_ado(requests_module):
            result = _provider().delete_review_comments(5, execute=False, author_substring="marsnik")

        assert result.selected_count == 1
        assert result.targets[0].marker_type is None
        assert result.targets[0].snippet == "Plain human comment."

    def test_missing_comment_type_is_skipped(self) -> None:
        threads = {"value": [{"id": 7, "comments": [{"id": 3, "content": _MARKER_COMMENT}]}]}
        requests_module = _requests_module(get_response=_response(json_value=threads))

        with _patched_ado(requests_module):
            result = _provider().delete_review_comments(42, execute=False)

        assert result.selected_count == 0

    def test_list_threads_http_error_raises_runtime_error(self) -> None:
        requests_module = _requests_module(
            get_response=_response(status_code=503, text="service unavailable"),
        )

        with _patched_ado(requests_module):
            with pytest.raises(RuntimeError) as excinfo:
                _provider().delete_review_comments(42, execute=False)

        message = str(excinfo.value)
        assert "Failed to list PR threads for #42" in message
        assert "HTTP 503: service unavailable" in message

    def test_urls_do_not_double_encode_project_name(self) -> None:
        provider = AzureDevOpsProvider(
            organization="https://dev.azure.com/myorg",
            project="My%20Project",
            repository="my-repo",
        )
        threads_url = provider._threads_url("repo-guid", 42)
        comment_url = provider._comment_url("repo-guid", 42, 7, 3)

        assert "/My%20Project/" in threads_url
        assert "/My%20Project/" in comment_url
        assert "My%2520Project" not in threads_url
        assert "My%2520Project" not in comment_url
        assert threads_url.endswith("api-version=7.1-preview.1")
        assert comment_url.endswith("api-version=7.1-preview.1")
