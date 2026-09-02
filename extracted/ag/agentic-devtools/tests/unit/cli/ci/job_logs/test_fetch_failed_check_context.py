"""Tests for fetch_failed_check_context()."""

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.job_logs import fetch_failed_check_context
from agentic_devtools.cli.ci.models import CheckRunStatus, FailedStepLog
from agentic_devtools.cli.shared.retry import ProviderRateLimitError, RetryableError

_JOB_URL = "https://github.com/owner/repo/actions/runs/9/job/77"


def _check(html_url: str = _JOB_URL) -> CheckRunStatus:
    return CheckRunStatus(id=1, name="raw-name", status="completed", conclusion="failure", html_url=html_url)


def _ok(stdout: str) -> SimpleNamespace:
    return SimpleNamespace(returncode=0, stdout=stdout)


def _fail(stderr: str = "") -> SimpleNamespace:
    return SimpleNamespace(returncode=1, stdout="", stderr=stderr)


class TestFetchFailedCheckContext:
    """Tests for composing a failing check's display name + per-step logs."""

    def test_returns_none_when_no_job_id(self) -> None:
        check = _check(html_url="https://github.com/owner/repo/security/code-scanning/5")
        with patch("agentic_devtools.cli.ci.job_logs.fetch_job_details") as mock_details:
            result = fetch_failed_check_context(check, repo="owner/repo")
        assert result is None
        mock_details.assert_not_called()

    def test_returns_none_when_repo_empty(self) -> None:
        with patch("agentic_devtools.cli.ci.job_logs.fetch_job_details") as mock_details:
            result = fetch_failed_check_context(_check(), repo="")
        assert result is None
        mock_details.assert_not_called()

    def test_full_display_name_and_per_step_logs(self) -> None:
        steps_raw = "\n".join(
            [
                "job\tStep One\terror one",
                "job\tStep Two\terror two",
            ]
        )
        with (
            patch(
                "agentic_devtools.cli.ci.job_logs.fetch_job_details",
                return_value={"workflow_name": "CI", "name": "Run Checks", "run_id": 9},
            ),
            patch("agentic_devtools.cli.ci.job_logs.fetch_run_event", return_value="pull_request") as mock_event,
            patch("agentic_devtools.cli.ci.job_logs.run_safe", return_value=_ok(steps_raw)),
            patch("agentic_devtools.cli.ci.job_logs.fetch_condensed_job_log") as mock_whole,
        ):
            result = fetch_failed_check_context(_check(), repo="owner/repo", token="tok")
        assert result is not None
        assert result.display_name == "CI / Run Checks (pull_request)"
        assert [s.step_name for s in result.step_logs] == ["Step One", "Step Two"]
        assert result.step_logs[0].condensed_log == "error one"
        mock_whole.assert_not_called()
        mock_event.assert_called_once_with(9, repo="owner/repo", token="tok")

    def test_display_name_drops_event_when_run_event_empty(self) -> None:
        with (
            patch(
                "agentic_devtools.cli.ci.job_logs.fetch_job_details",
                return_value={"workflow_name": "CI", "name": "Run Checks", "run_id": 9},
            ),
            patch("agentic_devtools.cli.ci.job_logs.fetch_run_event", return_value=""),
            patch("agentic_devtools.cli.ci.job_logs.run_safe", return_value=_fail()),
            patch("agentic_devtools.cli.ci.job_logs.fetch_condensed_job_log", return_value="whole job log"),
        ):
            result = fetch_failed_check_context(_check(), repo="owner/repo")
        assert result is not None
        assert result.display_name == "CI / Run Checks"
        assert result.step_logs == (FailedStepLog(step_name="", condensed_log="whole job log"),)

    def test_converts_rate_limit_from_gh_run_view(self) -> None:
        with (
            patch("agentic_devtools.cli.ci.job_logs.fetch_job_details", return_value=None),
            patch(
                "agentic_devtools.cli.ci.job_logs.run_safe",
                return_value=_fail("HTTP 429: rate limit exceeded"),
            ),
        ):
            with pytest.raises(ProviderRateLimitError) as exc_info:
                fetch_failed_check_context(_check(), repo="owner/repo")

        assert exc_info.value.is_rate_limit is True

    def test_issue_url_digits_do_not_trigger_rate_limit(self) -> None:
        with (
            patch("agentic_devtools.cli.ci.job_logs.fetch_job_details", return_value=None),
            patch(
                "agentic_devtools.cli.ci.job_logs.run_safe",
                return_value=_fail("lookup failed: https://github.com/owner/repo/issues/429"),
            ),
            patch("agentic_devtools.cli.ci.job_logs.fetch_condensed_job_log", return_value=""),
        ):
            result = fetch_failed_check_context(_check(), repo="owner/repo")

        assert result is not None
        assert result.step_logs == ()

    def test_preserves_provider_rate_limit_from_gh_run_view(self) -> None:
        error = ProviderRateLimitError(provider="github")
        with (
            patch("agentic_devtools.cli.ci.job_logs.fetch_job_details", return_value=None),
            patch("agentic_devtools.cli.ci.job_logs.run_safe", side_effect=error),
        ):
            with pytest.raises(ProviderRateLimitError) as exc_info:
                fetch_failed_check_context(_check(), repo="owner/repo")
        assert exc_info.value is error

    def test_display_name_job_only_when_no_workflow(self) -> None:
        with (
            patch(
                "agentic_devtools.cli.ci.job_logs.fetch_job_details",
                return_value={"workflow_name": "", "name": "Run Checks", "run_id": 9},
            ),
            patch("agentic_devtools.cli.ci.job_logs.fetch_run_event", return_value="pull_request"),
            patch("agentic_devtools.cli.ci.job_logs.run_safe", side_effect=RuntimeError("gh missing")),
            patch("agentic_devtools.cli.ci.job_logs.fetch_condensed_job_log", return_value=""),
        ):
            result = fetch_failed_check_context(_check(), repo="owner/repo")
        assert result is not None
        assert result.display_name == "Run Checks"
        assert result.step_logs == ()

    def test_non_rate_limit_retryable_log_error_falls_back_to_whole_job(self) -> None:
        error = RetryableError("temporary failure", is_rate_limit=False)
        with (
            patch("agentic_devtools.cli.ci.job_logs.fetch_job_details", return_value=None),
            patch("agentic_devtools.cli.ci.job_logs.run_safe", side_effect=error),
            patch("agentic_devtools.cli.ci.job_logs.fetch_condensed_job_log", return_value="whole job log"),
        ):
            result = fetch_failed_check_context(_check(), repo="owner/repo")
        assert result is not None
        assert result.step_logs == (FailedStepLog(step_name="", condensed_log="whole job log"),)

    def test_empty_display_name_when_no_job_details(self) -> None:
        with (
            patch("agentic_devtools.cli.ci.job_logs.fetch_job_details", return_value=None),
            patch("agentic_devtools.cli.ci.job_logs.fetch_run_event") as mock_event,
            patch("agentic_devtools.cli.ci.job_logs.run_safe", return_value=_fail()),
            patch("agentic_devtools.cli.ci.job_logs.fetch_condensed_job_log", return_value="log"),
        ):
            result = fetch_failed_check_context(_check(), repo="owner/repo")
        assert result is not None
        assert result.display_name == ""
        mock_event.assert_not_called()

    def test_run_event_cache_hit_skips_fetch(self) -> None:
        cache = {9: "schedule"}
        with (
            patch(
                "agentic_devtools.cli.ci.job_logs.fetch_job_details",
                return_value={"workflow_name": "CI", "name": "Run", "run_id": 9},
            ),
            patch("agentic_devtools.cli.ci.job_logs.fetch_run_event") as mock_event,
            patch("agentic_devtools.cli.ci.job_logs.run_safe", return_value=_fail()),
            patch("agentic_devtools.cli.ci.job_logs.fetch_condensed_job_log", return_value="log"),
        ):
            result = fetch_failed_check_context(_check(), repo="owner/repo", run_event_cache=cache)
        assert result is not None
        assert result.display_name == "CI / Run (schedule)"
        mock_event.assert_not_called()

    def test_run_event_cache_miss_stores_result(self) -> None:
        cache: dict[int, str] = {}
        with (
            patch(
                "agentic_devtools.cli.ci.job_logs.fetch_job_details",
                return_value={"workflow_name": "CI", "name": "Run", "run_id": 9},
            ),
            patch("agentic_devtools.cli.ci.job_logs.fetch_run_event", return_value="push") as mock_event,
            patch("agentic_devtools.cli.ci.job_logs.run_safe", return_value=_fail()),
            patch("agentic_devtools.cli.ci.job_logs.fetch_condensed_job_log", return_value="log"),
        ):
            result = fetch_failed_check_context(_check(), repo="owner/repo", run_event_cache=cache)
        assert result is not None
        assert result.display_name == "CI / Run (push)"
        assert cache == {9: "push"}
        mock_event.assert_called_once_with(9, repo="owner/repo", token=None)
