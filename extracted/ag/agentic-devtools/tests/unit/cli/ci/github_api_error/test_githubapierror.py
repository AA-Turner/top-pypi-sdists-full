"""Permanent API failures retain only safe status data."""

from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci import github_provider
from agentic_devtools.cli.ci.github_api_error import GitHubApiError
from agentic_devtools.cli.ci.github_provider import _gh_api


class TestGitHubApiError:
    @pytest.mark.parametrize("status", [401, 403, 404, 422, None])
    def test_runtime_error_compatibility_and_safe_status(self, status: int | None) -> None:
        error = GitHubApiError(status)
        assert isinstance(error, RuntimeError)
        assert error.http_status == status
        assert (
            str(error) == f"GitHub API error: {'HTTP ' + str(status) if status is not None else 'status unavailable'}"
        )

    def test_safe_diagnostic_message_retains_status(self) -> None:
        error = GitHubApiError(404, safe_message="Agent Tasks failure diagnostics: http_status=404")
        assert error.http_status == 404
        assert str(error) == "Agent Tasks failure diagnostics: http_status=404"

    def test_permanent_provider_response_is_typed_and_not_retried(self, monkeypatch: pytest.MonkeyPatch) -> None:
        result = SimpleNamespace(returncode=1, stdout="HTTP/1.1 403 Forbidden\n\n", stderr="permission denied")
        runner = Mock(return_value=result)
        monkeypatch.setattr(github_provider, "run_safe", runner)

        with pytest.raises(GitHubApiError) as caught:
            _gh_api("/repos/o/r", read_pool=False)

        assert caught.value.http_status == 403
        runner.assert_called_once()
