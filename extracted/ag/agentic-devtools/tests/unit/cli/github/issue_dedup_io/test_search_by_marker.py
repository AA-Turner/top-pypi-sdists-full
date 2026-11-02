"""Tests for search_by_marker."""

from __future__ import annotations

import json
from unittest.mock import patch

import pytest

from agentic_devtools.cli.shared.retry import ProviderRateLimitError, RetryableError

_MOD = "agentic_devtools.cli.github.issue_dedup_io"


class TestSearchByMarker:
    """Tests for the search_by_marker function."""

    @patch(f"{_MOD}.resolve_github_repo", return_value="owner/repo")
    @patch(f"{_MOD}._gh_api")
    def test_single_page_results(self, mock_api, mock_repo) -> None:
        """Returns items from a single page."""
        from agentic_devtools.cli.github.issue_dedup_io import search_by_marker

        mock_api.return_value = json.dumps({"items": [{"number": 1, "body": "test"}]})
        result = search_by_marker("abc123def456abcd", repo="owner/repo")
        assert result == [{"number": 1, "body": "test"}]
        mock_api.assert_called_once()

    @patch(f"{_MOD}.resolve_github_repo", return_value="owner/repo")
    @patch(f"{_MOD}._gh_api")
    def test_multi_page_aggregation(self, mock_api, mock_repo) -> None:
        """Aggregates items from multiple pages."""
        from agentic_devtools.cli.github.issue_dedup_io import search_by_marker

        # Page 1: full page (100 items)
        page1_items = [{"number": i, "body": "x"} for i in range(100)]
        # Page 2: partial page (2 items)
        page2_items = [{"number": 200, "body": "y"}, {"number": 201, "body": "z"}]
        mock_api.side_effect = [
            json.dumps({"items": page1_items}),
            json.dumps({"items": page2_items}),
        ]
        result = search_by_marker("abc123def456abcd", repo="owner/repo")
        assert len(result) == 102

    @patch(f"{_MOD}.resolve_github_repo", return_value="owner/repo")
    @patch(f"{_MOD}._gh_api")
    def test_empty_results(self, mock_api, mock_repo) -> None:
        """Returns empty list when no results."""
        from agentic_devtools.cli.github.issue_dedup_io import search_by_marker

        mock_api.return_value = json.dumps({"items": []})
        result = search_by_marker("abc123def456abcd", repo="owner/repo")
        assert result == []

    @patch(f"{_MOD}.resolve_github_repo", return_value="owner/repo")
    @patch(f"{_MOD}._gh_api")
    def test_malformed_json_returns_empty(self, mock_api, mock_repo, capsys) -> None:
        """Malformed JSON returns empty list with stderr warning."""
        from agentic_devtools.cli.github.issue_dedup_io import search_by_marker

        mock_api.return_value = "not valid json {"
        result = search_by_marker("abc123def456abcd", repo="owner/repo")
        assert result == []
        assert "Malformed JSON" in capsys.readouterr().err

    @patch(f"{_MOD}.resolve_github_repo", return_value="owner/repo")
    @patch(f"{_MOD}._gh_api")
    def test_malformed_later_page_discards_partial_results(self, mock_api, mock_repo, capsys) -> None:
        """Malformed page after valid pages still returns empty list."""
        from agentic_devtools.cli.github.issue_dedup_io import search_by_marker

        page1_items = [{"number": i, "body": "x"} for i in range(100)]
        mock_api.side_effect = [
            json.dumps({"items": page1_items}),
            "not valid json {",
        ]
        result = search_by_marker("abc123def456abcd", repo="owner/repo")
        assert result == []
        assert "Malformed JSON" in capsys.readouterr().err

    @patch(f"{_MOD}.resolve_github_repo", return_value="owner/repo")
    @patch(f"{_MOD}._gh_api")
    def test_missing_items_key_returns_empty(self, mock_api, mock_repo, capsys) -> None:
        """Response without 'items' key returns empty list."""
        from agentic_devtools.cli.github.issue_dedup_io import search_by_marker

        mock_api.return_value = json.dumps({"total_count": 0})
        result = search_by_marker("abc123def456abcd", repo="owner/repo")
        assert result == []
        assert "Missing or invalid" in capsys.readouterr().err

    @patch(f"{_MOD}.resolve_github_repo", return_value="owner/repo")
    @patch(f"{_MOD}._gh_api")
    def test_non_json_output_returns_empty(self, mock_api, mock_repo, capsys) -> None:
        """Non-JSON output returns empty list with warning."""
        from agentic_devtools.cli.github.issue_dedup_io import search_by_marker

        mock_api.return_value = ""
        result = search_by_marker("abc123def456abcd", repo="owner/repo")
        assert result == []

    @patch(f"{_MOD}.resolve_github_repo", return_value="owner/repo")
    @patch(f"{_MOD}._gh_api")
    def test_url_encoding_in_query(self, mock_api, mock_repo) -> None:
        """Query string is URL-encoded in the endpoint."""
        from agentic_devtools.cli.github.issue_dedup_io import search_by_marker

        mock_api.return_value = json.dumps({"items": []})
        search_by_marker("abc123def456abcd", repo="owner/repo")
        endpoint = mock_api.call_args.args[0]
        # Should not contain raw spaces or quotes
        assert " " not in endpoint.split("?")[1]
        assert '"' not in endpoint.split("?")[1]

    @patch(f"{_MOD}.resolve_github_repo", return_value="owner/repo")
    @patch(f"{_MOD}._gh_api")
    def test_rate_limit_retry_fixed_5s_backoff(self, mock_api, mock_repo) -> None:
        """Rate limit triggers fixed 5-second retry."""
        from agentic_devtools.cli.github.issue_dedup_io import search_by_marker

        # Fail with rate limit 3 times then succeed
        call_count = 0

        def side_effect(endpoint, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count <= 3:
                raise RetryableError("secondary rate limit")
            return json.dumps({"items": [{"number": 1, "body": "x"}]})

        mock_api.side_effect = side_effect
        with patch("agentic_devtools.cli.shared.retry.time.sleep") as mock_sleep:
            result = search_by_marker("abc123def456abcd", repo="owner/repo")
        assert result == [{"number": 1, "body": "x"}]
        # Fixed 5s backoff for each retry
        assert mock_sleep.call_count == 3
        for call in mock_sleep.call_args_list:
            assert call.args[0] == 5.0

    @patch(f"{_MOD}.resolve_github_repo", return_value="owner/repo")
    @patch(f"{_MOD}._gh_api")
    def test_rate_limit_exhaustion_raises(self, mock_api, mock_repo) -> None:
        """Raises ProviderRateLimitError after 3 retries exhausted."""
        from agentic_devtools.cli.github.issue_dedup_io import search_by_marker

        mock_api.side_effect = RetryableError("rate limited", is_rate_limit=True)
        with patch("agentic_devtools.cli.shared.retry.time.sleep"):
            with pytest.raises(ProviderRateLimitError):
                search_by_marker("abc123def456abcd", repo="owner/repo")

    @patch(f"{_MOD}.resolve_github_repo", return_value="owner/repo")
    @patch(f"{_MOD}._gh_api")
    def test_unexpected_response_format(self, mock_api, mock_repo, capsys) -> None:
        """Non-dict response returns empty list."""
        from agentic_devtools.cli.github.issue_dedup_io import search_by_marker

        mock_api.return_value = json.dumps([1, 2, 3])
        result = search_by_marker("abc123def456abcd", repo="owner/repo")
        assert result == []
        assert "Unexpected response format" in capsys.readouterr().err

    @patch(f"{_MOD}.resolve_github_repo", return_value="owner/repo")
    @patch(f"{_MOD}._gh_api")
    def test_runtime_error_propagates_to_caller(self, mock_api, mock_repo) -> None:
        """Non-retryable RuntimeError propagates for fail-fast dedup policy."""
        from agentic_devtools.cli.github.issue_dedup_io import search_by_marker

        page1_items = [{"number": i, "body": "x"} for i in range(100)]
        mock_api.side_effect = [
            json.dumps({"items": page1_items}),
            RuntimeError("Not Found"),
        ]
        with pytest.raises(RuntimeError, match="Not Found"):
            search_by_marker("abc123def456abcd", repo="owner/repo")
