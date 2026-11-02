from unittest.mock import MagicMock, patch

from agentic_devtools.cli.ci.critique_adjudicator import (
    build_critique_task_comment,
    build_critique_task_id_marker,
)
from agentic_devtools.cli.ci.models import IssueCommentInfo, ReviewInfo
from agentic_devtools.cli.ci.pipeline.actions import critique_task_binding
from agentic_devtools.cli.ci.pipeline.gate_verdict import REASON_NEW_CCR_NOT_APPROVED, CopilotGateVerdict
from agentic_devtools.cli.ci.pipeline.models import ActionDecision
from agentic_devtools.cli.ci.pipeline.snapshot_models import PRStateSnapshot


def _snapshot(classification: str = "critique") -> PRStateSnapshot:
    headline = "A concrete parser regression remains."
    body = f"<!-- ccr-overview-v2 -->\n### Needs a closer look\n\n{headline}\n\n0 open findings"
    return PRStateSnapshot(
        pr_number=42,
        head_sha="head",
        base_repo_full_name="owner/repo",
        effective_review_comment_count=0,
        effective_review_comment_count_review_id=100,
        effective_review_comment_filter_applied=False,
        reviews=[ReviewInfo(100, "copilot[bot]", "COMMENTED", body, "head")],
        copilot_gate_verdict=CopilotGateVerdict(
            False,
            REASON_NEW_CCR_NOT_APPROVED,
            100,
            body_comment_count=0,
        ),
        critique_headline_classification=classification,
    )


def _unbound_task(comment_id: int = 7, attempt: int = 1) -> IssueCommentInfo:
    return IssueCommentInfo(
        comment_id,
        "github-actions[bot]",
        build_critique_task_comment(42, "head", 100, attempt),
    )


def _provider(comments: list[IssueCommentInfo]) -> MagicMock:
    provider = MagicMock()
    provider.list_issue_comments.return_value = comments
    provider.get_trusted_loop_comment_logins.return_value = {"github-actions[bot]"}
    return provider


def test_reconciliation_skips_ineligible_or_unattempted_critique() -> None:
    provider = _provider([])

    assert (
        critique_task_binding.reconcile_dispatched_critique_task_binding(
            provider,
            _snapshot("approval_worthy"),
            {"critique:100:1"},
            {"task:owner/repo:task-123"},
            "dispatch_repair",
        )
        is None
    )
    assert (
        critique_task_binding.reconcile_dispatched_critique_task_binding(
            provider,
            _snapshot(),
            set(),
            {"task:owner/repo:task-123"},
            "dispatch_repair",
        )
        is None
    )
    provider.list_issue_comments.assert_not_called()


def test_reconciliation_skips_when_no_unbound_marker_exists() -> None:
    comments = [
        IssueCommentInfo(
            7,
            "github-actions[bot]",
            build_critique_task_comment(42, "head", 100, 1) + "\n" + build_critique_task_id_marker("task-123"),
        )
    ]

    result = critique_task_binding.reconcile_dispatched_critique_task_binding(
        _provider(comments),
        _snapshot(),
        {"critique:100:1"},
        {"task:owner/repo:task-123"},
        "dispatch_repair",
    )

    assert result is None


def test_reconciliation_waits_when_no_receipt_has_been_persisted() -> None:
    result = critique_task_binding.reconcile_dispatched_critique_task_binding(
        _provider([_unbound_task()]),
        _snapshot(),
        {"critique:100:1"},
        set(),
        "dispatch_repair",
    )

    assert result is None


def test_reconciliation_fails_closed_when_multiple_receipts_match() -> None:
    result = critique_task_binding.reconcile_dispatched_critique_task_binding(
        _provider([_unbound_task()]),
        _snapshot(),
        {"critique:100:1"},
        {"task:owner/repo:task-123", "task:owner/repo:task-456"},
        "dispatch_repair",
    )

    assert result is not None
    assert result.decision is ActionDecision.FAILED
    assert "uniquely reconcile" in (result.error or "")


def test_reconciliation_fails_closed_when_marker_is_not_unique() -> None:
    result = critique_task_binding.reconcile_dispatched_critique_task_binding(
        _provider([_unbound_task(7), _unbound_task(8)]),
        _snapshot(),
        {"critique:100:1"},
        {"task:owner/repo:task-123"},
        "dispatch_repair",
    )

    assert result is not None
    assert result.decision is ActionDecision.FAILED
    assert "uniquely reconcile" in (result.error or "")


def test_reconciliation_requires_a_single_persisted_marker_id() -> None:
    result = critique_task_binding.reconcile_dispatched_critique_task_binding(
        _provider([_unbound_task(True)]),
        _snapshot(),
        {"critique:100:1"},
        {"task:owner/repo:task-123"},
        "dispatch_repair",
    )

    assert result is not None
    assert result.decision is ActionDecision.FAILED
    assert "identify" in (result.error or "")


def test_reconciliation_rebinds_the_unique_unbound_task_receipt() -> None:
    provider = _provider([_unbound_task()])
    with patch(
        "agentic_devtools.cli.ci.pipeline.actions.critique_task_binding.bind_dispatched_critique_task",
        return_value=None,
    ) as bind:
        result = critique_task_binding.reconcile_dispatched_critique_task_binding(
            provider,
            _snapshot(),
            {"critique:100:1"},
            {"task:owner/repo:task-123"},
            "dispatch_repair",
        )

    assert result is None
    assert bind.call_args.args[2] == (7, 100, 1)
    assert bind.call_args.args[3] == "task:owner/repo:task-123"


def test_existing_reconciliation_skips_unrelated_or_unattempted_snapshots() -> None:
    ledger = MagicMock()
    provider = _provider([])

    assert (
        critique_task_binding.reconcile_existing_critique_task_binding(
            provider,
            _snapshot("approval_worthy"),
            {"critique:100:1"},
            ledger,
            "dispatch_repair",
        )
        is None
    )
    assert (
        critique_task_binding.reconcile_existing_critique_task_binding(
            provider,
            _snapshot(),
            {"review:100"},
            ledger,
            "dispatch_repair",
        )
        is None
    )
    ledger.read.assert_not_called()


def test_existing_reconciliation_reads_ledger_for_eligible_attempt() -> None:
    ledger = MagicMock()
    ledger.read.return_value = ({"task:owner/repo:task-123"}, False, 3)
    provider = _provider([])

    with patch(
        "agentic_devtools.cli.ci.pipeline.actions.critique_task_binding.reconcile_dispatched_critique_task_binding",
        return_value=None,
    ) as reconcile:
        result = critique_task_binding.reconcile_existing_critique_task_binding(
            provider,
            _snapshot(),
            {"critique:100:1"},
            ledger,
            "dispatch_repair",
        )

    assert result is None
    reconcile.assert_called_once_with(
        provider,
        _snapshot(),
        {"critique:100:1"},
        {"task:owner/repo:task-123"},
        "dispatch_repair",
    )
