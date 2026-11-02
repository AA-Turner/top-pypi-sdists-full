"""Tests for handing current-run session evidence to the pipeline summary."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.agent_task_inventory import FailureCategory
from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult
from agentic_devtools.cli.ci.pipeline.runner import run_pipeline
from agentic_devtools.cli.ci.pipeline.session_detector import SessionOutcome, SessionState
from agentic_devtools.cli.ci.pipeline.snapshot_models import PRStateSnapshot
from tests.unit.cli.ci.pipeline._runner_fixtures import _MockAction


class _RecordSessionStateAction:
    """Make typed session state available only in the current pipeline run."""

    name = "retry_failed_session"

    def __init__(self, state: SessionState) -> None:
        self._state = state

    def evaluate(self, _snapshot, derived) -> ActionResult:
        derived.set("latest_session_state", self._state)
        return ActionResult(self.name, ActionDecision.SKIP)

    def execute(self, _provider, _snapshot, _derived) -> ActionResult:
        raise AssertionError("a skipped action must not execute")


@pytest.mark.parametrize(
    "state",
    [
        SessionState(
            SessionOutcome.UNKNOWN,
            failure_category=FailureCategory.HTTP_NOT_FOUND,
            http_status=404,
            failure_source="agent-task-inventory",
        ),
        SessionState(SessionOutcome.ACTIVE, task_id="task-verified"),
        SessionState(SessionOutcome.ACTIVE),
    ],
)
def test_run_pipeline_hands_off_only_current_run_typed_session_state(state: SessionState) -> None:
    provider = MagicMock()
    with (
        patch("agentic_devtools.cli.ci.pipeline.runner.reconcile_agent_task_lifecycles"),
        patch("agentic_devtools.cli.ci.pipeline.runner._find_recent_diff_preservation_blocker", return_value=None),
    ):
        summary = run_pipeline(
            provider,
            PRStateSnapshot(pr_number=42),
            [
                _RecordSessionStateAction(state),
                _MockAction("approve", ActionDecision.SKIP),
            ],
        )

    assert summary.session_evidence is state
    assert [result.decision for result in summary.results] == [ActionDecision.SKIP, ActionDecision.SKIP]
    provider.list_agent_tasks.assert_not_called()
    provider.list_pr_agent_task_lifecycles.assert_not_called()


def test_run_pipeline_does_not_carry_session_evidence_between_runs() -> None:
    provider = MagicMock()
    with (
        patch("agentic_devtools.cli.ci.pipeline.runner.reconcile_agent_task_lifecycles"),
        patch("agentic_devtools.cli.ci.pipeline.runner._find_recent_diff_preservation_blocker", return_value=None),
    ):
        summary = run_pipeline(provider, PRStateSnapshot(pr_number=42), [_MockAction("approve", ActionDecision.SKIP)])

    assert summary.session_evidence is None
    assert summary.results[0].decision is ActionDecision.SKIP
