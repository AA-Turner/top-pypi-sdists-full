"""Tests for DeferSuppressedAction."""

from __future__ import annotations

import os
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.models import ReviewInfo
from agentic_devtools.cli.ci.pipeline.actions.defer_suppressed import (
    DEFAULT_MAX_OPEN_DEFERRALS,
    FEATURE_FLAG_ENV,
    DeferSuppressedAction,
)
from agentic_devtools.cli.ci.pipeline.gate_verdict import (
    REASON_SUPPRESSED_COMMENTS,
    SUPPRESSED_FOLLOW_UP_LABEL,
    CopilotGateVerdict,
)
from agentic_devtools.cli.ci.pipeline.models import ActionDecision
from agentic_devtools.cli.ci.pipeline.snapshot import DerivedState, PRStateSnapshot
from agentic_devtools.cli.shared.retry import ProviderRateLimitError

REVIEW_BODY = """### Comments suppressed due to low confidence (2)

**specs/3672-deferral/spec.md**

The acceptance criteria are ambiguous here.

**docs/design.md**

Consider clarifying the rollout order.
"""


def _snapshot(
    *,
    suppressed_count: int = 2,
    review_body: str = REVIEW_BODY,
    labels: list[str] | None = None,
    files: list[str] | None = None,
    head_changed_since_review: bool = False,
) -> PRStateSnapshot:
    return PRStateSnapshot(
        pr_number=11,
        head_sha="abc1234",
        labels=labels if labels is not None else ["ai-auto-merge-allowed"],
        files=files if files is not None else ["specs/3672-deferral/spec.md", "docs/design.md"],
        head_changed_since_review=head_changed_since_review,
        reviews=[ReviewInfo(id=42, user="Copilot", state="COMMENTED", body=review_body)],
        copilot_gate_verdict=CopilotGateVerdict(
            passed=False,
            reason=REASON_SUPPRESSED_COMMENTS,
            review_id=42,
            body_comment_count=0,
            suppressed_count=suppressed_count,
        ),
    )


def _provider() -> MagicMock:
    provider = MagicMock()
    provider.list_all_review_comments.return_value = []
    provider.count_open_issues_with_label.return_value = 0
    provider.list_linked_issue_labels.return_value = ["enhancement"]
    provider.find_deferral_issue.return_value = None
    provider.create_deferral_issue.return_value = 4242
    return provider


class TestDeferSuppressedActionName:
    """Tests for the action name."""

    def test_name(self) -> None:
        assert DeferSuppressedAction().name == "defer_suppressed"


class TestDeferSuppressedActionEvaluate:
    """Tests for DeferSuppressedAction.evaluate()."""

    @patch.dict(os.environ, {}, clear=True)
    def test_skips_when_feature_flag_unset(self) -> None:
        snapshot = _snapshot()
        result = DeferSuppressedAction().evaluate(snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["feature_enabled"] is False

    @patch.dict(os.environ, {FEATURE_FLAG_ENV: "true"}, clear=False)
    def test_executes_for_specs_only_suppressed_only_round(self) -> None:
        snapshot = _snapshot()
        result = DeferSuppressedAction().evaluate(snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["snapshot_conditions_met"] is True

    @patch.dict(os.environ, {FEATURE_FLAG_ENV: "true"}, clear=False)
    def test_skips_when_pr_is_not_an_auto_merge_parent(self) -> None:
        snapshot = _snapshot(labels=["enhancement"])
        result = DeferSuppressedAction().evaluate(snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["auto_merge_parent"] is False

    @patch.dict(os.environ, {FEATURE_FLAG_ENV: "true"}, clear=False)
    def test_skips_when_already_deferred(self) -> None:
        snapshot = _snapshot()
        derived = DerivedState(snapshot)
        derived.set("suppressed_deferral_review_id", 42)
        result = DeferSuppressedAction().evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["not_already_deferred"] is False

    @patch.dict(os.environ, {FEATURE_FLAG_ENV: "true"}, clear=False)
    def test_skips_when_executable_file_in_diff(self) -> None:
        snapshot = _snapshot(files=["specs/3672-deferral/spec.md", "agentic_devtools/state.py"])
        result = DeferSuppressedAction().evaluate(snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["snapshot_conditions_met"] is False

    @patch.dict(os.environ, {FEATURE_FLAG_ENV: "true"}, clear=False)
    def test_skips_for_follow_up_pr(self) -> None:
        snapshot = _snapshot(labels=[SUPPRESSED_FOLLOW_UP_LABEL, "ai-auto-merge-allowed"])
        result = DeferSuppressedAction().evaluate(snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["snapshot_conditions_met"] is False

    @patch.dict(os.environ, {FEATURE_FLAG_ENV: "true"}, clear=False)
    def test_skips_when_suppressed_entries_do_not_reconcile(self) -> None:
        snapshot = _snapshot(suppressed_count=3)
        result = DeferSuppressedAction().evaluate(snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.SKIP


class TestDeferSuppressedActionExecute:
    """Tests for DeferSuppressedAction.execute()."""

    def test_creates_issue_posts_marker_and_defers_dispatch_to_merge(self) -> None:
        snapshot = _snapshot()
        derived = DerivedState(snapshot)
        provider = _provider()

        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.defer_suppressed.post_suppressed_deferral_marker",
            return_value=True,
        ) as mock_post:
            result = DeferSuppressedAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        assert "#4242" in result.details
        create_kwargs = provider.create_deferral_issue.call_args.kwargs
        assert create_kwargs["pr_number"] == 11
        assert create_kwargs["review_id"] == 42
        assert create_kwargs["labels"] == [SUPPRESSED_FOLLOW_UP_LABEL, "ai-auto-merge-allowed"]
        assert [path for path, _ in create_kwargs["findings"]] == [
            "specs/3672-deferral/spec.md",
            "docs/design.md",
        ]
        provider.dispatch_suppressed_triage.assert_not_called()
        mock_post.assert_called_once_with(provider, 11, 42, 4242)
        assert derived.get("suppressed_deferral_review_id") == 42
        assert derived.get("suppressed_deferral_issue_number") == 4242

    def test_skips_when_pr_does_not_carry_the_auto_merge_label(self) -> None:
        """Without the label MergeAction never runs, so the issue would never be dispatched."""
        snapshot = _snapshot(labels=["enhancement"])
        provider = _provider()

        result = DeferSuppressedAction().execute(provider, snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["auto_merge_parent"] is False
        provider.create_deferral_issue.assert_not_called()

    def test_reuses_existing_deferral_issue_instead_of_creating_a_duplicate(self) -> None:
        snapshot = _snapshot()
        derived = DerivedState(snapshot)
        provider = _provider()
        provider.find_deferral_issue.return_value = 777

        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.defer_suppressed.post_suppressed_deferral_marker",
            return_value=True,
        ) as mock_post:
            result = DeferSuppressedAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        provider.create_deferral_issue.assert_not_called()
        mock_post.assert_called_once_with(provider, 11, 42, 777)
        assert derived.get("suppressed_deferral_issue_number") == 777

    def test_skips_when_existing_deferral_lookup_fails(self) -> None:
        snapshot = _snapshot()
        provider = _provider()
        provider.find_deferral_issue.side_effect = RuntimeError("search down")

        result = DeferSuppressedAction().execute(provider, snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["existing_deferral_resolved"] is False
        provider.create_deferral_issue.assert_not_called()

    def test_skips_when_prior_executable_posted_finding_exists(self) -> None:
        snapshot = _snapshot()
        provider = _provider()
        provider.list_all_review_comments.return_value = [
            MagicMock(is_suppressed=False, author_login="Copilot", path="agentic_devtools/state.py")
        ]

        result = DeferSuppressedAction().execute(provider, snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.SKIP
        provider.create_deferral_issue.assert_not_called()

    def test_skips_when_linked_issue_carries_follow_up_label(self) -> None:
        snapshot = _snapshot()
        provider = _provider()
        provider.list_linked_issue_labels.return_value = [SUPPRESSED_FOLLOW_UP_LABEL]

        result = DeferSuppressedAction().execute(provider, snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.SKIP
        provider.create_deferral_issue.assert_not_called()

    def test_skips_when_deferral_backlog_is_at_ceiling(self) -> None:
        snapshot = _snapshot()
        provider = _provider()
        provider.count_open_issues_with_label.return_value = 99

        result = DeferSuppressedAction().execute(provider, snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.SKIP

    def test_reuses_orphaned_issue_even_when_backlog_is_at_ceiling(self) -> None:
        """An orphaned (PR, review) issue should be recovered even when the ceiling is met.

        The orphaned issue already counts against the ceiling — requiring capacity
        for a second slot would permanently block recovery.
        """
        snapshot = _snapshot()
        derived = DerivedState(snapshot)
        provider = _provider()
        provider.count_open_issues_with_label.return_value = DEFAULT_MAX_OPEN_DEFERRALS
        provider.find_deferral_issue.return_value = 888  # orphaned issue exists

        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.defer_suppressed.post_suppressed_deferral_marker",
            return_value=True,
        ):
            result = DeferSuppressedAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        provider.create_deferral_issue.assert_not_called()
        assert derived.get("suppressed_deferral_issue_number") == 888

    def test_skips_orphaned_issue_when_prior_executable_posted_finding_now_exists(self) -> None:
        snapshot = _snapshot()
        provider = _provider()
        provider.find_deferral_issue.return_value = 888
        provider.list_all_review_comments.return_value = [
            MagicMock(is_suppressed=False, author_login="Copilot", path="agentic_devtools/state.py")
        ]

        result = DeferSuppressedAction().execute(provider, snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.SKIP
        provider.create_deferral_issue.assert_not_called()

    def test_skips_orphaned_issue_when_follow_up_label_now_exists(self) -> None:
        snapshot = _snapshot()
        provider = _provider()
        provider.find_deferral_issue.return_value = 888
        provider.list_linked_issue_labels.return_value = [SUPPRESSED_FOLLOW_UP_LABEL]

        result = DeferSuppressedAction().execute(provider, snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.SKIP
        provider.create_deferral_issue.assert_not_called()

    def test_skips_orphaned_issue_when_backlog_exceeds_recovered_slot(self) -> None:
        snapshot = _snapshot()
        provider = _provider()
        provider.count_open_issues_with_label.return_value = DEFAULT_MAX_OPEN_DEFERRALS + 1
        provider.find_deferral_issue.return_value = 888

        result = DeferSuppressedAction().execute(provider, snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.SKIP
        provider.create_deferral_issue.assert_not_called()

    def test_skips_when_preconditions_cannot_be_resolved(self) -> None:
        snapshot = _snapshot()
        provider = _provider()
        provider.count_open_issues_with_label.side_effect = RuntimeError("API down")

        result = DeferSuppressedAction().execute(provider, snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["preconditions_resolved"] is False
        provider.create_deferral_issue.assert_not_called()

    def test_fails_when_issue_creation_raises(self) -> None:
        snapshot = _snapshot()
        provider = _provider()
        provider.create_deferral_issue.side_effect = RuntimeError("boom")

        result = DeferSuppressedAction().execute(provider, snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.FAILED
        assert result.error == "boom"

    def test_fails_when_marker_cannot_be_posted(self) -> None:
        snapshot = _snapshot()
        derived = DerivedState(snapshot)
        provider = _provider()

        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.defer_suppressed.post_suppressed_deferral_marker",
            return_value=False,
        ):
            result = DeferSuppressedAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.FAILED
        assert derived.get("suppressed_deferral_review_id") is None

    def test_skips_when_verdict_is_missing(self) -> None:
        snapshot = PRStateSnapshot(pr_number=11)
        result = DeferSuppressedAction().execute(_provider(), snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.SKIP

    def test_rate_limit_error_propagates_from_precondition_lookup(self) -> None:
        """ProviderRateLimitError from provider calls must not be swallowed."""
        snapshot = _snapshot()
        provider = _provider()
        provider.count_open_issues_with_label.side_effect = ProviderRateLimitError(is_rate_limit=True)

        with pytest.raises(ProviderRateLimitError):
            DeferSuppressedAction().execute(provider, snapshot, DerivedState(snapshot))
