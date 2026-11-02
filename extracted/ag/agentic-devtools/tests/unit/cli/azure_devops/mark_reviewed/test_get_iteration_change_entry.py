"""Tests for _get_iteration_change_entry function."""

from unittest.mock import MagicMock

from agentic_devtools.cli.azure_devops.mark_reviewed import _get_iteration_change_entry


class TestGetIterationChangeEntry:
    """Tests for _get_iteration_change_entry."""

    def test_finds_matching_entry(self):
        """Returns ChangeEntry when file path matches."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "value": [
                {
                    "item": {"path": "/src/app/component.ts", "objectId": "abc123"},
                    "changeTrackingId": 42,
                }
            ]
        }
        mock_requests.get.return_value = mock_response

        result = _get_iteration_change_entry(
            mock_requests,
            {"Authorization": "Basic abc"},
            "https://dev.azure.com/org/project/_apis/git/repositories/repo/pullRequests/1/iterations/1/changes?api-version=7.1-preview.1",
            "/src/app/component.ts",
        )
        assert result is not None
        assert result.change_tracking_id == 42
        assert result.object_id == "abc123"
        assert result.path == "/src/app/component.ts"

    def test_case_insensitive_match(self):
        """Matches path case-insensitively."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "value": [
                {
                    "item": {"path": "/SRC/App/Component.ts", "objectId": "def456"},
                    "changeTrackingId": 7,
                }
            ]
        }
        mock_requests.get.return_value = mock_response

        result = _get_iteration_change_entry(
            mock_requests,
            {"Authorization": "Basic abc"},
            "https://example.com/changes?api-version=7.1",
            "/src/app/component.ts",
        )
        assert result is not None
        assert result.change_tracking_id == 7

    def test_returns_none_when_not_found(self):
        """Returns None when no entry matches target path."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "value": [
                {
                    "item": {"path": "/other/file.ts", "objectId": "xyz"},
                    "changeTrackingId": 1,
                }
            ]
        }
        mock_requests.get.return_value = mock_response

        result = _get_iteration_change_entry(
            mock_requests,
            {"Authorization": "Basic abc"},
            "https://example.com/changes?api-version=7.1",
            "/src/app/component.ts",
        )
        assert result is None

    def test_skips_entries_without_change_tracking_id(self):
        """Skips entries that don't have changeTrackingId."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "value": [
                {
                    "item": {"path": "/src/file.ts", "objectId": "abc"},
                    # No changeTrackingId
                }
            ]
        }
        mock_requests.get.return_value = mock_response

        result = _get_iteration_change_entry(
            mock_requests, {"Authorization": "Basic abc"}, "https://example.com/changes?api-version=7.1", "/src/file.ts"
        )
        assert result is None

    def test_uses_change_entries_key(self):
        """Falls back to 'changeEntries' key when 'value' is empty."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "value": [],
            "changeEntries": [
                {
                    "item": {"path": "/src/file.ts", "objectId": "abc"},
                    "changeTrackingId": 99,
                }
            ],
        }
        mock_requests.get.return_value = mock_response

        result = _get_iteration_change_entry(
            mock_requests, {"Authorization": "Basic abc"}, "https://example.com/changes?api-version=7.1", "/src/file.ts"
        )
        assert result is not None
        assert result.change_tracking_id == 99

    def test_follows_header_continuation_token(self):
        """Follows the Azure continuation response header for later pages."""
        mock_requests = MagicMock()
        first_response = MagicMock()
        first_response.headers = {"x-ms-continuationtoken": "header page"}
        first_response.json.return_value = {"value": []}
        second_response = MagicMock()
        second_response.headers = {}
        second_response.json.return_value = {
            "value": [
                {
                    "item": {"path": "/src/file.ts", "objectId": "abc123"},
                    "changeTrackingId": 42,
                }
            ]
        }
        mock_requests.get.side_effect = [first_response, second_response]

        result = _get_iteration_change_entry(
            mock_requests,
            {"Authorization": "Basic abc"},
            "https://example.com/changes?api-version=7.1",
            "/src/file.ts",
        )

        assert result is not None
        assert result.change_tracking_id == 42
        assert "continuationToken=header%20page" in mock_requests.get.call_args_list[1].args[0]

    def test_follows_next_skip_and_next_top(self):
        """Follows Azure iteration paging fields when locating a file on a later page."""
        mock_requests = MagicMock()
        first_response = MagicMock()
        first_response.headers = {}
        first_response.json.return_value = {"changeEntries": [], "nextSkip": 200, "nextTop": 74}
        second_response = MagicMock()
        second_response.headers = {}
        second_response.json.return_value = {
            "changeEntries": [
                {
                    "item": {"path": "/src/file.ts", "objectId": "abc123"},
                    "changeTrackingId": 42,
                }
            ]
        }
        mock_requests.get.side_effect = [first_response, second_response]

        result = _get_iteration_change_entry(
            mock_requests,
            {"Authorization": "Basic abc"},
            "https://example.com/changes?api-version=7.1",
            "/src/file.ts",
        )

        assert result is not None
        assert result.change_tracking_id == 42
        assert "$skip=200&$top=74" in mock_requests.get.call_args_list[1].args[0]
