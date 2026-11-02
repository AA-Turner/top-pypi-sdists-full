"""Integration regression for WIP delivery gates across pipeline publication paths."""

from unittest.mock import Mock, patch

import pytest

from agentic_devtools.cli.ci.models import PRMetadata
from agentic_devtools.cli.ci.pipeline.actions import GuardsAction, PublishAction, SquashAction
from agentic_devtools.cli.ci.pipeline.models import ActionDecision
from agentic_devtools.cli.ci.pipeline.runner import run_pipeline
from agentic_devtools.cli.ci.pipeline.session_detector import SessionOutcome, SessionState
from agentic_devtools.cli.ci.pipeline.snapshot_models import DerivedState, PRStateSnapshot


def test_unknown_wip_delivery_blocks_publish_even_when_downstream_squash_runs() -> None:
    snapshot = PRStateSnapshot(
        pr_number=42,
        head_sha="head-sha",
        base_branch="main",
        head_branch="feature",
        commit_count=3,
        ci_status="passing",
        review_state="APPROVED",
        unresolved_threads=0,
        is_draft=True,
        title="[WIP] completed work",
        files=["src/main.py"],
        has_changes=True,
        base_repo_full_name="owner/repo",
        head_repo_full_name="owner/repo",
    )
    provider = Mock()
    provider.get_pr_metadata.return_value = PRMetadata(
        number=42,
        title=snapshot.title,
        head_branch="feature",
        head_sha="head-sha",
        base_branch="main",
        is_draft=True,
        changed_files=1,
    )
    provider.get_ref_sha.return_value = "base-sha"
    provider.list_pr_files_complete.return_value = None

    with (
        patch(
            "agentic_devtools.cli.ci.pipeline.runner.reconcile_agent_task_lifecycles",
        ),
        patch(
            "agentic_devtools.cli.ci.pipeline.actions.guards.get_latest_session_state",
            return_value=SessionState(SessionOutcome.FINISHED),
        ),
        patch(
            "agentic_devtools.cli.ci.pipeline.actions.publish.is_copilot_session_active_via_agent_task",
            return_value=False,
        ),
        patch(
            "agentic_devtools.cli.ci.pipeline.actions.squash.is_copilot_session_active_via_agent_task",
            return_value=False,
        ),
    ):
        summary = run_pipeline(provider, snapshot, [GuardsAction(), PublishAction(), SquashAction()])

    assert [result.decision for result in summary.results] == [
        ActionDecision.EXECUTE,
        ActionDecision.SKIP,
        ActionDecision.EXECUTE,
    ]
    assert provider.list_pr_files_complete.call_count == 1
    provider.squash_before_publish.assert_not_called()
    provider.squash_post_repair.assert_called_once()
    provider.update_pr_title.assert_not_called()
    provider.publish_pr.assert_not_called()


@pytest.mark.parametrize(
    ("retry_inventory", "retry_changed_files", "should_publish_on_retry"),
    [
        ([], 0, False),
        (None, 1, False),
        (["src/main.py"], 1, True),
    ],
)
def test_retry_rechecks_real_delivery_evidence_after_title_normalization(
    retry_inventory: list[str] | None,
    retry_changed_files: int,
    should_publish_on_retry: bool,
) -> None:
    snapshot = PRStateSnapshot(
        pr_number=42,
        head_sha="head-sha",
        base_branch="main",
        head_branch="feature",
        is_draft=True,
        title="[WIP] completed work",
        files=["src/main.py"],
        has_changes=True,
    )
    provider = Mock()
    initial_metadata = PRMetadata(
        number=42,
        title=snapshot.title,
        head_branch="feature",
        head_sha="head-sha",
        base_branch="main",
        changed_files=1,
    )
    retry_metadata = PRMetadata(
        number=42,
        title="completed work",
        head_branch="feature",
        head_sha="head-sha",
        base_branch="main",
        changed_files=retry_changed_files,
    )
    provider.get_pr_metadata.side_effect = [initial_metadata] * 4 + [retry_metadata] * 2
    provider.get_ref_sha.return_value = "base-sha"
    provider.list_pr_files_complete.side_effect = [["src/main.py"], ["src/main.py"], retry_inventory]
    provider.publish_pr.side_effect = [RuntimeError("publish failed"), None]
    derived = DerivedState(snapshot)
    derived.set("latest_session_state", SessionState(SessionOutcome.FINISHED))

    first_result = PublishAction().execute(provider, snapshot, derived)

    assert first_result.decision is ActionDecision.FAILED
    assert first_result.details == "publish_pr failed"
    title_updates_before_retry = provider.update_pr_title.call_count
    publishes_before_retry = provider.publish_pr.call_count

    retry_snapshot = PRStateSnapshot(
        pr_number=42,
        head_sha="head-sha",
        base_branch="main",
        head_branch="feature",
        is_draft=True,
        title="completed work",
        files=["src/main.py"],
        has_changes=True,
    )
    retry_result = PublishAction().execute(provider, retry_snapshot, DerivedState(retry_snapshot))

    assert title_updates_before_retry == 1
    assert provider.update_pr_title.call_count == title_updates_before_retry
    assert provider.publish_pr.call_count == publishes_before_retry + int(should_publish_on_retry)
    if should_publish_on_retry:
        assert retry_result.decision is ActionDecision.EXECUTE
    else:
        assert retry_result.decision is ActionDecision.SKIP
        assert retry_result.invalidates_snapshot is True
        assert retry_result.preserves_diff_fingerprint is True
