"""Branch-focused tests for critique dispatch helper functions."""

from dataclasses import replace
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.critique_adjudicator import (
    build_critique_task_cancellation_comment,
    build_critique_task_comment,
)
from agentic_devtools.cli.ci.models import COPILOT_REVIEWER_LOGIN, ReviewInfo
from agentic_devtools.cli.ci.pipeline.actions import critique_dispatch
from agentic_devtools.cli.ci.pipeline.gate_verdict import REASON_CLEAN, REASON_NEW_CCR_NOT_APPROVED, CopilotGateVerdict
from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult
from agentic_devtools.cli.ci.pipeline.repair_attempts import RepairAttemptTracker
from agentic_devtools.cli.ci.pipeline.snapshot_models import PRStateSnapshot
from agentic_devtools.cli.ci.provider import RepairDispatchNotAttemptedError


def _zero_finding_snapshot(headline: str, classification: str = "critique") -> PRStateSnapshot:
    body = f"<!-- ccr-overview-v2 -->\n### 🔵 Needs a closer look\n\n{headline}\n\n0 open findings"
    return PRStateSnapshot(
        pr_number=42,
        head_sha="head",
        ci_status="passing",
        effective_review_comment_count=0,
        effective_review_comment_count_review_id=100,
        effective_review_comment_filter_applied=False,
        critique_headline_classification=classification,
        reviews=[ReviewInfo(100, COPILOT_REVIEWER_LOGIN, "COMMENTED", body, "head")],
        copilot_gate_verdict=CopilotGateVerdict(False, REASON_NEW_CCR_NOT_APPROVED, 100, body_comment_count=0),
    )


def test_ineligible_snapshot_is_not_a_known_empty_overview() -> None:
    snapshot = PRStateSnapshot(pr_number=42, head_sha="head")

    assert critique_dispatch.known_empty_zero_findings_overview(snapshot) is None
    assert critique_dispatch.zero_findings_headline(snapshot) is None
    assert critique_dispatch.should_skip_zero_findings_repair(snapshot, stuck_prior_threads=False) is False


def test_clean_zero_finding_overview_is_known_for_critique_dispatch() -> None:
    headline = "A concrete parser regression remains."
    snapshot = replace(
        _zero_finding_snapshot(headline),
        copilot_gate_verdict=CopilotGateVerdict(True, REASON_CLEAN, 100, body_comment_count=0),
    )

    assert critique_dispatch.known_empty_zero_findings_overview(snapshot) == (snapshot.reviews[0], headline)
    assert critique_dispatch.zero_findings_headline(snapshot) == (100, headline)
    assert critique_dispatch.should_skip_zero_findings_repair(snapshot, stuck_prior_threads=False) is False


def test_footer_free_zero_findings_overview_is_eligible_with_known_empty_inventory() -> None:
    headline = "A concrete parser regression remains."
    snapshot = replace(
        _zero_finding_snapshot(headline),
        copilot_gate_verdict=CopilotGateVerdict(True, REASON_CLEAN, 100, body_comment_count=None),
    )

    assert critique_dispatch.known_empty_zero_findings_overview(snapshot) == (snapshot.reviews[0], headline)
    assert critique_dispatch.zero_findings_headline(snapshot) == (100, headline)


def test_actionable_review_id_preserves_critique_review_id() -> None:
    snapshot = _zero_finding_snapshot("A concrete parser regression remains.")

    assert critique_dispatch.approval_worthy_headline(snapshot) is None
    assert critique_dispatch.actionable_review_id(snapshot, 100) == 100


def test_passed_verdict_with_other_reason_is_not_a_known_empty_overview() -> None:
    snapshot = replace(
        _zero_finding_snapshot("A concrete parser regression remains."),
        copilot_gate_verdict=CopilotGateVerdict(True, "other", 100, body_comment_count=0),
    )

    assert critique_dispatch.known_empty_zero_findings_overview(snapshot) is None


def test_failing_ci_preserves_existing_repair_path() -> None:
    headline = "Previously reported parser regressions remain unresolved and can lose findings or block promotion."
    snapshot = replace(_zero_finding_snapshot(headline), ci_status="failing")

    assert critique_dispatch.should_skip_zero_findings_repair(snapshot, stuck_prior_threads=False) is False


def test_noncritique_logging_returns_when_no_new_ccr_verdict_exists(caplog) -> None:
    critique_dispatch.log_noncritique_overview(PRStateSnapshot(pr_number=42, head_sha="head"))

    assert "zero-open-findings CCR overview" not in caplog.text


def test_critique_attempt_cap_returns_a_skip_result() -> None:
    headline = "Previously reported parser regressions remain unresolved and can lose findings or block promotion."

    result = critique_dispatch.plan_review_attempt(
        "dispatch_repair",
        _zero_finding_snapshot(headline),
        100,
        body_only_work=True,
        stuck_prior_threads=False,
        attempted={"critique:100:1", "critique:100:2"},
    )

    assert isinstance(result, ActionResult)
    assert result.decision is ActionDecision.SKIP


def test_register_review_attempt_escalates_an_existing_key() -> None:
    provider = MagicMock()
    provider.list_issue_comments.return_value = []
    attempts = RepairAttemptTracker(provider, 42, "head")
    attempts.attempted = {"review:100"}

    with patch.object(attempts, "escalate") as escalate:
        result, shortfall = critique_dispatch.register_review_attempt(
            "dispatch_repair",
            PRStateSnapshot(pr_number=42, head_sha="head"),
            100,
            body_only_work=True,
            stuck_prior_threads=False,
            attempts=attempts,
            review_keys=set(),
            provider=provider,
            finding_aware=False,
            shortfall=1,
            duplicate_trigger=lambda *_args, **_kwargs: False,
        )

    assert result is None
    assert shortfall == 0
    escalate.assert_called_once_with("review:100")


def test_register_review_attempt_migrates_legacy_duplicate_trigger() -> None:
    provider = MagicMock()
    provider.list_issue_comments.return_value = []
    attempts = RepairAttemptTracker(provider, 42, "head")

    with (
        patch.object(attempts, "reserve") as reserve,
        patch.object(attempts, "escalate") as escalate,
    ):
        result, shortfall = critique_dispatch.register_review_attempt(
            "dispatch_repair",
            PRStateSnapshot(pr_number=42, head_sha="head"),
            100,
            body_only_work=True,
            stuck_prior_threads=False,
            attempts=attempts,
            review_keys=set(),
            provider=provider,
            finding_aware=False,
            shortfall=1,
            duplicate_trigger=lambda *_args, **_kwargs: True,
        )

    assert result is None
    assert shortfall == 0
    reserve.assert_called_once_with({"review:100"})
    escalate.assert_called_once_with("review:100")


def test_validated_followup_attempt_bypasses_legacy_duplicate_trigger() -> None:
    provider = MagicMock()
    provider.list_issue_comments.return_value = []
    attempts = RepairAttemptTracker(provider, 42, "head")
    attempts.attempted = {"critique:100:1"}
    snapshot = replace(
        _zero_finding_snapshot("A concrete parser regression remains."),
        critique_followup_instruction="Repair the parser boundary case.",
        critique_adjudicated_review_id=100,
        critique_adjudicated_head_sha="head",
        critique_adjudicated_headline="A concrete parser regression remains.",
        critique_adjudicated_verdict="needs_repair",
    )
    duplicate_trigger = MagicMock(return_value=True)
    review_keys: set[str] = set()

    result, shortfall = critique_dispatch.register_review_attempt(
        "dispatch_repair",
        snapshot,
        100,
        body_only_work=True,
        stuck_prior_threads=False,
        attempts=attempts,
        review_keys=review_keys,
        provider=provider,
        finding_aware=False,
        shortfall=1,
        duplicate_trigger=duplicate_trigger,
    )

    assert result is None
    assert shortfall == 1
    assert review_keys == {"critique:100:2"}
    duplicate_trigger.assert_not_called()


def test_critique_marker_requires_matching_review_context() -> None:
    headline = "Previously reported parser regressions remain unresolved and can lose findings or block promotion."
    provider = MagicMock()

    assert critique_dispatch.create_critique_dispatch_marker(
        provider,
        _zero_finding_snapshot(headline),
        101,
        {"critique:100:1"},
    ) == (None, None)
    provider.post_comment_as_pr_token.assert_not_called()


def test_marker_write_failure_reconciles_before_precreation_error() -> None:
    snapshot = _zero_finding_snapshot("A concrete parser regression remains.")
    provider = MagicMock()
    provider.post_comment_as_pr_token.return_value = 0
    provider.find_comment.return_value = None

    with pytest.raises(RepairDispatchNotAttemptedError, match="Critique task marker write failed"):
        critique_dispatch.create_critique_dispatch_marker(provider, snapshot, 100, {"critique:100:1"})

    provider.find_comment.assert_called_once()


def test_marker_write_failure_reconciliation_error_remains_uncertain() -> None:
    snapshot = _zero_finding_snapshot("A concrete parser regression remains.")
    provider = MagicMock()
    provider.post_comment_as_pr_token.return_value = 0
    provider.find_comment.side_effect = RuntimeError("readback unavailable")

    with pytest.raises(RuntimeError, match="Critique task marker reconciliation failed"):
        critique_dispatch.create_critique_dispatch_marker(provider, snapshot, 100, {"critique:100:1"})


def test_critique_repair_parameters_omits_missing_prompt() -> None:
    assert critique_dispatch.critique_repair_parameters(None) == {}


@pytest.mark.parametrize("bookkeeping_audit", [None, []])
def test_dispatched_repair_result_without_new_bookkeeping_entries(bookkeeping_audit) -> None:
    result = critique_dispatch.dispatched_repair_result(
        "dispatch_repair",
        "review",
        "receipt",
        bookkeeping_audit,
        0,
        None,
    )

    assert result.decision is ActionDecision.EXECUTE
    assert result.details == "Repair dispatched (type=review, receipt=receipt)"


def test_missing_critique_marker_needs_no_cancellation() -> None:
    provider = MagicMock()

    critique_dispatch.cancel_critique_task_marker_if_present(
        provider,
        PRStateSnapshot(pr_number=42, head_sha="head"),
        None,
    )

    provider.update_comment_as_pr_token.assert_not_called()
    provider.find_comment.assert_not_called()


def test_reconcile_critique_marker_cancels_exact_marker() -> None:
    snapshot = _zero_finding_snapshot("A concrete parser regression remains.")
    marker_body = build_critique_task_comment(42, "head", 100, 2)
    cancelled_body = build_critique_task_cancellation_comment(42, "head", 100, 2)
    provider = MagicMock()
    provider.find_comment.side_effect = [(77, marker_body), (77, cancelled_body)]
    provider.update_comment_as_pr_token.return_value = None

    critique_dispatch.reconcile_critique_task_marker(provider, snapshot, {"critique:100:2"})

    provider.update_comment_as_pr_token.assert_called_once_with(77, cancelled_body)
    assert provider.find_comment.call_count == 2


def test_reconcile_critique_marker_ignores_missing_marker() -> None:
    snapshot = _zero_finding_snapshot("A concrete parser regression remains.")
    provider = MagicMock()
    provider.find_comment.return_value = None

    critique_dispatch.reconcile_critique_task_marker(provider, snapshot, {"critique:100:2"})

    provider.update_comment_as_pr_token.assert_not_called()


def test_reconcile_critique_marker_rejects_nonmatching_body() -> None:
    snapshot = _zero_finding_snapshot("A concrete parser regression remains.")
    provider = MagicMock()
    provider.find_comment.return_value = (77, "a different marker body")

    with pytest.raises(RuntimeError, match="could not be safely reconciled"):
        critique_dispatch.reconcile_critique_task_marker(provider, snapshot, {"critique:100:2"})

    provider.update_comment_as_pr_token.assert_not_called()


def test_reconcile_critique_marker_skips_unrelated_attempt_keys() -> None:
    snapshot = _zero_finding_snapshot("A concrete parser regression remains.")
    provider = MagicMock()

    critique_dispatch.reconcile_critique_task_marker(provider, snapshot, {"review:100"})

    provider.find_comment.assert_not_called()


def test_reconcile_critique_marker_skips_when_no_attempts_are_pending() -> None:
    snapshot = _zero_finding_snapshot("A concrete parser regression remains.")
    provider = MagicMock()

    critique_dispatch.reconcile_critique_task_marker(provider, snapshot, set())

    provider.find_comment.assert_not_called()


def test_reconcile_critique_marker_skips_noncritique_snapshot() -> None:
    provider = MagicMock()

    critique_dispatch.reconcile_critique_task_marker(provider, PRStateSnapshot(pr_number=42, head_sha="head"), set())

    provider.find_comment.assert_not_called()


def test_dispatch_marker_requires_a_reserved_critique_attempt() -> None:
    headline = "Previously reported parser regressions remain unresolved and can lose findings or block promotion."
    snapshot = _zero_finding_snapshot(headline)
    provider = MagicMock()

    assert critique_dispatch.create_critique_dispatch_marker(provider, snapshot, 100, set()) == (None, None)
    provider.post_comment_as_pr_token.assert_not_called()
