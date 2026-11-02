"""Tests for approve_pull_request function."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools import state
from agentic_devtools.cli import azure_devops
from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig

# Use string paths for patching to ensure we patch the right location
COMMANDS_MODULE = "agentic_devtools.cli.azure_devops.commands"
# The fallback path in approve_pull_request() delegates to post_pr_comment(), which
# resolves require_requests/get_repository_id from its own module (helpers.py), not
# from commands.py, so fallback-path tests must patch this module instead.
HELPERS_MODULE = "agentic_devtools.cli.azure_devops.helpers"


@pytest.fixture(autouse=True)
def mock_pat_identity():
    with patch(
        "agentic_devtools.cli.azure_devops.finalization.identity.resolve_pat_identity",
        return_value="test-user",
    ):
        yield


class TestApprovePullRequest:
    """Tests for approve_pull_request command."""

    @pytest.mark.parametrize(
        ("kwargs", "message"),
        [
            ({"pull_request_id": True, "content": "LGTM!", "dry_run": False}, "positive integer"),
            ({"pull_request_id": "12345", "content": "LGTM!", "dry_run": False}, "positive integer"),
            ({"pull_request_id": 12345, "content": " ", "dry_run": False}, "content is required"),
            ({"pull_request_id": 12345, "content": 123, "dry_run": False}, "content is required"),
            ({"pull_request_id": 12345, "content": "LGTM!", "dry_run": "false"}, "dry_run must be a boolean"),
        ],
    )
    def test_explicit_arguments_are_validated(self, kwargs, message, clear_state_before):
        """Explicit approval arguments are validated before provider work."""
        with patch(f"{COMMANDS_MODULE}.update_review_narrative") as mock_update:
            with pytest.raises(ValueError, match=message):
                azure_devops.approve_pull_request(**kwargs)
        mock_update.assert_not_called()

    def test_dry_run(self, temp_state_dir, clear_state_before, capsys):
        """Test dry run output."""
        state.set_pull_request_id(12345)
        state.set_value("content", "LGTM!")
        state.set_dry_run(True)

        azure_devops.approve_pull_request()

        captured = capsys.readouterr()
        assert "[DRY RUN]" in captured.out

    def test_dry_run_mentions_review_narrative(self, temp_state_dir, clear_state_before, capsys):
        """Dry-run mentions that the Review Narrative will be updated."""
        state.set_pull_request_id(12345)
        state.set_value("content", "LGTM!")
        state.set_dry_run(True)

        azure_devops.approve_pull_request()

        captured = capsys.readouterr()
        assert "Review Narrative" in captured.out

    def test_dry_run_shows_content(self, temp_state_dir, clear_state_before, capsys):
        """Dry-run output includes the approval content."""
        state.set_pull_request_id(12345)
        state.set_value("content", "All criteria met!")
        state.set_dry_run(True)

        azure_devops.approve_pull_request()

        captured = capsys.readouterr()
        assert "All criteria met!" in captured.out

    def test_missing_pull_request_id(self, temp_state_dir, clear_state_before):
        """Test raises error when pull request ID is missing."""
        state.set_value("content", "LGTM!")
        with pytest.raises(KeyError, match="pull_request_id"):
            azure_devops.approve_pull_request()

    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    @patch(f"{HELPERS_MODULE}.require_requests")
    @patch(f"{HELPERS_MODULE}.get_repository_id")
    def test_explicit_config_mismatch_falls_back_to_new_comment(
        self, mock_get_repo, mock_requests, temp_state_dir, clear_state_before
    ):
        """A repository mismatch avoids stale thread IDs and posts a new PR comment."""
        from agentic_devtools.cli.azure_devops.review_state import FileEntry, OverallSummary, ReviewState

        mock_get_repo.return_value = "override-repo-guid"
        mock_req_module = MagicMock()
        mock_patch_response = MagicMock()
        mock_patch_response.json.return_value = {}
        mock_req_module.patch.return_value = mock_patch_response
        mock_post_response = MagicMock()
        mock_post_response.json.return_value = {"id": 123}
        mock_req_module.post.return_value = mock_post_response
        mock_requests.return_value = mock_req_module
        mock_req_module.get.return_value.json.return_value = {"value": []}

        review_state = ReviewState(
            prId=12345,
            repoId="stale-repo-guid",
            repoName="stale-repo-name",
            project="StaleProject",
            organization="https://dev.azure.com/stale-org",
            latestIterationId=1,
            scaffoldedUtc="2026-01-01T00:00:00Z",
            overallSummary=OverallSummary(threadId=99, commentId=1),
            files={
                "/src/app.py": FileEntry(threadId=10, commentId=1, folder="src", fileName="app.py", status="approved")
            },
        )

        with (
            patch(f"{COMMANDS_MODULE}.load_review_state", return_value=review_state),
            patch(f"{COMMANDS_MODULE}.save_review_state"),
        ):
            azure_devops.approve_pull_request(
                pull_request_id=12345,
                content="snapshotted content",
                dry_run=False,
                config=AzureDevOpsConfig(
                    organization="https://dev.azure.com/override-org",
                    project="OverrideProject",
                    repository="override-repo",
                ),
            )

        mock_get_repo.assert_called_once_with(
            "https://dev.azure.com/override-org",
            "OverrideProject",
            "override-repo",
        )
        patch_calls = mock_req_module.patch.call_args_list
        assert len(patch_calls) == 1
        assert "/threads/123" in patch_calls[0][0][0]
        post_call = mock_req_module.post.call_args
        assert "/repositories/override-repo-guid/" in post_call[0][0]
        assert post_call[1]["json"]["comments"][0]["content"].endswith("\nsnapshotted content")

    @pytest.mark.parametrize(
        ("stored_organization", "stored_project", "stored_repository", "config"),
        [
            (
                "https://dev.azure.com/example-org/",
                "My%20Project",
                "My%20Repo",
                AzureDevOpsConfig(
                    organization="https://dev.azure.com/example-org",
                    project="My Project",
                    repository="My Repo",
                ),
            ),
            (
                "https://dev.azure.com/example-org",
                "My Project",
                "My Repo",
                AzureDevOpsConfig(
                    organization="https://dev.azure.com/example-org/",
                    project="My%20Project",
                    repository="My%20Repo",
                ),
            ),
            (
                "https://dev.azure.com/Example-Org/",
                "My%20Project",
                "My%20Repo",
                AzureDevOpsConfig(
                    organization="https://dev.azure.com/example-org",
                    project="my project",
                    repository="my repo",
                ),
            ),
        ],
    )
    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    @patch(f"{COMMANDS_MODULE}.require_requests")
    @patch(f"{COMMANDS_MODULE}.get_repository_id")
    def test_equivalent_explicit_config_updates_review_narrative(
        self,
        mock_get_repo,
        mock_requests,
        stored_organization,
        stored_project,
        stored_repository,
        config,
        temp_state_dir,
        clear_state_before,
    ):
        """Equivalent Azure identifier spellings still update the existing narrative."""
        from agentic_devtools.cli.azure_devops.review_state import FileEntry, OverallSummary, ReviewState

        mock_get_repo.return_value = "repo-guid"
        mock_req_module = MagicMock()
        mock_requests.return_value = mock_req_module
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_req_module.patch.return_value = mock_response

        review_state = ReviewState(
            prId=12345,
            repoId="repo-guid",
            repoName=stored_repository,
            project=stored_project,
            organization=stored_organization,
            latestIterationId=1,
            scaffoldedUtc="2026-01-01T00:00:00Z",
            overallSummary=OverallSummary(threadId=99, commentId=1),
            files={
                "/src/app.py": FileEntry(threadId=10, commentId=1, folder="src", fileName="app.py", status="approved")
            },
        )

        with (
            patch(f"{COMMANDS_MODULE}.load_review_state", return_value=review_state),
            patch(f"{COMMANDS_MODULE}.save_review_state"),
        ):
            azure_devops.approve_pull_request(
                pull_request_id=12345,
                content="snapshotted content",
                dry_run=False,
                config=config,
            )

        mock_get_repo.assert_called_once_with(config.organization, config.project, config.repository)
        mock_req_module.patch.assert_called_once()
        mock_req_module.post.assert_not_called()


class TestApprovePullRequestActualCall:
    """Tests for approve_pull_request with mocked API calls."""

    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    @patch(f"{COMMANDS_MODULE}.require_requests")
    @patch(f"{COMMANDS_MODULE}.get_repository_id")
    def test_successful_approval_via_narrative_update(
        self, mock_get_repo, mock_requests, temp_state_dir, clear_state_before, capsys
    ):
        """Approval updates Review Narrative via patch when review state exists."""
        from agentic_devtools.cli.azure_devops.review_state import (
            FileEntry,
            OverallSummary,
            ReviewState,
        )

        mock_get_repo.return_value = "repo-guid-123"
        mock_req_module = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": 1, "content": "updated"}
        mock_req_module.patch.return_value = mock_response
        mock_requests.return_value = mock_req_module
        mock_req_module.get.return_value.json.return_value = {"value": []}

        review_state = ReviewState(
            prId=12345,
            repoId="repo-guid-123",
            repoName="example-repo-name",
            project="ExampleProject",
            organization="https://dev.azure.com/example-org",
            latestIterationId=1,
            scaffoldedUtc="2026-01-01T00:00:00Z",
            overallSummary=OverallSummary(threadId=99, commentId=1),
            files={
                "/src/app.py": FileEntry(threadId=10, commentId=1, folder="src", fileName="app.py", status="approved")
            },
        )

        state.set_pull_request_id(12345)
        state.set_value("content", "LGTM! All files reviewed.")

        with (
            patch(
                "agentic_devtools.cli.azure_devops.commands.load_review_state",
                return_value=review_state,
            ),
            patch("agentic_devtools.cli.azure_devops.commands.save_review_state"),
        ):
            outcome = azure_devops.approve_pull_request()

        # Should have called PATCH to update the summary comment
        assert mock_req_module.patch.called
        captured = capsys.readouterr()
        assert "Review Narrative updated successfully" in captured.out
        assert outcome == azure_devops.commands.AzureApprovalOutcome(
            resolved=True,
            thread_id=None,
            operation_kind="narrative_update",
        )

    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    @patch(f"{HELPERS_MODULE}.require_requests")
    @patch(f"{HELPERS_MODULE}.get_repository_id")
    def test_approval_falls_back_when_no_review_state(
        self, mock_get_repo, mock_requests, temp_state_dir, clear_state_before, capsys
    ):
        """Approval falls back to a new comment thread when review-state.json is missing."""
        mock_get_repo.return_value = "repo-guid-123"
        mock_req_module = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": 123}
        mock_req_module.post.return_value = mock_response
        mock_req_module.patch.return_value = mock_response
        mock_requests.return_value = mock_req_module
        mock_req_module.get.return_value.json.return_value = {"value": []}

        state.set_pull_request_id(12345)
        state.set_value("content", "LGTM!")

        with patch(
            "agentic_devtools.cli.azure_devops.commands.load_review_state",
            side_effect=FileNotFoundError("no review state"),
        ):
            outcome = azure_devops.approve_pull_request()

        # Should warn about narrative update failure and fall back to new comment
        captured = capsys.readouterr()
        assert "Could not update Review Narrative" in captured.err
        assert "Comment added successfully" in captured.out
        assert outcome == azure_devops.commands.AzureApprovalOutcome(
            resolved=True,
            thread_id=123,
            operation_kind="fallback_comment",
        )

    def test_review_narrative_file_not_found_uses_fallback(self, temp_state_dir, clear_state_before):
        """Any narrative update failure preserves the fallback approval path."""
        state.set_pull_request_id(12345)
        state.set_value("content", "LGTM!")

        with (
            patch(
                "agentic_devtools.cli.azure_devops.commands.update_review_narrative",
                side_effect=FileNotFoundError("missing local file"),
            ),
            patch("agentic_devtools.cli.azure_devops.commands.post_pr_comment", return_value=77) as mock_post,
        ):
            outcome = azure_devops.approve_pull_request()

        assert outcome == azure_devops.commands.AzureApprovalOutcome(
            resolved=True,
            thread_id=77,
            operation_kind="fallback_comment",
        )
        mock_post.assert_called_once()

    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    def test_approving_another_pr_preserves_existing_review_state(self, tmp_path, temp_state_dir, clear_state_before):
        """Approving PR B falls back without deleting PR A's review-state artifact."""
        import json

        from agentic_devtools.cli.azure_devops.review_state import (
            FileEntry,
            OverallSummary,
            ReviewState,
            get_review_state_file_path,
        )

        review_state = ReviewState(
            prId=12345,
            repoId="repo-guid-123",
            repoName="example-repo-name",
            project="ExampleProject",
            organization="https://dev.azure.com/example-org",
            latestIterationId=1,
            scaffoldedUtc="2026-01-01T00:00:00Z",
            overallSummary=OverallSummary(threadId=99, commentId=1),
            files={
                "/src/app.py": FileEntry(threadId=10, commentId=1, folder="src", fileName="app.py", status="approved")
            },
        )
        with patch(
            "agentic_devtools.cli.azure_devops.review_state.get_state_dir",
            return_value=tmp_path,
        ):
            state_file = get_review_state_file_path(12345)
            state_file.parent.mkdir(parents=True)
            state_file.write_text(json.dumps(review_state.to_dict()), encoding="utf-8")
            with (
                patch(f"{COMMANDS_MODULE}.require_requests", return_value=MagicMock()),
                patch(f"{COMMANDS_MODULE}.post_pr_comment", return_value=77) as mock_post,
            ):
                outcome = azure_devops.approve_pull_request(
                    pull_request_id=67890,
                    content="snapshotted content",
                    dry_run=False,
                    config=AzureDevOpsConfig(
                        organization="https://dev.azure.com/example-org",
                        project="ExampleProject",
                        repository="example-repo-name",
                    ),
                )

            assert json.loads(state_file.read_text(encoding="utf-8"))["prId"] == 12345

        mock_post.assert_called_once()
        assert outcome == azure_devops.commands.AzureApprovalOutcome(
            resolved=True,
            thread_id=77,
            operation_kind="fallback_comment",
        )

    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "secret-pat"})
    def test_fallback_warning_redacts_provider_credentials(self, temp_state_dir, clear_state_before, capsys):
        """Fallback warnings redact credentials embedded in provider exceptions."""
        state.set_pull_request_id(12345)
        state.set_value("content", "LGTM!")

        with (
            patch(
                f"{COMMANDS_MODULE}.update_review_narrative",
                side_effect=RuntimeError("request failed with secret-pat"),
            ),
            patch(f"{COMMANDS_MODULE}.post_pr_comment", return_value=77),
        ):
            azure_devops.approve_pull_request()

        assert "secret-pat" not in capsys.readouterr().err

    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    @patch(f"{HELPERS_MODULE}.require_requests")
    @patch(f"{HELPERS_MODULE}.get_repository_id")
    def test_plain_review_state_file_not_found_still_falls_back(
        self, mock_get_repo, mock_requests, temp_state_dir, clear_state_before, capsys
    ):
        """Legacy missing-review-state FileNotFoundError messages still use the fallback path."""
        mock_get_repo.return_value = "repo-guid-123"
        mock_req_module = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": 123}
        mock_req_module.post.return_value = mock_response
        mock_req_module.patch.return_value = mock_response
        mock_requests.return_value = mock_req_module
        mock_req_module.get.return_value.json.return_value = {"value": []}

        state.set_pull_request_id(12345)
        state.set_value("content", "LGTM!")

        with patch(
            "agentic_devtools.cli.azure_devops.commands.update_review_narrative",
            side_effect=FileNotFoundError("Review state not found for PR 12345: /tmp/review-state.json"),
        ):
            outcome = azure_devops.approve_pull_request()

        captured = capsys.readouterr()
        assert "Could not update Review Narrative" in captured.err
        assert "Comment added successfully" in captured.out
        assert outcome == azure_devops.commands.AzureApprovalOutcome(
            resolved=True,
            thread_id=123,
            operation_kind="fallback_comment",
        )

    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    @patch(f"{HELPERS_MODULE}.require_requests")
    @patch(f"{HELPERS_MODULE}.get_repository_id")
    def test_approval_fallback_clears_stale_path(
        self, mock_get_repo, mock_requests, temp_state_dir, clear_state_before
    ):
        """Fallback add_pull_request_comment posts PR-level (no file context) because path is cleared."""
        mock_get_repo.return_value = "repo-guid-123"
        mock_req_module = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": 123}
        mock_req_module.post.return_value = mock_response
        mock_req_module.patch.return_value = mock_response
        mock_requests.return_value = mock_req_module
        mock_req_module.get.return_value.json.return_value = {"value": []}

        state.set_pull_request_id(12345)
        state.set_value("content", "LGTM!")
        # Stale path from a previous file-review operation
        state.set_value("path", "src/reviewed_file.py")
        state.set_value("line", 10)

        with patch(
            "agentic_devtools.cli.azure_devops.commands.load_review_state",
            side_effect=FileNotFoundError("no review state"),
        ):
            azure_devops.approve_pull_request()

        # The fallback thread should have no file context
        post_call = mock_req_module.post.call_args_list[-1]
        body = post_call[1]["json"]
        assert "threadContext" not in body

    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    @patch(f"{HELPERS_MODULE}.require_requests")
    @patch(f"{HELPERS_MODULE}.get_repository_id")
    def test_snapshot_arguments_override_mutable_state(
        self, mock_get_repo, mock_requests, temp_state_dir, clear_state_before
    ):
        """Explicit snapshot arguments drive the fallback approval flow."""
        mock_get_repo.return_value = "repo-guid-123"
        mock_req_module = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": 123}
        mock_req_module.post.return_value = mock_response
        mock_requests.return_value = mock_req_module
        mock_req_module.get.return_value.json.return_value = {"value": []}

        state.set_pull_request_id(99999)
        state.set_value("content", "stale state content")
        state.set_value("path", "src/reviewed_file.py")
        state.set_value("line", 10)

        config = AzureDevOpsConfig(
            organization="https://dev.azure.com/example-org",
            project="ExampleProject",
            repository="snapshot-repo",
        )

        with patch(
            "agentic_devtools.cli.azure_devops.commands.load_review_state",
            side_effect=FileNotFoundError("no review state"),
        ):
            azure_devops.approve_pull_request(
                pull_request_id=12345,
                content="snapshotted content",
                dry_run=False,
                config=config,
            )

        mock_get_repo.assert_called_once_with(
            "https://dev.azure.com/example-org",
            "ExampleProject",
            "snapshot-repo",
        )
        post_call = mock_req_module.post.call_args_list[-1]
        assert "/pullRequests/12345/threads" in post_call[0][0]
        body = post_call[1]["json"]
        assert body["comments"][0]["content"].endswith("\nsnapshotted content")
        assert "threadContext" not in body
        assert state.get_value("path") == "src/reviewed_file.py"

    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    @patch(f"{HELPERS_MODULE}.require_requests")
    @patch(f"{HELPERS_MODULE}.get_repository_id")
    def test_snapshot_fallback_raises_without_valid_thread_id(
        self, mock_get_repo, mock_requests, temp_state_dir, clear_state_before
    ):
        """Fallback comment creation raises instead of silently skipping resolution.

        A successful HTTP response missing a valid positive-integer thread ``id``
        must not be treated as a completed approval: the thread was never resolved,
        so the task should fail loudly rather than report success.
        """
        mock_get_repo.return_value = "repo-guid-123"
        mock_req_module = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_req_module.post.return_value = mock_response
        mock_requests.return_value = mock_req_module
        mock_req_module.get.return_value.json.return_value = {"value": []}

        with (
            patch(
                "agentic_devtools.cli.azure_devops.commands.load_review_state",
                side_effect=FileNotFoundError("no review state"),
            ),
            pytest.raises(RuntimeError, match="positive integer"),
        ):
            azure_devops.approve_pull_request(
                pull_request_id=12345,
                content="snapshotted content",
                dry_run=False,
                config=AzureDevOpsConfig(
                    organization="https://dev.azure.com/example-org",
                    project="ExampleProject",
                    repository="snapshot-repo",
                ),
            )

        mock_req_module.patch.assert_not_called()

    def test_fallback_resolve_failure_returns_unresolved_outcome(self, temp_state_dir, clear_state_before, capsys):
        """A PrCommentResolveFailedError from the fallback path becomes a resolved=False outcome.

        The comment was already posted, so the failure must not be swallowed into a
        plain success nor re-raised (which would risk a duplicate repost on retry);
        it must be reported as a distinct partial outcome carrying the thread ID.
        """
        from agentic_devtools.cli.azure_devops.commands import AzureApprovalOutcome
        from agentic_devtools.cli.azure_devops.helpers import PrCommentResolveFailedError

        state.set_pull_request_id(12345)
        state.set_value("content", "LGTM!")

        with (
            patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"}),
            patch(
                "agentic_devtools.cli.azure_devops.commands.load_review_state",
                side_effect=FileNotFoundError("no review state"),
            ),
            patch(
                "agentic_devtools.cli.azure_devops.commands.post_pr_comment",
                side_effect=PrCommentResolveFailedError(77, "Comment posted (thread 77) but resolving it failed"),
            ),
        ):
            outcome = azure_devops.approve_pull_request()

        assert outcome == AzureApprovalOutcome(resolved=False, thread_id=77, operation_kind="fallback_comment")
        captured = capsys.readouterr()
        assert "Leaving the thread active" in captured.err

    def test_review_narrative_failure_uses_fallback(self, temp_state_dir, clear_state_before):
        """Operational narrative failures preserve the documented fallback behavior."""
        state.set_pull_request_id(12345)
        state.set_value("content", "LGTM!")

        with (
            patch(
                "agentic_devtools.cli.azure_devops.commands.update_review_narrative",
                side_effect=RuntimeError("auth failed"),
            ),
            patch("agentic_devtools.cli.azure_devops.commands.post_pr_comment", return_value=77) as mock_post,
        ):
            outcome = azure_devops.approve_pull_request()

        assert outcome == azure_devops.commands.AzureApprovalOutcome(
            resolved=True,
            thread_id=77,
            operation_kind="fallback_comment",
        )
        mock_post.assert_called_once()

    def test_review_narrative_value_error_uses_fallback(self, temp_state_dir, clear_state_before):
        """Narrative validation failures preserve the documented fallback behavior."""
        state.set_pull_request_id(12345)
        state.set_value("content", "LGTM!")

        with (
            patch(
                "agentic_devtools.cli.azure_devops.commands.update_review_narrative",
                side_effect=ValueError("bad payload"),
            ),
            patch("agentic_devtools.cli.azure_devops.commands.post_pr_comment", return_value=77) as mock_post,
        ):
            outcome = azure_devops.approve_pull_request()

        assert outcome == azure_devops.commands.AzureApprovalOutcome(
            resolved=True,
            thread_id=77,
            operation_kind="fallback_comment",
        )
        mock_post.assert_called_once()

    def test_update_review_narrative_uses_resolved_config_snapshot(self, temp_state_dir, clear_state_before) -> None:
        """Narrative updates reuse the already-resolved config instead of mutable global state."""
        state.set_pull_request_id(12345)
        state.set_value("content", "LGTM!")
        state.set_value("repository", "stale-state-repo")

        config = AzureDevOpsConfig(
            organization="https://dev.azure.com/example-org",
            project="ExampleProject",
            repository="snapshot-repo",
        )

        with (
            patch("agentic_devtools.cli.azure_devops.commands.update_review_narrative") as mock_update,
            patch("agentic_devtools.cli.azure_devops.commands.post_pr_comment") as mock_post,
        ):
            outcome = azure_devops.approve_pull_request(config=config)

        assert outcome == azure_devops.commands.AzureApprovalOutcome(
            resolved=True,
            thread_id=None,
            operation_kind="narrative_update",
        )
        mock_update.assert_called_once_with(12345, "LGTM!", config=config)
        mock_post.assert_not_called()
