"""Tests for critique task-cap adjudication."""

from unittest.mock import patch

from agentic_devtools.cli.ci.critique_adjudicator import CritiqueAdjudication
from agentic_devtools.cli.ci.evaluator.critique_actions import _adjudicate_snapshot
from tests.unit.cli.ci.evaluator.critique_actions._support import _make_snapshot, _make_task


def test_maximum_length_rationale_at_task_cap_is_bounded() -> None:
    rationale = "A" * 1_999 + "Z"
    snapshot = _make_snapshot(tasks=(_make_task(1), _make_task(2)))
    with patch(
        "agentic_devtools.cli.ci.evaluator.critique_actions.run_critique_adjudication",
        return_value=CritiqueAdjudication(
            verdict="needs_repair",
            rationale=rationale,
            concrete_instruction="Repair the defect.",
        ),
    ):
        decision = _adjudicate_snapshot(snapshot, "head", 100, 2)

    prefix = "The adjudicator requested another repair, but the two-task per-HEAD limit has been reached. "
    assert decision.verdict == "needs_human"
    assert decision.rationale == prefix + rationale[: 2_000 - len(prefix)]
