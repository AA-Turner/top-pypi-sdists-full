"""Runner integration test for the refreshed-head validation-evidence gate."""

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.ci.pipeline.actions.validation_evidence_gate import ValidationEvidenceGateAction
from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult
from agentic_devtools.cli.ci.pipeline.runner import run_pipeline
from agentic_devtools.cli.ci.pipeline.snapshot_models import DerivedState, PRStateSnapshot
from agentic_devtools.cli.ci.pipeline.validation_evidence import EVIDENCE_REQUIRED_LABEL
from agentic_devtools.cli.ci.provider import CIPlatformProvider

INITIAL_SHA = "1111111111111111111111111111111111111111"
PREPARED_SHA = "2222222222222222222222222222222222222222"


class _PrepareAction:
    """Test double for a branch-preparation action that invalidates the snapshot."""

    name = "prepare_branch"

    def __init__(self) -> None:
        self.evaluated_sha = ""
        self.executed_sha = ""

    def evaluate(self, snapshot: PRStateSnapshot, _derived: DerivedState) -> ActionResult:
        self.evaluated_sha = snapshot.head_sha
        return ActionResult(self.name, ActionDecision.EXECUTE)

    def execute(
        self,
        _provider: CIPlatformProvider,
        snapshot: PRStateSnapshot,
        _derived: DerivedState,
    ) -> ActionResult:
        self.executed_sha = snapshot.head_sha
        return ActionResult(self.name, ActionDecision.EXECUTE, invalidates_snapshot=True)


def test_gate_executes_against_the_refreshed_prepared_head() -> None:
    initial = PRStateSnapshot(
        pr_number=42,
        head_sha=INITIAL_SHA,
        head_branch="feature/validation",
        base_repo_full_name="owner/repo",
        labels=[EVIDENCE_REQUIRED_LABEL],
        is_draft=True,
        has_changes=True,
    )
    refreshed = PRStateSnapshot(
        pr_number=42,
        head_sha=PREPARED_SHA,
        head_branch="feature/validation",
        base_repo_full_name="owner/repo",
        labels=[EVIDENCE_REQUIRED_LABEL],
        is_draft=True,
        has_changes=True,
    )
    provider = MagicMock()
    provider.get_pr_metadata.return_value = SimpleNamespace(head_sha=PREPARED_SHA)
    provider.list_issue_comments.return_value = []
    prepare = _PrepareAction()
    gate = ValidationEvidenceGateAction()

    with (
        patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            return_value=refreshed,
        ) as refresh,
        patch(
            "agentic_devtools.cli.ci.pipeline.runner._find_recent_diff_preservation_blocker",
            return_value=None,
        ),
        patch(
            "agentic_devtools.cli.ci.pipeline.runner._find_recent_conflict_repair_head",
            return_value="",
        ),
        patch("agentic_devtools.cli.ci.pipeline.runner.reconcile_agent_task_lifecycles"),
        patch(
            "agentic_devtools.cli.ci.pipeline.runner.validate_diff_preservation",
            return_value=SimpleNamespace(valid=True, missing_files=[], reason=""),
        ),
        patch(
            "agentic_devtools.cli.ci.pipeline.actions.validation_evidence_gate.is_copilot_session_active_via_agent_task",
            return_value=False,
        ) as active_session,
    ):
        summary = run_pipeline(provider, initial, [prepare, gate])

    assert refresh.call_count == 1
    refresh.assert_called_once_with(provider, 42, actionable_check_names=None)
    assert prepare.evaluated_sha == INITIAL_SHA
    assert prepare.executed_sha == INITIAL_SHA
    assert summary.snapshot is not None
    assert summary.snapshot.head_sha == PREPARED_SHA
    assert summary.results[1].decision is ActionDecision.EXECUTE
    active_session.assert_called_once_with(
        "owner/repo",
        42,
        head_branch="feature/validation",
        pr_id=None,
        head_sha=PREPARED_SHA,
        provider=provider,
    )
    provider.post_comment.assert_called_once()
    assert PREPARED_SHA in provider.post_comment.call_args.args[1]
