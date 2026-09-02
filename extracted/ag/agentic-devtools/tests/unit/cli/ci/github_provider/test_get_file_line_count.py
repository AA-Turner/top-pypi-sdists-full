"""Tests for GitHubActionsProvider.get_file_line_count()."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider


class TestGetFileLineCount:
    """Tests for the citation-resolution read used by the suppressed-triage reaper."""

    def test_counts_lines_of_an_existing_file(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        with patch(
            "agentic_devtools.cli.ci.github_provider._gh_api",
            side_effect=['{"type":"file"}', "a\nb\nc\n"],
        ) as mock_api:
            assert provider.get_file_line_count("base-sha", "src/module.py") == 3

        endpoint = mock_api.call_args_list[0].args[0]
        assert "/contents/src/module.py?ref=base-sha" in endpoint
        assert mock_api.call_args_list[0].kwargs == {}
        assert mock_api.call_args_list[1].kwargs["headers"] == {"Accept": "application/vnd.github.raw"}
        assert mock_api.call_args_list[1].kwargs["include_headers"] is False

    def test_empty_file_has_zero_lines(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        with patch(
            "agentic_devtools.cli.ci.github_provider._gh_api",
            side_effect=['{"type":"file"}', ""],
        ):
            assert provider.get_file_line_count("base-sha", "empty.txt") == 0

    def test_missing_file_is_reported_as_none(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        with patch(
            "agentic_devtools.cli.ci.github_provider._gh_api",
            side_effect=RuntimeError("gh api failed: 404 Not Found"),
        ):
            assert provider.get_file_line_count("base-sha", "gone.py") is None

    def test_missing_raw_content_after_metadata_is_reported_as_none(self) -> None:
        """A file that disappears between the metadata and raw fetches stays unresolved."""
        provider = GitHubActionsProvider(repo="o/r")
        with patch(
            "agentic_devtools.cli.ci.github_provider._gh_api",
            side_effect=['{"type":"file"}', RuntimeError("gh api failed: 404 Not Found")],
        ):
            assert provider.get_file_line_count("base-sha", "gone.py") is None

    def test_other_failures_propagate(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        with patch(
            "agentic_devtools.cli.ci.github_provider._gh_api",
            side_effect=RuntimeError("gh api failed: 500 server error"),
        ):
            with pytest.raises(RuntimeError, match="500 server error"):
                provider.get_file_line_count("base-sha", "src/module.py")

    def test_other_raw_fetch_failures_propagate(self) -> None:
        """A non-404 failure after the file check still surfaces to the caller."""
        provider = GitHubActionsProvider(repo="o/r")
        with patch(
            "agentic_devtools.cli.ci.github_provider._gh_api",
            side_effect=['{"type":"file"}', RuntimeError("gh api failed: 500 server error")],
        ):
            with pytest.raises(RuntimeError, match="500 server error"):
                provider.get_file_line_count("base-sha", "src/module.py")

    @pytest.mark.parametrize("metadata", ['{"type":"dir"}', '[{"type":"file","path":"src/module.py"}]'])
    def test_non_file_entries_are_rejected_without_fetching_raw_content(self, metadata: str) -> None:
        """Directory and other non-file entries are never counted as file content."""
        provider = GitHubActionsProvider(repo="o/r")
        with patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value=metadata) as mock_api:
            assert provider.get_file_line_count("base-sha", "src") is None
        mock_api.assert_called_once()

    @pytest.mark.parametrize(
        "path",
        ["", "/etc/passwd", "src/", "../../etc/passwd", "src/../../etc/passwd", "https://x/y"],
    )
    def test_unsafe_paths_are_rejected_without_an_api_call(self, path: str) -> None:
        """A path taken from an untrusted PR body must never reach the endpoint."""
        provider = GitHubActionsProvider(repo="o/r")
        with patch("agentic_devtools.cli.ci.github_provider._gh_api") as mock_api:
            assert provider.get_file_line_count("base-sha", path) is None
        mock_api.assert_not_called()
