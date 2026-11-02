from unittest.mock import MagicMock, patch

from agentic_devtools.cli.ci.pipeline.actions import critique_task_binding
from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult
from agentic_devtools.cli.ci.pipeline.snapshot_models import PRStateSnapshot


def test_reconciles_ledger_before_retrying_task_binding() -> None:
    provider = MagicMock()
    snapshot = PRStateSnapshot(pr_number=42, head_sha="head")
    ledger = MagicMock()
    expected = ActionResult(name="dispatch_repair", decision=ActionDecision.FAILED, error="binding unresolved")
    attempted = {"critique:100:1"}

    with patch(
        "agentic_devtools.cli.ci.pipeline.actions.critique_task_binding.reconcile_existing_critique_task_binding",
        return_value=expected,
    ) as reconcile:
        result = critique_task_binding.reconcile_ledger_task_binding(
            provider,
            snapshot,
            attempted,
            ledger,
            "dispatch_repair",
        )

    assert result is expected
    ledger.reconcile.assert_called_once()
    reconcile.assert_called_once_with(provider, snapshot, attempted, ledger, "dispatch_repair")
