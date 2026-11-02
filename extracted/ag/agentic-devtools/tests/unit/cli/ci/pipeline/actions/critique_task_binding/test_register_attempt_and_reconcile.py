from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.pipeline.actions import critique_task_binding
from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult
from agentic_devtools.cli.ci.pipeline.snapshot_models import PRStateSnapshot


@pytest.mark.parametrize(
    ("binding_failure", "expected"),
    [
        (None, ActionResult(name="dispatch_repair", decision=ActionDecision.SKIP, details="attempt cap")),
        (
            ActionResult(name="dispatch_repair", decision=ActionDecision.FAILED, error="binding unresolved"),
            ActionResult(name="dispatch_repair", decision=ActionDecision.FAILED, error="binding unresolved"),
        ),
    ],
)
def test_attempt_result_prefers_binding_failure(
    binding_failure: ActionResult | None,
    expected: ActionResult,
) -> None:
    provider = MagicMock()
    snapshot = PRStateSnapshot(pr_number=42, head_sha="head")
    attempts = MagicMock()
    attempt_result = ActionResult(name="dispatch_repair", decision=ActionDecision.SKIP, details="attempt cap")

    with (
        patch(
            "agentic_devtools.cli.ci.pipeline.actions.critique_dispatch.register_review_attempt",
            return_value=(attempt_result, 2),
        ) as register,
        patch(
            "agentic_devtools.cli.ci.pipeline.actions.critique_task_binding.reconcile_before_attempt_skip",
            return_value=binding_failure,
        ) as reconcile,
    ):
        result = critique_task_binding.register_attempt_and_reconcile(
            provider,
            snapshot,
            {"critique:100:1"},
            100,
            True,
            False,
            attempts,
            set(),
            False,
            1,
            MagicMock(),
            [],
            0,
            "dispatch_repair",
        )

    assert result == (expected, 2)
    register.assert_called_once()
    reconcile.assert_called_once()


def test_no_attempt_result_skips_binding_reconciliation() -> None:
    provider = MagicMock()
    snapshot = PRStateSnapshot(pr_number=42, head_sha="head")

    with (
        patch(
            "agentic_devtools.cli.ci.pipeline.actions.critique_dispatch.register_review_attempt",
            return_value=(None, 0),
        ),
        patch(
            "agentic_devtools.cli.ci.pipeline.actions.critique_task_binding.reconcile_before_attempt_skip"
        ) as reconcile,
    ):
        result = critique_task_binding.register_attempt_and_reconcile(
            provider,
            snapshot,
            set(),
            100,
            False,
            False,
            MagicMock(),
            set(),
            False,
            1,
            MagicMock(),
            [],
            0,
            "dispatch_repair",
        )

    assert result == (None, 0)
    reconcile.assert_not_called()
