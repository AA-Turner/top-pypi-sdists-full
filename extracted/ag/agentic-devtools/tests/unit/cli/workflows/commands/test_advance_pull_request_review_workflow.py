"""Tests for AdvancePullRequestReviewWorkflow."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools import state
from agentic_devtools.cli.workflows import commands
from agentic_devtools.prompts import loader

_PROGRESS = "agentic_devtools.cli.azure_devops.pr_review_progress.compute_review_progress"
_READ_SUBMIT_RESULT = "agentic_devtools.cli.azure_devops.pr_review_submit.read_submit_result"
_VALID_SUBMIT_RESULT = {"dryRun": False, "prId": 123, "counts": {"posted": 1, "accepted": 1, "failed": 0}}


@pytest.fixture
def temp_prompts_dir(tmp_path):
    """Create a temporary prompts directory with test templates."""
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()
    with patch.object(loader, "get_prompts_dir", return_value=prompts_dir):
        yield prompts_dir


@pytest.fixture
def temp_output_dir(tmp_path):
    """Create a temporary output directory."""
    output_dir = tmp_path / "temp"
    output_dir.mkdir()
    with patch.object(loader, "get_temp_output_dir", return_value=output_dir):
        yield output_dir


@pytest.fixture
def clear_state_before(temp_state_dir):
    """Clear state before each test.

    Note: We only remove the state file, not the entire temp folder,
    to avoid deleting directories created by other fixtures (like temp_prompts_dir).
    """
    state_file = temp_state_dir / "state.json"
    if state_file.exists():
        state_file.unlink()
    yield


@pytest.fixture
def mock_workflow_state_clearing():
    """Mock clear_state_for_workflow_initiation to be a no-op.

    Workflow initiation commands reset workflow tracking keys (workflow,
    agdt_run_id) at the start.  This fixture prevents that reset, which
    is useful when tests pre-set workflow state before calling the command.
    """
    with patch("agentic_devtools.cli.workflows.commands.clear_state_for_workflow_initiation"):
        yield


def _progress(*, all_complete, completed, pending, total):
    """Build a compute_review_progress() return dict (manifest + ledger source)."""
    return {
        "all_complete": all_complete,
        "completed_count": completed,
        "pending_count": pending,
        "total_count": total,
    }


class TestAdvancePullRequestReviewWorkflow:
    """Tests for advance_pull_request_review_workflow function."""

    @pytest.fixture(autouse=True)
    def mock_read_submit_result(self):
        """Provide a valid submit-result by default so completion tests don't hit the guard."""
        with patch(_READ_SUBMIT_RESULT, return_value=_VALID_SUBMIT_RESULT):
            yield

    def test_advance_no_active_workflow(self, temp_state_dir, clear_state_before, capsys):
        """Test advance fails when workflow is not active."""
        with pytest.raises(SystemExit) as exc_info:
            commands.advance_pull_request_review_workflow()
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "pull-request-review workflow is not active" in captured.err

    def test_advance_no_workflow_state(self, temp_state_dir, clear_state_before, capsys):
        """Test advance fails when get_workflow_state returns None."""
        with patch("agentic_devtools.state.is_workflow_active", return_value=True):
            with patch("agentic_devtools.state.get_workflow_state", return_value=None):
                with pytest.raises(SystemExit) as exc_info:
                    commands.advance_pull_request_review_workflow()
                assert exc_info.value.code == 1
                captured = capsys.readouterr()
                assert "Could not get workflow state" in captured.err

    def test_advance_no_pull_request_id(self, temp_state_dir, clear_state_before, capsys):
        """Test advance fails when no pull_request_id in context or state."""
        state.set_workflow_state(
            name="pull-request-review",
            status="in-progress",
            step="initiate",
            context={},
        )

        with pytest.raises(SystemExit) as exc_info:
            commands.advance_pull_request_review_workflow()
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "No pull_request_id found" in captured.err

    def test_advance_invalid_pull_request_id(self, temp_state_dir, clear_state_before, capsys):
        """Test advance fails when pull_request_id is invalid."""
        state.set_workflow_state(
            name="pull-request-review",
            status="in-progress",
            step="initiate",
            context={"pull_request_id": "not-a-number"},
        )

        with pytest.raises(SystemExit) as exc_info:
            commands.advance_pull_request_review_workflow()
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Invalid pull_request_id" in captured.err

    def test_advance_auto_detects_decision_when_all_files_complete(
        self, temp_state_dir, temp_prompts_dir, temp_output_dir, clear_state_before, capsys
    ):
        """Test advance auto-detects decision step from consolidate-and-submit."""
        state.set_workflow_state(
            name="pull-request-review",
            status="in-progress",
            step="consolidate-and-submit",
            context={"pull_request_id": "123"},
        )

        with patch(_PROGRESS, return_value=_progress(all_complete=True, completed=5, pending=0, total=5)):
            workflow_dir = temp_prompts_dir / "pull-request-review"
            workflow_dir.mkdir()
            template_file = workflow_dir / "default-decision-prompt.md"
            template_file.write_text(
                "Decision for PR #{{pull_request_id}}\n"
                "Files: {{completed_count}} Approvals: {{approval_count}} Changes: {{changes_count}}",
                encoding="utf-8",
            )

            commands.advance_pull_request_review_workflow()

        workflow = state.get_workflow_state()
        assert workflow["step"] == "decision"

    def test_advance_stays_on_delegate_when_files_pending(
        self, temp_state_dir, temp_prompts_dir, temp_output_dir, clear_state_before, capsys
    ):
        """Stays on delegate step when all_complete is False (files still pending)."""
        state.set_workflow_state(
            name="pull-request-review",
            status="in-progress",
            step="delegate",
            context={"pull_request_id": "123"},
        )

        with patch(_PROGRESS, return_value=_progress(all_complete=False, completed=3, pending=2, total=5)):
            workflow_dir = temp_prompts_dir / "pull-request-review"
            workflow_dir.mkdir()
            template_file = workflow_dir / "default-delegate-prompt.md"
            template_file.write_text("Delegate for PR #{{pull_request_id}}", encoding="utf-8")

            commands.advance_pull_request_review_workflow()

        workflow = state.get_workflow_state()
        assert workflow["step"] == "delegate"

    def test_advance_delegate_to_consolidate_when_all_complete(
        self, temp_state_dir, temp_prompts_dir, temp_output_dir, clear_state_before, capsys
    ):
        """Advances from delegate to consolidate-and-submit when all_complete is True."""
        state.set_workflow_state(
            name="pull-request-review",
            status="in-progress",
            step="delegate",
            context={"pull_request_id": "123"},
        )

        with patch(_PROGRESS, return_value=_progress(all_complete=True, completed=5, pending=0, total=5)):
            workflow_dir = temp_prompts_dir / "pull-request-review"
            workflow_dir.mkdir()
            template_file = workflow_dir / "default-consolidate-and-submit-prompt.md"
            template_file.write_text("Consolidate for PR #{{pull_request_id}}", encoding="utf-8")

            commands.advance_pull_request_review_workflow()

        workflow = state.get_workflow_state()
        assert workflow["step"] == "consolidate-and-submit"

    def test_advance_renders_progress_counts_in_delegate_template(
        self, temp_state_dir, temp_prompts_dir, temp_output_dir, clear_state_before, capsys
    ):
        """The delegate template renders the manifest+ledger progress counts verbatim."""
        state.set_workflow_state(
            name="pull-request-review",
            status="in-progress",
            step="pr-synthesis",
            context={"pull_request_id": "123"},
        )

        with patch(_PROGRESS, return_value=_progress(all_complete=False, completed=3, pending=2, total=5)):
            workflow_dir = temp_prompts_dir / "pull-request-review"
            workflow_dir.mkdir()
            template_file = workflow_dir / "default-delegate-prompt.md"
            template_file.write_text(
                "Done: {{completed_count}} / {{total_count}}, Pending: {{pending_count}}, Complete: {{all_complete}}",
                encoding="utf-8",
            )

            commands.advance_pull_request_review_workflow()

        captured = capsys.readouterr()
        assert "Done: 3 / 5" in captured.out
        assert "Pending: 2" in captured.out
        assert "Complete: False" in captured.out

    def test_advance_to_decision_computes_approval_and_changes_counts(
        self, temp_state_dir, temp_prompts_dir, temp_output_dir, clear_state_before, capsys
    ):
        """Test decision step receives approval_count and changes_count from review-state."""
        state.set_workflow_state(
            name="pull-request-review",
            status="in-progress",
            step="consolidate-and-submit",
            context={"pull_request_id": "123"},
        )

        mock_file_approved = MagicMock()
        mock_file_approved.status = "approved"
        mock_file_needswork = MagicMock()
        mock_file_needswork.status = "needs-work"
        mock_review_state = MagicMock()
        mock_review_state.files = {
            "/src/a.py": mock_file_approved,
            "/src/b.py": mock_file_approved,
            "/src/c.py": mock_file_needswork,
        }

        with (
            patch(_PROGRESS, return_value=_progress(all_complete=True, completed=3, pending=0, total=3)),
            patch(
                "agentic_devtools.cli.azure_devops.review_state.load_review_state",
                return_value=mock_review_state,
            ),
        ):
            workflow_dir = temp_prompts_dir / "pull-request-review"
            workflow_dir.mkdir()
            template_file = workflow_dir / "default-decision-prompt.md"
            template_file.write_text(
                "Approvals: {{approval_count}}, Changes: {{changes_count}}",
                encoding="utf-8",
            )

            commands.advance_pull_request_review_workflow()

        captured = capsys.readouterr()
        assert "Approvals: 2" in captured.out
        assert "Changes: 1" in captured.out

    def test_advance_from_initiate_to_pull_request_overview(
        self, temp_state_dir, temp_prompts_dir, temp_output_dir, clear_state_before, capsys
    ):
        """Test advance from initiate step goes to pr-synthesis."""
        state.set_workflow_state(
            name="pull-request-review",
            status="in-progress",
            step="initiate",
            context={
                "pull_request_id": "123",
                "pr_url": "https://dev.azure.com/org/proj/_git/repo/pullrequest/123",
                "source_code_platform": "AzureDevOps",
            },
        )

        with patch(_PROGRESS, return_value=_progress(all_complete=False, completed=0, pending=5, total=5)):
            workflow_dir = temp_prompts_dir / "pull-request-review"
            workflow_dir.mkdir()
            template_file = workflow_dir / "default-pr-synthesis-prompt.md"
            template_file.write_text(
                "Synthesis for PR #{{pull_request_id}} at {{pr_url}}",
                encoding="utf-8",
            )

            commands.advance_pull_request_review_workflow()

        workflow = state.get_workflow_state()
        assert workflow["step"] == "pr-synthesis"

    def test_advance_to_decision_with_in_progress_file_status(
        self, temp_state_dir, temp_prompts_dir, temp_output_dir, clear_state_before, capsys
    ):
        """File with 'in-progress' status is neither approved nor needs-work (loop-back branch)."""
        state.set_workflow_state(
            name="pull-request-review",
            status="in-progress",
            step="consolidate-and-submit",
            context={"pull_request_id": "123"},
        )

        mock_file_approved = MagicMock()
        mock_file_approved.status = "approved"
        mock_file_in_progress = MagicMock()
        mock_file_in_progress.status = "in-progress"
        mock_review_state = MagicMock()
        mock_review_state.files = {
            "/src/a.py": mock_file_approved,
            "/src/b.py": mock_file_in_progress,
        }

        with (
            patch(_PROGRESS, return_value=_progress(all_complete=True, completed=2, pending=0, total=2)),
            patch(
                "agentic_devtools.cli.azure_devops.review_state.load_review_state",
                return_value=mock_review_state,
            ),
        ):
            workflow_dir = temp_prompts_dir / "pull-request-review"
            workflow_dir.mkdir()
            template_file = workflow_dir / "default-decision-prompt.md"
            template_file.write_text(
                "Approvals: {{approval_count}}, Changes: {{changes_count}}",
                encoding="utf-8",
            )

            commands.advance_pull_request_review_workflow()

        captured = capsys.readouterr()
        assert "Approvals: 1" in captured.out
        assert "Changes: 0" in captured.out

    def test_advance_from_pull_request_overview_to_file_review(
        self, temp_state_dir, temp_prompts_dir, temp_output_dir, clear_state_before, capsys
    ):
        """Test advance from pr-synthesis step goes to delegate."""
        state.set_workflow_state(
            name="pull-request-review",
            status="in-progress",
            step="pr-synthesis",
            context={"pull_request_id": "123"},
        )

        with patch(_PROGRESS, return_value=_progress(all_complete=False, completed=0, pending=5, total=5)):
            workflow_dir = temp_prompts_dir / "pull-request-review"
            workflow_dir.mkdir()
            template_file = workflow_dir / "default-delegate-prompt.md"
            template_file.write_text("Delegate for PR #{{pull_request_id}}", encoding="utf-8")

            commands.advance_pull_request_review_workflow()

        workflow = state.get_workflow_state()
        assert workflow["step"] == "delegate"

    def test_advance_rejects_invalid_step(self, temp_state_dir, clear_state_before, capsys):
        """Test advance rejects removed/unknown steps like 'summary'."""
        state.set_workflow_state(
            name="pull-request-review",
            status="in-progress",
            step="delegate",
            context={"pull_request_id": "123"},
        )

        with patch(_PROGRESS, return_value=_progress(all_complete=False, completed=0, pending=5, total=5)):
            with pytest.raises(SystemExit) as exc_info:
                commands.advance_pull_request_review_workflow(step="summary")
            assert exc_info.value.code == 1
            captured = capsys.readouterr()
            assert "Unknown step 'summary'" in captured.err
            assert "completion" in captured.err
            assert "decision" in captured.err
            assert "delegate" in captured.err
            assert "pr-synthesis" in captured.err

    def test_advance_rejects_explicit_consolidate_when_delegate_not_complete(
        self, temp_state_dir, clear_state_before, capsys
    ):
        """Explicit consolidate step is blocked until delegate queue is fully answered."""
        state.set_workflow_state(
            name="pull-request-review",
            status="in-progress",
            step="delegate",
            context={"pull_request_id": "123"},
        )

        with patch(_PROGRESS, return_value=_progress(all_complete=False, completed=1, pending=4, total=5)):
            with pytest.raises(SystemExit) as exc_info:
                commands.advance_pull_request_review_workflow(step="consolidate-and-submit")
            assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "Cannot advance from 'delegate' to 'consolidate-and-submit'" in captured.err
        workflow = state.get_workflow_state()
        assert workflow["step"] == "delegate"

    def test_advance_rejects_skipping_to_completion_from_delegate(self, temp_state_dir, clear_state_before, capsys):
        """Skipping straight from 'delegate' to 'completion' is refused."""
        state.set_workflow_state(
            name="pull-request-review",
            status="in-progress",
            step="delegate",
            context={"pull_request_id": "123"},
        )

        with patch(_PROGRESS, return_value=_progress(all_complete=False, completed=0, pending=39, total=39)):
            with pytest.raises(SystemExit) as exc_info:
                commands.advance_pull_request_review_workflow(step="completion")
            assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "Cannot skip from 'delegate' to 'completion'" in captured.err
        assert state.get_workflow_state()["step"] == "delegate"

    def test_advance_rejects_completion_when_review_incomplete(self, temp_state_dir, clear_state_before, capsys):
        """Completion is refused while the review ledger is still incomplete."""
        state.set_workflow_state(
            name="pull-request-review",
            status="in-progress",
            step="decision",
            context={"pull_request_id": "123"},
        )

        with patch(_PROGRESS, return_value=_progress(all_complete=False, completed=0, pending=39, total=39)):
            with pytest.raises(SystemExit) as exc_info:
                commands.advance_pull_request_review_workflow(step="completion")
            assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "the review was never submitted to the PR" in captured.err
        assert "0/39" in captured.err
        assert state.get_workflow_state()["step"] == "decision"

    def test_advance_rejects_completion_when_no_submit_result(self, temp_state_dir, clear_state_before, capsys):
        """Completion is refused when submit-result.json has not been written (no submission occurred)."""
        state.set_workflow_state(
            name="pull-request-review",
            status="in-progress",
            step="decision",
            context={"pull_request_id": "123"},
        )

        with (
            patch(_PROGRESS, return_value=_progress(all_complete=True, completed=5, pending=0, total=5)),
            patch(_READ_SUBMIT_RESULT, return_value=None),
        ):
            with pytest.raises(SystemExit) as exc_info:
                commands.advance_pull_request_review_workflow(step="completion")
            assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "no submission outcome recorded" in captured.err
        assert "agdt-pr-review-submit" in captured.err
        assert state.get_workflow_state()["step"] == "decision"

    def test_advance_to_completion_triggers_cascade(
        self, temp_state_dir, temp_prompts_dir, temp_output_dir, clear_state_before, capsys
    ):
        """Test advance to completion step triggers status cascade and saves review state."""
        state.set_workflow_state(
            name="pull-request-review",
            status="in-progress",
            step="decision",
            context={"pull_request_id": "123"},
        )

        mock_file_approved = MagicMock()
        mock_file_approved.status = "approved"
        mock_review_state = MagicMock()
        mock_review_state.files = {"/src/a.py": mock_file_approved}
        mock_review_state.repoId = "repo-guid"
        mock_review_state.overallSummary = MagicMock()
        mock_review_state.overallSummary.status = "approved"

        mock_patch_ops = [MagicMock()]

        with (
            patch(_PROGRESS, return_value=_progress(all_complete=True, completed=1, pending=0, total=1)),
            patch(
                "agentic_devtools.cli.azure_devops.review_state.load_review_state",
                return_value=mock_review_state,
            ) as mock_load,
            patch(
                "agentic_devtools.cli.azure_devops.status_cascade.cascade_overall_summary_update",
                return_value=mock_patch_ops,
            ) as mock_cascade,
            patch(
                "agentic_devtools.cli.azure_devops.status_cascade.execute_cascade",
            ) as mock_execute,
            patch(
                "agentic_devtools.cli.azure_devops.review_state.save_review_state",
            ) as mock_save,
            patch(
                "agentic_devtools.cli.azure_devops.auth.get_pat",
                return_value="fake-pat",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.auth.get_auth_headers",
                return_value={"Authorization": "Basic fake"},
            ),
            patch(
                "agentic_devtools.cli.azure_devops.helpers.require_requests",
                return_value=MagicMock(),
            ),
            patch(
                "agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_scaffold.build_pr_base_url",
                return_value="https://dev.azure.com/org/proj/_git/repo/pullrequest/123",
            ),
        ):
            workflow_dir = temp_prompts_dir / "pull-request-review"
            workflow_dir.mkdir()
            template_file = workflow_dir / "default-completion-prompt.md"
            template_file.write_text(
                "Complete! Decision: {{decision}}",
                encoding="utf-8",
            )

            commands.advance_pull_request_review_workflow(step="completion")

        mock_load.assert_called_with(123)
        mock_cascade.assert_called_once()
        mock_execute.assert_called_once()
        mock_save.assert_called_once_with(mock_review_state)

        workflow = state.get_workflow_state()
        assert workflow["step"] == "completion"
        assert workflow["status"] == "completed"

    def test_advance_to_completion_marks_active_session_completed(
        self, temp_state_dir, temp_prompts_dir, temp_output_dir, clear_state_before, capsys
    ):
        """Test completion step marks the in-progress review session as completed.

        Regression test for issue #1181: the review session (and, by extension,
        the Activity Log embedded in the consolidated review comment) must not
        remain stuck at "in_progress" once the workflow reaches completion.
        """
        from agentic_devtools.cli.azure_devops.review_state import (
            FileEntry,
            OverallSummary,
            ReviewSession,
            ReviewState,
        )

        state.set_workflow_state(
            name="pull-request-review",
            status="in-progress",
            step="decision",
            context={"pull_request_id": "123"},
        )

        session = ReviewSession(
            sessionId="session-123",
            modelId="model-a",
            startedUtc="2026-01-01T00:00:00+00:00",
            status="in_progress",
        )
        real_review_state = ReviewState(
            prId=123,
            repoId="repo-guid",
            repoName="repo",
            project="proj",
            organization="https://dev.azure.com/org",
            latestIterationId=1,
            scaffoldedUtc="2026-01-01T00:00:00+00:00",
            overallSummary=OverallSummary(threadId=1, commentId=2, status="approved"),
            files={"/src/a.py": FileEntry(threadId=0, commentId=0, folder="src", fileName="a.py", status="approved")},
            sessions=[session],
        )

        with (
            patch(_PROGRESS, return_value=_progress(all_complete=True, completed=1, pending=0, total=1)),
            patch(
                "agentic_devtools.cli.azure_devops.review_state.load_review_state",
                return_value=real_review_state,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.status_cascade.cascade_overall_summary_update",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.status_cascade.execute_cascade",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_state.save_review_state",
            ) as mock_save,
            patch(
                "agentic_devtools.cli.azure_devops.auth.get_pat",
                return_value="fake-pat",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.auth.get_auth_headers",
                return_value={"Authorization": "Basic fake"},
            ),
            patch(
                "agentic_devtools.cli.azure_devops.helpers.require_requests",
                return_value=MagicMock(),
            ),
            patch(
                "agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_scaffold.build_pr_base_url",
                return_value="https://dev.azure.com/org/proj/_git/repo/pullrequest/123",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.finalization.run_finalization_pass",
                return_value=MagicMock(status="no-op"),
            ),
        ):
            workflow_dir = temp_prompts_dir / "pull-request-review"
            workflow_dir.mkdir()
            template_file = workflow_dir / "default-completion-prompt.md"
            template_file.write_text(
                "Decision: {{decision}}",
                encoding="utf-8",
            )

            commands.advance_pull_request_review_workflow(step="completion")

        assert session.status == "completed"
        assert session.completedUtc is not None
        mock_save.assert_called_once_with(real_review_state)

    def test_advance_to_completion_sets_decision_variable(
        self, temp_state_dir, temp_prompts_dir, temp_output_dir, clear_state_before, capsys
    ):
        """Test decision variable is derived from overall status and rendered in prompt."""
        state.set_workflow_state(
            name="pull-request-review",
            status="in-progress",
            step="decision",
            context={"pull_request_id": "123"},
        )

        mock_file = MagicMock()
        mock_file.status = "approved"
        mock_review_state = MagicMock()
        mock_review_state.files = {"/src/a.py": mock_file}
        mock_review_state.repoId = "repo-guid"
        mock_review_state.overallSummary = MagicMock()
        mock_review_state.overallSummary.status = "approved"

        with (
            patch(_PROGRESS, return_value=_progress(all_complete=True, completed=1, pending=0, total=1)),
            patch(
                "agentic_devtools.cli.azure_devops.review_state.load_review_state",
                return_value=mock_review_state,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.status_cascade.cascade_overall_summary_update",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.status_cascade.execute_cascade",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_state.save_review_state",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.auth.get_pat",
                return_value="fake-pat",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.auth.get_auth_headers",
                return_value={"Authorization": "Basic fake"},
            ),
            patch(
                "agentic_devtools.cli.azure_devops.helpers.require_requests",
                return_value=MagicMock(),
            ),
            patch(
                "agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_scaffold.build_pr_base_url",
                return_value="https://dev.azure.com/org/proj/_git/repo/pullrequest/123",
            ),
        ):
            workflow_dir = temp_prompts_dir / "pull-request-review"
            workflow_dir.mkdir()
            template_file = workflow_dir / "default-completion-prompt.md"
            template_file.write_text(
                "Decision: {{decision}}",
                encoding="utf-8",
            )

            commands.advance_pull_request_review_workflow(step="completion")

        captured = capsys.readouterr()
        assert "✅ Approved" in captured.out

    def test_advance_to_completion_skips_cascade_when_review_state_missing(
        self, temp_state_dir, temp_prompts_dir, temp_output_dir, clear_state_before, capsys
    ):
        """Test workflow still completes when review state file is not found."""
        state.set_workflow_state(
            name="pull-request-review",
            status="in-progress",
            step="decision",
            context={"pull_request_id": "123"},
        )

        with (
            patch(_PROGRESS, return_value=_progress(all_complete=True, completed=1, pending=0, total=1)),
            patch(
                "agentic_devtools.cli.azure_devops.review_state.load_review_state",
                side_effect=FileNotFoundError("review-state.json not found"),
            ),
        ):
            workflow_dir = temp_prompts_dir / "pull-request-review"
            workflow_dir.mkdir()
            template_file = workflow_dir / "default-completion-prompt.md"
            template_file.write_text(
                "Complete! Decision: {{decision}}",
                encoding="utf-8",
            )

            commands.advance_pull_request_review_workflow(step="completion")

        captured = capsys.readouterr()
        assert "Review state not found" in captured.err
        assert "⚠️ Unavailable" in captured.out

        workflow = state.get_workflow_state()
        assert workflow["step"] == "completion"
        assert workflow["status"] == "completed"

    def test_advance_to_completion_continues_on_cascade_error(
        self, temp_state_dir, temp_prompts_dir, temp_output_dir, clear_state_before, capsys
    ):
        """Test workflow completes even when cascade execution fails, and state is saved."""
        state.set_workflow_state(
            name="pull-request-review",
            status="in-progress",
            step="decision",
            context={"pull_request_id": "123"},
        )

        mock_file = MagicMock()
        mock_file.status = "needs-work"
        mock_review_state = MagicMock()
        mock_review_state.files = {"/src/a.py": mock_file}
        mock_review_state.repoId = "repo-guid"
        mock_review_state.overallSummary = MagicMock()
        mock_review_state.overallSummary.status = "needs-work"

        with (
            patch(_PROGRESS, return_value=_progress(all_complete=True, completed=1, pending=0, total=1)),
            patch(
                "agentic_devtools.cli.azure_devops.review_state.load_review_state",
                return_value=mock_review_state,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.status_cascade.cascade_overall_summary_update",
                return_value=[MagicMock()],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.status_cascade.execute_cascade",
                side_effect=RuntimeError("API call failed"),
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_state.save_review_state",
            ) as mock_save,
            patch(
                "agentic_devtools.cli.azure_devops.auth.get_pat",
                return_value="fake-pat",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.auth.get_auth_headers",
                return_value={"Authorization": "Basic fake"},
            ),
            patch(
                "agentic_devtools.cli.azure_devops.helpers.require_requests",
                return_value=MagicMock(),
            ),
            patch(
                "agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_scaffold.build_pr_base_url",
                return_value="https://dev.azure.com/org/proj/_git/repo/pullrequest/123",
            ),
        ):
            workflow_dir = temp_prompts_dir / "pull-request-review"
            workflow_dir.mkdir()
            template_file = workflow_dir / "default-completion-prompt.md"
            template_file.write_text(
                "Complete! Decision: {{decision}}",
                encoding="utf-8",
            )

            commands.advance_pull_request_review_workflow(step="completion")

        captured = capsys.readouterr()
        assert "Failed to update PR summary" in captured.err

        # Decision should still be derived even though cascade failed
        assert "📝 Needs Work" in captured.out

        # save_review_state should still be called (finally block)
        mock_save.assert_called_once_with(mock_review_state)

        workflow = state.get_workflow_state()
        assert workflow["step"] == "completion"
        assert workflow["status"] == "completed"

    def test_advance_to_completion_handles_malformed_state_gracefully(
        self, temp_state_dir, temp_prompts_dir, temp_output_dir, clear_state_before, capsys
    ):
        """Test workflow completes even when cascade raises ValueError/KeyError from bad state."""
        state.set_workflow_state(
            name="pull-request-review",
            status="in-progress",
            step="decision",
            context={"pull_request_id": "123"},
        )

        with (
            patch(_PROGRESS, return_value=_progress(all_complete=True, completed=1, pending=0, total=1)),
            patch(
                "agentic_devtools.cli.azure_devops.review_state.load_review_state",
                side_effect=ValueError("malformed review state"),
            ),
        ):
            workflow_dir = temp_prompts_dir / "pull-request-review"
            workflow_dir.mkdir()
            template_file = workflow_dir / "default-completion-prompt.md"
            template_file.write_text(
                "Complete! Decision: {{decision}}",
                encoding="utf-8",
            )

            commands.advance_pull_request_review_workflow(step="completion")

        captured = capsys.readouterr()
        assert "Could not update PR summary" in captured.err
        assert "⚠️ Unavailable" in captured.out

        workflow = state.get_workflow_state()
        assert workflow["step"] == "completion"
        assert workflow["status"] == "completed"

    def test_advance_to_completion_calls_finalization(
        self, temp_state_dir, temp_prompts_dir, temp_output_dir, clear_state_before, capsys
    ):
        """Test finalization pass is called after cascade during completion."""
        state.set_workflow_state(
            name="pull-request-review",
            status="in-progress",
            step="decision",
            context={"pull_request_id": "123"},
        )

        mock_file = MagicMock()
        mock_file.status = "approved"
        mock_review_state = MagicMock()
        mock_review_state.files = {"/src/a.py": mock_file}
        mock_review_state.repoId = "repo-guid"
        mock_review_state.overallSummary = MagicMock()
        mock_review_state.overallSummary.status = "approved"

        mock_fin_report = MagicMock()
        mock_fin_report.status = "no-op"

        with (
            patch(_PROGRESS, return_value=_progress(all_complete=True, completed=1, pending=0, total=1)),
            patch(
                "agentic_devtools.cli.azure_devops.review_state.load_review_state",
                return_value=mock_review_state,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.status_cascade.cascade_overall_summary_update",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.status_cascade.execute_cascade",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_state.save_review_state",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.auth.get_pat",
                return_value="fake-pat",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.auth.get_auth_headers",
                return_value={"Authorization": "Basic fake"},
            ),
            patch(
                "agentic_devtools.cli.azure_devops.helpers.require_requests",
                return_value=MagicMock(),
            ),
            patch(
                "agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_scaffold.build_pr_base_url",
                return_value="https://dev.azure.com/org/proj/_git/repo/pullrequest/123",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.finalization.run_finalization_pass",
                return_value=mock_fin_report,
            ) as mock_finalization,
            patch(
                "agentic_devtools.state.is_dry_run",
                return_value=False,
            ),
        ):
            workflow_dir = temp_prompts_dir / "pull-request-review"
            workflow_dir.mkdir()
            template_file = workflow_dir / "default-completion-prompt.md"
            template_file.write_text(
                "Decision: {{decision}}",
                encoding="utf-8",
            )

            commands.advance_pull_request_review_workflow(step="completion")

        # Finalization was called
        mock_finalization.assert_called_once()

        # Workflow completes successfully
        workflow = state.get_workflow_state()
        assert workflow["step"] == "completion"
        assert workflow["status"] == "completed"

    def test_advance_to_completion_non_blocking_on_finalization_error(
        self, temp_state_dir, temp_prompts_dir, temp_output_dir, clear_state_before, capsys
    ):
        """Test workflow completes even when finalization raises an exception."""
        state.set_workflow_state(
            name="pull-request-review",
            status="in-progress",
            step="decision",
            context={"pull_request_id": "123"},
        )

        mock_file = MagicMock()
        mock_file.status = "approved"
        mock_review_state = MagicMock()
        mock_review_state.files = {"/src/a.py": mock_file}
        mock_review_state.repoId = "repo-guid"
        mock_review_state.overallSummary = MagicMock()
        mock_review_state.overallSummary.status = "approved"

        with (
            patch(_PROGRESS, return_value=_progress(all_complete=True, completed=1, pending=0, total=1)),
            patch(
                "agentic_devtools.cli.azure_devops.review_state.load_review_state",
                return_value=mock_review_state,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.status_cascade.cascade_overall_summary_update",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.status_cascade.execute_cascade",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_state.save_review_state",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.auth.get_pat",
                return_value="fake-pat",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.auth.get_auth_headers",
                return_value={"Authorization": "Basic fake"},
            ),
            patch(
                "agentic_devtools.cli.azure_devops.helpers.require_requests",
                return_value=MagicMock(),
            ),
            patch(
                "agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_scaffold.build_pr_base_url",
                return_value="https://dev.azure.com/org/proj/_git/repo/pullrequest/123",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.finalization.run_finalization_pass",
                side_effect=RuntimeError("finalization crash"),
            ),
            patch(
                "agentic_devtools.state.is_dry_run",
                return_value=False,
            ),
        ):
            workflow_dir = temp_prompts_dir / "pull-request-review"
            workflow_dir.mkdir()
            template_file = workflow_dir / "default-completion-prompt.md"
            template_file.write_text(
                "Decision: {{decision}}",
                encoding="utf-8",
            )

            commands.advance_pull_request_review_workflow(step="completion")

        captured = capsys.readouterr()
        assert "Finalization pass failed" in captured.err

        # Decision should still be correct even though finalization failed
        assert "✅ Approved" in captured.out

        # Workflow should still complete
        workflow = state.get_workflow_state()
        assert workflow["step"] == "completion"
        assert workflow["status"] == "completed"

    def test_advance_to_completion_skips_session_completion_in_dry_run(
        self, temp_state_dir, temp_prompts_dir, temp_output_dir, clear_state_before, capsys
    ):
        """Dry-run mode must not mark the review session as completed.

        Regression guard for issue #1181: preview renders (dry_run=True) must
        not persist a ``"completed"`` status to the saved ReviewSession, because
        nothing was actually posted to ADO and the session should remain
        ``"in_progress"`` from the perspective of a subsequent live run.
        """
        from agentic_devtools.cli.azure_devops.review_state import (
            FileEntry,
            OverallSummary,
            ReviewSession,
            ReviewState,
        )

        state.set_workflow_state(
            name="pull-request-review",
            status="in-progress",
            step="decision",
            context={"pull_request_id": "123"},
        )

        session = ReviewSession(
            sessionId="session-dry",
            modelId="model-a",
            startedUtc="2026-01-01T00:00:00+00:00",
            status="in_progress",
        )
        real_review_state = ReviewState(
            prId=123,
            repoId="repo-guid",
            repoName="repo",
            project="proj",
            organization="https://dev.azure.com/org",
            latestIterationId=1,
            scaffoldedUtc="2026-01-01T00:00:00+00:00",
            overallSummary=OverallSummary(threadId=1, commentId=2, status="approved"),
            files={"/src/a.py": FileEntry(threadId=0, commentId=0, folder="src", fileName="a.py", status="approved")},
            sessions=[session],
        )

        with (
            patch(_PROGRESS, return_value=_progress(all_complete=True, completed=1, pending=0, total=1)),
            patch(
                "agentic_devtools.cli.azure_devops.review_state.load_review_state",
                return_value=real_review_state,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.status_cascade.cascade_overall_summary_update",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.status_cascade.execute_cascade",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_state.save_review_state",
            ) as mock_save,
            patch(
                "agentic_devtools.cli.azure_devops.auth.get_pat",
                return_value="fake-pat",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.auth.get_auth_headers",
                return_value={"Authorization": "Basic fake"},
            ),
            patch(
                "agentic_devtools.cli.azure_devops.helpers.require_requests",
                return_value=MagicMock(),
            ),
            patch(
                "agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_scaffold.build_pr_base_url",
                return_value="https://dev.azure.com/org/proj/_git/repo/pullrequest/123",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.finalization.run_finalization_pass",
                return_value=MagicMock(status="no-op"),
            ),
            patch(
                "agentic_devtools.state.is_dry_run",
                return_value=True,
            ),
        ):
            workflow_dir = temp_prompts_dir / "pull-request-review"
            workflow_dir.mkdir()
            template_file = workflow_dir / "default-completion-prompt.md"
            template_file.write_text(
                "Decision: {{decision}}",
                encoding="utf-8",
            )

            commands.advance_pull_request_review_workflow(step="completion")

        # Session must remain in_progress — dry-run must not mutate saved state
        assert session.status == "in_progress"
        assert session.completedUtc is None
        mock_save.assert_called_once_with(real_review_state)

    def test_advance_to_completion_saves_state_when_cascade_overall_raises(
        self, temp_state_dir, temp_prompts_dir, temp_output_dir, clear_state_before, capsys
    ):
        """Session completion must be saved even if cascade_overall_summary_update raises.

        Regression guard for issue #1181: if the render/cascade step throws, the
        ``complete_active_session()`` mutation must still be flushed to disk via
        the inner try/finally ``save_review_state()`` call, so a subsequent live
        run sees the terminal status rather than re-entering the stuck
        ``"in_progress"`` state.
        """
        from agentic_devtools.cli.azure_devops.review_state import (
            FileEntry,
            OverallSummary,
            ReviewSession,
            ReviewState,
        )

        state.set_workflow_state(
            name="pull-request-review",
            status="in-progress",
            step="decision",
            context={"pull_request_id": "123"},
        )

        session = ReviewSession(
            sessionId="session-cascade-err",
            modelId="model-a",
            startedUtc="2026-01-01T00:00:00+00:00",
            status="in_progress",
        )
        real_review_state = ReviewState(
            prId=123,
            repoId="repo-guid",
            repoName="repo",
            project="proj",
            organization="https://dev.azure.com/org",
            latestIterationId=1,
            scaffoldedUtc="2026-01-01T00:00:00+00:00",
            overallSummary=OverallSummary(threadId=1, commentId=2, status="approved"),
            files={"/src/a.py": FileEntry(threadId=0, commentId=0, folder="src", fileName="a.py", status="approved")},
            sessions=[session],
        )

        with (
            patch(_PROGRESS, return_value=_progress(all_complete=True, completed=1, pending=0, total=1)),
            patch(
                "agentic_devtools.cli.azure_devops.review_state.load_review_state",
                return_value=real_review_state,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.status_cascade.cascade_overall_summary_update",
                side_effect=RuntimeError("render error"),
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_state.save_review_state",
            ) as mock_save,
            patch(
                "agentic_devtools.cli.azure_devops.auth.get_pat",
                return_value="fake-pat",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.auth.get_auth_headers",
                return_value={"Authorization": "Basic fake"},
            ),
            patch(
                "agentic_devtools.cli.azure_devops.helpers.require_requests",
                return_value=MagicMock(),
            ),
            patch(
                "agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_scaffold.build_pr_base_url",
                return_value="https://dev.azure.com/org/proj/_git/repo/pullrequest/123",
            ),
            patch(
                "agentic_devtools.state.is_dry_run",
                return_value=False,
            ),
        ):
            workflow_dir = temp_prompts_dir / "pull-request-review"
            workflow_dir.mkdir()
            template_file = workflow_dir / "default-completion-prompt.md"
            template_file.write_text(
                "Decision: {{decision}}",
                encoding="utf-8",
            )

            commands.advance_pull_request_review_workflow(step="completion")

        captured = capsys.readouterr()
        assert "Failed to update PR summary" in captured.err

        # Session should be completed even though cascade raised
        assert session.status == "completed"
        assert session.completedUtc is not None

        # State must be persisted via the finally block
        mock_save.assert_called_once_with(real_review_state)

        # Workflow should still complete
        workflow = state.get_workflow_state()
        assert workflow["step"] == "completion"
        assert workflow["status"] == "completed"

    def test_advance_to_completion_completes_session_when_auth_setup_fails(
        self, temp_state_dir, temp_prompts_dir, temp_output_dir, clear_state_before, capsys
    ):
        """Session completion should persist even when auth setup for cascade fails."""
        from agentic_devtools.cli.azure_devops.review_state import (
            FileEntry,
            OverallSummary,
            ReviewSession,
            ReviewState,
        )

        state.set_workflow_state(
            name="pull-request-review",
            status="in-progress",
            step="decision",
            context={"pull_request_id": "123"},
        )

        session = ReviewSession(
            sessionId="session-auth-err",
            modelId="model-a",
            startedUtc="2026-01-01T00:00:00+00:00",
            status="in_progress",
        )
        real_review_state = ReviewState(
            prId=123,
            repoId="repo-guid",
            repoName="repo",
            project="proj",
            organization="https://dev.azure.com/org",
            latestIterationId=1,
            scaffoldedUtc="2026-01-01T00:00:00+00:00",
            overallSummary=OverallSummary(threadId=1, commentId=2, status="approved"),
            files={"/src/a.py": FileEntry(threadId=0, commentId=0, folder="src", fileName="a.py", status="approved")},
            sessions=[session],
        )

        with (
            patch(_PROGRESS, return_value=_progress(all_complete=True, completed=1, pending=0, total=1)),
            patch(
                "agentic_devtools.cli.azure_devops.review_state.load_review_state",
                return_value=real_review_state,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_state.save_review_state",
            ) as mock_save,
            patch(
                "agentic_devtools.cli.azure_devops.auth.get_pat",
                side_effect=RuntimeError("missing PAT"),
            ),
            patch(
                "agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_scaffold.build_pr_base_url",
                return_value="https://dev.azure.com/org/proj/_git/repo/pullrequest/123",
            ),
            patch(
                "agentic_devtools.state.is_dry_run",
                return_value=False,
            ),
        ):
            workflow_dir = temp_prompts_dir / "pull-request-review"
            workflow_dir.mkdir()
            template_file = workflow_dir / "default-completion-prompt.md"
            template_file.write_text(
                "Decision: {{decision}}",
                encoding="utf-8",
            )

            commands.advance_pull_request_review_workflow(step="completion")

        captured = capsys.readouterr()
        assert "Failed to update PR summary" in captured.err
        assert "✅ Approved" in captured.out
        assert session.status == "completed"
        assert session.completedUtc is not None
        mock_save.assert_called_once_with(real_review_state)

    def test_advance_to_completion_persists_session_when_config_setup_fails(
        self, temp_state_dir, temp_prompts_dir, temp_output_dir, clear_state_before, capsys
    ):
        """Session completion should persist even when config/base-url setup fails."""
        from agentic_devtools.cli.azure_devops.review_state import (
            FileEntry,
            OverallSummary,
            ReviewSession,
            ReviewState,
        )

        state.set_workflow_state(
            name="pull-request-review",
            status="in-progress",
            step="decision",
            context={"pull_request_id": "123"},
        )

        session = ReviewSession(
            sessionId="session-config-err",
            modelId="model-a",
            startedUtc="2026-01-01T00:00:00+00:00",
            status="in_progress",
        )
        real_review_state = ReviewState(
            prId=123,
            repoId="repo-guid",
            repoName="repo",
            project="proj",
            organization="https://dev.azure.com/org",
            latestIterationId=1,
            scaffoldedUtc="2026-01-01T00:00:00+00:00",
            overallSummary=OverallSummary(threadId=1, commentId=2, status="approved"),
            files={"/src/a.py": FileEntry(threadId=0, commentId=0, folder="src", fileName="a.py", status="approved")},
            sessions=[session],
        )

        with (
            patch(_PROGRESS, return_value=_progress(all_complete=True, completed=1, pending=0, total=1)),
            patch(
                "agentic_devtools.cli.azure_devops.review_state.load_review_state",
                return_value=real_review_state,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_state.save_review_state",
            ) as mock_save,
            patch(
                "agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state",
                side_effect=RuntimeError("missing config"),
            ),
            patch(
                "agentic_devtools.state.is_dry_run",
                return_value=False,
            ),
        ):
            workflow_dir = temp_prompts_dir / "pull-request-review"
            workflow_dir.mkdir()
            template_file = workflow_dir / "default-completion-prompt.md"
            template_file.write_text(
                "Decision: {{decision}}",
                encoding="utf-8",
            )

            commands.advance_pull_request_review_workflow(step="completion")

        captured = capsys.readouterr()
        assert "Failed to update PR summary" in captured.err
        assert "✅ Approved" in captured.out
        assert session.status == "completed"
        assert session.completedUtc is not None
        mock_save.assert_called_once_with(real_review_state)
