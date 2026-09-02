"""Tests for suppressed_deferral_eligible in the gate_verdict module."""

from __future__ import annotations

from typing import Any

import pytest

from agentic_devtools.cli.ci.pipeline.gate_verdict import (
    REASON_CLEAN,
    REASON_HAS_COMMENTS,
    REASON_NEW_CCR_NOT_APPROVED,
    REASON_SUPPRESSED_COMMENTS,
    REASON_UNPARSED_SUPPRESSION,
    SUPPRESSED_FOLLOW_UP_LABEL,
    CopilotGateVerdict,
    suppressed_deferral_eligible,
)


def _verdict(
    *,
    reason: str = REASON_SUPPRESSED_COMMENTS,
    review_id: int = 42,
    suppressed_count: int = 2,
    passed: bool = False,
    body_comment_count: int = 0,
) -> CopilotGateVerdict:
    return CopilotGateVerdict(
        passed=passed,
        reason=reason,
        review_id=review_id,
        body_comment_count=body_comment_count,
        suppressed_count=suppressed_count,
    )


def _kwargs(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "head_changed_since_review": False,
        "unresolved_threads": 0,
        "suppressed_paths": ["specs/3672/spec.md", "docs/design.md"],
        "changed_files": ["specs/3672/spec.md", "docs/design.md", "README.md"],
        "prior_executable_posted_findings": 0,
        "pr_labels": ["ai-auto-merge-allowed"],
        "linked_issue_labels": ["enhancement"],
        "open_deferral_count": 0,
        "max_open_deferrals": 5,
    }
    base.update(overrides)
    return base


class TestSuppressedDeferralEligible:
    """All ten conditions must hold; each one alone is enough to block."""

    def test_all_conditions_hold_returns_true(self) -> None:
        assert suppressed_deferral_eligible(_verdict(), **_kwargs()) is True

    def test_new_ccr_suppressed_only_verdict_returns_true(self) -> None:
        verdict = _verdict(reason=REASON_NEW_CCR_NOT_APPROVED, suppressed_count=1)
        assert suppressed_deferral_eligible(verdict, **_kwargs(suppressed_paths=["specs/3672/spec.md"])) is True

    # Condition 1 — suppressed-only block
    def test_condition_1_none_verdict_returns_false(self) -> None:
        assert suppressed_deferral_eligible(None, **_kwargs()) is False

    def test_condition_1_passed_verdict_returns_false(self) -> None:
        verdict = _verdict(reason=REASON_CLEAN, passed=True, suppressed_count=0)
        assert suppressed_deferral_eligible(verdict, **_kwargs()) is False

    def test_condition_1_posted_comments_returns_false(self) -> None:
        verdict = _verdict(reason=REASON_HAS_COMMENTS, body_comment_count=3)
        assert suppressed_deferral_eligible(verdict, **_kwargs()) is False

    def test_condition_1_unparsed_suppression_returns_false(self) -> None:
        verdict = _verdict(reason=REASON_UNPARSED_SUPPRESSION)
        assert suppressed_deferral_eligible(verdict, **_kwargs()) is False

    # Condition 2 — a concrete review id
    def test_condition_2_missing_review_id_returns_false(self) -> None:
        assert suppressed_deferral_eligible(_verdict(review_id=0), **_kwargs()) is False

    # Condition 3 — HEAD unchanged
    def test_condition_3_head_changed_returns_false(self) -> None:
        assert suppressed_deferral_eligible(_verdict(), **_kwargs(head_changed_since_review=True)) is False

    # Condition 4 — no unresolved threads
    def test_condition_4_unresolved_threads_returns_false(self) -> None:
        assert suppressed_deferral_eligible(_verdict(), **_kwargs(unresolved_threads=1)) is False

    # Condition 5 — recovered entries reconcile with the declared count
    def test_condition_5_count_mismatch_returns_false(self) -> None:
        assert suppressed_deferral_eligible(_verdict(suppressed_count=3), **_kwargs()) is False

    def test_zero_suppressed_count_with_no_recovered_paths_returns_false(self) -> None:
        # Condition 1 rejects this first: a suppressed-only block requires
        # ``suppressed_count > 0``, which in turn guarantees a non-empty
        # recovered-path list once condition 5 holds.
        verdict = _verdict(suppressed_count=0)
        assert suppressed_deferral_eligible(verdict, **_kwargs(suppressed_paths=[])) is False

    # Condition 6 — attributed, well-formed, non-executable paths
    def test_condition_6_executable_finding_path_returns_false(self) -> None:
        kwargs = _kwargs(
            suppressed_paths=["specs/3672/spec.md", "agentic_devtools/state.py"],
            changed_files=["specs/3672/spec.md", "agentic_devtools/state.py"],
        )
        assert suppressed_deferral_eligible(_verdict(), **kwargs) is False

    @pytest.mark.parametrize("bogus", ["get_issue_types()", "(unknown file)", "--dry-run"])
    def test_condition_6_non_path_finding_returns_false(self, bogus: str) -> None:
        kwargs = _kwargs(suppressed_paths=["specs/3672/spec.md", bogus])
        assert suppressed_deferral_eligible(_verdict(), **kwargs) is False

    # Condition 7 — no prior posted finding on executable code
    def test_condition_7_prior_executable_posted_finding_returns_false(self) -> None:
        assert suppressed_deferral_eligible(_verdict(), **_kwargs(prior_executable_posted_findings=1)) is False

    # Condition 8 — open-deferral circuit breaker
    def test_condition_8_backlog_at_ceiling_returns_false(self) -> None:
        kwargs = _kwargs(open_deferral_count=5, max_open_deferrals=5)
        assert suppressed_deferral_eligible(_verdict(), **kwargs) is False

    def test_condition_8_non_positive_ceiling_returns_false(self) -> None:
        kwargs = _kwargs(open_deferral_count=0, max_open_deferrals=0)
        assert suppressed_deferral_eligible(_verdict(), **kwargs) is False

    # Condition 9 — one generation only
    def test_condition_9_pr_label_returns_false(self) -> None:
        kwargs = _kwargs(pr_labels=[SUPPRESSED_FOLLOW_UP_LABEL])
        assert suppressed_deferral_eligible(_verdict(), **kwargs) is False

    def test_condition_9_linked_issue_label_returns_false(self) -> None:
        kwargs = _kwargs(linked_issue_labels=[SUPPRESSED_FOLLOW_UP_LABEL])
        assert suppressed_deferral_eligible(_verdict(), **kwargs) is False

    # Condition 10 — the PR diff itself carries no executable file
    def test_condition_10_executable_file_in_diff_returns_false(self) -> None:
        kwargs = _kwargs(changed_files=["specs/3672/spec.md", "scripts/targeted-checks.sh"])
        assert suppressed_deferral_eligible(_verdict(), **kwargs) is False

    def test_condition_10_empty_changed_files_fails_closed(self) -> None:
        assert suppressed_deferral_eligible(_verdict(), **_kwargs(changed_files=[])) is False
