"""Tests for SquashAction."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.models import SquashResult
from agentic_devtools.cli.ci.pipeline.actions.squash import SquashAction
from agentic_devtools.cli.ci.pipeline.gate_verdict import (
    REASON_CLEAN,
    REASON_HAS_COMMENTS,
    REASON_SUPPRESSED_COMMENTS,
    CopilotGateVerdict,
)
from agentic_devtools.cli.ci.pipeline.models import ActionDecision
from agentic_devtools.cli.ci.pipeline.snapshot import DerivedState, PRStateSnapshot
from agentic_devtools.cli.ci.retry import ProviderRateLimitError


class TestSquashAction:
    """Tests for squash action evaluation."""

    def test_skip_when_review_gate_has_not_passed(self) -> None:
        """Repair commits accumulate until the Copilot review gate passes."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            commit_count=3,
            ci_status="passing",
            copilot_gate_verdict=CopilotGateVerdict(
                passed=False,
                reason=REASON_HAS_COMMENTS,
                review_id=7,
                body_comment_count=2,
            ),
        )
        derived = DerivedState(snapshot)
        action = SquashAction()
        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.squash.is_copilot_session_active_via_agent_task",
            return_value=False,
        ):
            result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["review_clean"] is False
        assert "3 commits retained" in result.details
        assert "review gate passes" in result.details

    def test_skip_when_no_review_exists_yet(self) -> None:
        """A PR that has never been reviewed is not merge-ready — squash is deferred."""
        snapshot = PRStateSnapshot(pr_number=1, commit_count=3, ci_status="passing")
        derived = DerivedState(snapshot)
        action = SquashAction()
        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.squash.is_copilot_session_active_via_agent_task",
            return_value=False,
        ):
            result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["review_clean"] is False

    def test_execute_when_gate_verdict_passed(self) -> None:
        """Once the review gate passes, the accumulated commits are squashed."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            commit_count=3,
            ci_status="passing",
            copilot_gate_verdict=CopilotGateVerdict(passed=True, reason=REASON_CLEAN),
        )
        derived = DerivedState(snapshot)
        action = SquashAction()
        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.squash.is_copilot_session_active_via_agent_task",
            return_value=False,
        ):
            result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["review_clean"] is True

    def test_execute_when_suppressed_only_block_was_evaluated(self) -> None:
        """The squash gate honours the same suppressed-only bypass as approve/merge."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            commit_count=3,
            ci_status="passing",
            repair_satisfied_review_id=42,
            head_changed_since_review=False,
            copilot_gate_verdict=CopilotGateVerdict(
                passed=False,
                reason=REASON_SUPPRESSED_COMMENTS,
                review_id=42,
                body_comment_count=0,
                suppressed_count=2,
            ),
        )
        derived = DerivedState(snapshot)
        action = SquashAction()
        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.squash.is_copilot_session_active_via_agent_task",
            return_value=False,
        ):
            result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["review_clean"] is True

    def test_skip_when_single_commit_short_circuits_before_review_gate(self) -> None:
        """The cheap structural check still short-circuits before the review gate."""
        snapshot = PRStateSnapshot(pr_number=1, commit_count=1, ci_status="passing")
        derived = DerivedState(snapshot)
        action = SquashAction()
        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.squash.is_copilot_session_active_via_agent_task",
            return_value=False,
        ):
            result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "review_clean" not in result.preconditions

    def test_skip_when_single_commit(self) -> None:
        snapshot = PRStateSnapshot(pr_number=1, commit_count=1, ci_status="passing")
        derived = DerivedState(snapshot)
        action = SquashAction()
        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.squash.is_copilot_session_active_via_agent_task",
            return_value=False,
        ):
            result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "1 commit" in result.details

    def test_skip_when_active_session(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            commit_count=3,
            ci_status="passing",
            review_state="APPROVED",
            base_repo_full_name="owner/repo",
        )
        derived = DerivedState(snapshot)
        action = SquashAction()
        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.squash.is_copilot_session_active_via_agent_task",
            return_value=True,
        ) as mock_detector:
            result = action.evaluate(snapshot, derived)
            mock_detector.assert_called_once_with("owner/repo", 1)
        assert result.decision == ActionDecision.SKIP
        assert "active" in result.details.lower()

    def test_skip_when_repair_dispatched(self) -> None:
        snapshot = PRStateSnapshot(pr_number=1, commit_count=3, ci_status="passing", review_state="APPROVED")
        derived = DerivedState(snapshot)
        derived.set("repair_dispatched", True)
        action = SquashAction()
        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.squash.is_copilot_session_active_via_agent_task",
            return_value=False,
        ):
            result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "repair dispatched" in result.details.lower()

    def test_skip_when_unresolved_threads_remain(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            commit_count=3,
            ci_status="passing",
            review_state="APPROVED",
            unresolved_threads=2,
            repairable_threads=2,
        )
        derived = DerivedState(snapshot)
        action = SquashAction()
        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.squash.is_copilot_session_active_via_agent_task",
            return_value=False,
        ):
            result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["all_threads_resolved"] is False
        assert "unresolved_threads" in result.details

    def test_execute_when_unresolved_threads_zero(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            commit_count=3,
            ci_status="passing",
            review_state="APPROVED",
            unresolved_threads=0,
            repairable_threads=0,
        )
        derived = DerivedState(snapshot)
        action = SquashAction()
        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.squash.is_copilot_session_active_via_agent_task",
            return_value=False,
        ):
            result = action.evaluate(snapshot, derived)
        assert result.preconditions["all_threads_resolved"] is True
        assert result.decision == ActionDecision.EXECUTE

    def test_execute_when_derived_unresolved_threads_override_is_zero(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            commit_count=3,
            ci_status="passing",
            review_state="APPROVED",
            unresolved_threads=3,
            repairable_threads=3,
        )
        derived = DerivedState(snapshot)
        derived.set("unresolved_threads", 0)
        action = SquashAction()
        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.squash.is_copilot_session_active_via_agent_task",
            return_value=False,
        ):
            result = action.evaluate(snapshot, derived)
        assert result.preconditions["all_threads_resolved"] is True
        assert result.decision == ActionDecision.EXECUTE

    def test_execute_when_multiple_commits(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            commit_count=3,
            ci_status="passing",
            review_state="APPROVED",
            copilot_review_pending=False,
        )
        derived = DerivedState(snapshot)
        action = SquashAction()
        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.squash.is_copilot_session_active_via_agent_task",
            return_value=False,
        ):
            result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE

    def test_skip_when_ci_pending(self) -> None:
        snapshot = PRStateSnapshot(pr_number=1, commit_count=3, ci_status="pending", review_state="APPROVED")
        derived = DerivedState(snapshot)
        action = SquashAction()
        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.squash.is_copilot_session_active_via_agent_task",
            return_value=False,
        ):
            result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "ci is pending" in result.details.lower()

    def test_skip_when_ci_failing(self) -> None:
        snapshot = PRStateSnapshot(pr_number=1, commit_count=3, ci_status="failing", review_state="APPROVED")
        derived = DerivedState(snapshot)
        action = SquashAction()
        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.squash.is_copilot_session_active_via_agent_task",
            return_value=False,
        ):
            result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "ci is failing" in result.details.lower()

    def test_execute_when_derived_pending_review_is_true(self) -> None:
        """Pending review does NOT block squash — only active session does."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            commit_count=3,
            ci_status="passing",
            review_state="APPROVED",
            copilot_review_pending=False,
        )
        derived = DerivedState(snapshot)
        derived.set("copilot_review_pending", True)
        action = SquashAction()
        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.squash.is_copilot_session_active_via_agent_task",
            return_value=False,
        ):
            result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE

    def test_execute_calls_squash(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            commit_count=3,
            head_sha="abc",
            base_branch="main",
            head_branch="feature",
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.squash_post_repair.return_value = SquashResult(before_tree="t1", after_tree="t1")
        action = SquashAction()
        result = action.execute(provider, snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE
        assert result.invalidates_snapshot is True
        provider.squash_post_repair.assert_called_once()
        assert derived.commit_count == 1

    def test_execute_returns_failed_when_squash_raises(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            commit_count=3,
            head_sha="abc",
            base_branch="main",
            head_branch="feature",
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.squash_post_repair.side_effect = RuntimeError("squash failed")
        action = SquashAction()
        result = action.execute(provider, snapshot, derived)
        assert result.decision == ActionDecision.FAILED
        assert result.details == "squash_post_repair failed"
        assert result.error == "squash failed"

    def test_execute_sets_squash_preserved_green_when_tree_preserved_and_green(self) -> None:
        """Tree-preserving squash after green CI sets the run-scoped optimization flag."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            commit_count=3,
            head_sha="abc",
            base_branch="main",
            head_branch="feature",
            ci_status="passing",
            commits_behind=0,
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.squash_post_repair.return_value = SquashResult(
            before_tree="tree1", after_tree="tree1", after_sha="squashed-sha"
        )
        action = SquashAction()
        result = action.execute(provider, snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE
        assert result.invalidates_snapshot is True
        assert derived.get("squash_preserved_green") is True
        assert derived.get("squash_preserved_green_sha") == "squashed-sha"

    def test_execute_does_not_set_flag_when_ci_not_passing(self) -> None:
        """The optimization flag is not set unless pre-squash CI was passing."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            commit_count=3,
            head_sha="abc",
            base_branch="main",
            head_branch="feature",
            ci_status="unknown",
            commits_behind=0,
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.squash_post_repair.return_value = SquashResult(before_tree="tree1", after_tree="tree1")
        action = SquashAction()
        result = action.execute(provider, snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE
        assert derived.get("squash_preserved_green", False) is False

    def test_execute_does_not_set_flag_when_tree_not_preserved(self) -> None:
        """A squash whose actual post-squash tree differs from head_sha's tree — no flag.

        Even when the pre-execution snapshot reported ``commits_behind == 0``, the
        squash may have absorbed a commit pushed during finalization, changing the
        tree. The flag must not be carried onto that newly introduced code.
        """
        snapshot = PRStateSnapshot(
            pr_number=1,
            commit_count=3,
            head_sha="abc",
            base_branch="main",
            head_branch="feature",
            ci_status="passing",
            commits_behind=0,
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.squash_post_repair.return_value = SquashResult(before_tree="tree1", after_tree="tree2")
        action = SquashAction()
        result = action.execute(provider, snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE
        assert derived.get("squash_preserved_green", False) is False

    def test_execute_does_not_set_flag_when_branch_was_behind_base(self) -> None:
        """A behind-base snapshot never reuses prior green CI in the same run."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            commit_count=3,
            head_sha="abc",
            base_branch="main",
            head_branch="feature",
            ci_status="passing",
            commits_behind=1,
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.squash_post_repair.return_value = SquashResult(
            before_tree="tree1", after_tree="tree1", after_sha="squashed-sha"
        )
        action = SquashAction()
        result = action.execute(provider, snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE
        assert derived.get("squash_preserved_green", False) is False

    def test_execute_does_not_set_flag_when_tree_unresolved(self) -> None:
        """When squash_post_repair could not resolve a tree, tree preservation is unproven."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            commit_count=3,
            head_sha="abc",
            base_branch="main",
            head_branch="feature",
            ci_status="passing",
            commits_behind=0,
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.squash_post_repair.return_value = SquashResult(before_tree="", after_tree="")
        action = SquashAction()
        result = action.execute(provider, snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE
        assert derived.get("squash_preserved_green", False) is False

    def test_execute_re_raises_rate_limit_error(self) -> None:
        snapshot = PRStateSnapshot(pr_number=1, commit_count=3, head_sha="abc", base_branch="main", head_branch="f")
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.squash_post_repair.side_effect = ProviderRateLimitError(is_rate_limit=True)

        with pytest.raises(ProviderRateLimitError):
            SquashAction().execute(provider, snapshot, derived)
