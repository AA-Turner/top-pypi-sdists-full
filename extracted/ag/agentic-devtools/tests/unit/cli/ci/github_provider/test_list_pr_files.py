"""Tests for GitHubActionsProvider.list_pr_files() method."""

import json
from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.read_token_pool import ReadCredential
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


class TestListPRFiles:
    """Tests for GitHubActionsProvider.list_pr_files()."""

    @pytest.mark.parametrize(
        "stderr",
        ["429 Too Many Requests", "HTTP 429: Too Many Requests", "403 API rate limit exceeded"],
    )
    def test_records_rate_limit_and_fails_over(self, stderr: str, monkeypatch: pytest.MonkeyPatch) -> None:
        credential = ReadCredential("POOL_CREDENTIAL", "offline-pool-token", "pool-user")
        pool = Mock()
        pool.repo = "owner/repo"
        pool.default_token = "offline-default-token"
        pool.default_identity = "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"
        pool.default_is_active = False
        pool.select.side_effect = [credential, None]
        monkeypatch.setenv("GH_TOKEN", pool.default_token)
        monkeypatch.setenv("AI_PR_LOOP_CREDENTIAL_IDENTITY", pool.default_identity)
        limited = SimpleNamespace(returncode=1, stdout="", stderr=stderr)
        success = SimpleNamespace(returncode=0, stdout='[{"filename": "src/main.py"}]', stderr="")

        with (
            patch("agentic_devtools.cli.ci.github_provider._get_read_token_pool", return_value=pool),
            patch("agentic_devtools.cli.ci.github_provider.run_safe", side_effect=[limited, success]) as runner,
        ):
            assert GitHubActionsProvider(repo="owner/repo").list_pr_files(42) == ["src/main.py"]

        pool.mark_rate_limited.assert_called_once()
        identity, error = pool.mark_rate_limited.call_args.args
        assert identity == credential.secret_name
        assert error.is_rate_limit is True
        assert error.provider == "github"
        assert error.credential_identity == credential.secret_name
        assert error.source == "fallback"
        assert [call.kwargs["env"]["GH_TOKEN"] for call in runner.call_args_list] == [
            credential.token,
            pool.default_token,
        ]

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_returns_file_paths(self, mock_run_safe) -> None:
        class _Result:
            returncode = 0
            stdout = json.dumps([{"filename": "src/main.py"}, {"filename": "tests/test_main.py"}])
            stderr = ""

        mock_run_safe.return_value = _Result()

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.list_pr_files(42)

        assert result == ["src/main.py", "tests/test_main.py"]

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_empty_files(self, mock_run_safe) -> None:
        class _Result:
            returncode = 0
            stdout = json.dumps([])
            stderr = ""

        mock_run_safe.return_value = _Result()

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.list_pr_files(1)

        assert result == []


class TestListPRFilesComplete:
    """Tests that the complete inventory API refuses unproven file lists."""

    @pytest.mark.parametrize(
        ("response", "expected_count", "expected"),
        [
            ("[]", 0, []),
            ('[{"filename":"src/a.py"}][{"filename":"src/b.py"}]', 2, ["src/a.py", "src/b.py"]),
            ("", 0, None),
            ('[{"filename":"src/a.py"}', 1, None),
            ('[{"filename":"src/a.py"}]', 2, None),
            ("[]{}", 0, None),
            ('[{"filename":""}]', 1, None),
        ],
    )
    def test_only_complete_nonempty_raw_response_matches_count(
        self, response: str, expected_count: int, expected: list[str] | None
    ) -> None:
        provider = GitHubActionsProvider(repo="owner/repo")

        with patch(
            "agentic_devtools.cli.ci.github_provider.GitHubActionsProvider._gh_api",
            return_value=response,
        ):
            assert provider.list_pr_files_complete(42, expected_count) == expected

    def test_refuses_inventory_at_api_file_limit(self) -> None:
        provider = GitHubActionsProvider(repo="owner/repo")

        with patch("agentic_devtools.cli.ci.github_provider.GitHubActionsProvider._gh_api") as gh_api:
            assert provider.list_pr_files_complete(42, 3000) is None

        gh_api.assert_not_called()

    @pytest.mark.parametrize("expected_count", [-1, True, None])
    def test_refuses_invalid_expected_file_count(self, expected_count: object) -> None:
        provider = GitHubActionsProvider(repo="owner/repo")

        with patch("agentic_devtools.cli.ci.github_provider.GitHubActionsProvider._gh_api") as gh_api:
            assert provider.list_pr_files_complete(42, expected_count) is None  # type: ignore[arg-type]

        gh_api.assert_not_called()

    def test_propagates_rate_limit_error(self) -> None:
        provider = GitHubActionsProvider(repo="owner/repo")
        error = ProviderRateLimitError(30, provider="github")

        with (
            patch("agentic_devtools.cli.ci.github_provider.GitHubActionsProvider._gh_api", side_effect=error),
            pytest.raises(ProviderRateLimitError) as exc_info,
        ):
            provider.list_pr_files_complete(42, 0)

        assert exc_info.value is error
