"""Verify critique headlines route through a single Agent Tasks repair."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.critique_adjudicator import CritiqueHeadlineClassification
from agentic_devtools.cli.ci.pipeline.actions.dispatch_repair import DispatchRepairAction
from agentic_devtools.cli.ci.pipeline.gate_verdict import copilot_review_gate_passed
from agentic_devtools.cli.ci.pipeline.models import ActionDecision
from agentic_devtools.cli.ci.pipeline.snapshot_builder import build_pr_state_snapshot
from agentic_devtools.cli.ci.pipeline.snapshot_models import DerivedState
from tests.workflows.ci.test_critique_headline_dispatch import HEADLINE, _provider


@pytest.mark.parametrize(
    ("heading", "review_state"),
    [
        ("### 🔵 Needs a closer look", "COMMENTED"),
        ("### 🔴 Not ready to approve", "CHANGES_REQUESTED"),
        ("### ✅ Ready to approve", "APPROVED"),
    ],
)
def test_current_head_zero_findings_critique_blocks_and_dispatches_once(
    heading: str,
    review_state: str,
) -> None:
    body = f"<!-- ccr-overview-v2 -->\n\n{heading}\n\n{HEADLINE}\n\n**Comments generated:** 0\n**No open issues** 🎉"
    provider = _provider(body, review_state)

    with patch(
        "agentic_devtools.cli.ci.pipeline.critique_snapshot.classify_critique_headline",
        return_value=CritiqueHeadlineClassification(verdict="critique"),
    ):
        snapshot = build_pr_state_snapshot(
            provider,
            42,
            actionable_check_names=frozenset({"Build"}),
            promote_findings=False,
        )

    assert snapshot.critique_headline_classification == "critique"
    assert snapshot.copilot_gate_verdict is not None
    assert not copilot_review_gate_passed(snapshot, unresolved_threads=snapshot.unresolved_threads)

    with patch(
        "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_copilot_session_active_via_agent_task",
        return_value=False,
    ):
        result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))

    assert result.decision is ActionDecision.EXECUTE
    provider.dispatch_repair.assert_called_once()
    assert provider.dispatch_repair.call_args.kwargs["review_id"] == 100
    assert provider.dispatch_repair.call_args.kwargs["agent_task_prompt"] == (
        f"@copilot please address the following critique of this pr:\n\n{HEADLINE}"
    )
