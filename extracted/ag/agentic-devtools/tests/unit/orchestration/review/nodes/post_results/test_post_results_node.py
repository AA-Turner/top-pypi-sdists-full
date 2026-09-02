"""Tests for post_results_node()."""

from __future__ import annotations

import json
from contextlib import nullcontext
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.azure_devops.review_state import (
    FileEntry,
    OverallSummary,
    ReviewSession,
    ReviewState,
    ReviewStatus,
    SuggestionEntry,
)
from agentic_devtools.orchestration.review.nodes.post_results import (
    _post_consolidated_comment,
    _post_line_comment,
    _post_suggestion_threads,
    _update_final_review_state,
    post_results_node,
)


def _make_review_state(files: dict | None = None) -> ReviewState:
    return ReviewState(
        prId=123,
        repoId="repo-guid",
        repoName="test-repo",
        project="TestProject",
        organization="https://dev.azure.com/org",
        latestIterationId=1,
        scaffoldedUtc="2024-01-01T00:00:00+00:00",
        overallSummary=OverallSummary(threadId=1, commentId=1, status=ReviewStatus.UNREVIEWED.value),
        files=files or {},
    )


def _make_file_entry(status: str) -> FileEntry:
    return FileEntry(threadId=1, commentId=1, folder="src", fileName="main.py", status=status)


class TestPostResultsNode:
    """Tests for the post_results node."""

    def test_produces_structured_output(self, capsys) -> None:
        """Prints structured JSON output to stdout (NFR-003)."""
        post_results_node(
            {
                "file_results": [
                    {
                        "outcome": "approve",
                        "summary": "OK",
                        "file_path": "/src/a.py",
                        "suggestions": [],
                    },
                ],
                "overall_decision": "approve",
                "summary": "All good",
            }
        )

        output = json.loads(capsys.readouterr().out)
        assert output["status"] == "completed"
        assert output["decision"] == "approve"
        assert output["files_reviewed"] == 1

    def test_handles_missing_pr_id(self) -> None:
        """Handles gracefully when pr_id is missing."""
        result = post_results_node(
            {
                "file_results": [],
                "overall_decision": "approve",
                "summary": "No files",
            }
        )
        assert result["errors"] == []

    def test_upstream_errors_appear_in_stdout_summary(self, capsys) -> None:
        """Upstream pipeline errors from state['errors'] are included in the stdout JSON summary."""
        post_results_node(
            {
                "file_results": [],
                "overall_decision": "approve",
                "summary": "Done",
                "errors": ["fetch_pr_details: auth failure", "scaffold_comments: API timeout"],
            }
        )

        output = json.loads(capsys.readouterr().out)
        assert "fetch_pr_details: auth failure" in output["errors"]
        assert "scaffold_comments: API timeout" in output["errors"]

    def test_upstream_errors_combined_with_local_errors_in_stdout(self, capsys) -> None:
        """Both upstream and local post_results errors appear in the stdout JSON summary."""
        with patch(
            "agentic_devtools.orchestration.review.nodes.post_results._update_final_review_state",
            side_effect=RuntimeError("state update failure"),
        ):
            post_results_node(
                {
                    "file_results": [],
                    "overall_decision": "approve",
                    "summary": "Done",
                    "pr_id": 123,
                    "errors": ["upstream: some earlier node failed"],
                }
            )

        output = json.loads(capsys.readouterr().out)
        assert "upstream: some earlier node failed" in output["errors"]
        assert any("failed to update review state" in e for e in output["errors"])

    def test_upstream_errors_not_added_to_return_value(self) -> None:
        """Upstream errors do not pollute the state delta returned by post_results_node."""
        result = post_results_node(
            {
                "file_results": [],
                "overall_decision": "approve",
                "summary": "Done",
                "errors": ["upstream: earlier node error"],
            }
        )
        # The return value only adds new post_results errors (not upstream ones),
        # because LangGraph's Annotated[list, operator.add] reducer will re-append
        # the upstream errors if they are included here.
        assert result["errors"] == []

    @patch("agentic_devtools.orchestration.review.nodes.post_results._update_final_review_state")
    def test_updates_review_state_when_pr_id_present(self, mock_update) -> None:
        """Calls _update_final_review_state when pr_id is set."""
        post_results_node(
            {
                "file_results": [],
                "overall_decision": "approve",
                "summary": "Done",
                "pr_id": 123,
            }
        )

        mock_update.assert_called_once_with(
            pr_id=123,
            file_results=[],
            overall_decision="approve",
            summary="Done",
        )

    @patch(
        "agentic_devtools.orchestration.review.nodes.post_results._update_final_review_state",
        side_effect=RuntimeError("boom"),
    )
    def test_captures_review_state_update_error(self, mock_update) -> None:
        """Captures error when review state update fails."""
        result = post_results_node(
            {
                "file_results": [],
                "overall_decision": "approve",
                "summary": "Done",
                "pr_id": 123,
            }
        )

        assert len(result["errors"]) == 1
        assert "failed to update review state" in result["errors"][0]

    @patch("agentic_devtools.orchestration.review.nodes.post_results._post_suggestion_threads")
    @patch("agentic_devtools.orchestration.review.nodes.post_results._post_consolidated_comment")
    @patch("agentic_devtools.orchestration.review.nodes.post_results._update_final_review_state")
    def test_posts_to_ado_when_all_params_present(
        self,
        mock_update,
        mock_post,
        mock_suggest,
    ) -> None:
        """Posts consolidated comment when all ADO params present."""
        post_results_node(
            {
                "file_results": [],
                "overall_decision": "approve",
                "summary": "Done",
                "pr_id": 123,
                "organization": "https://dev.azure.com/org",
                "project": "MyProject",
                "repo_id": "repo-guid",
            }
        )

        mock_post.assert_called_once()
        mock_suggest.assert_called_once()

    @patch("agentic_devtools.orchestration.review.nodes.post_results._post_suggestion_threads")
    @patch("agentic_devtools.orchestration.review.nodes.post_results._post_consolidated_comment")
    @patch("agentic_devtools.orchestration.review.nodes.post_results._update_final_review_state")
    def test_suggestion_threads_posted_before_consolidated_comment(
        self,
        mock_update,
        mock_consolidated,
        mock_suggestions,
    ) -> None:
        """Suggestion threads are posted and persisted before the consolidated comment is rendered.

        The consolidated renderer sources suggestions from review-state.json, so
        _post_suggestion_threads must run before _post_consolidated_comment to ensure
        the consolidated comment includes all suggestion thread IDs.
        """
        call_order: list[str] = []
        mock_suggestions.side_effect = lambda **_kw: call_order.append("suggestions")
        mock_consolidated.side_effect = lambda **_kw: call_order.append("consolidated")

        post_results_node(
            {
                "file_results": [],
                "overall_decision": "approve",
                "summary": "Done",
                "pr_id": 123,
                "organization": "https://dev.azure.com/org",
                "project": "MyProject",
                "repo_id": "repo-guid",
            }
        )

        assert call_order == ["suggestions", "consolidated"]

    @patch("agentic_devtools.orchestration.review.nodes.post_results._post_suggestion_threads")
    @patch(
        "agentic_devtools.orchestration.review.nodes.post_results._post_consolidated_comment",
        side_effect=RuntimeError("API error"),
    )
    @patch("agentic_devtools.orchestration.review.nodes.post_results._update_final_review_state")
    def test_captures_consolidated_comment_error(self, mock_update, mock_post, mock_suggest) -> None:
        """Captures error when posting consolidated comment fails."""
        result = post_results_node(
            {
                "file_results": [],
                "overall_decision": "approve",
                "summary": "Done",
                "pr_id": 123,
                "organization": "https://dev.azure.com/org",
                "project": "MyProject",
                "repo_id": "repo-guid",
            }
        )

        assert any("failed to post consolidated comment" in error for error in result["errors"])

    @patch(
        "agentic_devtools.orchestration.review.nodes.post_results._post_suggestion_threads",
        side_effect=RuntimeError("thread error"),
    )
    @patch("agentic_devtools.orchestration.review.nodes.post_results._post_consolidated_comment")
    @patch("agentic_devtools.orchestration.review.nodes.post_results._update_final_review_state")
    def test_captures_suggestion_threads_error(
        self,
        mock_update,
        mock_post,
        mock_suggest,
    ) -> None:
        """Captures error when posting suggestion threads fails; consolidated comment still runs."""
        result = post_results_node(
            {
                "file_results": [],
                "overall_decision": "request-changes",
                "summary": "Issues found",
                "pr_id": 456,
                "organization": "https://dev.azure.com/org",
                "project": "MyProject",
                "repo_id": "repo-guid",
            }
        )

        assert any("failed to post suggestion threads" in error for error in result["errors"])
        # Consolidated comment is attempted even when suggestion threads fail
        mock_post.assert_called_once()


class TestUpdateFinalReviewState:
    """Tests for _update_final_review_state()."""

    @patch("agentic_devtools.cli.azure_devops.review_state.save_review_state")
    @patch("agentic_devtools.cli.azure_devops.review_state.load_review_state")
    def test_sets_approved_status(self, mock_load, mock_save) -> None:
        """Overall status is derived as approved when all files are approved."""
        review_state = _make_review_state(files={"/src/a.py": _make_file_entry(ReviewStatus.APPROVED.value)})
        mock_load.return_value = review_state

        _update_final_review_state(pr_id=123, file_results=[], overall_decision="approve")

        assert review_state.overallSummary.status == ReviewStatus.APPROVED.value
        mock_save.assert_called_once_with(review_state)

    @patch("agentic_devtools.cli.azure_devops.review_state.save_review_state")
    @patch("agentic_devtools.cli.azure_devops.review_state.load_review_state")
    def test_sets_needs_work_when_any_file_needs_work(self, mock_load, mock_save) -> None:
        """Overall status is derived as needs-work when any file has that status."""
        review_state = _make_review_state(files={"/src/a.py": _make_file_entry(ReviewStatus.NEEDS_WORK.value)})
        mock_load.return_value = review_state

        _update_final_review_state(
            pr_id=123,
            file_results=[],
            overall_decision="request-changes",
        )

        assert review_state.overallSummary.status == ReviewStatus.NEEDS_WORK.value
        mock_save.assert_called_once_with(review_state)

    @patch("agentic_devtools.cli.azure_devops.review_state.save_review_state")
    @patch("agentic_devtools.cli.azure_devops.review_state.load_review_state")
    def test_derives_status_from_files_not_decision(self, mock_load, mock_save) -> None:
        """File-level needs-work is preserved even when decision says approve."""
        # File says needs-work; decision says approve — file status wins (policy cannot loosen).
        review_state = _make_review_state(files={"/src/a.py": _make_file_entry(ReviewStatus.NEEDS_WORK.value)})
        mock_load.return_value = review_state

        _update_final_review_state(pr_id=123, file_results=[], overall_decision="approve")

        assert review_state.overallSummary.status == ReviewStatus.NEEDS_WORK.value
        mock_save.assert_called_once_with(review_state)

    @patch("agentic_devtools.cli.azure_devops.review_state.save_review_state")
    @patch("agentic_devtools.cli.azure_devops.review_state.load_review_state")
    def test_policy_decision_tightens_approved_status(self, mock_load, mock_save) -> None:
        """Policy request-changes overrides approved file statuses to needs-work."""
        # All files approved; policy says request-changes — policy wins (tightens status).
        review_state = _make_review_state(files={"/src/a.py": _make_file_entry(ReviewStatus.APPROVED.value)})
        mock_load.return_value = review_state

        _update_final_review_state(pr_id=123, file_results=[], overall_decision="request-changes")

        assert review_state.overallSummary.status == ReviewStatus.NEEDS_WORK.value
        mock_save.assert_called_once_with(review_state)

    @patch("agentic_devtools.cli.azure_devops.review_state.save_review_state")
    @patch("agentic_devtools.cli.azure_devops.review_state.load_review_state")
    def test_persists_narrative_summary(self, mock_load, mock_save) -> None:
        """Graph-level review summary is saved for consolidated comment rendering."""
        review_state = _make_review_state(files={"/src/a.py": _make_file_entry(ReviewStatus.APPROVED.value)})
        mock_load.return_value = review_state

        _update_final_review_state(
            pr_id=123,
            file_results=[],
            overall_decision="approve",
            summary="Reviewed 1 file: approved.",
        )

        assert review_state.overallSummary.narrativeSummary == "Reviewed 1 file: approved."
        mock_save.assert_called_once_with(review_state)

    @patch("agentic_devtools.cli.azure_devops.review_state.save_review_state")
    @patch("agentic_devtools.cli.azure_devops.review_state.load_review_state")
    def test_promotes_single_effective_model_to_review_state_and_active_session(self, mock_load, mock_save) -> None:
        """A single effective served model updates the global attribution fields."""
        review_state = _make_review_state(files={"/src/a.py": _make_file_entry(ReviewStatus.APPROVED.value)})
        review_state.modelId = "requested-model"
        review_state.sessions = [
            ReviewSession(
                sessionId="session-1",
                modelId="requested-model",
                startedUtc="2024-01-01T00:00:00+00:00",
                status="in_progress",
            )
        ]
        mock_load.return_value = review_state

        _update_final_review_state(
            pr_id=123,
            file_results=[{"file_path": "/src/a.py", "model_id": "canonical-model"}],
            overall_decision="approve",
        )

        assert review_state.modelId == "canonical-model"
        assert review_state.sessions[0].modelId == "canonical-model"
        mock_save.assert_called_once_with(review_state)

    @patch("agentic_devtools.cli.azure_devops.review_state.save_review_state")
    @patch("agentic_devtools.cli.azure_devops.review_state.load_review_state")
    def test_keeps_scaffolded_model_when_file_results_use_multiple_models(self, mock_load, mock_save) -> None:
        """Mixed per-file routing keeps the scaffolded global model attribution."""
        review_state = _make_review_state(files={"/src/a.py": _make_file_entry(ReviewStatus.APPROVED.value)})
        review_state.modelId = "requested-model"
        review_state.sessions = [
            ReviewSession(
                sessionId="session-1",
                modelId="requested-model",
                startedUtc="2024-01-01T00:00:00+00:00",
                status="in_progress",
            )
        ]
        mock_load.return_value = review_state

        _update_final_review_state(
            pr_id=123,
            file_results=[
                {"file_path": "/src/a.py", "model_id": "canonical-model"},
                {"file_path": "/src/b.py", "model_id": "other-model"},
            ],
            overall_decision="approve",
        )

        assert review_state.modelId == "requested-model"
        assert review_state.sessions[0].modelId == "requested-model"
        mock_save.assert_called_once_with(review_state)

    @patch("agentic_devtools.cli.azure_devops.review_state.save_review_state")
    @patch("agentic_devtools.cli.azure_devops.review_state.load_review_state")
    def test_keeps_scaffolded_model_when_any_file_result_has_no_model(self, mock_load, mock_save) -> None:
        """Global attribution is not promoted when any file result lacks an effective model."""
        review_state = _make_review_state(files={"/src/a.py": _make_file_entry(ReviewStatus.APPROVED.value)})
        review_state.modelId = "requested-model"
        review_state.sessions = [
            ReviewSession(
                sessionId="session-1",
                modelId="requested-model",
                startedUtc="2024-01-01T00:00:00+00:00",
                status="in_progress",
            )
        ]
        mock_load.return_value = review_state

        _update_final_review_state(
            pr_id=123,
            file_results=[
                {"file_path": "/src/a.py", "model_id": "canonical-model"},
                {"file_path": "/src/b.py", "model_id": None},
            ],
            overall_decision="approve",
        )

        assert review_state.modelId == "requested-model"
        assert review_state.sessions[0].modelId == "requested-model"
        mock_save.assert_called_once_with(review_state)

    @patch("agentic_devtools.cli.azure_devops.review_state.save_review_state")
    @patch("agentic_devtools.cli.azure_devops.review_state.load_review_state")
    def test_effective_model_skips_terminal_sessions(self, mock_load, mock_save) -> None:
        """Only in-progress sessions are rewritten during attribution promotion."""
        review_state = _make_review_state(files={"/src/a.py": _make_file_entry(ReviewStatus.APPROVED.value)})
        review_state.modelId = "requested-model"
        review_state.sessions = [
            ReviewSession(
                sessionId="session-1",
                modelId="requested-model",
                startedUtc="2024-01-01T00:00:00+00:00",
                status="completed",
            ),
            ReviewSession(
                sessionId="session-2",
                modelId="requested-model",
                startedUtc="2024-01-01T00:00:00+00:00",
                status="in_progress",
            ),
        ]
        mock_load.return_value = review_state

        _update_final_review_state(
            pr_id=123,
            file_results=[{"file_path": "/src/a.py", "model_id": "canonical-model"}],
            overall_decision="approve",
        )

        assert review_state.sessions[0].modelId == "requested-model"
        assert review_state.sessions[1].modelId == "canonical-model"
        mock_save.assert_called_once_with(review_state)

    @patch("agentic_devtools.cli.azure_devops.review_state.save_review_state")
    @patch("agentic_devtools.cli.azure_devops.review_state.load_review_state")
    def test_effective_model_keeps_global_model_when_no_session_is_in_progress(self, mock_load, mock_save) -> None:
        """Global attribution still updates even when there is no active session to rewrite."""
        review_state = _make_review_state(files={"/src/a.py": _make_file_entry(ReviewStatus.APPROVED.value)})
        review_state.modelId = "requested-model"
        review_state.sessions = [
            ReviewSession(
                sessionId="session-1",
                modelId="requested-model",
                startedUtc="2024-01-01T00:00:00+00:00",
                status="completed",
            )
        ]
        mock_load.return_value = review_state

        _update_final_review_state(
            pr_id=123,
            file_results=[{"file_path": "/src/a.py", "model_id": "canonical-model"}],
            overall_decision="approve",
        )

        assert review_state.modelId == "canonical-model"
        assert review_state.sessions[0].modelId == "requested-model"
        mock_save.assert_called_once_with(review_state)

    @patch("agentic_devtools.cli.azure_devops.review_state.save_review_state")
    @patch("agentic_devtools.cli.azure_devops.review_state.load_review_state")
    def test_migrates_commit_comment_model_ref_when_effective_model_differs(self, mock_load, mock_save) -> None:
        """Commit registry ref is renamed to the effective model to avoid a duplicate entry.

        When the provider returns a model identifier that differs from the
        scaffolded/requested model (e.g. an alias resolves to a canonical name),
        the existing ModelCommentRef in commitComments must be renamed before
        _sync_commit_registry runs so it upserts into the *same* ref rather
        than appending a new one, which would otherwise render as two model
        reviews for a single run.
        """
        from agentic_devtools.cli.azure_devops.review_state import CommitComment, ModelCommentRef

        review_state = _make_review_state(files={"/src/a.py": _make_file_entry(ReviewStatus.APPROVED.value)})
        review_state.modelId = "requested-model"
        review_state.commitHash = "abc123"
        commit_entry = CommitComment(commitHash="abc123", threadId=1)
        ref = ModelCommentRef(modelId="requested-model", commentId=42)
        commit_entry.models.append(ref)
        review_state.commitComments = {"abc123": commit_entry}
        mock_load.return_value = review_state

        _update_final_review_state(
            pr_id=123,
            file_results=[{"file_path": "/src/a.py", "model_id": "canonical-model"}],
            overall_decision="approve",
        )

        assert review_state.modelId == "canonical-model"
        assert commit_entry.get_model("requested-model") is None
        renamed = commit_entry.get_model("canonical-model")
        assert renamed is not None
        assert renamed.commentId == 42
        mock_save.assert_called_once_with(review_state)

    @patch("agentic_devtools.cli.azure_devops.review_state.save_review_state")
    @patch("agentic_devtools.cli.azure_devops.review_state.load_review_state")
    def test_migration_prefers_scaffolded_session_over_newer_unrelated_session(self, mock_load, mock_save) -> None:
        """Migration does not consume another active model's current-commit ref."""
        from agentic_devtools.cli.azure_devops.review_state import CommitComment, ModelCommentRef

        review_state = _make_review_state(files={"/src/a.py": _make_file_entry(ReviewStatus.APPROVED.value)})
        review_state.modelId = "requested-model"
        review_state.commitHash = "abc123"
        review_state.sessions = [
            ReviewSession(
                sessionId="scaffolded-model",
                modelId="requested-model",
                startedUtc="2024-01-01T00:00:00+00:00",
                status="in_progress",
                commitHash="abc123",
            ),
            ReviewSession(
                sessionId="unrelated-model",
                modelId="unrelated-model",
                startedUtc="2024-01-01T00:01:00+00:00",
                status="in_progress",
                commitHash="abc123",
            ),
        ]
        commit_entry = CommitComment(commitHash="abc123", threadId=1)
        requested_ref = ModelCommentRef(modelId="requested-model", commentId=42)
        unrelated_ref = ModelCommentRef(modelId="unrelated-model", commentId=77)
        commit_entry.models.extend([requested_ref, unrelated_ref])
        review_state.commitComments = {"abc123": commit_entry}
        mock_load.return_value = review_state

        _update_final_review_state(
            pr_id=123,
            file_results=[{"file_path": "/src/a.py", "model_id": "canonical-model"}],
            overall_decision="approve",
        )

        assert commit_entry.get_model("requested-model") is None
        migrated = commit_entry.get_model("canonical-model")
        assert migrated is requested_ref
        assert migrated.commentId == 42
        assert commit_entry.get_model("unrelated-model") is unrelated_ref
        mock_save.assert_called_once_with(review_state)

    @patch("agentic_devtools.cli.azure_devops.review_state.save_review_state")
    @patch("agentic_devtools.cli.azure_devops.review_state.load_review_state")
    def test_migration_without_scaffolded_model_does_not_select_active_alias(self, mock_load, mock_save) -> None:
        """Migration does not infer a source ref when no scaffolded model exists."""
        from agentic_devtools.cli.azure_devops.review_state import CommitComment, ModelCommentRef

        review_state = _make_review_state(files={"/src/a.py": _make_file_entry(ReviewStatus.APPROVED.value)})
        review_state.modelId = None
        review_state.commitHash = "abc123"
        review_state.sessions = [
            ReviewSession(
                sessionId="active-model",
                modelId="active-model",
                startedUtc="2024-01-01T00:00:00+00:00",
                status="in_progress",
                commitHash="abc123",
            )
        ]
        commit_entry = CommitComment(commitHash="abc123", threadId=1)
        active_ref = ModelCommentRef(modelId="active-model", commentId=77)
        commit_entry.models.append(active_ref)
        review_state.commitComments = {"abc123": commit_entry}
        mock_load.return_value = review_state

        _update_final_review_state(
            pr_id=123,
            file_results=[{"file_path": "/src/a.py", "model_id": "canonical-model"}],
            overall_decision="approve",
        )

        assert commit_entry.get_model("active-model") is active_ref
        assert commit_entry.get_model("canonical-model") is None
        mock_save.assert_called_once_with(review_state)

    @patch("agentic_devtools.cli.azure_devops.review_state.save_review_state")
    @patch("agentic_devtools.cli.azure_devops.review_state.load_review_state")
    def test_alias_fallback_excludes_normalized_scaffolded_model(self, mock_load, mock_save) -> None:
        """Alias fallback does not re-select a scaffolded model with surrounding whitespace."""
        from agentic_devtools.cli.azure_devops.review_state import CommitComment, ModelCommentRef

        review_state = _make_review_state(files={"/src/a.py": _make_file_entry(ReviewStatus.APPROVED.value)})
        review_state.modelId = "requested-model"
        review_state.commitHash = "abc123"
        review_state.sessions = [
            ReviewSession(
                sessionId="scaffolded-model",
                modelId=" requested-model ",
                startedUtc="2024-01-01T00:00:00+00:00",
                status="in_progress",
                commitHash="abc123",
            )
        ]
        commit_entry = CommitComment(commitHash="abc123", threadId=1)
        requested_ref = ModelCommentRef(modelId="requested-model", commentId=42)
        commit_entry.models.append(requested_ref)
        review_state.commitComments = {"abc123": commit_entry}
        mock_load.return_value = review_state

        _update_final_review_state(
            pr_id=123,
            file_results=[{"file_path": "/src/a.py", "model_id": "canonical-model"}],
            overall_decision="approve",
        )

        migrated = commit_entry.get_model("canonical-model")
        assert migrated is requested_ref
        assert migrated.commentId == 42
        assert review_state.sessions[0].modelId == "canonical-model"
        mock_save.assert_called_once_with(review_state)

    @patch("agentic_devtools.cli.azure_devops.review_state.save_review_state")
    @patch("agentic_devtools.cli.azure_devops.review_state.load_review_state")
    def test_does_not_touch_commit_comments_when_model_unchanged(self, mock_load, mock_save) -> None:
        """No commit registry mutation when scaffolded and effective model are identical."""
        from agentic_devtools.cli.azure_devops.review_state import CommitComment, ModelCommentRef

        review_state = _make_review_state(files={"/src/a.py": _make_file_entry(ReviewStatus.APPROVED.value)})
        review_state.modelId = "gemini-3.7-flash"
        review_state.commitHash = "abc123"
        commit_entry = CommitComment(commitHash="abc123", threadId=1)
        ref = ModelCommentRef(modelId="gemini-3.7-flash", commentId=99)
        commit_entry.models.append(ref)
        review_state.commitComments = {"abc123": commit_entry}
        mock_load.return_value = review_state

        _update_final_review_state(
            pr_id=123,
            file_results=[{"file_path": "/src/a.py", "model_id": "gemini-3.7-flash"}],
            overall_decision="approve",
        )

        assert review_state.modelId == "gemini-3.7-flash"
        kept = commit_entry.get_model("gemini-3.7-flash")
        assert kept is not None
        assert kept.commentId == 99
        mock_save.assert_called_once_with(review_state)

    @patch("agentic_devtools.cli.azure_devops.review_state.save_review_state")
    @patch("agentic_devtools.cli.azure_devops.review_state.load_review_state")
    def test_skips_commit_entry_with_no_ref_for_old_model(self, mock_load, mock_save) -> None:
        """Migration is a no-op for commit entries that have no ref keyed by the old model."""
        from agentic_devtools.cli.azure_devops.review_state import CommitComment, ModelCommentRef

        review_state = _make_review_state(files={"/src/a.py": _make_file_entry(ReviewStatus.APPROVED.value)})
        review_state.modelId = "requested-model"
        review_state.commitHash = "abc123"
        commit_entry = CommitComment(commitHash="abc123", threadId=1)
        unrelated_ref = ModelCommentRef(modelId="some-other-model", commentId=7)
        commit_entry.models.append(unrelated_ref)
        review_state.commitComments = {"abc123": commit_entry}
        mock_load.return_value = review_state

        _update_final_review_state(
            pr_id=123,
            file_results=[{"file_path": "/src/a.py", "model_id": "canonical-model"}],
            overall_decision="approve",
        )

        assert review_state.modelId == "canonical-model"
        assert commit_entry.get_model("requested-model") is None
        assert commit_entry.get_model("canonical-model") is None
        assert commit_entry.get_model("some-other-model") is unrelated_ref
        mock_save.assert_called_once_with(review_state)

    @patch("agentic_devtools.cli.azure_devops.review_state.save_review_state")
    @patch("agentic_devtools.cli.azure_devops.review_state.load_review_state")
    def test_skips_commit_registry_migration_when_current_commit_entry_is_missing(self, mock_load, mock_save) -> None:
        """Migration only applies to the current commit entry and skips global rewrites."""
        from agentic_devtools.cli.azure_devops.review_state import CommitComment, ModelCommentRef

        review_state = _make_review_state(files={"/src/a.py": _make_file_entry(ReviewStatus.APPROVED.value)})
        review_state.modelId = "requested-model"
        review_state.commitHash = "missing-hash"
        historical_entry = CommitComment(commitHash="oldhash", threadId=1)
        historical_ref = ModelCommentRef(modelId="requested-model", commentId=42)
        historical_entry.models.append(historical_ref)
        review_state.commitComments = {"oldhash": historical_entry}
        mock_load.return_value = review_state

        _update_final_review_state(
            pr_id=123,
            file_results=[{"file_path": "/src/a.py", "model_id": "canonical-model"}],
            overall_decision="approve",
        )

        assert review_state.modelId == "canonical-model"
        assert historical_entry.get_model("requested-model") is historical_ref
        assert historical_entry.get_model("canonical-model") is None
        mock_save.assert_called_once_with(review_state)

    @patch("agentic_devtools.cli.azure_devops.review_state.save_review_state")
    @patch("agentic_devtools.cli.azure_devops.review_state.load_review_state")
    def test_merges_active_alias_ref_into_effective_model_ref(self, mock_load, mock_save) -> None:
        """Active alias refs are merged into the effective model ref for current-commit attribution."""
        from agentic_devtools.cli.azure_devops.review_state import CommitComment, ModelCommentRef

        review_state = _make_review_state(files={"/src/a.py": _make_file_entry(ReviewStatus.APPROVED.value)})
        review_state.modelId = "canonical-model"
        review_state.commitHash = "abc123"
        review_state.sessions = [
            ReviewSession(
                sessionId="active-alias",
                modelId="requested-alias",
                startedUtc="2024-01-01T00:00:00+00:00",
                status="in_progress",
                commitHash="abc123",
            )
        ]
        commit_entry = CommitComment(commitHash="abc123", threadId=1)
        canonical_ref = ModelCommentRef(modelId="canonical-model", commentId=11)
        alias_ref = ModelCommentRef(
            modelId="requested-alias",
            commentId=22,
            continuationCommentIds=[23],
            status=ReviewStatus.NEEDS_WORK.value,
            timestamp="2024-01-02T00:00:00+00:00",
        )
        commit_entry.models.extend([canonical_ref, alias_ref])
        review_state.commitComments = {"abc123": commit_entry}
        mock_load.return_value = review_state

        _update_final_review_state(
            pr_id=123,
            file_results=[{"file_path": "/src/a.py", "model_id": "canonical-model"}],
            overall_decision="approve",
        )

        assert review_state.modelId == "canonical-model"
        assert commit_entry.get_model("requested-alias") is None
        merged = commit_entry.get_model("canonical-model")
        assert merged is canonical_ref
        assert merged.commentId == 22
        assert merged.continuationCommentIds == [23]
        assert merged.status == ReviewStatus.NEEDS_WORK.value
        assert merged.timestamp == "2024-01-02T00:00:00+00:00"
        mock_save.assert_called_once_with(review_state)

    @patch("agentic_devtools.cli.azure_devops.review_state.save_review_state")
    @patch("agentic_devtools.cli.azure_devops.review_state.load_review_state")
    def test_alias_merge_ignores_ineligible_sessions_and_blank_model(self, mock_load, mock_save) -> None:
        """Alias merge keeps existing target metadata when source has no useful fields."""
        from agentic_devtools.cli.azure_devops.review_state import CommitComment, ModelCommentRef

        review_state = _make_review_state(files={"/src/a.py": _make_file_entry(ReviewStatus.APPROVED.value)})
        review_state.modelId = "canonical-model"
        review_state.commitHash = "abc123"
        review_state.sessions = [
            ReviewSession(
                sessionId="active-alias",
                modelId="requested-alias",
                startedUtc="2024-01-01T00:03:00+00:00",
                status="in_progress",
                commitHash="abc123",
            ),
            ReviewSession(
                sessionId="blank-model",
                modelId="",
                startedUtc="2024-01-01T00:02:00+00:00",
                status="in_progress",
                commitHash="abc123",
            ),
            ReviewSession(
                sessionId="other-commit",
                modelId="requested-alias",
                startedUtc="2024-01-01T00:01:00+00:00",
                status="in_progress",
                commitHash="different",
            ),
            ReviewSession(
                sessionId="completed-first",
                modelId="requested-alias",
                startedUtc="2024-01-01T00:00:00+00:00",
                status="completed",
                commitHash="abc123",
            ),
        ]
        commit_entry = CommitComment(commitHash="abc123", threadId=1)
        canonical_ref = ModelCommentRef(
            modelId="canonical-model",
            commentId=11,
            continuationCommentIds=[23],
            status=ReviewStatus.APPROVED.value,
            timestamp="2024-01-01T00:00:00+00:00",
        )
        alias_ref = ModelCommentRef(
            modelId="requested-alias",
            commentId=0,
            continuationCommentIds=[23],
            status="",
            timestamp=None,
        )
        commit_entry.models.extend([canonical_ref, alias_ref])
        review_state.commitComments = {"abc123": commit_entry}
        mock_load.return_value = review_state

        _update_final_review_state(
            pr_id=123,
            file_results=[{"file_path": "/src/a.py", "model_id": "canonical-model"}],
            overall_decision="approve",
        )

        assert review_state.modelId == "canonical-model"
        assert commit_entry.get_model("requested-alias") is None
        merged = commit_entry.get_model("canonical-model")
        assert merged is canonical_ref
        assert merged.commentId == 11
        assert merged.continuationCommentIds == [23]
        assert merged.status == ReviewStatus.APPROVED.value
        assert merged.timestamp == "2024-01-01T00:00:00+00:00"
        mock_save.assert_called_once_with(review_state)

    @patch("agentic_devtools.cli.azure_devops.review_state.save_review_state")
    @patch("agentic_devtools.cli.azure_devops.review_state.load_review_state")
    def test_effective_model_leaves_unattributed_alias_session_unchanged(self, mock_load, mock_save) -> None:
        """Fallback leaves an unattributed active session unchanged."""
        review_state = _make_review_state(files={"/src/a.py": _make_file_entry(ReviewStatus.APPROVED.value)})
        review_state.modelId = "canonical-model"
        review_state.commitHash = "abc123"
        review_state.sessions = [
            ReviewSession(
                sessionId="stale-other-commit",
                modelId="canonical-model",
                startedUtc="2024-01-01T00:00:00+00:00",
                status="in_progress",
                commitHash="different",
            ),
            ReviewSession(
                sessionId="current-alias",
                modelId="gemini-3.7-flash",
                startedUtc="2024-01-02T00:00:00+00:00",
                status="in_progress",
                commitHash="abc123",
            ),
        ]
        mock_load.return_value = review_state

        _update_final_review_state(
            pr_id=123,
            file_results=[{"file_path": "/src/a.py", "model_id": "served-model"}],
            overall_decision="approve",
        )

        assert review_state.modelId == "served-model"
        assert review_state.sessions[0].modelId == "canonical-model"
        assert review_state.sessions[1].modelId == "gemini-3.7-flash"
        mock_save.assert_called_once_with(review_state)

    @patch("agentic_devtools.cli.azure_devops.review_state.save_review_state")
    @patch("agentic_devtools.cli.azure_devops.review_state.load_review_state")
    def test_promotes_effective_model_when_no_scaffolded_model_id(self, mock_load, mock_save) -> None:
        """Session relabelling skips model filtering when no scaffolded modelId was set."""
        review_state = _make_review_state(files={"/src/a.py": _make_file_entry(ReviewStatus.APPROVED.value)})
        review_state.modelId = None
        review_state.sessions = [
            ReviewSession(
                sessionId="session-1",
                modelId="some-model",
                startedUtc="2024-01-01T00:00:00+00:00",
                status="in_progress",
            ),
            ReviewSession(
                sessionId="completed-session",
                modelId="some-model",
                startedUtc="2024-01-01T00:01:00+00:00",
                status="completed",
            ),
        ]
        mock_load.return_value = review_state

        _update_final_review_state(
            pr_id=123,
            file_results=[{"file_path": "/src/a.py", "model_id": "canonical-model"}],
            overall_decision="approve",
        )

        assert review_state.modelId == "canonical-model"
        assert review_state.sessions[0].modelId == "canonical-model"
        mock_save.assert_called_once_with(review_state)

    @patch(
        "agentic_devtools.cli.azure_devops.review_state.load_review_state",
        side_effect=FileNotFoundError,
    )
    def test_missing_review_state_warns_and_returns(self, mock_load, capsys) -> None:
        """Missing review-state.json is a non-fatal condition."""
        _update_final_review_state(pr_id=123, file_results=[], overall_decision="approve")

        assert "review-state.json not found" in capsys.readouterr().err


class TestPostConsolidatedComment:
    """Tests for _post_consolidated_comment()."""

    @patch(
        "agentic_devtools.cli.azure_devops.review_state.load_review_state",
        side_effect=FileNotFoundError,
    )
    def test_missing_review_state_skips_cascade(self, mock_load, capsys) -> None:
        """Missing review-state.json skips the cascade update."""
        _post_consolidated_comment(
            pr_id=123,
            organization="https://dev.azure.com/org",
            project="My Project",
            repo_id="repo-guid",
        )

        assert "review-state.json not found" in capsys.readouterr().err

    @patch("agentic_devtools.cli.azure_devops.review_state.save_review_state")
    @patch("agentic_devtools.cli.azure_devops.status_cascade.execute_cascade")
    @patch("agentic_devtools.cli.azure_devops.status_cascade.cascade_overall_summary_update")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.review_state.load_review_state")
    def test_executes_cascade_when_ops_exist(
        self,
        mock_load,
        mock_get_pat,
        mock_get_auth,
        mock_from_state,
        mock_cascade,
        mock_execute,
        mock_save,
    ) -> None:
        """Computed cascade operations are executed and state is persisted."""
        review_state = _make_review_state()
        mock_load.return_value = review_state
        mock_get_pat.return_value = "pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_from_state.return_value = MagicMock()
        mock_cascade.return_value = ["op"]

        _post_consolidated_comment(
            pr_id=123,
            organization="https://dev.azure.com/org",
            project="My Project",
            repo_id="repo-guid",
        )

        mock_cascade.assert_called_once()
        mock_execute.assert_called_once()
        execute_kwargs = mock_execute.call_args.kwargs
        assert execute_kwargs["config"] is mock_from_state.return_value
        assert execute_kwargs["repo_id"] == "repo-guid"
        assert execute_kwargs["pull_request_id"] == 123
        assert execute_kwargs["state"] is review_state
        mock_save.assert_called_once_with(review_state)

    @patch("agentic_devtools.cli.azure_devops.review_state.save_review_state")
    @patch("agentic_devtools.cli.azure_devops.status_cascade.execute_cascade")
    @patch("agentic_devtools.cli.azure_devops.status_cascade.cascade_overall_summary_update")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.review_state.load_review_state")
    def test_skips_execute_when_no_cascade_ops(
        self,
        mock_load,
        mock_get_pat,
        mock_get_auth,
        mock_from_state,
        mock_cascade,
        mock_execute,
        mock_save,
    ) -> None:
        """No-op cascades are not executed, but state is still saved."""
        review_state = _make_review_state()
        mock_load.return_value = review_state
        mock_get_pat.return_value = "pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_from_state.return_value = MagicMock()
        mock_cascade.return_value = []

        _post_consolidated_comment(
            pr_id=123,
            organization="https://dev.azure.com/org",
            project="MyProject",
            repo_id="repo-guid",
        )

        mock_execute.assert_not_called()
        mock_save.assert_called_once_with(review_state)

    @patch("agentic_devtools.cli.azure_devops.review_state.save_review_state")
    @patch("agentic_devtools.cli.azure_devops.status_cascade.execute_cascade")
    @patch("agentic_devtools.cli.azure_devops.status_cascade.cascade_overall_summary_update")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.review_state.load_review_state")
    def test_url_encodes_reserved_project_characters(
        self,
        mock_load,
        mock_get_pat,
        mock_get_auth,
        mock_from_state,
        mock_cascade,
        mock_execute,
        mock_save,
    ) -> None:
        """Project names are fully URL-encoded before cascade calls."""
        review_state = _make_review_state()
        mock_load.return_value = review_state
        mock_get_pat.return_value = "pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_from_state.return_value = MagicMock()
        mock_cascade.return_value = []

        _post_consolidated_comment(
            pr_id=123,
            organization="https://dev.azure.com/org",
            project="My/Project #1",
            repo_id="repo-guid",
        )

        base_url = mock_cascade.call_args.args[1]
        assert base_url == (
            "https://dev.azure.com/org/My%2FProject%20%231/_apis/git/repositories/repo-guid/pullRequests/123"
        )
        mock_execute.assert_not_called()
        mock_save.assert_called_once_with(review_state)


class TestPostSuggestionThreads:
    """Tests for _post_suggestion_threads()."""

    @patch("agentic_devtools.orchestration.review.nodes.post_results._post_line_comment")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.orchestration.review.nodes.post_results._list_existing_suggestion_thread_keys")
    @patch("agentic_devtools.cli.azure_devops.review_state.read_modify_write_review_state")
    def test_posts_only_line_anchored_suggestions(
        self,
        mock_rw_state,
        mock_existing,
        mock_get_pat,
        mock_get_auth,
        mock_post_line,
        capsys,
    ) -> None:
        """Only suggestions with a target line are posted; lineless ones warn to stderr."""
        mock_existing.return_value = set()
        mock_get_pat.return_value = "pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_rw_state.return_value.__enter__.return_value = _make_review_state(
            files={
                "/src/a.py": FileEntry(threadId=1, commentId=1, folder="src", fileName="a.py"),
                "/src/b.py": FileEntry(threadId=1, commentId=1, folder="src", fileName="b.py"),
            }
        )
        mock_post_line.side_effect = [(11, 21), (12, 22), (13, 23)]

        object_result = SimpleNamespace(
            file_path="/src/b.py",
            suggestions=[
                SimpleNamespace(
                    replacement_code="return 2",
                    line=9,
                    endLine=11,
                    content="Use the constant.",
                )
            ],
        )

        _post_suggestion_threads(
            pr_id=123,
            organization="https://dev.azure.com/org",
            project="MyProject",
            repo_id="repo-guid",
            file_results=[
                {
                    "file_path": "/src/a.py",
                    "suggestions": [
                        {"content": "comment only", "line": 1},
                        {"content": "missing line", "replacement_code": "x"},
                        {
                            "content": "dict suggestion",
                            "line": 4,
                            "endLine": 6,
                            "replacement_code": "return 1",
                        },
                    ],
                },
                object_result,
            ],
        )

        assert mock_post_line.call_count == 3
        first_call = mock_post_line.call_args_list[0].kwargs
        assert first_call["file_path"] == "/src/a.py"
        assert first_call["replacement_code"] is None
        second_call = mock_post_line.call_args_list[1].kwargs
        assert second_call["replacement_code"] == "return 1"
        assert second_call["end_line"] == 6
        third_call = mock_post_line.call_args_list[2].kwargs
        assert third_call["file_path"] == "/src/b.py"
        assert third_call["line"] == 9
        assert third_call["end_line"] == 11
        # Lineless suggestion emits a warning instead of silently dropping
        assert "no line anchor" in capsys.readouterr().err

    @patch("agentic_devtools.orchestration.review.nodes.post_results._post_line_comment")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.orchestration.review.nodes.post_results._list_existing_suggestion_thread_keys")
    @patch("agentic_devtools.cli.azure_devops.review_state.read_modify_write_review_state")
    def test_warns_and_skips_suggestion_without_line(
        self,
        mock_rw_state,
        mock_existing,
        mock_get_pat,
        mock_get_auth,
        mock_post_line,
        capsys,
    ) -> None:
        """A suggestion dict with no line anchor emits a warning and is not posted."""
        mock_existing.return_value = set()
        mock_get_pat.return_value = "pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_rw_state.return_value.__enter__.return_value = _make_review_state()

        _post_suggestion_threads(
            pr_id=123,
            organization="https://dev.azure.com/org",
            project="MyProject",
            repo_id="repo-guid",
            file_results=[
                {
                    "file_path": "/src/orphan.py",
                    "suggestions": [
                        {"content": "no line anchor here", "severity": "medium"},
                    ],
                }
            ],
        )

        mock_post_line.assert_not_called()
        stderr = capsys.readouterr().err
        assert "no line anchor" in stderr
        assert "/src/orphan.py" in stderr

    @patch("agentic_devtools.orchestration.review.nodes.post_results._post_line_comment")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.orchestration.review.nodes.post_results._list_existing_suggestion_thread_keys")
    @patch("agentic_devtools.cli.azure_devops.review_state.read_modify_write_review_state")
    def test_persists_posted_suggestion_thread_ids(
        self,
        mock_rw_state,
        mock_existing,
        mock_get_pat,
        mock_get_auth,
        mock_post_line,
    ) -> None:
        """Posted suggestion thread/comment IDs are written back to review state."""
        review_state = _make_review_state(
            files={"/src/a.py": FileEntry(threadId=1, commentId=1, folder="src", fileName="a.py")}
        )
        mock_rw_state.return_value.__enter__.return_value = review_state
        mock_existing.return_value = set()
        mock_get_pat.return_value = "pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_post_line.return_value = (17, 23)

        _post_suggestion_threads(
            pr_id=123,
            organization="https://dev.azure.com/org",
            project="MyProject",
            repo_id="repo-guid",
            file_results=[
                {
                    "file_path": "/src/a.py",
                    "suggestions": [
                        {
                            "severity": "high",
                            "content": "dict suggestion",
                            "line": 4,
                            "endLine": 6,
                            "replacement_code": "return 1",
                        }
                    ],
                }
            ],
        )

        saved_suggestion = review_state.files["/src/a.py"].suggestions
        assert len(saved_suggestion) == 1
        assert saved_suggestion[0].threadId == 17
        assert saved_suggestion[0].commentId == 23
        assert saved_suggestion[0].linkText == "lines 4 - 6"
        assert saved_suggestion[0].replacement_code == "return 1"

    @patch("agentic_devtools.cli.azure_devops.review_state.read_modify_write_review_state")
    def test_warns_when_posted_suggestion_file_is_missing(self, mock_rw_state, capsys) -> None:
        """Missing file entries downgrade persistence gaps to warnings."""
        review_state = _make_review_state(files={})
        mock_rw_state.return_value = nullcontext(review_state)

        from agentic_devtools.orchestration.review.nodes.post_results import _persist_posted_suggestions

        _persist_posted_suggestions(
            pr_id=123,
            posted_suggestions=[
                ("/src/missing.py", 17, 23, 4, 6, "high", "dict suggestion", False, "lines 4 - 6", None)
            ],
        )

        assert "unknown file" in capsys.readouterr().err

    @patch("agentic_devtools.cli.azure_devops.review_state.read_modify_write_review_state")
    def test_skips_duplicate_persisted_suggestion_thread_ids(self, mock_rw_state) -> None:
        """Already-persisted thread IDs are not duplicated in review state."""
        review_state = _make_review_state(
            files={
                "/src/a.py": FileEntry(
                    threadId=1,
                    commentId=1,
                    folder="src",
                    fileName="a.py",
                    suggestions=[],
                )
            }
        )
        review_state.files["/src/a.py"].suggestions.append(
            SuggestionEntry(
                threadId=17,
                commentId=23,
                line=4,
                endLine=6,
                severity="high",
                outOfScope=False,
                linkText="lines 4 - 6",
                content="dict suggestion",
            )
        )
        mock_rw_state.return_value = nullcontext(review_state)

        from agentic_devtools.orchestration.review.nodes.post_results import _persist_posted_suggestions

        _persist_posted_suggestions(
            pr_id=123,
            posted_suggestions=[("/src/a.py", 17, 23, 4, 6, "high", "dict suggestion", False, "lines 4 - 6", None)],
        )

        assert len(review_state.files["/src/a.py"].suggestions) == 1

    @patch("agentic_devtools.cli.azure_devops.review_state.read_modify_write_review_state")
    def test_replaces_draft_suggestion_when_real_entry_is_posted(self, mock_rw_state) -> None:
        """Draft entries (threadId=0) for the same line+endLine+content are removed before the real entry is added."""
        review_state = _make_review_state(
            files={
                "/src/a.py": FileEntry(
                    threadId=1,
                    commentId=1,
                    folder="src",
                    fileName="a.py",
                    suggestions=[],
                )
            }
        )
        # Seed a draft suggestion written by _update_review_state_for_file
        review_state.files["/src/a.py"].suggestions.append(
            SuggestionEntry(
                threadId=0,
                commentId=0,
                line=4,
                endLine=4,
                severity="high",
                outOfScope=False,
                linkText="",
                content="dict suggestion",
            )
        )
        mock_rw_state.return_value = nullcontext(review_state)

        from agentic_devtools.orchestration.review.nodes.post_results import _persist_posted_suggestions

        _persist_posted_suggestions(
            pr_id=123,
            posted_suggestions=[("/src/a.py", 42, 55, 4, 4, "high", "dict suggestion", False, "line 4", None)],
        )

        suggestions = review_state.files["/src/a.py"].suggestions
        assert len(suggestions) == 1  # draft replaced, not duplicated
        assert suggestions[0].threadId == 42  # real ADO thread ID
        assert suggestions[0].commentId == 55  # real ADO comment ID
        assert suggestions[0].linkText == "line 4"

    @patch("agentic_devtools.cli.azure_devops.review_state.read_modify_write_review_state")
    def test_does_not_remove_draft_with_different_end_line(self, mock_rw_state) -> None:
        """Draft cleanup is scoped by endLine; a draft with a different endLine is preserved."""
        review_state = _make_review_state(
            files={
                "/src/a.py": FileEntry(
                    threadId=1,
                    commentId=1,
                    folder="src",
                    fileName="a.py",
                    suggestions=[],
                )
            }
        )
        # Draft covers lines 4–8; real posting only covers line 4–4
        review_state.files["/src/a.py"].suggestions.append(
            SuggestionEntry(
                threadId=0,
                commentId=0,
                line=4,
                endLine=8,
                severity="high",
                outOfScope=False,
                linkText="",
                content="dict suggestion",
            )
        )
        mock_rw_state.return_value = nullcontext(review_state)

        from agentic_devtools.orchestration.review.nodes.post_results import _persist_posted_suggestions

        _persist_posted_suggestions(
            pr_id=123,
            # posted entry has end_line=4, draft has endLine=8 → draft must NOT be removed
            posted_suggestions=[("/src/a.py", 42, 55, 4, 4, "high", "dict suggestion", False, "line 4", None)],
        )

        suggestions = review_state.files["/src/a.py"].suggestions
        assert len(suggestions) == 2  # draft kept + real entry added

    @patch("agentic_devtools.orchestration.review.nodes.post_results._post_line_comment")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.orchestration.review.nodes.post_results._list_existing_suggestion_thread_keys")
    def test_skips_existing_suggestion_threads(
        self,
        mock_existing,
        mock_get_pat,
        mock_get_auth,
        mock_post_line,
    ) -> None:
        """Existing marked suggestion threads are not posted again."""
        mock_existing.return_value = {("/src/a.py", 4, 4, "high", "dict suggestion\n\n```suggestion\nreturn 1\n```")}
        mock_get_pat.return_value = "pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}

        _post_suggestion_threads(
            pr_id=123,
            organization="https://dev.azure.com/org",
            project="MyProject",
            repo_id="repo-guid",
            file_results=[
                {
                    "file_path": "/src/a.py",
                    "suggestions": [
                        {
                            "severity": "high",
                            "content": "dict suggestion",
                            "line": 4,
                            "replacement_code": "return 1",
                        }
                    ],
                }
            ],
        )

        mock_post_line.assert_not_called()

    @patch("agentic_devtools.orchestration.review.nodes.post_results._post_line_comment")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.orchestration.review.nodes.post_results._list_existing_suggestion_thread_keys")
    def test_dedup_distinguishes_suggestions_by_end_line(
        self,
        mock_existing,
        mock_get_pat,
        mock_get_auth,
        mock_post_line,
    ) -> None:
        """A different end line is treated as a distinct suggestion thread."""
        mock_existing.return_value = {("/src/a.py", 4, 4, "high", "dict suggestion\n\n```suggestion\nreturn 1\n```")}
        mock_get_pat.return_value = "pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}

        _post_suggestion_threads(
            pr_id=123,
            organization="https://dev.azure.com/org",
            project="MyProject",
            repo_id="repo-guid",
            file_results=[
                {
                    "file_path": "/src/a.py",
                    "suggestions": [
                        {
                            "severity": "high",
                            "content": "dict suggestion",
                            "line": 4,
                            "endLine": 6,
                            "replacement_code": "return 1",
                        }
                    ],
                }
            ],
        )

        mock_post_line.assert_called_once()
        assert mock_post_line.call_args.kwargs["end_line"] == 6

    @patch(
        "agentic_devtools.orchestration.review.nodes.post_results._post_line_comment",
        side_effect=RuntimeError("api boom"),
    )
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.orchestration.review.nodes.post_results._list_existing_suggestion_thread_keys")
    def test_logs_suggestion_post_failures(
        self,
        mock_existing,
        mock_get_pat,
        mock_get_auth,
        mock_post_line,
        capsys,
    ) -> None:
        """Per-suggestion posting failures are downgraded to warnings."""
        mock_existing.return_value = set()
        mock_get_pat.return_value = "pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}

        _post_suggestion_threads(
            pr_id=123,
            organization="https://dev.azure.com/org",
            project="MyProject",
            repo_id="repo-guid",
            file_results=[
                {
                    "file_path": "/src/a.py",
                    "suggestions": [
                        {
                            "content": "dict suggestion",
                            "line": 4,
                            "replacement_code": "return 1",
                        }
                    ],
                }
            ],
        )

        assert "failed to post suggestion thread" in capsys.readouterr().err

    @patch("requests.get")
    def test_lists_existing_suggestion_thread_keys(self, mock_get) -> None:
        """Existing AGDT suggestion threads are recovered by marker and content."""
        from agentic_devtools.orchestration.review.nodes.post_results import (
            _list_existing_suggestion_thread_keys,
        )

        response = MagicMock()
        response.json.return_value = {
            "value": [
                {
                    "threadContext": {
                        "filePath": "/src/a.py",
                        "rightFileEnd": {"line": 8, "offset": 1},
                    },
                    "comments": [
                        {
                            "content": (
                                "<!-- agdt-review:v1 type:suggestion file:/src/a.py pr:123 line:4 severity:high -->\n"
                                "dict suggestion\n\n```suggestion\nreturn 1\n```"
                            )
                        }
                    ],
                }
            ]
        }
        mock_get.return_value = response

        existing = _list_existing_suggestion_thread_keys(
            pr_id=123,
            organization="https://dev.azure.com/org",
            project="MyProject",
            repo_id="repo-guid",
            headers={"Authorization": "Basic fake"},
        )

        assert existing == {("/src/a.py", 4, 8, "high", "dict suggestion\n\n```suggestion\nreturn 1\n```")}
        response.raise_for_status.assert_called_once_with()

    @patch("requests.get")
    def test_ignores_malformed_existing_threads(self, mock_get) -> None:
        """Malformed or non-suggestion threads are skipped during recovery."""
        from agentic_devtools.orchestration.review.nodes.post_results import (
            _list_existing_suggestion_thread_keys,
        )

        response = MagicMock()
        response.json.return_value = [
            "not-a-thread",
            {},
            {"comments": [0]},
            {"comments": [{}]},
            {"comments": [{"content": 123}]},
            {"comments": [{"content": "<!-- agdt-review:v1 type:overall-summary pr:123 -->\nsummary"}]},
            {
                "comments": [
                    {"content": ("<!-- agdt-review:v1 type:suggestion file:/src/a.py pr:123 severity:high -->\nbody")}
                ]
            },
            {
                "comments": [{"content": "<!-- agdt-review:v1 type:suggestion pr:123 line:5 severity:low -->\nbody"}],
                "threadContext": {"filePath": "/src/fallback.py"},
            },
            {
                "comments": [{"content": "<!-- agdt-review:v1 type:suggestion pr:123 line:6 severity:low -->\nbody"}],
                "threadContext": {"filePath": 42},
            },
            {
                "comments": [
                    {
                        "content": (
                            "<!-- agdt-review:v1 type:suggestion file:/src/no-context.py "
                            "pr:123 line:7 severity:low -->\n"
                            "no context"
                        )
                    }
                ],
                "threadContext": "not-a-dict",
            },
            {
                "comments": [
                    {
                        "content": (
                            "<!-- agdt-review:v1 type:suggestion file:/src/non-int-end.py "
                            "pr:123 line:8 severity:low -->\n"
                            "non-int end"
                        )
                    }
                ],
                "threadContext": {
                    "filePath": "/src/non-int-end.py",
                    "rightFileEnd": {"line": "12", "offset": 1},
                },
            },
        ]
        mock_get.return_value = response

        existing = _list_existing_suggestion_thread_keys(
            pr_id=123,
            organization="https://dev.azure.com/org",
            project="MyProject",
            repo_id="repo-guid",
            headers={"Authorization": "Basic fake"},
        )

        assert existing == {
            ("/src/fallback.py", 5, 5, "low", "body"),
            ("/src/no-context.py", 7, 7, "low", "no context"),
            ("/src/non-int-end.py", 8, 8, "low", "non-int end"),
        }


class TestPostLineComment:
    """Tests for _post_line_comment()."""

    @patch("requests.post")
    def test_posts_line_anchored_comment_payload(self, mock_post) -> None:
        """Line comments use the expected ADO endpoint and payload."""
        response = MagicMock()
        response.json.return_value = {"id": 19, "comments": [{"id": 29}]}
        mock_post.return_value = response

        thread_id, comment_id = _post_line_comment(
            pr_id=123,
            organization="https://dev.azure.com/org",
            project="My Project",
            repo_id="repo-guid",
            headers={"Authorization": "Basic fake"},
            file_path="/src/main.py",
            line=17,
            end_line=19,
            content="Prefer a helper.",
            replacement_code="helper()",
        )

        called_url = mock_post.call_args.args[0]
        called_body = mock_post.call_args.kwargs["json"]
        assert "My%20Project" in called_url
        assert called_body["threadContext"]["filePath"] == "/src/main.py"
        assert called_body["threadContext"]["rightFileStart"]["line"] == 17
        assert called_body["threadContext"]["rightFileEnd"]["line"] == 19
        assert called_body["comments"][0]["commentType"] == "text"
        assert called_body["status"] == "active"
        assert (
            "<!-- agdt-review:v1 type:suggestion file:/src/main.py pr:123 line:17 -->"
            in called_body["comments"][0]["content"]
        )
        assert "```suggestion\nhelper()\n```" in called_body["comments"][0]["content"]
        assert thread_id == 19
        assert comment_id == 29
        response.raise_for_status.assert_called_once_with()

    @pytest.mark.parametrize(
        ("payload", "message"),
        [
            ("not-a-dict", "Unexpected Azure DevOps thread response payload type"),
            ({"id": "19", "comments": [{"id": 29}]}, "integer thread id"),
            ({"id": 19, "comments": []}, "did not include comments"),
            ({"id": 19, "comments": ["not-a-dict"]}, "valid comment object"),
            ({"id": 19, "comments": [{"id": "29"}]}, "integer comment id"),
        ],
    )
    @patch("requests.post")
    def test_validates_thread_post_response_shape(self, mock_post, payload, message) -> None:
        """Malformed Azure DevOps thread responses fail with clear errors."""
        response = MagicMock()
        response.json.return_value = payload
        mock_post.return_value = response

        with pytest.raises(RuntimeError, match=message):
            _post_line_comment(
                pr_id=123,
                organization="https://dev.azure.com/org",
                project="My Project",
                repo_id="repo-guid",
                headers={"Authorization": "Basic fake"},
                file_path="/src/main.py",
                line=17,
                end_line=19,
                content="Prefer a helper.",
                replacement_code="helper()",
            )

    @patch("requests.post")
    def test_omits_suggestion_fence_when_replacement_missing(self, mock_post) -> None:
        """Comment-only findings do not add an empty suggestion fence."""
        response = MagicMock()
        response.json.return_value = {"id": 19, "comments": [{"id": 29}]}
        mock_post.return_value = response

        _post_line_comment(
            pr_id=123,
            organization="https://dev.azure.com/org",
            project="My Project",
            repo_id="repo-guid",
            headers={"Authorization": "Basic fake"},
            file_path="/src/main.py",
            line=17,
            end_line=17,
            content="Prefer a helper.",
            replacement_code=None,
        )

        comment_content = mock_post.call_args.kwargs["json"]["comments"][0]["content"]
        assert "Prefer a helper." in comment_content
        assert "```suggestion" not in comment_content

    @patch("requests.post")
    def test_url_encodes_reserved_project_characters(self, mock_post) -> None:
        """Reserved characters in project names are encoded in thread URLs."""
        response = MagicMock()
        response.json.return_value = {"id": 19, "comments": [{"id": 29}]}
        mock_post.return_value = response

        _post_line_comment(
            pr_id=321,
            organization="https://dev.azure.com/org",
            project="My/Project #1",
            repo_id="repo-guid",
            headers={"Authorization": "Basic fake"},
            file_path="/src/main.py",
            line=10,
            end_line=None,
            content="Consider this",
            replacement_code="pass",
        )

        assert mock_post.call_args.args[0] == (
            "https://dev.azure.com/org/My%2FProject%20%231/_apis/git/repositories/"
            "repo-guid/pullRequests/321/threads?api-version=7.1-preview.1"
        )
        response.raise_for_status.assert_called_once_with()
