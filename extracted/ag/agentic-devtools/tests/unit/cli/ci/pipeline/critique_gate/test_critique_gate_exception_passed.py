from dataclasses import replace

from agentic_devtools.cli.ci.models import COPILOT_REVIEWER_LOGIN, ReviewInfo
from agentic_devtools.cli.ci.pipeline.critique_gate import critique_gate_exception_passed
from agentic_devtools.cli.ci.pipeline.gate_verdict import (
    REASON_CLEAN,
    REASON_NEW_CCR_NOT_APPROVED,
    CopilotGateVerdict,
    copilot_review_gate_passed,
)
from agentic_devtools.cli.ci.pipeline.snapshot_models import PRStateSnapshot

HUMAN_REVIEW_HEADLINE = "Broad modernization and limited baseline verification require final human review."


def test_unadjudicated_critique_keeps_gate_blocked() -> None:
    headline = "A concrete parser regression remains."
    body = f"<!-- ccr-overview-v2 -->\n### Needs a closer look\n\n{headline}\n\n0 open findings"
    snapshot = PRStateSnapshot(
        pr_number=42,
        head_sha="head",
        copilot_gate_verdict=CopilotGateVerdict(False, REASON_NEW_CCR_NOT_APPROVED, 100, body_comment_count=0),
        effective_review_comment_count=0,
        effective_review_comment_count_review_id=100,
        effective_review_comment_filter_applied=False,
        reviews=[ReviewInfo(100, COPILOT_REVIEWER_LOGIN, "COMMENTED", body, "head")],
        critique_headline_classification="critique",
    )

    assert critique_gate_exception_passed(snapshot, unresolved_threads=0) is False


def test_footer_free_critique_is_blocked_when_api_confirms_no_open_comments() -> None:
    snapshot = _gate_snapshot()
    snapshot = replace(
        snapshot,
        copilot_gate_verdict=CopilotGateVerdict(True, REASON_CLEAN, 100, body_comment_count=None),
    )

    assert critique_gate_exception_passed(snapshot, unresolved_threads=0) is False


def test_unparseable_overview_does_not_relax_the_gate() -> None:
    snapshot = PRStateSnapshot(
        pr_number=42,
        head_sha="head",
        copilot_gate_verdict=CopilotGateVerdict(False, REASON_NEW_CCR_NOT_APPROVED, 100, body_comment_count=0),
        effective_review_comment_count=0,
        effective_review_comment_count_review_id=100,
        effective_review_comment_filter_applied=False,
        reviews=[ReviewInfo(100, COPILOT_REVIEWER_LOGIN, "COMMENTED", "not an overview", "head")],
    )

    assert critique_gate_exception_passed(snapshot, unresolved_threads=0) is None


def _gate_snapshot(
    *,
    classification: str = "critique",
    adjudicated: bool = False,
    include_review: bool = True,
    headline: str = "A concrete parser regression remains.",
    heading: str = "### Needs a closer look",
) -> PRStateSnapshot:
    body = f"<!-- ccr-overview-v2 -->\n{heading}\n\n{headline}\n\n0 open findings"
    return PRStateSnapshot(
        pr_number=42,
        head_sha="head",
        copilot_gate_verdict=CopilotGateVerdict(False, REASON_NEW_CCR_NOT_APPROVED, 100, body_comment_count=0),
        effective_review_comment_count=0,
        effective_review_comment_count_review_id=100,
        effective_review_comment_filter_applied=False,
        reviews=[ReviewInfo(100, COPILOT_REVIEWER_LOGIN, "COMMENTED", body, "head")] if include_review else [],
        critique_headline_classification=classification,
        critique_adjudicated_review_id=100 if adjudicated else None,
        critique_adjudicated_head_sha="head" if adjudicated else "",
        critique_adjudicated_headline=headline if adjudicated else "",
        critique_adjudicated_verdict="rebutted" if adjudicated else "",
    )


def test_missing_verdict_or_current_review_is_not_applicable() -> None:
    assert critique_gate_exception_passed(PRStateSnapshot(pr_number=42, head_sha="head"), 0) is None
    assert critique_gate_exception_passed(_gate_snapshot(include_review=False), 0) is None


def test_approval_worthy_headline_relaxes_gate_only_without_unresolved_threads() -> None:
    snapshot = _gate_snapshot(classification="approval_worthy")

    assert critique_gate_exception_passed(snapshot, unresolved_threads=0) is True
    assert critique_gate_exception_passed(snapshot, unresolved_threads=1) is False


def test_approval_worthy_headline_stays_blocked_when_critique_task_state_is_unavailable() -> None:
    snapshot = replace(_gate_snapshot(classification="approval_worthy"), critique_task_state_available=False)

    assert copilot_review_gate_passed(snapshot, unresolved_threads=0) is False


def test_not_approved_human_review_headline_passes_with_all_gate_guards() -> None:
    for heading in ("### 🔴 Not ready to approve", "### 🔵 Needs a closer look"):
        snapshot = _gate_snapshot(
            classification="approval_worthy",
            headline=HUMAN_REVIEW_HEADLINE,
            heading=heading,
        )

        assert snapshot.copilot_gate_verdict is not None
        assert snapshot.copilot_gate_verdict.reason == REASON_NEW_CCR_NOT_APPROVED
        assert copilot_review_gate_passed(snapshot, unresolved_threads=0) is True


def test_unknown_classification_blocks_not_approved_gate_with_or_without_matching_rebuttal() -> None:
    for adjudicated in (False, True):
        snapshot = _gate_snapshot(
            classification="UNKNOWN",
            adjudicated=adjudicated,
            headline=HUMAN_REVIEW_HEADLINE,
            heading="### 🔴 Not ready to approve",
        )

        assert critique_gate_exception_passed(snapshot, unresolved_threads=0) is False
        assert copilot_review_gate_passed(snapshot, unresolved_threads=0) is False


def test_not_approved_human_review_headline_stays_blocked_with_unresolved_threads() -> None:
    snapshot = _gate_snapshot(
        classification="approval_worthy",
        headline=HUMAN_REVIEW_HEADLINE,
        heading="### 🔴 Not ready to approve",
    )

    assert copilot_review_gate_passed(snapshot, unresolved_threads=1) is False


def test_not_approved_human_review_headline_stays_blocked_with_unknown_inventory() -> None:
    snapshot = _gate_snapshot(
        classification="approval_worthy",
        headline=HUMAN_REVIEW_HEADLINE,
        heading="### 🔵 Needs a closer look",
    )
    snapshot = replace(
        snapshot,
        effective_review_comment_count=None,
        effective_review_comment_filter_applied=None,
    )

    assert copilot_review_gate_passed(snapshot, unresolved_threads=0) is False


def test_not_approved_human_review_headline_stays_blocked_for_stale_head() -> None:
    snapshot = _gate_snapshot(
        classification="approval_worthy",
        headline=HUMAN_REVIEW_HEADLINE,
    )
    snapshot = replace(snapshot, head_changed_since_review=True)

    assert copilot_review_gate_passed(snapshot, unresolved_threads=0) is False


def test_clean_critique_headline_still_blocks_shared_gate() -> None:
    snapshot = _gate_snapshot()
    snapshot = replace(snapshot, copilot_gate_verdict=CopilotGateVerdict(True, REASON_CLEAN, 100, body_comment_count=0))

    assert critique_gate_exception_passed(snapshot, unresolved_threads=0) is False
    assert copilot_review_gate_passed(snapshot, unresolved_threads=0) is False


def test_clean_critique_headline_stays_blocked_with_unknown_comment_inventory() -> None:
    snapshot = _gate_snapshot()
    snapshot = replace(
        snapshot,
        copilot_gate_verdict=CopilotGateVerdict(True, REASON_CLEAN, 100, body_comment_count=0),
        effective_review_comment_count=None,
        effective_review_comment_count_review_id=None,
        effective_review_comment_filter_applied=None,
    )

    assert critique_gate_exception_passed(snapshot, unresolved_threads=0) is False
    assert copilot_review_gate_passed(snapshot, unresolved_threads=0) is False


def test_clean_approval_worthy_headline_keeps_existing_gate_path() -> None:
    snapshot = _gate_snapshot(classification="approval_worthy")
    snapshot = replace(snapshot, copilot_gate_verdict=CopilotGateVerdict(True, REASON_CLEAN, 100, body_comment_count=0))

    assert critique_gate_exception_passed(snapshot, unresolved_threads=0) is None
    assert copilot_review_gate_passed(snapshot, unresolved_threads=0) is True


def test_clean_unclassified_headline_keeps_existing_gate_path() -> None:
    snapshot = _gate_snapshot(classification="")
    snapshot = replace(snapshot, copilot_gate_verdict=CopilotGateVerdict(True, REASON_CLEAN, 100, body_comment_count=0))

    assert critique_gate_exception_passed(snapshot, unresolved_threads=0) is None
    assert copilot_review_gate_passed(snapshot, unresolved_threads=0) is True


def test_matching_rebuttal_relaxes_gate_only_without_unresolved_threads() -> None:
    snapshot = _gate_snapshot(adjudicated=True)

    assert critique_gate_exception_passed(snapshot, unresolved_threads=0) is True
    assert critique_gate_exception_passed(snapshot, unresolved_threads=1) is False


def test_matching_rebuttal_still_relaxes_clean_critique_gate() -> None:
    snapshot = _gate_snapshot(adjudicated=True)
    snapshot = replace(snapshot, copilot_gate_verdict=CopilotGateVerdict(True, REASON_CLEAN, 100, body_comment_count=0))

    assert critique_gate_exception_passed(snapshot, unresolved_threads=0) is True
    assert copilot_review_gate_passed(snapshot, unresolved_threads=0) is True
