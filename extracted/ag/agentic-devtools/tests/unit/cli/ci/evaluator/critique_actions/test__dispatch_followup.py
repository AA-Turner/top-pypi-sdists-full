"""Tests for dispatching critique follow-up repairs."""

from types import SimpleNamespace
from unittest.mock import Mock, patch

from agentic_devtools.cli.ci.critique_adjudicator import CritiqueAdjudication
from agentic_devtools.cli.ci.evaluator.critique_actions import _dispatch_followup
from agentic_devtools.cli.ci.pipeline.models import ActionDecision
from tests.unit.cli.ci.evaluator.critique_actions._support import _make_needs_repair_dispatch_case


def test_lock_loss_after_preflight_prevents_followup_dispatch() -> None:
    provider, _, snapshot, live_snapshot = _make_needs_repair_dispatch_case()
    decision = CritiqueAdjudication(
        verdict="needs_repair",
        rationale="A concrete parser regression remains.",
        concrete_instruction="Add a regression test.",
    )
    dispatch = Mock()
    dispatch.evaluate.return_value = SimpleNamespace(decision=ActionDecision.EXECUTE)

    with (
        patch(
            "agentic_devtools.cli.ci.evaluator.critique_actions.build_pr_state_snapshot",
            return_value=live_snapshot,
        ),
        patch(
            "agentic_devtools.cli.ci.evaluator.critique_actions.critique_dispatch.zero_findings_headline",
            return_value=(100, snapshot.critique_headline),
        ),
        patch("agentic_devtools.cli.ci.evaluator.critique_actions.DispatchRepairAction", return_value=dispatch),
    ):
        _, result = _dispatch_followup(
            provider,
            snapshot,
            "head",
            100,
            snapshot.critique_headline,
            decision,
            0,
            Mock(return_value=False),
        )

    assert result is not None and result.success is False
    dispatch.execute.assert_not_called()
