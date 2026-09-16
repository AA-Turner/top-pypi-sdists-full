"""Tests for GitHubActionsProvider.delete_comment() method."""

from unittest.mock import patch

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider


class TestDeleteComment:
    """Tests for GitHubActionsProvider.delete_comment()."""

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_deletes_comment(self, mock_run_safe) -> None:
        class _Result:
            returncode = 0
            stdout = ""
            stderr = ""

        mock_run_safe.return_value = _Result()

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.delete_comment(100)

        assert result is None

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_uses_delete_method(self, mock_run_safe) -> None:
        class _Result:
            returncode = 0
            stdout = ""
            stderr = ""

        mock_run_safe.return_value = _Result()

        provider = GitHubActionsProvider(repo="owner/repo")
        provider.delete_comment(100)

        args = mock_run_safe.call_args[0][0]
        assert "DELETE" in args
        assert "/issues/comments/100" in args[2]
