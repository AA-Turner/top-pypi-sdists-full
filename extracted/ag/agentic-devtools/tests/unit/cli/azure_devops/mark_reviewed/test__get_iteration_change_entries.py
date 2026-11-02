"""Tests for _get_iteration_change_entries."""

from unittest.mock import MagicMock

from agentic_devtools.cli.azure_devops.mark_reviewed import _get_iteration_change_entries


class TestGetIterationChangeEntries:
    def test_returns_matching_entries(self):
        """Matching paths are returned as ChangeEntry values."""
        requests = MagicMock()
        response = MagicMock()
        response.json.return_value = {
            "value": [
                {"changeTrackingId": 1, "item": {"path": "/src/first.ts", "objectId": "abc123"}},
                {"changeTrackingId": 2, "item": {"path": "/src/other.ts", "objectId": "def456"}},
            ]
        }
        requests.get.return_value = response

        result = _get_iteration_change_entries(requests, {}, "https://example/changes", ["/src/first.ts"])

        assert list(result) == ["/src/first.ts"]
        assert result["/src/first.ts"].object_id == "abc123"
        requests.get.assert_called_once()

    def test_handles_pagination_and_change_entries_alias(self):
        """The helper follows a next link and accepts the alternate response key."""
        requests = MagicMock()
        first_response = MagicMock()
        first_response.json.return_value = {"changeEntries": [], "nextLink": "https://example/changes?page=2"}
        second_response = MagicMock()
        second_response.json.return_value = {
            "changeEntries": [{"changeTrackingId": 1, "item": {"path": "/src/second.ts", "objectId": "abc123"}}]
        }
        requests.get.side_effect = [first_response, second_response]

        result = _get_iteration_change_entries(requests, {}, "https://example/changes", ["/src/second.ts"])

        assert result["/src/second.ts"].change_tracking_id == 1
        assert requests.get.call_count == 2

    def test_ignores_malformed_and_unmatched_entries(self):
        """Malformed entries and entries without change IDs are ignored."""
        requests = MagicMock()
        response = MagicMock()
        response.json.return_value = {
            "value": [
                None,
                {"item": {"path": "/src/first.ts", "objectId": "abc123"}},
                {"changeTrackingId": 1, "item": {"path": "/src/other.ts"}},
                {"changeTrackingId": 2, "item": {"path": "/src/first.ts", "objectId": "abc123"}},
            ]
        }
        requests.get.return_value = response

        result = _get_iteration_change_entries(requests, {}, "https://example/changes", ["/src/first.ts"])

        assert result["/src/first.ts"].change_tracking_id == 2

    def test_follows_continuation_token(self):
        """A continuation token is encoded into the next request URL."""
        requests = MagicMock()
        first_response = MagicMock()
        first_response.json.return_value = {"value": [], "continuationToken": "next page"}
        second_response = MagicMock()
        second_response.json.return_value = {
            "value": [{"changeTrackingId": 1, "item": {"path": "/src/second.ts", "objectId": "abc123"}}]
        }
        requests.get.side_effect = [first_response, second_response]

        result = _get_iteration_change_entries(requests, {}, "https://example/changes", ["/src/second.ts"])

        assert result["/src/second.ts"].change_tracking_id == 1
        assert "continuationToken=next%20page" in requests.get.call_args_list[1].args[0]

    def test_follows_header_continuation_token(self):
        """The Azure continuation response header is followed when JSON has no token."""
        requests = MagicMock()
        first_response = MagicMock()
        first_response.headers = {"x-ms-continuationtoken": "header page"}
        first_response.json.return_value = {"value": []}
        second_response = MagicMock()
        second_response.headers = {}
        second_response.json.return_value = {
            "value": [{"changeTrackingId": 1, "item": {"path": "/src/second.ts", "objectId": "abc123"}}]
        }
        requests.get.side_effect = [first_response, second_response]

        result = _get_iteration_change_entries(requests, {}, "https://example/changes", ["/src/second.ts"])

        assert result["/src/second.ts"].change_tracking_id == 1
        assert "continuationToken=header%20page" in requests.get.call_args_list[1].args[0]

    def test_follows_next_skip_and_next_top(self):
        """The Azure iteration response paging fields are followed for later pages."""
        requests = MagicMock()
        first_response = MagicMock()
        first_response.headers = {}
        first_response.json.return_value = {"changeEntries": [], "nextSkip": 200, "nextTop": 74}
        second_response = MagicMock()
        second_response.headers = {}
        second_response.json.return_value = {
            "changeEntries": [{"changeTrackingId": 1, "item": {"path": "/src/second.ts", "objectId": "abc123"}}]
        }
        requests.get.side_effect = [first_response, second_response]

        result = _get_iteration_change_entries(requests, {}, "https://example/changes", ["/src/second.ts"])

        assert result["/src/second.ts"].change_tracking_id == 1
        assert "$skip=200&$top=74" in requests.get.call_args_list[1].args[0]

    def test_skips_invalid_entries_and_empty_targets(self):
        """Invalid entry shapes are ignored and an empty target list does no I/O."""
        requests = MagicMock()
        response = MagicMock()
        response.json.return_value = {
            "value": [
                {"item": []},
                {"changeTrackingId": 1, "item": {"path": 42}},
            ]
        }
        requests.get.return_value = response

        assert _get_iteration_change_entries(requests, {}, "https://example/changes", []) == {}
        assert _get_iteration_change_entries(requests, {}, "https://example/changes", ["/src/missing.ts"]) == {}
        assert requests.get.call_count == 1

    def test_ignores_non_list_response_entries(self):
        """A malformed response collection is treated as empty."""
        requests = MagicMock()
        response = MagicMock()
        response.json.return_value = {"value": {"path": "/src/first.ts"}}
        requests.get.return_value = response

        assert _get_iteration_change_entries(requests, {}, "https://example/changes", ["/src/first.ts"]) == {}
