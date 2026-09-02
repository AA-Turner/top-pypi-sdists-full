"""Tests for _sync_viewed_status function."""

from unittest.mock import MagicMock

from agentic_devtools.cli.azure_devops.mark_reviewed import _sync_viewed_status


class TestSyncViewedStatus:
    """Tests for _sync_viewed_status."""

    def _make_iteration_response(self, iterations):
        """Helper to create iteration response."""
        mock = MagicMock()
        mock.json.return_value = {"value": iterations}
        return mock

    def _make_change_response(self, entries):
        """Helper to create change entries response."""
        mock = MagicMock()
        mock.json.return_value = {"value": entries}
        return mock

    def test_returns_early_when_no_iterations(self, capsys):
        """Returns early with message when no iterations."""
        mock_requests = MagicMock()
        # iterations response
        iter_response = MagicMock()
        iter_response.json.return_value = {"value": []}
        mock_requests.get.return_value = iter_response

        _sync_viewed_status(
            mock_requests,
            {"Authorization": "Basic abc"},
            "https://dev.azure.com/org",
            "MyProject",
            "project-id",
            "my-repo",
            "repo-id",
            123,
            "/src/file.ts",
            "org-account",
            "instance-1",
            [],
        )

        captured = capsys.readouterr()
        assert "Unable to resolve pull request iterations" in captured.out

    def test_returns_early_when_change_entry_not_found(self, capsys):
        """Returns early when file not found in any iteration."""
        mock_requests = MagicMock()
        # iterations response
        iter_response = MagicMock()
        iter_response.json.return_value = {"value": [{"id": 1}]}
        # changes response - no matching file
        changes_response = MagicMock()
        changes_response.json.return_value = {"value": [{"item": {"path": "/other.ts"}, "changeTrackingId": 1}]}
        mock_requests.get.side_effect = [iter_response, changes_response]

        _sync_viewed_status(
            mock_requests,
            {"Authorization": "Basic abc"},
            "https://dev.azure.com/org",
            "MyProject",
            "project-id",
            "my-repo",
            "repo-id",
            123,
            "/src/file.ts",
            "org-account",
            "instance-1",
            [],
        )

        captured = capsys.readouterr()
        assert "Unable to find change entry" in captured.out

    def test_returns_early_when_no_object_id(self, capsys):
        """Returns early when change entry has no objectId."""
        mock_requests = MagicMock()
        iter_response = MagicMock()
        iter_response.json.return_value = {"value": [{"id": 1}]}
        changes_response = MagicMock()
        changes_response.json.return_value = {
            "value": [{"item": {"path": "/src/file.ts", "objectId": None}, "changeTrackingId": 42}]
        }
        mock_requests.get.side_effect = [iter_response, changes_response]

        _sync_viewed_status(
            mock_requests,
            {"Authorization": "Basic abc"},
            "https://dev.azure.com/org",
            "MyProject",
            "project-id",
            "my-repo",
            "repo-id",
            123,
            "/src/file.ts",
            "org-account",
            "instance-1",
            [],
        )

        captured = capsys.readouterr()
        assert "missing object hash" in captured.out

    def test_successful_sync(self, capsys):
        """Posts contribution API call for successful sync."""
        mock_requests = MagicMock()
        iter_response = MagicMock()
        iter_response.json.return_value = {"value": [{"id": 2}, {"id": 1}]}
        changes_response = MagicMock()
        changes_response.json.return_value = {
            "value": [{"item": {"path": "/src/file.ts", "objectId": "abcdef12"}, "changeTrackingId": 5}]
        }
        contribution_response = MagicMock()
        mock_requests.get.side_effect = [iter_response, changes_response]
        mock_requests.post.return_value = contribution_response

        _sync_viewed_status(
            mock_requests,
            {"Authorization": "Basic abc"},
            "https://dev.azure.com/org",
            "MyProject",
            "project-id",
            "my-repo",
            "repo-id",
            123,
            "/src/file.ts",
            "org-account",
            "instance-1",
            [],
        )

        captured = capsys.readouterr()
        assert "Syncing viewed status" in captured.out
        mock_requests.post.assert_called_once()
        # Verify the post was to the Contribution API
        post_call = mock_requests.post.call_args
        assert "Contribution/HierarchyQuery" in post_call[0][0]

    def test_sorts_iterations_descending(self, capsys):
        """Checks most recent iteration first."""
        mock_requests = MagicMock()
        iter_response = MagicMock()
        iter_response.json.return_value = {"value": [{"id": 1}, {"id": 3}, {"id": 2}]}
        # First GET after iterations (for id=3) returns match
        changes_response_3 = MagicMock()
        changes_response_3.json.return_value = {
            "value": [{"item": {"path": "/src/file.ts", "objectId": "hash999"}, "changeTrackingId": 10}]
        }
        contribution_response = MagicMock()
        mock_requests.get.side_effect = [iter_response, changes_response_3]
        mock_requests.post.return_value = contribution_response

        _sync_viewed_status(
            mock_requests,
            {"Authorization": "Basic abc"},
            "https://dev.azure.com/org",
            "MyProject",
            "project-id",
            "my-repo",
            "repo-id",
            123,
            "/src/file.ts",
            None,
            None,
            [],
        )

        # Should have called get twice: iterations + changes for id=3 (highest)
        assert mock_requests.get.call_count == 2
        second_get_url = mock_requests.get.call_args_list[1][0][0]
        assert "iterations/3/changes" in second_get_url

    def test_matches_existing_hash_tokens(self, capsys):
        """Processes existing hash tokens that match the file path."""
        mock_requests = MagicMock()
        iter_response = MagicMock()
        iter_response.json.return_value = {"value": [{"id": 1}]}
        changes_response = MagicMock()
        changes_response.json.return_value = {
            "value": [{"item": {"path": "/src/file.ts", "objectId": "abcdef99"}, "changeTrackingId": 5}]
        }
        contribution_response = MagicMock()
        mock_requests.get.side_effect = [iter_response, changes_response]
        mock_requests.post.return_value = contribution_response

        # Pass existing tokens - one matches the path pattern
        existing_tokens = [
            "1@DEADBEEF@/src/file.ts",
            "1@CAFEBABE@/other/file.ts",
        ]

        _sync_viewed_status(
            mock_requests,
            {"Authorization": "Basic abc"},
            "https://dev.azure.com/org",
            "MyProject",
            "project-id",
            "my-repo",
            "repo-id",
            123,
            "/src/file.ts",
            "org-account",
            "instance-1",
            existing_tokens,
        )

        captured = capsys.readouterr()
        assert "Syncing viewed status" in captured.out
        mock_requests.post.assert_called_once()

    def test_no_project_no_source_page(self, capsys):
        """Skips source_page when project is empty."""
        mock_requests = MagicMock()
        iter_response = MagicMock()
        iter_response.json.return_value = {"value": [{"id": 1}]}
        changes_response = MagicMock()
        changes_response.json.return_value = {
            "value": [{"item": {"path": "/src/file.ts", "objectId": "abc12345"}, "changeTrackingId": 3}]
        }
        contribution_response = MagicMock()
        mock_requests.get.side_effect = [iter_response, changes_response]
        mock_requests.post.return_value = contribution_response

        _sync_viewed_status(
            mock_requests,
            {"Authorization": "Basic abc"},
            "https://dev.azure.com/org",
            "",
            "project-id",
            "",
            "repo-id",
            123,
            "/src/file.ts",
            None,
            None,
            [],
        )

        # Should still post (without sourcePage property)
        mock_requests.post.assert_called_once()
        post_payload = mock_requests.post.call_args[1]["json"]
        properties = post_payload["dataProviderContext"]["properties"]
        assert "sourcePage" not in properties
