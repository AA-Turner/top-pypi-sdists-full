"""Tests for _get_existing_viewed_state_tokens function."""

from unittest.mock import MagicMock

from agentic_devtools.cli.azure_devops.mark_reviewed import _get_existing_viewed_state_tokens


class TestGetExistingViewedStateTokens:
    """Tests for _get_existing_viewed_state_tokens."""

    def test_returns_hash_keys(self):
        """Returns hash keys from viewed state."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "dataProviders": {
                "ms.vss-code-web.pr-detail-visit-data-provider": {
                    "visit": {"viewedState": '{"hashes": {"token1": 1, "token2": 2}}'}
                }
            }
        }
        mock_requests.post.return_value = mock_response

        result = _get_existing_viewed_state_tokens(
            mock_requests, {"Authorization": "Basic abc"}, "https://dev.azure.com/org", "project-id", "repo-id", 123
        )
        assert sorted(result) == ["token1", "token2"]

    def test_returns_empty_on_exception(self):
        """Returns empty list on API failure."""
        mock_requests = MagicMock()
        mock_requests.post.side_effect = Exception("Network error")

        result = _get_existing_viewed_state_tokens(
            mock_requests, {"Authorization": "Basic abc"}, "https://dev.azure.com/org", "project-id", "repo-id", 123
        )
        assert result == []

    def test_returns_empty_when_no_viewed_state(self):
        """Returns empty list when viewedState is null/missing."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "dataProviders": {"ms.vss-code-web.pr-detail-visit-data-provider": {"visit": {"viewedState": None}}}
        }
        mock_requests.post.return_value = mock_response

        result = _get_existing_viewed_state_tokens(
            mock_requests, {"Authorization": "Basic abc"}, "https://dev.azure.com/org", "project-id", "repo-id", 123
        )
        assert result == []

    def test_returns_empty_on_invalid_json(self):
        """Returns empty list when viewedState is invalid JSON."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "dataProviders": {
                "ms.vss-code-web.pr-detail-visit-data-provider": {"visit": {"viewedState": "not-valid-json{"}}
            }
        }
        mock_requests.post.return_value = mock_response

        result = _get_existing_viewed_state_tokens(
            mock_requests, {"Authorization": "Basic abc"}, "https://dev.azure.com/org", "project-id", "repo-id", 123
        )
        assert result == []

    def test_returns_empty_when_hashes_not_dict(self):
        """Returns empty list when hashes is not a dict."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "dataProviders": {
                "ms.vss-code-web.pr-detail-visit-data-provider": {"visit": {"viewedState": '{"hashes": "not-a-dict"}'}}
            }
        }
        mock_requests.post.return_value = mock_response

        result = _get_existing_viewed_state_tokens(
            mock_requests, {"Authorization": "Basic abc"}, "https://dev.azure.com/org", "project-id", "repo-id", 123
        )
        assert result == []
