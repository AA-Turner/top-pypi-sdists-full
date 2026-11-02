"""Tests for _sync_viewed_status_batch."""

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.azure_devops.mark_reviewed import (
    ChangeEntry,
    ViewedStatusSyncError,
    _sync_viewed_status_batch,
)


class TestSyncViewedStatusBatch:
    def test_fetches_changes_once_and_posts_one_contribution_batch(self):
        """All matching file tokens are sent in one Contribution request."""
        requests = MagicMock()
        iterations_response = MagicMock()
        iterations_response.json.return_value = {"value": [{"id": 2}, {"id": 1}]}
        changes_response = MagicMock()
        changes_response.json.return_value = {
            "value": [
                {"changeTrackingId": 1, "item": {"path": "/src/first.ts", "objectId": "abc123456"}},
                {"changeTrackingId": 2, "item": {"path": "/src/second.ts", "objectId": "def987654"}},
            ]
        }
        requests.get.side_effect = [iterations_response, changes_response]

        result = _sync_viewed_status_batch(
            requests,
            {"Authorization": "Basic xxx"},
            "https://dev.azure.com/test",
            "TestProject",
            "project-id",
            "TestRepo",
            "repo-guid",
            123,
            ["/src/first.ts", "/src/second.ts"],
            "test-org",
            "instance-id",
            [],
        )

        assert result.synced_paths == ["/src/first.ts", "/src/second.ts"]
        assert result.failed_paths == []
        assert requests.get.call_count == 2
        requests.post.assert_called_once()
        payload = requests.post.call_args.kwargs["json"]
        assert payload["dataProviderContext"]["properties"]["modifyHashes"] == [
            "1@ABC12345@/src/first.ts",
            "1@DEF98765@/src/second.ts",
        ]

    def test_splits_large_token_set_into_bounded_contribution_batches(self):
        """Large viewed-status updates are split into requests of at most 200 tokens."""
        requests = MagicMock()
        iterations_response = MagicMock()
        iterations_response.json.return_value = {"value": [{"id": 1}]}
        changes_response = MagicMock()
        paths = [f"/src/file-{index}.ts" for index in range(250)]
        changes_response.json.return_value = {
            "value": [
                {"changeTrackingId": index, "item": {"path": path, "objectId": f"{index:08x}"}}
                for index, path in enumerate(paths, start=1)
            ]
        }
        requests.get.side_effect = [iterations_response, changes_response]

        result = _sync_viewed_status_batch(
            requests,
            {},
            "https://dev.azure.com/test",
            "TestProject",
            "project-id",
            "TestRepo",
            "repo-guid",
            123,
            paths,
            None,
            None,
            [],
        )

        assert result.failed_paths == []
        assert requests.post.call_count == 2
        token_batches = [
            call.kwargs["json"]["dataProviderContext"]["properties"]["modifyHashes"]
            for call in requests.post.call_args_list
        ]
        assert [len(batch) for batch in token_batches] == [200, 50]

    def test_uses_existing_token_when_object_id_is_missing(self):
        """An existing viewed token remains usable when the change has no object ID."""
        requests = MagicMock()
        iterations_response = MagicMock()
        iterations_response.json.return_value = {"value": [{"id": 1}]}
        changes_response = MagicMock()
        changes_response.json.return_value = {"value": [{"changeTrackingId": 1, "item": {"path": "/src/first.ts"}}]}
        requests.get.side_effect = [iterations_response, changes_response]

        result = _sync_viewed_status_batch(
            requests,
            {},
            "https://dev.azure.com/test",
            "",
            "project-id",
            "",
            "repo-guid",
            123,
            ["/src/first.ts"],
            None,
            None,
            ["1@ABC@/src/first.ts"],
        )

        assert result.synced_paths == ["/src/first.ts"]
        requests.post.assert_called_once()
        payload = requests.post.call_args.kwargs["json"]
        assert payload["dataProviderContext"]["properties"]["modifyHashes"] == ["1@ABC@/src/first.ts"]
        assert "sourcePage" not in payload["dataProviderContext"]["properties"]

    def test_deduplicates_matching_existing_tokens(self):
        """Duplicate existing tokens are collapsed before submission."""
        requests = MagicMock()
        iterations_response = MagicMock()
        iterations_response.json.return_value = {"value": [{"id": 1}]}
        changes_response = MagicMock()
        changes_response.json.return_value = {"value": [{"changeTrackingId": 1, "item": {"path": "/src/first.ts"}}]}
        requests.get.side_effect = [iterations_response, changes_response]

        result = _sync_viewed_status_batch(
            requests,
            {},
            "https://dev.azure.com/test",
            "",
            "project-id",
            "",
            "repo-guid",
            123,
            ["/src/first.ts"],
            None,
            None,
            ["1@ABC@/src/first.ts", "1@ABC@/src/first.ts"],
        )

        assert result.synced_paths == ["/src/first.ts"]
        payload = requests.post.call_args.kwargs["json"]
        assert payload["dataProviderContext"]["properties"]["modifyHashes"] == ["1@ABC@/src/first.ts"]

    def test_uses_nonpreferred_existing_token_and_omits_service_host(self):
        """A non-preferred existing token is retained when no service instance is provided."""
        requests = MagicMock()
        iterations_response = MagicMock()
        iterations_response.json.return_value = {"value": [{"id": 1}]}
        changes_response = MagicMock()
        changes_response.json.return_value = {"value": [{"changeTrackingId": 1, "item": {"path": "/src/first.ts"}}]}
        requests.get.side_effect = [iterations_response, changes_response]

        result = _sync_viewed_status_batch(
            requests,
            {},
            "https://dev.azure.com/test",
            "TestProject",
            "project-id",
            "TestRepo",
            "repo-guid",
            123,
            ["/src/first.ts"],
            "test-org",
            None,
            ["2@ABC@/src/first.ts"],
        )

        assert result.synced_paths == ["/src/first.ts"]
        payload = requests.post.call_args.kwargs["json"]
        assert payload["dataProviderContext"]["properties"]["modifyHashes"] == ["2@ABC@/src/first.ts"]
        assert "serviceHost" not in payload["dataProviderContext"]["properties"]["sourcePage"]["routeValues"]

    def test_returns_without_post_when_iterations_are_missing(self):
        """Missing iteration data prevents a Contribution request."""
        requests = MagicMock()
        response = MagicMock()
        response.json.return_value = {"value": []}
        requests.get.return_value = response

        result = _sync_viewed_status_batch(
            requests,
            {},
            "https://dev.azure.com/test",
            "TestProject",
            "project-id",
            "TestRepo",
            "repo-guid",
            123,
            ["/src/first.ts"],
            None,
            None,
            [],
        )

        assert result.synced_paths == []
        assert result.failed_paths == ["/src/first.ts"]
        requests.post.assert_not_called()

    @patch(
        "agentic_devtools.cli.azure_devops.mark_reviewed._get_iteration_change_entries",
        return_value={"/src/missing.ts": ChangeEntry(change_tracking_id=1, object_id=None, path="/src/missing.ts")},
    )
    def test_returns_without_post_when_no_tokens_can_be_built(self, mock_entries):
        """Files without a change entry or existing token are skipped."""
        requests = MagicMock()
        response = MagicMock()
        response.json.return_value = {"value": [{"id": 1}]}
        requests.get.return_value = response

        result = _sync_viewed_status_batch(
            requests,
            {},
            "https://dev.azure.com/test",
            "TestProject",
            "project-id",
            "TestRepo",
            "repo-guid",
            123,
            ["/src/missing.ts"],
            None,
            None,
            [],
        )

        mock_entries.assert_called_once()
        assert result.synced_paths == []
        assert result.failed_paths == ["/src/missing.ts"]
        requests.post.assert_not_called()

    @patch("agentic_devtools.cli.azure_devops.mark_reviewed._get_iteration_change_entries", return_value={})
    def test_skips_non_dict_and_missing_id_iterations(self, mock_entries):
        """Invalid iteration records are skipped before valid records are queried."""
        requests = MagicMock()
        response = MagicMock()
        response.json.return_value = {"value": [None, {}, {"id": "invalid"}]}
        requests.get.return_value = response

        result = _sync_viewed_status_batch(
            requests,
            {},
            "https://dev.azure.com/test",
            "TestProject",
            "project-id",
            "TestRepo",
            "repo-guid",
            123,
            ["/src/missing.ts"],
            None,
            None,
            [],
        )

        mock_entries.assert_called_once()
        assert result.failed_paths == ["/src/missing.ts"]

    def test_raises_with_synced_and_failed_paths_when_later_batch_post_fails(self):
        """Later Contribution failures preserve the synced/failed path split."""
        requests = MagicMock()
        iterations_response = MagicMock()
        iterations_response.json.return_value = {"value": [{"id": 1}]}
        changes_response = MagicMock()
        paths = [f"/src/file-{index}.ts" for index in range(201)]
        changes_response.json.return_value = {
            "value": [
                {"changeTrackingId": index, "item": {"path": path, "objectId": f"{index:08x}"}}
                for index, path in enumerate(paths, start=1)
            ]
        }
        failing_response = MagicMock()
        failing_response.raise_for_status.side_effect = RuntimeError("boom")
        requests.get.side_effect = [iterations_response, changes_response]
        requests.post.side_effect = [MagicMock(), failing_response]

        try:
            _sync_viewed_status_batch(
                requests,
                {},
                "https://dev.azure.com/test",
                "TestProject",
                "project-id",
                "TestRepo",
                "repo-guid",
                123,
                paths,
                None,
                None,
                [],
            )
        except ViewedStatusSyncError as exc:
            assert exc.synced_paths == paths[:200]
            assert exc.failed_paths == [paths[200]]
        else:  # pragma: no cover
            raise AssertionError("Expected viewed-status synchronization to fail")
