"""Tests for GitHubActionsProvider commit-range diff retrieval."""

import os
import subprocess
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.retry import ProviderRateLimitError, RetryableError


def _mock_run_safe_result(*, returncode: int, stdout: str | bytes = "", stderr: str | bytes = ""):
    return SimpleNamespace(returncode=returncode, stdout=stdout, stderr=stderr)


class TestGetCommitRangeDiff:
    """Tests for commit-range diff retrieval."""

    @patch.dict("os.environ", {"GH_TOKEN": "ambient-token"}, clear=True)
    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_uses_configured_token_when_ambient_token_differs(self, mock_run_safe):
        mock_run_safe.return_value = _mock_run_safe_result(returncode=0, stdout=b"diff --git a/x b/x")
        provider = GitHubActionsProvider(repo="owner/repo", token="configured-token")

        result = provider.get_commit_range_diff("abc", "def")

        assert result == "diff --git a/x b/x"
        mock_run_safe.assert_called_once_with(
            [
                "gh",
                "api",
                "/repos/owner/repo/compare/abc...def",
                "--method",
                "GET",
                "--include",
                "-H",
                "Accept: application/vnd.github.v3.diff",
            ],
            capture_output=True,
            text=False,
            shell=False,
            env={**os.environ, "GH_TOKEN": "configured-token"},
            timeout=60,
        )

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_preserves_carriage_returns_from_diff_bytes(self, mock_run_safe):
        mock_run_safe.return_value = _mock_run_safe_result(
            returncode=0,
            stdout=b"diff --git a/x b/x\n@@ -1 +1 @@\n-old\n+new\rsuffix\n",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.get_commit_range_diff("abc", "def")

        assert "+new\rsuffix\n" in result

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_replaces_invalid_utf8_for_existing_text_consumers(self, mock_run_safe):
        mock_run_safe.return_value = _mock_run_safe_result(returncode=0, stdout=b"diff \xff\n")
        provider = GitHubActionsProvider(repo="owner/repo")

        assert provider.get_commit_range_diff("abc", "def") == "diff \ufffd\n"

    @pytest.mark.parametrize("stderr", [b"HTTP 503 service unavailable", b"503 service unavailable"])
    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_raises_retryable_error_on_transient_failure(self, mock_run_safe, _mock_sleep, stderr):
        mock_run_safe.return_value = _mock_run_safe_result(
            returncode=1,
            stderr=stderr,
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(RetryableError) as exc_info:
            provider.get_commit_range_diff("abc", "def")
        assert exc_info.value.is_rate_limit is False

    @pytest.mark.parametrize(
        ("method_name", "stderr"),
        [
            ("get_commit_range_diff", b"HTTP 429 rate limit exceeded"),
            ("get_commit_range_diff_change_counts", "HTTP 429 rate limit exceeded"),
        ],
    )
    @patch.dict(
        "os.environ",
        {"GH_TOKEN": "ambient-token", "REPO_VARIABLE_WRITER_PAT": "configured-token"},
        clear=True,
    )
    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_propagates_configured_token_identity_after_rate_limit_retries(
        self, mock_gh_api, mock_run_safe, _mock_sleep, method_name, stderr
    ):
        mock_run_safe.return_value = _mock_run_safe_result(returncode=1, stderr=stderr)
        mock_gh_api.side_effect = ProviderRateLimitError(
            provider="github", credential_identity="REPO_VARIABLE_WRITER_PAT"
        )
        provider = GitHubActionsProvider(repo="owner/repo", token="configured-token")

        with pytest.raises(ProviderRateLimitError) as exc_info:
            getattr(provider, method_name)("abc", "def")

        assert exc_info.value.provider == "github"
        assert exc_info.value.credential_identity == "REPO_VARIABLE_WRITER_PAT"

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_raises_runtime_error_on_non_transient_failure(self, mock_run_safe):
        mock_run_safe.return_value = _mock_run_safe_result(returncode=1, stderr=b"boom")
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(RuntimeError, match="gh api compare diff failed: boom"):
            provider.get_commit_range_diff("abc", "def")

    @patch.dict(
        "os.environ",
        {"AGDT_GITHUB_SECRETS_JSON": '{"DEFAULT_CLASSIC_REPO_WORKFLOW_PAT":"default-secret"}'},
        clear=True,
    )
    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    @patch("agentic_devtools.cli.ci.github_provider._call_with_read_token_pool")
    @patch("agentic_devtools.cli.ci.github_provider._should_use_read_token_pool", return_value=True)
    def test_uses_pooled_token_without_exposing_secret_json_to_subprocess(
        self, _mock_should_pool, mock_call_with_pool, mock_run_safe
    ):
        mock_run_safe.return_value = _mock_run_safe_result(returncode=0, stdout=b"diff bytes")
        mock_call_with_pool.side_effect = lambda _resource, operation: operation(
            "read-token", "READ_ONLY_REPO_WORKFLOW_PAT"
        )[0]
        provider = GitHubActionsProvider(repo="owner/repo")

        assert provider.get_commit_range_diff_bytes("abc", "def") == b"diff bytes"

        assert mock_run_safe.call_args.kwargs["env"] == {"GH_TOKEN": "read-token"}
        mock_call_with_pool.assert_called_once()

    @patch.dict("os.environ", {"AGDT_GITHUB_SECRETS_JSON": "{}"}, clear=True)
    @patch("agentic_devtools.cli.ci.github_provider.run_safe", side_effect=subprocess.TimeoutExpired("gh api", 60))
    @patch("agentic_devtools.cli.ci.github_provider._should_use_read_token_pool", return_value=False)
    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    def test_retries_timed_out_compare_diff_request(self, _mock_sleep, _mock_should_pool, _mock_run_safe):
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(RetryableError, match="timed out"):
            provider.get_commit_range_diff_bytes("abc", "def")


class TestGetCommitRangeDiffChangeCounts:
    """Tests for provider-reported changed-line totals."""

    @patch.dict("os.environ", {"GH_TOKEN": "ambient-token"}, clear=True)
    @patch(
        "agentic_devtools.cli.ci.github_provider._gh_api",
        return_value='{"files":[{"filename":"src/a.py","changes":4},{"filename":"new.py","changes":0}]}',
    )
    def test_returns_change_counts_by_filename(self, mock_gh_api):
        provider = GitHubActionsProvider(repo="owner/repo", token="configured-token")

        assert provider.get_commit_range_diff_change_counts("abc", "def") == {
            "src/a.py": 4,
            "new.py": 0,
        }
        mock_gh_api.assert_called_once_with(
            "/repos/owner/repo/compare/abc...def",
            token="configured-token",
            credential_identity="explicit-token",
        )

    @pytest.mark.parametrize(
        "stdout",
        [
            "not json",
            "[]",
            "{}",
            '{"files":[null]}',
            '{"files":[{"filename":1,"changes":1}]}',
            '{"files":[{"filename":"file.py","changes":true}]}',
            '{"files":[{"filename":"","changes":1}]}',
            '{"files":[{"filename":"file.py","changes":-1}]}',
            '{"files":[{"filename":"file.py","changes":1},{"filename":"file.py","changes":1}]}',
        ],
    )
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_rejects_invalid_change_count_responses(self, mock_gh_api, stdout):
        mock_gh_api.return_value = stdout
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(RuntimeError, match="compare change counts"):
            provider.get_commit_range_diff_change_counts("abc", "def")

    @pytest.mark.parametrize(
        ("error", "error_type", "message"),
        [
            (RetryableError("rate limited"), RetryableError, "rate limited"),
            (RuntimeError("boom"), RuntimeError, "compare change counts failed"),
        ],
    )
    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_surfaces_compare_metadata_failures(self, mock_gh_api, _mock_sleep, error, error_type, message):
        mock_gh_api.side_effect = error
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(error_type, match=message):
            provider.get_commit_range_diff_change_counts("abc", "def")
