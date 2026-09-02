"""Tests for DispatchConflictResolutionAction."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.guards import (
    CONFLICT_REPAIR_ESCALATION_MARKER_PREFIX,
    MAX_CONFLICT_REPAIR_ATTEMPTS,
)
from agentic_devtools.cli.ci.pipeline.actions.dispatch_conflict_resolution import (
    DispatchConflictResolutionAction,
)
from agentic_devtools.cli.ci.pipeline.models import ActionDecision
from agentic_devtools.cli.ci.pipeline.snapshot import DerivedState, PRStateSnapshot
from agentic_devtools.cli.shared.retry import ProviderRateLimitError

_MODULE = "agentic_devtools.cli.ci.pipeline.actions.dispatch_conflict_resolution"
_HEAD = "a" * 40
_BASE = "b" * 40


def _make_snapshot(**kwargs: object) -> PRStateSnapshot:
    defaults: dict[str, object] = {
        "pr_number": 42,
        "head_sha": _HEAD,
        "base_branch": "main",
        "head_branch": "feature/foo",
        "base_repo_full_name": "owner/repo",
    }
    defaults.update(kwargs)
    return PRStateSnapshot(**defaults)  # type: ignore[arg-type]


def _make_provider(*, base_sha: str = _BASE) -> MagicMock:
    provider = MagicMock()
    provider.get_ref_sha.return_value = base_sha
    provider.get_approver_login.return_value = ""
    provider.get_pr_token_login.return_value = "loop-bot"
    provider.list_issue_comments.return_value = []
    provider.find_comment.return_value = None
    provider.dispatch_conflict_repair.return_value = 987
    provider.post_comment.return_value = 654
    provider.post_comment_as_pr_token.return_value = 654
    return provider


class TestDispatchConflictResolutionActionName:
    """Tests for the action identity."""

    def test_name(self) -> None:
        """The action reports its pipeline name."""
        assert DispatchConflictResolutionAction().name == "dispatch_conflict_resolution"

    def test_does_not_run_after_invalidation(self) -> None:
        """The action must not run against a stale snapshot after HEAD changed."""
        assert getattr(DispatchConflictResolutionAction(), "runs_after_invalidation", False) is False


class TestDispatchConflictResolutionActionEvaluate:
    """Tests for evaluate()."""

    def test_skips_when_no_conflict_signal(self) -> None:
        """No rebase conflict and a clean mergeable_state → skip."""
        snapshot = _make_snapshot(mergeable_state="clean")
        derived = DerivedState(snapshot)

        result = DispatchConflictResolutionAction().evaluate(snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["merge_conflict_detected"] is False
        assert "no merge conflict" in result.details.lower()

    def test_executes_on_rebase_conflict_signal(self) -> None:
        """The derived rebase_conflict flag triggers dispatch."""
        snapshot = _make_snapshot()
        derived = DerivedState(snapshot)
        derived.set("rebase_conflict", True)

        with patch(f"{_MODULE}.is_copilot_session_active_via_agent_task", return_value=False):
            result = DispatchConflictResolutionAction().evaluate(snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["merge_conflict_detected"] is True

    def test_executes_on_dirty_mergeable_state(self) -> None:
        """A provider-reported dirty mergeable_state triggers dispatch."""
        snapshot = _make_snapshot(mergeable_state="DIRTY")
        derived = DerivedState(snapshot)

        with patch(f"{_MODULE}.is_copilot_session_active_via_agent_task", return_value=False):
            result = DispatchConflictResolutionAction().evaluate(snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE

    def test_skips_when_repair_already_dispatched(self) -> None:
        """A CI/review repair dispatched in this run defers conflict repair."""
        snapshot = _make_snapshot(mergeable_state="dirty")
        derived = DerivedState(snapshot)
        derived.set("repair_dispatched", True)

        result = DispatchConflictResolutionAction().evaluate(snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["no_repair_dispatched"] is False

    def test_skips_when_copilot_session_active(self) -> None:
        """An in-flight Copilot session defers conflict repair."""
        snapshot = _make_snapshot(mergeable_state="dirty")
        derived = DerivedState(snapshot)

        with patch(f"{_MODULE}.is_copilot_session_active_via_agent_task", return_value=True):
            result = DispatchConflictResolutionAction().evaluate(snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["no_active_session"] is False
        assert derived.get("repair_dispatched", False) is True


class TestDispatchConflictResolutionActionExecute:
    """Tests for execute()."""

    def test_dispatches_conflict_repair(self) -> None:
        """A first conflict dispatch posts the @copilot comment."""
        snapshot = _make_snapshot(mergeable_state="dirty")
        derived = DerivedState(snapshot)
        provider = _make_provider()

        with patch(f"{_MODULE}.should_dispatch_conflict_repair", return_value=True) as should_dispatch:
            result = DispatchConflictResolutionAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        should_dispatch.assert_called_once_with(provider, 42, _HEAD, _BASE, dispatch_login="loop-bot")
        provider.dispatch_conflict_repair.assert_called_once_with(
            pr_number=42,
            head_sha=_HEAD,
            base_sha=_BASE,
            base_branch="main",
            head_branch="feature/foo",
        )
        assert derived.get("repair_dispatched", False) is True
        assert "987" in result.details

    def test_skips_when_base_sha_unresolved(self) -> None:
        """An unresolvable base SHA fails closed (no unmarked dispatch)."""
        snapshot = _make_snapshot(mergeable_state="dirty")
        derived = DerivedState(snapshot)
        provider = _make_provider(base_sha="")

        result = DispatchConflictResolutionAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        provider.dispatch_conflict_repair.assert_not_called()
        assert "base branch sha" in result.details.lower()
        assert derived.get("repair_dispatched", False) is True

    def test_skips_when_base_sha_lookup_raises(self) -> None:
        """A provider error while resolving the base SHA fails closed."""
        snapshot = _make_snapshot(mergeable_state="dirty")
        derived = DerivedState(snapshot)
        provider = _make_provider()
        provider.get_ref_sha.side_effect = RuntimeError("boom")

        result = DispatchConflictResolutionAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        provider.dispatch_conflict_repair.assert_not_called()

    def test_skips_when_attempt_count_lookup_raises(self) -> None:
        """An unknown attempt count fails closed rather than risking unbounded retries."""
        snapshot = _make_snapshot(mergeable_state="dirty")
        derived = DerivedState(snapshot)
        provider = _make_provider()

        with patch(f"{_MODULE}.count_conflict_repair_dispatches", side_effect=RuntimeError("boom")):
            result = DispatchConflictResolutionAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        provider.dispatch_conflict_repair.assert_not_called()

    def test_skips_when_pr_token_login_raises(self) -> None:
        """A failure to resolve the dispatch identity fails closed."""
        snapshot = _make_snapshot(mergeable_state="dirty")
        derived = DerivedState(snapshot)
        provider = _make_provider()
        provider.get_pr_token_login.side_effect = RuntimeError("auth unavailable")

        result = DispatchConflictResolutionAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        assert "pr-token login unavailable" in result.details.lower()
        provider.dispatch_conflict_repair.assert_not_called()

    def test_skips_when_pr_token_login_is_empty(self) -> None:
        """An empty PR-token login fails closed — cannot authenticate dispatch identity."""
        snapshot = _make_snapshot(mergeable_state="dirty")
        derived = DerivedState(snapshot)
        provider = _make_provider()
        provider.get_pr_token_login.return_value = ""

        result = DispatchConflictResolutionAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        assert "pr-token login unavailable" in result.details.lower()
        provider.dispatch_conflict_repair.assert_not_called()

    def test_skips_when_dedup_marker_is_fresh(self) -> None:
        """An in-TTL marker for the same head+base suppresses re-dispatch."""
        snapshot = _make_snapshot(mergeable_state="dirty")
        derived = DerivedState(snapshot)
        provider = _make_provider()

        with patch(f"{_MODULE}.should_dispatch_conflict_repair", return_value=False):
            result = DispatchConflictResolutionAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        provider.dispatch_conflict_repair.assert_not_called()
        assert "already dispatched" in result.details.lower()
        assert derived.get("repair_dispatched", False) is True

    def test_skips_when_dedup_check_raises(self) -> None:
        """A failing dedup lookup fails closed."""
        snapshot = _make_snapshot(mergeable_state="dirty")
        derived = DerivedState(snapshot)
        provider = _make_provider()

        with patch(f"{_MODULE}.should_dispatch_conflict_repair", side_effect=RuntimeError("boom")):
            result = DispatchConflictResolutionAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        provider.dispatch_conflict_repair.assert_not_called()

    def test_returns_failed_when_dispatch_raises(self) -> None:
        """A dispatch error surfaces as FAILED."""
        snapshot = _make_snapshot(mergeable_state="dirty")
        derived = DerivedState(snapshot)
        provider = _make_provider()
        provider.dispatch_conflict_repair.side_effect = RuntimeError("no token")

        with patch(f"{_MODULE}.should_dispatch_conflict_repair", return_value=True):
            result = DispatchConflictResolutionAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.FAILED
        assert result.error == "no token"
        assert derived.get("repair_dispatched", False) is True

    def test_rate_limit_error_propagates_from_base_sha_lookup(self) -> None:
        """ProviderRateLimitError from get_ref_sha must not be swallowed."""
        snapshot = _make_snapshot(mergeable_state="dirty")
        derived = DerivedState(snapshot)
        provider = _make_provider()
        provider.get_ref_sha.side_effect = ProviderRateLimitError(is_rate_limit=True)

        with pytest.raises(ProviderRateLimitError):
            DispatchConflictResolutionAction().execute(provider, snapshot, derived)


class TestDispatchConflictResolutionActionEscalation:
    """Tests for the bounded-retry escalation path."""

    def test_escalates_after_attempt_budget_exhausted(self) -> None:
        """Reaching the attempt cap posts a human-attention comment and blocks."""
        snapshot = _make_snapshot(mergeable_state="dirty")
        derived = DerivedState(snapshot)
        provider = _make_provider()

        with patch(f"{_MODULE}.count_conflict_repair_dispatches", return_value=MAX_CONFLICT_REPAIR_ATTEMPTS):
            result = DispatchConflictResolutionAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.BLOCKED
        assert result.limit_reached is True
        assert derived.get("repair_dispatched", False) is True
        provider.dispatch_conflict_repair.assert_not_called()
        provider.post_comment_as_pr_token.assert_called_once()
        body = provider.post_comment_as_pr_token.call_args.args[1]
        assert body.startswith(f"{CONFLICT_REPAIR_ESCALATION_MARKER_PREFIX}{_HEAD} -->")
        assert "@copilot" not in body

    def test_escalation_comment_is_posted_once_per_head(self) -> None:
        """An existing escalation marker for this HEAD is not duplicated."""
        from agentic_devtools.cli.ci.guards import build_conflict_repair_escalation_marker
        from agentic_devtools.cli.ci.models import IssueCommentInfo

        snapshot = _make_snapshot(mergeable_state="dirty")
        derived = DerivedState(snapshot)
        provider = _make_provider()
        existing_marker = build_conflict_repair_escalation_marker(head_sha=snapshot.head_sha)
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(id=5, author="loop-bot", body=f"{existing_marker}\nalready escalated"),
        ]

        with patch(f"{_MODULE}.count_conflict_repair_dispatches", return_value=MAX_CONFLICT_REPAIR_ATTEMPTS + 1):
            result = DispatchConflictResolutionAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.BLOCKED
        assert result.limit_reached is True
        provider.post_comment_as_pr_token.assert_not_called()

    def test_escalation_comment_failure_is_non_fatal(self) -> None:
        """A failure to post the escalation notice still blocks the loop."""
        snapshot = _make_snapshot(mergeable_state="dirty")
        derived = DerivedState(snapshot)
        provider = _make_provider()
        provider.post_comment_as_pr_token.side_effect = RuntimeError("comment failed")

        with patch(f"{_MODULE}.count_conflict_repair_dispatches", return_value=MAX_CONFLICT_REPAIR_ATTEMPTS):
            result = DispatchConflictResolutionAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.BLOCKED
        assert result.limit_reached is True
