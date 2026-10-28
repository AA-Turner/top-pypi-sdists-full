"""Guard (2026-10-27): an AI workflow step whose turn a spend gate refused fails with
``details.caller_refusal`` and the approval link — so the engine never retries it, recovery never
resumes it, and the run says where to approve it.

Live evidence: run 1aa73a14 — refused items failed as bare ``ai_turn_failed`` and were
re-dispatched 615 times. Break caught: the refusal flag or the envelope dropped from the failure.
"""

from __future__ import annotations

from types import SimpleNamespace

from matrx_graph.spend_gate import is_caller_refusal
from matrx_graph.types.result import Failure

from matrx_ai.graph_nodes.shared import normalize_completed_result
from matrx_ai.providers.run_approval_gate import RunApprovalRequiredError

APPROVAL = "https://manage.aimatrx.com/admin/intelligence/mandates/flashcards.generate_from_source/approvals"


def _completed(error_type: str, terminal: BaseException | None) -> SimpleNamespace:
    return SimpleNamespace(
        metadata={
            "status": "failed",
            "error_type": error_type,
            "error": "This agent's first run cost more than its approval limit, so it waits for an administrator to approve it.",
        },
        total_usage=None,
        request=SimpleNamespace(conversation_id="23f2e4c9-fd3b-41cb-9926-d6e92f104ce8", request_id="b47f292d"),
        terminal_exception=terminal,
    )


def test_a_spend_refusal_fails_the_step_as_a_refusal_with_its_approval_link():
    refusal = RunApprovalRequiredError(
        approval_id="6f1e2d3c-4b5a-4968-8776-5a4b3c2d1e0f",
        subject_kind="mandate",
        subject_id="flashcards.generate_from_source",
        status="waiting",
        approval_url=APPROVAL,
        reason="over_threshold",
    )
    result = normalize_completed_result(_completed("run_approval_required", refusal))
    assert isinstance(result, Failure)
    assert is_caller_refusal(node_error=result.error)
    assert result.error.details["approval_url"] == APPROVAL
    assert result.error.details["refusal_code"] == "run_approval_required"
    assert result.error.message.startswith("This agent's first run cost more")


def test_a_provider_failure_is_not_a_refusal():
    result = normalize_completed_result(_completed("provider_overloaded", RuntimeError("529 overloaded")))
    assert isinstance(result, Failure)
    assert not is_caller_refusal(node_error=result.error)
    assert "approval_url" not in result.error.details
