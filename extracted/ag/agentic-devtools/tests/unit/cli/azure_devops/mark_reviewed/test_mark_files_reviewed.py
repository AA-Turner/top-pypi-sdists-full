"""Tests for mark_files_reviewed."""

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig
from agentic_devtools.cli.azure_devops.mark_reviewed import (
    AuthenticatedUser,
    CachedReviewerContext,
    ViewedStatusSyncError,
    mark_files_reviewed,
)


def _make_config() -> AzureDevOpsConfig:
    return AzureDevOpsConfig(
        organization="https://dev.azure.com/test",
        project="TestProject",
        repository="TestRepo",
    )


_DEFAULT_REVIEWER_ENTRY = object()


def _make_context(reviewer_entry=_DEFAULT_REVIEWER_ENTRY) -> CachedReviewerContext:
    return CachedReviewerContext(
        requests=MagicMock(),
        headers={"Authorization": "Basic xxx"},
        auth_user=AuthenticatedUser(
            display_name="Test User",
            descriptor="aad.123",
            storage_key="guid-456",
            subject_descriptor=None,
        ),
        reviewer_id="guid-456",
        instance_id="inst-1",
        organization_account_name="test-org",
        reviewer_entry={"reviewedFiles": []} if reviewer_entry is _DEFAULT_REVIEWER_ENTRY else reviewer_entry,
    )


class TestMarkFilesReviewed:
    @patch("agentic_devtools.cli.azure_devops.mark_reviewed._sync_viewed_status_batch")
    @patch("agentic_devtools.cli.azure_devops.mark_reviewed._get_existing_viewed_state_tokens", return_value=[])
    @patch("agentic_devtools.cli.azure_devops.mark_reviewed._get_project_id_via_api", return_value="project-id")
    @patch("agentic_devtools.cli.azure_devops.mark_reviewed._update_reviewer_entry")
    def test_batches_reviewer_and_viewed_status_updates(
        self,
        mock_update_reviewer,
        mock_project_id,
        mock_existing_tokens,
        mock_sync_viewed,
        capsys,
    ):
        """Multiple files use one reviewer update and one viewed-status batch."""
        context = _make_context()

        result = mark_files_reviewed(
            ["src/first.ts", "src/second.ts"],
            pull_request_id=123,
            config=_make_config(),
            repo_id="repo-guid",
            cached_context=context,
        )

        assert result is True
        mock_update_reviewer.assert_called_once()
        assert mock_update_reviewer.call_args.args[-1] == ["/src/first.ts", "/src/second.ts"]
        mock_project_id.assert_called_once()
        mock_existing_tokens.assert_called_once()
        mock_sync_viewed.assert_called_once()
        assert context.reviewer_entry["reviewedFiles"] == ["/src/first.ts", "/src/second.ts"]
        assert "Marked 2 files as reviewed." in capsys.readouterr().out

    def test_rejects_invalid_path(self, capsys):
        """An invalid path aborts the batch before resolving API context."""
        assert mark_files_reviewed([""], 123, _make_config(), "repo-guid") is False
        assert "Invalid file path" in capsys.readouterr().err

    def test_reports_all_paths_when_one_path_is_invalid(self):
        """An invalid path aborts the batch and reports every requested path."""
        result = mark_files_reviewed(
            ["src/first.ts", "", "src/third.ts", " ", ""],
            123,
            _make_config(),
            "repo-guid",
            return_details=True,
        )

        assert result.succeeded is False
        assert result.failed_paths == ["/src/first.ts", "", "/src/third.ts", " "]

    def test_dry_run_skips_api_context(self, capsys):
        """Dry-run mode reports the batch without resolving reviewer context."""
        with patch("agentic_devtools.cli.azure_devops.mark_reviewed._build_reviewer_context") as build_context:
            assert mark_files_reviewed(["src/first.ts"], 123, _make_config(), "repo-guid", dry_run=True) is True

        build_context.assert_not_called()
        assert "DRY-RUN" in capsys.readouterr().out

    def test_returns_false_when_reviewer_context_setup_fails(self):
        """Reviewer context setup failures are surfaced as a failed batch."""
        with (
            patch("agentic_devtools.cli.azure_devops.mark_reviewed.get_batch_context", return_value=None),
            patch(
                "agentic_devtools.cli.azure_devops.mark_reviewed._build_reviewer_context",
                side_effect=RuntimeError("context unavailable"),
            ),
        ):
            assert mark_files_reviewed(["src/first.ts"], 123, _make_config(), "repo-guid") is False

    def test_returns_false_when_reviewer_entry_lookup_fails(self):
        """Reviewer entry lookup failures prevent the batch update."""
        context = _make_context(reviewer_entry=None)
        with patch(
            "agentic_devtools.cli.azure_devops.mark_reviewed._get_reviewer_entry",
            side_effect=RuntimeError("reviewer unavailable"),
        ):
            assert (
                mark_files_reviewed(["src/first.ts"], 123, _make_config(), "repo-guid", cached_context=context) is False
            )

    @patch("agentic_devtools.cli.azure_devops.mark_reviewed._sync_viewed_status_batch")
    @patch("agentic_devtools.cli.azure_devops.mark_reviewed._get_existing_viewed_state_tokens", return_value=[])
    @patch("agentic_devtools.cli.azure_devops.mark_reviewed._get_project_id_via_api", return_value="project-id")
    @patch("agentic_devtools.cli.azure_devops.mark_reviewed._update_reviewer_entry")
    @patch("agentic_devtools.cli.azure_devops.mark_reviewed._get_reviewer_entry", return_value=None)
    def test_creates_reviewer_entry_when_lookup_returns_none(
        self,
        mock_reviewer_entry,
        mock_update_reviewer,
        mock_project_id,
        mock_existing_tokens,
        mock_sync_viewed,
    ):
        """A missing reviewer entry is created with the complete batch."""
        context = _make_context(reviewer_entry=None)

        assert mark_files_reviewed(["src/first.ts"], 123, _make_config(), "repo-guid", cached_context=context) is True

        mock_reviewer_entry.assert_called_once()
        mock_update_reviewer.assert_called_once()
        mock_project_id.assert_called_once()
        mock_existing_tokens.assert_called_once()
        mock_sync_viewed.assert_called_once()

    @patch("agentic_devtools.cli.azure_devops.mark_reviewed._sync_viewed_status_batch")
    @patch("agentic_devtools.cli.azure_devops.mark_reviewed._get_existing_viewed_state_tokens", return_value=[])
    @patch("agentic_devtools.cli.azure_devops.mark_reviewed._get_project_id_via_api", return_value="project-id")
    @patch("agentic_devtools.cli.azure_devops.mark_reviewed._update_reviewer_entry")
    @patch(
        "agentic_devtools.cli.azure_devops.mark_reviewed._get_reviewer_entry",
        return_value={"reviewedFiles": [], "vote": 0},
    )
    def test_caches_reviewer_entry_returned_by_lookup(
        self,
        mock_reviewer_entry,
        mock_update_reviewer,
        mock_project_id,
        mock_existing_tokens,
        mock_sync_viewed,
    ):
        """A reviewer entry returned by lookup is cached before the batch update."""
        context = _make_context(reviewer_entry=None)

        assert mark_files_reviewed(["src/first.ts"], 123, _make_config(), "repo-guid", cached_context=context)

        mock_reviewer_entry.assert_called_once()
        assert context.reviewer_entry["reviewedFiles"] == ["/src/first.ts"]
        mock_update_reviewer.assert_called_once()
        mock_project_id.assert_called_once()
        mock_existing_tokens.assert_called_once()
        mock_sync_viewed.assert_called_once()

    def test_skips_batch_when_all_paths_are_reviewed(self):
        """Already-reviewed files still retry viewed-status synchronization."""
        context = _make_context(reviewer_entry={"reviewedFiles": ["/src/first.ts"]})
        with (
            patch("agentic_devtools.cli.azure_devops.mark_reviewed._update_reviewer_entry") as update,
            patch("agentic_devtools.cli.azure_devops.mark_reviewed._get_project_id_via_api", return_value="project-id"),
            patch("agentic_devtools.cli.azure_devops.mark_reviewed._get_existing_viewed_state_tokens", return_value=[]),
            patch("agentic_devtools.cli.azure_devops.mark_reviewed._sync_viewed_status_batch") as sync,
        ):
            assert mark_files_reviewed(["src/first.ts"], 123, _make_config(), "repo-guid", cached_context=context)
        update.assert_not_called()
        sync.assert_called_once()

    def test_returns_false_when_reviewer_update_fails(self):
        """A reviewer entry update failure aborts the batch."""
        context = _make_context()
        with patch(
            "agentic_devtools.cli.azure_devops.mark_reviewed._update_reviewer_entry",
            side_effect=RuntimeError("update unavailable"),
        ):
            assert (
                mark_files_reviewed(["src/first.ts"], 123, _make_config(), "repo-guid", cached_context=context) is False
            )

    @patch("agentic_devtools.cli.azure_devops.mark_reviewed._get_existing_viewed_state_tokens")
    @patch("agentic_devtools.cli.azure_devops.mark_reviewed._get_project_id_via_api")
    @patch("agentic_devtools.cli.azure_devops.mark_reviewed._update_reviewer_entry")
    def test_reuses_cached_project_and_tokens(self, mock_update_reviewer, mock_project_id, mock_existing_tokens):
        """Pre-populated batch context skips both shared context lookups."""
        context = _make_context()
        context.project_id = "project-id"
        context.existing_hash_tokens = []
        with patch("agentic_devtools.cli.azure_devops.mark_reviewed._sync_viewed_status_batch") as sync:
            assert mark_files_reviewed(["src/first.ts"], 123, _make_config(), "repo-guid", cached_context=context)

        mock_update_reviewer.assert_called_once()
        mock_project_id.assert_not_called()
        mock_existing_tokens.assert_not_called()
        sync.assert_called_once()

    @patch("agentic_devtools.cli.azure_devops.mark_reviewed._sync_viewed_status_batch")
    @patch(
        "agentic_devtools.cli.azure_devops.mark_reviewed._get_existing_viewed_state_tokens",
        side_effect=RuntimeError("tokens unavailable"),
    )
    @patch("agentic_devtools.cli.azure_devops.mark_reviewed._get_project_id_via_api", return_value="project-id")
    @patch("agentic_devtools.cli.azure_devops.mark_reviewed._update_reviewer_entry")
    def test_continues_when_existing_tokens_lookup_fails(
        self, mock_update_reviewer, mock_project_id, mock_existing_tokens, mock_sync_viewed
    ):
        """A best-effort viewed-token lookup failure still keeps reviewer marking successful."""
        context = _make_context()
        assert mark_files_reviewed(["src/first.ts"], 123, _make_config(), "repo-guid", cached_context=context)
        assert context.existing_hash_tokens == []
        mock_sync_viewed.assert_called_once()

    @patch("agentic_devtools.cli.azure_devops.mark_reviewed._sync_viewed_status_batch")
    @patch(
        "agentic_devtools.cli.azure_devops.mark_reviewed._get_project_id_via_api",
        side_effect=RuntimeError("project unavailable"),
    )
    @patch("agentic_devtools.cli.azure_devops.mark_reviewed._update_reviewer_entry")
    def test_returns_false_when_project_id_lookup_fails(self, mock_update_reviewer, mock_project_id, mock_sync_viewed):
        """A project lookup failure keeps the batch retriable."""
        context = _make_context()

        assert mark_files_reviewed(["src/first.ts"], 123, _make_config(), "repo-guid", cached_context=context) is False
        mock_project_id.assert_called_once()
        mock_sync_viewed.assert_not_called()

    @patch("agentic_devtools.cli.azure_devops.mark_reviewed._sync_viewed_status_batch")
    @patch("agentic_devtools.cli.azure_devops.mark_reviewed._get_project_id_via_api", return_value=None)
    @patch("agentic_devtools.cli.azure_devops.mark_reviewed._update_reviewer_entry")
    def test_returns_false_when_project_id_is_missing(self, mock_update_reviewer, mock_project_id, mock_sync_viewed):
        """A missing project ID leaves viewed-status finalization incomplete."""
        context = _make_context()

        assert mark_files_reviewed(["src/first.ts"], 123, _make_config(), "repo-guid", cached_context=context) is False
        mock_project_id.assert_called_once()
        mock_sync_viewed.assert_not_called()

    @patch(
        "agentic_devtools.cli.azure_devops.mark_reviewed._sync_viewed_status_batch",
        side_effect=RuntimeError("sync failed"),
    )
    @patch("agentic_devtools.cli.azure_devops.mark_reviewed._get_existing_viewed_state_tokens", return_value=[])
    @patch("agentic_devtools.cli.azure_devops.mark_reviewed._get_project_id_via_api", return_value="project-id")
    @patch("agentic_devtools.cli.azure_devops.mark_reviewed._update_reviewer_entry")
    def test_returns_false_when_viewed_status_sync_fails(
        self, mock_update_reviewer, mock_project_id, mock_existing_tokens, mock_sync_viewed
    ):
        """Viewed-status synchronization failure makes the batch unsuccessful."""
        context = _make_context()
        assert mark_files_reviewed(["src/first.ts"], 123, _make_config(), "repo-guid", cached_context=context) is False
        mock_sync_viewed.assert_called_once()

    @patch("agentic_devtools.cli.azure_devops.mark_reviewed._get_existing_viewed_state_tokens", return_value=[])
    @patch("agentic_devtools.cli.azure_devops.mark_reviewed._get_project_id_via_api", return_value="project-id")
    @patch("agentic_devtools.cli.azure_devops.mark_reviewed._update_reviewer_entry")
    def test_returns_false_when_viewed_status_sync_reports_partial_progress(
        self, mock_update_reviewer, mock_project_id, mock_existing_tokens
    ):
        """Structured viewed-status failures preserve the synced/failed split."""
        context = _make_context()
        with patch(
            "agentic_devtools.cli.azure_devops.mark_reviewed._sync_viewed_status_batch",
            side_effect=ViewedStatusSyncError(
                "Failed to sync viewed status: boom",
                synced_paths=["/src/first.ts"],
                failed_paths=["/src/second.ts"],
            ),
        ):
            result = mark_files_reviewed(
                ["src/first.ts", "src/second.ts"],
                123,
                _make_config(),
                "repo-guid",
                cached_context=context,
                return_details=True,
            )

        assert result.succeeded is False
        assert result.synced_paths == ["/src/first.ts"]
        assert result.failed_paths == ["/src/second.ts"]

    @patch("agentic_devtools.cli.azure_devops.mark_reviewed._get_existing_viewed_state_tokens", return_value=[])
    @patch("agentic_devtools.cli.azure_devops.mark_reviewed._get_project_id_via_api", return_value="project-id")
    @patch("agentic_devtools.cli.azure_devops.mark_reviewed._update_reviewer_entry")
    def test_returns_false_when_some_paths_are_not_synchronized(
        self, mock_update_reviewer, mock_project_id, mock_existing_tokens
    ):
        """Partial viewed-status synchronization reports a failed batch."""
        context = _make_context()
        with patch(
            "agentic_devtools.cli.azure_devops.mark_reviewed._sync_viewed_status_batch",
            return_value=MagicMock(synced_paths=["/src/first.ts"], failed_paths=["/src/second.ts"]),
        ):
            result = mark_files_reviewed(
                ["src/first.ts", "src/second.ts"],
                123,
                _make_config(),
                "repo-guid",
                cached_context=context,
                return_details=True,
            )

        assert result.succeeded is False
        assert result.synced_paths == ["/src/first.ts"]
        assert result.failed_paths == ["/src/second.ts"]

    @patch("agentic_devtools.cli.azure_devops.mark_reviewed._sync_viewed_status_batch")
    @patch("agentic_devtools.cli.azure_devops.mark_reviewed._get_existing_viewed_state_tokens", return_value=[])
    @patch("agentic_devtools.cli.azure_devops.mark_reviewed._get_project_id_via_api", return_value="project-id")
    @patch("agentic_devtools.cli.azure_devops.mark_reviewed._update_reviewer_entry")
    def test_deduplicates_paths_and_skips_already_reviewed_files(
        self,
        mock_update_reviewer,
        mock_project_id,
        mock_existing_tokens,
        mock_sync_viewed,
    ):
        """Already reviewed and duplicate paths are excluded from the batch."""
        context = _make_context(reviewer_entry={"reviewedFiles": ["/src/first.ts"]})

        assert (
            mark_files_reviewed(
                ["src/first.ts", "src/second.ts", "src/second.ts"],
                pull_request_id=123,
                config=_make_config(),
                repo_id="repo-guid",
                cached_context=context,
            )
            is True
        )

        mock_update_reviewer.assert_called_once()
        assert mock_update_reviewer.call_args.args[-1] == ["/src/first.ts", "/src/second.ts"]
        mock_project_id.assert_called_once()
        mock_existing_tokens.assert_called_once()
        mock_sync_viewed.assert_called_once()

    def test_empty_batch_is_a_noop(self):
        """An empty batch returns successfully without requiring API context."""
        assert mark_files_reviewed([], 123, _make_config(), "repo-guid") is True
