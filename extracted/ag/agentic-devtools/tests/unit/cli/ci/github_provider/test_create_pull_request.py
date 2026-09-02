"""Tests for GitHubActionsProvider.create_pull_request() method."""

from unittest.mock import patch

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider


def _mock_success(stdout: str = ""):
    class _Result:
        returncode = 0
        stderr = ""

        def __init__(self, out: str) -> None:
            self.stdout = out

    return _Result(stdout)


def _mock_failure(stderr: str = "some error"):
    class _Result:
        returncode = 1
        stdout = ""

        def __init__(self, err: str) -> None:
            self.stderr = err

    return _Result(stderr)


class TestCreatePullRequest:
    """Tests for GitHubActionsProvider.create_pull_request()."""

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_returns_pr_url_on_success(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_success("https://github.com/owner/repo/pull/99\n")

        provider = GitHubActionsProvider(repo="owner/repo")
        url = provider.create_pull_request(title="My PR", body="Description")

        assert url == "https://github.com/owner/repo/pull/99"

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_draft_flag_appended_when_draft_true(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_success("https://github.com/owner/repo/pull/1")

        provider = GitHubActionsProvider(repo="owner/repo")
        provider.create_pull_request(title="Draft PR", body="body", draft=True)

        cmd = mock_run_safe.call_args[0][0]
        assert "--draft" in cmd

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_draft_flag_omitted_when_draft_false(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_success("https://github.com/owner/repo/pull/2")

        provider = GitHubActionsProvider(repo="owner/repo")
        provider.create_pull_request(title="Ready PR", body="body", draft=False)

        cmd = mock_run_safe.call_args[0][0]
        assert "--draft" not in cmd

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_returns_empty_string_on_failure(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_failure("gh pr create failed")

        provider = GitHubActionsProvider(repo="owner/repo")
        url = provider.create_pull_request(title="Bad PR", body="body")

        assert url == ""

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_shell_false_is_used(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_success("https://github.com/owner/repo/pull/3")

        provider = GitHubActionsProvider(repo="owner/repo")
        provider.create_pull_request(title="T", body="B")

        kwargs = mock_run_safe.call_args[1]
        assert kwargs.get("shell") is False

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_repo_flag_passed_when_repo_is_set(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_success("https://github.com/owner/repo/pull/5")

        provider = GitHubActionsProvider(repo="owner/repo")
        provider.create_pull_request(title="T", body="B")

        cmd = mock_run_safe.call_args[0][0]
        assert "--repo" in cmd
        assert cmd[cmd.index("--repo") + 1] == "owner/repo"

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_repo_flag_omitted_when_repo_is_empty(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_success("https://github.com/owner/repo/pull/6")

        provider = GitHubActionsProvider(repo="")
        provider.create_pull_request(title="T", body="B")

        cmd = mock_run_safe.call_args[0][0]
        assert "--repo" not in cmd

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_returns_existing_url_when_pr_already_exists(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_failure(
            'a pull request for branch "x" into branch "main" already exists:\nhttps://github.com/owner/repo/pull/77'
        )

        provider = GitHubActionsProvider(repo="owner/repo")
        url = provider.create_pull_request(title="T", body="B")

        assert url == "https://github.com/owner/repo/pull/77"

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_returns_existing_url_when_message_on_stdout(self, mock_run_safe) -> None:
        """Idempotency works even when gh emits the 'already exists' message on stdout."""

        class _Result:
            returncode = 1
            stdout = 'a pull request for branch "x" into branch "main" already exists:\nhttps://github.com/owner/repo/pull/88'
            stderr = ""

        mock_run_safe.return_value = _Result()

        provider = GitHubActionsProvider(repo="owner/repo")
        url = provider.create_pull_request(title="T", body="B")

        assert url == "https://github.com/owner/repo/pull/88"

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_returns_existing_url_when_message_split_across_streams(self, mock_run_safe) -> None:
        """Idempotency works when gh splits the message across stdout and stderr."""

        class _Result:
            returncode = 1
            stdout = 'a pull request for branch "x" into branch "main" already exists:'
            stderr = "https://github.com/owner/repo/pull/99"

        mock_run_safe.return_value = _Result()

        provider = GitHubActionsProvider(repo="owner/repo")
        url = provider.create_pull_request(title="T", body="B")

        assert url == "https://github.com/owner/repo/pull/99"
