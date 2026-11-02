"""Tests for constructing the final result of a dispatched repair."""

from agentic_devtools.cli.ci.pipeline.actions.critique_dispatch import dispatched_repair_result
from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult


def test_returns_a_failed_task_binding_result_unchanged() -> None:
    binding_failure = ActionResult(name="dispatch_repair", decision=ActionDecision.FAILED, error="unverified")

    result = dispatched_repair_result("dispatch_repair", "review", "receipt", None, 0, binding_failure)

    assert result is binding_failure


def test_includes_only_bookkeeping_entries_added_during_dispatch() -> None:
    result = dispatched_repair_result("dispatch_repair", "review", "receipt", ["prior", "new entry"], 1, None)

    assert result.decision is ActionDecision.EXECUTE
    assert result.details == "Repair dispatched (type=review, receipt=receipt); bookkeeping audit: new entry"


def test_omits_bookkeeping_details_when_no_audit_list_exists() -> None:
    result = dispatched_repair_result("dispatch_repair", "review", "receipt", None, 0, None)

    assert result.decision is ActionDecision.EXECUTE
    assert result.details == "Repair dispatched (type=review, receipt=receipt)"


def test_omits_bookkeeping_details_when_no_new_entries_were_added() -> None:
    result = dispatched_repair_result("dispatch_repair", "review", "receipt", [], 0, None)

    assert result.decision is ActionDecision.EXECUTE
    assert result.details == "Repair dispatched (type=review, receipt=receipt)"
