"""Unit tests for main entry point of cleanup_pr_summary_comments."""

from unittest.mock import MagicMock, patch

from scripts.cleanup_pr_summary_comments import main


def test_main_with_explicit_prs() -> None:
    with (
        patch("scripts.cleanup_pr_summary_comments.GitHubActionsProvider") as mock_cls,
        patch("scripts.cleanup_pr_summary_comments.cleanup_collapsed_summaries", return_value=5) as mock_cleanup,
    ):
        mock_provider = MagicMock()
        mock_cls.return_value = mock_provider

        exit_code = main(["4182", "4162", "--repo", "swai-factory/agentic-devtools"])

        assert exit_code == 0
        mock_cls.assert_called_once_with(repo="swai-factory/agentic-devtools")
        assert mock_cleanup.call_count == 2
        mock_cleanup.assert_any_call(mock_provider, 4182, dry_run=False)
        mock_cleanup.assert_any_call(mock_provider, 4162, dry_run=False)


def test_main_with_default_prs() -> None:
    with (
        patch("scripts.cleanup_pr_summary_comments.GitHubActionsProvider") as mock_cls,
        patch("scripts.cleanup_pr_summary_comments.cleanup_collapsed_summaries", return_value=2) as mock_cleanup,
    ):
        mock_provider = MagicMock()
        mock_cls.return_value = mock_provider

        exit_code = main([])

        assert exit_code == 0
        assert mock_cleanup.call_count == 3
        mock_cleanup.assert_any_call(mock_provider, 4182, dry_run=False)
        mock_cleanup.assert_any_call(mock_provider, 4162, dry_run=False)
        mock_cleanup.assert_any_call(mock_provider, 4137, dry_run=False)
