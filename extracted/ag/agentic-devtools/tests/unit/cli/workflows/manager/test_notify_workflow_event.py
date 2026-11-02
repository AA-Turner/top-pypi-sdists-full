"""Tests for notify_workflow_event function."""

from unittest.mock import patch

from agentic_devtools.cli.workflows.manager import (
    NotifyEventResult,
    WorkflowDefinition,
    WorkflowEvent,
    WorkflowTransition,
    notify_workflow_event,
)


class TestNotifyWorkflowEvent:
    """Tests for notify_workflow_event function."""

    def test_returns_not_triggered_when_no_workflow_active(self):
        """Should return triggered=False when no workflow is active in state."""
        with patch(
            "agentic_devtools.cli.workflows.manager.get_workflow_state",
            return_value=None,
        ):
            result = notify_workflow_event(WorkflowEvent.MANUAL_ADVANCE)

        assert isinstance(result, NotifyEventResult)
        assert result.triggered is False

    def test_returns_not_triggered_when_workflow_has_no_step(self):
        """Should return triggered=False when workflow is active but has no step."""
        with patch(
            "agentic_devtools.cli.workflows.manager.get_workflow_state",
            return_value={"active": "work-on-jira-issue", "step": None},
        ):
            result = notify_workflow_event(WorkflowEvent.MANUAL_ADVANCE)

        assert result.triggered is False

    def test_returns_not_triggered_for_unknown_workflow(self):
        """Should return triggered=False when workflow definition is not found."""
        with patch(
            "agentic_devtools.cli.workflows.manager.get_workflow_state",
            return_value={"active": "nonexistent-workflow", "step": "some-step"},
        ):
            with patch(
                "agentic_devtools.cli.workflows.manager.get_workflow_definition",
                return_value=None,
            ):
                result = notify_workflow_event(WorkflowEvent.MANUAL_ADVANCE)

        assert result.triggered is False

    def test_returns_notify_event_result_instance(self):
        """Return value should always be a NotifyEventResult instance."""
        with patch(
            "agentic_devtools.cli.workflows.manager.get_workflow_state",
            return_value=None,
        ):
            result = notify_workflow_event(WorkflowEvent.MANUAL_ADVANCE)

        assert isinstance(result, NotifyEventResult)

    def test_auto_advance_false_saves_context_without_advancing(self):
        """Should save updated context but not advance when auto_advance is False."""
        definition = WorkflowDefinition(
            name="test-workflow",
            transitions=[
                WorkflowTransition(
                    from_step="step-a",
                    to_step="step-b",
                    trigger_events={WorkflowEvent.MANUAL_ADVANCE},
                    auto_advance=False,
                ),
            ],
        )

        with patch(
            "agentic_devtools.cli.workflows.manager.get_workflow_state",
            return_value={
                "active": "test-workflow",
                "step": "step-a",
                "status": "in-progress",
                "context": {},
            },
        ):
            with patch(
                "agentic_devtools.cli.workflows.manager.get_workflow_definition",
                return_value=definition,
            ):
                with patch(
                    "agentic_devtools.cli.workflows.manager.set_workflow_state",
                ) as mock_set:
                    result = notify_workflow_event(WorkflowEvent.MANUAL_ADVANCE)

        assert result.triggered is True
        assert result.immediate_advance is False
        # Should save state with current step (not advanced)
        mock_set.assert_called_once()
        call_kwargs = mock_set.call_args[1]
        assert call_kwargs["step"] == "step-a"

    def test_returns_not_triggered_when_no_matching_transition(self):
        """No transition for the current step + event yields triggered=False."""
        definition = WorkflowDefinition(
            name="test-workflow",
            transitions=[
                WorkflowTransition(
                    from_step="step-a",
                    to_step="step-b",
                    trigger_events={WorkflowEvent.MANUAL_ADVANCE},
                ),
            ],
        )

        with (
            patch(
                "agentic_devtools.cli.workflows.manager.get_workflow_state",
                return_value={"active": "test-workflow", "step": "other", "context": {}},
            ),
            patch(
                "agentic_devtools.cli.workflows.manager.get_workflow_definition",
                return_value=definition,
            ),
        ):
            result = notify_workflow_event(WorkflowEvent.MANUAL_ADVANCE)

        assert result.triggered is False

    def test_auto_advance_no_tasks_renders_prompt_immediately(self, tmp_path):
        """Auto-advance with no required tasks advances + renders the next prompt."""
        definition = WorkflowDefinition(
            name="test-workflow",
            transitions=[
                WorkflowTransition(
                    from_step="step-a",
                    to_step="step-b",
                    trigger_events={WorkflowEvent.MANUAL_ADVANCE},
                    auto_advance=True,
                ),
            ],
        )

        with (
            patch(
                "agentic_devtools.cli.workflows.manager.get_workflow_state",
                return_value={
                    "active": "test-workflow",
                    "step": "step-a",
                    "status": "in-progress",
                    "context": {},
                },
            ),
            patch(
                "agentic_devtools.cli.workflows.manager.get_workflow_definition",
                return_value=definition,
            ),
            patch("agentic_devtools.cli.workflows.manager.set_workflow_state") as mock_set,
            patch(
                "agentic_devtools.cli.workflows.manager._render_step_prompt",
                return_value="next prompt body",
            ),
            patch(
                "agentic_devtools.cli.workflows.manager.get_temp_output_dir",
                return_value=tmp_path,
            ),
        ):
            result = notify_workflow_event(
                WorkflowEvent.MANUAL_ADVANCE,
                context_updates={"pull_request_id": 7},
            )

        assert result.triggered is True
        assert result.immediate_advance is True
        assert result.prompt_rendered is True
        assert result.new_step == "step-b"
        mock_set.assert_called_once()

    def test_auto_advance_with_required_tasks_defers_pending_transition(self):
        """Auto-advance with required tasks records a pending_transition (no immediate advance)."""
        definition = WorkflowDefinition(
            name="test-workflow",
            transitions=[
                WorkflowTransition(
                    from_step="step-a",
                    to_step="step-b",
                    trigger_events={WorkflowEvent.MANUAL_ADVANCE},
                    required_tasks=["agdt-some-task"],
                    auto_advance=True,
                ),
            ],
        )

        captured: dict[str, object] = {}

        def _capture(**kwargs):
            captured.update(kwargs)

        with (
            patch(
                "agentic_devtools.cli.workflows.manager.get_workflow_state",
                return_value={
                    "active": "test-workflow",
                    "step": "step-a",
                    "status": "in-progress",
                    "context": {},
                },
            ),
            patch(
                "agentic_devtools.cli.workflows.manager.get_workflow_definition",
                return_value=definition,
            ),
            patch("agentic_devtools.cli.workflows.manager.set_workflow_state", side_effect=_capture),
        ):
            result = notify_workflow_event(WorkflowEvent.MANUAL_ADVANCE)

        assert result.triggered is True
        assert result.immediate_advance is False
        assert captured["step"] == "step-a"
        assert captured["context"]["pending_transition"]["to_step"] == "step-b"
