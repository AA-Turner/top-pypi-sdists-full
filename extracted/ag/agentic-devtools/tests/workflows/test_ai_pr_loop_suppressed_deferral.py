"""End-to-end scenarios for the suppressed-comment deferral path of the AI PR loop.

This is an *integration* test (it crosses ``DeferSuppressedAction``, the real
ten-condition predicate, the real deferral marker subsystem, ``DispatchRepairAction``
and the shared approve/merge gate against a fake provider that stores comments), so
it lives in ``tests/workflows/`` rather than under the 1:1:1 ``tests/unit/`` tree.

It covers the four end-to-end acceptance scenarios of the trigger:

1. specs-only suppressed-only round → deferral filed, repair skipped, gate opens;
2. one executable suppressed entry → no deferral, gate stays closed (repair);
3. specs-only entries but an executable file in the PR-API diff → repair;
4. the follow-up PR itself → repair, never a second generation.
"""

from __future__ import annotations

from dataclasses import replace
from typing import cast
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.models import (
    COPILOT_REVIEWER_LOGIN,
    IssueCommentInfo,
    ReviewInfo,
)
from agentic_devtools.cli.ci.pipeline.actions import DeferSuppressedAction, DispatchRepairAction
from agentic_devtools.cli.ci.pipeline.deferral import (
    SUPPRESSED_DEFERRAL_SENTINEL,
    read_active_suppressed_deferral,
)
from agentic_devtools.cli.ci.pipeline.gate_verdict import (
    REASON_SUPPRESSED_COMMENTS,
    SUPPRESSED_FOLLOW_UP_LABEL,
    CopilotGateVerdict,
    copilot_review_gate_passed,
)
from agentic_devtools.cli.ci.pipeline.models import ActionDecision
from agentic_devtools.cli.ci.pipeline.snapshot import DerivedState, PRStateSnapshot
from agentic_devtools.cli.ci.provider import CIPlatformProvider

PR_NUMBER = 4242
REVIEW_ID = 900100
HEAD_SHA = "headsha00000000000000000000000000000000a"
DEFERRAL_ISSUE = 7777

SPECS_FINDINGS = "**specs/3672/spec.md**: Tighten the wording\n**specs/3672/plan.md**: Add a rollout note"
EXECUTABLE_FINDINGS = "**specs/3672/spec.md**: Tighten the wording\n**agentic_devtools/state.py**: Guard the read"


def _review_body(entries: str, count: int = 2) -> str:
    return (
        f"<details>\n<summary>Comments suppressed due to low confidence ({count})</summary>\n\n{entries}\n\n</details>"
    )


class _FakeProvider:
    """Minimal provider recording the calls the deferral path makes.

    Duck-typed rather than a :class:`CIPlatformProvider` subclass: the deferral path
    touches seven of its methods, and implementing the remaining abstract surface
    would bury the scenarios under stubs.
    """

    def __init__(self, *, linked_issue_labels: list[str] | None = None) -> None:
        self.comments: list[IssueCommentInfo] = []
        self.linked_issue_labels = linked_issue_labels or []
        self.created_issues: list[dict] = []
        self.dispatched: list[dict] = []
        self.repair_dispatches: list[dict] = []
        self.approved: bool = False
        self._next_comment_id = 1

    # --- comment plumbing used by the real deferral marker code ---
    def list_issue_comments(self, pr_number: int) -> list[IssueCommentInfo]:
        return list(self.comments)

    def post_comment(self, pr_number: int, body: str) -> None:
        self.comments.append(
            IssueCommentInfo(id=self._next_comment_id, author="github-actions[bot]", body=body),
        )
        self._next_comment_id += 1

    def find_comment(self, pr_number: int, marker: str) -> tuple[int, str] | None:
        for comment in reversed(self.comments):
            if marker in comment.body:
                return (comment.id, comment.body)
        return None

    def update_comment(self, comment_id: int, body: str) -> None:
        for index, comment in enumerate(self.comments):
            if comment.id == comment_id:
                self.comments[index] = IssueCommentInfo(id=comment.id, author=comment.author, body=body)
                return
        raise AssertionError(f"comment {comment_id} not found")

    # --- deferral preconditions ---
    def list_all_review_comments(self, pr_number: int) -> list:
        return []

    def count_open_issues_with_label(self, label: str) -> int:
        return 0

    def list_linked_issue_labels(self, pr_number: int) -> list[str]:
        return list(self.linked_issue_labels)

    def find_deferral_issue(self, *, pr_number: int, review_id: int) -> int | None:
        for issue in self.created_issues:
            if issue["pr_number"] == pr_number and issue["review_id"] == review_id:
                return DEFERRAL_ISSUE
        return None

    # --- deferral side effects ---
    def create_deferral_issue(
        self,
        *,
        pr_number: int,
        review_id: int,
        base_sha: str,
        findings: list[tuple[str, str]],
        labels: list[str],
    ) -> int:
        self.created_issues.append(
            {
                "pr_number": pr_number,
                "review_id": review_id,
                "base_sha": base_sha,
                "findings": list(findings),
                "labels": list(labels),
            },
        )
        return DEFERRAL_ISSUE

    def dispatch_suppressed_triage(self, *, issue_number: int, pr_number: int, review_id: int) -> None:
        self.dispatched.append({"issue": issue_number, "pr": pr_number, "review": review_id})

    def approve_pr(self, pr_number: int, head_sha: str, body: str) -> bool:
        self.approved = True
        return True

    def list_review_comments(self, pr_number: int, review_id: int) -> list:
        return []

    def dispatch_repair(
        self,
        *,
        pr_number: int,
        head_sha: str,
        repair_type: str,
        failed_checks: list,
        review_comments: list,
        review_id: int,
        declared_author_comment_count: int = 0,
        declared_author_comment_counts_by_review: dict[int, int] | None = None,
    ) -> int:
        self.repair_dispatches.append(
            {
                "pr_number": pr_number,
                "head_sha": head_sha,
                "repair_type": repair_type,
                "failed_checks": list(failed_checks),
                "review_comments": list(review_comments),
                "review_id": review_id,
                "declared_author_comment_count": declared_author_comment_count,
                "declared_author_comment_counts_by_review": declared_author_comment_counts_by_review or {},
            }
        )
        marker = f"<!-- copilot-trigger:{review_id}:2026-08-15T00:00:00+00:00 -->"
        self.post_comment(pr_number, marker)
        return self._next_comment_id - 1

    # --- merge plumbing for MergeAction dispatch tests ---
    def merge_pr(self, pr_number: int, head_sha: str, method: str, **kwargs: object) -> None:
        pass

    def delete_branch(self, branch: str) -> None:
        pass


def _snapshot(
    *,
    entries: str = SPECS_FINDINGS,
    files: list[str] | None = None,
    labels: list[str] | None = None,
) -> PRStateSnapshot:
    return PRStateSnapshot(
        pr_number=PR_NUMBER,
        head_sha=HEAD_SHA,
        ci_status="passing",
        copilot_review_id=REVIEW_ID,
        labels=labels if labels is not None else ["ai-auto-merge-allowed"],
        files=files if files is not None else ["specs/3672/spec.md", "specs/3672/plan.md"],
        reviews=[
            ReviewInfo(
                id=REVIEW_ID,
                user=COPILOT_REVIEWER_LOGIN,
                state="COMMENTED",
                body=_review_body(entries),
                commit_sha=HEAD_SHA,
            ),
        ],
        copilot_gate_verdict=CopilotGateVerdict(
            passed=False,
            reason=REASON_SUPPRESSED_COMMENTS,
            review_id=REVIEW_ID,
            body_comment_count=0,
            suppressed_count=2,
        ),
    )


def _as_provider(provider: _FakeProvider) -> CIPlatformProvider:
    """Narrow the duck-typed fake to the provider protocol the actions expect."""
    return cast(CIPlatformProvider, provider)


def _run_defer(provider: _FakeProvider, snapshot: PRStateSnapshot) -> tuple[ActionDecision, DerivedState]:
    """Run ``DeferSuppressedAction`` end to end, honouring its evaluate gate."""
    action = DeferSuppressedAction()
    derived = DerivedState(snapshot)
    evaluation = action.evaluate(snapshot, derived)
    if evaluation.decision != ActionDecision.EXECUTE:
        return evaluation.decision, derived
    return action.execute(_as_provider(provider), snapshot, derived).decision, derived


@pytest.fixture(autouse=True)
def _enable_feature(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ENABLE_SUPPRESSED_DEFERRAL", "true")


class TestSpecsOnlyRoundIsDeferredAndMerges:
    """Scenario 1 — specs-only suppressed-only round reaches merge."""

    def test_files_the_issue_records_the_marker_and_opens_the_gate(self) -> None:
        provider = _FakeProvider()
        snapshot = _snapshot()

        decision, derived = _run_defer(provider, snapshot)

        assert decision == ActionDecision.EXECUTE
        assert provider.created_issues[0]["findings"] == [
            ("specs/3672/spec.md", "Tighten the wording"),
            ("specs/3672/plan.md", "Add a rollout note"),
        ]
        # The parent PR carried the auto-merge label, so the follow-up inherits it.
        assert provider.created_issues[0]["labels"] == [
            SUPPRESSED_FOLLOW_UP_LABEL,
            "ai-auto-merge-allowed",
        ]
        # Dispatch does NOT happen yet — it is deferred to MergeAction so the triage
        # agent runs against the merged tree, not a pre-merge main.
        assert provider.dispatched == []
        # The issue number and review ID are forwarded in derived state for MergeAction.
        assert derived.get("suppressed_deferral_issue_number") == DEFERRAL_ISSUE
        assert derived.get("suppressed_deferral_review_id") == REVIEW_ID

        # The durable marker is on the PR and readable by a later pipeline run.
        assert any(SUPPRESSED_DEFERRAL_SENTINEL in comment.body for comment in provider.comments)
        assert read_active_suppressed_deferral(_as_provider(provider), PR_NUMBER, REVIEW_ID) is not None

        # Repair dispatch stands down, and the approve/merge gate opens.
        repair = DispatchRepairAction().execute(_as_provider(provider), snapshot, derived)
        assert repair.decision == ActionDecision.SKIP
        assert copilot_review_gate_passed(
            snapshot,
            unresolved_threads=derived.unresolved_threads,
            deferred_review_id=derived.get("suppressed_deferral_review_id"),
        )

    def test_never_generates_a_second_deferral_for_the_same_review(self) -> None:
        provider = _FakeProvider()
        snapshot = _snapshot()

        _run_defer(provider, snapshot)
        # A later pipeline run reads the recorded marker off the snapshot.
        second_snapshot = replace(_snapshot(), suppressed_deferral_review_id=REVIEW_ID)
        decision, _derived = _run_defer(provider, second_snapshot)

        assert decision == ActionDecision.SKIP
        assert len(provider.created_issues) == 1

    def test_failed_marker_post_is_retried_against_the_same_issue(self) -> None:
        """A crash between issue creation and marker post must not manufacture a duplicate."""
        provider = _FakeProvider()
        snapshot = _snapshot()

        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.defer_suppressed.post_suppressed_deferral_marker",
            return_value=False,
        ):
            decision, _derived = _run_defer(provider, snapshot)
        assert decision == ActionDecision.FAILED
        assert len(provider.created_issues) == 1
        assert read_active_suppressed_deferral(_as_provider(provider), PR_NUMBER, REVIEW_ID) is None

        # The next run recovers the orphaned issue rather than filing a second one.
        decision, derived = _run_defer(provider, snapshot)

        assert decision == ActionDecision.EXECUTE
        assert len(provider.created_issues) == 1
        assert derived.get("suppressed_deferral_issue_number") == DEFERRAL_ISSUE
        assert read_active_suppressed_deferral(_as_provider(provider), PR_NUMBER, REVIEW_ID) is not None

    def test_disabled_flag_leaves_the_gate_closed(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ENABLE_SUPPRESSED_DEFERRAL", "false")
        provider = _FakeProvider()
        snapshot = _snapshot()

        decision, derived = _run_defer(provider, snapshot)

        assert decision == ActionDecision.SKIP
        assert provider.created_issues == []
        assert not copilot_review_gate_passed(
            snapshot,
            unresolved_threads=derived.unresolved_threads,
            deferred_review_id=derived.get("suppressed_deferral_review_id"),
        )


class TestExecutableEvidenceFallsBackToRepair:
    """Scenarios 2 and 3 — any executable evidence keeps the repair round."""

    def test_executable_suppressed_entry_is_not_deferred(self) -> None:
        provider = _FakeProvider()
        snapshot = _snapshot(entries=EXECUTABLE_FINDINGS)

        decision, derived = _run_defer(provider, snapshot)

        assert decision == ActionDecision.SKIP
        assert provider.created_issues == []
        assert read_active_suppressed_deferral(_as_provider(provider), PR_NUMBER, REVIEW_ID) is None
        assert not copilot_review_gate_passed(
            snapshot,
            unresolved_threads=derived.unresolved_threads,
            deferred_review_id=derived.get("suppressed_deferral_review_id"),
        )

    def test_executable_file_in_the_pr_api_diff_is_not_deferred(self) -> None:
        provider = _FakeProvider()
        # Every recovered finding is specs-only, but the PR itself touches code —
        # condition 10 reads the PR API file list, not the finding paths.
        snapshot = _snapshot(files=["specs/3672/spec.md", "agentic_devtools/state.py"])

        decision, derived = _run_defer(provider, snapshot)

        assert decision == ActionDecision.SKIP
        assert provider.created_issues == []
        assert not copilot_review_gate_passed(
            snapshot,
            unresolved_threads=derived.unresolved_threads,
            deferred_review_id=derived.get("suppressed_deferral_review_id"),
        )


class TestFollowUpPrIsNeverDeferredAgain:
    """Scenario 4 — the one-generation cap holds on both sides of the link."""

    def test_labelled_follow_up_pr_is_not_deferred(self) -> None:
        provider = _FakeProvider()
        snapshot = _snapshot(labels=[SUPPRESSED_FOLLOW_UP_LABEL, "ai-auto-merge-allowed"])

        decision, _derived = _run_defer(provider, snapshot)

        assert decision == ActionDecision.SKIP
        assert provider.created_issues == []

    def test_pr_linked_to_a_deferral_issue_is_not_deferred(self) -> None:
        provider = _FakeProvider(linked_issue_labels=[SUPPRESSED_FOLLOW_UP_LABEL])
        snapshot = _snapshot()

        decision, _derived = _run_defer(provider, snapshot)

        assert decision == ActionDecision.SKIP
        assert provider.created_issues == []
        assert read_active_suppressed_deferral(_as_provider(provider), PR_NUMBER, REVIEW_ID) is None


class TestPipelineRunnerIntegration:
    """Verify action ordering and same-run derived-state propagation via run_pipeline.

    These tests exercise the configured sequence
    [DeferSuppressedAction, DispatchRepairAction, ApproveAction, MergeAction] through
    the real pipeline runner so that a misordered or missing action would be detected.
    """

    def test_specs_only_round_skips_repair_approves_and_merges(self) -> None:
        """Scenario 1 via the pipeline runner.

        DeferSuppressedAction files the issue and posts the marker (EXECUTE);
        DispatchRepairAction reads the same-run marker and skips (SKIP);
        ApproveAction sees the derived suppressed_deferral_review_id gate and
        executes (EXECUTE);
        MergeAction sees the same-run approval and the deferral marker and merges
        (EXECUTE), proving the full deferral → approve → merge path works end-to-end.
        """
        from agentic_devtools.cli.ci.pipeline.actions import ApproveAction, MergeAction
        from agentic_devtools.cli.ci.pipeline.runner import run_pipeline

        provider = _FakeProvider()
        snapshot = _snapshot()

        summary = run_pipeline(
            _as_provider(provider),
            snapshot,
            [DeferSuppressedAction(), DispatchRepairAction(), ApproveAction(), MergeAction()],
        )

        decisions = {r.name: r.decision for r in summary.results}
        assert decisions["defer_suppressed"] == ActionDecision.EXECUTE, summary.results
        # DispatchRepairAction must skip via the deferral marker — not proceed to repair.
        assert decisions["dispatch_repair"] == ActionDecision.SKIP, summary.results
        # ApproveAction must reach execute: the gate was cleared by the deferral marker
        # recorded in derived state by DeferSuppressedAction in the same run.
        assert decisions["approve"] == ActionDecision.EXECUTE, summary.results
        assert provider.approved, "approve_pr was not called"
        # MergeAction must also execute: same-run approval + deferral marker clear the gate.
        assert decisions["merge"] == ActionDecision.EXECUTE, summary.results

    def test_executable_entry_pipeline_does_not_defer_and_blocks_approve_and_merge(self) -> None:
        """Scenario 2 via the pipeline runner.

        DeferSuppressedAction is skipped (executable entry in findings);
        DispatchRepairAction proceeds without the deferral bypass (must NOT be SKIP
        due to a false deferral);
        ApproveAction is skipped because the review gate is still closed;
        MergeAction is skipped because no approval was recorded (proving the
        executable-entry path never reaches merge).
        """
        from agentic_devtools.cli.ci.pipeline.actions import ApproveAction, MergeAction
        from agentic_devtools.cli.ci.pipeline.runner import run_pipeline

        provider = _FakeProvider()
        snapshot = _snapshot(entries=EXECUTABLE_FINDINGS)

        summary = run_pipeline(
            _as_provider(provider),
            snapshot,
            [DeferSuppressedAction(), DispatchRepairAction(), ApproveAction(), MergeAction()],
        )

        decisions = {r.name: r.decision for r in summary.results}
        assert decisions["defer_suppressed"] == ActionDecision.SKIP, summary.results
        # The critical invariant: DispatchRepairAction must take the real dispatch
        # path rather than skipping behind a false deferral marker.
        assert decisions["dispatch_repair"] == ActionDecision.EXECUTE, summary.results
        assert provider.repair_dispatches == [
            {
                "pr_number": PR_NUMBER,
                "head_sha": HEAD_SHA,
                "repair_type": "review",
                "failed_checks": [],
                "review_comments": [],
                "review_id": REVIEW_ID,
                "declared_author_comment_count": 2,
                "declared_author_comment_counts_by_review": {REVIEW_ID: 2},
            }
        ]
        # No false deferral means the gate stays closed and approve is skipped.
        assert decisions["approve"] == ActionDecision.SKIP, summary.results
        assert not provider.approved
        # Without approval, merge must also be skipped.
        assert decisions["merge"] == ActionDecision.SKIP, summary.results


class TestMergeActionDispatchesTriage:
    """Triage dispatch happens in MergeAction after a successful merge.

    DeferSuppressedAction defers the triage agent dispatch so that it runs
    against the merged tree, not a pre-merge main.  MergeAction reads the
    ``suppressed_deferral_issue_number`` / ``suppressed_deferral_review_id``
    derived keys and dispatches immediately after the merge succeeds.
    """

    def test_dispatch_fires_after_merge_when_keys_are_set(self) -> None:
        from agentic_devtools.cli.ci.pipeline.actions import MergeAction

        provider = _FakeProvider()
        snapshot = _snapshot()
        derived = DerivedState(snapshot)
        # Simulate the keys DeferSuppressedAction records.
        derived.set("suppressed_deferral_issue_number", DEFERRAL_ISSUE)
        derived.set("suppressed_deferral_review_id", REVIEW_ID)

        result = MergeAction().execute(_as_provider(provider), snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        assert provider.dispatched == [{"issue": DEFERRAL_ISSUE, "pr": PR_NUMBER, "review": REVIEW_ID}]

    def test_no_dispatch_when_keys_absent(self) -> None:
        from agentic_devtools.cli.ci.pipeline.actions import MergeAction

        provider = _FakeProvider()
        snapshot = _snapshot()
        derived = DerivedState(snapshot)
        # No deferral keys — normal (non-deferred) merge.

        result = MergeAction().execute(_as_provider(provider), snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        assert provider.dispatched == []

    def test_dispatch_failure_fails_merge(self) -> None:
        from agentic_devtools.cli.ci.pipeline.actions import MergeAction

        class _FailDispatchProvider(_FakeProvider):
            def dispatch_suppressed_triage(self, *, issue_number: int, pr_number: int, review_id: int) -> None:
                raise RuntimeError("SPECKIT_PR_TOKEN not set")

        provider = _FailDispatchProvider()
        snapshot = _snapshot()
        derived = DerivedState(snapshot)
        derived.set("suppressed_deferral_issue_number", DEFERRAL_ISSUE)
        derived.set("suppressed_deferral_review_id", REVIEW_ID)

        result = MergeAction().execute(_as_provider(provider), snapshot, derived)

        # Dispatch failure returns FAILED so the pipeline run records the failure
        # faithfully.  On a re-trigger the snapshot will carry
        # mergeable_state="merged"; the execute path detects this, skips
        # merge_pr, and retries dispatch directly.
        assert result.decision == ActionDecision.FAILED
