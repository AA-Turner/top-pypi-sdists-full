from dataclasses import FrozenInstanceError

import pytest

from agentic_devtools.cli.github.review_orchestration import RepairPlan


def test_plan_is_immutable_and_defaults_to_no_actions():
    plan = RepairPlan("waiting", "incomplete", 1300)
    assert plan.batches == ()
    assert not plan.invalidate_evidence
    with pytest.raises(FrozenInstanceError):
        plan.reason = "ready"
