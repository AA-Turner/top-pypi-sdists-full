"""Tests for WorkflowRun dataclass."""

from agentic_devtools.cli.ci.reconciliation.models import WorkflowRun


class TestWorkflowRun:
    """Tests for WorkflowRun dataclass."""

    def test_creation_with_required_fields(self) -> None:
        """WorkflowRun can be created with all required fields."""
        run = WorkflowRun(
            id=123,
            name="CI Build",
            conclusion="failure",
            run_attempt=1,
            created_at="2024-01-15T10:00:00Z",
            event="push",
            head_branch="main",
        )
        assert run.id == 123
        assert run.name == "CI Build"
        assert run.conclusion == "failure"
        assert run.run_attempt == 1
        assert run.created_at == "2024-01-15T10:00:00Z"
        assert run.event == "push"
        assert run.head_branch == "main"

    def test_optional_fields_default_to_empty(self) -> None:
        """Optional fields default to empty strings."""
        run = WorkflowRun(
            id=1,
            name="test",
            conclusion="success",
            run_attempt=1,
            created_at="2024-01-01T00:00:00Z",
            event="push",
            head_branch="main",
        )
        assert run.html_url == ""
        assert run.triggering_actor == ""
        assert run.repository_full_name == ""
        assert run.status == ""
        assert run.run_started_at == ""
        assert run.head_sha == ""
        assert run.workflow_id == ""
        assert run.task_id == ""
        assert run.session_id == ""

    def test_lifecycle_fields_preserve_run_identity_and_start(self) -> None:
        """Stores the run status, actual start, head SHA, and discovered workflow ID."""
        run = WorkflowRun(
            id=1,
            name="Copilot",
            conclusion="",
            run_attempt=2,
            created_at="2026-10-16T08:00:00Z",
            event="workflow_dispatch",
            head_branch="copilot/pr-42",
            status="in_progress",
            run_started_at="2026-10-16T08:01:00Z",
            head_sha="a" * 40,
            workflow_id="294804460",
            task_id="task-1",
            session_id="session-1",
        )

        assert run.status == "in_progress"
        assert run.run_started_at == "2026-10-16T08:01:00Z"
        assert run.head_sha == "a" * 40
        assert run.workflow_id == "294804460"
        assert run.task_id == "task-1"
        assert run.session_id == "session-1"

    def test_frozen(self) -> None:
        """WorkflowRun is immutable."""
        run = WorkflowRun(
            id=1,
            name="test",
            conclusion="success",
            run_attempt=1,
            created_at="2024-01-01T00:00:00Z",
            event="push",
            head_branch="main",
        )
        import pytest

        with pytest.raises(AttributeError):
            run.id = 999  # type: ignore[misc]
